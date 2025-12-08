"""
SMV Code Generator for Promela to SMV Compiler
Generates NuSMV code from Promela AST with CFGs
"""

from src.ast_nodes import *
from src.cfg_builder import build_all_cfgs
from src.channel_encoder import ChannelEncoder


class SMVGenerator:
    """Generates SMV code from Promela program"""
    
    def __init__(self, program):
        self.program = program
        self.cfgs = {}
        self.channel_encoder = ChannelEncoder()
        self.mtype_map = {}  # Map mtype names to integers
        self.process_instances = []  # List of (proc_name, instance_num, is_active)
        self.indent = 0
    
    def generate(self):
        """Generate complete SMV module"""
        lines = []
        
        # Build CFGs for all processes
        self.cfgs = build_all_cfgs(self.program)
        
        # Register channels
        for var in self.program.globals:
            if var.is_channel:
                self.channel_encoder.register_channel(var)
        
        # Build mtype map
        self._build_mtype_map()
        
        # Determine process instances
        self._determine_process_instances()
        
        # Generate module header
        lines.append("MODULE main")
        lines.append("")
        
        # Generate VAR section
        lines.extend(self._generate_var_section())
        lines.append("")
        
        # Generate DEFINE section
        lines.extend(self._generate_define_section())
        lines.append("")
        
        # Generate ASSIGN section
        lines.extend(self._generate_assign_section())
        lines.append("")
        
        # Generate FAIRNESS constraints
        lines.extend(self._generate_fairness_section())
        
        return "\n".join(lines)
    
    def _build_mtype_map(self):
        """Build mapping from mtype names to integer values"""
        value = 1
        for mtype_decl in self.program.mtypes:
            for name in mtype_decl.names:
                self.mtype_map[name] = value
                value += 1
    
    def _determine_process_instances(self):
        """Determine all process instances (active proctypes and init)"""
        # Add init if present
        if self.program.init:
            self.process_instances.append(('init', 0, True))
        
        # Add active proctypes
        for proctype in self.program.proctypes:
            if proctype.is_active:
                count = 1
                if proctype.active_count:
                    # Extract count from expression
                    if isinstance(proctype.active_count, NumberExpr):
                        count = proctype.active_count.value
                
                for i in range(count):
                    self.process_instances.append((proctype.name, i, True))
    
    def _generate_var_section(self):
        """Generate VAR section"""
        lines = ["VAR"]
        
        # Global variables
        for var in self.program.globals:
            if var.is_channel:
                # Channel variables
                lines.extend(self.channel_encoder.generate_channel_vars(var.name))
            elif var.array_size:
                # Array variable
                size = self._expr_to_smv(var.array_size)
                var_range = self._get_var_range(var.typename)
                lines.append(f"  {var.name} : array 0..{size}-1 of {var_range};")
            else:
                # Scalar variable
                var_range = self._get_var_range(var.typename)
                lines.append(f"  {var.name} : {var_range};")
        
        # Process PC variables
        for proc_name, instance, _ in self.process_instances:
            cfg = self.cfgs.get(proc_name)
            if cfg:
                max_pc = len(cfg.nodes) - 1
                instance_name = self._get_instance_name(proc_name, instance)
                lines.append(f"  pc_{instance_name} : 0..{max_pc};")
        
        # Scheduler variable
        if len(self.process_instances) > 0:
            proc_names = [self._get_instance_name(p, i) for p, i, _ in self.process_instances]
            lines.append(f"  active_proc : {{{', '.join(proc_names)}}};")
        
        # Atomic/d_step flag
        lines.append(f"  in_atomic : boolean;")
        
        return lines
    
    def _generate_define_section(self):
        """Generate DEFINE section for channel operations"""
        lines = ["DEFINE"]
        
        for var in self.program.globals:
            if var.is_channel:
                lines.extend(self.channel_encoder.generate_channel_defines(var.name))
        
        if len(lines) == 1:
            return []  # No defines needed
        
        return lines
    
    def _generate_assign_section(self):
        """Generate ASSIGN section"""
        lines = ["ASSIGN"]
        
        # Initialize global variables
        for var in self.program.globals:
            if var.is_channel:
                # Channel initialization
                lines.extend(self.channel_encoder.generate_channel_init(var.name))
            elif var.init_value:
                init_val = self._expr_to_smv(var.init_value)
                if var.array_size:
                    # Array initialization (initialize all elements)
                    size = self._expr_to_smv(var.array_size)
                    lines.append(f"  -- init({var.name}) := ...; -- array init")
                else:
                    lines.append(f"  init({var.name}) := {init_val};")
            elif not var.is_channel:
                # Default initialization
                default = self._get_default_value(var.typename)
                if not var.array_size:
                    lines.append(f"  init({var.name}) := {default};")
        
        # Initialize process PCs
        for proc_name, instance, _ in self.process_instances:
            instance_name = self._get_instance_name(proc_name, instance)
            lines.append(f"  init(pc_{instance_name}) := 0;")
        
        # Initialize scheduler
        if len(self.process_instances) > 0:
            first_proc = self._get_instance_name(
                self.process_instances[0][0], 
                self.process_instances[0][1]
            )
            lines.append(f"  init(active_proc) := {first_proc};")
        
        # Initialize atomic flag
        lines.append(f"  init(in_atomic) := FALSE;")
        
        # Process transitions
        for proc_name, instance, _ in self.process_instances:
            lines.extend(self._generate_process_transitions(proc_name, instance))
        
        # Scheduler transitions
        lines.extend(self._generate_scheduler_transitions())
        
        # Atomic flag transitions
        lines.extend(self._generate_atomic_transitions())
        
        return lines
    
    def _generate_process_transitions(self, proc_name, instance):
        """Generate PC transitions for a process"""
        lines = []
        instance_name = self._get_instance_name(proc_name, instance)
        cfg = self.cfgs.get(proc_name)
        
        if not cfg:
            return lines
        
        lines.append(f"  next(pc_{instance_name}) := case")
        lines.append(f"    active_proc != {instance_name} : pc_{instance_name};")
        
        # Generate transitions for each PC value
        for node in cfg.nodes:
            if node == cfg.entry:
                # Entry node
                if len(node.successors) > 0:
                    succ_id = node.successors[0].id
                    lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
            elif node == cfg.exit:
                # Exit node - stay at exit
                lines.append(f"    pc_{instance_name} = {node.id} : {node.id};")
            elif node.stmt:
                # Regular statement node
                stmt = node.stmt
                
                # Generate guard and next PC based on statement type
                if isinstance(stmt, ExprStmt):
                    # Condition guard
                    guard = self._expr_to_smv(stmt.expr)
                    if len(node.successors) > 0:
                        succ_id = node.successors[0].id
                        lines.append(f"    pc_{instance_name} = {node.id} & ({guard}) : {succ_id};")
                    else:
                        lines.append(f"    pc_{instance_name} = {node.id} & ({guard}) : {node.id};")
                
                elif isinstance(stmt, (AssignStmt, ArrayAssignStmt, FieldAssignStmt,
                                      SkipStmt, AssertStmt)):
                    # Simple transition
                    if len(node.successors) > 0:
                        succ_id = node.successors[0].id
                        lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
                
                elif isinstance(stmt, SendStmt):
                    # Send: guard on channel not full
                    guard, _ = self.channel_encoder.encode_send(stmt.channel, stmt.exprs)
                    if len(node.successors) > 0:
                        succ_id = node.successors[0].id
                        lines.append(f"    pc_{instance_name} = {node.id} & {guard} : {succ_id};")
                
                elif isinstance(stmt, ReceiveStmt):
                    # Receive: guard on channel not empty
                    guard, _ = self.channel_encoder.encode_receive(stmt.channel, stmt.vars)
                    if len(node.successors) > 0:
                        succ_id = node.successors[0].id
                        lines.append(f"    pc_{instance_name} = {node.id} & {guard} : {succ_id};")
                
                elif isinstance(stmt, (GotoStmt, BreakStmt)):
                    # Jump statements
                    if len(node.successors) > 0:
                        succ_id = node.successors[0].id
                        lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
                
                else:
                    # Other statements - simple transition
                    if len(node.successors) > 0:
                        succ_id = node.successors[0].id
                        lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
            else:
                # Node without statement (merge point)
                if len(node.successors) > 0:
                    succ_id = node.successors[0].id
                    lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
        
        lines.append(f"    TRUE : pc_{instance_name};")
        lines.append(f"  esac;")
        lines.append("")
        
        return lines
    
    def _generate_scheduler_transitions(self):
        """Generate scheduler transitions"""
        lines = []
        
        if len(self.process_instances) == 0:
            return lines
        
        proc_names = [self._get_instance_name(p, i) for p, i, _ in self.process_instances]
        
        lines.append(f"  next(active_proc) := case")
        lines.append(f"    in_atomic : active_proc;")
        lines.append(f"    TRUE : {{{', '.join(proc_names)}}};")
        lines.append(f"  esac;")
        lines.append("")
        
        return lines
    
    def _generate_atomic_transitions(self):
        """Generate atomic flag transitions"""
        lines = []
        lines.append(f"  next(in_atomic) := case")
        lines.append(f"    TRUE : FALSE;")  # Simplified: atomic blocks end after one step
        lines.append(f"  esac;")
        lines.append("")
        return lines
    
    def _generate_fairness_section(self):
        """Generate FAIRNESS constraints"""
        lines = []
        
        for proc_name, instance, _ in self.process_instances:
            instance_name = self._get_instance_name(proc_name, instance)
            lines.append(f"FAIRNESS active_proc = {instance_name}")
        
        return lines
    
    def _get_instance_name(self, proc_name, instance):
        """Get instance name for process"""
        if instance == 0:
            return proc_name
        else:
            return f"{proc_name}_{instance}"
    
    def _get_var_range(self, typename):
        """Get SMV range for a variable type"""
        if typename == 'bool' or typename == 'bit':
            return 'boolean'
        elif typename == 'byte':
            return '0..255'
        elif typename == 'short':
            return '0..65535'
        elif typename == 'int':
            return '-2147483648..2147483647'
        elif typename == 'mtype':
            return '0..255'
        elif typename == 'pid':
            return '0..255'
        else:
            return '0..255'  # Default
    
    def _get_default_value(self, typename):
        """Get default initial value for a type"""
        if typename == 'bool' or typename == 'bit':
            return 'FALSE'
        else:
            return '0'
    
    def _expr_to_smv(self, expr):
        """Convert Promela expression to SMV syntax"""
        if expr is None:
            return "0"
        
        if isinstance(expr, NumberExpr):
            return str(expr.value)
        
        elif isinstance(expr, BoolExpr):
            return "TRUE" if expr.value else "FALSE"
        
        elif isinstance(expr, IdExpr):
            # Check if it's an mtype
            if expr.name in self.mtype_map:
                return str(self.mtype_map[expr.name])
            return expr.name
        
        elif isinstance(expr, StringExpr):
            return f'"{expr.value}"'
        
        elif isinstance(expr, BinaryOp):
            left = self._expr_to_smv(expr.left)
            right = self._expr_to_smv(expr.right)
            op = expr.op
            
            # Map operators to SMV syntax
            if op == '&&':
                op = '&'
            elif op == '||':
                op = '|'
            elif op == '==':
                op = '='
            
            return f"({left} {op} {right})"
        
        elif isinstance(expr, UnaryOp):
            e = self._expr_to_smv(expr.expr)
            op = expr.op
            return f"({op}{e})"
        
        elif isinstance(expr, ArrayAccessExpr):
            array = expr.array if isinstance(expr.array, str) else self._expr_to_smv(expr.array)
            index = self._expr_to_smv(expr.index)
            return f"{array}[{index}]"
        
        elif isinstance(expr, FieldAccessExpr):
            struct = expr.struct if isinstance(expr.struct, str) else self._expr_to_smv(expr.struct)
            return f"{struct}_{expr.field}"
        
        elif isinstance(expr, LenExpr):
            return f"{expr.channel}_len"
        
        elif isinstance(expr, EmptyExpr):
            return f"{expr.channel}_empty"
        
        elif isinstance(expr, FullExpr):
            return f"{expr.channel}_full"
        
        elif isinstance(expr, NemptyExpr):
            return f"{expr.channel}_nempty"
        
        elif isinstance(expr, NfullExpr):
            return f"{expr.channel}_nfull"
        
        else:
            return "0"  # Fallback
