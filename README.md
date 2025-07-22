# 高考考点分析系统 (Kaodian)

一个基于人工智能的高考考点分析和管理系统，帮助教师和学生更好地理解和掌握高考知识点。

## 🎯 项目简介

高考考点分析系统是一个现代化的Web应用，集成了AI智能分析、考点管理、试卷管理等功能。系统通过Ollama大语言模型对高考试题进行智能分析，自动提取考点信息，为教学和学习提供数据支持。

## ✨ 主要功能

### 🔐 用户管理
- 用户注册、登录、权限管理
- 多级用户角色（管理员、教师、学生）
- JWT Token认证

### �� 考点管理
- 考点信息的增删改查
- 按省份、科目、年级分类管理
- 考点覆盖率统计
- 支持批量导入考点数据

### �� 试卷管理
- 高考试卷上传和管理
- 支持多种文件格式（PDF、Word、Excel等）
- 试卷信息录入和查询
- 试卷与考点关联

### �� AI智能分析
- 基于Ollama大语言模型的试题分析
- 自动提取试题中的考点信息
- 智能识别题目类型和难度
- 生成考点覆盖率报告

### �� 数据统计
- 考点覆盖率可视化
- 试题分布统计
- 用户行为分析
- 导出Excel报告

## ��️ 技术架构

### 前端技术栈
- **React 18** - 现代化的前端框架
- **TypeScript** - 类型安全的JavaScript
- **React Router** - 路由管理
- **Axios** - HTTP客户端
- **Tailwind CSS** - 实用优先的CSS框架
- **KaTeX** - 数学公式渲染
- **XLSX** - Excel文件处理

### 后端技术栈
- **FastAPI** - 高性能Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL** - 关系型数据库
- **JWT** - 身份认证
- **Ollama** - 本地大语言模型服务
- **Uvicorn** - ASGI服务器

### 开发工具
- **pnpm** - 快速、节省磁盘空间的包管理器
- **pytest** - Python测试框架
- **Jest** - JavaScript测试框架
- **ESLint** - 代码质量检查

## 🚀 快速开始

### 环境要求
- Node.js 16+
- Python 3.11+
- MySQL 8.0+
- Ollama (本地AI模型服务)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd kaodian
```

2. **安装前端依赖**
```bash
cd frontend
pnpm install
```

3. **安装后端依赖**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

4. **配置数据库**
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE kaodian CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **配置环境变量**
```bash
# 编辑 backend/config.py 文件
# 修改数据库连接信息和其他配置
```

6. **启动Ollama服务**
```bash
# 确保Ollama服务运行在 http://127.0.0.1:11434
ollama serve
```

7. **启动应用**
```bash
# 使用管理脚本一键启动
./manage.sh start

# 或分别启动
# 后端
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 前端
cd frontend && pnpm start
```

### 访问地址
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📁 项目结构

```
kaodian/
├── frontend/                 # 前端React应用
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── services/        # API服务
│   │   ├── utils/           # 工具函数
│   │   └── config/          # 配置文件
│   ├── public/              # 静态资源
│   └── package.json         # 前端依赖
├── backend/                  # 后端FastAPI应用
│   ├── models.py            # 数据模型
│   ├── schemas.py           # 数据验证
│   ├── auth.py              # 认证模块
│   ├── ollama_service.py    # AI服务
│   ├── utils.py             # 工具函数
│   └── requirements.txt     # 后端依赖
├── test_reports/            # 测试报告
├── manage.sh                # 项目管理脚本
└── README.md               # 项目文档
```

## 🧪 测试

### 运行测试
```bash
# 后端测试
./manage.sh test

# 前端测试
cd frontend && pnpm test

# 端到端测试
python e2e_test.py
```

### 测试覆盖率
```bash
# 后端覆盖率
cd backend && pytest --cov=. --cov-report=html

# 前端覆盖率
cd frontend && pnpm test:coverage
```

## 📊 数据格式

### 考点数据结构
```json
{
  "province": "北京",
  "subject": "数学",
  "grade": "高三",
  "semester": "上学期",
  "level1_point": "集合、函数与导数",
  "level2_point": "集合的综合应用",
  "level3_point": "集合与函数定义域、值域的结合",
  "description": "详细的考点描述...",
  "coverage_rate": 90.0
}
```

##  管理脚本

项目提供了便捷的管理脚本 `manage.sh`：

```bash
# 启动所有服务
./manage.sh start

# 停止所有服务
./manage.sh stop

# 运行测试
./manage.sh test

# 检查服务状态
./manage.sh status

# 导入省份数据
./manage.sh import_provinces
```

##  贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

##  许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

##  联系方式

- 项目维护者: [您的姓名]
- 邮箱: [您的邮箱]
- 项目地址: [项目GitHub地址]

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的Python Web框架
- [React](https://reactjs.org/) - 用户界面库
- [Ollama](https://ollama.ai/) - 本地大语言模型服务
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的CSS框架

---

**注意**: 首次使用需要配置Ollama服务并下载相应的AI模型。建议使用国内镜像源加速下载。
