#!/bin/bash

echo "========================================"
echo "Simple Compiler Launcher"
echo "========================================"
echo ""
echo "Select mode:"
echo "1. Interactive mode (Recommended)"
echo "2. Compile test file"
echo "3. Test error code fixing"
echo "4. Exit"
echo ""

read -p "Enter option (1-4): " choice

if [ "$choice" = "1" ]; then
    echo "Starting interactive mode..."
    python main.py
elif [ "$choice" = "2" ]; then
    echo "Available test files:"
    echo "1. test_simple.c - Simple example"
    echo "2. test2.c - Complex example (if-else and while)"
    echo "3. test_for.c - For loop example"
    echo "4. test_full.c - Complete example"
    echo ""
    read -p "Select test file (1-4): " test_choice
    
    if [ "$test_choice" = "1" ]; then
        python main.py test_simple.c
    elif [ "$test_choice" = "2" ]; then
        python main.py test2.c
    elif [ "$test_choice" = "3" ]; then
        python main.py test_for.c
    elif [ "$test_choice" = "4" ]; then
        python main.py test_full.c
    else
        echo "Invalid selection"
    fi
elif [ "$choice" = "3" ]; then
    echo "========================================"
    echo "Error Code Fixing Tests"
    echo "========================================"
    echo ""
    echo "Available error test files:"
    echo "1. test_with_errors.c - Multiple error types"
    echo "2. test_error_missing_semicolon.c - Missing semicolons"
    echo "3. test_error_typo_keywords.c - Keyword typos"
    echo "4. test_error_missing_parentheses.c - Missing parentheses"
    echo "5. test_error_missing_braces.c - Missing braces"
    echo "6. test_error_complex.c - Complex multiple errors"
    echo "7. Run ALL error tests"
    echo ""
    read -p "Select error test (1-7): " error_choice
    
    if [ "$error_choice" = "1" ]; then
        echo "Testing: test_with_errors.c"
        python main.py test_with_errors.c
    elif [ "$error_choice" = "2" ]; then
        echo "Testing: test_error_missing_semicolon.c"
        python main.py test_error_missing_semicolon.c
    elif [ "$error_choice" = "3" ]; then
        echo "Testing: test_error_typo_keywords.c"
        python main.py test_error_typo_keywords.c
    elif [ "$error_choice" = "4" ]; then
        echo "Testing: test_error_missing_parentheses.c"
        python main.py test_error_missing_parentheses.c
    elif [ "$error_choice" = "5" ]; then
        echo "Testing: test_error_missing_braces.c"
        python main.py test_error_missing_braces.c
    elif [ "$error_choice" = "6" ]; then
        echo "Testing: test_error_complex.c"
        python main.py test_error_complex.c
    elif [ "$error_choice" = "7" ]; then
        echo "Running ALL error tests..."
        echo ""
        echo "========================================"
        echo "Test 1: test_with_errors.c"
        echo "========================================"
        python main.py test_with_errors.c
        echo ""
        echo "========================================"
        echo "Test 2: test_error_missing_semicolon.c"
        echo "========================================"
        python main.py test_error_missing_semicolon.c
        echo ""
        echo "========================================"
        echo "Test 3: test_error_typo_keywords.c"
        echo "========================================"
        python main.py test_error_typo_keywords.c
        echo ""
        echo "========================================"
        echo "Test 4: test_error_missing_parentheses.c"
        echo "========================================"
        python main.py test_error_missing_parentheses.c
        echo ""
        echo "========================================"
        echo "Test 5: test_error_missing_braces.c"
        echo "========================================"
        python main.py test_error_missing_braces.c
        echo ""
        echo "========================================"
        echo "Test 6: test_error_complex.c"
        echo "========================================"
        python main.py test_error_complex.c
        echo ""
        echo "========================================"
        echo "All error tests completed!"
        echo "========================================"
    else
        echo "Invalid selection"
    fi
elif [ "$choice" = "4" ]; then
    echo "Exit"
else
    echo "Invalid selection"
fi

read -p "Press Enter to continue..."
