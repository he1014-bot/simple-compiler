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
echo 3. Exit
echo.

set /p choice="Enter option (1-3): "

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
    echo Exit
) else (
    echo Invalid selection
    pause
)
