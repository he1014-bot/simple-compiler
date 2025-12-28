#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syntax analyzer module
Function: Parse token sequence, check syntax, build abstract syntax tree
"""

from typing import List, Optional, Any
from lexer import Token, TokenType

class ASTNode:
    """Abstract Syntax Tree Node"""
    def __init__(self, node_type: str, value: Any = None, children: List['ASTNode'] = None):
        self.node_type = node_type      # Node type
        self.value = value              # Node value
        self.children = children if children is not None else []  # Child nodes
    
    def add_child(self, child: 'ASTNode'):
        """Add child node"""
        self.children.append(child)
    
    def __repr__(self):
        return f"ASTNode({self.node_type}, value={self.value}, children={len(self.children)})"
    
    def __str__(self):
        return self._to_string()
    
    def _to_string(self, level: int = 0) -> str:
        """Convert to string representation"""
        indent = "  " * level
        result = f"{indent}{self.node_type}"
        if self.value is not None:
            result += f" [{self.value}]"
        
        if self.children:
            result += ":\n"
            for child in self.children:
                result += child._to_string(level + 1) + "\n"
        else:
            result += "\n"
        
        return result.rstrip()

class Parser:
    """Syntax analyzer (recursive descent)"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0               # Current token position
        self.current_token = None       # Current token
        self.ast = None                 # Abstract syntax tree
        self.errors: List[str] = []     # Error list
        
        # Initialize: get first token
        if tokens:
            self.current_token = tokens[0]
    
    def parse(self) -> Optional[ASTNode]:
        """Parse program, return AST root node"""
        try:
            self.ast = self._program()
            return self.ast
        except Exception as e:
            self.errors.append(f"Parsing error: {e}")
            return None
    
    def _advance(self):
        """Move to next token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def _match(self, expected_type: TokenType) -> bool:
        """Check if current token matches expected type"""
        if self.current_token and self.current_token.type == expected_type:
            return True
        return False
    
    def _consume(self, expected_type: TokenType, error_msg: str = "") -> bool:
        """Consume token of expected type, report error if mismatch"""
        if self._match(expected_type):
            self._advance()
            return True
        else:
            if not error_msg:
                error_msg = f"Expected {expected_type.name}, got {self.current_token.type if self.current_token else 'EOF'}"
            self.errors.append(f"Syntax error at line {self.current_token.line if self.current_token else '?'}: {error_msg}")
            return False
    
    def _program(self) -> ASTNode:
        """<program> -> main(){<declaration_sequence><statement_sequence>}"""
        node = ASTNode("Program")
        
        # main keyword
        if not self._consume(TokenType.MAIN, "Expected 'main' keyword"):
            return node
        
        # '('
        if not self._consume(TokenType.LPAREN, "Expected '(' after 'main'"):
            return node
        
        # ')'
        if not self._consume(TokenType.RPAREN, "Expected ')' after '('"):
            return node
        
        # '{'
        if not self._consume(TokenType.LBRACE, "Expected '{' after 'main()'"):
            return node
        
        # <declaration_sequence>
        decl_seq = self._declaration_sequence()
        if decl_seq:
            node.add_child(decl_seq)
        
        # <statement_sequence>
        stmt_seq = self._statement_sequence()
        if stmt_seq:
            node.add_child(stmt_seq)
        
        # '}'
        if not self._consume(TokenType.RBRACE, "Expected '}' at end of program"):
            return node
        
        return node
    
    def _declaration_sequence(self) -> Optional[ASTNode]:
        """<declaration_sequence> -> <declaration_sequence><declaration> | <declaration> | ε"""
        node = ASTNode("DeclarationSequence")
        has_declarations = False
        
        while self._match(TokenType.INT):
            decl = self._declaration()
            if decl:
                node.add_child(decl)
                has_declarations = True
        
        if has_declarations:
            return node
        else:
            return None  # ε (empty)
    
    def _declaration(self) -> Optional[ASTNode]:
        """<declaration> -> int <identifier_list>;"""
        node = ASTNode("Declaration")
        
        # int keyword
        if not self._consume(TokenType.INT, "Expected 'int' keyword"):
            return None
        
        # <identifier_list>
        id_list = self._identifier_list()
        if id_list:
            node.add_child(id_list)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after declaration"):
            return None
        
        return node
    
    def _identifier_list(self) -> ASTNode:
        """<identifier_list> -> <identifier>,<identifier_list> | <identifier>"""
        node = ASTNode("IdentifierList")
        
        # First identifier
        if self._match(TokenType.IDENTIFIER):
            id_node = ASTNode("Identifier", self.current_token.value)
            node.add_child(id_node)
            self._advance()
        else:
            self.errors.append(f"Expected identifier at line {self.current_token.line if self.current_token else '?'}")
            return node
        
        # More identifiers separated by commas
        while self._match(TokenType.COMMA):
            self._advance()  # Consume comma
            
            if self._match(TokenType.IDENTIFIER):
                id_node = ASTNode("Identifier", self.current_token.value)
                node.add_child(id_node)
                self._advance()
            else:
                self.errors.append(f"Expected identifier after comma at line {self.current_token.line if self.current_token else '?'}")
                break
        
        return node
    
    def _statement_sequence(self) -> Optional[ASTNode]:
        """<statement_sequence> -> <statement_sequence><statement> | <statement>"""
        node = ASTNode("StatementSequence")
        has_statements = False
        
        while self._is_statement_start():
            stmt = self._statement()
            if stmt:
                node.add_child(stmt)
                has_statements = True
        
        if has_statements:
            return node
        else:
            return None  # ε (empty)
    
    def _is_statement_start(self) -> bool:
        """Check if current token can start a statement"""
        if not self.current_token:
            return False
        
        # Statement can start with: identifier (assignment), if, while, for, '{'
        return (self._match(TokenType.IDENTIFIER) or 
                self._match(TokenType.IF) or 
                self._match(TokenType.WHILE) or 
                self._match(TokenType.FOR) or
                self._match(TokenType.LBRACE))
    
    def _statement(self) -> Optional[ASTNode]:
        """<statement> -> <if_statement> | <while_statement> | <for_statement> | <compound_statement> | <assignment_statement>"""
        if self._match(TokenType.IF):
            return self._if_statement()
        elif self._match(TokenType.WHILE):
            return self._while_statement()
        elif self._match(TokenType.FOR):
            return self._for_statement()
        elif self._match(TokenType.LBRACE):
            return self._compound_statement()
        elif self._match(TokenType.IDENTIFIER):
            return self._assignment_statement()
        else:
            self.errors.append(f"Unexpected token at line {self.current_token.line if self.current_token else '?'}: {self.current_token}")
            return None
    
    def _if_statement(self) -> ASTNode:
        """<if_statement> -> if (<expression>) <compound_statement>; | if (<expression>) <compound_statement> else <compound_statement>;"""
        node = ASTNode("IfStatement")
        
        # if keyword
        if not self._consume(TokenType.IF, "Expected 'if' keyword"):
            return node
        
        # '('
        if not self._consume(TokenType.LPAREN, "Expected '(' after 'if'"):
            return node
        
        # <expression>
        expr = self._expression()
        if expr:
            node.add_child(expr)
        
        # ')'
        if not self._consume(TokenType.RPAREN, "Expected ')' after expression"):
            return node
        
        # <compound_statement>
        then_block = self._compound_statement()
        if then_block:
            node.add_child(then_block)
        
        # Optional else part
        if self._match(TokenType.ELSE):
            self._advance()  # Consume else
            
            else_block = self._compound_statement()
            if else_block:
                node.add_child(else_block)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after if statement"):
            return node
        
        return node
    
    def _while_statement(self) -> ASTNode:
        """<while_statement> -> while (<expression>) <compound_statement>;"""
        node = ASTNode("WhileStatement")
        
        # while keyword
        if not self._consume(TokenType.WHILE, "Expected 'while' keyword"):
            return node
        
        # '('
        if not self._consume(TokenType.LPAREN, "Expected '(' after 'while'"):
            return node
        
        # <expression>
        expr = self._expression()
        if expr:
            node.add_child(expr)
        
        # ')'
        if not self._consume(TokenType.RPAREN, "Expected ')' after expression"):
            return node
        
        # <compound_statement>
        block = self._compound_statement()
        if block:
            node.add_child(block)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after while statement"):
            return node
        
        return node
    
    def _for_statement(self) -> ASTNode:
        """<for_statement> -> for (<expression>;<expression>;<expression>) <compound_statement>;"""
        node = ASTNode("ForStatement")
        
        # for keyword
        if not self._consume(TokenType.FOR, "Expected 'for' keyword"):
            return node
        
        # '('
        if not self._consume(TokenType.LPAREN, "Expected '(' after 'for'"):
            return node
        
        # First expression (initialization)
        if not self._match(TokenType.SEMICOLON):
            expr1 = self._expression()
            if expr1:
                node.add_child(expr1)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after first expression in for"):
            return node
        
        # Second expression (condition)
        if not self._match(TokenType.SEMICOLON):
            expr2 = self._expression()
            if expr2:
                node.add_child(expr2)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after second expression in for"):
            return node
        
        # Third expression (increment)
        if not self._match(TokenType.RPAREN):
            expr3 = self._expression()
            if expr3:
                node.add_child(expr3)
        
        # ')'
        if not self._consume(TokenType.RPAREN, "Expected ')' after for expressions"):
            return node
        
        # <compound_statement>
        block = self._compound_statement()
        if block:
            node.add_child(block)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after for statement"):
            return node
        
        return node
    
    def _compound_statement(self) -> ASTNode:
        """<compound_statement> -> {<statement_sequence>}"""
        node = ASTNode("CompoundStatement")
        
        # '{'
        if not self._consume(TokenType.LBRACE, "Expected '{' for compound statement"):
            return node
        
        # <statement_sequence>
        stmt_seq = self._statement_sequence()
        if stmt_seq:
            node.add_child(stmt_seq)
        
        # '}'
        if not self._consume(TokenType.RBRACE, "Expected '}' at end of compound statement"):
            return node
        
        return node
    
    def _assignment_statement(self) -> ASTNode:
        """<assignment_statement> -> <expression>;"""
        node = ASTNode("AssignmentStatement")
        
        # <expression>
        expr = self._expression()
        if expr:
            node.add_child(expr)
        
        # ';'
        if not self._consume(TokenType.SEMICOLON, "Expected ';' after assignment"):
            return node
        
        return node
    
    def _expression(self) -> Optional[ASTNode]:
        """<expression> -> <identifier>=<arithmetic_expression> | <boolean_expression>"""
        # Try assignment expression first
        if self._match(TokenType.IDENTIFIER):
            # Look ahead to see if next token is '='
            next_pos = self.position + 1
            if next_pos < len(self.tokens) and self.tokens[next_pos].type == TokenType.ASSIGN:
                node = ASTNode("AssignmentExpression")
                
                # Identifier
                id_node = ASTNode("Identifier", self.current_token.value)
                node.add_child(id_node)
                self._advance()
                
                # '='
                self._advance()  # Consume '='
                
                # <arithmetic_expression>
                arith_expr = self._arithmetic_expression()
                if arith_expr:
                    node.add_child(arith_expr)
                
                return node
        
        # If not assignment, try boolean expression
        return self._boolean_expression()
    
    def _boolean_expression(self) -> Optional[ASTNode]:
        """<boolean_expression> -> <arithmetic_expression> | <arithmetic_expression><relational_operator><arithmetic_expression>"""
        # First arithmetic expression
        left = self._arithmetic_expression()
        if not left:
            return None
        
        # Check for relational operator
        if (self._match(TokenType.GT) or self._match(TokenType.LT) or 
            self._match(TokenType.GE) or self._match(TokenType.LE) or
            self._match(TokenType.EQ) or self._match(TokenType.NE)):
            
            node = ASTNode("BooleanExpression")
            node.add_child(left)
            
            # Relational operator
            op_node = ASTNode("RelationalOperator", self.current_token.lexeme)
            node.add_child(op_node)
            self._advance()
            
            # Second arithmetic expression
            right = self._arithmetic_expression()
            if right:
                node.add_child(right)
            
            return node
        else:
            # Just arithmetic expression
            return left
    
    def _arithmetic_expression(self) -> Optional[ASTNode]:
        """<arithmetic_expression> -> <arithmetic_expression>+<term> | <arithmetic_expression>-<term> | <term>"""
        # Start with first term
        node = self._term()
        if not node:
            return None
        
        # Handle + and - operators
        while self._match(TokenType.PLUS) or self._match(TokenType.MINUS):
            op_node = ASTNode("ArithmeticExpression")
            op_node.add_child(node)
            
            # Operator
            operator = ASTNode("Operator", self.current_token.lexeme)
            op_node.add_child(operator)
            self._advance()
            
            # Next term
            next_term = self._term()
            if next_term:
                op_node.add_child(next_term)
            
            node = op_node
        
        return node
    
    def _term(self) -> Optional[ASTNode]:
        """<term> -> <term>*<factor> | <term>/<factor> | <factor>"""
        # Start with first factor
        node = self._factor()
        if not node:
            return None
        
        # Handle * and / operators
        while self._match(TokenType.MULTIPLY) or self._match(TokenType.DIVIDE):
            op_node = ASTNode("Term")
            op_node.add_child(node)
            
            # Operator
            operator = ASTNode("Operator", self.current_token.lexeme)
            op_node.add_child(operator)
            self._advance()
            
            # Next factor
            next_factor = self._factor()
            if next_factor:
                op_node.add_child(next_factor)
            
            node = op_node
        
        return node
    
    def _factor(self) -> Optional[ASTNode]:
        """<factor> -> <identifier> | <number> | (<arithmetic_expression>)"""
        if self._match(TokenType.IDENTIFIER):
            node = ASTNode("Identifier", self.current_token.value)
            self._advance()
            return node
        
        elif self._match(TokenType.NUMBER):
            node = ASTNode("Number", self.current_token.value)
            self._advance()
            return node
        
        elif self._match(TokenType.LPAREN):
            self._advance()  # Consume '('
            
            expr = self._arithmetic_expression()
            if not expr:
                self.errors.append(f"Expected expression after '(' at line {self.current_token.line if self.current_token else '?'}")
                return None
            
            if not self._consume(TokenType.RPAREN, "Expected ')' after expression"):
                return None
