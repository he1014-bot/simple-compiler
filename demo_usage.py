#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compiler Usage Demo
Show how to input code and what the compiler can do
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from codegen import CodeGenerator

def demo_basic_usage():
    """Demonstrate basic usage"""
    print("=" * 70)
    print("Simple Compiler Usage Demo")
    print("=" * 70)
    
    # Example 1: Simplest program
    print("\n1. Simplest program:")
    code1 = """main(){
    int a;
    a = 10;
}"""
    print(f"Source code:\n{code1}")
    
    lexer = Lexer(code1)
    tokens = lexer.tokenize()
    print(f"Lexical analysis: generated {len(tokens)} tokens")
    
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"Syntax analysis: {'Success' if ast else 'Failed'}")
    
    if ast:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print(f"Semantic analysis: generated {len(analyzer.quadruples)} quadruples")
    
    print("\n" + "-" * 70)
    
    # Example 2: Program with arithmetic operations
    print("\n2. Program with arithmetic operations:")
    code2 = """main(){
    int x, y, result;
    x = 5;
    y = 3;
    result = x + y * 2;
}"""
    print(f"Source code:\n{code2}")
    
    lexer = Lexer(code2)
    tokens = lexer.tokenize()
    print(f"Lexical analysis: generated {len(tokens)} tokens")
    
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"Syntax analysis: {'Success' if ast else 'Failed'}")
    
    print("\n" + "-" * 70)
    
    # Example 3: Conditional statement
    print("\n3. Conditional statement (if-else):")
    code3 = """main(){
    int a, b, max;
    a = 10;
    b = 20;
    
    if (a > b) {
        max = a;
    } else {
        max = b;
    }
}"""
    print(f"Source code:\n{code3}")
    
    lexer = Lexer(code3)
    tokens = lexer.tokenize()
    print(f"Lexical analysis: generated {len(tokens)} tokens")
    
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"Syntax analysis: {'Success' if ast else 'Failed'}")
    
    print("\n" + "-" * 70)
    
    # Example 4: Loop statement
    print("\n4. Loop statement (while):")
    code4 = """main(){
    int i, sum;
    i = 0;
    sum = 0;
    
    while (i < 10) {
        sum = sum + i;
        i = i + 1;
    }
}"""
    print(f"Source code:\n{code4}")
    
    lexer = Lexer(code4)
    tokens = lexer.tokenize()
    print(f"Lexical analysis: generated {len(tokens)} tokens")
    
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"Syntax analysis: {'Success' if ast else 'Failed'}")

def demo_compiler_features():
    """Demonstrate compiler features"""
    print("\n" + "=" * 70)
    print("Compiler Supported Features")
    print("=" * 70)
    
    features = [
        ("Lexical Elements", [
            "Keywords: main, int, if, else, while, for",
            "Identifiers: start with letter, followed by letters or digits",
            "Constants: unsigned integers (e.g., 123, 456)",
            "Operators: +, -, *, /, =, >, <, >=, <=, ==, !=",
            "Delimiters: (, ), {, }, ;, ,",
            "Comments: // single-line comment and /* multi-line comment */"
        ]),
        
        ("Syntax Structures", [
            "Program structure: main(){ ... }",
            "Variable declaration: int a, b, c;",
            "Assignment statement: a = 1;",
            "Arithmetic expression: a + b * 2",
            "Relational expression: a > b, a == b",
            "Conditional statement: if (a > b) { ... } and if (a > b) { ... } else { ... }",
            "Loop statement: while (a < 10) { ... }",
            "Compound statement: { ... }"
        ]),
        
        ("Semantic Rules", [
            "Variables must be declared before use",
            "Variables cannot be redeclared",
            "Type system: only int type",
            "Scope: global scope"
        ]),
        
        ("Error Handling", [
            "Lexical errors: illegal characters, unclosed comments, number format errors",
            "Syntax errors: missing semicolons, mismatched parentheses, keyword spelling errors",
            "Semantic errors: undeclared variables, redeclared variables"
        ]),
        
        ("Output Results", [
            "tokens.txt - Lexical analysis results (Token sequence)",
            "ast.txt - Abstract syntax tree",
            "symbol_table.txt - Symbol table",
            "quadruples.txt - Quadruple intermediate code",
            "compile_report.txt - Compilation report"
        ])
    ]
    
    for feature_name, items in features:
        print(f"\n{feature_name}:")
        for item in items:
            print(f"  ? {item}")

def demo_usage_modes():
    """Demonstrate usage modes"""
    print("\n" + "=" * 70)
    print("Usage Modes")
    print("=" * 70)
    
    print("\n1. Interactive mode:")
    print("   python main.py")
    print("   In interactive mode, you can choose:")
    print("   - Compile file: Enter source file path to compile")
    print("   - Test examples: Run predefined test cases")
    print("   - View help: Learn about compiler features and usage")
    print("   - Exit: End the program")
    
    print("\n2. Command line mode:")
    print("   # Compile single file")
    print("   python main.py test.c")
    print("")
    print("   # Specify output directory")
    print("   python main.py test.c my_output")
    
    print("\n3. Direct module testing:")
    print("   # Test lexical analyzer")
    print("   python lexer.py")
    print("")
    print("   # Test syntax analyzer")
    print("   python parser.py")
    print("")
    print("   # Test semantic analyzer")
    print("   python semantic.py")
    print("")
    print("   # Test optimizer (optional)")
    print("   python optimizer.py")
    print("")
    print("   # Test code generator (optional)")
    print("   python codegen.py")

def demo_input_examples():
    """Demonstrate input examples"""
    print("\n" + "=" * 70)
    print("Input Examples")
    print("=" * 70)
    
    examples = [
        ("Simple variable declaration and assignment", """main(){
    int a, b;
    a = 5;
    b = a + 3;
}"""),
        
        ("Arithmetic operations", """main(){
    int x, y, z;
    x = 10;
    y = 20;
    z = (x + y) * 2;
}"""),
        
        ("Conditional judgment", """main(){
    int score, grade;
    score = 85;
    
    if (score >= 90) {
        grade = 1;
    } else if (score >= 80) {
        grade = 2;
    } else {
        grade = 3;
    }
}"""),
        
        ("Loop calculation", """main(){
    int i, factorial;
    i = 1;
    factorial = 1;
    
    while (i <= 5) {
        factorial = factorial * i;
        i = i + 1;
    }
}"""),
        
        ("Complex expression", """main(){
    int a, b, c, result;
    a = 2;
    b = 3;
    c = 4;
    result = a * b + c / 2 - 1;
}""")
    ]
    
    for i, (desc, code) in enumerate(examples, 1):
        print(f"\n{i}. {desc}:")
        print(f"```c\n{code}\n```")

if __name__ == "__main__":
    demo_basic_usage()
    demo_compiler_features()
    demo_usage_modes()
    demo_input_examples()
    
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print("""
This compiler supports simplified C language (mini C), including complete compilation process:
1. Lexical analysis ¡ú 2. Syntax analysis ¡ú 3. Semantic analysis ¡ú 4. Intermediate code generation

Optional modules:
5. Code optimization ¡ú 6. Target code generation

Usage:
1. Save source code as .c file
2. Run python main.py filename.c
3. Check result files in output directory

Supported language features include variable declaration, assignment, arithmetic operations,
relational operations, conditional statements, loop statements and other basic programming structures.
""")
