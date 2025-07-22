#!/usr/bin/env python3
import requests
import json

def test_login():
    """测试登录功能"""
    print("🔍 开始测试登录功能...")
    
    # 测试后端健康检查
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"✅ 后端健康检查: {response.status_code}")
    except Exception as e:
        print(f"❌ 后端健康检查失败: {e}")
        return False
    
    # 测试登录API
    login_data = {
        'username': 'admin',
        'password': '111111'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/auth/login',
            data=login_data,
            timeout=5
        )
        
        print(f"📊 登录响应状态: {response.status_code}")
        print(f"📄 响应内容: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                print("✅ 登录成功！获取到JWT token")
                return True
            else:
                print("❌ 登录响应中没有access_token")
                return False
        else:
            print(f"❌ 登录失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False

def test_frontend_access():
    """测试前端访问"""
    print("\n🌐 测试前端访问...")
    
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        print(f"✅ 前端访问成功: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ 前端访问失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始系统登录功能测试")
    print("=" * 50)
    
    backend_ok = test_login()
    frontend_ok = test_frontend_access()
    
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    print(f"   后端登录: {'✅ 通过' if backend_ok else '❌ 失败'}")
    print(f"   前端访问: {'✅ 通过' if frontend_ok else '❌ 失败'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 系统登录功能正常！")
        print("💡 提示: 现在可以在浏览器中访问 http://localhost:3000 进行登录测试")
    else:
        print("\n⚠️  系统存在问题，请检查服务状态") 