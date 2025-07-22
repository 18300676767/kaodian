#!/usr/bin/env python3
import jwt
import requests

def debug_token():
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDEiLCJleHAiOjE3NTE4MDcyMjN9.wg1p8M_-1insRuVzaQOdUFM"
    SECRET_KEY = "your-secret-key-here-change-in-production"
    ALGORITHM = "HS256"
    
    try:
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ Token解码成功:")
        print(f"Payload: {payload}")
        print(f"Username: {payload.get('sub')}")
        print(f"Expires: {payload.get('exp')}")
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get("http://localhost:8000/users/me", headers=headers)
        print(f"\nAPI调用结果:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except jwt.ExpiredSignatureError:
        print("❌ Token已过期")
    except jwt.InvalidTokenError as e:
        print(f"❌ Token无效: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    debug_token()
