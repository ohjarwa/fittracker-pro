from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.workout import WorkoutSession, WorkoutSet
from app.models.exercise import Exercise
from app.schemas.workout import (
    WorkoutSessionCreate,
    WorkoutSessionUpdate,
    WorkoutSessionResponse,
    WorkoutSessionDetailResponse,
    WorkoutSessionListResponse,
    WorkoutSetCreate,
    WorkoutSetUpdate,
    WorkoutSetResponse,
    WorkoutTemplateCreate,
    WorkoutFromTemplateCreate,
)
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=WorkoutSessionListResponse)
async def get_workout_sessions(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取训练记录列表"""
    query = select(WorkoutSession).where(WorkoutSession.user_id == current_user.id)

    # 日期筛选
    if start_date:
        query = query.where(WorkoutSession.date >= start_date)
    if end_date:
        query = query.where(WorkoutSession.date <= end_date)

    # 计算总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 分页
    query = query.order_by(WorkoutSession.date.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    sessions = result.scalars().all()

    return WorkoutSessionListResponse(total=total, items=sessions)


@router.post("", response_model=WorkoutSessionDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_workout_session(
    session_create: WorkoutSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建训练记录（含训练组）"""
    # 验证所有动作是否存在
    exercise_ids = list(set(s.exercise_id for s in session_create.sets))
    if exercise_ids:
        result = await db.execute(select(Exercise).where(Exercise.id.in_(exercise_ids)))
        exercises = result.scalars().all()
        found_ids = {e.id for e in exercises}
        missing_ids = set(exercise_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"动作不存在: {missing_ids}",
            )

    # 创建训练课
    session = WorkoutSession(
        **session_create.model_dump(exclude={"sets"}),
        user_id=current_user.id,
    )
    db.add(session)
    await db.flush()  # 获取 session.id

    # 创建训练组
    for set_data in session_create.sets:
        workout_set = WorkoutSet(
            **set_data.model_dump(),
            session_id=session.id,
        )
        db.add(workout_set)

    await db.flush()
    await db.refresh(session)

    # 重新查询以加载关联
    result = await db.execute(
        select(WorkoutSession)
        .options(selectinload(WorkoutSession.sets))
        .where(WorkoutSession.id == session.id)
    )
    session = result.scalar_one()

    return session


@router.get("/{session_id}", response_model=WorkoutSessionDetailResponse)
async def get_workout_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取单次训练详情"""
    result = await db.execute(
        select(WorkoutSession)
        .options(selectinload(WorkoutSession.sets))
        .where(WorkoutSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练记录不存在",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限访问此训练记录",
        )

    return session


@router.put("/{session_id}", response_model=WorkoutSessionResponse)
async def update_workout_session(
    session_id: int,
    session_update: WorkoutSessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新训练记录"""
    result = await db.execute(select(WorkoutSession).where(WorkoutSession.id == session_id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练记录不存在",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此训练记录",
        )

    # 更新字段
    update_data = session_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)

    await db.flush()
    await db.refresh(session)

    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除训练记录"""
    result = await db.execute(select(WorkoutSession).where(WorkoutSession.id == session_id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练记录不存在",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此训练记录",
        )

    await db.delete(session)


# ===== 训练组操作 =====

@router.post("/{session_id}/sets", response_model=WorkoutSetResponse, status_code=status.HTTP_201_CREATED)
async def add_workout_set(
    session_id: int,
    set_create: WorkoutSetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """向训练课添加训练组"""
    result = await db.execute(select(WorkoutSession).where(WorkoutSession.id == session_id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练记录不存在",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此训练记录",
        )

    # 验证动作存在
    result = await db.execute(select(Exercise).where(Exercise.id == set_create.exercise_id))
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="动作不存在",
        )

    workout_set = WorkoutSet(**set_create.model_dump(), session_id=session_id)
    db.add(workout_set)
    await db.flush()
    await db.refresh(workout_set)

    return workout_set


@router.put("/{session_id}/sets/{set_id}", response_model=WorkoutSetResponse)
async def update_workout_set(
    session_id: int,
    set_id: int,
    set_update: WorkoutSetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新训练组"""
    result = await db.execute(
        select(WorkoutSet)
        .join(WorkoutSession)
        .where(and_(WorkoutSet.id == set_id, WorkoutSet.session_id == session_id))
    )
    workout_set = result.scalar_one_or_none()

    if not workout_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练组不存在",
        )

    if workout_set.session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此训练组",
        )

    update_data = set_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workout_set, field, value)

    await db.flush()
    await db.refresh(workout_set)

    return workout_set


@router.delete("/{session_id}/sets/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_set(
    session_id: int,
    set_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除训练组"""
    result = await db.execute(
        select(WorkoutSet)
        .join(WorkoutSession)
        .where(and_(WorkoutSet.id == set_id, WorkoutSet.session_id == session_id))
    )
    workout_set = result.scalar_one_or_none()

    if not workout_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练组不存在",
        )

    if workout_set.session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此训练组",
        )

    await db.delete(workout_set)


# ===== 模板功能 =====

@router.post("/{session_id}/save-template", status_code=status.HTTP_201_CREATED)
async def save_as_template(
    session_id: int,
    template: WorkoutTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """将训练课保存为模板（更新 template_name 字段）"""
    result = await db.execute(select(WorkoutSession).where(WorkoutSession.id == session_id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练记录不存在",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限操作此训练记录",
        )

    session.template_name = template.template_name
    await db.flush()

    return {"message": "模板保存成功", "template_name": template.template_name}


@router.post("/from-template", response_model=WorkoutSessionDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_from_template(
    template_create: WorkoutFromTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """从模板创建训练课"""
    # 查找最近的同模板训练课
    result = await db.execute(
        select(WorkoutSession)
        .options(selectinload(WorkoutSession.sets))
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.template_name == template_create.template_name,
        ))
        .order_by(WorkoutSession.date.desc())
        .limit(1)
    )
    template_session = result.scalar_one_or_none()

    if not template_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模板不存在",
        )

    # 创建新训练课
    new_session = WorkoutSession(
        user_id=current_user.id,
        date=template_create.date,
        template_name=template_create.template_name,
    )
    db.add(new_session)
    await db.flush()

    # 复制训练组
    for old_set in template_session.sets:
        new_set = WorkoutSet(
            session_id=new_session.id,
            exercise_id=old_set.exercise_id,
            set_order=old_set.set_order,
            weight=old_set.weight,
            reps=old_set.reps,
            rpe=old_set.rpe,
            rest_seconds=old_set.rest_seconds,
            tempo=old_set.tempo,
            notes=old_set.notes,
        )
        db.add(new_set)

    await db.flush()

    # 重新查询以加载关联
    result = await db.execute(
        select(WorkoutSession)
        .options(selectinload(WorkoutSession.sets))
        .where(WorkoutSession.id == new_session.id)
    )
    new_session = result.scalar_one()

    return new_session


@router.get("/templates/list")
async def list_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取用户的训练模板列表"""
    result = await db.execute(
        select(WorkoutSession.template_name, func.count(WorkoutSession.id).label("usage_count"))
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.template_name.isnot(None),
        ))
        .group_by(WorkoutSession.template_name)
        .order_by(func.count(WorkoutSession.id).desc())
    )
    templates = result.all()

    return {
        "templates": [
            {"name": t.template_name, "usage_count": t.usage_count}
            for t in templates
        ]
    }
