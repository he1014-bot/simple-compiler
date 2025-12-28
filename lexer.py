#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lexical analyzer module
Function: Scan source code, identify tokens, generate token sequence
"""

import re
from enum import Enum
from typing import List, Tuple, Optional

class TokenType(Enum):
    """Token type codes"""
    # Keywords
    MAIN = 1
    INT = 2
    IF = 3
    ELSE = 4
    WHILE = 5
    FOR = 6
    
    # Identifiers and constants
    IDENTIFIER = 10
    NUMBER = 11
    
    # Operators
    PLUS = 21        # +
    MINUS = 22       # -
    MULTIPLY = 23    # *
    DIVIDE = 24      # /
    ASSIGN = 25      # =
    GT = 26          # >
    LT = 27          # <
    GE = 28          # >=
    LE = 29          # <=
    EQ = 30          # ==
    NE = 31          # !=
    
    # Delimiters
    LPAREN = 41      # (
    RPAREN = 42      # )
    LBRACE = 43      # {
    RBRACE = 44      # }
    SEMICOLON = 45   # ;
    COMMA = 46       # ,
    
    # Special
    EOF = 99         # End of file

class Token:
    """Token class"""
    def __init__(self, token_type: TokenType, lexeme: str = "", value: any = None, line: int = 1, column: int = 1):
        self.type = token_type
        self.lexeme = lexeme          # Token string
        self.value = value            # Attribute value (e.g., number value, symbol table pointer)
        self.line = line              # Line number
        self.column = column          # Column number
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', value={self.value}, line={self.line}, col={self.column})"
    
    def __str__(self):
        return f"({self.type.value}, {self.value if self.value is not None else self.lexeme})"

class LexerError(Exception):
    """Lexical analysis error"""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexical error [line {line}, column {column}]: {message}")
        self.line = line
        self.column = column

class Lexer:
    """Lexical analyzer"""
    
    # Keyword mapping
    KEYWORDS = {
        'main': TokenType.MAIN,
        'int': TokenType.INT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR
    }
    
    # Operator and delimiter mapping
    OPERATORS = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '=': TokenType.ASSIGN,
        '>': TokenType.GT,
        '<': TokenType.LT,
        '>=': TokenType.GE,
        '<=': TokenType.LE,
        '==': TokenType.EQ,
        '!=': TokenType.NE,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
        ';': TokenType.SEMICOLON,
        ',': TokenType.COMMA
    }
    
    # Regular expression patterns
    PATTERNS = [
        (r'//[^\n]*', None),               # Single line comment
        (r'/\*.*?\*/', None),              # Multi-line comment (non-greedy)
        (r'[ \t\r]+', None),               # Whitespace (excluding newline)
        (r'\n', None),                     # Newline (handled separately to update line number)
        (r'[0-9]+', 'NUMBER'),             # Unsigned integer
        (r'[a-zA-Z][a-zA-Z0-9]*', 'ID'),   # Identifier
        (r'>=|<=|==|!=', 'OPERATOR'),      # Two-character operators
        (r'[+\-*/=><;{},()]', 'OPERATOR'), # Single character operators and delimiters
    ]
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0                  # Current position
        self.line = 1                      # Current line number
        self.column = 1                    # Current column number
        self.tokens: List[Token] = []      # Generated token list
        self.errors: List[str] = []        # Error message list
    
    def tokenize(self) -> List[Token]:
        """Perform lexical analysis, return token list"""
        while self.position < len(self.source):
            token = self._next_token()
            if token:
                self.tokens.append(token)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens
    
    def _next_token(self) -> Optional[Token]:
        """Get next token"""
        if self.position >= len(self.source):
            return None
        
        # Try to match all patterns
        for pattern, token_type in self.PATTERNS:
            regex = re.compile(pattern)
            match = regex.match(self.source, self.position)
            
            if match:
                text = match.group()
                start_pos = self.position
                self.position = match.end()
                
                # Update line and column numbers
                if pattern == r'\n':
                    self.line += 1
                    self.column = 1
                    return None
                elif pattern.startswith(r'//') or pattern.startswith(r'/\*'):
                    # Comment, skip
                    # Count newlines in comment to update line number
                    newlines = text.count('\n')
                    if newlines > 0:
                        self.line += newlines
                        self.column = 1
                    else:
                        self.column += len(text)
                    return None
                elif pattern == r'[ \t\r]+':
                    # Whitespace
                    self.column += len(text)
                    return None
                
                # Calculate token start column
                token_column = self.column
                self.column += len(text)
                
                # Create token based on token type
                if token_type == 'NUMBER':
                    return self._create_number_token(text, token_column)
                elif token_type == 'ID':
                    return self._create_identifier_token(text, token_column)
                elif token_type == 'OPERATOR':
                    return self._create_operator_token(text, token_column)
        
        # No pattern matched, report error
        char = self.source[self.position]
        error_msg = f"Illegal character: '{char}' (ASCII: {ord(char)})"
        self.errors.append(f"Line {self.line} column {self.column}: {error_msg}")
        
        # Skip illegal character and continue analysis
        self.position += 1
        self.column += 1
        return None
    
    def _create_number_token(self, text: str, column: int) -> Token:
        """Create number token"""
        try:
            value = int(text)
            return Token(TokenType.NUMBER, text, value, self.line, column)
        except ValueError:
            error_msg = f"Number format error: {text}"
            self.errors.append(f"Line {self.line} column {column}: {error_msg}")
            return Token(TokenType.NUMBER, text, 0, self.line, column)
    
    def _create_identifier_token(self, text: str, column: int) -> Token:
        """Create identifier or keyword token"""
        # Check if it's a keyword
        if text in self.KEYWORDS:
            return Token(self.KEYWORDS[text], text, None, self.line, column)
        else:
            # Identifier, attribute value is symbol table pointer (using identifier name for now)
            return Token(TokenType.IDENTIFIER, text, text, self.line, column)
    
    def _create_operator_token(self, text: str, column: int) -> Token:
        """Create operator or delimiter token"""
        if text in self.OPERATORS:
            return Token(self.OPERATORS[text], text, None, self.line, column)
        else:
            # Should not happen since regex matched
            error_msg = f"Unknown operator: {text}"
            self.errors.append(f"Line {self.line} column {column}: {error_msg}")
            return Token(TokenType.ASSIGN, text, None, self.line, column)
    
    def print_tokens(self):
        """Print all tokens"""
        print("Lexical analysis result:")
        print("=" * 60)
        for i, token in enumerate(self.tokens):
            if token.type != TokenType.EOF:
                print(f"{i:3d}: {token}")
        print(f"{len(self.tokens):3d}: (99, EOF)")
        print("=" * 60)
    
    def print_errors(self):
        """Print all errors"""
        if self.errors:
            print("Lexical analysis errors:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("Lexical analysis completed, no errors found.")

def test_lexer():
    """Test lexical analyzer"""
    test_code = """main(){
    int a, b;
    a = 1;
    b = a + 2;
    if (a > b) {
        a = b;
    } else {
        b = a;
    }
    while (a < 10) {
        a = a + 1;
    }
}"""
    
    print("Test source code:")
    print(test_code)
    print("\n" + "="*60 + "\n")
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    lexer.print_tokens()
    lexer.print_errors()
    
    return tokens

if __name__ == "__main__":
    test_lexer()
