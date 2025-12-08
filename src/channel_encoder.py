"""
Channel Encoder for Promela Channels to SMV
Converts channel operations to array-based queue implementations
"""

from src.ast_nodes import *


class ChannelEncoder:
    """Encodes Promela channels as SMV arrays with head/tail pointers"""
    
    def __init__(self):
        self.channels = {}  # Map from channel name to channel info
    
    def register_channel(self, var_decl):
        """Register a channel declaration"""
        if var_decl.is_channel:
            self.channels[var_decl.name] = {
                'size': var_decl.channel_size or 1,
                'types': var_decl.channel_types or ['byte'],
                'type_ranges': self._get_type_ranges(var_decl.channel_types or ['byte'])
            }
    
    def _get_type_ranges(self, types):
        """Get SMV range for each type"""
        ranges = []
        for t in types:
            if t == 'bool' or t == 'bit':
                ranges.append('boolean')
            elif t == 'byte':
                ranges.append('0..255')
            elif t == 'short':
                ranges.append('0..65535')
            elif t == 'int':
                ranges.append('-2147483648..2147483647')
            elif t == 'mtype':
                ranges.append('0..255')  # Assuming mtype fits in byte
            else:
                ranges.append('0..255')  # Default
        return ranges
    
    def generate_channel_vars(self, channel_name):
        """Generate SMV variable declarations for a channel"""
        if channel_name not in self.channels:
            return []
        
        info = self.channels[channel_name]
        size = info['size']
        types = info['types']
        ranges = info['type_ranges']
        
        lines = []
        
        # Data array(s) - one for each field type
        for i, (typ, rng) in enumerate(zip(types, ranges)):
            if len(types) == 1:
                field_name = f"{channel_name}_data"
            else:
                field_name = f"{channel_name}_data{i}"
            
            lines.append(f"  {field_name} : array 0..{size-1} of {rng};")
        
        # Head and tail pointers
        lines.append(f"  {channel_name}_head : 0..{size};")
        lines.append(f"  {channel_name}_tail : 0..{size};")
        
        return lines
    
    def generate_channel_init(self, channel_name):
        """Generate SMV initialization for a channel"""
        if channel_name not in self.channels:
            return []
        
        lines = []
        lines.append(f"  init({channel_name}_head) := 0;")
        lines.append(f"  init({channel_name}_tail) := 0;")
        
        return lines
    
    def generate_channel_defines(self, channel_name):
        """Generate SMV DEFINE macros for channel operations"""
        if channel_name not in self.channels:
            return []
        
        info = self.channels[channel_name]
        size = info['size']
        
        lines = []
        
        # Length calculation
        lines.append(f"  {channel_name}_len := ({channel_name}_tail - {channel_name}_head + {size}) mod {size};")
        
        # Empty check
        lines.append(f"  {channel_name}_empty := ({channel_name}_head = {channel_name}_tail);")
        
        # Full check
        lines.append(f"  {channel_name}_full := ({channel_name}_len = {size-1});")
        
        # Nempty (not empty)
        lines.append(f"  {channel_name}_nempty := !{channel_name}_empty;")
        
        # Nfull (not full)
        lines.append(f"  {channel_name}_nfull := !{channel_name}_full;")
        
        return lines
    
    def encode_send(self, channel_name, exprs):
        """
        Generate SMV code for channel send operation
        Returns guard condition and list of assignments
        """
        if channel_name not in self.channels:
            return "TRUE", []
        
        info = self.channels[channel_name]
        size = info['size']
        types = info['types']
        
        # Guard: channel must not be full
        guard = f"!{channel_name}_full"
        
        # Assignments
        assignments = []
        
        # Write data to tail position
        for i, expr in enumerate(exprs[:len(types)]):
            if len(types) == 1:
                field_name = f"{channel_name}_data"
            else:
                field_name = f"{channel_name}_data{i}"
            
            assignments.append(
                f"next({field_name}[{channel_name}_tail]) := {self._expr_to_smv(expr)};"
            )
        
        # Advance tail pointer
        assignments.append(
            f"next({channel_name}_tail) := ({channel_name}_tail + 1) mod {size};"
        )
        
        return guard, assignments
    
    def encode_receive(self, channel_name, vars):
        """
        Generate SMV code for channel receive operation
        Returns guard condition and list of assignments
        """
        if channel_name not in self.channels:
            return "TRUE", []
        
        info = self.channels[channel_name]
        size = info['size']
        types = info['types']
        
        # Guard: channel must not be empty
        guard = f"!{channel_name}_empty"
        
        # Assignments
        assignments = []
        
        # Read data from head position
        for i, var in enumerate(vars[:len(types)]):
            if len(types) == 1:
                field_name = f"{channel_name}_data"
            else:
                field_name = f"{channel_name}_data{i}"
            
            assignments.append(
                f"next({var}) := {field_name}[{channel_name}_head];"
            )
        
        # Advance head pointer
        assignments.append(
            f"next({channel_name}_head) := ({channel_name}_head + 1) mod {size};"
        )
        
        return guard, assignments
    
    def _expr_to_smv(self, expr):
        """Convert a Promela expression to SMV syntax"""
        if isinstance(expr, NumberExpr):
            return str(expr.value)
        elif isinstance(expr, BoolExpr):
            return "TRUE" if expr.value else "FALSE"
        elif isinstance(expr, IdExpr):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = self._expr_to_smv(expr.left)
            right = self._expr_to_smv(expr.right)
            op = expr.op
            # Map operators to SMV syntax
            if op == '&&':
                op = '&'
            elif op == '||':
                op = '|'
            elif op == '!=':
                op = '!='
            return f"({left} {op} {right})"
        elif isinstance(expr, UnaryOp):
            e = self._expr_to_smv(expr.expr)
            return f"({expr.op}{e})"
        elif isinstance(expr, ArrayAccessExpr):
            array = expr.array if isinstance(expr.array, str) else self._expr_to_smv(expr.array)
            index = self._expr_to_smv(expr.index)
            return f"{array}[{index}]"
        else:
            # Default fallback
            return "0"
