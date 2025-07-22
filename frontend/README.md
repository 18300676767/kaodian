# 🎓 高考考点分析系统 (Kaodian)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.14-green.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9.5-blue.svg)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 一个基于AI智能分析的高考考点管理系统，支持试题自动提取、考点管理和数据分析

## 📖 项目简介

高考考点分析系统是一个现代化的教育管理平台，旨在帮助教育工作者更好地管理和分析高考考点信息。系统集成了AI智能功能，能够自动从文档中提取试题信息，并提供完整的考点管理、用户管理和数据分析功能。

### ✨ 核心特性

- 🤖 **AI智能提取**：基于Ollama大模型自动从文档中提取试题信息
- 📊 **考点管理**：完整的考点信息管理，支持Excel导入导出
- 👥 **用户管理**：多级用户权限管理，支持管理员和普通用户
- 📝 **试题管理**：试题库管理，支持多种题型和格式
- 📈 **数据分析**：考点分布分析和统计报表
- 🔐 **安全认证**：JWT token认证，确保数据安全
- 📱 **响应式设计**：支持多设备访问的现代化界面

## 🛠️ 技术栈

### 后端技术
- **Python 3.11+** - 主要开发语言
- **FastAPI** - 现代化Web框架
- **SQLAlchemy** - ORM数据库操作
- **PyMySQL** - MySQL数据库连接
- **JWT** - 用户认证
- **Uvicorn** - ASGI服务器
- **Ollama** - AI模型集成（qwen2.5:7b）

### 前端技术
- **React 18** - 用户界面框架
- **TypeScript** - 类型安全的JavaScript
- **Tailwind CSS** - 现代化CSS框架
- **React Router** - 客户端路由
- **Axios** - HTTP客户端
- **XLSX** - Excel文件处理
- **KaTeX** - 数学公式渲染

### 数据库
- **MySQL 8.0+** - 关系型数据库

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Ollama (用于AI功能)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/18300676767/kaodian.git
cd kaodian
```

2. **后端设置**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **数据库配置**
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE kaodian CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. **前端设置**
```bash
cd frontend
npm install
# 或使用pnpm
pnpm install
```

5. **启动服务**
```bash
# 启动后端 (在backend目录)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动前端 (在frontend目录)
npm start
# 或 pnpm start
```

6. **访问系统**
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📁 项目结构

```
kaodian/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI主应用
│   ├── models.py           # 数据库模型
│   ├── config.py           # 配置文件
│   ├── ollama_service.py   # AI服务集成
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # React组件
│   │   ├── services/       # API服务
│   │   ├── utils/          # 工具函数
│   │   └── config/         # 配置文件
│   ├── package.json        # Node.js依赖
│   └── public/             # 静态资源
├── docs/                   # 项目文档
│   ├── API.md             # API文档
│   └── DEPLOYMENT.md      # 部署指南
├── README.md              # 项目说明
├── LICENSE                # 开源协议
└── .gitignore            # Git忽略文件
```

## 🔧 功能模块

### 1. 用户管理
- 用户注册/登录
- 权限管理
- 个人信息管理

### 2. 考点管理
- 考点信息录入
- Excel批量导入
- 考点分类管理
- 数据导出

### 3. 试题管理
- 试题录入
- 文件上传解析
- AI智能提取
- 试题分类

### 4. 数据分析
- 考点分布统计
- 试题分析
- 报表生成

## 📚 API文档

详细的API文档请参考 [docs/API.md](docs/API.md)

### 主要接口
- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册
- `GET /users/` - 获取用户列表
- `GET /exam-points/` - 获取考点列表
- `POST /exam-points/` - 创建考点
- `GET /exam-papers/` - 获取试卷列表
- `POST /exam-papers/upload` - 上传试卷文件

## 🚀 部署

详细的部署指南请参考 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### 生产环境部署
1. 配置环境变量
2. 设置数据库
3. 配置Nginx反向代理
4. 使用Supervisor管理进程
5. 配置SSL证书

## 🧪 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

## 🔒 安全

- JWT token认证
- 密码加密存储
- CORS配置
- 输入验证
- SQL注入防护

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **18300676767** - *初始工作* - [GitHub](https://github.com/18300676767)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [React](https://reactjs.org/) - 用户界面库
- [Ollama](https://ollama.ai/) - 本地大语言模型
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的CSS框架

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
