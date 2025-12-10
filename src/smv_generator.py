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
            if var is not None and var.is_channel:  # Guard against None
                self.channel_encoder.register_channel(var)
        
        # Build mtype map
        self._build_mtype_map()
        
        # Determine process instances
        self._determine_process_instances()
        
        # Generate module header with source information
        lines.append("-- ========================================")
        lines.append("-- SMV Model Generated from Promela Source")
        lines.append("-- ========================================")
        lines.append("MODULE main")
        lines.append("")
        
        # Generate VAR section
        lines.append("-- ========== Variable Declarations ==========")
        lines.extend(self._generate_var_section())
        lines.append("")
        
        # Generate DEFINE section
        lines.append("-- ========== Channel Definitions ==========")
        lines.extend(self._generate_define_section())
        lines.append("")
        
        # Generate ASSIGN section
        lines.append("-- ========== State Transitions ==========")
        lines.extend(self._generate_assign_section())
        lines.append("")
        
        # Generate FAIRNESS constraints
        lines.append("-- ========== Fairness Constraints ==========")
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
        """Determine all process instances (active proctypes, init, and run-created processes)"""
        # Add init if present
        if self.program.init:
            self. process_instances.append(('init', 0, True))
            # 扫描 init 块中的 run 语句，添加动态创建的进程
            self._scan_run_statements(self.program.init. body)
        
        # Add active proctypes
        for proctype in self.program.proctypes:
            if proctype.is_active:
                count = 1
                if proctype.active_count:
                    if isinstance(proctype.active_count, NumberExpr):
                        count = proctype.active_count.value
                
                for i in range(count):
                    self.process_instances.append((proctype.name, i, True))

    def _scan_run_statements(self, body):
        """递归扫描 body 中的 run 语句并添加对应的进程实例"""
        if body is None:
            return
        
        if isinstance(body, Sequence):
            for stmt in body.steps:
                self._scan_run_statements(stmt)
        elif isinstance(body, RunStmt):
            # 找到 run 语句，添加进程实例
            proc_name = body.procname
            # 计算该进程已有的实例数
            existing_count = sum(1 for p, _, _ in self.process_instances if p == proc_name)
            self.process_instances.append((proc_name, existing_count, True))
        elif isinstance(body, (AtomicStmt, DstepStmt, BlockStmt)):
            self._scan_run_statements(body.body)
        elif isinstance(body, IfStmt):
            for guard, seq in body.options:
                self._scan_run_statements(seq)
        elif isinstance(body, DoStmt):
            for guard, seq in body.options:
                self._scan_run_statements(seq)
    
    def _generate_var_section(self):
        """Generate VAR section"""
        lines = ["VAR"]
        
        # Global variables
        for var in self.program.globals:
            if var is None:  # Guard against None
                continue
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
            if var is None:  # Guard against None
                continue
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
        
        # Variable transitions
        lines.extend(self._generate_variable_transitions())
        
        # Process transitions
        for proc_name, instance, _ in self.process_instances:
            lines.extend(self._generate_process_transitions(proc_name, instance))
        
        # Scheduler transitions
        lines.extend(self._generate_scheduler_transitions())
        
        # Atomic flag transitions
        lines.extend(self._generate_atomic_transitions())
        
        return lines
    
    def _generate_variable_transitions(self):
        """Generate next-state transitions for all variables"""
        lines = []
        
        # For each global variable, generate next() assignments
        for var in self.program.globals:
            if var is None:  # Guard against None
                continue
            if var.is_channel:
                # Skip channels for now - they need special handling
                continue
            
            if var.array_size:
                # Array variable - generate transitions for array elements
                lines.append(f"  next({var.name}[0]) := case")
                
                for proc_name, instance, _ in self.process_instances:
                    instance_name = self._get_instance_name(proc_name, instance)
                    cfg = self.cfgs.get(proc_name)
                    if cfg:
                        for node in cfg.nodes:
                            if node.stmt and isinstance(node.stmt, ArrayAssignStmt):
                                if node.stmt.var == var.name:
                                    # Check if index matches
                                    index_smv = self._expr_to_smv(node.stmt.index)
                                    expr_smv = self._expr_to_smv(node.stmt.expr)
                                    lines.append(
                                        f"    active_proc = {instance_name} & pc_{instance_name} = {node.id} & ({index_smv} = 0) : {expr_smv};"
                                    )
                
                lines.append(f"    TRUE : {var.name}[0];")
                lines.append(f"  esac;")
                
                # Generate for index 1 (assuming max array size of 2 for examples)
                lines.append(f"  next({var.name}[1]) := case")
                
                for proc_name, instance, _ in self.process_instances:
                    instance_name = self._get_instance_name(proc_name, instance)
                    cfg = self.cfgs.get(proc_name)
                    if cfg:
                        for node in cfg.nodes:
                            if node.stmt and isinstance(node.stmt, ArrayAssignStmt):
                                if node.stmt.var == var.name:
                                    index_smv = self._expr_to_smv(node.stmt.index)
                                    expr_smv = self._expr_to_smv(node.stmt.expr)
                                    lines.append(
                                        f"    active_proc = {instance_name} & pc_{instance_name} = {node.id} & ({index_smv} = 1) : {expr_smv};"
                                    )
                
                lines.append(f"    TRUE : {var.name}[1];")
                lines.append(f"  esac;")
                lines.append("")
            else:
                # Scalar variable
                lines.append(f"  next({var.name}) := case")
                
                # Check all processes for assignments to this variable
                for proc_name, instance, _ in self.process_instances:
                    instance_name = self._get_instance_name(proc_name, instance)
                    cfg = self.cfgs.get(proc_name)
                    if cfg:
                        for node in cfg.nodes:
                            if node.stmt and isinstance(node.stmt, AssignStmt):
                                if node.stmt.var == var.name:
                                    expr_smv = self._expr_to_smv(node.stmt.expr)
                                    lines.append(
                                        f"    active_proc = {instance_name} & pc_{instance_name} = {node.id} : {expr_smv};"
                                    )
                
                lines.append(f"    TRUE : {var.name};")
                lines.append(f"  esac;")
                lines.append("")
        
        return lines
    
    def _generate_process_transitions(self, proc_name, instance):
        """Generate PC transitions for a process"""
        lines = []
        instance_name = self._get_instance_name(proc_name, instance)
        cfg = self.cfgs. get(proc_name)
        
        if not cfg:
            return lines
        
        lines.append(f"  next(pc_{instance_name}) := case")
        lines.append(f"    active_proc != {instance_name} :  pc_{instance_name};")
        
        # Generate transitions for each PC value
        for node in cfg.nodes:
            if node == cfg.exit: 
                # Exit node - stay at exit
                lines.append(f"    pc_{instance_name} = {node. id} : {node.id};")
                continue
            
            # 处理有多个后继的节点（分支点）
            if len(node. successors) > 1:
                # 这是一个分支节点，生成非确定性选择
                succ_ids = [str(s.id) for s in node.successors]
                lines.append(f"    pc_{instance_name} = {node.id} : {{{', '.join(succ_ids)}}};")
                continue
            
            if len(node.successors) == 0:
                # 没有后继，保持原状态
                lines.append(f"    pc_{instance_name} = {node.id} : {node.id};")
                continue
            
            # 单个后继的情况
            succ_id = node.successors[0].id
            
            if node.stmt is None:
                # Entry node 或 merge node
                lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
            elif isinstance(node.stmt, ExprStmt):
                # 条件守卫 - 需要检查条件是否为真
                guard = self._expr_to_smv(node.stmt.expr)
                # 处理特殊的 timeout 表达式
                if isinstance(node.stmt.expr, TimeoutExpr):
                    guard = "TRUE"  # 简化处理，或者用更复杂的逻辑
                lines.append(f"    pc_{instance_name} = {node.id} & ({guard}) : {succ_id};")
            elif isinstance(node.stmt, SendStmt):
                # Send:  guard on channel not full
                guard, _ = self. channel_encoder.encode_send(node.stmt.channel, node.stmt.exprs)
                lines.append(f"    pc_{instance_name} = {node.id} & {guard} : {succ_id};")
            elif isinstance(node.stmt, ReceiveStmt):
                # Receive: guard on channel not empty
                guard, _ = self.channel_encoder.encode_receive(node.stmt.channel, node.stmt.vars)
                lines.append(f"    pc_{instance_name} = {node. id} & {guard} : {succ_id};")
            elif isinstance(node.stmt, (GotoStmt, BreakStmt)):
                # 跳转语句 - 无条件转换
                lines.append(f"    pc_{instance_name} = {node.id} : {succ_id};")
            else:
                # 其他语句 - 无条件转换
                lines. append(f"    pc_{instance_name} = {node.id} : {succ_id};")
        
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
            elif op == '!=':
                op = '!='
            
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


        elif isinstance(expr, TimeoutExpr):
            return "TRUE"  # 简化：timeout 作为非确定性选择

        elif isinstance(expr, IdExpr):
            # 处理特殊变量
            if expr.name == '_pid':
                # 返回进程 ID，这里需要更复杂的处理
                return "0"  # 简化处理
            elif expr.name == '_nr_pr':
                # 返回进程数量
                return str(len(self.process_instances))
            elif expr.name in self.mtype_map:
                return str(self.mtype_map[expr.name])
            return expr.name
        
        else:
            return "0"  # Fallback
