"""
Main entry point for PML to SMV compiler
"""

import sys
import os
import re

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to use ANTLR-generated parser, fall back to simple parser
try:
    from antlr4 import *
    from grammar.PromelaLexer import PromelaLexer
    from grammar.PromelaParser import PromelaParser
    from grammar.PromelaVisitor import PromelaVisitor
    from antlr4.tree.Tree import TerminalNode
    USE_ANTLR = True
except ImportError:
    USE_ANTLR = False

from src.ast_nodes import *
from src.simple_parser import parse_promela_file
from src.inline_expander import InlineExpander
from src.smv_generator import SMVGenerator
from src.preprocessor import PromelaPreprocessor


if USE_ANTLR:
    class PromelaASTBuilder(PromelaVisitor):
        """Visitor to build AST from parse tree"""
        
        def __init__(self):
            self.program = Program()

        # Helper: ensure the returned ctx.xxx() is always a list for easier handling
        def _ensure_list(self, val):
            if val is None:
                return []
            if isinstance(val, list):
                return val
            return [val]
    
        def visitSpec(self, ctx):
            """Visit the top-level spec rule"""
            for unit_ctx in ctx.unit():
                self.visit(unit_ctx)
            return self.program
        
        def visitUnit(self, ctx):
            """Visit a unit (top-level declaration)"""
            if ctx.mtypeDecl():
                mtype = self.visit(ctx.mtypeDecl())
                self.program.mtypes.append(mtype)
            elif ctx.varDecl():
                var = self.visit(ctx.varDecl())
                if isinstance(var, list):
                    self.program.globals.extend(var)
                elif var is not None:  # Guard against None
                    self.program.globals.append(var)
            elif ctx.proctype():
                proc = self.visit(ctx.proctype())
                self.program.proctypes.append(proc)
            elif ctx.init():
                self.program.init = self.visit(ctx.init())
            elif ctx.inlineDecl():
                inline = self.visit(ctx.inlineDecl())
                self.program.inlines.append(inline)
            elif ctx.typedefDecl():
                typedef = self.visit(ctx.typedefDecl())
                self.program.typedefs.append(typedef)
            elif ctx.chanDecl():
                chan = self.visit(ctx.chanDecl())
                if chan is not None:  # Guard against None
                    self.program.globals.append(chan)
        
        def visitChanDecl(self, ctx):
            name = ctx.ID().getText()
            size_expr = self.visit(ctx.expr())  # 通道大小
            types = [self.visit(typename_ctx) for typename_ctx in ctx.typename()]
            return VarDecl('chan', name, array_size=None, init_value=None, is_channel=True, channel_size=size_expr, channel_types=types)

        def visitMtypeDecl(self, ctx):
            """Visit mtype declaration"""
            names = [id_node.getText() for id_node in ctx.ID()]
            return MtypeDecl(names)
        
        def visitTypedefDecl(self, ctx):
            """Visit typedef declaration"""
            name = ctx.ID().getText()
            fields = []
            for var_ctx in ctx.varDecl():
                var = self.visit(var_ctx)
                if isinstance(var, list):
                    fields.extend(var)
                else:
                    fields.append(var)
            return TypeDef(name, fields)
        
        def visitVarDecl(self, ctx):
            """Visit variable declaration

            This parses a rule of the form:
              typename ID ('[' expr ']')? ('=' expr)? (',' ID ('[' expr ']')? ('=' expr)?)* ';'?
            We iterate over the parse-tree children to extract each ID and its optional array size and init value.
            """
            typename = self.visit(ctx.typename())
            vars = []

            # Collect children as a list for index-based scanning
            children = list(ctx.getChildren()) if hasattr(ctx, 'getChildren') else []
            # Skip the first child if it corresponds to the typename node
            i = 0
            if len(children) > 0 and children[0].getText() == typename:
                i = 1

            # Helper regex to detect identifier-like terminal nodes
            ident_re = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

            while i < len(children):
                child = children[i]
                text = child.getText()

                # Skip non-ID tokens until we find an identifier
                if not ident_re.match(text):
                    i += 1
                    continue

                name = text
                array_size = None
                init_value = None

                j = i + 1
                # Check for optional array size: '[' expr ']'
                if j < len(children) and children[j].getText() == '[':
                    # children[j+1] should be an expr context
                    if j + 1 < len(children):
                        expr_ctx = children[j + 1]
                        # Only visit if it's a parser context (expr); otherwise skip
                        try:
                            array_size = self.visit(expr_ctx)
                        except Exception:
                            array_size = None
                    j += 3  # skip '[', expr, ']'

                # Check for optional initialization: '=' expr
                if j < len(children) and children[j].getText() == '=':
                    if j + 1 < len(children):
                        expr_ctx = children[j + 1]
                        try:
                            init_value = self.visit(expr_ctx)
                        except Exception:
                            init_value = None
                    j += 2  # skip '=', expr

                # Build VarDecl
                is_channel = (typename == 'chan')
                var = VarDecl(typename, name, array_size, init_value, is_channel)
                vars.append(var)

                # Advance i to after this variable; skip comma if present
                i = j
                if i < len(children) and children[i].getText() == ',':
                    i += 1

            return vars if len(vars) > 1 else vars[0] if vars else None
        
        def visitTypename(self, ctx):
            """Visit typename"""
            return ctx.getText()
        


        def visitProctype(self, ctx):
            """Visit proctype declaration"""
            is_active = ctx.getChild(0).getText() == 'active'
            active_count = None
            
            name = ctx.ID().getText()
            
            # Get parameters - 使用 paramGroup 规则
            params = []
            for param_group_ctx in self._ensure_list(ctx. paramGroup()):
                # 获取类型名
                typename = self. visit(param_group_ctx. typename())
                
                # 获取该类型下的所有参数名（ID 列表）
                for id_token in param_group_ctx.ID():
                    param_name = id_token.getText()
                    params.append(VarDecl(typename, param_name))
            
            # Get body
            body = self.visit(ctx.sequence())
            
            return Proctype(name, params, body, is_active, active_count)

        def visitParamGroup(self, ctx):
            """Visit parameter group"""
            typename = self.visit(ctx.typename())
            params = []
            for id_token in ctx.ID():
                params.append(VarDecl(typename, id_token.getText()))
            return params
        def visitInit(self, ctx):
            """Visit init process"""
            body = self.visit(ctx.sequence())
            return Init(body)
        
        def visitInlineDecl(self, ctx):
            """Visit inline declaration"""
            ids = self._ensure_list(ctx.ID())
            name = ids[0].getText() if ids else ""
            params = [id_node.getText() for id_node in ids[1:]]
            body = self.visit(ctx.sequence())
            return InlineDecl(name, params, body)
        
        def visitSequence(self, ctx):
            steps = []
            for child in self._ensure_list(ctx.getChildren()):
                # 处理局部变量声明
                if hasattr(child, 'accept') and isinstance(child, PromelaParser.VarDeclContext):
                    var = self. visit(child)
                    if isinstance(var, list):
                        self.program.globals. extend(var)
                    elif var is not None:
                        self. program.globals. append(var)
                # 处理 step
                elif hasattr(child, 'accept') and isinstance(child, PromelaParser.StepContext):
                    step = self.visit(child)
                    if step is not None:
                        if isinstance(step, Sequence):
                            # 如果返回的是 Sequence，展开它
                            steps.extend(step.steps)
                        else:
                            steps.append(step)
            return Sequence(steps)
        
        def visitStep(self, ctx):
            """Visit a step (statement or unless)"""
            if ctx.getChildCount() == 1:
                return self.visit(ctx.stmt(0))
            else:
                # unless statement
                main_stmt = self.visit(ctx.stmt(0))
                unless_stmt = self.visit(ctx.stmt(1))
                return UnlessStmt(main_stmt, unless_stmt)
        
        # Statement visitors
        
        def visitSkipStmt(self, ctx):
            return SkipStmt()
        
        def visitBreakStmt(self, ctx):
            return BreakStmt()
        
        def visitLabeledStmt(self, ctx):
            label = ctx.ID().getText()
            stmt = self.visit(ctx.stmt())
            return LabeledStmt(label, stmt)
        
        def visitGotoStmt(self, ctx):
            label = ctx.ID().getText()
            return GotoStmt(label)
        
        def visitExprStmt(self, ctx):
            expr = self.visit(ctx.expr())
            return ExprStmt(expr)
        
        def visitAssignStmt(self, ctx):
            var = ctx.ID().getText()
            expr = self.visit(ctx.expr())
            return AssignStmt(var, expr)
        
        def visitArrayAssignStmt(self, ctx):
            var = ctx.ID().getText()
            index = self.visit(ctx.expr(0))
            expr = self.visit(ctx.expr(1))
            return ArrayAssignStmt(var, index, expr)
        
        def visitFieldAssignStmt(self, ctx):
            var = ctx.ID(0).getText()
            field = ctx.ID(1).getText()
            expr = self.visit(ctx.expr())
            return FieldAssignStmt(var, field, expr)
        
        def visitIfStmt(self, ctx):
            # 改为访问 optionLists() 而不是 option()
            options = self.visitOptionLists(ctx. optionLists())
            return IfStmt(options)

        def visitDoStmt(self, ctx):
            # 改为访问 optionLists() 而不是 option()
            options = self.visitOptionLists(ctx.optionLists())
            return DoStmt(options)
        
        def visitOptionLists(self, ctx):
            """Visit optionLists rule and return list of (guard, body) pairs"""
            options = []
            for option_ctx in ctx.option():
                guard = None
                if option_ctx.expr():
                    guard = self.visit(option_ctx.expr())
                body = self.visit(option_ctx.sequence())
                options.append((guard, body))
            return options

        def visitAtomicStmt(self, ctx):
            body = self.visit(ctx.sequence())
            return AtomicStmt(body)
        
        def visitDstepStmt(self, ctx):
            body = self.visit(ctx.sequence())
            return DstepStmt(body)
        
        def visitBlockStmt(self, ctx):
            body = self.visit(ctx.sequence())
            return BlockStmt(body)
        
        def visitAssertStmt(self, ctx):
            expr = self.visit(ctx.expr())
            return AssertStmt(expr)
        
        def visitPrintfStmt(self, ctx):
            format_str = ctx.STRING().getText()
            args_ctx = self._ensure_list(ctx.expr())
            args = [self.visit(expr_ctx) for expr_ctx in args_ctx]
            return PrintfStmt(format_str, args)
        
        def visitPrintmStmt(self, ctx):
            expr = self.visit(ctx.expr())
            return PrintmStmt(expr)
        
        def visitSendStmt(self, ctx):
            channel = ctx.ID().getText()
            exprs_ctx = self._ensure_list(ctx.expr())
            exprs = [self.visit(expr_ctx) for expr_ctx in exprs_ctx]
            return SendStmt(channel, exprs)
        
        def visitReceiveStmt(self, ctx):
            channel = self._ensure_list(ctx.ID())[0].getText()
            vars = [id_node.getText() for id_node in self._ensure_list(ctx.ID())[1:]]
            return ReceiveStmt(channel, vars, is_poll=False)
        
        def visitReceivePollStmt(self, ctx):
            ids = self._ensure_list(ctx.ID())
            channel = ids[0].getText() if ids else ""
            vars = [id_node.getText() for id_node in ids[1:]]
            return ReceiveStmt(channel, vars, is_poll=True)
        
        def visitReceiveArrowStmt(self, ctx):
            """Visit receive with arrow: ch ? msg -> stmt"""
            ids = self._ensure_list(ctx.ID())
            channel = ids[0].getText() if ids else ""
            vars = [id_node.getText() for id_node in ids[1:]]
            receive_stmt = ReceiveStmt(channel, vars, is_poll=False)
            # The arrow statement combines receive with a following statement
            following_stmt = self.visit(ctx.stmt())
            # Return as a sequence
            return Sequence([receive_stmt, following_stmt])
        
        def visitRunStmt(self, ctx):
            procname = ctx.ID().getText()
            args_ctx = self._ensure_list(ctx.expr())
            args = [self.visit(expr_ctx) for expr_ctx in args_ctx]
            return RunStmt(procname, args)
        
        def visitInlineCallStmt(self, ctx):
            name = ctx.ID().getText()
            args_ctx = self._ensure_list(ctx.expr())
            args = [self.visit(expr_ctx) for expr_ctx in args_ctx]
            return InlineCallStmt(name, args)
        
        def visitOptions(self, ctx):
            """Visit options (collection of option branches)"""
            options = []
            for option_ctx in self._ensure_list(ctx.option()):
                result = self.visit(option_ctx)
                options.append(result)
            return options

        def visitOption(self, ctx):
            exprs = ctx.expr()
            if exprs is None:
                guard_expr = BoolExpr(True)
            else:
                guard_expr = self.visit(exprs)
            body = self.visit(ctx.sequence())
            return (guard_expr, body)
        
        # Expression visitors
        
        def visitNumberExpr(self, ctx):
            return NumberExpr(int(ctx.NUMBER().getText()))
        
        def visitTrueExpr(self, ctx):
            return BoolExpr(True)
        
        def visitFalseExpr(self, ctx):
            return BoolExpr(False)
        
        def visitStringExpr(self, ctx):
            text = ctx.STRING().getText()
            return StringExpr(text[1:-1])  # Remove quotes
        
        def visitIdExpr(self, ctx):
            return IdExpr(ctx.ID().getText())
        
        def visitParenExpr(self, ctx):
            return self.visit(ctx.expr())
        
        def visitBinaryOpExpr(self, ctx):
            """Generic binary operation visitor"""
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            op = ctx.getChild(1).getText()
            return BinaryOp(op, left, right)
        
        # Map specific binary operators
        visitMulDivModExpr = visitBinaryOpExpr
        visitAddSubExpr = visitBinaryOpExpr
        visitShiftExpr = visitBinaryOpExpr
        visitRelationalExpr = visitBinaryOpExpr
        visitEqualityExpr = visitBinaryOpExpr
        visitBitwiseAndExpr = visitBinaryOpExpr
        visitBitwiseXorExpr = visitBinaryOpExpr
        visitBitwiseOrExpr = visitBinaryOpExpr
        visitLogicalAndExpr = visitBinaryOpExpr
        visitLogicalOrExpr = visitBinaryOpExpr
        
        def visitUnaryOpExpr(self, ctx):
            """Generic unary operation visitor"""
            expr = self.visit(ctx.expr())
            op = ctx.getChild(0).getText() if ctx.getChildCount() > 1 else ctx.getChild(1).getText()
            return UnaryOp(op, expr)
        
        visitLogicalNotExpr = visitUnaryOpExpr
        visitBitwiseNotExpr = visitUnaryOpExpr
        visitUnaryMinusExpr = visitUnaryOpExpr
        visitUnaryPlusExpr = visitUnaryOpExpr
        
        def visitArrayAccessExpr(self, ctx):
            array = ctx.ID().getText()
            index = self.visit(ctx.expr())
            return ArrayAccessExpr(array, index)
        
        def visitFieldAccessExpr(self, ctx):
            struct = ctx.ID(0).getText()
            field = ctx.ID(1).getText()
            return FieldAccessExpr(struct, field)
        
        def visitLenExpr(self, ctx):
            channel = ctx.ID().getText()
            return LenExpr(channel)
        
        def visitEmptyExpr(self, ctx):
            channel = ctx.ID().getText()
            return EmptyExpr(channel)
        
        def visitFullExpr(self, ctx):
            channel = ctx.ID().getText()
            return FullExpr(channel)
        
        def visitNemptyExpr(self, ctx):
            channel = ctx.ID().getText()
            return NemptyExpr(channel)
        
        def visitNfullExpr(self, ctx):
            channel = ctx.ID().getText()
            return NfullExpr(channel)
        
        def visitPidExpr(self, ctx):
            """Visit _pid built-in variable"""
            return IdExpr('_pid')
        
        def visitNrPrExpr(self, ctx):
            """Visit _nr_pr built-in variable"""
            return IdExpr('_nr_pr')
        
        def visitEnabledExpr(self, ctx):
            expr = self.visit(ctx.expr())
            return EnabledExpr(expr)
        
        def visitTimeoutExpr(self, ctx):
            return TimeoutExpr()
        
        def visitNonProgressExpr(self, ctx):
            return NonProgressExpr()


def compile_pml_to_smv(input_file, output_file):
    """Compile a Promela file to SMV"""
    try:
        # Parse the input file
        if USE_ANTLR:
            # Preprocess the file to expand #define macros
            preprocessor = PromelaPreprocessor()
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            preprocessed_code = preprocessor.preprocess(source_code)
            
            # Use ANTLR-generated parser on preprocessed code
            input_stream = InputStream(preprocessed_code)
            lexer = PromelaLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = PromelaParser(stream)
            tree = parser.spec()
            
            # Build AST
            builder = PromelaASTBuilder()
            program = builder.visit(tree)
        else:
            # Use simple hand-written parser
            program = parse_promela_file(input_file)
        
        # Expand inline macros
        expander = InlineExpander()
        program = expander.expand_program(program)
        
        # Generate SMV code
        generator = SMVGenerator(program)
        smv_code = generator.generate()
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(smv_code)
        
        print(f"Successfully compiled {input_file} to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error compiling {input_file}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <input.pml> [output.smv]")
        print("  If output.smv is not specified, it will be derived from input filename")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Derive output filename from input
        base = os.path.splitext(input_file)[0]
        output_file = base + '.smv'
    
    success = compile_pml_to_smv(input_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
