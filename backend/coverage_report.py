#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考点覆盖率详细分析报告
生成科学合理的覆盖率分析报告
"""

import pymysql
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

def get_detailed_data():
    """获取详细数据"""
    connection = connect_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, province, subject, grade, semester, 
                       level1_point, level2_point, level3_point, 
                       description, coverage_rate, complexity_score
                FROM exam_points
                ORDER BY subject, coverage_rate DESC
            """)
            return cursor.fetchall()
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []
    finally:
        connection.close()

def generate_detailed_report():
    """生成详细分析报告"""
    print("📊 考点覆盖率详细分析报告")
    print("=" * 60)
    
    data = get_detailed_data()
    if not data:
        print("❌ 无法获取数据")
        return
    
    # 统计信息
    total_count = len(data)
    subject_stats = defaultdict(list)
    coverage_ranges = defaultdict(int)
    complexity_stats = []
    
    # 分析数据
    for point in data:
        point_id, province, subject, grade, semester, level1_point, level2_point, level3_point, description, coverage_rate, complexity_score = point
        
        subject_stats[subject].append({
            'id': point_id,
            'coverage_rate': coverage_rate,
            'complexity_score': complexity_score,
            'level1': level1_point,
            'level2': level2_point,
            'level3': level3_point
        })
        
        # 覆盖率范围统计
        if coverage_rate < 50:
            coverage_ranges['低覆盖率(30-49%)'] += 1
        elif coverage_rate < 70:
            coverage_ranges['中覆盖率(50-69%)'] += 1
        else:
            coverage_ranges['高覆盖率(70%+)'] += 1
        
        complexity_stats.append(complexity_score)
    
    # 总体统计
    print(f"\n📈 总体统计:")
    print(f"  总考点数: {total_count}")
    print(f"  涉及科目: {len(subject_stats)} 个")
    print(f"  平均复杂度: {sum(complexity_stats)/len(complexity_stats):.1f}/10")
    
    # 覆盖率分布
    print(f"\n📊 覆盖率分布:")
    for range_name, count in coverage_ranges.items():
        percentage = (count / total_count) * 100
        print(f"  {range_name}: {count} 个考点 ({percentage:.1f}%)")
    
    # 各科目详细分析
    print(f"\n📚 各科目详细分析:")
    print("-" * 60)
    
    for subject, points in subject_stats.items():
        avg_coverage = sum(p['coverage_rate'] for p in points) / len(points)
        avg_complexity = sum(p['complexity_score'] for p in points) / len(points)
        max_coverage = max(p['coverage_rate'] for p in points)
        min_coverage = min(p['coverage_rate'] for p in points)
        
        print(f"\n🔸 {subject} ({len(points)} 个考点):")
        print(f"   平均覆盖率: {avg_coverage:.1f}%")
        print(f"   覆盖率范围: {min_coverage}% - {max_coverage}%")
        print(f"   平均复杂度: {avg_complexity:.1f}/10")
        
        # 显示该科目中覆盖率最高的3个考点
        top_points = sorted(points, key=lambda x: x['coverage_rate'], reverse=True)[:3]
        print(f"   高覆盖率考点:")
        for point in top_points:
            level_info = point['level3'] or point['level2'] or point['level1']
            print(f"     - {level_info}: {point['coverage_rate']}% (复杂度: {point['complexity_score']})")
    
    # 科学建议
    print(f"\n💡 科学建议:")
    print("-" * 60)
    
    # 分析各科目的覆盖率合理性
    subject_analysis = {}
    for subject, points in subject_stats.items():
        avg_coverage = sum(p['coverage_rate'] for p in points) / len(points)
        
        # 根据科目特点给出建议
        if subject == '数学':
            if avg_coverage < 60:
                suggestion = "建议适当提高数学考点覆盖率，数学是高考核心科目"
            else:
                suggestion = "数学考点覆盖率合理"
        elif subject in ['语文', '英语']:
            if avg_coverage < 55:
                suggestion = "建议适当提高语言类科目覆盖率"
            else:
                suggestion = "语言类科目覆盖率合理"
        elif subject in ['物理', '化学']:
            if avg_coverage < 50:
                suggestion = "理科科目覆盖率偏低，建议适当提高"
            else:
                suggestion = "理科科目覆盖率合理"
        else:
            if avg_coverage < 45:
                suggestion = "文科科目覆盖率偏低，建议适当提高"
            else:
                suggestion = "文科科目覆盖率合理"
        
        subject_analysis[subject] = {
            'avg_coverage': avg_coverage,
            'suggestion': suggestion
        }
    
    for subject, analysis in subject_analysis.items():
        print(f"  {subject}: {analysis['suggestion']} (当前平均: {analysis['avg_coverage']:.1f}%)")
    
    # 复杂度分析
    print(f"\n🧮 复杂度分析:")
    print("-" * 60)
    
    low_complexity = [c for c in complexity_stats if c < 2]
    medium_complexity = [c for c in complexity_stats if 2 <= c < 5]
    high_complexity = [c for c in complexity_stats if c >= 5]
    
    print(f"  低复杂度考点 (<2.0): {len(low_complexity)} 个 ({len(low_complexity)/total_count*100:.1f}%)")
    print(f"  中复杂度考点 (2.0-4.9): {len(medium_complexity)} 个 ({len(medium_complexity)/total_count*100:.1f}%)")
    print(f"  高复杂度考点 (≥5.0): {len(high_complexity)} 个 ({len(high_complexity)/total_count*100:.1f}%)")
    
    if len(high_complexity) > 0:
        print(f"  💡 发现 {len(high_complexity)} 个高复杂度考点，建议重点关注")
    
    # 生成JSON报告
    report_data = {
        'summary': {
            'total_points': total_count,
            'subject_count': len(subject_stats),
            'avg_complexity': float(sum(complexity_stats)/len(complexity_stats)),
            'coverage_ranges': dict(coverage_ranges)
        },
        'subjects': {
            subject: {
                'count': len(points),
                'avg_coverage': float(sum(p['coverage_rate'] for p in points) / len(points)),
                'avg_complexity': float(sum(p['complexity_score'] for p in points) / len(points)),
                'suggestion': subject_analysis[subject]['suggestion']
            }
            for subject, points in subject_stats.items()
        },
        'complexity_analysis': {
            'low': len(low_complexity),
            'medium': len(medium_complexity),
            'high': len(high_complexity)
        }
    }
    
    # 保存报告
    with open('coverage_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存到: coverage_analysis_report.json")
    print(f"🎯 覆盖率分析完成！")

def main():
    """主函数"""
    generate_detailed_report()

if __name__ == "__main__":
    main() 