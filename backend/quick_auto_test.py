#!/usr/bin/env python3
"""
快速自动化测试
"""

import subprocess
import sys

def run_test(test_name, command):
    """运行测试"""
    print(f"\n{'='*50}")
    print(f"🧪 {test_name}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 通过")
            return True
        else:
            print("❌ 失败")
            if result.stderr:
                print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"💥 异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始快速自动化测试")
    
    tests = [
        ("后端认证测试", "cd backend && python -m pytest tests/test_auth.py -v"),
        ("后端API测试", "cd backend && python -m pytest tests/test_integration.py -v"),
        ("所有后端测试", "cd backend && python -m pytest tests/ -v"),
        ("前端测试", "cd frontend && pnpm test --watchAll=false"),
    ]
    
    results = []
    for test_name, command in tests:
        success = run_test(test_name, command)
        results.append((test_name, success))
    
    # 总结
    print("\n" + "="*50)
    print("📊 测试结果:")
    fo 