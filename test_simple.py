#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Simple test script

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer

# Test source code
test_code = """main(){
    int a, b;
    a = 1;
    b = a + 2;
}"""

print("Testing Simple Compiler")
print("=" * 60)
print("Source code:")
print(test_code)
print("\n" + "=" * 60)

# Lexical analysis
print("\n1. Lexical Analysis")
lexer = Lexer(test_code)
tokens = lexer.tokenize()

if lexer.errors:
    print("Lexical analysis errors:")
    for error in lexer.errors:
        print(f"  - {error}")
else:
    print(f"Lexical analysis successful, generated {len(tokens)} tokens")
    lexer.print_tokens()

# Syntax analysis
print("\n2. Syntax Analysis")
parser = Parser(tokens)
ast = parser.parse()

if parser.errors:
    print("Syntax analysis errors:")
    for error in parser.errors:
        print(f"  - {error}")
else:
    print("Syntax analysis successful, built abstract syntax tree")
    parser.print_ast()

# Semantic analysis
print("\n3. Semantic Analysis and Intermediate Code Generation")
if ast:
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    if analyzer.errors:
        print("Semantic analysis errors:")
        for error in analyzer.errors:
            print(f"  - {error}")
    else:
        print("Semantic analysis successful")
        analyzer.symbol_table.print_table()
        analyzer.print_quadruples()

print("\n" + "=" * 60)
print("Test completed!")
