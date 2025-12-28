# Simple Compiler Usage Guide

## How to Use the Compiler

### 1. Interactive Mode
```bash
cd simple-compiler
python main.py
```

In interactive mode, you can:
- Compile a file: Enter source file path
- Test examples: Run predefined test cases
- View help: Learn about compiler features
- Exit: End the program

### 2. Command Line Mode
```bash
# Compile a single file
python main.py test.c

# Specify output directory
python main.py test.c my_output
```

### 3. Direct Module Testing
```bash
# Test lexical analyzer
python lexer.py

# Test syntax analyzer
python parser.py

# Test semantic analyzer
python semantic.py

# Test optimizer (optional)
python optimizer.py

# Test code generator (optional)
python codegen.py
```

## What You Can Input

### Supported Language Features

#### 1. Program Structure
```c
main(){
    // Your code here
}
```

#### 2. Variable Declaration
```c
int a, b, c;
int x;
int y = 10;
```

#### 3. Assignment Statements
```c
a = 5;
b = a + 3;
c = (a + b) * 2;
```

#### 4. Arithmetic Expressions
```c
result = a + b;
result = a - b;
result = a * b;
result = a / b;
result = (a + b) * c - d / 2;
```

#### 5. Relational Expressions
```c
if (a > b) { ... }
if (a < b) { ... }
if (a >= b) { ... }
if (a <= b) { ... }
if (a == b) { ... }
if (a != b) { ... }
```

#### 6. Conditional Statements
```c
if (a > b) {
    max = a;
} else {
    max = b;
}

if (score >= 90) {
    grade = 1;
} else if (score >= 80) {
    grade = 2;
} else {
    grade = 3;
}
```

#### 7. Loop Statements
```c
while (i < 10) {
    sum = sum + i;
    i = i + 1;
}
```

#### 8. Compound Statements
```c
{
    int x, y;
    x = 1;
    y = 2;
    result = x + y;
}
```

## Example Programs

### Example 1: Simple Calculation
```c
main(){
    int a, b, sum;
    a = 10;
    b = 20;
    sum = a + b;
}
```

### Example 2: Factorial Calculation
```c
main(){
    int i, factorial;
    i = 1;
    factorial = 1;
    
    while (i <= 5) {
        factorial = factorial * i;
        i = i + 1;
    }
}
```

### Example 3: Find Maximum
```c
main(){
    int a, b, max;
    a = 15;
    b = 25;
    
    if (a > b) {
        max = a;
    } else {
        max = b;
    }
}
```

### Example 4: Complex Expression
```c
main(){
    int x, y, z, result;
    x = 2;
    y = 3;
    z = 4;
    result = x * y + z / 2 - 1;
}
```

## What the Compiler Produces

### Output Files (in output/ directory)

1. **tokens.txt** - Lexical analysis results (Token sequence)
2. **ast.txt** - Abstract syntax tree
3. **symbol_table.txt** - Symbol table with variable information
4. **quadruples.txt** - Intermediate code (quadruples)
5. **compile_report.txt** - Compilation statistics and summary

### Error Files (if errors occur)

1. **lexical_errors.txt** - Lexical errors (illegal characters, etc.)
2. **syntax_errors.txt** - Syntax errors (missing semicolons, etc.)
3. **semantic_errors.txt** - Semantic errors (undeclared variables, etc.)

## Quick Start

1. Create a C source file (e.g., `myprogram.c`):
```c
main(){
    int a, b, c;
    a = 5;
    b = 10;
    c = a + b * 2;
}
```

2. Compile it:
```bash
python main.py myprogram.c
```

3. Check the output:
```bash
# View tokens
cat output/tokens.txt

# View abstract syntax tree
cat output/ast.txt

# View intermediate code
cat output/quadruples.txt
```

## Supported Tokens

### Keywords
- `main`, `int`, `if`, `else`, `while`, `for`

### Identifiers
- Start with letter, followed by letters or digits
- Examples: `a`, `b`, `var1`, `result2`

### Constants
- Unsigned integers only
- Examples: `0`, `123`, `4567`

### Operators
- Arithmetic: `+`, `-`, `*`, `/`
- Assignment: `=`
- Relational: `>`, `<`, `>=`, `<=`, `==`, `!=`

### Delimiters
- Parentheses: `(`, `)`
- Braces: `{`, `}`
- Semicolon: `;`
- Comma: `,`

### Comments
- Single line: `// comment`
- Multi-line: `/* comment */`

## Error Examples

### Lexical Error (Illegal Character)
```c
main(){
    int a@b;  // @ is illegal character
}
```

### Syntax Error (Missing Semicolon)
```c
main(){
    int a
    a = 5  // Missing semicolon
}
```

### Semantic Error (Undeclared Variable)
```c
main(){
    a = 5;  // 'a' not declared
}
```

## Tips for Best Results

1. **Start simple**: Begin with basic programs and gradually add complexity
2. **Check syntax**: Ensure all statements end with semicolons
3. **Declare variables**: All variables must be declared before use
4. **Use proper indentation**: Makes your code more readable
5. **Test incrementally**: Test each feature separately before combining them

## Need Help?

1. Check the `RUN.md` file for detailed running instructions
2. Look at `test.c` for working examples
3. Run the compiler in interactive mode for guided usage
4. Test individual modules to understand each compilation phase

The compiler is designed for educational purposes to demonstrate the complete compilation process from source code to intermediate representation. It implements all core compiler phases with clear separation between modules.
