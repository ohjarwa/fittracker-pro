from datetime import date as DateType
from typing import Optional
from sqlalchemy import String, Integer, Float, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Estimated1RM(Base, TimestampMixin):
    """1RM 推算记录"""
    __tablename__ = "estimated_1rms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)

    # 推算结果
    date: Mapped[DateType] = mapped_column(Date, nullable=False, index=True)  # 推算日期
    estimated_1rm: Mapped[float] = mapped_column(Float, nullable=False)  # 推算的 1RM 值
    method: Mapped[str] = mapped_column(String(50), nullable=False)  # 使用的计算方法
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 置信度 0-1

    # 原始数据（用于追溯）
    source_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 原始重量
    source_reps: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 原始次数
    source_rpe: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 原始 RPE
    source_set_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("workout_sets.id"), nullable=True)

    # 关系
    user = relationship("User", back_populates="estimated_1rms")
    source_set = relationship("WorkoutSet")
