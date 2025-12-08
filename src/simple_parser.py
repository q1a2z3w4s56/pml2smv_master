"""
Simplified Promela Parser
This is a hand-written parser for basic Promela constructs.
For full functionality, generate from ANTLR grammar using:
    antlr4 -Dlanguage=Python3 -visitor grammar/Promela.g4
"""

from src.ast_nodes import *
import re


class SimplePromelaParser:
    """Simple hand-written parser for Promela subset"""
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = self._tokenize(text)
        self.token_pos = 0
    
    def _tokenize(self, text):
        """Tokenize input text"""
        # Remove comments
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)
        
        # Token patterns
        patterns = [
            ('NUMBER', r'\d+'),
            ('STRING', r'"[^"]*"'),
            ('DCOLON', r'::'),
            ('ARROW', r'->'),
            ('EQ', r'=='),
            ('NE', r'!='),
            ('LE', r'<='),
            ('GE', r'>='),
            ('AND', r'&&'),
            ('OR', r'\|\|'),
            ('SEND', r'!(?!=)'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('SEMICOLON', r';'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('ASSIGN', r'='),
            ('LT', r'<'),
            ('GT', r'>'),
            ('NOT', r'!'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULT', r'\*'),
            ('DIV', r'/'),
            ('MOD', r'%'),
            ('DOT', r'\.'),
            ('RECV', r'\?'),
            ('WS', r'\s+'),
        ]
        
        tokens = []
        while text:
            text = text.lstrip()
            if not text:
                break
            
            matched = False
            for token_type, pattern in patterns:
                regex = re.compile('^' + pattern)
                match = regex.match(text)
                if match:
                    value = match.group(0)
                    if token_type != 'WS':
                        tokens.append((token_type, value))
                    text = text[len(value):]
                    matched = True
                    break
            
            if not matched:
                text = text[1:]  # Skip unknown character
        
        return tokens
    
    def peek(self, offset=0):
        """Peek at current token"""
        pos = self.token_pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return (None, None)
    
    def consume(self, expected=None):
        """Consume current token"""
        if self.token_pos >= len(self.tokens):
            return None, None
        
        token_type, value = self.tokens[self.token_pos]
        if expected and token_type != expected:
            raise Exception(f"Expected {expected}, got {token_type}")
        
        self.token_pos += 1
        return token_type, value
    
    def parse(self):
        """Parse the program"""
        program = Program()
        
        while self.token_pos < len(self.tokens):
            token_type, value = self.peek()
            
            if value == 'mtype':
                mtype_decl = self.parse_mtype()
                if mtype_decl:
                    program.mtypes.append(mtype_decl)
                else:
                    # It was just used as a type name, parse as var decl
                    vars = self.parse_var_decl()
                    program.globals.extend(vars if isinstance(vars, list) else [vars])
            elif value == 'typedef':
                program.typedefs.append(self.parse_typedef())
            elif value in ['bool', 'byte', 'short', 'int', 'mtype', 'chan', 'bit', 'pid']:
                vars = self.parse_var_decl()
                program.globals.extend(vars if isinstance(vars, list) else [vars])
            elif value == 'active':
                program.proctypes.append(self.parse_proctype())
            elif value == 'proctype':
                program.proctypes.append(self.parse_proctype())
            elif value == 'init':
                program.init = self.parse_init()
            elif value == 'inline':
                program.inlines.append(self.parse_inline())
            else:
                self.consume()  # Skip unknown tokens
        
        return program
    
    def parse_mtype(self):
        """Parse mtype declaration"""
        self.consume('ID')  # 'mtype'
        
        # Check if = or { follows
        if self.peek()[1] == '=':
            self.consume('ASSIGN')
            self.consume('LBRACE')
            
            names = []
            while True:
                _, name = self.consume('ID')
                names.append(name)
                
                if self.peek()[1] == ',':
                    self.consume('COMMA')
                else:
                    break
            
            self.consume('RBRACE')
            if self.peek()[1] == ';':
                self.consume('SEMICOLON')
            
            return MtypeDecl(names)
        else:
            # mtype used as a type - rewind
            self.token_pos -= 1
            return None
    
    def parse_typedef(self):
        """Parse typedef"""
        self.consume('ID')  # 'typedef'
        _, name = self.consume('ID')
        self.consume('LBRACE')
        
        fields = []
        while self.peek()[1] != '}':
            field_decls = self.parse_var_decl()
            fields.extend(field_decls if isinstance(field_decls, list) else [field_decls])
        
        self.consume('RBRACE')
        if self.peek()[1] == ';':
            self.consume('SEMICOLON')
        
        return TypeDef(name, fields)
    
    def parse_var_decl(self):
        """Parse variable declaration"""
        _, typename = self.consume('ID')
        
        vars = []
        while True:
            _, name = self.consume('ID')
            
            array_size = None
            channel_size = None
            channel_types = None
            is_channel = typename == 'chan'
            
            if self.peek()[1] == '[':
                self.consume('LBRACKET')
                size_expr = self.parse_expr()
                self.consume('RBRACKET')
                
                if is_channel:
                    # Channel size
                    channel_size = size_expr.value if isinstance(size_expr, NumberExpr) else 1
                else:
                    # Array size
                    array_size = size_expr
            
            init_value = None
            if self.peek()[1] == '=':
                self.consume('ASSIGN')
                
                if is_channel and self.peek()[1] == '[':
                    # Channel declaration: chan c = [N] of {type}
                    self.consume('LBRACKET')
                    size_expr = self.parse_expr()
                    channel_size = size_expr.value if isinstance(size_expr, NumberExpr) else 1
                    self.consume('RBRACKET')
                    
                    if self.peek()[1] == 'of':
                        self.consume('ID')  # 'of'
                        self.consume('LBRACE')
                        
                        channel_types = []
                        _, ctype = self.consume('ID')
                        channel_types.append(ctype)
                        
                        while self.peek()[1] == ',':
                            self.consume('COMMA')
                            _, ctype = self.consume('ID')
                            channel_types.append(ctype)
                        
                        self.consume('RBRACE')
                else:
                    init_value = self.parse_expr()
            
            var = VarDecl(typename, name, array_size, init_value, is_channel, 
                         channel_size, channel_types)
            vars.append(var)
            
            if self.peek()[1] == ',':
                self.consume('COMMA')
            else:
                break
        
        if self.peek()[1] == ';':
            self.consume('SEMICOLON')
        
        return vars
    
    def parse_proctype(self):
        """Parse proctype"""
        is_active = False
        active_count = None
        
        if self.peek()[1] == 'active':
            is_active = True
            self.consume('ID')
            
            if self.peek()[1] == '[':
                self.consume('LBRACKET')
                active_count = self.parse_expr()
                self.consume('RBRACKET')
        
        self.consume('ID')  # 'proctype'
        _, name = self.consume('ID')
        
        self.consume('LPAREN')
        params = []
        if self.peek()[1] != ')':
            # Parse parameters
            while True:
                _, ptype = self.consume('ID')
                _, pname = self.consume('ID')
                params.append(VarDecl(ptype, pname))
                
                if self.peek()[1] == ',':
                    self.consume('COMMA')
                elif self.peek()[1] == ')':
                    break
                else:
                    break
        self.consume('RPAREN')
        
        self.consume('LBRACE')
        body = self.parse_sequence()
        self.consume('RBRACE')
        
        return Proctype(name, params, body, is_active, active_count)
    
    def parse_init(self):
        """Parse init process"""
        self.consume('ID')  # 'init'
        self.consume('LBRACE')
        body = self.parse_sequence()
        self.consume('RBRACE')
        return Init(body)
    
    def parse_inline(self):
        """Parse inline definition"""
        self.consume('ID')  # 'inline'
        _, name = self.consume('ID')
        
        self.consume('LPAREN')
        params = []
        if self.peek()[1] != ')':
            while True:
                _, param = self.consume('ID')
                params.append(param)
                if self.peek()[1] == ',':
                    self.consume('COMMA')
                else:
                    break
        self.consume('RPAREN')
        
        self.consume('LBRACE')
        body = self.parse_sequence()
        self.consume('RBRACE')
        
        return InlineDecl(name, params, body)
    
    def parse_sequence(self):
        """Parse sequence of statements"""
        steps = []
        
        # First, parse any local variable declarations
        while self.peek()[1] in ['bool', 'byte', 'short', 'int', 'mtype', 'chan', 'bit', 'pid'] and \
              self.peek(1)[0] == 'ID' and self.peek(2)[1] in [';', '=', '[', ',']:
            # This looks like a variable declaration
            var_decls = self.parse_var_decl()
            # Local variables are stored but not added as statements
            # For now, we'll just skip them as we don't track local scope
        
        while self.peek()[1] not in ['}', 'fi', 'od', None]:
            if self.peek()[1] == ';':
                self.consume('SEMICOLON')
                continue
            
            stmt = self.parse_statement()
            if stmt:
                steps.append(stmt)
        
        return Sequence(steps)
    
    def parse_statement(self):
        """Parse a single statement"""
        token_type, value = self.peek()
        
        if value == 'skip':
            self.consume()
            return SkipStmt()
        
        elif value == 'break':
            self.consume()
            return BreakStmt()
        
        elif value == 'goto':
            self.consume()
            _, label = self.consume('ID')
            return GotoStmt(label)
        
        elif value == 'assert':
            self.consume()
            self.consume('LPAREN')
            expr = self.parse_expr()
            self.consume('RPAREN')
            return AssertStmt(expr)
        
        elif value == 'if':
            return self.parse_if()
        
        elif value == 'do':
            return self.parse_do()
        
        elif value == 'atomic':
            self.consume()
            self.consume('LBRACE')
            body = self.parse_sequence()
            self.consume('RBRACE')
            return AtomicStmt(body)
        
        elif value == 'd_step':
            self.consume()
            self.consume('LBRACE')
            body = self.parse_sequence()
            self.consume('RBRACE')
            return DstepStmt(body)
        
        elif value == 'run':
            self.consume()
            _, procname = self.consume('ID')
            self.consume('LPAREN')
            args = []
            if self.peek()[1] != ')':
                args.append(self.parse_expr())
                while self.peek()[1] == ',':
                    self.consume('COMMA')
                    args.append(self.parse_expr())
            self.consume('RPAREN')
            return RunStmt(procname, args)
        
        elif token_type == 'ID':
            # Could be assignment, labeled statement, or expression
            _, id_val = self.consume('ID')
            
            if self.peek()[1] == ':':
                # Labeled statement
                self.consume('COLON')
                stmt = self.parse_statement()
                return LabeledStmt(id_val, stmt)
            
            elif self.peek()[1] == '=':
                # Assignment
                self.consume('ASSIGN')
                expr = self.parse_expr()
                return AssignStmt(id_val, expr)
            
            elif self.peek()[1] == '[':
                # Array assignment or access
                self.consume('LBRACKET')
                index = self.parse_expr()
                self.consume('RBRACKET')
                
                if self.peek()[1] == '=':
                    self.consume('ASSIGN')
                    expr = self.parse_expr()
                    return ArrayAssignStmt(id_val, index, expr)
                else:
                    # Array access in expression - treat as expression statement
                    arr_expr = ArrayAccessExpr(id_val, index)
                    return ExprStmt(arr_expr)
            
            elif self.peek()[0] == 'SEND':
                # Channel send
                self.consume('SEND')
                exprs = [self.parse_expr()]
                while self.peek()[1] == ',':
                    self.consume('COMMA')
                    exprs.append(self.parse_expr())
                return SendStmt(id_val, exprs)
            
            elif self.peek()[0] == 'RECV':
                # Channel receive
                self.consume('RECV')
                vars = []
                _, var = self.consume('ID')
                vars.append(var)
                while self.peek()[1] == ',':
                    self.consume('COMMA')
                    _, var = self.consume('ID')
                    vars.append(var)
                return ReceiveStmt(id_val, vars)
            
            elif self.peek()[1] == '(':
                # Inline call or function call
                self.consume('LPAREN')
                args = []
                if self.peek()[1] != ')':
                    args.append(self.parse_expr())
                    while self.peek()[1] == ',':
                        self.consume('COMMA')
                        args.append(self.parse_expr())
                self.consume('RPAREN')
                return InlineCallStmt(id_val, args)
            
            else:
                # Expression statement (identifier)
                return ExprStmt(IdExpr(id_val))
        
        elif self.peek()[1] == '(':
            # Parenthesized expression
            expr = self.parse_expr()
            return ExprStmt(expr)
        
        else:
            # Try to parse as expression
            expr = self.parse_expr()
            if expr:
                return ExprStmt(expr)
        
        return None
    
    def parse_if(self):
        """Parse if statement"""
        self.consume('ID')  # 'if'
        
        options = []
        while self.peek()[1] == '::':
            self.consume('DCOLON')
            
            # Parse sequence in this branch
            # First statement could be a guard (expression) or just a statement
            body_steps = []
            
            # Try to determine if we have guard -> body or just body
            # If we see -> after some tokens, there's a guard
            # Otherwise, the whole thing is the body
            
            has_arrow = False
            lookahead_pos = self.token_pos
            paren_depth = 0
            # Look ahead to see if there's an arrow before next :: or fi
            while lookahead_pos < len(self.tokens):
                tt, tv = self.tokens[lookahead_pos]
                if tv == '(':
                    paren_depth += 1
                elif tv == ')':
                    paren_depth -= 1
                elif paren_depth == 0:
                    if tt == 'ARROW':
                        has_arrow = True
                        break
                    elif tv in ['::', 'fi', '}']:
                        break
                lookahead_pos += 1
            
            if has_arrow:
                # Parse guard expression
                guard = self.parse_expr()
                if self.peek()[0] == 'ARROW':
                    self.consume('ARROW')
            else:
                # No explicit guard, use true
                guard = BoolExpr(True)
            
            # Parse body statements
            while self.peek()[1] not in ['::', 'fi', '}']:
                if self.peek()[1] == ';':
                    self.consume('SEMICOLON')
                    continue
                if self.peek()[1] is None:
                    break
                stmt = self.parse_statement()
                if stmt:
                    body_steps.append(stmt)
            
            options.append((guard, Sequence(body_steps)))
        
        if self.peek()[1] == 'fi':
            self.consume('ID')  # 'fi'
        return IfStmt(options)
    
    def parse_do(self):
        """Parse do statement"""
        self.consume('ID')  # 'do'
        
        options = []
        while self.peek()[1] == '::':
            self.consume('DCOLON')
            
            # Similar to if: check if there's a guard with arrow
            has_arrow = False
            lookahead_pos = self.token_pos
            paren_depth = 0
            while lookahead_pos < len(self.tokens):
                tt, tv = self.tokens[lookahead_pos]
                if tv == '(':
                    paren_depth += 1
                elif tv == ')':
                    paren_depth -= 1
                elif paren_depth == 0:
                    if tt == 'ARROW':
                        has_arrow = True
                        break
                    elif tv in ['::', 'od', '}']:
                        break
                lookahead_pos += 1
            
            if has_arrow:
                # Parse guard expression
                guard = self.parse_expr()
                if self.peek()[0] == 'ARROW':
                    self.consume('ARROW')
            else:
                # No explicit guard, use true
                guard = BoolExpr(True)
            
            body_steps = []
            while self.peek()[1] not in ['::', 'od', '}']:
                if self.peek()[1] == ';':
                    self.consume('SEMICOLON')
                    continue
                if self.peek()[1] is None:
                    break
                stmt = self.parse_statement()
                if stmt:
                    body_steps.append(stmt)
            
            options.append((guard, Sequence(body_steps)))
        
        if self.peek()[1] == 'od':
            self.consume('ID')  # 'od'
        return DoStmt(options)
    
    def parse_expr(self):
        """Parse expression (simplified)"""
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        """Parse logical OR"""
        left = self.parse_logical_and()
        
        while self.peek()[0] == 'OR':
            self.consume('OR')
            right = self.parse_logical_and()
            left = BinaryOp('||', left, right)
        
        return left
    
    def parse_logical_and(self):
        """Parse logical AND"""
        left = self.parse_equality()
        
        while self.peek()[0] == 'AND':
            self.consume('AND')
            right = self.parse_equality()
            left = BinaryOp('&&', left, right)
        
        return left
    
    def parse_equality(self):
        """Parse equality operators"""
        left = self.parse_relational()
        
        while self.peek()[0] in ['EQ', 'NE']:
            op_type, op = self.consume()
            right = self.parse_relational()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_relational(self):
        """Parse relational operators"""
        left = self.parse_additive()
        
        while self.peek()[0] in ['LT', 'GT', 'LE', 'GE']:
            op_type, op = self.consume()
            right = self.parse_additive()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_additive(self):
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.peek()[0] in ['PLUS', 'MINUS']:
            op_type, op = self.consume()
            right = self.parse_multiplicative()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_multiplicative(self):
        """Parse multiplication, division, modulo"""
        left = self.parse_unary()
        
        while self.peek()[0] in ['MULT', 'DIV', 'MOD']:
            op_type, op = self.consume()
            right = self.parse_unary()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_unary(self):
        """Parse unary operators"""
        if self.peek()[0] == 'NOT':
            self.consume('NOT')
            expr = self.parse_unary()
            return UnaryOp('!', expr)
        
        elif self.peek()[0] == 'MINUS':
            self.consume('MINUS')
            expr = self.parse_unary()
            return UnaryOp('-', expr)
        
        return self.parse_primary()
    
    def parse_primary(self):
        """Parse primary expressions"""
        token_type, value = self.peek()
        
        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return NumberExpr(int(value))
        
        elif value == 'true':
            self.consume()
            return BoolExpr(True)
        
        elif value == 'false':
            self.consume()
            return BoolExpr(False)
        
        elif token_type == 'STRING':
            self.consume('STRING')
            return StringExpr(value[1:-1])
        
        elif token_type == 'ID':
            _, id_val = self.consume('ID')
            
            # Check for array access
            if self.peek()[1] == '[':
                self.consume('LBRACKET')
                index = self.parse_expr()
                self.consume('RBRACKET')
                return ArrayAccessExpr(id_val, index)
            
            # Check for field access
            elif self.peek()[0] == 'DOT':
                self.consume('DOT')
                _, field = self.consume('ID')
                return FieldAccessExpr(id_val, field)
            
            # Check for function calls like len(), empty(), full()
            elif self.peek()[1] == '(':
                self.consume('LPAREN')
                if id_val == 'len':
                    _, ch = self.consume('ID')
                    self.consume('RPAREN')
                    return LenExpr(ch)
                elif id_val == 'empty':
                    _, ch = self.consume('ID')
                    self.consume('RPAREN')
                    return EmptyExpr(ch)
                elif id_val == 'full':
                    _, ch = self.consume('ID')
                    self.consume('RPAREN')
                    return FullExpr(ch)
                else:
                    # Regular function call - skip for now
                    self.consume('RPAREN')
                    return IdExpr(id_val)
            
            return IdExpr(id_val)
        
        elif self.peek()[1] == '(':
            self.consume('LPAREN')
            expr = self.parse_expr()
            self.consume('RPAREN')
            return expr
        
        return None


def parse_promela_file(filename):
    """Parse a Promela file and return AST"""
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    parser = SimplePromelaParser(text)
    return parser.parse()
