#!/usr/bin/env python3
"""#!/usr/bin/env python3

测试运行脚本
支持运行所有测试、特定测试类别、生成覆盖率报告等
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    print(f"🚀 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ 执行成功!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ 执行失败!")
        print(f"错误代码: {e.returncode}")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")你
            print(e.stderr)
        return False

def main():
    """主函数"""
    print("🧪 高考考点分析系统 - 测试套件")
    print("="*50)
    
    # 检查是否在正确的目录
    if not Path("main.py").exists():
        print("❌ 错误: 请在backend目录下运行此脚本")
        sys.exit(1)
    
    # 检查测试目录
    if not Path("tests").exists():
        print("❌ 错误: 测试目录不存在")
        sys.exit(1)
    
    # 显示测试选项
    print("\n📋 可用测试选项:")
    print("1. 运行所有测试")
    print("2. 运行单元测试")
    print("3. 运行API测试")
    print("4. 运行认证测试")
    print("5. 运行模型测试")
    print("6. 生成覆盖率报告")
    print("7. 运行特定测试文件")
    print("0. 退出")
    
    while True:
        try:
            choice = input("\n请选择测试选项 (0-7): ").strip()
            
            if choice == "0":
                print("👋 退出测试")
                break
            elif choice == "1":
                success = run_command("python -m pytest tests/ -v", "运行所有测试")
            elif choice == "2":
                success = run_command("python -m pytest tests/ -m unit -v", "运行单元测试")
            elif choice == "3":
                success = run_command("python -m pytest tests/ -m api -v", "运行API测试")
            elif choice == "4":
                success = run_command("python -m pytest tests/test_auth.py -v", "运行认证测试")
            elif choice == "5":
                success = run_command("python -m pytest tests/test_models.py -v", "运行模型测试")
            elif choice == "6":
                # 安装覆盖率工具
                subprocess.run("pip install pytest-cov", shell=True, check=True)
                success = run_command(
                    "python -m pytest tests/ --cov=. --cov-report=html --cov-report=term",
                    "生成覆盖率报告"
                )
                if success:
                    print("\n📊 覆盖率报告已生成在 htmlcov/ 目录")
            elif choice == "7":
                test_file = input("请输入测试文件名 (例如: test_auth.py): ").strip()
                if test_file:
                    success = run_command(f"python -m pytest tests/{test_file} -v", f"运行测试文件 {test_file}")
                else:
                    print("❌ 文件名不能为空")
            else:
                print("❌ 无效选择，请输入 0-7")
                continue
            
            if success:
                print("\n🎉 测试完成!")
            else:
                print("\n💥 测试失败!")
            
            # 询问是否继续
            continue_test = input("\n是否继续运行其他测试? (y/n): ").strip().lower()
            if continue_test != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出测试")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            break

if __name__ == "__main__":
    main() 