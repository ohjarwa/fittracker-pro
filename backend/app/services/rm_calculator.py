"""
1RM 推算引擎
采用多公式加权 + RPE 修正策略
"""
from typing import Optional, Dict, List, Union
from dataclasses import dataclass


@dataclass
class OneRMResult:
    """1RM 计算结果"""
    estimated_1rm: float
    effective_reps: int
    method_weights: Dict[str, float]
    confidence: float


# RPE 映射表：RPE -> 还能做的次数
RPE_TO_REPS_IN_TANK = {
    10: 0,   # 力竭
    9.5: 0.5,
    9: 1,
    8.5: 1.5,
    8: 2,
    7.5: 2.5,
    7: 3,
    6.5: 3.5,
    6: 4,
    5.5: 4.5,
    5: 5,
}


def calculate_effective_reps(reps: int, rpe: Union[int, float]) -> int:
    """
    RPE 修正实际次数

    示例: 100kg × 5reps @ RPE 8 → 有效次数 = 5 + 2 = 7

    Args:
        reps: 实际完成的次数
        rpe: 主观疲劳度评分 (1-10)

    Returns:
        修正后的有效次数
    """
    # 处理 RPE 边界
    rpe = max(5, min(10, rpe))
    reps_in_tank = RPE_TO_REPS_IN_TANK.get(rpe, 0)
    return reps + reps_in_tank


def epley_formula(weight: float, reps: int) -> float:
    """
    Epley 公式
    适用范围: 中等次数 (5-10)
    1RM = weight × (1 + reps / 30)
    """
    return weight * (1 + reps / 30)


def brzycki_formula(weight: float, reps: int) -> float:
    """
    Brzycki 公式
    适用范围: 低次数 (1-6)
    1RM = weight × 36 / (37 - reps)
    """
    if reps >= 37:
        return weight * reps  # 防止除零
    return weight * 36 / (37 - reps)


def lombardi_formula(weight: float, reps: int) -> float:
    """
    Lombardi 公式
    适用范围: 高次数 (10+)
    1RM = weight × reps^0.10
    """
    return weight * (reps ** 0.10)


def oconner_formula(weight: float, reps: int) -> float:
    """
    O'Conner 公式
    适用范围: 通用
    1RM = weight × (1 + 0.025 × reps)
    """
    return weight * (1 + 0.025 * reps)


def get_method_weights(reps: int) -> Dict[str, float]:
    """
    根据次数范围动态调整各公式权重

    Args:
        reps: 有效次数

    Returns:
        各公式的权重字典
    """
    if reps <= 3:
        # 极低次数：主要依赖 Brzycki
        return {
            "epley": 0.15,
            "brzycki": 0.50,
            "lombardi": 0.10,
            "oconner": 0.25,
        }
    elif reps <= 6:
        # 低次数
        return {
            "epley": 0.25,
            "brzycki": 0.40,
            "lombardi": 0.10,
            "oconner": 0.25,
        }
    elif reps <= 10:
        # 中等次数
        return {
            "epley": 0.35,
            "brzycki": 0.35,
            "lombardi": 0.15,
            "oconner": 0.15,
        }
    elif reps <= 15:
        # 高次数
        return {
            "epley": 0.25,
            "brzycki": 0.20,
            "lombardi": 0.35,
            "oconner": 0.20,
        }
    else:
        # 极高次数
        return {
            "epley": 0.15,
            "brzycki": 0.10,
            "lombardi": 0.50,
            "oconner": 0.25,
        }


def calculate_1rm(
    weight: float,
    reps: int,
    rpe: Optional[Union[int, float]] = None,
) -> OneRMResult:
    """
    计算估算 1RM

    Args:
        weight: 训练重量 (kg)
        reps: 完成次数
        rpe: 主观疲劳度 (可选，默认为 10 表示力竭)

    Returns:
        OneRMResult 包含估算值、有效次数、方法权重、置信度
    """
    # 默认 RPE 为 10（力竭）
    if rpe is None:
        rpe = 10

    # RPE 修正有效次数
    effective_reps = calculate_effective_reps(reps, rpe)

    # 获取权重
    weights = get_method_weights(effective_reps)

    # 计算各公式结果
    results = {
        "epley": epley_formula(weight, effective_reps),
        "brzycki": brzycki_formula(weight, effective_reps),
        "lombardi": lombardi_formula(weight, effective_reps),
        "oconner": oconner_formula(weight, effective_reps),
    }

    # 加权平均
    estimated_1rm = sum(results[method] * weights[method] for method in weights)

    # 计算置信度
    # 基于次数范围：1-5 次最准确，次数越多误差越大
    if effective_reps <= 5:
        confidence = 0.95
    elif effective_reps <= 8:
        confidence = 0.90
    elif effective_reps <= 12:
        confidence = 0.85
    elif effective_reps <= 15:
        confidence = 0.80
    else:
        confidence = 0.75

    # 如果有 RPE 且非 10，略微降低置信度（主观评分有误差）
    if rpe != 10:
        confidence *= 0.95

    return OneRMResult(
        estimated_1rm=round(estimated_1rm, 2),
        effective_reps=effective_reps,
        method_weights=weights,
        confidence=round(confidence, 2),
    )


def calculate_volume_load(sets: List[Dict]) -> float:
    """
    计算训练容量负荷 (Volume Load)
    Volume Load = Σ(weight × reps)

    Args:
        sets: 训练组列表，每组包含 weight 和 reps

    Returns:
        总容量负荷
    """
    return sum(s.get("weight", 0) * s.get("reps", 0) for s in sets)


def calculate_relative_intensity(weight: float, estimated_1rm: float) -> float:
    """
    计算相对强度 (%1RM)

    Args:
        weight: 实际重量
        estimated_1rm: 估算 1RM

    Returns:
        相对强度百分比
    """
    if estimated_1rm <= 0:
        return 0
    return round((weight / estimated_1rm) * 100, 1)
