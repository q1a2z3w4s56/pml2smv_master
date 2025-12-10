"""
Control Flow Graph Builder for Promela Processes
"""

from src.ast_nodes import *


class CFGNode:
    """Node in the control flow graph"""
    next_id = 0
    
    def __init__(self, stmt=None, label=None):
        self.id = CFGNode.next_id
        CFGNode.next_id += 1
        self.stmt = stmt          # Statement or None (for entry/exit nodes)
        self.label = label        # String or None
        self.successors = []      # List of CFGNode
        self.predecessors = []    # List of CFGNode
    
    def add_successor(self, node):
        """Add a successor node"""
        if node not in self.successors:
            self.successors.append(node)
        if self not in node.predecessors:
            node.predecessors.append(self)
    
    def __repr__(self):
        label_str = f"[{self.label}]" if self.label else ""
        return f"CFGNode({self.id}{label_str})"


class CFG:
    """Control Flow Graph for a process"""
    def __init__(self, name):
        self.name = name
        self.entry = CFGNode()    # Entry node
        self.exit = CFGNode()     # Exit node
        self.nodes = []           # All nodes including entry/exit
        self.labels = {}          # Map from label name to CFGNode
        
    def add_node(self, node):
        """Add a node to the CFG"""
        if node not in self.nodes:
            self.nodes.append(node)
        return node


class CFGBuilder:
    """Builds control flow graphs for processes"""
    
    def __init__(self):
        self.current_cfg = None
        self.break_targets = []   # Stack of break target nodes
        self.goto_fixups = []     # List of (node, label) for goto fixup
    
    def build_cfg(self, proctype):
        """Build CFG for a proctype or init"""
        CFGNode.next_id = 0  # Reset node IDs for each process
        
        cfg = CFG(proctype.name if hasattr(proctype, 'name') else 'init')
        self.current_cfg = cfg
        self.break_targets = []
        self.goto_fixups = []
        
        # Build CFG from body
        if proctype.body:
            last_node = self.build_sequence(proctype.body, cfg.entry)
            if last_node:
                last_node.add_successor(cfg.exit)
        else:
            cfg.entry.add_successor(cfg.exit)
        
        # Fix up goto statements
        for node, label in self.goto_fixups:
            if label in cfg.labels:
                node.add_successor(cfg.labels[label])
            else:
                # Label not found - just skip to next statement
                pass
        
        # Collect all nodes
        self._collect_nodes(cfg, cfg.entry, set())
        
        return cfg
    
    def _collect_nodes(self, cfg, node, visited):
        """Recursively collect all reachable nodes"""
        if node in visited:
            return
        visited.add(node)
        cfg.add_node(node)
        for succ in node.successors:
            self._collect_nodes(cfg, succ, visited)
    
    def build_sequence(self, sequence, entry_node):
        """Build CFG for a sequence of statements"""
        current = entry_node
        
        for step in sequence.steps:
            if isinstance(step, UnlessStmt):
                # Handle unless: main_stmt unless unless_stmt
                # Execute main_stmt, but unless_stmt can interrupt
                main_node = self.build_statement(step.main_stmt, current)
                unless_node = self.build_statement(step.unless_stmt, current)
                # Both branches merge
                next_node = CFGNode()
                if main_node:
                    main_node.add_successor(next_node)
                if unless_node:
                    unless_node.add_successor(next_node)
                current = next_node
            else:
                current = self.build_statement(step, current)
                if current is None:
                    break
        
        return current
    
    def build_statement(self, stmt, entry_node):
        """Build CFG for a single statement"""
        if stmt is None:
            return entry_node
        
        if isinstance(stmt, SkipStmt):
            # Skip is a no-op
            node = CFGNode(stmt)
            entry_node.add_successor(node)
            return node
        
        elif isinstance(stmt, BreakStmt):
            # Break jumps to the break target
            node = CFGNode(stmt)
            entry_node.add_successor(node)
            if self.break_targets:
                node.add_successor(self.break_targets[-1])
            return None  # No fallthrough
        
        elif isinstance(stmt, LabeledStmt):
            # 为标签创建一个显式的入口节点
            label_node = CFGNode(label=stmt.label)
            entry_node. add_successor(label_node)
            
            # 注册标签
            self.current_cfg.labels[stmt.label] = label_node
            
            # 构建被标记的语句
            inner_last = self.build_statement(stmt. stmt, label_node)
            return inner_last
        
        elif isinstance(stmt, GotoStmt):
            # Goto jumps to a label
            node = CFGNode(stmt)
            entry_node.add_successor(node)
            self.goto_fixups.append((node, stmt.label))
            return None  # No fallthrough
        
        elif isinstance(stmt, (AssignStmt, ArrayAssignStmt, FieldAssignStmt, 
                               ExprStmt, AssertStmt, PrintfStmt, PrintmStmt,
                               SendStmt, ReceiveStmt, RunStmt, InlineCallStmt)):
            # Simple statements
            node = CFGNode(stmt)
            entry_node.add_successor(node)
            return node
        
        elif isinstance(stmt, IfStmt):
            # if :: guard1 -> seq1 :: guard2 -> seq2 ... fi
            merge_node = CFGNode()
            
            for guard, body in stmt.options:
                # Create guard node
                guard_node = CFGNode(ExprStmt(guard))
                entry_node.add_successor(guard_node)
                
                # Build body sequence
                last_node = self.build_sequence(body, guard_node)
                if last_node:
                    last_node.add_successor(merge_node)
            
            return merge_node
        
        elif isinstance(stmt, DoStmt):
            # do :: guard1 -> seq1 :: guard2 -> seq2 ... od
            # Loop header where all branches converge
            loop_header = CFGNode()
            entry_node.add_successor(loop_header)
            
            # Break target is after the loop
            break_node = CFGNode()
            self.break_targets.append(break_node)
            
            for guard, body in stmt.options:
                # Create guard node
                guard_node = CFGNode(ExprStmt(guard))
                loop_header.add_successor(guard_node)
                
                # Build body sequence
                last_node = self.build_sequence(body, guard_node)
                if last_node:
                    # Loop back to header
                    last_node.add_successor(loop_header)
            
            # Exit loop via break or all guards false
            loop_header.add_successor(break_node)
            
            self.break_targets.pop()
            return break_node
        
        elif isinstance(stmt, (AtomicStmt, DstepStmt, BlockStmt)):
            # Build CFG for the body
            return self.build_sequence(stmt.body, entry_node)
        
        else:
            # Unknown statement type - treat as simple statement
            node = CFGNode(stmt)
            entry_node.add_successor(node)
            return node


def build_all_cfgs(program):
    """Build CFGs for all processes in the program"""
    builder = CFGBuilder()
    cfgs = {}
    
    # Build CFG for init process
    if program.init:
        cfgs['init'] = builder.build_cfg(program.init)
    
    # Build CFG for each proctype
    for proctype in program.proctypes:
        cfgs[proctype.name] = builder.build_cfg(proctype)
    
    return cfgs
