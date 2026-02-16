"""
预置动作数据 seed 脚本
运行: python -m seeds.exercises
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker, init_db
from app.models.exercise import Exercise


# 预置动作数据
EXERCISES_DATA = [
    # ===== 胸部 (Chest) =====
    # 复合动作
    {"name": "平板杠铃卧推", "name_en": "Barbell Bench Press", "primary_muscle": "chest", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["triceps", "shoulders"]},
    {"name": "上斜杠铃卧推", "name_en": "Incline Barbell Bench Press", "primary_muscle": "chest", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["triceps", "shoulders"]},
    {"name": "下斜杠铃卧推", "name_en": "Decline Barbell Bench Press", "primary_muscle": "chest", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["triceps", "shoulders"]},
    {"name": "平板哑铃卧推", "name_en": "Dumbbell Bench Press", "primary_muscle": "chest", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["triceps", "shoulders"]},
    {"name": "上斜哑铃卧推", "name_en": "Incline Dumbbell Bench Press", "primary_muscle": "chest", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["triceps", "shoulders"]},
    {"name": "双杠臂屈伸", "name_en": "Dips", "primary_muscle": "chest", "category": "compound", "equipment": "bodyweight", "difficulty": 3, "secondary_muscles": ["triceps", "shoulders"]},
    {"name": "俯卧撑", "name_en": "Push-ups", "primary_muscle": "chest", "category": "compound", "equipment": "bodyweight", "difficulty": 1, "secondary_muscles": ["triceps", "shoulders"]},
    # 孤立动作
    {"name": "龙门架夹胸", "name_en": "Cable Crossover", "primary_muscle": "chest", "category": "isolation", "equipment": "cable", "difficulty": 2},
    {"name": "蝴蝶机夹胸", "name_en": "Pec Deck Fly", "primary_muscle": "chest", "category": "isolation", "equipment": "machine", "difficulty": 1},
    {"name": "哑铃飞鸟", "name_en": "Dumbbell Fly", "primary_muscle": "chest", "category": "isolation", "equipment": "dumbbell", "difficulty": 2},

    # ===== 背部 (Back) =====
    # 复合动作
    {"name": "硬拉", "name_en": "Deadlift", "primary_muscle": "back", "category": "compound", "equipment": "barbell", "difficulty": 4, "secondary_muscles": ["glutes", "hamstrings", "core"]},
    {"name": "杠铃划船", "name_en": "Barbell Row", "primary_muscle": "back", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["biceps", "shoulders"]},
    {"name": "哑铃划船", "name_en": "Dumbbell Row", "primary_muscle": "back", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["biceps"]},
    {"name": "引体向上", "name_en": "Pull-ups", "primary_muscle": "back", "category": "compound", "equipment": "bodyweight", "difficulty": 3, "secondary_muscles": ["biceps", "shoulders"]},
    {"name": "反握引体向上", "name_en": "Chin-ups", "primary_muscle": "back", "category": "compound", "equipment": "bodyweight", "difficulty": 2, "secondary_muscles": ["biceps"]},
    {"name": "坐姿划船", "name_en": "Seated Cable Row", "primary_muscle": "back", "category": "compound", "equipment": "cable", "difficulty": 2, "secondary_muscles": ["biceps"]},
    {"name": "高位下拉", "name_en": "Lat Pulldown", "primary_muscle": "back", "category": "compound", "equipment": "cable", "difficulty": 2, "secondary_muscles": ["biceps"]},
    {"name": "T杠划船", "name_en": "T-Bar Row", "primary_muscle": "back", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["biceps"]},
    # 孤立动作
    {"name": "直臂下压", "name_en": "Straight Arm Pulldown", "primary_muscle": "back", "category": "isolation", "equipment": "cable", "difficulty": 2},
    {"name": "绳索面拉", "name_en": "Face Pull", "primary_muscle": "back", "category": "isolation", "equipment": "cable", "difficulty": 2, "secondary_muscles": ["shoulders"]},

    # ===== 股四头肌 (Quads) =====
    {"name": "杠铃深蹲", "name_en": "Barbell Back Squat", "primary_muscle": "quads", "category": "compound", "equipment": "barbell", "difficulty": 4, "secondary_muscles": ["glutes", "hamstrings", "core"]},
    {"name": "前蹲", "name_en": "Front Squat", "primary_muscle": "quads", "category": "compound", "equipment": "barbell", "difficulty": 4, "secondary_muscles": ["glutes", "core"]},
    {"name": "腿举", "name_en": "Leg Press", "primary_muscle": "quads", "category": "compound", "equipment": "machine", "difficulty": 2, "secondary_muscles": ["glutes", "hamstrings"]},
    {"name": "哈克深蹲", "name_en": "Hack Squat", "primary_muscle": "quads", "category": "compound", "equipment": "machine", "difficulty": 2, "secondary_muscles": ["glutes"]},
    {"name": "箭步蹲", "name_en": "Lunges", "primary_muscle": "quads", "category": "compound", "equipment": "bodyweight", "difficulty": 2, "secondary_muscles": ["glutes", "hamstrings"]},
    {"name": "腿屈伸", "name_en": "Leg Extension", "primary_muscle": "quads", "category": "isolation", "equipment": "machine", "difficulty": 1},
    {"name": "保加利亚分腿蹲", "name_en": "Bulgarian Split Squat", "primary_muscle": "quads", "category": "compound", "equipment": "bodyweight", "difficulty": 3, "secondary_muscles": ["glutes", "hamstrings"]},

    # ===== 股二头肌 (Hamstrings) =====
    {"name": "罗马尼亚硬拉", "name_en": "Romanian Deadlift", "primary_muscle": "hamstrings", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["glutes", "back"]},
    {"name": "直腿硬拉", "name_en": "Stiff-Leg Deadlift", "primary_muscle": "hamstrings", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["glutes"]},
    {"name": "腿弯举", "name_en": "Leg Curl", "primary_muscle": "hamstrings", "category": "isolation", "equipment": "machine", "difficulty": 1},
    {"name": "哑铃罗马尼亚硬拉", "name_en": "Dumbbell RDL", "primary_muscle": "hamstrings", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["glutes"]},

    # ===== 臀部 (Glutes) =====
    {"name": "臀推", "name_en": "Hip Thrust", "primary_muscle": "glutes", "category": "compound", "equipment": "barbell", "difficulty": 2, "secondary_muscles": ["hamstrings"]},
    {"name": "臀桥", "name_en": "Glute Bridge", "primary_muscle": "glutes", "category": "compound", "equipment": "bodyweight", "difficulty": 1, "secondary_muscles": ["hamstrings"]},
    {"name": "臀 kickback", "name_en": "Cable Kickback", "primary_muscle": "glutes", "category": "isolation", "equipment": "cable", "difficulty": 1},
    {"name": "蚌式开合", "name_en": "Clamshell", "primary_muscle": "glutes", "category": "isolation", "equipment": "band", "difficulty": 1},

    # ===== 肩部 (Shoulders) =====
    {"name": "杠铃推举", "name_en": "Barbell Overhead Press", "primary_muscle": "shoulders", "category": "compound", "equipment": "barbell", "difficulty": 3, "secondary_muscles": ["triceps", "core"]},
    {"name": "哑铃推举", "name_en": "Dumbbell Shoulder Press", "primary_muscle": "shoulders", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["triceps"]},
    {"name": "阿诺德推举", "name_en": "Arnold Press", "primary_muscle": "shoulders", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["triceps"]},
    {"name": "哑铃侧平举", "name_en": "Lateral Raise", "primary_muscle": "shoulders", "category": "isolation", "equipment": "dumbbell", "difficulty": 1},
    {"name": "哑铃前平举", "name_en": "Front Raise", "primary_muscle": "shoulders", "category": "isolation", "equipment": "dumbbell", "difficulty": 1},
    {"name": "俯身哑铃飞鸟", "name_en": "Rear Delt Fly", "primary_muscle": "shoulders", "category": "isolation", "equipment": "dumbbell", "difficulty": 2},
    {"name": "直立划船", "name_en": "Upright Row", "primary_muscle": "shoulders", "category": "compound", "equipment": "barbell", "difficulty": 2, "secondary_muscles": ["biceps"]},

    # ===== 肱二头肌 (Biceps) =====
    {"name": "杠铃弯举", "name_en": "Barbell Curl", "primary_muscle": "biceps", "category": "isolation", "equipment": "barbell", "difficulty": 1},
    {"name": "哑铃弯举", "name_en": "Dumbbell Curl", "primary_muscle": "biceps", "category": "isolation", "equipment": "dumbbell", "difficulty": 1},
    {"name": "锤式弯举", "name_en": "Hammer Curl", "primary_muscle": "biceps", "category": "isolation", "equipment": "dumbbell", "difficulty": 1, "secondary_muscles": ["forearms"]},
    {"name": "集中弯举", "name_en": "Concentration Curl", "primary_muscle": "biceps", "category": "isolation", "equipment": "dumbbell", "difficulty": 1},
    {"name": "牧师椅弯举", "name_en": "Preacher Curl", "primary_muscle": "biceps", "category": "isolation", "equipment": "barbell", "difficulty": 1},
    {"name": "绳索弯举", "name_en": "Cable Curl", "primary_muscle": "biceps", "category": "isolation", "equipment": "cable", "difficulty": 1},

    # ===== 肱三头肌 (Triceps) =====
    {"name": "绳索下压", "name_en": "Tricep Pushdown", "primary_muscle": "triceps", "category": "isolation", "equipment": "cable", "difficulty": 1},
    {"name": "仰卧臂屈伸", "name_en": "Skull Crushers", "primary_muscle": "triceps", "category": "isolation", "equipment": "barbell", "difficulty": 2},
    {"name": "哑铃颈后臂屈伸", "name_en": "Overhead Dumbbell Extension", "primary_muscle": "triceps", "category": "isolation", "equipment": "dumbbell", "difficulty": 1},
    {"name": "窄距卧推", "name_en": "Close Grip Bench Press", "primary_muscle": "triceps", "category": "compound", "equipment": "barbell", "difficulty": 2, "secondary_muscles": ["chest", "shoulders"]},
    {"name": "双杠臂屈伸(三头)", "name_en": "Tricep Dips", "primary_muscle": "triceps", "category": "compound", "equipment": "bodyweight", "difficulty": 2, "secondary_muscles": ["chest", "shoulders"]},

    # ===== 前臂 (Forearms) =====
    {"name": "腕弯举", "name_en": "Wrist Curl", "primary_muscle": "forearms", "category": "isolation", "equipment": "barbell", "difficulty": 1},
    {"name": "反握腕弯举", "name_en": "Reverse Wrist Curl", "primary_muscle": "forearms", "category": "isolation", "equipment": "barbell", "difficulty": 1},
    {"name": "农夫行走", "name_en": "Farmer's Walk", "primary_muscle": "forearms", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["core", "shoulders"]},

    # ===== 小腿 (Calves) =====
    {"name": "站姿提踵", "name_en": "Standing Calf Raise", "primary_muscle": "calves", "category": "isolation", "equipment": "machine", "difficulty": 1},
    {"name": "坐姿提踵", "name_en": "Seated Calf Raise", "primary_muscle": "calves", "category": "isolation", "equipment": "machine", "difficulty": 1},
    {"name": "驴式提踵", "name_en": "Donkey Calf Raise", "primary_muscle": "calves", "category": "isolation", "equipment": "bodyweight", "difficulty": 1},

    # ===== 核心 (Core) =====
    {"name": "平板支撑", "name_en": "Plank", "primary_muscle": "core", "category": "isolation", "equipment": "bodyweight", "difficulty": 1},
    {"name": "卷腹", "name_en": "Crunch", "primary_muscle": "core", "category": "isolation", "equipment": "bodyweight", "difficulty": 1},
    {"name": "仰卧起坐", "name_en": "Sit-up", "primary_muscle": "core", "category": "compound", "equipment": "bodyweight", "difficulty": 1},
    {"name": "悬垂举腿", "name_en": "Hanging Leg Raise", "primary_muscle": "core", "category": "compound", "equipment": "bodyweight", "difficulty": 3},
    {"name": "俄罗斯转体", "name_en": "Russian Twist", "primary_muscle": "core", "category": "isolation", "equipment": "bodyweight", "difficulty": 1},
    {"name": "死虫", "name_en": "Dead Bug", "primary_muscle": "core", "category": "isolation", "equipment": "bodyweight", "difficulty": 1},
    {"name": "健腹轮", "name_en": "Ab Wheel Rollout", "primary_muscle": "core", "category": "compound", "equipment": "other", "difficulty": 4},
    {"name": "绳索卷腹", "name_en": "Cable Crunch", "primary_muscle": "core", "category": "isolation", "equipment": "cable", "difficulty": 1},

    # ===== 全身 (Full Body) =====
    {"name": "高脚杯深蹲", "name_en": "Goblet Squat", "primary_muscle": "full_body", "category": "compound", "equipment": "dumbbell", "difficulty": 2, "secondary_muscles": ["quads", "glutes", "core"]},
    {"name": "壶铃摇摆", "name_en": "Kettlebell Swing", "primary_muscle": "full_body", "category": "compound", "equipment": "kettlebell", "difficulty": 3, "secondary_muscles": ["glutes", "hamstrings", "shoulders"]},
    {"name": "波比跳", "name_en": "Burpee", "primary_muscle": "full_body", "category": "compound", "equipment": "bodyweight", "difficulty": 2},
    {"name": "土耳其起身", "name_en": "Turkish Get-Up", "primary_muscle": "full_body", "category": "compound", "equipment": "kettlebell", "difficulty": 5},
    {"name": "抓举", "name_en": "Snatch", "primary_muscle": "full_body", "category": "compound", "equipment": "barbell", "difficulty": 5},
    {"name": "挺举", "name_en": "Clean and Jerk", "primary_muscle": "full_body", "category": "compound", "equipment": "barbell", "difficulty": 5},
]


async def seed_exercises():
    """填充预置动作数据"""
    async with async_session_maker() as session:
        # 检查是否已有数据
        from sqlalchemy import select, func
        result = await session.execute(select(func.count()).select_from(Exercise))
        count = result.scalar()

        if count > 0:
            print(f"动作库已有 {count} 条数据，跳过填充")
            return

        # 插入数据
        for data in EXERCISES_DATA:
            exercise = Exercise(**data, is_custom=False)
            session.add(exercise)

        await session.commit()
        print(f"成功填充 {len(EXERCISES_DATA)} 个预置动作")


async def main():
    """主函数"""
    print("初始化数据库...")
    await init_db()

    print("开始填充动作库数据...")
    await seed_exercises()

    print("完成！")


if __name__ == "__main__":
    asyncio.run(main())
