from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.database import get_db
from app.models.exercise import Exercise, MUSCLE_GROUPS, EXERCISE_CATEGORIES, EQUIPMENT_TYPES
from app.models.user import User
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseResponse,
    ExerciseListResponse,
)
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=ExerciseListResponse)
async def get_exercises(
    muscle_group: Optional[str] = Query(None, description="按肌群筛选"),
    category: Optional[str] = Query(None, description="按分类筛选 (compound/isolation)"),
    equipment: Optional[str] = Query(None, description="按器械筛选"),
    search: Optional[str] = Query(None, description="搜索动作名称"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    """获取动作列表（预置动作 + 用户自定义动作）"""
    query = select(Exercise).where(
        or_(
            Exercise.is_custom == False,  # 预置动作
            Exercise.user_id == current_user.id if current_user else False,  # 或用户自己的自定义动作
        )
    )

    # 筛选条件
    if muscle_group:
        query = query.where(Exercise.primary_muscle == muscle_group)
    if category:
        query = query.where(Exercise.category == category)
    if equipment:
        query = query.where(Exercise.equipment == equipment)
    if search:
        query = query.where(
            or_(
                Exercise.name.contains(search),
                Exercise.name_en.contains(search),
            )
        )

    # 计算总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 分页
    query = query.order_by(Exercise.id).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    exercises = result.scalars().all()

    return ExerciseListResponse(total=total, items=exercises)


@router.get("/muscle-groups")
async def get_muscle_groups():
    """获取所有肌群分类"""
    return {"muscle_groups": MUSCLE_GROUPS}


@router.get("/equipment-types")
async def get_equipment_types():
    """获取所有器械类型"""
    return {"equipment_types": EQUIPMENT_TYPES}


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    """获取单个动作详情"""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="动作不存在",
        )

    # 检查权限：自定义动作只有创建者可以查看
    if exercise.is_custom and (not current_user or exercise.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="动作不存在",
        )

    return exercise


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise_create: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建自定义动作"""
    # 验证分类
    if exercise_create.category not in EXERCISE_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"分类必须是: {EXERCISE_CATEGORIES}",
        )

    # 验证肌群
    if exercise_create.primary_muscle not in MUSCLE_GROUPS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"肌群必须是: {MUSCLE_GROUPS}",
        )

    exercise = Exercise(
        **exercise_create.model_dump(),
        is_custom=True,
        user_id=current_user.id,
    )
    db.add(exercise)
    await db.flush()
    await db.refresh(exercise)

    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新自定义动作"""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="动作不存在",
        )

    # 检查权限
    if not exercise.is_custom or exercise.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此动作",
        )

    # 更新字段
    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercise, field, value)

    await db.flush()
    await db.refresh(exercise)

    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除自定义动作"""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="动作不存在",
        )

    # 检查权限
    if not exercise.is_custom or exercise.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此动作",
        )

    await db.delete(exercise)
