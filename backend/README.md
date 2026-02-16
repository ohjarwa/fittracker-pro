# FitTracker Pro Backend

智能健身训练管理系统后端 API

## 技术栈

- **框架**: FastAPI
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT
- **数据验证**: Pydantic v2

## 快速开始

### 1. 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 根据需要修改 .env 文件
```

### 3. 启动服务

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload

# 指定端口
uvicorn app.main:app --reload --port 8000
```

### 4. 填充预置动作数据

```bash
python -m seeds.exercises
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 路由

| 模块 | 路径 | 说明 |
|------|------|------|
| 认证 | `/api/auth` | 注册、登录、Token 刷新 |
| 动作库 | `/api/exercises` | 动作 CRUD、肌群/器械分类 |
| 训练记录 | `/api/workouts` | 训练课/训练组 CRUD、模板 |
| 数据分析 | `/api/analysis` | 1RM 推算、容量统计、进步报告 |

## 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # SQLAlchemy 模型
│   ├── schemas/             # Pydantic 模型
│   ├── routers/             # API 路由
│   ├── services/            # 业务逻辑
│   └── utils/               # 工具函数
├── migrations/              # Alembic 迁移
├── seeds/                   # 初始数据脚本
├── requirements.txt
├── alembic.ini
└── .env
```

## 数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回退迁移
alembic downgrade -1
```

## 测试示例

### 注册用户

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 登录获取 Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

### 使用 Token 访问 API

```bash
curl "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer <your_access_token>"
```
