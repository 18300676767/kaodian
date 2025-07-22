#!/usr/bin/env python3
"""
错误定位脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    print(f"🔍 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"退出码: {result.returncode}")
        
        if result.stdout:
            print("标准输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"执行异常: {e}")
        return False

def main():
    """主函数"""
    print("�� 开始错误定位")
    print("="*50)
    
    # 1. 检查当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 2. 检查Python环境
    print("\n🔍 检查Python环境...")
    run_command("python --version", "Python版本")
    run_command("which python", "Python路径")
    
    # 3. 检查conda环境
    print("\n�� 检查conda环境...")
    run_command("conda info --envs", "conda环境列表")
    run_command("conda list | grep python", "Python包列表")
    
    # 4. 检查依赖包
    print("\n🔍 检查依赖包...")
    packages = ["fastapi", "sqlalchemy", "pymysql", "passlib", "pytest"]
    for package in packages:
        run_command(f"python -c \"import {package}; print('{package}版本:', {package}.__version__)\"", f"检查{package}")
    
    # 5. 检查数据库连接
    print("\n🔍 检查数据库连接...")
    db_test = """
import sys
sys.path.append('.')
try:
    from database import engine
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ 数据库连接成功")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
"""
    run_command(f"python -c \"{db_test}\"", "数据库连接测试")
    
    # 6. 运行单个测试
    print("\n🔍 运行单个测试...")
    run_command("python -m pytest tests/test_auth.py::TestAuthFunctions::test_password_hashing -v -s", "密码哈希测试")
    
    # 7. 检查测试文件
    print("\n🔍 检查测试文件...")
    run_command("ls -la tests/", "测试文件列表")
    run_command("head -20 tests/test_auth.py", "认证测试文件前20行")

if __name__ == "__main__":
    main() 