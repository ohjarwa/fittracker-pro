from datetime import date, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case

from app.database import get_db
from app.models.user import User
from app.models.workout import WorkoutSession, WorkoutSet
from app.models.exercise import Exercise
from app.models.analysis import Estimated1RM
from app.schemas.analysis import (
    OneRMTrendResponse,
    OneRMTrendPoint,
    OneRMCalculateRequest,
    OneRMCalculateResponse,
    VolumeStatsResponse,
    VolumeStatsPoint,
    MuscleBalanceResponse,
    MuscleVolumePoint,
    ProgressReportResponse,
    ExerciseProgress,
)
from app.services.rm_calculator import calculate_1rm, calculate_volume_load
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("/1rm/calculate", response_model=OneRMCalculateResponse)
async def calculate_1rm_endpoint(
    request: OneRMCalculateRequest,
    current_user: User = Depends(get_current_user),
):
    """计算单次训练的 1RM 估算值"""
    result = calculate_1rm(request.weight, request.reps, request.rpe)
    return OneRMCalculateResponse(
        estimated_1rm=result.estimated_1rm,
        effective_reps=result.effective_reps,
        method_weights=result.method_weights,
        confidence=result.confidence,
    )


@router.get("/1rm/{exercise_id}", response_model=OneRMTrendResponse)
async def get_1rm_trend(
    exercise_id: int,
    days: int = Query(90, ge=7, le=365, description="查询天数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取指定动作的 1RM 趋势"""
    # 验证动作存在
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="动作不存在")

    # 查询该动作的训练记录
    start_date = date.today() - timedelta(days=days)
    result = await db.execute(
        select(WorkoutSet, WorkoutSession.date)
        .join(WorkoutSession)
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSet.exercise_id == exercise_id,
            WorkoutSession.date >= start_date,
        ))
        .order_by(WorkoutSession.date)
    )
    sets_with_dates = result.all()

    # 计算 1RM 趋势
    trend_points = []
    for workout_set, session_date in sets_with_dates:
        calc_result = calculate_1rm(
            workout_set.weight,
            workout_set.reps,
            workout_set.rpe,
        )
        trend_points.append(OneRMTrendPoint(
            date=session_date,
            estimated_1rm=calc_result.estimated_1rm,
            source_weight=workout_set.weight,
            source_reps=workout_set.reps,
            source_rpe=workout_set.rpe,
            confidence=calc_result.confidence,
        ))

    # 取最高 1RM 作为当前值
    current_1rm = None
    previous_1rm = None
    change_percentage = None

    if trend_points:
        # 按 1RM 降序取最高
        sorted_points = sorted(trend_points, key=lambda x: x.estimated_1rm, reverse=True)
        current_1rm = sorted_points[0].estimated_1rm

        # 计算变化（最近30天 vs 之前）
        recent_cutoff = date.today() - timedelta(days=30)
        recent_points = [p for p in trend_points if p.date >= recent_cutoff]
        older_points = [p for p in trend_points if p.date < recent_cutoff]

        if recent_points and older_points:
            recent_max = max(p.estimated_1rm for p in recent_points)
            older_max = max(p.estimated_1rm for p in older_points)
            previous_1rm = older_max
            if older_max > 0:
                change_percentage = round((recent_max - older_max) / older_max * 100, 1)

    return OneRMTrendResponse(
        exercise_id=exercise_id,
        exercise_name=exercise.name,
        current_1rm=current_1rm,
        previous_1rm=previous_1rm,
        change_percentage=change_percentage,
        trend=trend_points,
    )


@router.get("/volume", response_model=VolumeStatsResponse)
async def get_volume_stats(
    period: str = Query("week", regex="^(week|month)$", description="统计周期"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取容量统计"""
    # 确定日期范围
    end_date = date.today()
    if start_date is None:
        if period == "week":
            start_date = end_date - timedelta(days=7)
        else:
            start_date = end_date - timedelta(days=30)

    # 查询训练课
    result = await db.execute(
        select(WorkoutSession)
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.date >= start_date,
            WorkoutSession.date <= end_date,
        ))
        .order_by(WorkoutSession.date)
    )
    sessions = result.scalars().all()

    # 统计每日数据
    daily_stats = {}
    total_sets = 0
    total_reps = 0
    total_volume = 0

    for session in sessions:
        # 获取该训练课的所有组
        sets_result = await db.execute(
            select(WorkoutSet).where(WorkoutSet.session_id == session.id)
        )
        sets = sets_result.scalars().all()

        day_sets = len(sets)
        day_reps = sum(s.reps for s in sets)
        day_volume = sum(s.weight * s.reps for s in sets)
        exercises_count = len(set(s.exercise_id for s in sets))

        daily_stats[session.date] = VolumeStatsPoint(
            date=session.date,
            total_sets=day_sets,
            total_reps=day_reps,
            total_volume=day_volume,
            exercises_count=exercises_count,
        )

        total_sets += day_sets
        total_reps += day_reps
        total_volume += day_volume

    return VolumeStatsResponse(
        period=period,
        start_date=start_date,
        end_date=end_date,
        total_sessions=len(sessions),
        total_sets=total_sets,
        total_reps=total_reps,
        total_volume=round(total_volume, 2),
        daily_stats=list(daily_stats.values()),
    )


@router.get("/muscle-balance", response_model=MuscleBalanceResponse)
async def get_muscle_balance(
    days: int = Query(30, ge=7, le=90, description="查询天数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取肌群平衡分析"""
    start_date = date.today() - timedelta(days=days)

    # 查询各肌群的训练组数
    result = await db.execute(
        select(
            Exercise.primary_muscle,
            func.count(WorkoutSet.id).label("total_sets"),
            func.sum(WorkoutSet.weight * WorkoutSet.reps).label("total_volume"),
        )
        .select_from(WorkoutSet)
        .join(WorkoutSession)
        .join(Exercise, WorkoutSet.exercise_id == Exercise.id)
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.date >= start_date,
        ))
        .group_by(Exercise.primary_muscle)
    )
    muscle_stats = result.all()

    # 计算总容量
    total_volume = sum(float(s.total_volume or 0) for s in muscle_stats)

    # 构建响应
    muscle_volumes = []
    for stat in muscle_stats:
        volume = float(stat.total_volume or 0)
        percentage = round(volume / total_volume * 100, 1) if total_volume > 0 else 0
        muscle_volumes.append(MuscleVolumePoint(
            muscle_group=stat.primary_muscle,
            total_sets=stat.total_sets,
            total_volume=round(volume, 2),
            percentage=percentage,
        ))

    # 按容量排序
    muscle_volumes.sort(key=lambda x: x.total_volume, reverse=True)

    # 生成建议
    recommendations = []
    trained_muscles = {m.muscle_group for m in muscle_volumes}

    # 检查未训练的肌群
    all_muscles = {"chest", "back", "shoulders", "biceps", "triceps", "quads", "hamstrings", "glutes", "calves", "core"}
    untrained = all_muscles - trained_muscles
    if untrained:
        recommendations.append(f"建议增加以下肌群的训练: {', '.join(untrained)}")

    # 检查不平衡
    if muscle_volumes:
        top_muscle = muscle_volumes[0]
        if top_muscle.percentage > 40:
            recommendations.append(f"{top_muscle.muscle_group} 训练占比过高 ({top_muscle.percentage}%)，建议平衡其他肌群")

    if not recommendations:
        recommendations.append("训练分布良好，继续保持！")

    return MuscleBalanceResponse(
        period_start=start_date,
        period_end=date.today(),
        muscle_volumes=muscle_volumes,
        recommendations=recommendations,
    )


@router.get("/progress-report", response_model=ProgressReportResponse)
async def get_progress_report(
    days: int = Query(90, ge=30, le=365, description="查询天数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取综合进步报告"""
    start_date = date.today() - timedelta(days=days)

    # 查询训练课总数和总容量
    result = await db.execute(
        select(
            func.count(WorkoutSession.id).label("total_sessions"),
        )
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.date >= start_date,
        ))
    )
    session_stats = result.one()

    # 查询总容量
    result = await db.execute(
        select(func.sum(WorkoutSet.weight * WorkoutSet.reps))
        .join(WorkoutSession)
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.date >= start_date,
        ))
    )
    total_volume = result.scalar() or 0

    # 获取各动作的进步情况
    result = await db.execute(
        select(Exercise.id, Exercise.name)
        .join(WorkoutSet)
        .join(WorkoutSession)
        .where(and_(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.date >= start_date,
        ))
        .distinct()
    )
    exercises = result.all()

    exercises_progress = []
    improving_count = 0
    plateau_count = 0

    for exercise_id, exercise_name in exercises:
        # 获取该动作的趋势
        result = await db.execute(
            select(WorkoutSet, WorkoutSession.date)
            .join(WorkoutSession)
            .where(and_(
                WorkoutSession.user_id == current_user.id,
                WorkoutSet.exercise_id == exercise_id,
                WorkoutSession.date >= start_date,
            ))
            .order_by(WorkoutSession.date)
        )
        sets_with_dates = result.all()

        if not sets_with_dates:
            continue

        # 计算各时期的 1RM
        cutoff_date = date.today() - timedelta(days=days // 2)
        early_points = [(s, d) for s, d in sets_with_dates if d < cutoff_date]
        late_points = [(s, d) for s, d in sets_with_dates if d >= cutoff_date]

        starting_1rm = None
        current_1rm = None
        progress_percentage = None
        trend = "plateau"

        if early_points:
            early_1rms = [calculate_1rm(s.weight, s.reps, s.rpe).estimated_1rm for s, d in early_points]
            starting_1rm = max(early_1rms)

        if late_points:
            late_1rms = [calculate_1rm(s.weight, s.reps, s.rpe).estimated_1rm for s, d in late_points]
            current_1rm = max(late_1rms)

        if starting_1rm and current_1rm:
            progress_percentage = round((current_1rm - starting_1rm) / starting_1rm * 100, 1)

            if progress_percentage > 5:
                trend = "improving"
                improving_count += 1
            elif progress_percentage < -5:
                trend = "declining"
            else:
                trend = "plateau"
                plateau_count += 1

        exercises_progress.append(ExerciseProgress(
            exercise_id=exercise_id,
            exercise_name=exercise_name,
            starting_1rm=starting_1rm,
            current_1rm=current_1rm,
            progress_percentage=progress_percentage,
            trend=trend,
        ))

    # 生成总结
    if improving_count > len(exercises_progress) * 0.7:
        summary = "训练效果显著，大部分动作都在进步！"
    elif improving_count > len(exercises_progress) * 0.3:
        summary = "训练进展稳定，继续保持！"
    elif plateau_count > len(exercises_progress) * 0.7:
        summary = "可能进入平台期，建议调整训练计划。"
    else:
        summary = "建议检查训练强度和恢复情况。"

    return ProgressReportResponse(
        period_start=start_date,
        period_end=date.today(),
        total_sessions=session_stats.total_sessions or 0,
        total_volume=round(float(total_volume), 2),
        exercises_progress=exercises_progress,
        summary=summary,
    )
