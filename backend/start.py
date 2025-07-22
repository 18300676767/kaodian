#!/usr/bin/env python3
"""
高考考点分析系统 - 后端启动脚本
"""

import uvicorn
import os
import sys

def main():
    print("🚀 启动高考考点分析系统后端...")
    print("📊 数据库配置: MySQL - kaodian")
    print("🔐 认证系统: JWT Token")
    print("🌐 API地址: http://localhost:8000")
    print("📚 文档地址: http://localhost:8000/docs")
    print("-" * 50)
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 