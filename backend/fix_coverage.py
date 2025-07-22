#!/usr/bin/env python3
import sqlite3

def fix_coverage_rate():
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        # 查看所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("数据库中的表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # 查找考点相关的表
        for table in tables:
            table_name = table[0]
            if 'exam' in table_name.lower() or 'point' in table_name.lower():
                print(f"\n检查表: {table_name}")
                try:
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    print(f"列信息: {columns}")
                    
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    rows = cursor.fetchall()
                    print(f"前3行数据: {rows}")
                except Exception as e:
                    print(f"查询表 {table_name} 失败: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    fix_coverage_rate()
