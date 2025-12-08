"""
AST Node Definitions for Promela to SMV Compiler
"""

class ASTNode:
    """Base class for all AST nodes"""
    pass


class Program(ASTNode):
    """Root node representing entire Promela program"""
    def __init__(self):
        self.mtypes = []           # List of MtypeDecl
        self.typedefs = []         # List of TypeDef
        self.globals = []          # List of VarDecl
        self.proctypes = []        # List of Proctype
        self.inlines = []          # List of InlineDecl
        self.init = None           # Init process (optional)


class MtypeDecl(ASTNode):
    """mtype declaration: mtype = {A, B, C}"""
    def __init__(self, names):
        self.names = names  # List of identifier strings


class TypeDef(ASTNode):
    """typedef declaration: typedef Name { fields }"""
    def __init__(self, name, fields):
        self.name = name        # String
        self.fields = fields    # List of VarDecl


class VarDecl(ASTNode):
    """Variable declaration"""
    def __init__(self, typename, name, array_size=None, init_value=None, is_channel=False, 
                 channel_size=None, channel_types=None):
        self.typename = typename          # String: 'bool', 'byte', 'int', 'mtype', 'chan', etc.
        self.name = name                  # String
        self.array_size = array_size      # Expression or None
        self.init_value = init_value      # Expression or None
        self.is_channel = is_channel      # Boolean
        self.channel_size = channel_size  # Integer or None (for channels)
        self.channel_types = channel_types # List of type names (for channels)


class Proctype(ASTNode):
    """Process type definition"""
    def __init__(self, name, params, body, is_active=False, active_count=None):
        self.name = name                # String
        self.params = params            # List of VarDecl
        self.body = body                # Sequence
        self.is_active = is_active      # Boolean
        self.active_count = active_count # Expression or None (1 if active without count)


class Init(ASTNode):
    """Init process: init { statements }"""
    def __init__(self, body):
        self.body = body  # Sequence


class InlineDecl(ASTNode):
    """Inline macro definition"""
    def __init__(self, name, params, body):
        self.name = name      # String
        self.params = params  # List of parameter names (strings)
        self.body = body      # Sequence


class Sequence(ASTNode):
    """Sequence of statements"""
    def __init__(self, steps):
        self.steps = steps  # List of statements


# Statement Nodes

class Statement(ASTNode):
    """Base class for statements"""
    pass


class SkipStmt(Statement):
    """skip statement"""
    pass


class BreakStmt(Statement):
    """break statement"""
    pass


class LabeledStmt(Statement):
    """Labeled statement: label: stmt"""
    def __init__(self, label, stmt):
        self.label = label  # String
        self.stmt = stmt    # Statement


class GotoStmt(Statement):
    """goto statement"""
    def __init__(self, label):
        self.label = label  # String


class AssignStmt(Statement):
    """Assignment: x = expr"""
    def __init__(self, var, expr):
        self.var = var    # String (variable name)
        self.expr = expr  # Expression


class ArrayAssignStmt(Statement):
    """Array assignment: arr[idx] = expr"""
    def __init__(self, var, index, expr):
        self.var = var      # String
        self.index = index  # Expression
        self.expr = expr    # Expression


class FieldAssignStmt(Statement):
    """Field assignment: struct.field = expr"""
    def __init__(self, var, field, expr):
        self.var = var      # String
        self.field = field  # String
        self.expr = expr    # Expression


class ExprStmt(Statement):
    """Expression as statement (condition/guard)"""
    def __init__(self, expr):
        self.expr = expr  # Expression


class IfStmt(Statement):
    """if...fi statement"""
    def __init__(self, options):
        self.options = options  # List of (guard, sequence) tuples


class DoStmt(Statement):
    """do...od statement"""
    def __init__(self, options):
        self.options = options  # List of (guard, sequence) tuples


class AtomicStmt(Statement):
    """atomic { ... } block"""
    def __init__(self, body):
        self.body = body  # Sequence


class DstepStmt(Statement):
    """d_step { ... } block"""
    def __init__(self, body):
        self.body = body  # Sequence


class BlockStmt(Statement):
    """{ ... } block"""
    def __init__(self, body):
        self.body = body  # Sequence


class AssertStmt(Statement):
    """assert(expr)"""
    def __init__(self, expr):
        self.expr = expr  # Expression


class PrintfStmt(Statement):
    """printf(format, args...)"""
    def __init__(self, format_str, args):
        self.format_str = format_str  # String
        self.args = args              # List of expressions


class PrintmStmt(Statement):
    """printm(expr)"""
    def __init__(self, expr):
        self.expr = expr  # Expression


class SendStmt(Statement):
    """Channel send: ch ! expr"""
    def __init__(self, channel, exprs):
        self.channel = channel  # String
        self.exprs = exprs      # List of expressions


class ReceiveStmt(Statement):
    """Channel receive: ch ? var"""
    def __init__(self, channel, vars, is_poll=False):
        self.channel = channel  # String
        self.vars = vars        # List of variable names (strings)
        self.is_poll = is_poll  # Boolean (for <> syntax)


class RunStmt(Statement):
    """run statement: run ProcName(args)"""
    def __init__(self, procname, args):
        self.procname = procname  # String
        self.args = args          # List of expressions


class InlineCallStmt(Statement):
    """Inline call: inlineName(args)"""
    def __init__(self, name, args):
        self.name = name  # String
        self.args = args  # List of expressions


class UnlessStmt(Statement):
    """stmt unless stmt"""
    def __init__(self, main_stmt, unless_stmt):
        self.main_stmt = main_stmt      # Statement
        self.unless_stmt = unless_stmt  # Statement


# Expression Nodes

class Expression(ASTNode):
    """Base class for expressions"""
    pass


class BinaryOp(Expression):
    """Binary operation"""
    def __init__(self, op, left, right):
        self.op = op        # String: '+', '-', '*', '/', etc.
        self.left = left    # Expression
        self.right = right  # Expression


class UnaryOp(Expression):
    """Unary operation"""
    def __init__(self, op, expr):
        self.op = op      # String: '!', '~', '-', '+', '++', '--'
        self.expr = expr  # Expression


class IdExpr(Expression):
    """Identifier"""
    def __init__(self, name):
        self.name = name  # String


class NumberExpr(Expression):
    """Number literal"""
    def __init__(self, value):
        self.value = value  # Integer


class BoolExpr(Expression):
    """Boolean literal"""
    def __init__(self, value):
        self.value = value  # Boolean


class StringExpr(Expression):
    """String literal"""
    def __init__(self, value):
        self.value = value  # String


class ArrayAccessExpr(Expression):
    """Array access: arr[idx]"""
    def __init__(self, array, index):
        self.array = array  # String or Expression
        self.index = index  # Expression


class FieldAccessExpr(Expression):
    """Field access: struct.field"""
    def __init__(self, struct, field):
        self.struct = struct  # String or Expression
        self.field = field    # String


class LenExpr(Expression):
    """len(channel)"""
    def __init__(self, channel):
        self.channel = channel  # String


class EmptyExpr(Expression):
    """empty(channel)"""
    def __init__(self, channel):
        self.channel = channel  # String


class FullExpr(Expression):
    """full(channel)"""
    def __init__(self, channel):
        self.channel = channel  # String


class NemptyExpr(Expression):
    """nempty(channel) - not empty"""
    def __init__(self, channel):
        self.channel = channel  # String


class NfullExpr(Expression):
    """nfull(channel) - not full"""
    def __init__(self, channel):
        self.channel = channel  # String


class EnabledExpr(Expression):
    """enabled(expr)"""
    def __init__(self, expr):
        self.expr = expr  # Expression


class TimeoutExpr(Expression):
    """timeout"""
    pass


class NonProgressExpr(Expression):
    """np_ (non-progress)"""
    pass
