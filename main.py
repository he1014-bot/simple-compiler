#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compiler Main Program
Function: Integrate lexical analysis, syntax analysis, semantic analysis and intermediate code generation modules
"""

import sys
import os
from lexer import Lexer
from parser import Parser, ASTNode
from semantic import SemanticAnalyzer

def compile_file(filename: str, output_dir: str = "output"):
    """Compile source file"""
    print(f"Compiling file: {filename}")
    print("=" * 60)
    
    # Read source file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' does not exist")
        return False
    except Exception as e:
        print(f"Error: Failed to read file - {e}")
        return False
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Lexical analysis
    print("\n1. Lexical Analysis")
    print("-" * 40)
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    if lexer.errors:
        lexer.print_errors()
        # Save errors to file
        error_file = os.path.join(output_dir, "lexical_errors.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write("Lexical Analysis Errors:\n")
            for error in lexer.errors:
                f.write(f"  - {error}\n")
        print(f"Lexical analysis errors saved to: {error_file}")
        return False
    else:
        lexer.print_tokens()
        # Save token sequence to file
        token_file = os.path.join(output_dir, "tokens.txt")
        with open(token_file, 'w', encoding='utf-8') as f:
            f.write("Lexical Analysis Result:\n")
            f.write("=" * 60 + "\n")
            for i, token in enumerate(lexer.tokens):
                if token.type.value != 99:  # Not EOF
                    f.write(f"{i:3d}: {token}\n")
            f.write(f"{len(lexer.tokens):3d}: (99, EOF)\n")
            f.write("=" * 60 + "\n")
        print(f"Token sequence saved to: {token_file}")
    
    # Syntax analysis
    print("\n2. Syntax Analysis")
    print("-" * 40)
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.errors:
        parser.print_errors()
        # Save errors to file
        error_file = os.path.join(output_dir, "syntax_errors.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write("Syntax Analysis Errors:\n")
            for error in parser.errors:
                f.write(f"  - {error}\n")
        print(f"Syntax analysis errors saved to: {error_file}")
        return False
    else:
        parser.print_ast()
        # Save syntax tree to file
        ast_file = os.path.join(output_dir, "ast.txt")
        with open(ast_file, 'w', encoding='utf-8') as f:
            f.write("Abstract Syntax Tree:\n")
            f.write("=" * 60 + "\n")
            
            def write_ast_node(node, level=0, file=f):
                indent = "  " * level
                value_str = f": {node.value}" if node.value is not None else ""
                file.write(f"{indent}{node.node_type}{value_str}\n")
                for child in node.children:
                    if isinstance(child, ASTNode):
                        write_ast_node(child, level + 1, file)
                    else:
                        file.write(f"{indent}  {child}\n")
            
            write_ast_node(ast)
            f.write("=" * 60 + "\n")
        print(f"Syntax tree saved to: {ast_file}")
    
    # Semantic analysis and intermediate code generation
    print("\n3. Semantic Analysis and Intermediate Code Generation")
    print("-" * 40)
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    analyzer.print_errors()
    
    if not success:
        # Save errors to file
        error_file = os.path.join(output_dir, "semantic_errors.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write("Semantic Analysis Errors:\n")
            for error in analyzer.errors:
                f.write(f"  - {error}\n")
        print(f"Semantic analysis errors saved to: {error_file}")
        return False
    else:
        analyzer.symbol_table.print_table()
        analyzer.print_quadruples()
        
        # Save symbol table to file
        symbol_file = os.path.join(output_dir, "symbol_table.txt")
        with open(symbol_file, 'w', encoding='utf-8') as f:
            f.write("Symbol Table:\n")
            f.write("=" * 60 + "\n")
            f.write(f"{'Name':<10} {'Type':<10} {'Attributes':<20}\n")
            f.write("-" * 60 + "\n")
            for name, info in analyzer.symbol_table.symbols.items():
                attrs = ", ".join(f"{k}={v}" for k, v in info.items() if k not in ["name", "type"])
                f.write(f"{name:<10} {info['type']:<10} {attrs:<20}\n")
            f.write("=" * 60 + "\n")
        print(f"Symbol table saved to: {symbol_file}")
        
        # Save quadruples to file
        quad_file = os.path.join(output_dir, "quadruples.txt")
        with open(quad_file, 'w', encoding='utf-8') as f:
            f.write("Quadruple Intermediate Code:\n")
            f.write("=" * 60 + "\n")
            for i, quad in enumerate(analyzer.quadruples):
                f.write(f"{i:3d}: {quad}\n")
            f.write("=" * 60 + "\n")
        print(f"Quadruples saved to: {quad_file}")
        
        # Generate summary report
        report_file = os.path.join(output_dir, "compile_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Compiler Execution Report\n")
            f.write("=" * 60 + "\n")
            f.write(f"Source File: {filename}\n")
            f.write(f"Compilation Time: {os.path.getctime(filename)}\n")
            f.write("\n")
            f.write("Compilation Result: Success\n")
            f.write("\n")
            f.write("Statistics:\n")
            f.write(f"  - Token Count: {len(tokens)}\n")
            f.write(f"  - Symbol Table Entries: {len(analyzer.symbol_table.symbols)}\n")
            f.write(f"  - Quadruple Count: {len(analyzer.quadruples)}\n")
            f.write(f"  - Temporary Variable Count: {analyzer.symbol_table.next_temp - 1}\n")
            f.write(f"  - Label Count: {analyzer.next_label - 1}\n")
            f.write("\n")
            f.write("Output Files:\n")
            f.write(f"  - Token Sequence: {token_file}\n")
            f.write(f"  - Syntax Tree: {ast_file}\n")
            f.write(f"  - Symbol Table: {symbol_file}\n")
            f.write(f"  - Quadruples: {quad_file}\n")
            f.write("=" * 60 + "\n")
        print(f"Compilation report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("Compilation Completed!")
    return True

def interactive_mode():
    """Interactive Mode"""
    print("Simple Compiler Interactive Mode")
    print("Enter 'quit' or 'exit' to quit")
    print("=" * 60)
    
    while True:
        # Clear some space for better readability
        print("\n" + "=" * 60)
        print("Select Operation:")
        print("1. Compile File")
        print("2. Test Examples")
        print("3. View Help")
        print("4. Exit")
        
        choice = input("\nPlease enter option (1-4): ").strip()
        
        if choice == '1':
            filename = input("Please enter source file path: ").strip()
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist")
                continue
            
            output_dir = input("Please enter output directory (default is 'output'): ").strip()
            if not output_dir:
                output_dir = "output"
            
            compile_file(filename, output_dir)
        
        elif choice == '2':
            print("\n" + "-" * 40)
            print("Test Examples:")
            print("1. Simple Assignment")
            print("2. Conditional Statement")
            print("3. Loop Statement")
            print("4. Complete Example")
            
            test_choice = input("\nPlease select test example (1-4): ").strip()
            
            test_cases = {
                '1': """main(){
    int a;
    a = 10;
}""",
                '2': """main(){
    int a, b;
    a = 5;
    b = 3;
    if (a > b) {
        a = b;
    }
}""",
                '3': """main(){
    int i;
    i = 0;
    while (i < 5) {
        i = i + 1;
    };
}""",
                '4': """main(){
    int a, b, sum;
    a = 1;
    b = 2;
    sum = a + b;
    
    if (sum > 0) {
        a = sum;
    } else {
        b = sum;
    };
    
    while (a < 10) {
        a = a + 1;
    };
}"""
            }
            
            if test_choice in test_cases:
                # Create temporary file
                temp_file = "test.c"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(test_cases[test_choice])
                
                print("\n" + "=" * 60)
                print("Test Code:")
                print("=" * 60)
                print(test_cases[test_choice])
                print("=" * 60)
                
                success = compile_file(temp_file, "test_output")
                
                # Clean up temporary file
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                if not success:
                    print("Test compilation failed!")
            else:
                print("Invalid selection")
        
        elif choice == '3':
            print("\n" + "=" * 60)
            print("Help Information:")
            print("=" * 60)
            print("1. Supported Syntax:")
            print("   - Variable Declaration: int a, b;")
            print("   - Assignment Statement: a = 1;")
            print("   - Arithmetic Expression: a + b * 2")
            print("   - Relational Expression: a > b, a == b")
            print("   - Conditional Statement: if (a > b) { ... }")
            print("   - Loop Statement: while (a < 10) { ... }")
            print("   - Compound Statement: { ... }")
            print("\n2. Output Files:")
            print("   - tokens.txt: Token Sequence")
            print("   - ast.txt: Abstract Syntax Tree")
            print("   - symbol_table.txt: Symbol Table")
            print("   - quadruples.txt: Quadruple Intermediate Code")
            print("   - compile_report.txt: Compilation Report")
            print("=" * 60)
        
        elif choice == '4' or choice.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        else:
            print("Invalid option, please re-enter")

def main():
    """Main Function"""
    print("Simple Compiler v1.0")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Command line mode
        filename = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
        success = compile_file(filename, output_dir)
        sys.exit(0 if success else 1)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
