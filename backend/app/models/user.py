from typing import Optional
from sqlalchemy import String, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    nickname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 用户身体数据
    body_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 体重 kg
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 身高 cm
    training_age: Mapped[Optional[int]] = mapped_column(Integer, default=0)  # 训练年限

    # 偏好设置
    unit_preference: Mapped[str] = mapped_column(String(10), default="kg")  # kg 或 lb
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 关系
    exercises = relationship("Exercise", back_populates="user", foreign_keys="Exercise.user_id")
    workout_sessions = relationship("WorkoutSession", back_populates="user")
    estimated_1rms = relationship("Estimated1RM", back_populates="user")
