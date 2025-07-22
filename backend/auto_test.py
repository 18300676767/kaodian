#!/usr/bin/env python3
"""
自动化测试执行器
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

class AutoTestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.results = []
        self.start_time = time.time()
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def run_test(self, command, test_name, cwd=None):
        """运行单个测试"""
        self.log(f"🧪 执行 {test_name}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=300
            )
            
            if result.returncode == 0:
                self.log(f"✅ {test_name} 通过")
                return True, result.stdout
            else:
                self.log(f"❌ {test_name} 失败")
                if result.stderr:
                    print(f"错误: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self.log(f"⏰ {test_name} 超时")
            return False, "执行超时"
        except Exception as e:
            self.log(f"💥 {test_name} 异常: {e}")
            return False, str(e)
    
    def run_backend_tests(self):
        """运行后端测试"""
        self.log("🚀 开始后端测试")
        
        backend_tests = [
            ("认证测试", "python -m pytest tests/test_auth.py -v", self.backend_dir),
            ("API集成测试", "python -m pytest tests/test_integration.py -v", self.backend_dir),
            ("模型测试", "python -m pytest tests/test_models.py -v", self.backend_dir),
            ("所有后端测试", "python -m pytest tests/ -v", self.backend_dir),
        ]
        
        for test_name, command, cwd in backend_tests:
            success, output = self.run_test(command, test_name, cwd)
            self.results.append({
                "test_name": test_name,
                "success": success,
                "type": "backend"
            })
    
    def run_frontend_tests(self):
        """运行前端测试"""
        self.log("🚀 开始前端测试")
        
        frontend_tests = [
            ("前端基础测试", "pnpm test --watchAll=false", self.frontend_dir),
        ]
        
        for test_name, command, cwd in frontend_tests:
            success, output = self.run_test(command, test_name, cwd)
            self.results.append({
                "test_name": test_name,
                "success": success,
                "type": "frontend"
            })
    
    def generate_coverage(self):
        """生成覆盖率报告"""
        self.log("📊 生成覆盖率报告")
        
        command = "python -m pytest tests/ --cov=. --cov-report=term-missing --cov-report=html"
        success, output = self.run_test(command, "覆盖率报告", self.backend_dir)
        
        self.results.append({
            "test_name": "覆盖率报告",
            "success": success,
            "type": "coverage"
        })
    
    def print_summary(self):
        """打印测试总结"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        
        print("\n" + "="*60)
        print("📊 自动化测试结果总结")
        print("="*60)
        print(f"总测试数: {total}")
        print(f"通过测试: {passed}")
        print(f"失败测试: {failed}")
        print(f"成功率: {(passed/total*100):.1f}%" if total > 0 else "成功率: 0%")
        
        print("\n详细结果:")
        for result in self.results:
            status = "✅ 通过" if result["success"] else "❌ 失败"
            print(f"  {result['test_name']}: {status}")
        
        if passed == total and total > 0:
            print("\n🎉 所有测试都通过了!")
        else:
            print(f"\n💥 {failed} 个测试失败")
        
        print("="*60)
        
        return passed == total
    
    def run(self):
        """运行完整的自动化测试"""
        self.log("🚀 开始自动化测试套件")
        
        try:
            # 1. 后端测试
            self.run_backend_tests()
            
            # 2. 前端测试
            self.run_frontend_tests()
            
            # 3. 覆盖率报告
            self.generate_coverage()
            
            # 4. 打印总结
            success = self.print_summary()
            
            return success
            
        except Exception as e:
            self.log(f"💥 自动化测试执行异常: {e}")
            return False

def main():
    """主函数"""
    runner = AutoTestRunner()
    success = runner.run()
    
    if success:
        print("\n🎉 自动化测试执行成功!")
        sys.exit(0)
    else:
        print("\n💥 自动化测试执行失败!")
        sys.exit(1)

if __name__ == "__main__":
    main() 