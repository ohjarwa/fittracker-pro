from datetime import date as DateType
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Text, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class WorkoutSession(Base, TimestampMixin):
    """训练课（一次完整训练）"""
    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # 训练基本信息
    date: Mapped[DateType] = mapped_column(Date, nullable=False, index=True)  # 训练日期
    duration_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 训练时长（分钟）
    body_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 当天体重

    # 训练评价
    overall_rpe: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 整体 RPE 1-10
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 训练备注

    # 模板相关
    template_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 来自的模板名称

    # 关系
    user = relationship("User", back_populates="workout_sessions")
    sets = relationship("WorkoutSet", back_populates="session", cascade="all, delete-orphan")


class WorkoutSet(Base, TimestampMixin):
    """训练组（单个动作的一组）"""
    __tablename__ = "workout_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("workout_sessions.id"), nullable=False, index=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)

    # 组数据
    set_order: Mapped[int] = mapped_column(Integer, nullable=False)  # 组序号
    weight: Mapped[float] = mapped_column(Float, nullable=False)  # 重量
    reps: Mapped[int] = mapped_column(Integer, nullable=False)  # 次数

    # 可选数据
    rpe: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # RPE 1-10
    rest_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 休息时长（秒）
    tempo: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 节奏 如 "3-1-2"
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 组备注

    # 关系
    session = relationship("WorkoutSession", back_populates="sets")
    exercise = relationship("Exercise", back_populates="workout_sets")
