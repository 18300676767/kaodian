#!/usr/bin/env python3
"""
简单的测试执行器
"""

import subprocess
import sys
import os

def run_test(test_name, command):
    """运行单个测试"""
    print(f"\n{'='*50}")
    print(f"🧪 运行 {test_name}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 测试通过!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ 测试失败!")
            if result.stdout:
                print("标准输出:")
                print(result.stdout)
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始执行修复后的测试...")
    
    tests = [
        ("认证测试", "python -m pytest tests/test_auth.py -v"),
        ("API集成测试", "python -m pytest tests/test_integration.py -v"),
        ("模型测试", "python -m pytest tests/test_models.py -v"),
        ("所有测试", "python -m pytest tests/ -v"),
    ]
    
    results = []
    for test_name, command in tests:
        success = run_test(test_name, command)
        results.append((test_name, success))
    
    # 总结
    print("\n" + "="*50)
    print("📊 测试结果总结:")
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了!")
    else:
        print("💥 部分测试失败，请检查错误信息")

if __name__ == "__main__":
    main()