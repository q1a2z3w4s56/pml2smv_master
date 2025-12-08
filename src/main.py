"""
Main entry point for PML to SMV compiler
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to use ANTLR-generated parser, fall back to simple parser
try:
    from antlr4 import *
    from grammar.PromelaLexer import PromelaLexer
    from grammar.PromelaParser import PromelaParser
    from grammar.PromelaVisitor import PromelaVisitor
    USE_ANTLR = True
except ImportError:
    USE_ANTLR = False

from src.ast_nodes import *
from src.simple_parser import parse_promela_file
from src.inline_expander import InlineExpander
from src.smv_generator import SMVGenerator


if USE_ANTLR:
    class PromelaASTBuilder(PromelaVisitor):
        """Visitor to build AST from parse tree"""
        
        def __init__(self):
            self.program = Program()
    
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
            else:
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
        """Visit variable declaration"""
        typename = self.visit(ctx.typename())
        
        # Handle multiple declarations in one line
        vars = []
        ids = ctx.ID()
        exprs_list = ctx.expr()
        expr_idx = 0
        
        for i, id_node in enumerate(ids):
            name = id_node.getText()
            array_size = None
            init_value = None
            
            # Check for array
            # This is simplified - proper implementation needs better parsing
            
            # Check for initialization
            if expr_idx < len(exprs_list):
                # Could be array size or init value
                init_value = self.visit(exprs_list[expr_idx])
                expr_idx += 1
            
            # Check if it's a channel
            is_channel = (typename == 'chan')
            
            var = VarDecl(typename, name, array_size, init_value, is_channel)
            vars.append(var)
        
        return vars if len(vars) > 1 else vars[0] if vars else None
    
    def visitTypename(self, ctx):
        """Visit typename"""
        return ctx.getText()
    
    def visitProctype(self, ctx):
        """Visit proctype declaration"""
        is_active = ctx.getChild(0).getText() == 'active'
        active_count = None
        
        name_idx = 2 if is_active else 1
        name = ctx.ID().getText()
        
        # Get parameters
        params = []
        if ctx.varDecl():
            for var_ctx in ctx.varDecl():
                var = self.visit(var_ctx)
                if isinstance(var, list):
                    params.extend(var)
                else:
                    params.append(var)
        
        # Get body
        body = self.visit(ctx.sequence())
        
        return Proctype(name, params, body, is_active, active_count)
    
    def visitInit(self, ctx):
        """Visit init process"""
        body = self.visit(ctx.sequence())
        return Init(body)
    
    def visitInlineDecl(self, ctx):
        """Visit inline declaration"""
        name = ctx.ID()[0].getText()
        params = [id_node.getText() for id_node in ctx.ID()[1:]]
        body = self.visit(ctx.sequence())
        return InlineDecl(name, params, body)
    
    def visitSequence(self, ctx):
        """Visit sequence of statements"""
        steps = []
        for step_ctx in ctx.step():
            step = self.visit(step_ctx)
            if step:
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
        options = self.visit(ctx.options())
        return IfStmt(options)
    
    def visitDoStmt(self, ctx):
        options = self.visit(ctx.options())
        return DoStmt(options)
    
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
        args = [self.visit(expr_ctx) for expr_ctx in ctx.expr()]
        return PrintfStmt(format_str, args)
    
    def visitPrintmStmt(self, ctx):
        expr = self.visit(ctx.expr())
        return PrintmStmt(expr)
    
    def visitSendStmt(self, ctx):
        channel = ctx.ID().getText()
        exprs = [self.visit(expr_ctx) for expr_ctx in ctx.expr()]
        return SendStmt(channel, exprs)
    
    def visitReceiveStmt(self, ctx):
        channel = ctx.ID()[0].getText()
        vars = [id_node.getText() for id_node in ctx.ID()[1:]]
        return ReceiveStmt(channel, vars, is_poll=False)
    
    def visitReceivePollStmt(self, ctx):
        channel = ctx.ID()[0].getText()
        vars = [id_node.getText() for id_node in ctx.ID()[1:]]
        return ReceiveStmt(channel, vars, is_poll=True)
    
    def visitRunStmt(self, ctx):
        procname = ctx.ID().getText()
        args = [self.visit(expr_ctx) for expr_ctx in ctx.expr()]
        return RunStmt(procname, args)
    
    def visitInlineCallStmt(self, ctx):
        name = ctx.ID().getText()
        args = [self.visit(expr_ctx) for expr_ctx in ctx.expr()]
        return InlineCallStmt(name, args)
    
    def visitOptions(self, ctx):
        """Visit options in if/do"""
        options = []
        sequences = ctx.sequence()
        for seq_ctx in sequences:
            # First statement is the guard
            seq = self.visit(seq_ctx)
            if seq and len(seq.steps) > 0:
                guard = seq.steps[0]
                if isinstance(guard, ExprStmt):
                    guard_expr = guard.expr
                else:
                    guard_expr = BoolExpr(True)
                
                # Rest are the body
                body_steps = seq.steps[1:] if len(seq.steps) > 1 else []
                body = Sequence(body_steps)
                options.append((guard_expr, body))
            else:
                # Empty sequence
                options.append((BoolExpr(True), Sequence([])))
        
        return options
    
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
            # Use ANTLR-generated parser
            input_stream = FileStream(input_file, encoding='utf-8')
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
