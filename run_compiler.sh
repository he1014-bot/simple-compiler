#!/bin/bash

echo "========================================"
echo "简单编译器启动脚本"
echo "========================================"
echo ""
echo "请选择启动模式："
echo "1. 交互式模式 (推荐)"
echo "2. 编译测试文件"
echo "3. 退出"
echo ""

read -p "请输入选项 (1-3): " choice

if [ "$choice" = "1" ]; then
    echo "启动交互式模式..."
    python main.py
elif [ "$choice" = "2" ]; then
    echo "可用的测试文件："
    echo "1. test_simple.c - 简单示例"
    echo "2. test2.c - 复杂示例（if-else和while）"
    echo "3. test_for.c - for循环示例"
    echo "4. test_full.c - 完整示例"
    echo ""
    read -p "请选择测试文件 (1-4): " test_choice
    
    if [ "$test_choice" = "1" ]; then
        python main.py test_simple.c
    elif [ "$test_choice" = "2" ]; then
        python main.py test2.c
    elif [ "$test_choice" = "3" ]; then
        python main.py test_for.c
    elif [ "$test_choice" = "4" ]; then
        python main.py test_full.c
    else
        echo "无效的选择"
    fi
elif [ "$choice" = "3" ]; then
    echo "退出"
else
    echo "无效的选择"
fi

read -p "按回车键继续..."
