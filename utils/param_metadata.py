# param_metadata.py (v6.0)
"""
参数默认值定义模块（v6.0）。

本模块仅提供必要的默认值字典，用于快速查找初始值。
为精简项目结构，此处省略详细元数据；如需更多说明请参考项目文档。
"""

param_info = {
    "ship_length": {"default": 85.0},
    "carry_per_meter": {"default": 10.0},
    "avg_trip_distance": {"default": 50.0},
    "economic_speed": {"default": 10.0},
    "turnaround_time": {"default": 4.0},
    "annual_hours": {"default": 2500.0},
    "crew_num": {"default": 5.0},
    "crew_avg_cost": {"default": 40000.0},
    "mgo_price": {"default": 0.6},
    "electricity_price": {"default": 0.27},
    "diesel_consumption_per_hour": {"default": 120.0},
    "electric_consumption_per_hour": {"default": 250.0},
    "battery_price": {"default": 500.0},
    "battery_capacity_kWh": {"default": 2000.0},
    "battery_cycle_life": {"default": 5000.0},
    "battery_replace_ratio_eu": {"default": 0.5},
    "battery_replace_ratio_cn": {"default": 0.5},
    "maintenance_cost_diesel": {"default": 20000.0},
    "maintenance_cost_electric": {"default": 15000.0},
    "port_fee": {"default": 20000.0},
    "overhaul_interval_years_diesel": {"default": 10},
    "overhaul_cost_per_event_diesel": {"default": 100000.0},
    "unit_income": {"default": 0.025},
    "insurance_discount": {"default": 5.0},
}


def get_param_help(key: str) -> str:
    """返回参数的帮助说明（占位函数）。实际说明请参考项目文档。"""
    return ""