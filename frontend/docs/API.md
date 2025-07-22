# API 文档

## 概述

高考考点分析系统提供RESTful API接口，支持用户认证、考点管理、试题管理等功能。

## 基础信息

- **Base URL**: `http://localhost:8000`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8

## 认证

### 获取访问令牌

```http
POST /auth/login
Content-Type: multipart/form-data

username=your_username&password=your_password
```

**响应示例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 使用令牌

在请求头中添加：
```
Authorization: Bearer <your_access_token>
```

## 用户管理

### 用户注册

```http
POST /auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "phone": "13800138000",
  "real_name": "张三",
  "age": 25,
  "grade": "高三",
  "province_id": 1,
  "city_id": 1
}
```

### 获取当前用户信息

```http
GET /users/me
Authorization: Bearer <token>
```

### 获取用户列表

```http
GET /users?skip=0&limit=100
Authorization: Bearer <token>
```

### 更新用户信息

```http
PUT /users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "newusername",
  "email": "newemail@example.com",
  "phone": "13900139000"
}
```

### 审核用户

```http
PUT /users/{user_id}/approve
Authorization: Bearer <token>
Content-Type: application/json

{
  "is_approved": true
}
```

### 切换用户状态

```http
PUT /users/{user_id}/toggle-status
Authorization: Bearer <token>
```

### 删除用户

```http
DELETE /users/{user_id}
Authorization: Bearer <token>
```

## 考点管理

### 获取考点列表

```http
GET /exam-points?province_id=1&subject=数学&grade=高三&semester=上学期
Authorization: Bearer <token>
```

**查询参数**:
- `province_id`: 省份ID
- `subject`: 科目
- `grade`: 年级
- `semester`: 学期
- `level1_point`: 一级考点
- `level2_point`: 二级考点
- `level3_point`: 三级考点
- `description`: 考点描述

### 创建考点

```http
POST /exam-points
Authorization: Bearer <token>
Content-Type: application/json

{
  "province_id": 1,
  "subject": "数学",
  "grade": "高三",
  "semester": "上学期",
  "level1_point": "函数",
  "level2_point": "基本初等函数",
  "level3_point": "指数函数",
  "description": "指数函数的基本性质和应用",
  "coverage_rate": 85,
  "added_by": "admin"
}
```

### 更新考点

```http
PUT /exam-points/{exam_point_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "description": "更新后的考点描述",
  "coverage_rate": 90
}
```

### 删除考点

```http
DELETE /exam-points/{exam_point_id}
Authorization: Bearer <token>
```

### 批量导入考点

```http
POST /exam-points/import
Authorization: Bearer <token>
Content-Type: application/json

{
  "exam_points": [
    {
      "province_id": 1,
      "subject": "数学",
      "grade": "高三",
      "semester": "上学期",
      "level1_point": "函数",
      "level2_point": "基本初等函数",
      "level3_point": "指数函数",
      "description": "指数函数的基本性质和应用",
      "coverage_rate": 85,
      "added_by": "admin"
    }
  ]
}
```

## 试题管理

### 获取试卷列表

```http
GET /exam-papers?year=2024&province_id=1&subject=数学
Authorization: Bearer <token>
```

### 创建试卷

```http
POST /exam-papers
Authorization: Bearer <token>
Content-Type: application/json

{
  "year": 2024,
  "province_id": 1,
  "subject": "数学",
  "paper_name": "2024年北京高考数学试卷",
  "total_score": 150,
  "exam_time": 120,
  "added_by": "admin"
}
```

### 上传试卷文件

```http
POST /exam-papers/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <file_data>
```

### AI提取试题

```http
POST /exam-papers/{paper_id}/extract-with-ollama
Authorization: Bearer <token>
```

### 获取试题列表

```http
GET /exam-questions?exam_paper_id=1&question_type=选择题
Authorization: Bearer <token>
```

### 创建试题

```http
POST /exam-questions
Authorization: Bearer <token>
Content-Type: application/json

{
  "exam_paper_id": 1,
  "question_number": "1",
  "question_type": "选择题",
  "question_content": "下列哪个选项...",
  "score": 5.0,
  "difficulty_level": "中等",
  "exam_points": "函数的基本性质",
  "answer_content": "A",
  "answer_explanation": "解析内容...",
  "added_by": "admin"
}
```

## 地理位置

### 获取省份列表

```http
GET /provinces
Authorization: Bearer <token>
```

### 获取城市列表

```http
GET /provinces/{province_id}/cities
Authorization: Bearer <token>
```

## 系统状态

### 健康检查

```http
GET /health
```

### Ollama状态检查

```http
GET /ollama/status
Authorization: Bearer <token>
```

## 错误处理

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 常见HTTP状态码

- `200`: 请求成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未授权
- `403`: 禁止访问
- `404`: 资源不存在
- `422`: 数据验证错误
- `500`: 服务器内部错误

## 数据模型

### 用户模型

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "phone": "13800138000",
  "real_name": "张三",
  "age": 25,
  "grade": "高三",
  "province_id": 1,
  "city_id": 1,
  "is_active": true,
  "is_approved": true,
  "is_deleted": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 考点模型

```json
{
  "id": 1,
  "province_id": 1,
  "subject": "数学",
  "grade": "高三",
  "semester": "上学期",
  "level1_point": "函数",
  "level2_point": "基本初等函数",
  "level3_point": "指数函数",
  "description": "指数函数的基本性质和应用",
  "coverage_rate": 85,
  "added_by": "admin",
  "added_date": "2024-01-01T00:00:00Z",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 试卷模型

```json
{
  "id": 1,
  "year": 2024,
  "province_id": 1,
  "subject": "数学",
  "paper_name": "2024年北京高考数学试卷",
  "file_path": "/uploads/paper.pdf",
  "file_type": "pdf",
  "total_score": 150,
  "exam_time": 120,
  "added_by": "admin",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 试题模型

```json
{
  "id": 1,
  "exam_paper_id": 1,
  "question_number": "1",
  "question_type": "选择题",
  "question_content": "题目内容...",
  "score": 5.0,
  "difficulty_level": "中等",
  "exam_points": "相关考点",
  "answer_content": "参考答案",
  "answer_explanation": "答案解析",
  "added_by": "admin",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
``` 