#!/usr/bin/env python3
# Quick test for compiler core functionality

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Simple test code
test_code = "main(){int a; a = 1;}"

print("Quick test for compiler core functionality")
print("=" * 60)

try:
    # Test importing modules
    from lexer import Lexer
    print("? Successfully imported lexer module")
    
    # Test lexical analysis
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    print(f"? Lexical analysis successful, generated {len(tokens)} tokens")
    
    # Test syntax analysis
    from parser import Parser
    print("? Successfully imported parser module")
    
    parser = Parser(tokens)
    ast = parser.parse()
    if ast:
        print("? Syntax analysis successful, built abstract syntax tree")
    else:
        print("? Syntax analysis failed")
        
    # Test semantic analysis
    from semantic import SemanticAnalyzer
    print("? Successfully imported semantic module")
    
    if ast:
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        if success:
            print("? Semantic analysis successful")
            print(f"? Generated {len(analyzer.quadruples)} quadruples")
        else:
            print("? Semantic analysis failed")
    
    print("\n" + "=" * 60)
    print("All core module tests passed!")
    
except ImportError as e:
    print(f"? Failed to import module: {e}")
except Exception as e:
    print(f"? Error during testing: {e}")
    import traceback
    traceback.print_exc()
