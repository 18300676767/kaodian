#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import engine, Base
from models import ExamPoint

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def import_from_json():
    """从JSON文件导入考点数据"""
    try:
        # 读取JSON文件
        with open('exam_points_sample.json', 'r', encoding='utf-8') as f:
            exam_points_data = json.load(f)
        
        print(f"📄 从JSON文件读取到 {len(exam_points_data)} 条考点数据")
        
        db = SessionLocal()
        
        # 清空现有数据
        db.query(ExamPoint).delete()
        db.commit()
        print("✅ 已清空现有考点数据")
        
        # 导入新数据
        for i, data in enumerate(exam_points_data, 1):
            exam_point = ExamPoint(**data)
            db.add(exam_point)
            if i % 20 == 0 or i == len(exam_points_data):
                print(f"📝 正在导入第 {i} 条考点数据: {data['province']} - {data['subject']} - {data['level1_point']}")
        
        db.commit()
        print(f"✅ 成功导入 {len(exam_points_data)} 条考点数据到数据库")
        
        # 验证导入结果
        count = db.query(ExamPoint).count()
        print(f"📊 数据库中现有 {count} 条考点记录")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始从JSON文件导入考点数据...")
    success = import_from_json()
    if success:
        print("🎉 考点数据导入完成！")
    else:
        print("💥 考点数据导入失败！")
        sys.exit(1)
