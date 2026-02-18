"""
FitTracker Pro 测试数据生成脚本

为所有用户生成测试数据，包括：
- 训练记录 (workout_sessions)
- 训练组 (workout_sets)
- 估算1RM (estimated_1rms)
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from random import randint, choice, uniform

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.database import async_session_maker
from app.models.workout import WorkoutSession, WorkoutSet
from app.models.exercise import Exercise
from app.models.user import User
from app.models.analysis import Estimated1RM


async def generate_test_data():
    """生成测试数据"""
    async with async_session_maker() as db:
        # 获取所有用户和所有动作
        result = await db.execute(select(User))
        users = result.scalars().all()

        if not users:
            print("❌ 没有找到用户，请先创建用户")
            return

        result = await db.execute(select(Exercise))
        exercises = result.scalars().all()

        if not exercises:
            print("❌ 没有找到动作，请先初始化动作数据")
            return

        print(f"👤 找到 {len(users)} 个用户")
        print(f"💪 可用动作: {len(exercises)} 个\n")

        total_workouts = 0
        total_sets = 0
        total_onerm = 0

        # 为每个用户生成训练数据
        for user in users:
            print(f"👤 为用户 {user.nickname} (ID: {user.id}) 生成数据...")

            # 生成过去30天的训练记录
            today = datetime.now()
            workout_count = 0
            set_count = 0
            onerm_count = 0

            # 生成10次训练记录
            for i in range(10):
                workout_date = today - timedelta(days=randint(0, 30))

                # 创建训练session
                workout = WorkoutSession(
                    user_id=user.id,
                    date=workout_date,
                    notes=f"测试训练记录{i + 1}",
                    duration_min=randint(30, 90),
                    overall_rpe=randint(6, 9),
                    template_name=f"模板{choice(['胸部', '背部', '腿部', '肩部'])}"
                )
                db.add(workout)
                await db.flush()
                workout_count += 1

                # 为每次训练添加3-6个训练组
                num_sets = randint(3, 6)
                for j in range(num_sets):
                    exercise = choice(exercises)

                    # 生成合理的重量和次数
                    if exercise.equipment in ['barbell', 'dumbbell']:
                        weight = round(uniform(10, 100), 1)
                    elif exercise.equipment == 'machine':
                        weight = round(uniform(20, 150), 1)
                    else:  # bodyweight
                        weight = 0

                    reps = randint(8, 15)
                    rpe = round(uniform(6, 10), 1)
                    rest_time = randint(60, 180)

                    workout_set = WorkoutSet(
                        session_id=workout.id,
                        exercise_id=exercise.id,
                        weight=weight,
                        reps=reps,
                        rpe=int(rpe),
                        rest_seconds=rest_time,
                        set_order=j + 1
                    )
                    db.add(workout_set)
                    set_count += 1

                    # 为部分训练组生成1RM估算
                    if j % 2 == 0 and weight > 0:  # 50%的训练组
                        # 使用 Epley 公式估算1RM: weight * (1 + reps/30)
                        estimated_1rm = round(weight * (1 + reps / 30), 2)

                        onerm = Estimated1RM(
                            user_id=user.id,
                            exercise_id=exercise.id,
                            source_weight=weight,
                            source_reps=reps,
                            source_rpe=int(rpe),
                            estimated_1rm=estimated_1rm,
                            date=workout_date,
                            method="Epley"
                        )
                        db.add(onerm)
                        onerm_count += 1

                print(f"  ✅ 创建训练{i + 1}: {workout_date.strftime('%Y-%m-%d')} - {num_sets}组")

            total_workouts += workout_count
            total_sets += set_count
            total_onerm += onerm_count

            print(f"  📊 用户 {user.nickname} 完成: {workout_count}条训练, {set_count}组, {onerm_count}条1RM\n")

        await db.commit()

        print(f"\n🎉 所有用户测试数据生成完成！")
        print(f"   - 总训练记录: {total_workouts} 条")
        print(f"   - 总训练组: {total_sets} 条")
        print(f"   - 总1RM估算: {total_onerm} 条")


if __name__ == "__main__":
    print("🚀 开始生成测试数据...\n")
    asyncio.run(generate_test_data())
