"""
Preprocessor for Promela files
Handles #define macro expansion before ANTLR parsing
"""

import re
from typing import Dict, Tuple


class PromelaPreprocessor:
    """Preprocessor to expand #define macros in Promela source code"""
    
    def __init__(self):
        self.macros: Dict[str, str] = {}
        
    def preprocess(self, source_code: str) -> str:
        """
        Preprocess Promela source code by expanding #define macros
        
        Args:
            source_code: Raw Promela source code
            
        Returns:
            Preprocessed source code with macros expanded
        """
        lines = source_code.split('\n')
        output_lines = []
        
        for line in lines:
            # Check if this is a #define directive
            if line.strip().startswith('#define'):
                self._parse_define(line)
                # Keep the #define line commented out for reference
                output_lines.append('// ' + line)
            else:
                # Expand macros in this line
                expanded_line = self._expand_macros(line)
                output_lines.append(expanded_line)
        
        return '\n'.join(output_lines)
    
    def _parse_define(self, line: str) -> None:
        """
        Parse a #define directive and store the macro
        
        Supports formats:
        - #define NAME VALUE
        - #define NAME (expression)
        """
        # Remove #define prefix and whitespace
        line = line.strip()[7:].strip()  # Remove '#define'
        
        if not line:
            return
        
        # Match pattern: NAME followed by value/expression
        # Handle both simple values and parenthesized expressions
        match = re.match(r'(\w+)\s+(.+)', line)
        if match:
            name = match.group(1)
            value = match.group(2).strip()
            self.macros[name] = value
    
    def _expand_macros(self, line: str) -> str:
        """
        Expand all macros in a line
        Handles nested macro expansion
        """
        # Keep expanding until no more macros are found
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            expanded = line
            changed = False
            
            # Sort macros by length (longest first) to handle overlapping names
            for macro_name in sorted(self.macros.keys(), key=len, reverse=True):
                # Use word boundaries to match whole identifiers only
                pattern = r'\b' + re.escape(macro_name) + r'\b'
                macro_value = self.macros[macro_name]
                
                # Check if macro is in the line
                if re.search(pattern, expanded):
                    # Replace the macro
                    expanded = re.sub(pattern, f'({macro_value})', expanded)
                    changed = True
            
            if not changed:
                break
                
            line = expanded
            iteration += 1
        
        return line


def preprocess_file(input_path: str, output_path: str = None) -> str:
    """
    Preprocess a Promela file
    
    Args:
        input_path: Path to input .pml file
        output_path: Optional path to write preprocessed output
        
    Returns:
        Preprocessed source code
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    preprocessor = PromelaPreprocessor()
    preprocessed = preprocessor.preprocess(source_code)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(preprocessed)
    
    return preprocessed


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python preprocessor.py <input.pml> [output.pml]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None
    
    preprocessed = preprocess_file(input_file, output_file)
    
    if not output_file:
        print(preprocessed)
