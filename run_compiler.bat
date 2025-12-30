@echo off
REM Change to the directory where the batch file is located
cd /d "%~dp0"

echo ========================================
echo Simple Compiler Launcher
echo ========================================
echo.
echo Select mode:
echo 1. Interactive mode (Recommended)
echo 2. Compile test file
echo 3. Test error code fixing
echo 4. Exit
echo.

set /p choice="Enter option (1-4): "

if "%choice%"=="1" (
    echo Starting interactive mode...
    python main.py
    pause
) else if "%choice%"=="2" (
    echo Available test files:
    echo 1. test_simple.c - Simple example
    echo 2. test2.c - Complex example (if-else and while)
    echo 3. test_for.c - For loop example
    echo 4. test_full.c - Complete example
    echo.
    set /p test_choice="Select test file (1-4): "
    
    if "%test_choice%"=="1" (
        python main.py test_simple.c
    ) else if "%test_choice%"=="2" (
        python main.py test2.c
    ) else if "%test_choice%"=="3" (
        python main.py test_for.c
    ) else if "%test_choice%"=="4" (
        python main.py test_full.c
    ) else (
        echo Invalid selection
    )
    pause
) else if "%choice%"=="3" (
    echo ========================================
    echo Error Code Fixing Tests
    echo ========================================
    echo.
    echo Available error test files:
    echo 1. test_with_errors.c - Multiple error types
    echo 2. test_error_missing_semicolon.c - Missing semicolons
    echo 3. test_error_typo_keywords.c - Keyword typos
    echo 4. test_error_missing_parentheses.c - Missing parentheses
    echo 5. test_error_missing_braces.c - Missing braces
    echo 6. test_error_complex.c - Complex multiple errors
    echo 7. Run ALL error tests
    echo.
    set /p error_choice="Select error test (1-7): "
    
    if "%error_choice%"=="1" (
        echo Testing: test_with_errors.c
        python main.py test_with_errors.c
    ) else if "%error_choice%"=="2" (
        echo Testing: test_error_missing_semicolon.c
        python main.py test_error_missing_semicolon.c
    ) else if "%error_choice%"=="3" (
        echo Testing: test_error_typo_keywords.c
        python main.py test_error_typo_keywords.c
    ) else if "%error_choice%"=="4" (
        echo Testing: test_error_missing_parentheses.c
        python main.py test_error_missing_parentheses.c
    ) else if "%error_choice%"=="5" (
        echo Testing: test_error_missing_braces.c
        python main.py test_error_missing_braces.c
    ) else if "%error_choice%"=="6" (
        echo Testing: test_error_complex.c
        python main.py test_error_complex.c
    ) else if "%error_choice%"=="7" (
        echo Running ALL error tests...
        echo.
        echo ========================================
        echo Test 1: test_with_errors.c
        echo ========================================
        python main.py test_with_errors.c
        echo.
        echo ========================================
        echo Test 2: test_error_missing_semicolon.c
        echo ========================================
        python main.py test_error_missing_semicolon.c
        echo.
        echo ========================================
        echo Test 3: test_error_typo_keywords.c
        echo ========================================
        python main.py test_error_typo_keywords.c
        echo.
        echo ========================================
        echo Test 4: test_error_missing_parentheses.c
        echo ========================================
        python main.py test_error_missing_parentheses.c
        echo.
        echo ========================================
        echo Test 5: test_error_missing_braces.c
        echo ========================================
        python main.py test_error_missing_braces.c
        echo.
        echo ========================================
        echo Test 6: test_error_complex.c
        echo ========================================
        python main.py test_error_complex.c
        echo.
        echo ========================================
        echo All error tests completed!
        echo ========================================
    ) else (
        echo Invalid selection
    )
    pause
) else if "%choice%"=="4" (
    echo Exit
) else (
    echo Invalid selection
    pause
)
