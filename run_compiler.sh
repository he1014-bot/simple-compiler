#!/bin/bash

main_menu() {
    clear
    echo "========================================"
    echo "      Simple Compiler Launcher v2.0"
    echo "========================================"
    echo ""
    echo "[MAIN MENU]"
    echo "1. Interactive Mode (Recommended for beginners)"
    echo "2. Compile Standard Test Files"
    echo "3. Test Error Code Fixing Feature"
    echo "4. Run All Tests (Standard + Error Tests)"
    echo "5. View Help and Documentation"
    echo "6. Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1) interactive_mode ;;
        2) standard_tests ;;
        3) error_tests ;;
        4) all_tests ;;
        5) help_menu ;;
        6) exit_program ;;
        *) echo "Invalid selection! Please try again." 
           read -p "Press Enter to continue..."
           main_menu ;;
    esac
}

interactive_mode() {
    clear
    echo "========================================"
    echo "      Interactive Mode"
    echo "========================================"
    echo ""
    echo "Starting interactive mode..."
    echo ""
    python main.py
    read -p "Press Enter to continue..."
    main_menu
}

standard_tests() {
    clear
    echo "========================================"
    echo "      Standard Test Files"
    echo "========================================"
    echo ""
    echo "[BASIC TESTS]"
    echo "1. test_simple.c    - Simple variable declarations and assignments"
    echo "2. test2.c          - Complex example with if-else and while loops"
    echo ""
    echo "[ADVANCED TESTS]"
    echo "3. test_for.c       - For loop example"
    echo "4. test_full.c      - Complete program with all features"
    echo ""
    echo "[OTHER OPTIONS]"
    echo "5. Return to Main Menu"
    echo ""
    read -p "Select test file (1-5): " test_choice
    
    case $test_choice in
        1) echo "Compiling: test_simple.c"; python main.py test_simple.c ;;
        2) echo "Compiling: test2.c"; python main.py test2.c ;;
        3) echo "Compiling: test_for.c"; python main.py test_for.c ;;
        4) echo "Compiling: test_full.c"; python main.py test_full.c ;;
        5) main_menu ;;
        *) echo "Invalid selection!" ;;
    esac
    
    read -p "Press Enter to continue..."
    standard_tests
}

error_tests() {
    clear
    echo "========================================"
    echo "      Error Code Fixing Tests"
    echo "========================================"
    echo ""
    echo "These tests demonstrate the code fixing feature that automatically"
    echo "detects and fixes common errors in C source code."
    echo ""
    echo "[SINGLE ERROR TYPE TESTS]"
    echo "1. Missing Semicolons      - test_error_missing_semicolon.c"
    echo "2. Keyword Typos           - test_error_typo_keywords.c"
    echo "3. Missing Parentheses     - test_error_missing_parentheses.c"
    echo "4. Missing Braces          - test_error_missing_braces.c"
    echo ""
    echo "[COMPLEX ERROR TESTS]"
    echo "5. Multiple Error Types    - test_with_errors.c"
    echo "6. Complex Multiple Errors - test_error_complex.c"
    echo ""
    echo "[BATCH TESTING]"
    echo "7. Run ALL Error Tests"
    echo ""
    echo "[OTHER OPTIONS]"
    echo "8. Return to Main Menu"
    echo ""
    read -p "Select test (1-8): " error_choice
    
    case $error_choice in
        1) echo "Testing: Missing Semicolons"; python main.py test_error_missing_semicolon.c output ;;
        2) echo "Testing: Keyword Typos"; python main.py test_error_typo_keywords.c output ;;
        3) echo "Testing: Missing Parentheses"; python main.py test_error_missing_parentheses.c output ;;
        4) echo "Testing: Missing Braces"; python main.py test_error_missing_braces.c output ;;
        5) echo "Testing: Multiple Error Types"; python main.py test_with_errors.c output ;;
        6) echo "Testing: Complex Multiple Errors"; python main.py test_error_complex.c output ;;
        7) run_all_error_tests ;;
        8) main_menu ;;
        *) echo "Invalid selection!" ;;
    esac
    
    read -p "Press Enter to continue..."
    error_tests
}

run_all_error_tests() {
    echo "Running ALL error tests..."
    echo ""
    echo "========================================"
    echo "Test 1: Missing Semicolons"
    echo "========================================"
    python main.py test_error_missing_semicolon.c output
    echo ""
    echo "========================================"
    echo "Test 2: Keyword Typos"
    echo "========================================"
    python main.py test_error_typo_keywords.c output
    echo ""
    echo "========================================"
    echo "Test 3: Missing Parentheses"
    echo "========================================"
    python main.py test_error_missing_parentheses.c output
    echo ""
    echo "========================================"
    echo "Test 4: Missing Braces"
    echo "========================================"
    python main.py test_error_missing_braces.c output
    echo ""
    echo "========================================"
    echo "Test 5: Multiple Error Types"
    echo "========================================"
    python main.py test_with_errors.c output
    echo ""
    echo "========================================"
    echo "Test 6: Complex Multiple Errors"
    echo "========================================"
    python main.py test_error_complex.c output
    echo ""
    echo "========================================"
    echo "All error tests completed!"
    echo "========================================"
}

all_tests() {
    clear
    echo "========================================"
    echo "      Running All Tests"
    echo "========================================"
    echo ""
    echo "This will run all standard and error tests."
    echo "Output will be saved to the 'output' directory."
    echo ""
    read -p "Are you sure? (y/n): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        main_menu
    fi
    
    echo ""
    echo "========================================"
    echo "      Standard Tests"
    echo "========================================"
    echo ""
    echo "Test 1: Simple Example"
    python main.py test_simple.c
    echo ""
    echo "Test 2: Complex Example"
    python main.py test2.c
    echo ""
    echo "Test 3: For Loop Example"
    python main.py test_for.c
    echo ""
    echo "Test 4: Complete Example"
    python main.py test_full.c
    echo ""
    echo "========================================"
    echo "      Error Tests"
    echo "========================================"
    echo ""
    echo "Test 5: Missing Semicolons"
    python main.py test_error_missing_semicolon.c output
    echo ""
    echo "Test 6: Keyword Typos"
    python main.py test_error_typo_keywords.c output
    echo ""
    echo "Test 7: Missing Parentheses"
    python main.py test_error_missing_parentheses.c output
    echo ""
    echo "Test 8: Missing Braces"
    python main.py test_error_missing_braces.c output
    echo ""
    echo "Test 9: Multiple Error Types"
    python main.py test_with_errors.c output
    echo ""
    echo "Test 10: Complex Multiple Errors"
    python main.py test_error_complex.c output
    echo ""
    echo "========================================"
    echo "      All Tests Completed!"
    echo "========================================"
    echo ""
    echo "Check the 'output' directory for results."
    read -p "Press Enter to continue..."
    main_menu
}

help_menu() {
    clear
    echo "========================================"
    echo "      Help and Documentation"
    echo "========================================"
    echo ""
    echo "[COMPILER FEATURES]"
    echo "1. Code Error Detection and Fixing"
    echo "   - Automatically detects and fixes common C code errors"
    echo "   - Supports 6 error types: missing semicolons, keyword typos,"
    echo "     missing parentheses, missing braces, for loop errors,"
    echo "     variable declaration errors"
    echo ""
    echo "2. Full Compilation Pipeline"
    echo "   - Lexical Analysis (tokens.txt)"
    echo "   - Syntax Analysis (ast.txt)"
    echo "   - Semantic Analysis (symbol_table.txt)"
    echo "   - Intermediate Code Generation (quadruples.txt)"
    echo "   - x86-64 Assembly Code Generation (assembly.asm)"
    echo ""
    echo "[OUTPUT FILES]"
    echo "- output/ directory contains all generated files"
    echo "- For error-free code: original_code.c + standard outputs"
    echo "- For code with errors: fixed_code.c + error_report.txt + standard outputs"
    echo ""
    echo "[TEST FILES]"
    echo "- Standard tests: Demonstrate correct code compilation"
    echo "- Error tests: Demonstrate error detection and fixing"
    echo ""
    read -p "Press Enter to continue..."
    main_menu
}

exit_program() {
    echo ""
    echo "Thank you for using Simple Compiler!"
    echo "Goodbye!"
    sleep 2
    exit 0
}

# Start the main menu
main_menu
