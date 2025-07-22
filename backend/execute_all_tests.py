#!/usr/bin/env python3
"""
统一测试执行脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, cwd=None):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
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
    print("🧪 高考考点分析系统 - 完整测试套件")
    print("="*60)
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    print(f"项目根目录: {project_root}")
    print(f"后端目录: {backend_dir}")
    print(f"前端目录: {frontend_dir}")
    
    results = []
    
    # 1. 后端测试
    print("\n🔧 后端测试")
    print("-" * 30)
    
    # 认证测试
    auth_success = run_command(
        "python -m pytest tests/test_auth.py -v",
        "认证测试",
        cwd=backend_dir
    )
    results.append(("后端认证测试", auth_success))
    
    # API测试
    api_success = run_command(
        "python -m pytest tests/test_integration.py -v",
        "API集成测试",
        cwd=backend_dir
    )
    results.append(("后端API测试", api_success))
    
    # 所有后端测试
    all_backend_success = run_command(
        "python -m pytest tests/ -v",
        "所有后端测试",
        cwd=backend_dir
    )
    results.append(("所有后端测试", all_backend_success))
    
    # 2. 前端测试
    print("\n🎨 前端测试")
    print("-" * 30)
    
    # 前端基础测试
    frontend_success = run_command(
        "pnpm test --watchAll=false",
        "前端基础测试",
        cwd=frontend_dir
    )
    results.append(("前端基础测试", frontend_success))
    
    # 前端覆盖率测试
    frontend_coverage_success = run_command(
        "pnpm test:coverage",
        "前端覆盖率测试",
        cwd=frontend_dir
    )
    results.append(("前端覆盖率测试", frontend_coverage_success))
    
    # 3. 生成后端覆盖率报告
    print("\n📊 生成覆盖率报告")
    print("-" * 30)
    
    coverage_success = run_command(
        "python -m pytest tests/ --cov=. --cov-report=term-missing --cov-report=html",
        "生成后端覆盖率报告",
        cwd=backend_dir
    )
    results.append(("后端覆盖率报告", coverage_success))
    
    # 总结
    print("\n" + "="*60)
    print("📋 完整测试结果总结:")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了!")
        print("✅ 系统测试覆盖完整，可以安全部署")
    else:
        print("💥 部分测试失败，请检查错误信息")
        print("⚠️  建议修复失败的测试后再部署")
    
    print("="*60)

if __name__ == "__main__":
    main() 