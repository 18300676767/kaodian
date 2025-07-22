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

- 🤖 **AI智能提取**：基于Ollama模型自动从文档中提取试题信息
- 📊 **考点管理**：完整的考点CRUD操作和批量导入导出
- 📝 **试题管理**：高考试题的全生命周期管理
- 👥 **用户管理**：多级用户权限和审核机制
- 📈 **数据分析**：考点覆盖率和统计分析
- 🎨 **现代化UI**：响应式设计，用户体验优秀
- 🔐 **安全认证**：JWT Token认证，数据安全可靠

## 🏗️ 技术架构

### 后端技术栈
- **Python 3.11+** - 主要开发语言
- **FastAPI** - 高性能异步Web框架
- **SQLAlchemy** - ORM数据库操作
- **PyMySQL** - MySQL数据库连接
- **JWT** - 用户认证和授权
- **Ollama** - AI模型集成（qwen2.5:7b）
- **Uvicorn** - ASGI服务器

### 前端技术栈
- **React 18** - 用户界面库
- **TypeScript** - 类型安全的JavaScript
- **Tailwind CSS** - 实用优先的CSS框架
- **React Router** - 客户端路由管理
- **Axios** - HTTP客户端
- **XLSX** - Excel文件处理
- **KaTeX** - 数学公式渲染

### 数据库
- **MySQL 8.0+** - 关系型数据库

## 📋 系统要求

- Python 3.11+
- Node.js 16+
- MySQL 8.0+
- Conda环境 (kaodian)
- Ollama服务 (可选，用于AI功能)

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/18300676767/kaodian.git
cd kaodian
```

### 2. 数据库配置
确保MySQL服务正在运行，并创建数据库：
```sql
CREATE DATABASE kaodian CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'admin'@'localhost' IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON kaodian.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 后端设置
```bash
cd backend
conda activate kaodian
pip install -r requirements.txt
```

### 4. 前端设置
```bash
cd frontend
npm install
```

### 5. 启动系统

#### 启动后端服务
```bash
cd backend
conda activate kaodian
python start.py
```
后端将在 http://localhost:8000 运行
API文档: http://localhost:8000/docs

#### 启动前端服务
```bash
cd frontend
npm start
```
前端将在 http://localhost:3000 运行

## 📁 项目结构

```
kaodian/
├── backend/                    # 后端服务
│   ├── main.py                # FastAPI主应用
│   ├── models.py              # 数据模型定义
│   ├── schemas.py             # Pydantic数据验证模型
│   ├── auth.py                # 认证和授权逻辑
│   ├── ollama_service.py      # AI服务集成
│   ├── database.py            # 数据库配置
│   ├── config.py              # 系统配置
│   ├── utils.py               # 工具函数
│   ├── requirements.txt       # Python依赖
│   ├── start.py               # 启动脚本
│   └── uploads/               # 文件上传目录
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/        # React组件
│   │   │   ├── Dashboard.tsx  # 主仪表板
│   │   │   ├── Login.tsx      # 登录组件
│   │   │   ├── Register.tsx   # 注册组件
│   │   │   ├── UserManagement.tsx      # 用户管理
│   │   │   ├── ExamPointManagement.tsx # 考点管理
│   │   │   └── ExamPaperManagement.tsx # 试题管理
│   │   ├── services/          # API服务层
│   │   ├── utils/             # 工具函数
│   │   ├── config/            # 配置文件
│   │   └── App.tsx            # 主应用组件
│   ├── package.json           # Node.js依赖
│   └── tailwind.config.js     # Tailwind配置
├── tests/                      # 测试文件
├── docs/                       # 文档目录
└── README.md                   # 项目说明
```

## 🔧 功能模块

### 1. 用户认证系统
- ✅ 用户注册和登录
- ✅ JWT Token认证
- ✅ 用户信息管理
- ✅ 密码加密存储
- ✅ 会话管理

### 2. 用户管理系统
- ✅ 用户列表查看
- ✅ 用户信息编辑
- ✅ 用户审核机制
- ✅ 用户状态管理（激活/禁用/删除）
- ✅ 省份城市级联选择

### 3. 考点管理系统
- ✅ 考点CRUD操作
- ✅ 多条件查询（省份、科目、年级、学期等）
- ✅ Excel批量导入/导出
- ✅ JSON批量导入
- ✅ 分页显示
- ✅ 考点详情查看
- ✅ 覆盖率统计

### 4. 高考试题管理系统
- ✅ 试卷管理（CRUD）
- ✅ 试题管理（CRUD）
- ✅ 文件上传功能
- ✅ AI智能提取试题
- ✅ 试题预览功能
- ✅ 多种题型支持
- ✅ 答案和解析管理

### 5. AI智能功能
- ✅ Ollama模型集成
- ✅ 智能文档解析
- ✅ 试题自动提取
- ✅ 多格式文件支持（TXT、DOCX、PDF、MD）
- ✅ 结构化数据输出

## 🔐 安全特性

- **JWT认证**：安全的用户认证机制
- **密码加密**：使用bcrypt进行密码哈希
- **文件验证**：上传文件类型和大小验证
- **SQL注入防护**：使用ORM防止SQL注入
- **CORS配置**：跨域请求安全控制
- **输入验证**：Pydantic模型数据验证

## 📊 API接口

### 认证相关
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `GET /users/me` - 获取当前用户信息

### 用户管理
- `GET /users` - 获取用户列表
- `PUT /users/{user_id}` - 更新用户信息
- `PUT /users/{user_id}/approve` - 审核用户
- `PUT /users/{user_id}/toggle-status` - 切换用户状态
- `DELETE /users/{user_id}` - 删除用户

### 考点管理
- `GET /exam-points` - 获取考点列表
- `POST /exam-points` - 创建考点
- `PUT /exam-points/{id}` - 更新考点
- `DELETE /exam-points/{id}` - 删除考点
- `POST /exam-points/import` - 批量导入考点

### 试题管理
- `GET /exam-papers` - 获取试卷列表
- `POST /exam-papers` - 创建试卷
- `POST /exam-papers/upload` - 上传试卷文件
- `POST /exam-papers/{paper_id}/extract-with-ollama` - AI提取试题
- `GET /exam-questions` - 获取试题列表

### 系统相关
- `GET /health` - 健康检查
- `GET /provinces` - 获取省份列表
- `GET /provinces/{province_id}/cities` - 获取城市列表

## 🎨 界面预览

### 登录页面
- 现代化设计风格
- 渐变背景效果
- 表单验证和错误提示
- 响应式布局

### 主仪表板
- 功能模块卡片展示
- 用户信息显示
- 导航菜单
- 实时状态更新

### 考点管理
- 数据表格展示
- 搜索和筛选功能
- 批量操作支持
- 导入导出功能

### 试题管理
- 试卷列表管理
- 试题详情查看
- 文件上传界面
- AI提取结果展示

## 🧪 测试

### 运行测试
```bash
# 后端测试
cd backend
python -m pytest

# 前端测试
cd frontend
npm test
```

### 测试覆盖
- 单元测试
- 集成测试
- API接口测试
- 前端组件测试

## 🚀 部署

### 生产环境部署
```bash
# 后端部署
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# 前端部署
cd frontend
npm run build
```

### Docker部署（可选）
```dockerfile
# 后端Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 配置说明

### 环境变量
```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://admin:111111@localhost:3306/kaodian

# JWT配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama配置
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:7b

# 文件上传配置
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800
```

### 数据库配置
- 支持MySQL 8.0+
- 字符集：utf8mb4
- 排序规则：utf8mb4_unicode_ci

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查MySQL服务状态
   sudo systemctl status mysql
   
   # 检查数据库连接
   mysql -u admin -p -h localhost
   ```

2. **前端无法连接后端**
   - 确认后端服务正在运行
   - 检查CORS配置
   - 验证API地址和端口

3. **AI功能无法使用**
   - 确认Ollama服务已启动
   - 检查模型是否已下载
   - 验证Ollama配置

4. **文件上传失败**
   - 检查上传目录权限
   - 验证文件大小限制
   - 确认文件格式支持

### 日志查看
```bash
# 后端日志
tail -f backend/backend.log

# 前端日志
# 查看浏览器开发者工具控制台
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 开发规范
- 遵循PEP 8 Python代码规范
- 使用TypeScript进行前端开发
- 编写单元测试
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **18300676767** - *初始工作* - [GitHub](https://github.com/18300676767)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的Python Web框架
- [React](https://reactjs.org/) - 用户界面库
- [Tailwind CSS](https://tailwindcss.com/) - CSS框架
- [Ollama](https://ollama.ai/) - AI模型服务

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看 [Issues](https://github.com/18300676767/kaodian/issues) 页面
2. 创建新的 Issue
3. 联系项目维护者

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
