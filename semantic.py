#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Analysis and Intermediate Code Generation Module
Function: Perform semantic checks on syntax tree, generate quadruple intermediate code
"""

from typing import List, Dict, Optional, Any
from parser import ASTNode

class SymbolTable:
    """Symbol Table Class"""
    def __init__(self):
        self.symbols: Dict[str, Dict] = {}  # symbol name -> attribute dictionary
        self.next_temp = 1                   # next temporary variable number
    
    def add_symbol(self, name: str, symbol_type: str = "int", **kwargs):
        """Add symbol to symbol table"""
        if name in self.symbols:
            raise SemanticError(f"Symbol '{name}' redeclared")
        
        self.symbols[name] = {
            "type": symbol_type,
            "name": name,
            **kwargs
        }
    
    def lookup(self, name: str) -> Optional[Dict]:
        """Look up symbol"""
        return self.symbols.get(name)
    
    def exists(self, name: str) -> bool:
        """Check if symbol exists"""
        return name in self.symbols
    
    def new_temp(self) -> str:
        """Generate new temporary variable name"""
        temp_name = f"t{self.next_temp}"
        self.next_temp += 1
        self.add_symbol(temp_name, "int", is_temp=True)
        return temp_name
    
    def print_table(self):
        """Print symbol table"""
        print("Symbol Table:")
        print("=" * 60)
        print(f"{'Name':<10} {'Type':<10} {'Attributes':<20}")
        print("-" * 60)
        for name, info in self.symbols.items():
            attrs = ", ".join(f"{k}={v}" for k, v in info.items() if k not in ["name", "type"])
            print(f"{name:<10} {info['type']:<10} {attrs:<20}")
        print("=" * 60)

class Quadruple:
    """Quadruple Class"""
    def __init__(self, op: str, arg1: Any, arg2: Any, result: Any):
        self.op = op          # operator
        self.arg1 = arg1      # first operand
        self.arg2 = arg2      # second operand
        self.result = result  # result
    
    def __repr__(self):
        arg1_str = self.arg1 if self.arg1 is not None else "_"
        arg2_str = self.arg2 if self.arg2 is not None else "_"
        return f"({self.op}, {arg1_str}, {arg2_str}, {self.result})"
    
    def __str__(self):
        return self.__repr__()

class SemanticError(Exception):
    """Semantic Error"""
    def __init__(self, message: str, node: ASTNode = None):
        super().__init__(f"Semantic error: {message}")
        self.node = node

class SemanticAnalyzer:
    """Semantic Analyzer"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.quadruples: List[Quadruple] = []  # quadruple list
        self.errors: List[str] = []            # error message list
        self.next_label = 1                    # next label number
    
    def analyze(self, ast: ASTNode) -> bool:
        """Perform semantic analysis, return success status"""
        try:
            self._analyze_program(ast)
            return len(self.errors) == 0
        except SemanticError as e:
            self.errors.append(str(e))
            return False
    
    def _analyze_program(self, node: ASTNode):
        """Analyze program node"""
        if node.node_type != "Program":
            raise SemanticError(f"Expected Program node, got {node.node_type}", node)
        
        # Analyze all child nodes
        for child in node.children:
            if child.node_type == "DeclarationSequence":
                self._analyze_decl_list(child)
            elif child.node_type == "StatementSequence":
                self._analyze_stmt_list(child)
    
    def _analyze_decl_list(self, node: ASTNode):
        """Analyze declaration list"""
        for child in node.children:
            if child.node_type == "Declaration":
                self._analyze_declaration(child)
    
    def _analyze_declaration(self, node: ASTNode):
        """Analyze declaration statement"""
        # In our grammar, declaration node has only one child: IdentifierList
        # Get identifier list
        id_list_node = next((c for c in node.children if c.node_type == "IdentifierList"), None)
        if not id_list_node:
            raise SemanticError("Declaration missing identifier list", node)
        
        # Add all identifiers to symbol table
        for child in id_list_node.children:
            if child.node_type == "Identifier":
                self.symbol_table.add_symbol(child.value, "int")
    
    def _analyze_stmt_list(self, node: ASTNode):
        """Analyze statement list"""
        for child in node.children:
            self._analyze_statement(child)
    
    def _analyze_statement(self, node: ASTNode):
        """Analyze statement"""
        if node.node_type == "AssignmentStatement":
            self._analyze_assignment_stmt(node)
        elif node.node_type == "IfStatement":
            self._analyze_if_stmt(node)
        elif node.node_type == "WhileStatement":
            self._analyze_while_stmt(node)
        elif node.node_type == "ForStatement":
            self._analyze_for_stmt(node)
        elif node.node_type == "CompoundStatement":
            self._analyze_compound_stmt(node)
        elif node.node_type == "EmptyStatement":
            pass  # empty statement, do nothing
        else:
            raise SemanticError(f"Unknown statement type: {node.node_type}", node)
    
    def _analyze_assignment_stmt(self, node: ASTNode):
        """Analyze assignment statement"""
        # Get expression node
        expr_node = next((c for c in node.children if c.node_type in ["AssignmentExpression", "BoolExpression"]), None)
        if not expr_node:
            raise SemanticError("Assignment statement missing expression", node)
        
        # Analyze expression and generate quadruple
        result = self._analyze_expression(expr_node)
        
        # If it's an assignment expression, result is already handled in expression
        # Here we just need to ensure expression analysis is complete
    
    def _analyze_if_stmt(self, node: ASTNode):
        """Analyze if statement"""
        # Get condition expression
        expr_node = next((c for c in node.children if c.node_type in ["AssignmentExpression", "BooleanExpression"]), None)
        if not expr_node:
            raise SemanticError("if statement missing condition expression", node)
        
        # Analyze condition expression
        cond_result = self._analyze_expression(expr_node)
        
        # Generate conditional jump quadruple
        false_label = self._new_label()
        end_label = self._new_label()
        
        # Generate jump based on condition result
        if expr_node.node_type == "BooleanExpression" and len(expr_node.children) > 1:
            # Boolean expression with relational operator
            # cond_result is a Quadruple object
            self.quadruples.append(Quadruple(f"j{cond_result.op}", cond_result.arg1, cond_result.arg2, false_label))
        else:
            # Simple expression, need to compare with 0
            temp = self.symbol_table.new_temp()
            self.quadruples.append(Quadruple("!=", cond_result, 0, temp))
            self.quadruples.append(Quadruple("j==", temp, 0, false_label))
        
        # Get then statement (first compound statement after condition)
        then_stmt = None
        for child in node.children:
            if child.node_type == "CompoundStatement":
                then_stmt = child
                break
        
        if then_stmt:
            self._analyze_compound_stmt(then_stmt)
        
        # Jump to end
        self.quadruples.append(Quadruple("jump", None, None, end_label))
        
        # Generate false label
        self.quadruples.append(Quadruple("label", None, None, false_label))
        
        # Get else statement (second compound statement)
        compound_stmts = [c for c in node.children if c.node_type == "CompoundStatement"]
        if len(compound_stmts) > 1:
            else_stmt = compound_stmts[1]
            self._analyze_compound_stmt(else_stmt)
        
        # Generate end label
        self.quadruples.append(Quadruple("label", None, None, end_label))
    
    def _analyze_while_stmt(self, node: ASTNode):
        """Analyze while statement"""
        # Generate labels
        start_label = self._new_label()
        end_label = self._new_label()
        
        # Start label
        self.quadruples.append(Quadruple("label", None, None, start_label))
        
        # Get condition expression
        expr_node = next((c for c in node.children if c.node_type in ["AssignmentExpression", "BooleanExpression"]), None)
        if not expr_node:
            raise SemanticError("while statement missing condition expression", node)
        
        # Analyze condition expression
        cond_result = self._analyze_expression(expr_node)
        
        # Generate conditional jump to end
        if expr_node.node_type == "BooleanExpression" and len(expr_node.children) > 1:
            # Boolean expression with relational operator
            # cond_result is a Quadruple object
            self.quadruples.append(Quadruple(f"j!{cond_result.op}", cond_result.arg1, cond_result.arg2, end_label))
        else:
            # Simple expression, need to compare with 0
            temp = self.symbol_table.new_temp()
            self.quadruples.append(Quadruple("==", cond_result, 0, temp))
            self.quadruples.append(Quadruple("j!=", temp, 0, end_label))
        
        # Get loop body
        body_stmt = next((c for c in node.children if c.node_type == "CompoundStatement"), None)
        if body_stmt:
            self._analyze_compound_stmt(body_stmt)
        
        # Jump back to start
        self.quadruples.append(Quadruple("jump", None, None, start_label))
        
        # End label
        self.quadruples.append(Quadruple("label", None, None, end_label))
    
    def _analyze_for_stmt(self, node: ASTNode):
        """Analyze for statement"""
        # For statement has 4 children: init_expr, cond_expr, iter_expr, body
        if len(node.children) >= 4:
            # Initialization expression (first child)
            init_expr = node.children[0]
            if init_expr:
                self._analyze_expression(init_expr)
            
            # Start label
            start_label = self._new_label()
            end_label = self._new_label()
            
            self.quadruples.append(Quadruple("label", None, None, start_label))
            
            # Condition expression (second child)
            cond_expr = node.children[1]
            if cond_expr:
                cond_result = self._analyze_expression(cond_expr)
                
                # Generate conditional jump to end
                if cond_expr.node_type == "BooleanExpression" and len(cond_expr.children) > 1:
                    # cond_result is a Quadruple object
                    self.quadruples.append(Quadruple(f"j!{cond_result.op}", cond_result.arg1, cond_result.arg2, end_label))
                else:
                    temp = self.symbol_table.new_temp()
                    self.quadruples.append(Quadruple("==", cond_result, 0, temp))
                    self.quadruples.append(Quadruple("j!=", temp, 0, end_label))
            
            # Loop body (fourth child)
            body_stmt = node.children[3]
            if body_stmt and body_stmt.node_type == "CompoundStatement":
                self._analyze_compound_stmt(body_stmt)
            
            # Iteration expression (third child)
            iter_expr = node.children[2]
            if iter_expr:
                self._analyze_expression(iter_expr)
            
            # Jump back to start
            self.quadruples.append(Quadruple("jump", None, None, start_label))
            
            # End label
            self.quadruples.append(Quadruple("label", None, None, end_label))
        else:
            raise SemanticError("For statement has incorrect number of children", node)
    
    def _analyze_compound_stmt(self, node: ASTNode):
        """Analyze compound statement"""
        # Find statement sequence
        stmt_seq = next((c for c in node.children if c.node_type == "StatementSequence"), None)
        if stmt_seq:
            self._analyze_stmt_list(stmt_seq)
    
    def _analyze_expression(self, node: ASTNode) -> Any:
        """Analyze expression, return result (variable name or temporary variable)"""
        if node.node_type == "AssignmentExpression":
            return self._analyze_assign_expr(node)
        elif node.node_type == "BooleanExpression":
            return self._analyze_bool_expr(node)
        elif node.node_type == "ArithExpression":
            return self._analyze_arith_expr(node)
        elif node.node_type == "Term":
            return self._analyze_term(node)
        elif node.node_type == "Factor":
            return self._analyze_factor(node)
        else:
            raise SemanticError(f"Unknown expression type: {node.node_type}", node)
    
    def _analyze_assign_expr(self, node: ASTNode) -> str:
        """Analyze assignment expression"""
        # Get left-hand identifier (first child)
        if len(node.children) < 2:
            raise SemanticError("Assignment expression missing right-hand expression", node)
        
        id_node = node.children[0]
        if id_node.node_type != "Identifier":
            raise SemanticError("Assignment expression missing left-hand identifier", node)
        
        # Check if identifier is declared
        if not self.symbol_table.exists(id_node.value):
            raise SemanticError(f"Identifier '{id_node.value}' not declared", id_node)
        
        # Get right-hand expression (second child)
        right_expr = node.children[1]
        
        # Analyze right-hand expression
        if right_expr.node_type == "ArithmeticExpression":
            right_value = self._analyze_arith_expr(right_expr)
        elif right_expr.node_type == "Identifier":
            # Check if identifier is declared
            if not self.symbol_table.exists(right_expr.value):
                raise SemanticError(f"Identifier '{right_expr.value}' not declared", right_expr)
            right_value = right_expr.value
        elif right_expr.node_type == "Number":
            right_value = right_expr.value
        else:
            # Try to analyze as expression
            right_value = self._analyze_expression(right_expr)
        
        # Generate assignment quadruple
        self.quadruples.append(Quadruple("=", right_value, None, id_node.value))
        
        return id_node.value
    
    def _analyze_bool_expr(self, node: ASTNode) -> Quadruple:
        """Analyze boolean expression"""
        if len(node.children) == 1:
            # Single arithmetic expression
            arith_result = self._analyze_arith_expr(node.children[0])
            # Create temporary variable to store comparison result
            temp = self.symbol_table.new_temp()
            self.quadruples.append(Quadruple("!=", arith_result, 0, temp))
            return Quadruple("!=", arith_result, 0, temp)
        elif len(node.children) == 3:
            # Relational expression
            left_expr = node.children[0]
            rel_op_node = node.children[1]
            right_expr = node.children[2]
            
            # Analyze left and right expressions
            # They could be identifiers or numbers
            if left_expr.node_type == "Identifier":
                left_result = left_expr.value
                # Check if identifier is declared
                if not self.symbol_table.exists(left_result):
                    raise SemanticError(f"Identifier '{left_result}' not declared", left_expr)
            elif left_expr.node_type == "Number":
                left_result = left_expr.value
            else:
                left_result = self._analyze_arith_expr(left_expr)
            
            if right_expr.node_type == "Identifier":
                right_result = right_expr.value
                # Check if identifier is declared
                if not self.symbol_table.exists(right_result):
                    raise SemanticError(f"Identifier '{right_result}' not declared", right_expr)
            elif right_expr.node_type == "Number":
                right_result = right_expr.value
            else:
                right_result = self._analyze_arith_expr(right_expr)
            
            # Get relational operator
            rel_op = rel_op_node.value
            
            # Return Quadruple object without generating actual quadruple
            # The actual jump quadruple will be generated by the caller (if/while statement)
            return Quadruple(rel_op, left_result, right_result, None)
        else:
            raise SemanticError("Boolean expression format error", node)
    
    def _analyze_arith_expr(self, node: ASTNode) -> str:
        """Analyze arithmetic expression"""
        # In our parser, ArithmeticExpression has 3 children: left, operator, right
        if len(node.children) == 3:
            left_child = node.children[0]
            op_child = node.children[1]
            right_child = node.children[2]
            
            # Analyze left and right expressions
            if left_child.node_type == "Identifier":
                left_result = left_child.value
                # Check if identifier is declared
                if not self.symbol_table.exists(left_result):
                    raise SemanticError(f"Identifier '{left_result}' not declared", left_child)
            elif left_child.node_type == "Number":
                left_result = left_child.value
            elif left_child.node_type == "ArithmeticExpression":
                left_result = self._analyze_arith_expr(left_child)
            else:
                left_result = self._analyze_expression(left_child)
            
            if right_child.node_type == "Identifier":
                right_result = right_child.value
                # Check if identifier is declared
                if not self.symbol_table.exists(right_result):
                    raise SemanticError(f"Identifier '{right_result}' not declared", right_child)
            elif right_child.node_type == "Number":
                right_result = right_child.value
            elif right_child.node_type == "ArithmeticExpression":
                right_result = self._analyze_arith_expr(right_child)
            else:
                right_result = self._analyze_expression(right_child)
            
            # Generate quadruple
            temp = self.symbol_table.new_temp()
            self.quadruples.append(Quadruple(op_child.value, left_result, right_result, temp))
            
            return temp
        else:
            # Single operand
            return self._analyze_expression(node.children[0])
    
    def _analyze_arith_expr_prime(self, node: ASTNode, left_value: str) -> str:
        """Analyze arithmetic expression'"""
        if not node.children:
            return left_value
        
        # Get operator
        op_node = node.children[0]
        op = op_node.value
        
        # Analyze term
        term_result = self._analyze_term(node.children[1])
        
        # Generate quadruple
        temp = self.symbol_table.new_temp()
        self.quadruples.append(Quadruple(op, left_value, term_result, temp))
        
        # Recursively process remaining part
        if len(node.children) > 2 and node.children[2].node_type == "ArithExpressionPrime":
            return self._analyze_arith_expr_prime(node.children[2], temp)
        
        return temp
    
    def _analyze_term(self, node: ASTNode) -> str:
        """Analyze term"""
        # In our parser, Term may have 3 children: left, operator, right
        if len(node.children) == 3:
            left_child = node.children[0]
            op_child = node.children[1]
            right_child = node.children[2]
            
            # Analyze left and right expressions
            if left_child.node_type == "Identifier":
                left_result = left_child.value
                # Check if identifier is declared
                if not self.symbol_table.exists(left_result):
                    raise SemanticError(f"Identifier '{left_result}' not declared", left_child)
            elif left_child.node_type == "Number":
                left_result = left_child.value
            elif left_child.node_type == "Factor":
                left_result = self._analyze_factor(left_child)
            else:
                left_result = self._analyze_expression(left_child)
            
            if right_child.node_type == "Identifier":
                right_result = right_child.value
                # Check if identifier is declared
                if not self.symbol_table.exists(right_result):
                    raise SemanticError(f"Identifier '{right_result}' not declared", right_child)
            elif right_child.node_type == "Number":
                right_result = right_child.value
            elif right_child.node_type == "Factor":
                right_result = self._analyze_factor(right_child)
            else:
                right_result = self._analyze_expression(right_child)
            
            # Generate quadruple
            temp = self.symbol_table.new_temp()
            self.quadruples.append(Quadruple(op_child.value, left_result, right_result, temp))
            
            return temp
        else:
            # Single factor
            return self._analyze_factor(node.children[0])
    
    def _analyze_term_prime(self, node: ASTNode, left_value: str) -> str:
        """Analyze term'"""
        if not node.children:
            return left_value
        
        # Get operator
        op_node = node.children[0]
        op = op_node.value
        
        # Analyze factor
        factor_result = self._analyze_factor(node.children[1])
        
        # Generate quadruple
        temp = self.symbol_table.new_temp()
        self.quadruples.append(Quadruple(op, left_value, factor_result, temp))
        
        # Recursively process remaining part
        if len(node.children) > 2 and node.children[2].node_type == "TermPrime":
            return self._analyze_term_prime(node.children[2], temp)
        
        return temp
    
    def _analyze_factor(self, node: ASTNode) -> str:
        """Analyze factor"""
        if not node.children:
            raise SemanticError("Factor is empty", node)
        
        child = node.children[0]
        
        if child.node_type == "Identifier":
            # Check if identifier is declared
            if not self.symbol_table.exists(child.value):
                raise SemanticError(f"Identifier '{child.value}' not declared", child)
            return child.value
        
        elif child.node_type == "Number":
            # Numeric constant
            return child.value
        
        elif child.node_type == "ArithExpression":
            # Parenthesized expression
            return self._analyze_arith_expr(child)
        
        else:
            raise SemanticError(f"Illegal factor type: {child.node_type}", child)
    
    def _new_label(self) -> str:
        """Generate new label"""
        label = f"L{self.next_label}"
        self.next_label += 1
        return label
    
    def print_quadruples(self):
        """Print quadruple sequence"""
        print("Quadruple Intermediate Code:")
        print("=" * 60)
        for i, quad in enumerate(self.quadruples):
            print(f"{i:3d}: {quad}")
        print("=" * 60)
    
    def print_errors(self):
        """Print all semantic errors"""
        if self.errors:
            print("Semantic analysis errors:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("Semantic analysis completed, no errors found.")


def test_semantic():
    """Test semantic analyzer"""
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
    
    # Lexical analysis
    from lexer import Lexer
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    if lexer.errors:
        lexer.print_errors()
        return
    
    # Syntax analysis
    from parser import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.errors:
        parser.print_errors()
        return
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    analyzer.print_errors()
    
    if success:
        analyzer.symbol_table.print_table()
        analyzer.print_quadruples()
    
    return analyzer


if __name__ == "__main__":
    test_semantic()
