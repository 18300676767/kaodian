#!/usr/bin/env python3
import requests
import json

def test_pagination():
    base_url = "http://localhost:8000"
    
    print("🚀 开始分页功能测试...")
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ 健康检查: {response.status_code}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return
    
    # 2. 测试获取所有考点数据
    print("\n2. 测试获取所有考点数据")
    try:
        response = requests.get(f"{base_url}/exam-points")
        print(f"✅ 获取所有数据: {response.status_code}")
        data = response.json()
        print(f"总数据条数: {len(data) if isinstance(data, list) else '未知'}")
    except Exception as e:
        print(f"❌ 获取所有数据失败: {e}")
        return
    
    # 3. 测试分页功能
    print("\n3. 测试分页功能")
    page_sizes = [5, 10, 20, 50]
    
    for page_size in page_sizes:
        print(f"\n--- 测试每页 {page_size} 条数据 ---")
        
        try:
            response = requests.get(f"{base_url}/exam-points?page=1&page_size={page_size}")
            print(f"✅ 第1页 (每页{page_size}条): {response.status_code}")
            data = response.json()
            if isinstance(data, list):
                print(f"返回数据条数: {len(data)}")
        except Exception as e:
            print(f"❌ 第1页测试失败: {e}")
    
    print("\n🎉 分页功能测试完成！")

if __name__ == "__main__":
    test_pagination()
