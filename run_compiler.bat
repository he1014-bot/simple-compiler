@echo off
REM Change to the directory where the batch file is located
cd /d "%~dp0"

:main_menu
cls
echo ========================================
echo      Simple Compiler Launcher v2.0
echo ========================================
echo.
echo [MAIN MENU]
echo 1. Interactive Mode (Recommended for beginners)
echo 2. Compile Standard Test Files
echo 3. Test Error Code Fixing Feature
echo 4. Run All Tests (Standard + Error Tests)
echo 5. View Help and Documentation
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto interactive_mode
if "%choice%"=="2" goto standard_tests
if "%choice%"=="3" goto error_tests
if "%choice%"=="4" goto all_tests
if "%choice%"=="5" goto help_menu
if "%choice%"=="6" goto exit_program
echo Invalid selection! Please try again.
pause
goto main_menu

:interactive_mode
cls
echo ========================================
echo      Interactive Mode
echo ========================================
echo.
echo Starting interactive mode...
echo.
python main.py
pause
goto main_menu

:standard_tests
cls
echo ========================================
echo      Standard Test Files
echo ========================================
echo.
echo [BASIC TESTS]
echo 1. test_simple.c    - Simple variable declarations and assignments
echo 2. test2.c          - Complex example with if-else and while loops
echo.
echo [ADVANCED TESTS]
echo 3. test_for.c       - For loop example
echo 4. test_full.c      - Complete program with all features
echo.
echo [OTHER OPTIONS]
echo 5. Return to Main Menu
echo.
set /p test_choice="Select test file (1-5): "

if "%test_choice%"=="1" (
    echo Compiling: test_simple.c
    python main.py test_simple.c
) else if "%test_choice%"=="2" (
    echo Compiling: test2.c
    python main.py test2.c
) else if "%test_choice%"=="3" (
    echo Compiling: test_for.c
    python main.py test_for.c
) else if "%test_choice%"=="4" (
    echo Compiling: test_full.c
    python main.py test_full.c
) else if "%test_choice%"=="5" (
    goto main_menu
) else (
    echo Invalid selection!
)
pause
goto standard_tests

:error_tests
cls
echo ========================================
echo      Error Code Fixing Tests
echo ========================================
echo.
echo These tests demonstrate the code fixing feature that automatically
echo detects and fixes common errors in C source code.
echo.
echo [SINGLE ERROR TYPE TESTS]
echo 1. Missing Semicolons      - test_error_missing_semicolon.c
echo 2. Keyword Typos           - test_error_typo_keywords.c
echo 3. Missing Parentheses     - test_error_missing_parentheses.c
echo 4. Missing Braces          - test_error_missing_braces.c
echo.
echo [COMPLEX ERROR TESTS]
echo 5. Multiple Error Types    - test_with_errors.c
echo 6. Complex Multiple Errors - test_error_complex.c
echo.
echo [BATCH TESTING]
echo 7. Run ALL Error Tests
echo.
echo [OTHER OPTIONS]
echo 8. Return to Main Menu
echo.
set /p error_choice="Select test (1-8): "

if "%error_choice%"=="1" (
    echo Testing: Missing Semicolons
    python main.py test_error_missing_semicolon.c output
) else if "%error_choice%"=="2" (
    echo Testing: Keyword Typos
    python main.py test_error_typo_keywords.c output
) else if "%error_choice%"=="3" (
    echo Testing: Missing Parentheses
    python main.py test_error_missing_parentheses.c output
) else if "%error_choice%"=="4" (
    echo Testing: Missing Braces
    python main.py test_error_missing_braces.c output
) else if "%error_choice%"=="5" (
    echo Testing: Multiple Error Types
    python main.py test_with_errors.c output
) else if "%error_choice%"=="6" (
    echo Testing: Complex Multiple Errors
    python main.py test_error_complex.c output
) else if "%error_choice%"=="7" (
    echo Running ALL error tests...
    echo.
    echo ========================================
    echo Test 1: Missing Semicolons
    echo ========================================
    python main.py test_error_missing_semicolon.c output
    echo.
    echo ========================================
    echo Test 2: Keyword Typos
    echo ========================================
    python main.py test_error_typo_keywords.c output
    echo.
    echo ========================================
    echo Test 3: Missing Parentheses
    echo ========================================
    python main.py test_error_missing_parentheses.c output
    echo.
    echo ========================================
    echo Test 4: Missing Braces
    echo ========================================
    python main.py test_error_missing_braces.c output
    echo.
    echo ========================================
    echo Test 5: Multiple Error Types
    echo ========================================
    python main.py test_with_errors.c output
    echo.
    echo ========================================
    echo Test 6: Complex Multiple Errors
    echo ========================================
    python main.py test_error_complex.c output
    echo.
    echo ========================================
    echo All error tests completed!
    echo ========================================
) else if "%error_choice%"=="8" (
    goto main_menu
) else (
    echo Invalid selection!
)
pause
goto error_tests

:all_tests
cls
echo ========================================
echo      Running All Tests
echo ========================================
echo.
echo This will run all standard and error tests.
echo Output will be saved to the 'output' directory.
echo.
set /p confirm="Are you sure? (y/n): "
if /i not "%confirm%"=="y" goto main_menu

echo.
echo ========================================
echo      Standard Tests
echo ========================================
echo.
echo Test 1: Simple Example
python main.py test_simple.c
echo.
echo Test 2: Complex Example
python main.py test2.c
echo.
echo Test 3: For Loop Example
python main.py test_for.c
echo.
echo Test 4: Complete Example
python main.py test_full.c
echo.
echo ========================================
echo      Error Tests
echo ========================================
echo.
echo Test 5: Missing Semicolons
python main.py test_error_missing_semicolon.c output
echo.
echo Test 6: Keyword Typos
python main.py test_error_typo_keywords.c output
echo.
echo Test 7: Missing Parentheses
python main.py test_error_missing_parentheses.c output
echo.
echo Test 8: Missing Braces
python main.py test_error_missing_braces.c output
echo.
echo Test 9: Multiple Error Types
python main.py test_with_errors.c output
echo.
echo Test 10: Complex Multiple Errors
python main.py test_error_complex.c output
echo.
echo ========================================
echo      All Tests Completed!
echo ========================================
echo.
echo Check the 'output' directory for results.
pause
goto main_menu

:help_menu
cls
echo ========================================
echo      Help and Documentation
echo ========================================
echo.
echo [COMPILER FEATURES]
echo 1. Code Error Detection and Fixing
echo    - Automatically detects and fixes common C code errors
echo    - Supports 6 error types: missing semicolons, keyword typos,
echo      missing parentheses, missing braces, for loop errors,
echo      variable declaration errors
echo.
echo 2. Full Compilation Pipeline
echo    - Lexical Analysis (tokens.txt)
echo    - Syntax Analysis (ast.txt)
echo    - Semantic Analysis (symbol_table.txt)
echo    - Intermediate Code Generation (quadruples.txt)
echo    - x86-64 Assembly Code Generation (assembly.asm)
echo.
echo [OUTPUT FILES]
echo - output/ directory contains all generated files
echo - For error-free code: original_code.c + standard outputs
echo - For code with errors: fixed_code.c + error_report.txt + standard outputs
echo.
echo [TEST FILES]
echo - Standard tests: Demonstrate correct code compilation
echo - Error tests: Demonstrate error detection and fixing
echo.
pause
goto main_menu

:exit_program
echo.
echo Thank you for using Simple Compiler!
echo Goodbye!
timeout /t 2 >nul
exit
