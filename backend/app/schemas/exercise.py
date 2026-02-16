from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    """动作基础模型"""
    name: str
    name_en: Optional[str] = None
    primary_muscle: str
    secondary_muscles: Optional[List[str]] = None
    category: str  # compound / isolation
    equipment: str
    difficulty: int = 1
    description: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    """创建自定义动作"""
    pass


class ExerciseUpdate(BaseModel):
    """更新动作"""
    name: Optional[str] = None
    name_en: Optional[str] = None
    primary_muscle: Optional[str] = None
    secondary_muscles: Optional[List[str]] = None
    category: Optional[str] = None
    equipment: Optional[str] = None
    difficulty: Optional[int] = None
    description: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    """动作响应"""
    id: int
    is_custom: bool
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExerciseListResponse(BaseModel):
    """动作列表响应"""
    total: int
    items: List[ExerciseResponse]
