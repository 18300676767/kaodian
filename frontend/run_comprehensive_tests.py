#!/usr/bin/env python3
"""
综合测试脚本
用于运行前后端测试并生成覆盖率报告
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class TestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent  # 回到项目根目录
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.reports_dir = self.project_root / "test_reports"
        
        # 创建报告目录
        self.reports_dir.mkdir(exist_ok=True)
        
        print(f"项目根目录: {self.project_root}")
        print(f"后端目录: {self.backend_dir}")
        print(f"前端目录: {self.frontend_dir}")
        
    def print_header(self, title):
        """打印标题"""
        print("\n" + "="*60)
        print(f" {title}")
        print("="*60)
        
    def run_command(self, command, cwd=None, capture_output=False):
        """运行命令"""
        if cwd is None:
            cwd = self.project_root
            
        print(f"执行命令: {command}")
        print(f"工作目录: {cwd}")
        
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=cwd, 
                    capture_output=True, 
                    text=True,
                    timeout=300
                )
                return result
            else:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=cwd, 
                    timeout=300
                )
                return result
        except subprocess.TimeoutExpired:
            print(f"命令超时: {command}")
            return None
        except Exception as e:
            print(f"命令执行失败: {e}")
            return None
    
    def check_backend_dependencies(self):
        """检查后端依赖"""
        self.print_header("检查后端依赖")
        
        # 检查Python环境
        result = self.run_command("python --version", cwd=self.backend_dir)
        if result and result.returncode == 0:
            print("✅ Python环境正常")
        else:
            print("❌ Python环境异常")
            return False
            
        # 检查pytest
        result = self.run_command("python -m pytest --version", cwd=self.backend_dir)
        if result and result.returncode == 0:
            print("✅ pytest已安装")
        else:
            print("❌ pytest未安装，正在安装...")
            self.run_command("pip install pytest pytest-asyncio httpx")
            
        return True
    
    def check_frontend_dependencies(self):
        """检查前端依赖"""
        self.print_header("检查前端依赖")
        
        # 检查Node.js
        result = self.run_command("node --version", cwd=self.frontend_dir)
        if result and result.returncode == 0:
            print("✅ Node.js环境正常")
        else:
            print("❌ Node.js环境异常")
            return False
            
        # 检查pnpm
        result = self.run_command("pnpm --version", cwd=self.frontend_dir)
        if result and result.returncode == 0:
            print("✅ pnpm已安装")
        else:
            print("❌ pnpm未安装")
            return False
            
        return True
    
    def run_backend_tests(self):
        """运行后端测试"""
        self.print_header("运行后端测试")
        
        # 运行测试（不使用覆盖率参数）
        command = "python -m pytest tests/ -v --tb=short"
        result = self.run_command(command, cwd=self.backend_dir, capture_output=True)
        
        if result and result.returncode == 0:
            print("✅ 后端测试通过")
            print(result.stdout)
        else:
            print("❌ 后端测试失败")
            if result:
                print(result.stderr)
            return False
            
        return True
    
    def run_frontend_tests(self):
        """运行前端测试"""
        self.print_header("运行前端测试")
        
        # 运行测试并生成覆盖率报告
        command = "pnpm test --coverage --watchAll=false --passWithNoTests"
        result = self.run_command(command, cwd=self.frontend_dir, capture_output=True)
        
        if result and result.returncode == 0:
            print("✅ 前端测试通过")
            print(result.stdout)
        else:
            print("❌ 前端测试失败")
            if result:
                print(result.stderr)
            return False
            
        return True
    
    def generate_test_summary(self):
        """生成测试总结"""
        self.print_header("生成测试总结")
        
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "backend_tests": {
                "status": "unknown",
                "coverage": "unknown"
            },
            "frontend_tests": {
                "status": "unknown", 
                "coverage": "unknown"
            },
            "recommendations": []
        }
        
        # 检查后端覆盖率报告
        backend_coverage_file = self.backend_dir / "htmlcov" / "index.html"
        if backend_coverage_file.exists():
            summary["backend_tests"]["status"] = "completed"
            summary["backend_tests"]["coverage"] = "available"
        else:
            summary["backend_tests"]["status"] = "failed"
            summary["recommendations"].append("后端测试失败，需要修复测试问题")
            
        # 检查前端覆盖率报告
        frontend_coverage_file = self.frontend_dir / "coverage" / "lcov-report" / "index.html"
        if frontend_coverage_file.exists():
            summary["frontend_tests"]["status"] = "completed"
            summary["frontend_tests"]["coverage"] = "available"
        else:
            summary["frontend_tests"]["status"] = "failed"
            summary["recommendations"].append("前端测试失败，需要修复Jest配置")
            
        # 保存总结报告
        summary_file = self.reports_dir / "test_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"测试总结已保存到: {summary_file}")
        
        # 打印总结
        print("\n测试总结:")
        print(f"后端测试状态: {summary['backend_tests']['status']}")
        print(f"前端测试状态: {summary['frontend_tests']['status']}")
        
        if summary["recommendations"]:
            print("\n建议:")
            for rec in summary["recommendations"]:
                print(f"- {rec}")
    
    def run_all_tests(self):
        """运行所有测试"""
        self.print_header("开始综合测试")
        
        # 检查依赖
        if not self.check_backend_dependencies():
            print("❌ 后端依赖检查失败")
            return False
            
        if not self.check_frontend_dependencies():
            print("❌ 前端依赖检查失败")
            return False
        
        # 运行后端测试
        backend_success = self.run_backend_tests()
        
        # 运行前端测试
        frontend_success = self.run_frontend_tests()
        
        # 生成总结
        self.generate_test_summary()
        
        if backend_success and frontend_success:
            print("\n🎉 所有测试完成!")
            return True
        else:
            print("\n⚠️ 部分测试失败，请查看详细报告")
            return False

def main():
    """主函数"""
    runner = TestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 