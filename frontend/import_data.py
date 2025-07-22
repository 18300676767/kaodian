#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import engine, Base
from exam_points import ExamPoint

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 考点数据
exam_points_data = [
    {
        "province": "四川",
        "subject": "英语",
        "grade": "高一",
        "semester": "上学期",
        "level1_point": "几何",
        "level2_point": "应用",
        "level3_point": "D类",
        "description": "自动生成的考点描述 1",
        "coverage_rate": 97.9,
        "added_by": "user7",
        "added_date": "2022-07-11",
        "is_active": True
    },
    {
        "province": "河南",
        "subject": "历史",
        "grade": "高三",
        "semester": "上学期",
        "level1_point": "综合",
        "level2_point": "进阶",
        "level3_point": "B类",
        "description": "自动生成的考点描述 2",
        "coverage_rate": 72.6,
        "added_by": "user5",
        "added_date": "2023-01-14",
        "is_active": True
    },
    {
        "province": "江苏",
        "subject": "地理",
        "grade": "高三",
        "semester": "上学期",
        "level1_point": "实验",
        "level2_point": "进阶",
        "level3_point": "D类",
        "description": "自动生成的考点描述 3",
        "coverage_rate": 60.5,
        "added_by": "user9",
        "added_date": "2024-02-02",
        "is_active": False
    },
    {
        "province": "上海",
        "subject": "政治",
        "grade": "高三",
        "semester": "上学期",
        "level1_point": "综合",
        "level2_point": "基础",
        "level3_point": "A类",
        "description": "自动生成的考点描述 4",
        "coverage_rate": 85.2,
        "added_by": "user1",
        "added_date": "2023-01-15",
        "is_active": True
    },
    {
        "province": "广东",
        "subject": "数学",
        "grade": "高二",
        "semester": "下学期",
        "level1_point": "函数",
        "level2_point": "进阶",
        "level3_point": "B类",
        "description": "自动生成的考点描述 5",
        "coverage_rate": 92.1,
        "added_by": "user3",
        "added_date": "2022-09-22",
        "is_active": False
    }
]

def import_exam_points():
    """导入考点数据到数据库"""
    db = SessionLocal()
    try:
        # 清空现有数据
        db.query(ExamPoint).delete()
        db.commit()
        print("✅ 已清空现有考点数据")
        
        # 导入新数据
        for i, data in enumerate(exam_points_data, 1):
            exam_point = ExamPoint(**data)
            db.add(exam_point)
            print(f"📝 正在导入第 {i} 条考点数据: {data['province']} - {data['subject']} - {data['level1_point']}")
        
        db.commit()
        print(f"✅ 成功导入 {len(exam_points_data)} 条考点数据到数据库")
        
        # 验证导入结果
        count = db.query(ExamPoint).count()
        print(f"📊 数据库中现有 {count} 条考点记录")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 导入失败: {e}")
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    print("🚀 开始导入考点数据...")
    success = import_exam_points()
    if success:
        print("🎉 考点数据导入完成！")
    else:
        print("💥 考点数据导入失败！")
        sys.exit(1) 