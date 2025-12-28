#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码优化模块（可选）
功能：对四元式中间代码进行优化，包括常量折叠、公共子表达式消除等
"""

from typing import List, Dict, Set, Tuple
from semantic import Quadruple

class Optimizer:
    """代码优化器"""
    
    def __init__(self, quadruples: List[Quadruple]):
        self.quadruples = quadruples
        self.optimized_quads: List[Quadruple] = []
        self.constants: Dict[str, int] = {}  # 常量表：变量名 -> 常数值
    
    def optimize(self) -> List[Quadruple]:
        """执行优化，返回优化后的四元式列表"""
        if not self.quadruples:
            return []
        
        # 复制原始四元式
        self.optimized_quads = self.quadruples.copy()
        
        # 应用优化策略
        self._constant_folding()
        self._common_subexpression_elimination()
        self._dead_code_elimination()
        self._strength_reduction()
        
        return self.optimized_quads
    
    def _constant_folding(self):
        """常量折叠：计算编译时的常量表达式"""
        new_quads = []
        i = 0
        
        while i < len(self.optimized_quads):
            quad = self.optimized_quads[i]
            
            # 检查是否为赋值操作
            if quad.op == "=":
                # 如果右操作数是常量，记录到常量表
                if isinstance(quad.arg1, int):
                    self.constants[quad.result] = quad.arg1
                elif quad.arg1 in self.constants:
                    # 如果右操作数是已知常量变量
                    self.constants[quad.result] = self.constants[quad.arg1]
                new_quads.append(quad)
            
            # 检查是否为算术运算
            elif quad.op in ["+", "-", "*", "/"]:
                # 获取操作数值
                arg1_val = self._get_value(quad.arg1)
                arg2_val = self._get_value(quad.arg2)
                
                # 如果两个操作数都是常量，进行常量折叠
                if arg1_val is not None and arg2_val is not None:
                    try:
                        result_val = self._compute_constant(quad.op, arg1_val, arg2_val)
                        # 替换为赋值语句
                        new_quad = Quadruple("=", result_val, None, quad.result)
                        new_quads.append(new_quad)
                        self.constants[quad.result] = result_val
                    except ZeroDivisionError:
                        # 除零错误，保留原四元式
                        new_quads.append(quad)
                else:
                    new_quads.append(quad)
            
            # 检查是否为关系运算
            elif quad.op in ["==", "!=", ">", "<", ">=", "<="]:
                arg1_val = self._get_value(quad.arg1)
                arg2_val = self._get_value(quad.arg2)
                
                # 如果两个操作数都是常量，进行常量折叠
                if arg1_val is not None and arg2_val is not None:
                    result_val = self._compute_constant(quad.op, arg1_val, arg2_val)
                    new_quad = Quadruple("=", result_val, None, quad.result)
                    new_quads.append(new_quad)
                    self.constants[quad.result] = result_val
                else:
                    new_quads.append(quad)
            
            else:
                new_quads.append(quad)
            
            i += 1
        
        self.optimized_quads = new_quads
    
    def _get_value(self, operand: any) -> any:
        """获取操作数的值，如果是常量则返回数值，否则返回None"""
        if isinstance(operand, int):
            return operand
        elif isinstance(operand, str) and operand in self.constants:
            return self.constants[operand]
        return None
    
    def _compute_constant(self, op: str, arg1: int, arg2: int) -> int:
        """计算常量表达式"""
        if op == "+":
            return arg1 + arg2
        elif op == "-":
            return arg1 - arg2
        elif op == "*":
            return arg1 * arg2
        elif op == "/":
            return arg1 // arg2  # 整数除法
        elif op == "==":
            return 1 if arg1 == arg2 else 0
        elif op == "!=":
            return 1 if arg1 != arg2 else 0
        elif op == ">":
            return 1 if arg1 > arg2 else 0
        elif op == "<":
            return 1 if arg1 < arg2 else 0
        elif op == ">=":
            return 1 if arg1 >= arg2 else 0
        elif op == "<=":
            return 1 if arg1 <= arg2 else 0
        else:
            raise ValueError(f"未知操作符: {op}")
    
    def _common_subexpression_elimination(self):
        """公共子表达式消除"""
        # 记录已计算的表达式
        expressions: Dict[Tuple[str, any, any], str] = {}
        new_quads = []
        
        for quad in self.optimized_quads:
            if quad.op in ["+", "-", "*", "/", "==", "!=", ">", "<", ">=", "<="]:
                # 创建表达式键
                expr_key = (quad.op, quad.arg1, quad.arg2)
                
                # 检查是否已计算过相同表达式
                if expr_key in expressions:
                    # 用已存在的变量替换
                    existing_var = expressions[expr_key]
                    new_quad = Quadruple("=", existing_var, None, quad.result)
                    new_quads.append(new_quad)
                else:
                    # 记录新表达式
                    expressions[expr_key] = quad.result
                    new_quads.append(quad)
            else:
                new_quads.append(quad)
        
        self.optimized_quads = new_quads
    
    def _dead_code_elimination(self):
        """死代码消除：删除未被使用的赋值"""
        # 收集所有被使用的变量
        used_vars: Set[str] = set()
        
        # 第一遍：收集所有在表达式中使用的变量
        for quad in self.optimized_quads:
            if quad.arg1 and isinstance(quad.arg1, str) and not quad.arg1.startswith("t"):
                used_vars.add(quad.arg1)
            if quad.arg2 and isinstance(quad.arg2, str) and not quad.arg2.startswith("t"):
                used_vars.add(quad.arg2)
        
        # 第二遍：收集跳转目标
        for quad in self.optimized_quads:
            if quad.op == "label":
                used_vars.add(quad.result)
        
        # 第三遍：删除未被使用的临时变量赋值
        new_quads = []
        for quad in self.optimized_quads:
            if quad.op == "=" and quad.result.startswith("t"):
                # 检查临时变量是否被使用
                is_used = False
                for q in self.optimized_quads:
                    if (q.arg1 == quad.result or q.arg2 == quad.result or 
                        (q.op == "jump" and q.result == quad.result)):
                        is_used = True
                        break
                
                if is_used:
                    new_quads.append(quad)
                # 否则删除这个赋值（死代码）
            else:
                new_quads.append(quad)
        
        self.optimized_quads = new_quads
    
    def _strength_reduction(self):
        """强度削弱：用更快的操作替换慢速操作"""
        new_quads = []
        
        for quad in self.optimized_quads:
            if quad.op == "*":
                # 检查乘法操作数是否为2的幂
                if quad.arg2 == 2:
                    # 用左移替换乘以2
                    new_quad = Quadruple("<<", quad.arg1, 1, quad.result)
                    new_quads.append(new_quad)
                elif quad.arg1 == 2:
                    # 用左移替换乘以2
                    new_quad = Quadruple("<<", quad.arg2, 1, quad.result)
                    new_quads.append(new_quad)
                else:
                    new_quads.append(quad)
            elif quad.op == "/":
                # 检查除法操作数是否为2的幂
                if quad.arg2 == 2:
                    # 用右移替换除以2
                    new_quad = Quadruple(">>", quad.arg1, 1, quad.result)
                    new_quads.append(new_quad)
                else:
                    new_quads.append(quad)
            else:
                new_quads.append(quad)
        
        self.optimized_quads = new_quads
    
    def print_optimization_report(self, original_quads: List[Quadruple]):
        """打印优化报告"""
        print("代码优化报告:")
        print("=" * 60)
        print(f"原始四元式数量: {len(original_quads)}")
        print(f"优化后四元式数量: {len(self.optimized_quads)}")
        print(f"优化比例: {(1 - len(self.optimized_quads)/len(original_quads))*100:.1f}%")
        print("\n优化策略应用:")
        print("  - 常量折叠: ?")
        print("  - 公共子表达式消除: ?")
        print("  - 死代码消除: ?")
        print("  - 强度削弱: ?")
        print("=" * 60)


def test_optimizer():
    """测试优化器"""
    # 创建测试四元式
    test_quads = [
        Quadruple("=", 5, None, "a"),
        Quadruple("=", 3, None, "b"),
        Quadruple("+", "a", "b", "t1"),
        Quadruple("*", "t1", 2, "t2"),
        Quadruple("=", 2, None, "c"),
        Quadruple("*", "c", 2, "t3"),
        Quadruple("+", "t2", "t3", "t4"),
        Quadruple("=", "t4", None, "result"),
        Quadruple(">", "result", 20, "t5"),
        Quadruple("j!=", "t5", 0, "L1"),
        Quadruple("=", 0, None, "result"),
        Quadruple("label", None, None, "L1"),
    ]
    
    print("测试优化器")
    print("=" * 60)
    print("原始四元式:")
    for i, quad in enumerate(test_quads):
        print(f"{i:3d}: {quad}")
    
    optimizer = Optimizer(test_quads)
    optimized = optimizer.optimize()
    
    print("\n优化后四元式:")
    for i, quad in enumerate(optimized):
        print(f"{i:3d}: {quad}")
    
    optimizer.print_optimization_report(test_quads)


if __name__ == "__main__":
    test_optimizer()
