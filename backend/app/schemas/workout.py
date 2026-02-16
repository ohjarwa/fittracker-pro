from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ===== 训练组 Schemas =====

class WorkoutSetBase(BaseModel):
    """训练组基础模型"""
    exercise_id: int
    set_order: int = Field(..., ge=1)
    weight: float = Field(..., gt=0)
    reps: int = Field(..., ge=1)
    rpe: Optional[int] = Field(None, ge=1, le=10)
    rest_seconds: Optional[int] = Field(None, ge=0)
    tempo: Optional[str] = None
    notes: Optional[str] = None


class WorkoutSetCreate(WorkoutSetBase):
    """创建训练组"""
    pass


class WorkoutSetUpdate(BaseModel):
    """更新训练组"""
    exercise_id: Optional[int] = None
    set_order: Optional[int] = Field(None, ge=1)
    weight: Optional[float] = Field(None, gt=0)
    reps: Optional[int] = Field(None, ge=1)
    rpe: Optional[int] = Field(None, ge=1, le=10)
    rest_seconds: Optional[int] = Field(None, ge=0)
    tempo: Optional[str] = None
    notes: Optional[str] = None


class WorkoutSetResponse(WorkoutSetBase):
    """训练组响应"""
    id: int
    session_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== 训练课 Schemas =====

class WorkoutSessionBase(BaseModel):
    """训练课基础模型"""
    date: date
    duration_min: Optional[int] = Field(None, ge=0)
    body_weight: Optional[float] = Field(None, gt=0)
    overall_rpe: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    template_name: Optional[str] = None


class WorkoutSessionCreate(WorkoutSessionBase):
    """创建训练课（含训练组）"""
    sets: List[WorkoutSetCreate] = []


class WorkoutSessionUpdate(BaseModel):
    """更新训练课"""
    date: Optional[date] = None
    duration_min: Optional[int] = Field(None, ge=0)
    body_weight: Optional[float] = Field(None, gt=0)
    overall_rpe: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    template_name: Optional[str] = None


class WorkoutSessionResponse(WorkoutSessionBase):
    """训练课响应（不含组详情）"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkoutSessionDetailResponse(WorkoutSessionResponse):
    """训练课详情响应（含组详情）"""
    sets: List[WorkoutSetResponse] = []


class WorkoutSessionListResponse(BaseModel):
    """训练课列表响应"""
    total: int
    items: List[WorkoutSessionResponse]


# ===== 训练模板 Schemas =====

class WorkoutTemplateCreate(BaseModel):
    """从训练课创建模板"""
    template_name: str


class WorkoutFromTemplateCreate(BaseModel):
    """从模板创建训练课"""
    template_name: str
    date: date
