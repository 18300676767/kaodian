#!/usr/bin/env python3
"""
测试错误诊断脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def run_diagnostic_test(test_name, command):
    """运行诊断测试"""
    print(f"\n{'='*60}")
    print(f"🔍 诊断测试: {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"退出码: {result.returncode}")
        
        if result.stdout:
            print("标准输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        return result.returncode == 0, result.stdout, result.stderr
        
    except Exception as e:
        print(f"执行异常: {e}")
        return False, "", str(e)

def check_environment():
    """检查环境"""
    print("�� 检查环境...")
    
    # 检查Python版本
    python_version = subprocess.run("python --version", shell=True, capture_output=True, text=True)
    print(f"Python版本: {python_version.stdout.strip()}")
    
    # 检查pytest
    pytest_version = subprocess.run("python -m pytest --version", shell=True, capture_output=True, text=True)
    print(f"Pytest版本: {pytest_version.stdout.strip()}")
    
    # 检查依赖
    try:
        import fastapi
        print(f"FastAPI版本: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI未安装")
    
    try:
        import sqlalchemy
        print(f"SQLAlchemy版本: {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy未安装")

def check_database_connection():
    """检查数据库连接"""
    print("\n�� 检查数据库连接...")
    
    test_script = """
import sys
sys.path.append('.')
from database import engine
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ 数据库连接成功")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
"""
    
    success, stdout, stderr = run_diagnostic_test("数据库连接测试", f"python -c \"{test_script}\"")
    return success

def check_imports():
    """检查模块导入"""
    print("\n🔍 检查模块导入...")
    
    modules = [
        "fastapi",
        "sqlalchemy",
        "pymysql",
        "passlib",
        "python-jose",
        "pytest",
        "models",
        "auth",
        "database",
        "schemas"
    ]
    
    for module in modules:
        try:
            if module in ["models", "auth", "database", "schemas"]:
                # 本地模块
                exec(f"import {module}")
            else:
                # 外部模块
                exec(f"import {module}")
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")

def run_simple_test():
    """运行简单测试"""
    print("\n🔍 运行简单测试...")
    
    simple_test = """
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    print("✅ 健康检查通过")

if __name__ == "__main__":
    test_health_check()
"""
    
    success, stdout, stderr = run_diagnostic_test("简单健康检查测试", f"python -c \"{simple_test}\"")
    return success

def run_auth_test():
    """运行认证测试"""
    print("\n🔍 运行认证测试...")
    
    auth_test = """
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import models
from database import Base, get_db
from main import app

# 创建内存数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_register():
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = client.post("/auth/register", json=test_user)
    print(f"注册响应状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ 用户注册成功")
    else:
        print(f"❌ 用户注册失败: {response.text}")
    return response.status_code == 200

if __name__ == "__main__":
    test_register()
"""
    
    success, stdout, stderr = run_diagnostic_test("认证测试", f"python -c \"{auth_test}\"")
    return success

def main():
    """主函数"""
    print("🔍 开始测试错误诊断")
    print("="*60)
    
    # 1. 检查环境
    check_environment()
    
    # 2. 检查模块导入
    check_imports()
    
    # 3. 检查数据库连接
    db_success = check_database_connection()
    
    # 4. 运行简单测试
    simple_success = run_simple_test()
    
    # 5. 运行认证测试
    auth_success = run_auth_test()
    
    # 总结
    print("\n" + "="*60)
    print("📊 诊断结果总结:")
    print(f"数据库连接: {'✅ 成功' if db_success else '❌ 失败'}")
    print(f"简单测试: {'✅ 成功' if simple_success else '❌ 失败'}")
    print(f"认证测试: {'✅ 成功' if auth_success else '❌ 失败'}")
    
    if db_success and simple_success and auth_success:
        print("\n🎉 所有诊断测试通过!")
    else:
        print("\n�� 部分诊断测试失败，请检查上述错误信息")

if __name__ == "__main__":
    main() 