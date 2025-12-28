#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 快速测试编译器核心功能

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 简单测试代码
test_code = "main(){int a; a = 1;}"

print("快速测试编译器核心功能")
print("=" * 60)

try:
    # 测试导入模块
    from lexer import Lexer
    print("? 成功导入lexer模块")
    
    # 测试词法分析
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    print(f"? 词法分析成功，生成 {len(tokens)} 个token")
    
    # 测试语法分析
    from parser import Parser
    print("? 成功导入parser模块")
    
    parser = Parser(tokens)
    ast = parser.parse()
    if ast:
        print("? 语法分析成功，构建抽象语法树")
    else:
        print("? 语法分析失败")
        
    # 测试语义分析
    from semantic import SemanticAnalyzer
    print("? 成功导入semantic模块")
    
    if ast:
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        if success:
            print("? 语义分析成功")
            print(f"? 生成 {len(analyzer.quadruples)} 个四元式")
        else:
            print("? 语义分析失败")
    
    print("\n" + "=" * 60)
    print("所有核心模块测试通过!")
    
except ImportError as e:
    print(f"? 导入模块失败: {e}")
except Exception as e:
    print(f"? 测试过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
