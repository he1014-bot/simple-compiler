import os
import sys

# Check if file exists
file_path = r"..\Ω≤Ω‚”√\error_test.c"
print(f"Checking file: {file_path}")
print(f"Absolute path: {os.path.abspath(file_path)}")
print(f"File exists: {os.path.exists(file_path)}")

# Try to read the file
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read(100)
        print(f"First 100 chars: {content}")
except Exception as e:
