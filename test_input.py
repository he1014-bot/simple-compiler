# Test input function
print("Test input function")
print("=" * 40)

# Test 1: Simple input
try:
    test1 = input("Enter number 1: ")
    print(f"You entered: '{test1}'")
except Exception as e:
    print(f"Input error: {e}")

# Test 2: Input with spaces
try:
    test2 = input("Enter option (1-4): ").strip()
    print(f"You entered: '{test2}'")
except Exception as e:
    print(f"Input error: {e}")

print("Test completed")
