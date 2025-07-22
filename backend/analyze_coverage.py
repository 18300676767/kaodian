#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考点覆盖率分析脚本
分析考点内容，生成科学合理的覆盖率建议
"""

import pymysql
import re
from collections import defaultdict
import json

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': '111111',
    'database': 'kaodian',
    'charset': 'utf8mb4',
    'port': 3306
}

def connect_db():
    """连接数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def get_exam_points_data():
    """获取考点数据"""
    connection = connect_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, province, subject, grade, semester, 
                       level1_point, level2_point, level3_point, 
                       description, coverage_rate
                FROM exam_points
                ORDER BY id
            """)
            return cursor.fetchall()
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []
    finally:
        connection.close()

def analyze_content_complexity(description):
    """分析内容复杂度"""
    if not description:
        return 1
    
    # 计算数学公式数量
    math_formulas = len(re.findall(r'\\[a-zA-Z]+|\\[{}[\]]|\\[()]', description))
    
    # 计算特殊符号数量
    special_symbols = len(re.findall(r'[∫∑∏√∞≠≤≥±×÷]', description))
    
    # 计算关键词数量
    keywords = len(re.findall(r'(定理|公式|定义|性质|证明|计算|推导|应用)', description))
    
    # 计算句子数量
    sentences = len(re.split(r'[。！？]', description))
    
    # 复杂度评分 (1-10)
    complexity = min(10, 1 + math_formulas * 0.5 + special_symbols * 0.3 + keywords * 0.2 + sentences * 0.1)
    
    return round(complexity, 1)

def analyze_subject_importance(subject):
    """分析科目重要性"""
    # 高考科目重要性权重
    subject_weights = {
        '数学': 1.0,
        '语文': 0.9,
        '英语': 0.9,
        '物理': 0.8,
        '化学': 0.8,
        '生物': 0.7,
        '历史': 0.6,
        '地理': 0.6,
        '政治': 0.6
    }
    return subject_weights.get(subject, 0.5)

def analyze_level_importance(level1, level2, level3):
    """分析考点层级重要性"""
    # 一级考点权重最高
    if level1 and level1.strip():
        return 1.0
    # 二级考点权重中等
    elif level2 and level2.strip():
        return 0.8
    # 三级考点权重较低
    elif level3 and level3.strip():
        return 0.6
    else:
        return 0.4

def calculate_scientific_coverage_rate(point_data):
    """计算科学的覆盖率"""
    # 基础覆盖率 (20-40%)
    base_rate = 30
    
    # 内容复杂度调整 (0-20%)
    complexity = analyze_content_complexity(point_data['description'])
    complexity_adjustment = (complexity - 1) * 2
    
    # 科目重要性调整 (0-15%)
    subject_weight = analyze_subject_importance(point_data['subject'])
    subject_adjustment = (subject_weight - 0.5) * 30
    
    # 考点层级调整 (0-15%)
    level_weight = analyze_level_importance(
        point_data['level1_point'], 
        point_data['level2_point'], 
        point_data['level3_point']
    )
    level_adjustment = (level_weight - 0.5) * 30
    
    # 计算最终覆盖率
    final_rate = base_rate + complexity_adjustment + subject_adjustment + level_adjustment
    
    # 确保覆盖率在合理范围内 (5-95%)
    final_rate = max(5, min(95, final_rate))
    
    return round(final_rate)

def generate_coverage_analysis():
    """生成覆盖率分析报告"""
    print("🔍 开始分析考点数据...")
    
    # 获取数据
    data = get_exam_points_data()
    if not data:
        print("❌ 无法获取考点数据")
        return
    
    print(f"📊 共获取到 {len(data)} 条考点数据")
    
    # 分析统计
    subject_stats = defaultdict(list)
    coverage_stats = defaultdict(int)
    complexity_stats = []
    
    updated_data = []
    
    for point in data:
        # 解包数据 (id, province, subject, grade, semester, level1_point, level2_point, level3_point, description, coverage_rate)
        point_id, province, subject, grade, semester, level1_point, level2_point, level3_point, description, coverage_rate = point
        
        # 构建数据字典
        point_dict = {
            'id': point_id,
            'province': province,
            'subject': subject,
            'grade': grade,
            'semester': semester,
            'level1_point': level1_point,
            'level2_point': level2_point,
            'level3_point': level3_point,
            'description': description,
            'coverage_rate': coverage_rate
        }
        
        # 计算科学覆盖率
        scientific_rate = calculate_scientific_coverage_rate(point_dict)
        
        # 分析复杂度
        complexity = analyze_content_complexity(description)
        
        # 统计信息
        subject_stats[subject].append(scientific_rate)
        coverage_stats[scientific_rate] += 1
        complexity_stats.append(complexity)
        
        # 准备更新数据
        updated_point = point_dict.copy()
        updated_point['scientific_coverage_rate'] = scientific_rate
        updated_point['complexity_score'] = complexity
        updated_data.append(updated_point)
    
    # 生成分析报告
    print("\n📈 覆盖率分析报告:")
    print("=" * 50)
    
    # 科目统计
    print("\n📚 各科目平均覆盖率:")
    for subject, rates in subject_stats.items():
        avg_rate = sum(rates) / len(rates)
        print(f"  {subject}: {avg_rate:.1f}% ({len(rates)} 个考点)")
    
    # 覆盖率分布
    print("\n📊 覆盖率分布:")
    for rate in sorted(coverage_stats.keys()):
        count = coverage_stats[rate]
        percentage = (count / len(data)) * 100
        print(f"  {rate}%: {count} 个考点 ({percentage:.1f}%)")
    
    # 复杂度统计
    avg_complexity = sum(complexity_stats) / len(complexity_stats)
    print(f"\n🧮 平均复杂度评分: {avg_complexity:.1f}/10")
    
    # 建议更新
    print(f"\n💡 建议更新 {len(data)} 条记录的覆盖率")
    
    return updated_data

def update_database_coverage(updated_data):
    """更新数据库中的覆盖率"""
    connection = connect_db()
    if not connection:
        print("❌ 无法连接数据库")
        return False
    
    try:
        with connection.cursor() as cursor:
            updated_count = 0
            for point in updated_data:
                cursor.execute("""
                    UPDATE exam_points 
                    SET coverage_rate = %s, updated_at = NOW()
                    WHERE id = %s
                """, (point['scientific_coverage_rate'], point['id']))
                updated_count += 1
            
            connection.commit()
            print(f"✅ 成功更新 {updated_count} 条记录的覆盖率")
            return True
            
    except Exception as e:
        print(f"❌ 更新数据库失败: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def add_coverage_analysis_columns():
    """添加覆盖率分析相关列"""
    connection = connect_db()
    if not connection:
        print("❌ 无法连接数据库")
        return False
    
    try:
        with connection.cursor() as cursor:
            # 添加复杂度评分列
            cursor.execute("""
                ALTER TABLE exam_points 
                ADD COLUMN complexity_score DECIMAL(3,1) DEFAULT 1.0
                COMMENT '内容复杂度评分 (1-10)'
            """)
            print("✅ 添加复杂度评分列")
            
            # 添加分析时间列
            cursor.execute("""
                ALTER TABLE exam_points 
                ADD COLUMN analyzed_at DATETIME DEFAULT NULL
                COMMENT '覆盖率分析时间'
            """)
            print("✅ 添加分析时间列")
            
            connection.commit()
            return True
            
    except Exception as e:
        print(f"❌ 添加列失败: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def main():
    """主函数"""
    print("🎯 考点覆盖率科学分析工具")
    print("=" * 50)
    
    # 生成分析报告
    updated_data = generate_coverage_analysis()
    if not updated_data:
        return
    
    # 询问是否更新数据库
    print("\n❓ 是否要更新数据库中的覆盖率? (y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            # 添加新列
            if add_coverage_analysis_columns():
                # 更新覆盖率
                if update_database_coverage(updated_data):
                    print("\n🎉 覆盖率更新完成!")
                    
                    # 显示更新后的统计
                    connection = connect_db()
                    if connection:
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                SELECT 
                                    MIN(coverage_rate) as min_rate,
                                    MAX(coverage_rate) as max_rate,
                                    AVG(coverage_rate) as avg_rate,
                                    COUNT(*) as total_count
                                FROM exam_points
                            """)
                            stats = cursor.fetchone()
                            if stats:
                                print(f"\n📊 更新后统计:")
                                print(f"  最小覆盖率: {stats[0]}%")
                                print(f"  最大覆盖率: {stats[1]}%")
                                print(f"  平均覆盖率: {stats[2]:.1f}%")
                                print(f"  总记录数: {stats[3]}")
                            else:
                                print("❌ 无法获取更新后统计")
                        connection.close()
                else:
                    print("❌ 覆盖率更新失败")
            else:
                print("❌ 表结构更新失败")
        else:
            print("⏭️  跳过数据库更新")
    except KeyboardInterrupt:
        print("\n⏹️  操作已取消")

if __name__ == "__main__":
    main() 