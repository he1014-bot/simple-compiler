#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标代码生成模块（可选）
功能：将四元式中间代码翻译为x86-64汇编代码
"""

from typing import List, Dict, Set
from semantic import Quadruple

class CodeGenerator:
    """目标代码生成器（x86-64汇编�?"""
    
    def __init__(self, quadruples: List[Quadruple], symbol_table: Dict):
        self.quadruples = quadruples
        self.symbol_table = symbol_table
        self.assembly: List[str] = []  # 汇编代码�?
        self.label_count = 0           # 标号计数�?
        self.temp_count = 0            # 临时变量计数�?
        
        # 寄存器分配（简化版：使用固定寄存器�?
        self.registers = {
            'rax': '累加�?',
            'rbx': '基址寄存�?',
            'rcx': '计数寄存�?',
            'rdx': '数据寄存�?',
            'rsi': '源索�?',
            'rdi': '目的索引',
            'r8': '通用寄存�?8',
            'r9': '通用寄存�?9',
            'r10': '通用寄存�?10',
            'r11': '通用寄存�?11',
            'r12': '通用寄存�?12',
            'r13': '通用寄存�?13',
            'r14': '通用寄存�?14',
            'r15': '通用寄存�?15'
        }
        
        # 变量到寄存器的映�?
        self.var_to_reg: Dict[str, str] = {}
        # 寄存器使用状�?
        self.reg_used: Dict[str, bool] = {reg: False for reg in self.registers}
    
    def generate(self) -> List[str]:
        """生成汇编代码"""
        self._generate_header()
        
        for quad in self.quadruples:
            self._generate_quad(quad)
        
        self._generate_footer()
        
        return self.assembly
    
    def _generate_header(self):
        """生成汇编头部"""
        self.assembly.extend([
            "; =========================================",
            "; 小C语言编译器生成的x86-64汇编代码",
            "; 目标平台: Linux x86-64",
            "; 调用约定: System V AMD64 ABI",
            "; =========================================",
            "",
            "section .data",
            "    ; 数据�?"
        ])
        
        # 为所有变量分配存储空�?
        for name, info in self.symbol_table.items():
            if not info.get('is_temp', False):  # 非临时变�?
                self.assembly.append(f"    {name} dq 0  ; {info.get('type', 'int')}类型变量")
        
        self.assembly.extend([
            "",
            "section .bss",
            "    ; 未初始化数据�?",
            "    ; (暂无)",
            "",
            "section .text",
            "    global _start",
            "",
            "_start:",
            "    ; 程序入口�?",
            "    push rbp",
            "    mov rbp, rsp",
            ""
        ])
    
    def _generate_footer(self):
        """生成汇编尾部"""
        self.assembly.extend([
            "",
            "    ; 程序退�?",
            "    mov rsp, rbp",
            "    pop rbp",
            "    mov rax, 60     ; sys_exit",
            "    xor rdi, rdi    ; exit code 0",
            "    syscall",
            ""
        ])
    
    def _generate_quad(self, quad: Quadruple):
        """生成单个四元式的汇编代码"""
        op = quad.op
        arg1 = quad.arg1
        arg2 = quad.arg2
        result = quad.result
        
        # 添加注释
        self.assembly.append(f"    ; {quad}")
        
        if op == "=":
            # 赋值操�?
            self._generate_assignment(arg1, result)
        
        elif op in ["+", "-", "*", "/"]:
            # 算术运算
            self._generate_arithmetic(op, arg1, arg2, result)
        
        elif op in ["==", "!=", ">", "<", ">=", "<="]:
            # 关系运算
            self._generate_relation(op, arg1, arg2, result)
        
        elif op.startswith("j"):
            # 跳转指令
            self._generate_jump(op, arg1, arg2, result)
        
        elif op == "jump":
            # 无条件跳�?
            self.assembly.append(f"    jmp {result}")
        
        elif op == "label":
            # 标号定义
            self.assembly.append(f"{result}:")
        
        else:
            # 未知操作
            self.assembly.append(f"    ; 未知操作: {op}")
    
    def _generate_assignment(self, source, dest):
        """生成赋值语句汇�?"""
        if isinstance(source, int):
            # 常量赋�?
            self.assembly.append(f"    mov qword [{dest}], {source}")
        elif isinstance(source, str):
            # 变量到变量赋�?
            if source in self.symbol_table and dest in self.symbol_table:
                self.assembly.append(f"    mov rax, qword [{source}]")
                self.assembly.append(f"    mov qword [{dest}], rax")
            else:
                # 临时变量或寄存器
                self.assembly.append(f"    ; 赋�?: {dest} = {source}")
        else:
            self.assembly.append(f"    ; 无法处理的赋�?: {dest} = {source}")
    
    def _generate_arithmetic(self, op, arg1, arg2, result):
        """生成算术运算汇编"""
        # 加载第一个操作数到rax
        if isinstance(arg1, int):
            self.assembly.append(f"    mov rax, {arg1}")
        elif isinstance(arg1, str):
            self.assembly.append(f"    mov rax, qword [{arg1}]")
        else:
            self.assembly.append(f"    ; 无法处理的操作数1: {arg1}")
            return
        
        # 加载第二个操作数到rbx（如果需要）
        if arg2 is not None:
            if isinstance(arg2, int):
                self.assembly.append(f"    mov rbx, {arg2}")
            elif isinstance(arg2, str):
                self.assembly.append(f"    mov rbx, qword [{arg2}]")
            else:
                self.assembly.append(f"    ; 无法处理的操作数2: {arg2}")
                return
        
        # 生成运算指令
        if op == "+":
            if arg2 is not None:
                self.assembly.append("    add rax, rbx")
            else:
                self.assembly.append("    ; 错误: 加法需要两个操作数")
        elif op == "-":
            if arg2 is not None:
                self.assembly.append("    sub rax, rbx")
            else:
                self.assembly.append("    ; 错误: 减法需要两个操作数")
        elif op == "*":
            if arg2 is not None:
                self.assembly.append("    imul rax, rbx")
            else:
                self.assembly.append("    ; 错误: 乘法需要两个操作数")
        elif op == "/":
            if arg2 is not None:
                self.assembly.extend([
                    "    xor rdx, rdx      ; 清零rdx（被除数高位�?",
                    "    idiv rbx          ; 有符号除�?: rdx:rax / rbx"
                ])
            else:
                self.assembly.append("    ; 错误: 除法需要两个操作数")
        else:
            self.assembly.append(f"    ; 未知算术操作: {op}")
            return
        
        # 保存结果
        if result in self.symbol_table:
            self.assembly.append(f"    mov qword [{result}], rax")
        else:
            self.assembly.append(f"    ; 结果保存�?: {result}")
    
    def _generate_relation(self, op, arg1, arg2, result):
        """生成关系运算汇编"""
        # 加载操作�?
        if isinstance(arg1, int):
            self.assembly.append(f"    mov rax, {arg1}")
        elif isinstance(arg1, str):
            self.assembly.append(f"    mov rax, qword [{arg1}]")
        
        if isinstance(arg2, int):
            self.assembly.append(f"    mov rbx, {arg2}")
        elif isinstance(arg2, str):
            self.assembly.append(f"    mov rbx, qword [{arg2}]")
        
        # 比较操作
        self.assembly.append("    cmp rax, rbx")
        
        # 根据操作符设置条�?
        cond_map = {
            "==": "e",  # equal
            "!=": "ne", # not equal
            ">": "g",   # greater (signed)
            "<": "l",   # less (signed)
            ">=": "ge", # greater or equal
            "<=": "le"  # less or equal
        }
        
        if op in cond_map:
            cond = cond_map[op]
            # 设置结果�?0�?1�?
            label_true = f".L{self.label_count}_true"
            label_end = f".L{self.label_count}_end"
            self.label_count += 1
            
            self.assembly.extend([
                f"    j{cond} {label_true}  ; 如果条件成立",
                "    mov rax, 0           ; 条件不成立，结果�?0",
                f"    jmp {label_end}",
                f"{label_true}:",
                "    mov rax, 1           ; 条件成立，结果为1",
                f"{label_end}:"
            ])
            
            # 保存结果
            if result in self.symbol_table:
                self.assembly.append(f"    mov qword [{result}], rax")
        else:
            self.assembly.append(f"    ; 未知关系操作: {op}")
    
    def _generate_jump(self, op, arg1, arg2, target):
        """生成条件跳转汇编"""
        if op == "jump":
            # 无条件跳�?
            self.assembly.append(f"    jmp {target}")
            return
        
        # 条件跳转
        if arg1 is None or arg2 is None:
            # 简单条件跳转（基于单个值）
            if isinstance(arg1, str):
                self.assembly.append(f"    mov rax, qword [{arg1}]")
                self.assembly.append("    test rax, rax")
            
            # 根据操作符确定跳转条�?
            if op == "j!=":
                self.assembly.append(f"    jnz {target}")
            elif op == "j==":
                self.assembly.append(f"    jz {target}")
            else:
                self.assembly.append(f"    ; 未知跳转条件: {op}")
        else:
            # 基于比较的跳�?
            if isinstance(arg1, int):
                self.assembly.append(f"    mov rax, {arg1}")
            elif isinstance(arg1, str):
                self.assembly.append(f"    mov rax, qword [{arg1}]")
            
            if isinstance(arg2, int):
                self.assembly.append(f"    mov rbx, {arg2}")
            elif isinstance(arg2, str):
                self.assembly.append(f"    mov rbx, qword [{arg2}]")
            
            self.assembly.append("    cmp rax, rbx")
            
            # 映射跳转条件
            jump_map = {
                "j==": "je",
                "j!=": "jne",
                "j>": "jg",
                "j<": "jl",
                "j>=": "jge",
                "j<=": "jle"
            }
            
            if op in jump_map:
                self.assembly.append(f"    {jump_map[op]} {target}")
            else:
                self.assembly.append(f"    ; 未知跳转: {op}")
    
    def save_assembly(self, filename: str):
        """保存汇编代码到文�?"""
        with open(filename, 'w', encoding='utf-8') as f:
            for line in self.assembly:
                f.write(line + '\n')
        print(f"汇编代码已保存到: {filename}")
    
    def print_assembly(self):
        """打印汇编代码"""
        print("生成的x86-64汇编代码:")
        print("=" * 60)
        for line in self.assembly:
            print(line)
        print("=" * 60)


def test_codegen():
    """测试代码生成�?"""
    # 创建测试四元�?
    test_quads = [
        Quadruple("=", 5, None, "a"),
        Quadruple("=", 3, None, "b"),
        Quadruple("+", "a", "b", "t1"),
        Quadruple("=", "t1", None, "c"),
        Quadruple(">", "c", 7, "t2"),
        Quadruple("j!=", "t2", 0, "L1"),
        Quadruple("=", 0, None, "result"),
        Quadruple("jump", None, None, "L2"),
        Quadruple("label", None, None, "L1"),
        Quadruple("=", 1, None, "result"),
        Quadruple("label", None, None, "L2"),
    ]
    
    # 创建符号�?
    symbol_table = {
        "a": {"type": "int"},
        "b": {"type": "int"},
        "c": {"type": "int"},
        "result": {"type": "int"},
        "t1": {"type": "int", "is_temp": True},
        "t2": {"type": "int", "is_temp": True}
    }
    
    print("测试代码生成�?")
    print("=" * 60)
    
    generator = CodeGenerator(test_quads, symbol_table)
    assembly = generator.generate()
    generator.print_assembly()
    
    # 保存到文�?
    generator.save_assembly("test.asm")
    
    print("\n汇编代码说明:")
    print("1. 使用NASM语法")
    print("2. 目标平台: Linux x86-64")
    print("3. 调用约定: System V AMD64 ABI")
    print("4. 需要NASM和ld进行汇编和链�?")
    print("=" * 60)


if __name__ == "__main__":
    test_codegen()
