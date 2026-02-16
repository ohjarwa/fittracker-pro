from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Exercise(Base, TimestampMixin):
    """动作模型（动作库）"""
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # 动作名称（中文）
    name_en: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 英文名称

    # 肌群分类
    primary_muscle: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # 主要肌群
    secondary_muscles: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # 辅助肌群

    # 动作属性
    category: Mapped[str] = mapped_column(String(20), nullable=False)  # compound/isolation
    equipment: Mapped[str] = mapped_column(String(50), nullable=False)  # 所需器械
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 难度 1-5

    # 自定义动作标识
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    # 描述
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 关系
    user = relationship("User", back_populates="exercises", foreign_keys=[user_id])
    workout_sets = relationship("WorkoutSet", back_populates="exercise")


# 肌群枚举值（用于参考）
MUSCLE_GROUPS = [
    "chest",       # 胸部
    "back",        # 背部
    "shoulders",   # 肩部
    "biceps",      # 肱二头肌
    "triceps",     # 肱三头肌
    "forearms",    # 前臂
    "quads",       # 股四头肌
    "hamstrings",  # 股二头肌
    "glutes",      # 臀部
    "calves",      # 小腿
    "core",        # 核心
    "full_body",   # 全身
]

# 动作分类
EXERCISE_CATEGORIES = ["compound", "isolation"]

# 器械类型
EQUIPMENT_TYPES = [
    "barbell",      # 杠铃
    "dumbbell",     # 哑铃
    "machine",      # 固定器械
    "cable",        # 龙门架/绳索
    "bodyweight",   # 自重
    "kettlebell",   # 壶铃
    "band",         # 弹力带
    "other",        # 其他
]
