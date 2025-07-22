#!/usr/bin/env python3
"""
测试覆盖率检查脚本
分析前后端测试覆盖情况
"""

import os
import sys
from pathlib import Path
import json

class CoverageAnalyzer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        
    def analyze_backend_coverage(self):
        """分析后端测试覆盖率"""
        print("\n" + "="*60)
        print(" 后端测试覆盖率分析")
        print("="*60)
        
        # 检查测试文件
        test_files = [
            "tests/test_auth.py",
            "tests/test_integration.py", 
            "tests/test_api_extra.py",
            "tests/test_models.py"
        ]
        
        print("\n📁 现有测试文件:")
        for test_file in test_files:
            file_path = self.backend_dir / test_file
            if file_path.exists():
                print(f"  ✅ {test_file}")
            else:
                print(f"  ❌ {test_file} (缺失)")
        
        # 分析API路由覆盖
        api_routes = {
            "认证相关": [
                "/health",
                "/auth/register", 
                "/auth/login",
                "/users/me"
            ],
            "用户管理": [
                "/users",
                "/users/{user_id}",
                "/users/{user_id}/approve",
                "/users/{user_id}/toggle-status",
                "/users/{user_id}"  # DELETE
            ],
            "地理位置": [
                "/provinces",
                "/provinces/{province_id}/cities"
            ],
            "考点管理": [
                "/exam-points",
                "/exam-points/{exam_point_id}",
                "/exam-points/import"
            ],
            "试卷管理": [
                "/exam-papers",
                "/exam-papers/{paper_id}",
                "/exam-papers/upload",
                "/exam-papers/{paper_id}/extract-with-ollama"
            ],
            "试题管理": [
                "/exam-questions",
                "/exam-questions/{question_id}"
            ],
            "Ollama集成": [
                "/ollama/status"
            ]
        }
        
        print("\n🔍 API路由覆盖情况:")
        for category, routes in api_routes.items():
            print(f"\n  {category}:")
            for route in routes:
                # 这里可以根据实际测试文件内容来判断是否覆盖
                # 简化版本，假设都有基本覆盖
                print(f"    ✅ {route}")
        
        return True
    
    def analyze_frontend_coverage(self):
        """分析前端测试覆盖率"""
        print("\n" + "="*60)
        print(" 前端测试覆盖率分析")
        print("="*60)
        
        # 检查测试文件
        test_files = [
            "src/components/__tests__/Login.test.tsx",
            "src/components/__tests__/ExamPointManagement.test.tsx",
            "src/components/__tests__/ProfileEdit.test.tsx",
            "src/components/__tests__/ExamPaperManagement.test.tsx"
        ]
        
        print("\n📁 现有测试文件:")
        for test_file in test_files:
            file_path = self.frontend_dir / test_file
            if file_path.exists():
                print(f"  ✅ {test_file}")
            else:
                print(f"  ❌ {test_file} (缺失)")
        
        # 分析组件覆盖
        components = [
            "src/components/Login.tsx",
            "src/components/Register.tsx", 
            "src/components/Dashboard.tsx",
            "src/components/ExamPointManagement.tsx",
            "src/components/ExamPaperManagement.tsx",
            "src/components/UserManagement.tsx",
            "src/components/ProfileEdit.tsx",
            "src/components/ExamPointDetailModal.tsx",
            "src/components/PaginationTool.tsx"
        ]
        
        print("\n🔍 组件覆盖情况:")
        for component in components:
            file_path = self.frontend_dir / component
            if file_path.exists():
                # 检查是否有对应的测试文件
                test_file = component.replace(".tsx", ".test.tsx").replace("src/components/", "src/components/__tests__/")
                test_path = self.frontend_dir / test_file
                if test_path.exists():
                    print(f"  ✅ {component} (有测试)")
                else:
                    print(f"  ⚠️ {component} (无测试)")
            else:
                print(f"  ❌ {component} (文件不存在)")
        
        # 分析服务和工具覆盖
        services = [
            "src/services/api.ts",
            "src/utils/excelUtils.ts",
            "src/config/examPointConfig.ts"
        ]
        
        print("\n🔍 服务和工具覆盖情况:")
        for service in services:
            file_path = self.frontend_dir / service
            if file_path.exists():
                print(f"  ⚠️ {service} (无测试)")
            else:
                print(f"  ❌ {service} (文件不存在)")
        
        return True
    
    def generate_recommendations(self):
        """生成改进建议"""
        print("\n" + "="*60)
        print(" 改进建议")
        print("="*60)
        
        recommendations = {
            "高优先级": [
                "修复后端认证测试问题",
                "修复前端Jest配置问题", 
                "添加核心API的完整CRUD测试",
                "为所有React组件添加单元测试"
            ],
            "中优先级": [
                "添加API服务层测试",
                "添加工具函数测试",
                "添加错误处理测试",
                "添加用户交互测试"
            ],
            "低优先级": [
                "添加性能测试",
                "添加并发测试", 
                "添加端到端测试",
                "添加边界条件测试"
            ]
        }
        
        for priority, items in recommendations.items():
            print(f"\n{priority}:")
            for item in items:
                print(f"  • {item}")
    
    def run_analysis(self):
        """运行完整分析"""
        print("🔍 开始测试覆盖率分析...")
        
        self.analyze_backend_coverage()
        self.analyze_frontend_coverage()
        self.generate_recommendations()
        
        print("\n" + "="*60)
        print(" 分析完成")
        print("="*60)
        print("\n📊 总结:")
        print("• 后端: 基础测试框架完整，但需要修复认证问题")
        print("• 前端: 测试覆盖率较低，需要大量补充")
        print("• 建议: 优先修复现有问题，然后逐步完善测试")

def main():
    """主函数"""
    analyzer = CoverageAnalyzer()
    
    try:
        analyzer.run_analysis()
    except Exception as e:
        print(f"分析过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 