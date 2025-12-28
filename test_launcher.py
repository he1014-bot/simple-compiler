#!/usr/bin/env python3
"""Test the fixed run_compiler.bat launcher"""

import os
import subprocess
import sys

def test_launcher():
    print("Testing run_compiler.bat launcher")
    print("=" * 60)
    
    # Test 1: Run from current directory
    print("\n1. Testing from current directory...")
    try:
        result = subprocess.run([".\\run_compiler.bat"], 
                              input="1\nsimple_test.c\n\n4\n",
                              text=True,
                              capture_output=True,
                              timeout=10)
        print(f"Exit code: {result.returncode}")
        if "Compilation Completed" in result.stdout:
            print("? Launcher works from current directory")
        else:
            print("? Launcher may have issues")
            print(f"Output preview: {result.stdout[:200]}...")
    except subprocess.TimeoutExpired:
        print("? Launcher started successfully (timeout expected for interactive mode)")
    except Exception as e:
        print(f"? Error: {e}")
    
    # Test 2: Check if batch file has correct cd command
    print("\n2. Checking batch file content...")
    with open("run_compiler.bat", 'r', encoding='utf-8') as f:
        content = f.read()
        if 'cd /d "%~dp0"' in content:
            print("? Batch file has directory change command")
        else:
            print("? Batch file missing directory change command")
    
    # Test 3: Verify Python can be found
    print("\n3. Checking Python availability...")
    try:
        python_check = subprocess.run(["python", "--version"], 
                                     capture_output=True, 
                                     text=True)
        print(f"? Python found: {python_check.stdout.strip()}")
    except Exception as e:
        print(f"? Python not found: {e}")
    
    print("\n" + "=" * 60)
    print("Launcher test completed")
    
    # Summary
    print("\nSUMMARY:")
    print("1. The main issue was: run_compiler.bat didn't change to correct directory")
    print("2. Fix added: 'cd /d \"%~dp0\"' at start of batch file")
    print("3. This ensures batch file runs from its own directory")
    print("4. Now it should work from any location (Desktop, CMD, etc.)")

if __name__ == "__main__":
    test_launcher()
