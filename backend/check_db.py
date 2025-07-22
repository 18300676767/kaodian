#!/usr/bin/env python3
"""
检查数据库配置
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

try:
    from database import engine, Base
    from models import User
    
    print("✅ 数据库模块导入成功")
    
    # 尝试连接数据库
    with engine.connect() as conn:
        print("✅ 数据库连接成功")
        
        # 检查表是否存在
        result = conn.execute("SHOW TABLES")
        tables = [row[0] for row in result]
        print(f"数据库中的表: {tables}")
        
except Exception as e:
    print(f"❌ 数据库配置错误: {e}")
    import traceback
    traceback.print_exc()