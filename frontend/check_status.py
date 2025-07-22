#!/usr/bin/env python3
"""
系统状态检查脚本
"""

import requests
import subprocess
import time

def check_backend():
    """检查后端状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正常运行")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端服务连接失败: {e}")
        return False

def check_frontend():
    """检查前端状态"""
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常运行")
            return True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False

def check_database():
    """检查数据库状态"""
    try:
        response = requests.get("http://localhost:8000/provinces", timeout=5)
        if response.status_code == 200:
            provinces = response.json()
            print(f"✅ 数据库连接正常，省市数据: {len(provinces)} 个省份")
            return True
        else:
            print(f"❌ 数据库查询异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 检查系统状态...")
    print("=" * 50)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    database_ok = check_database()
    
    print("=" * 50)
    if backend_ok and frontend_ok and database_ok:
        print("🎉 系统运行正常！")
        print("📝 访问地址:")
        print("   前端: http://localhost:3001")
        print("   后端API: http://localhost:8000")
        print("   API文档: http://localhost:8000/docs")
    else:
        print("⚠️  系统存在问题，请检查服务状态")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 