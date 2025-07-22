#!/usr/bin/env python3
"""
检查认证模块
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

try:
    from auth import get_password_hash, verify_password, create_access_token
    
    print("✅ 认证模块导入成功")
    
    # 测试密码哈希
    password = "testpass123"
    hashed = get_password_hash(password)
    print(f"密码哈希: {hashed}")
    
    # 测试密码验证
    is_valid = verify_password(password, hashed)
    print(f"密码验证: {is_valid}")
    
    # 测试token创建
    token = create_access_token({"sub": "testuser"})
    print(f"Token: {token}")
    
except Exception as e:
    print(f"❌ 认证模块错误: {e}")
    import traceback
    traceback.print_exc()