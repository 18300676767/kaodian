#!/usr/bin/env python3
"""
全局测试套件
包含后端和前端完整测试
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

class GlobalTestSuite:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root
        self.results = []
        self.start_time = time.time()
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def run_command(self, command, description, cwd=None, timeout=300):
        """运行命令并返回结果"""
        self.log(f"🧪 执行: {description}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout
            )
            
            if result.returncode == 0:
                self.log(f"✅ {description} 成功")
                if result.stdout:
                    print(result.stdout)
                return True, result.stdout
            else:
                self.log(f"❌ {description} 失败 (退出码: {result.returncode})")
                if result.stdout:
                    print("标准输出:")
                    print(result.stdout)
                if result.stderr:
                    print("错误输出:")
                    print(result.stderr)
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self.log(f"⏰ {description} 超时")
            return False, "执行超时"
        except Exception as e:
            self.log(f"💥 {description} 异常: {e}")
            return False, str(e)
    
    def check_environment(self):
        """检查环境"""
        self.log("🔍 检查环境...")
        
        # 检查目录结构
        if self.backend_dir.exists():
            self.log(f"✅ backend目录存在: {self.backend_dir}")
        else:
            self.log(f"❌ backend目录不存在: {self.backend_dir}")
            return False
            
        if self.frontend_dir.exists():
            self.log(f"✅ frontend目录存在: {self.frontend_dir}")
        else:
            self.log(f"❌ frontend目录不存在: {self.frontend_dir}")
            return False
        
        # 检查Python环境
        python_version = subprocess.run("python --version", shell=True, capture_output=True, text=True)
        self.log(f"Python版本: {python_version.stdout.strip()}")
        
        # 检查conda环境
        conda_env = subprocess.run("conda info --envs | grep '*'", shell=True, capture_output=True, text=True)
        self.log(f"当前conda环境: {conda_env.stdout.strip()}")
        
        return True
    
    def check_dependencies(self):
        """检查依赖"""
        self.log("🔍 检查依赖...")
        
        dependencies = [
            ("fastapi", "FastAPI"),
            ("sqlalchemy", "SQLAlchemy"),
            ("pymysql", "PyMySQL"),
            ("passlib", "Passlib"),
            ("pytest", "Pytest"),
            ("react", "React"),
            ("typescript", "TypeScript")
        ]
        
        for package, name in dependencies:
            try:
                if package in ["react", "typescript"]:
                    # 前端依赖
                    result = subprocess.run(f"pnpm list {package}", shell=True, capture_output=True, text=True, cwd=self.frontend_dir)
                else:
                    # 后端依赖
                    result = subprocess.run(f"python -c \"import {package}; print('{name}版本:', {package}.__version__)\"", 
                                          shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log(f"✅ {name}: 已安装")
                else:
                    self.log(f"❌ {name}: 未安装")
            except Exception as e:
                self.log(f"❌ {name}: {e}")
    
    def run_backend_tests(self):
        """运行后端测试"""
        self.log("�� 开始后端测试")
        
        backend_tests = [
            ("认证测试", "python -m pytest tests/test_auth.py -v", self.backend_dir),
            ("API集成测试", "python -m pytest tests/test_integration.py -v", self.backend_dir),
            ("模型测试", "python -m pytest tests/test_models.py -v", self.backend_dir),
            ("所有后端测试", "python -m pytest tests/ -v", self.backend_dir),
        ]
        
        for test_name, command, cwd in backend_tests:
            success, output = self.run_command(command, test_name, cwd)
            self.results.append({
                "test_name": test_name,
                "success": success,
                "type": "backend"
            })
    
    def run_frontend_tests(self):
        """运行前端测试"""
        self.log("�� 开始前端测试")
        
        frontend_tests = [
            ("前端基础测试", "pnpm test --watchAll=false", self.frontend_dir),
            ("前端覆盖率测试", "pnpm test:coverage", self.frontend_dir),
        ]
        
        for test_name, command, cwd in frontend_tests:
            success, output = self.run_command(command, test_name, cwd)
            self.results.append({
                "test_name": test_name,
                "success": success,
                "type": "frontend"
            })
    
    def generate_coverage_report(self):
        """生成覆盖率报告"""
        self.log("📊 生成覆盖率报告")
        
        coverage_command = "python -m pytest tests/ --cov=. --cov-report=term-missing --cov-report=html"
        success, output = self.run_command(coverage_command, "覆盖率报告", self.backend_dir)
        
        self.results.append({
            "test_name": "覆盖率报告",
            "success": success,
            "type": "coverage"
        })
    
    def run_integration_tests(self):
        """运行集成测试"""
        self.log("�� 开始集成测试")
        
        # 启动后端服务
        self.log("启动后端服务...")
        backend_process = subprocess.Popen(
            "python main.py",
            shell=True,
            cwd=self.backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待服务启动
        time.sleep(5)
        
        # 测试API连接
        api_test = """
import requests
try:
    response = requests.get('http://localhost:8000/health')
    print(f"API连接测试: {response.status_code}")
    if response.status_code == 200:
        print("✅ API连接成功")
    else:
        print("❌ API连接失败")
except Exception as e:
    print(f"❌ API连接异常: {e}")
"""
        
        success, output = self.run_command(f"python -c \"{api_test}\"", "API集成测试")
        
        # 停止后端服务
        backend_process.terminate()
        
        self.results.append({
            "test_name": "集成测试",
            "success": success,
            "type": "integration"
        })
    
    def generate_test_report(self):
        """生成测试报告"""
        self.log("�� 生成测试报告")
        
        # 统计结果
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        # 按类型分组
        backend_results = [r for r in self.results if r["type"] == "backend"]
        frontend_results = [r for r in self.results if r["type"] == "frontend"]
        coverage_results = [r for r in self.results if r["type"] == "coverage"]
        integration_results = [r for r in self.results if r["type"] == "integration"]
        
        backend_passed = sum(1 for r in backend_results if r["success"])
        frontend_passed = sum(1 for r in frontend_results if r["success"])
        coverage_passed = sum(1 for r in coverage_results if r["success"])
        integration_passed = sum(1 for r in integration_results if r["success"])
        
        # 生成报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "duration": time.time() - self.start_time,
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "backend": {
                "total": len(backend_results),
                "passed": backend_passed,
                "failed": len(backend_results) - backend_passed
            },
            "frontend": {
                "total": len(frontend_results),
                "passed": frontend_passed,
                "failed": len(frontend_results) - frontend_passed
            },
            "coverage": {
                "total": len(coverage_results),
                "passed": coverage_passed,
                "failed": len(coverage_results) - coverage_passed
            },
            "integration": {
                "total": len(integration_results),
                "passed": integration_passed,
                "failed": len(integration_results) - integration_passed
            },
            "details": self.results
        }
        
        # 保存报告
        report_file = self.project_root / "global_test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 测试报告已保存到: {report_file}")
        return report
    
    def print_summary(self, report):
        """打印测试总结"""
        print("\n" + "="*80)
        print("�� 全局测试结果总结")
        print("="*80)
        
        summary = report["summary"]
        print(f"总测试数: {summary['total_tests']}")
        print(f"通过测试: {summary['passed_tests']}")
        print(f"失败测试: {summary['failed_tests']}")
        print(f"成功率: {summary['success_rate']:.1f}%")
        print(f"执行时间: {summary['duration']:.1f}秒")
        
        if report["backend"]["total"] > 0:
            print(f"\n🔧 后端测试: {report['backend']['passed']}/{report['backend']['total']} 通过")
        
        if report["frontend"]["total"] > 0:
            print(f"🎨 前端测试: {report['frontend']['passed']}/{report['frontend']['total']} 通过")
        
        if report["coverage"]["total"] > 0:
            print(f"�� 覆盖率报告: {report['coverage']['passed']}/{report['coverage']['total']} 通过")
        
        if report["integration"]["total"] > 0:
            print(f"🔗 集成测试: {report['integration']['passed']}/{report['integration']['total']} 通过")
        
        print("\n详细结果:")
        for result in self.results:
            status = "✅ 通过" if result["success"] else "❌ 失败"
            print(f"  {result['test_name']}: {status}")
        
        if summary['success_rate'] == 100:
            print("\n🎉 所有测试都通过了!")
            print("✅ 系统测试覆盖完整，可以安全部署")
        else:
            print(f"\n�� {summary['failed_tests']} 个测试失败")
            print("⚠️  建议修复失败的测试后再部署")
        
        print("="*80)
    
    def run(self):
        """运行完整的全局测试套件"""
        self.log("🚀 开始全局测试套件")
        
        try:
            # 1. 检查环境
            if not self.check_environment():
                self.log("❌ 环境检查失败")
                return False
            
            # 2. 检查依赖
            self.check_dependencies()
            
            # 3. 运行后端测试
            self.run_backend_tests()
            
            # 4. 运行前端测试
            self.run_frontend_tests()
            
            # 5. 生成覆盖率报告
            self.generate_coverage_report()
            
            # 6. 运行集成测试
            self.run_integration_tests()
            
            # 7. 生成测试报告
            report = self.generate_test_report()
            
            # 8. 打印总结
            self.print_summary(report)
            
            return report["summary"]["success_rate"] == 100
            
        except Exception as e:
            self.log(f"💥 全局测试执行异常: {e}")
            return False

def main():
    """主函数"""
    test_suite = GlobalTestSuite()
    success = test_suite.run()
    
    if success:
        print("\n🎉 全局测试套件执行成功!")
        sys.exit(0)
    else:
        print("\n💥 全局测试套件执行失败!")
        sys.exit(1)

if __name__ == "__main__":
    main() 