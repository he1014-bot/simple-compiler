# Test full path compilation
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import compile_file

def test_full_path():
    print("Testing full path compilation")
    print("=" * 60)
    
    # Test 1: Relative path
    test1 = "test_simple.c"
    print(f"\n1. Test relative path: {test1}")
    if os.path.exists(test1):
        success = compile_file(test1, "test_output_1")
        print(f"Result: {'Success' if success else 'Failed'}")
    else:
        print(f"File not found: {test1}")
    
    # Test 2: Full path (current project)
    test2 = os.path.join(os.getcwd(), "test2.c")
    print(f"\n2. Test full path: {test2}")
    if os.path.exists(test2):
        success = compile_file(test2, "test_output_2")
        print(f"Result: {'Success' if success else 'Failed'}")
    else:
        print(f"File not found: {test2}")
    
    # Test 3: Create temp file in temp directory
    import tempfile
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test.c")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("main(){ int temp; temp = 123; }")
    
    print(f"\n3. Test temp file path: {temp_file}")
    if os.path.exists(temp_file):
        success = compile_file(temp_file, "test_output_3")
        print(f"Result: {'Success' if success else 'Failed'}")
        
        # Clean up
        os.remove(temp_file)
        print(f"Cleaned temp file: {temp_file}")
    else:
        print(f"Temp file creation failed: {temp_file}")
    
    print("\n" + "=" * 60)
    print("Full path test completed")

if __name__ == "__main__":
    test_full_path()
