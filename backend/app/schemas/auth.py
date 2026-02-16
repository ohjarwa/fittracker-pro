from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Token 响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 秒


class TokenPayload(BaseModel):
    """Token 载荷"""
    sub: int  # user_id
    exp: datetime
    type: str  # access / refresh


class LoginRequest(BaseModel):
    """登录请求"""
    email: str
    password: str


class RefreshRequest(BaseModel):
    """刷新 Token 请求"""
    refresh_token: str
