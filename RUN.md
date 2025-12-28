# 简单编译器运行说明

## 项目概述
这是一个支持简化版C语言（小C语言）的编译器实现，包含词法分析、语法分析、语义分析与中间代码生成等核心模块。可选模块包括代码优化和目标代码生成。

## 系统要求
- Python 3.6 或更高版本
- 操作系统：Windows/Linux/macOS
- 磁盘空间：约10MB

## 项目结构
```
simple-compiler/
├── README.md                    # 项目说明
├── language_spec.md             # 详细语言规范
├── lexer.py                     # 词法分析器
├── parser.py                    # 语法分析器（递归下降）
├── semantic.py                  # 语义分析与中间代码生成
├── optimizer.py                 # 代码优化模块（可选）
├── codegen.py                   # 目标代码生成模块（可选）
├── main.py                      # 主程序入口
├── test.c                       # 测试用例
├── RUN.md                       # 运行说明（本文件）
└── output/                      # 输出目录（运行后生成）
```

## 快速开始

### 1. 交互式模式
```bash
cd simple-compiler
python main.py
```

在交互式模式中，您可以选择：
- 编译文件：输入源文件路径进行编译
- 测试示例：运行预定义的测试用例
- 查看帮助：了解编译器功能和使用方法
- 退出：结束程序

### 2. 命令行模式
```bash
# 编译单个文件
python main.py test.c

# 指定输出目录
python main.py test.c my_output
```

### 3. 直接运行测试
```bash
# 测试词法分析器
python lexer.py

# 测试语法分析器
python parser.py

# 测试语义分析器
python semantic.py

# 测试优化器（可选）
python optimizer.py

# 测试代码生成器（可选）
python codegen.py
```

## 输出文件说明
编译成功后，在输出目录中会生成以下文件：

1. **tokens.txt** - 词法分析结果（Token序列）
2. **ast.txt** - 抽象语法树
3. **symbol_table.txt** - 符号表
4. **quadruples.txt** - 四元式中间代码
5. **compile_report.txt** - 编译报告（统计信息）

如果编译过程中出现错误，会生成相应的错误文件：
- lexical_errors.txt - 词法错误
- syntax_errors.txt - 语法错误
- semantic_errors.txt - 语义错误

## 支持的语言特性

### 词法元素
- 关键字：`main`, `int`, `if`, `else`, `while`, `for`
- 标识符：字母开头，后跟字母或数字
- 常量：无符号整数
- 运算符：`+`, `-`, `*`, `/`, `=`, `>`, `<`, `>=`, `<=`, `==`, `!=`
- 分隔符：`(`, `)`, `{`, `}`, `;`, `,`
- 注释：`// 单行注释` 和 `/* 多行注释 */`

### 语法结构
1. 程序结构：`main(){ ... }`
2. 变量声明：`int a, b, c;`
3. 赋值语句：`a = 1;`
4. 算术表达式：`a + b * 2`
5. 关系表达式：`a > b`, `a == b`
6. 条件语句：`if (a > b) { ... }` 和 `if (a > b) { ... } else { ... }`
7. 循环语句：`while (a < 10) { ... }`
8. 复合语句：`{ ... }`

### 语义规则
1. 变量必须先声明后使用
2. 变量不能重复声明
3. 类型系统：只有`int`类型
4. 作用域：全局作用域

## 示例程序

### 简单示例
```c
main(){
    int a, b;
    a = 1;
    b = a + 2;
}
```

### 条件语句示例
```c
main(){
    int x, y;
    x = 10;
    y = 5;
    
    if (x > y) {
        x = y;
    } else {
        y = x;
    }
}
```

### 循环语句示例
```c
main(){
    int i, sum;
    i = 0;
    sum = 0;
    
    while (i < 10) {
        sum = sum + i;
        i = i + 1;
    }
}
```

## 错误处理
编译器能够检测并报告以下错误：

### 词法错误
- 非法字符
- 未结束的注释
- 数字格式错误

### 语法错误
- 缺少分号
- 括号不匹配
- 关键字拼写错误
- 表达式语法错误

### 语义错误
- 变量未声明
- 变量重复声明
- 类型不匹配

## 可选模块使用

### 代码优化
```python
from semantic import Quadruple
from optimizer import Optimizer

# 创建四元式列表
quads = [...]  # 您的四元式列表

# 执行优化
optimizer = Optimizer(quads)
optimized_quads = optimizer.optimize()

# 打印优化报告
optimizer.print_optimization_report(quads)
```

### 目标代码生成
```python
from codegen import CodeGenerator

# 创建四元式列表和符号表
quads = [...]  # 您的四元式列表
symbol_table = {...}  # 您的符号表

# 生成汇编代码
generator = CodeGenerator(quads, symbol_table)
assembly = generator.generate()

# 保存汇编代码
generator.save_assembly("output.asm")
```

## 故障排除

### 常见问题
1. **Python版本不兼容**
   - 确保使用Python 3.6或更高版本
   - 检查Python安装：`python --version`

2. **文件路径错误**
   - 使用绝对路径或相对路径
   - 确保文件存在且有读取权限

3. **内存不足**
   - 减少源文件大小
   - 关闭其他占用内存的程序

4. **输出目录权限**
   - 确保有写入权限
   - 尝试使用不同的输出目录

### 调试建议
1. 使用交互式模式逐步测试
2. 查看生成的错误文件了解具体错误
3. 从简单程序开始测试，逐步增加复杂度
4. 参考test.c中的测试用例

## 扩展开发

### 添加新特性
1. **新数据类型**：修改`language_spec.md`和`semantic.py`
2. **新控制结构**：修改`parser.py`和`semantic.py`
3. **新运算符**：修改`lexer.py`、`parser.py`和`semantic.py`
4. **优化算法**：修改`optimizer.py`
5. **新目标平台**：修改`codegen.py`

### 代码结构说明
- `lexer.py`：词法分析，将源代码转换为Token序列
- `parser.py`：语法分析，构建抽象语法树
- `semantic.py`：语义分析，生成四元式中间代码
- `optimizer.py`：代码优化，改进中间代码效率
- `codegen.py`：目标代码生成，产生汇编代码
- `main.py`：主程序，整合所有模块

## 许可证
本项目采用MIT许可证。详见README.md文件。

## 作者
计科2306 贺元

## 更新日志
- v1.0 (2025-12-22): 初始版本发布
  - 实现词法分析、语法分析、语义分析
  - 支持基本的小C语言语法
  - 生成四元式中间代码
  - 可选代码优化和目标代码生成模块
  - 完整的错误处理机制
  - 交互式和命令行两种使用模式
