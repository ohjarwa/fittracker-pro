from datetime import date
from typing import Optional, List, Dict
from pydantic import BaseModel


# ===== 1RM 分析 =====

class OneRMTrendPoint(BaseModel):
    """1RM 趋势数据点"""
    date: date
    estimated_1rm: float
    source_weight: Optional[float] = None
    source_reps: Optional[int] = None
    source_rpe: Optional[int] = None
    confidence: Optional[float] = None


class OneRMTrendResponse(BaseModel):
    """1RM 趋势响应"""
    exercise_id: int
    exercise_name: str
    current_1rm: Optional[float] = None
    previous_1rm: Optional[float] = None
    change_percentage: Optional[float] = None
    trend: List[OneRMTrendPoint]


class OneRMCalculateRequest(BaseModel):
    """1RM 计算请求"""
    weight: float
    reps: int
    rpe: Optional[int] = None


class OneRMCalculateResponse(BaseModel):
    """1RM 计算响应"""
    estimated_1rm: float
    effective_reps: int
    method_weights: Dict[str, float]
    confidence: float


# ===== 容量分析 =====

class VolumeStatsPoint(BaseModel):
    """容量统计数据点"""
    date: date
    total_sets: int
    total_reps: int
    total_volume: float  # weight × reps
    exercises_count: int


class VolumeStatsResponse(BaseModel):
    """容量统计响应"""
    period: str  # week / month
    start_date: date
    end_date: date
    total_sessions: int
    total_sets: int
    total_reps: int
    total_volume: float
    daily_stats: List[VolumeStatsPoint]


class MuscleVolumePoint(BaseModel):
    """肌群容量数据点"""
    muscle_group: str
    total_sets: int
    total_volume: float
    percentage: float


class MuscleBalanceResponse(BaseModel):
    """肌群平衡分析响应"""
    period_start: date
    period_end: date
    muscle_volumes: List[MuscleVolumePoint]
    recommendations: List[str]


# ===== 进步报告 =====

class ExerciseProgress(BaseModel):
    """动作进步数据"""
    exercise_id: int
    exercise_name: str
    starting_1rm: Optional[float] = None
    current_1rm: Optional[float] = None
    progress_percentage: Optional[float] = None
    trend: str  # improving / plateau / declining


class ProgressReportResponse(BaseModel):
    """综合进步报告响应"""
    period_start: date
    period_end: date
    total_sessions: int
    total_volume: float
    exercises_progress: List[ExerciseProgress]
    summary: str
