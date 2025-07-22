import random
import json
import requests
from datetime import datetime, timedelta

# 生成随机数据
provinces = ['北京', '上海', '广东', '江苏', '浙江', '山东', '河南', '四川', '湖北', '湖南']
subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理']
grades = ['高一', '高二', '高三']
semesters = ['上学期', '下学期']
level1_points = ['函数', '代数', '几何', '概率', '阅读', '写作', '实验', '分析', '综合']
level2_points = ['基础', '进阶', '应用', '拓展']
level3_points = ['A类', 'B类', 'C类', 'D类']

def random_date():
    start = datetime(2022, 1, 1)
    end = datetime(2024, 7, 1)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')

# 生成100条数据
data = []
for i in range(100):
    item = {
        "province": random.choice(provinces),
        "subject": random.choice(subjects),
        "grade": random.choice(grades),
        "semester": random.choice(semesters),
        "level1_point": random.choice(level1_points),
        "level2_point": random.choice(level2_points),
        "level3_point": random.choice(level3_points),
        "description": f"自动生成的考点描述 {i+1}",
        "coverage_rate": round(random.uniform(60, 100), 1),
        "added_by": f"user{random.randint(1,10)}",
        "added_date": random_date(),
        "is_active": random.choice([True, False])
    }
    data.append(item)

# 保存到JSON文件
with open('exam_points_sample.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ 已生成 exam_points_sample.json')

# 通过API导入数据
try:
    # 首先获取token（假设有一个默认用户）
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    # 尝试登录获取token
    response = requests.post('http://localhost:8000/auth/login', data=login_data)
    if response.status_code == 200:
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 导入数据
        import_data = {"exam_points": data}
        response = requests.post('http://localhost:8000/exam-points/import', 
                               json=import_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f'✅ 成功导入 {result.get("imported_count", 0)} 条考点数据')
        else:
            print(f'❌ 导入失败: {response.status_code} - {response.text}')
    else:
        print('❌ 登录失败，请确保后端服务运行且admin用户存在')
        
except requests.exceptions.ConnectionError:
    print('❌ 无法连接到后端服务，请确保后端在 http://localhost:8000 运行')
except Exception as e:
    print(f'❌ 导入过程中出现错误: {e}') 