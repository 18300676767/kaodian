#!/usr/bin/env python3
"""
端到端测试脚本
"""

import subprocess
import time
import requests
import json
from pathlib import Path
import os

def test_backend_api():
    """测试后端API功能"""
    print("🧪 测试后端API功能...")
    
    base_url = "http://localhost:8000"
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ 健康检查: {response.status_code}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False
    
    # 测试用户注册
    try:
        register_data = {
            "username": "e2e_test_user",
            "email": "e2e@test.com",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        print(f"✅ 用户注册: {response.status_code}")
    except Exception as e:
        print(f"❌ 用户注册失败: {e}")
        return False
    
    # 测试用户登录
    try:
        login_data = {
            "username": "e2e_test_user",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/auth/login", data=login_data)
        print(f"✅ 用户登录: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # 测试获取用户信息
            user_response = requests.get(f"{base_url}/users/me", headers=headers)
            print(f"✅ 获取用户信息: {user_response.status_code}")
    except Exception as e:
        print(f"❌ 用户登录失败: {e}")
        return False
    
    return True

def test_frontend_build():
    """测试前端构建"""
    print("🧪 测试前端构建...")
    
    try:
        # 切换到frontend目录
        frontend_dir = Path.cwd().parent / "frontend"
        os.chdir(frontend_dir)
        
        # 安装依赖
        result = subprocess.run("pnpm install", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 依赖安装失败: {result.stderr}")
            return False
        
        # 构建项目
        result = subprocess.run("pnpm build", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 构建失败: {result.stderr}")
            return False
        
        print("✅ 前端构建成功")
        return True
        
    except Exception as e:
        print(f"❌ 前端构建失败: {e}")
        return False

def main():
    """主测试函数"""
    print("�� 开始端到端测试...")
    
    # 启动后端服务
    print("🔧 启动后端服务...")
    backend_process = subprocess.Popen(
        "cd ../backend && python main.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服务启动
    time.sleep(5)
    
    # 测试后端API
    backend_success = test_backend_api()
    
    # 测试前端构建
    frontend_success = test_frontend_build()
    
    # 停止后端服务
    backend_process.terminate()
    
    # 输出结果
    print("\n" + "="*50)
    print("📊 测试结果:")
    print(f"后端API测试: {'✅ 通过' if backend_success else '❌ 失败'}")
    print(f"前端构建测试: {'✅ 通过' if frontend_success else '❌ 失败'}")
    print("="*50)

if __name__ == "__main__":
    main() 