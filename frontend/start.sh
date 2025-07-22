#!/bin/bash

echo "🚀 启动高考考点分析系统..."
echo "📊 数据库: MySQL - kaodian"
echo "🔐 用户: admin / 密码: 111111"
echo "🌐 前端: http://localhost:3000"
echo "🔧 后端: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "=" * 50

# 检查conda环境
if ! conda info --envs | grep -q "kaodian"; then
    echo "❌ 错误: 未找到kaodian conda环境"
    echo "请先创建环境: conda create -n kaodian python=3.11"
    exit 1
fi

# 激活conda环境
echo "🔧 激活conda环境: kaodian"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate kaodian

# 检查MySQL连接
echo "🔍 检查数据库连接..."
python -c "
import pymysql
try:
    conn = pymysql.connect(
        host='localhost',
        user='admin',
        password='111111',
        database='kaodian'
    )
    print('✅ 数据库连接成功')
    conn.close()
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    print('请确保MySQL服务正在运行，并创建了kaodian数据库')
    exit(1)
"

# 启动后端
echo "🚀 启动后端服务..."
cd backend
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ 后端已启动 (PID: $BACKEND_PID)"

# 等待后端启动
sleep 3

# 测试后端API
echo "🔍 测试后端API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 后端API正常"
else
    echo "❌ 后端API测试失败"
fi

# 启动前端
echo "🚀 启动前端服务..."
cd ../frontend
nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ 前端已启动 (PID: $FRONTEND_PID)"

# 等待前端启动
sleep 10

# 测试前端
echo "🔍 测试前端服务..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务测试失败"
fi

echo ""
echo "🎉 系统启动完成！"
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "💡 提示:"
echo "- 首次使用请先注册账户"
echo "- 默认数据库: kaodian"
echo "- 默认用户: admin / 密码: 111111"
echo ""
echo "🛑 停止服务: pkill -f 'uvicorn\|npm start'"
echo "📋 查看日志: tail -f backend.log frontend.log" 