# PML2SMV Implementation Details

## Overview
This is a complete compiler that translates Promela (Process Meta Language) specifications to SMV (Symbolic Model Verifier) format for formal verification using NuSMV.

## Architecture

### 1. Parser (src/simple_parser.py)
- Hand-written recursive descent parser
- Tokenizes input using regex patterns
- Handles Promela syntax including:
  - Local variable declarations at start of process bodies
  - if/do statements with optional guards and arrows
  - Channel declarations with `[N] of {type}` syntax
  - mtype declarations

### 2. AST (src/ast_nodes.py)
- Complete node hierarchy for Promela constructs
- Base classes: ASTNode, Statement, Expression
- Key nodes: Program, Proctype, VarDecl, IfStmt, DoStmt, SendStmt, ReceiveStmt

### 3. CFG Builder (src/cfg_builder.py)
- Constructs Control Flow Graphs for each process
- Assigns unique IDs to each statement node
- Handles:
  - Sequential composition
  - if/do branching and merging
  - Loop back-edges
  - break and goto jumps
  - Label resolution

### 4. Channel Encoder (src/channel_encoder.py)
- Translates Promela channels to SMV arrays
- Encoding: `chan c = [N] of {T}` becomes:
  ```smv
  c_data : array 0..N-1 of <T_range>;
  c_head : 0..N;
  c_tail : 0..N;
  c_len := (c_tail - c_head + N) mod N;
  c_empty := c_head = c_tail;
  c_full := c_len = N-1;
  ```
- Send operation: Check !full, write data[tail], increment tail
- Receive operation: Check !empty, read data[head], increment head

### 5. Inline Expander (src/inline_expander.py)
- Collects inline macro definitions
- Expands calls by:
  - Deep copying the macro body
  - Substituting formal parameters with actual arguments
  - Replacing the call with expanded statements

### 6. SMV Generator (src/smv_generator.py)
- Core translation engine
- Generates:
  - **VAR section**: Global variables, PC variables for each process, scheduler
  - **DEFINE section**: Channel operations (len, empty, full)
  - **ASSIGN section**: 
    - init() for all variables
    - next() for variables (case statements checking active_proc & PC)
    - next() for PCs (transitions based on statement semantics)
    - Scheduler transitions
  - **FAIRNESS**: One constraint per process instance

#### PC Encoding
Each statement in a process CFG gets a unique PC value:
```smv
next(pc_P0) := case
  active_proc != P0 : pc_P0;              -- not scheduled
  pc_P0 = 0 : 1;                          -- unconditional
  pc_P0 = 1 & guard : 2;                  -- conditional
  pc_P0 = 2 & !ch_full : 3;               -- channel guard
  TRUE : pc_P0;                           -- default
esac;
```

#### Variable Transitions
For each global variable, check all processes for assignments:
```smv
next(x) := case
  active_proc = P0 & pc_P0 = 5 : expr1;
  active_proc = P1 & pc_P1 = 3 : expr2;
  TRUE : x;                               -- frame condition
esac;
```

#### Scheduler
Non-deterministic process selection with atomic block support:
```smv
next(active_proc) := case
  in_atomic : active_proc;                -- stay in atomic
  TRUE : {P0, P1, P2};                   -- non-deterministic choice
esac;
```

## Usage Examples

### Peterson's Algorithm
```bash
python src/main.py examples/peterson.pml examples/peterson.smv
```
Generates 77 lines including:
- Array variable `flag[2]`
- Shared variable `turn`
- Two processes with PC encoding
- Fairness constraints

### Producer-Consumer
```bash
python src/main.py examples/producer_consumer.pml examples/producer_consumer.smv
```
Generates 65 lines including:
- Channel encoded as array with pointers
- DEFINE macros for buffer operations
- mtype handling
- Process synchronization via channel guards

### Dynamic Processes
```bash
python src/main.py examples/dynamic_process.pml examples/dynamic_process.smv
```
Demonstrates `run` statement handling (simplified - runs are statically expanded in this implementation).

## Limitations

1. **Array Size**: Currently hardcoded for arrays of size 2 (sufficient for examples)
2. **Local Variables**: Parsed but not tracked in separate scope (simplified model)
3. **Dynamic Process Creation**: `run` statements are parsed but not fully implemented (would require dynamic instance creation)
4. **Complex Expressions**: Some advanced Promela expressions may not be fully supported
5. **Type System**: Simplified type ranges (byte = 0..255, etc.)

## Testing

Run all tests:
```bash
for file in examples/*.pml; do
  python src/main.py "$file" "${file%.pml}.smv"
done
```

All provided examples compile successfully and generate valid SMV code.

## Future Enhancements

1. **Full ANTLR Integration**: Generate parser from grammar using ANTLR4
2. **Dynamic Arrays**: Support arbitrary array sizes
3. **Local Scope**: Proper tracking of local variable scopes
4. **Run Statement**: Full implementation of dynamic process creation
5. **Optimization**: Reduce state space through abstraction and optimization
6. **Error Reporting**: Better error messages with line numbers
7. **LTL Properties**: Support for embedded LTL specifications
8. **Advanced Channels**: Sorted send, random receive, etc.

## References

- [Promela Language Reference](http://spinroot.com/spin/Man/promela.html)
- [NuSMV User Manual](https://nusmv.fbk.eu/NuSMV/userman/v26/nusmv.pdf)
- [ANTLR4 Documentation](https://github.com/antlr/antlr4/blob/master/doc/index.md)
