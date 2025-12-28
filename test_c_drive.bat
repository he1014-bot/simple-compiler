@echo off
REM Test script for C drive file compilation
echo Testing C drive file compilation
echo ========================================

REM First, show the test file location
echo Test file: C:\Users\heyua\Desktop\c_drive_test.c
echo.

REM Option 1: Direct Python compilation
echo 1. Direct Python compilation:
python main.py "C:\Users\heyua\Desktop\c_drive_test.c"
echo.

REM Option 2: Using run_compiler.bat (interactive mode)
echo 2. To use run_compiler.bat:
echo    - Run: run_compiler.bat
echo    - Select option 1 (Interactive mode)
echo    - When asked for source file path, enter:
echo      C:\Users\heyua\Desktop\c_drive_test.c
echo    - Press Enter for default output directory
echo.

REM Option 3: Create another test file
echo 3. Create another test file on C drive:
set /p create="Create another test file? (y/n): "
if /i "%create%"=="y" (
    python -c "with open(r'C:\Users\heyua\Desktop\test2.c', 'w') as f: f.write('main(){ int a; a = 42; }')"
    echo Created: C:\Users\heyua\Desktop\test2.c
)
echo.

echo Test completed!
pause
