#!/usr/bin/env python3
"""
快速诊断脚本
"""

import subprocess
import sys
import os

def quick_check():
    """快速检查"""
    print(" 快速诊断开始")
    print("="*40)
    
    checks = [
        ("Python版本", "python --version"),
        ("当前目录", "pwd"),
        ("conda环境", "conda info --envs | grep '*'"),
        ("FastAPI", "python -c \"import fastapi; print('FastAPI:', fastapi.__version__)\""),
        ("SQLAlchemy", "python -c \"import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)\""),
        ("PyMySQL", "python -c \"import pymysql; print('PyMySQL已安装')\""),
        ("Pytest", "python -c \"import pytest; print('Pytest:', pytest.__version__)\""),
    ]
    
    for name, command in checks:
        print(f"\n🔍 {name}:")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
            else:
                print(f"❌ 失败: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ 异常: {e}")

if __name__ == "__main__":
    quick_check()