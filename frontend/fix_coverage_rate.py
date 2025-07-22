#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from sqlalchemy.orm import sessionmaker
from database import engine, Base
from models import ExamPoint

def check_and_fix_coverage_rate():
    """检查并修正覆盖率字段"""
    
    # 方法1：使用SQLite直接查询
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
        print(f"SQLite查询失败: {e}")
    
    # 方法2：使用SQLAlchemy查询
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 查询所有考点数据
        exam_points = db.query(ExamPoint).all()
        print(f"\n通过SQLAlchemy查询到 {len(exam_points)} 条考点数据")
        
        if exam_points:
            print("\n前5条数据的覆盖率:")
            for i, point in enumerate(exam_points[:5]):
                print(f"  {i+1}. {point.province} - {point.subject}: {point.coverage_rate}")
            
            # 检查需要修正的数据
            need_fix = []
            for point in exam_points:
                if point.coverage_rate > 1:
                    need_fix.append(point)
            
            print(f"\n需要修正的数据: {len(need_fix)} 条")
            for point in need_fix[:5]:
                print(f"  {point.province} - {point.subject}: {point.coverage_rate} -> {point.coverage_rate * 100:.1f}%")
            
            # 修正数据
            if need_fix:
                print(f"\n开始修正 {len(need_fix)} 条数据...")
                for point in need_fix:
                    point.coverage_rate = point.coverage_rate * 100
                
                db.commit()
                print("✅ 覆盖率修正完成！")
                
                # 验证修正结果
                print("\n修正后的前5条数据:")
                for i, point in enumerate(exam_points[:5]):
                    print(f"  {i+1}. {point.province} - {point.subject}: {point.coverage_rate}%")
        
        db.close()
        
    except Exception as e:
        print(f"SQLAlchemy查询失败: {e}")

if __name__ == "__main__":
    print("🔍 检查并修正考点数据中的覆盖率字段...")
    check_and_fix_coverage_rate() 