"""
Inline Macro Expander for Promela
Expands inline macro calls by substituting parameters
"""

from src.ast_nodes import *
import copy


class InlineExpander:
    """Expands inline macro calls"""
    
    def __init__(self):
        self.inlines = {}  # Map from inline name to InlineDecl
    
    def register_inline(self, inline_decl):
        """Register an inline declaration"""
        self.inlines[inline_decl.name] = inline_decl
    
    def expand_program(self, program):
        """Expand all inline calls in a program"""
        # Register all inline declarations
        for inline in program.inlines:
            self.register_inline(inline)
        
        # Expand inlines in all proctypes
        for proctype in program.proctypes:
            if proctype.body:
                proctype.body = self.expand_sequence(proctype.body)
        
        # Expand inlines in init
        if program.init and program.init.body:
            program.init.body = self.expand_sequence(program.init.body)
        
        return program
    
    def expand_sequence(self, sequence):
        """Expand inline calls in a sequence"""
        new_steps = []
        
        for step in sequence.steps:
            if isinstance(step, UnlessStmt):
                # Expand both parts of unless
                step.main_stmt = self.expand_statement(step.main_stmt)
                step.unless_stmt = self.expand_statement(step.unless_stmt)
                new_steps.append(step)
            else:
                expanded = self.expand_statement(step)
                if isinstance(expanded, list):
                    # Inline was expanded to multiple statements
                    new_steps.extend(expanded)
                else:
                    new_steps.append(expanded)
        
        sequence.steps = new_steps
        return sequence
    
    def expand_statement(self, stmt):
        """Expand inline calls in a statement"""
        if stmt is None:
            return stmt
        
        if isinstance(stmt, InlineCallStmt):
            # Expand inline call
            if stmt.name in self.inlines:
                return self.expand_inline_call(stmt)
            else:
                # Unknown inline, keep as is
                return stmt
        
        elif isinstance(stmt, LabeledStmt):
            stmt.stmt = self.expand_statement(stmt.stmt)
            return stmt
        
        elif isinstance(stmt, IfStmt):
            # Expand bodies of if branches
            new_options = []
            for guard, body in stmt.options:
                new_body = self.expand_sequence(body)
                new_options.append((guard, new_body))
            stmt.options = new_options
            return stmt
        
        elif isinstance(stmt, DoStmt):
            # Expand bodies of do branches
            new_options = []
            for guard, body in stmt.options:
                new_body = self.expand_sequence(body)
                new_options.append((guard, new_body))
            stmt.options = new_options
            return stmt
        
        elif isinstance(stmt, (AtomicStmt, DstepStmt, BlockStmt)):
            stmt.body = self.expand_sequence(stmt.body)
            return stmt
        
        elif isinstance(stmt, UnlessStmt):
            stmt.main_stmt = self.expand_statement(stmt.main_stmt)
            stmt.unless_stmt = self.expand_statement(stmt.unless_stmt)
            return stmt
        
        else:
            # Other statements don't contain inline calls
            return stmt
    
    def expand_inline_call(self, call_stmt):
        """
        Expand an inline call by substituting parameters
        Returns a list of statements (the inline body with substitutions)
        """
        inline_decl = self.inlines[call_stmt.name]
        
        # Create parameter substitution map
        param_map = {}
        for i, param_name in enumerate(inline_decl.params):
            if i < len(call_stmt.args):
                param_map[param_name] = call_stmt.args[i]
        
        # Deep copy the inline body and substitute parameters
        expanded_body = copy.deepcopy(inline_decl.body)
        self.substitute_params(expanded_body, param_map)
        
        # Return the expanded statements
        return expanded_body.steps
    
    def substitute_params(self, node, param_map):
        """Recursively substitute parameters in AST nodes"""
        if isinstance(node, Sequence):
            for step in node.steps:
                self.substitute_params(step, param_map)
        
        elif isinstance(node, (AssignStmt, ArrayAssignStmt, FieldAssignStmt)):
            # Substitute in variable name and expression
            if hasattr(node, 'var') and node.var in param_map:
                # Parameter used as lvalue - substitute with expression's name
                if isinstance(param_map[node.var], IdExpr):
                    node.var = param_map[node.var].name
            if hasattr(node, 'expr'):
                node.expr = self.substitute_expr(node.expr, param_map)
            if hasattr(node, 'index'):
                node.index = self.substitute_expr(node.index, param_map)
        
        elif isinstance(node, ExprStmt):
            node.expr = self.substitute_expr(node.expr, param_map)
        
        elif isinstance(node, (AssertStmt, PrintmStmt)):
            node.expr = self.substitute_expr(node.expr, param_map)
        
        elif isinstance(node, PrintfStmt):
            node.args = [self.substitute_expr(arg, param_map) for arg in node.args]
        
        elif isinstance(node, SendStmt):
            node.exprs = [self.substitute_expr(expr, param_map) for expr in node.exprs]
        
        elif isinstance(node, ReceiveStmt):
            # Substitute variable names in receive
            new_vars = []
            for var in node.vars:
                if var in param_map and isinstance(param_map[var], IdExpr):
                    new_vars.append(param_map[var].name)
                else:
                    new_vars.append(var)
            node.vars = new_vars
        
        elif isinstance(node, RunStmt):
            node.args = [self.substitute_expr(arg, param_map) for arg in node.args]
        
        elif isinstance(node, IfStmt):
            new_options = []
            for guard, body in node.options:
                new_guard = self.substitute_expr(guard, param_map)
                self.substitute_params(body, param_map)
                new_options.append((new_guard, body))
            node.options = new_options
        
        elif isinstance(node, DoStmt):
            new_options = []
            for guard, body in node.options:
                new_guard = self.substitute_expr(guard, param_map)
                self.substitute_params(body, param_map)
                new_options.append((new_guard, body))
            node.options = new_options
        
        elif isinstance(node, (AtomicStmt, DstepStmt, BlockStmt)):
            self.substitute_params(node.body, param_map)
        
        elif isinstance(node, UnlessStmt):
            self.substitute_params(node.main_stmt, param_map)
            self.substitute_params(node.unless_stmt, param_map)
        
        elif isinstance(node, LabeledStmt):
            self.substitute_params(node.stmt, param_map)
    
    def substitute_expr(self, expr, param_map):
        """Substitute parameters in an expression"""
        if isinstance(expr, IdExpr):
            if expr.name in param_map:
                return copy.deepcopy(param_map[expr.name])
            return expr
        
        elif isinstance(expr, BinaryOp):
            expr.left = self.substitute_expr(expr.left, param_map)
            expr.right = self.substitute_expr(expr.right, param_map)
            return expr
        
        elif isinstance(expr, UnaryOp):
            expr.expr = self.substitute_expr(expr.expr, param_map)
            return expr
        
        elif isinstance(expr, ArrayAccessExpr):
            if isinstance(expr.array, str) and expr.array in param_map:
                if isinstance(param_map[expr.array], IdExpr):
                    expr.array = param_map[expr.array].name
            expr.index = self.substitute_expr(expr.index, param_map)
            return expr
        
        else:
            # Literals and other expressions don't need substitution
            return expr
