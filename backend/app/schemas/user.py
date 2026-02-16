from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    nickname: Optional[str] = None


class UserCreate(UserBase):
    """用户注册请求"""
    password: str


class UserUpdate(BaseModel):
    """用户更新请求"""
    nickname: Optional[str] = None
    body_weight: Optional[float] = None
    height: Optional[float] = None
    training_age: Optional[int] = None
    unit_preference: Optional[str] = None


class UserResponse(UserBase):
    """用户响应"""
    id: int
    body_weight: Optional[float] = None
    height: Optional[float] = None
    training_age: Optional[int] = None
    unit_preference: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
