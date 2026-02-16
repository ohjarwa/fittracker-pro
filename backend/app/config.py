from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # 应用配置
    app_name: str = "FitTracker Pro"
    app_env: str = "development"
    debug: bool = True

    # 数据库配置
    database_url: str = "sqlite+aiosqlite:///./fittracker.db"

    # JWT 配置
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # 跨域配置
    cors_origins: str = '["http://localhost:3000","http://localhost:5173"]'

    @property
    def cors_origins_list(self) -> List[str]:
        import json
        return json.loads(self.cors_origins)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
