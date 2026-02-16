from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：初始化数据库
    await init_db()
    yield
    # 关闭时：清理资源


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description="智能健身训练管理系统 API",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}


# 注册路由
from app.routers import auth, exercises, workouts, analysis
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["动作库"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["训练记录"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["数据分析"])
