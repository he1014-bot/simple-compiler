#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to test error report generation
"""

import os
import sys
sys.path.append('.')

from lexer import Lexer

# Test with error_test.c content (simplified ASCII only)
test_code = """int x = 5
int y = 10
int z = x + y
"""

print("Testing lexical error detection...")
lexer = Lexer(test_code)
tokens = lexer.tokenize()

print(f"Number of errors: {len(lexer.errors)}")
if lexer.errors:
    print("Errors found:")
    for error in lexer.errors:
        print(f"  - {error}")
    
    # Try to save errors
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    error_file = os.path.join(output_dir, "lexical_errors_debug.txt")
    print(f"Saving errors to: {error_file}")
    
    try:
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write("Lexical Analysis Errors:\n")
            for error in lexer.errors:
                f.write(f"  - {error}\n")
        print("File saved successfully!")
        
        # Check if file exists
        if os.path.exists(error_file):
            print(f"File exists: {error_file}")
            with open(error_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"File content:\n{content}")
        else:
            print(f"File does not exist: {error_file}")
            
    except Exception as e:
        print(f"Error saving file: {e}")
else:
    print("No errors found")
