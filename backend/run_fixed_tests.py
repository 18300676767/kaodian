#!/usr/bin/env python3
"""
修复后的测试执行脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
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
            print("错误输出:")
            print(e.stderr)
        return False

def main():
    """主函数"""
    print("�� 高考考点分析系统 - 修复后测试执行")
    print("="*60)
    
    # 检查是否在正确的目录
    if not Path("main.py").exists():
        print("❌ 错误: 请在backend目录下运行此脚本")
        sys.exit(1)
    
    # 检查测试目录
    if not Path("tests").exists():
        print("❌ 错误: 测试目录不存在")
        sys.exit(1)
    
    print("\n📋 开始执行修复后的测试...")
    
    # 1. 运行认证测试
    print("\n�� 步骤 1: 运行认证测试")
    auth_success = run_command("python -m pytest tests/test_auth.py -v", "认证测试")
    
    # 2. 运行API测试
    print("\n🌐 步骤 2: 运行API测试")
    api_success = run_command("python -m pytest tests/test_integration.py -v", "API集成测试")
    
    # 3. 运行所有测试
    print("\n�� 步骤 3: 运行所有测试")
    all_success = run_command("python -m pytest tests/ -v", "所有测试")
    
    # 4. 生成测试报告
    print("\n�� 步骤 4: 生成测试覆盖率报告")
    coverage_success = run_command(
        "python -m pytest tests/ --cov=. --cov-report=term-missing --cov-report=html",
        "生成覆盖率报告"
    )
    
    # 总结
    print("\n" + "="*60)
    print("📋 测试执行总结:")
    print(f"认证测试: {'✅ 通过' if auth_success else '❌ 失败'}")
    print(f"API测试: {'✅ 通过' if api_success else '❌ 失败'}")
    print(f"所有测试: {'✅ 通过' if all_success else '❌ 失败'}")
    print(f"覆盖率报告: {'✅ 生成成功' if coverage_success else '❌ 生成失败'}")
    
    if auth_success and api_success and all_success:
        print("\n🎉 所有测试都通过了!")
    else:
        print("\n💥 部分测试失败，请检查错误信息")
    
    print("="*60)

if __name__ == "__main__":
    main() 