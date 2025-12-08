# PML2SMV - Promela to SMV Compiler

A compiler that translates Promela (Process Meta Language) models to SMV (Symbolic Model Verifier) format for formal verification.

## Features

- **Full Promela Support**: 
  - mtype declarations
  - Global/local variable declarations (bool, byte, short, int, mtype, arrays)
  - proctype and active proctype definitions
  - init processes
  - Statements: assignment, if...fi, do...od, skip, break, assert, goto
  - atomic and d_step blocks
  - Channel declarations and operations (chan, !, ?, len, empty, full)
  - inline macro definitions and calls
  - unless statements
  - run statements (dynamic process creation)
  - typedef structures

- **SMV Translation**:
  - Program counter (PC) encoding for each process
  - Channel encoding using arrays and head/tail pointers
  - Static expansion of dynamic processes
  - Non-deterministic scheduler with fairness constraints
  - Inline macro expansion

## Installation

1. Clone the repository:
```bash
git clone https://github.com/q1a2z3w4s56/pml2smv_master.git
cd pml2smv_master
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate ANTLR parser (if grammar is modified):
```bash
cd grammar
antlr4 -Dlanguage=Python3 -visitor Promela.g4
cd ..
```

## Usage

Basic usage:
```bash
python src/main.py input.pml output.smv
```

Or with automatic output naming:
```bash
python src/main.py examples/peterson.pml
# Creates examples/peterson.smv
```

## Examples

### Peterson's Mutual Exclusion Algorithm
```bash
python src/main.py examples/peterson.pml
```

### Producer-Consumer with Channels
```bash
python src/main.py examples/producer_consumer.pml
```

### Dynamic Process Creation
```bash
python src/main.py examples/dynamic_process.pml
```

## Architecture

The compiler consists of several key components:

1. **ANTLR4 Grammar** (`grammar/Promela.g4`): Defines the Promela language syntax
2. **AST Nodes** (`src/ast_nodes.py`): Abstract Syntax Tree node definitions
3. **CFG Builder** (`src/cfg_builder.py`): Constructs Control Flow Graphs for each process
4. **Channel Encoder** (`src/channel_encoder.py`): Translates Promela channels to SMV arrays
5. **Inline Expander** (`src/inline_expander.py`): Expands inline macro calls
6. **SMV Generator** (`src/smv_generator.py`): Core translation logic to SMV format
7. **Main Compiler** (`src/main.py`): Entry point and orchestration

## Translation Details

### Program Counter Encoding
Each process gets a PC variable tracking its execution state:
```smv
VAR pc_P0 : 0..5;
ASSIGN
  next(pc_P0) := case
    active_proc != P0 : pc_P0;
    pc_P0 = 0 : 1;
    pc_P0 = 1 : 2;
    ...
  esac;
```

### Channel Encoding
Channels are encoded as bounded arrays with head/tail pointers:
```smv
-- chan c = [2] of { byte }
VAR
  c_data : array 0..1 of 0..255;
  c_head : 0..2;
  c_tail : 0..2;
DEFINE
  c_len := (c_tail - c_head + 2) mod 2;
  c_empty := c_head = c_tail;
  c_full := c_len = 2;
```

### Scheduler
A non-deterministic scheduler with fairness ensures all processes progress:
```smv
VAR active_proc : {P0, P1, P2};
ASSIGN
  next(active_proc) := case
    in_atomic : active_proc;
    TRUE : {P0, P1, P2};
  esac;
FAIRNESS active_proc = P0
FAIRNESS active_proc = P1
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.