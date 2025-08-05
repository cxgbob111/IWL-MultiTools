# helpers.py (v6.0)
"""通用辅助函数模块（v6.0）。

提供跳年计算等简单工具函数，供成本计算和可视化模块引用。
"""

from typing import List


def get_jump_years(cycle: float, last_year: int) -> List[int]:
    """根据周期长度计算跳年列表。例如电池更换或大修周期。

    Args:
        cycle: 周期长度（年）。
        last_year: 最后一年。

    Returns:
        列表，包含所有不超过 last_year 的整数年份。"""
    jumps = []
    if cycle <= 0:
        return jumps
    k = 1
    while True:
        y = int(round(k * cycle))
        if 0 < y <= last_year:
            jumps.append(y)
            k += 1
        else:
            break
    return jumps