# cost_calculations.py (v6.0)
"""
成本计算模块（v6.0）。

根据输入参数计算初期建造成本、年度运营成本、保险费、
周期性大修与换电费用、现金流与回本周期以及碳排放。
所有计算聚合在一个函数中，返回统一的结果字典。
"""

from typing import Dict, Any, List, Tuple
from utils.helpers import get_jump_years


def calculate_costs(params: Dict[str, Any]) -> Dict[str, Any]:
    """根据输入参数计算成本与现金流。"""
    years: List[int] = list(range(26))

    # 年收入估算
    travel_time = params['avg_trip_distance'] * 2.0 / params['economic_speed'] if params['economic_speed'] else 0
    trip_time = travel_time + params['turnaround_time']
    trips_per_year = params['annual_hours'] / trip_time if trip_time > 0 else 0
    annual_volume = trips_per_year * params['ship_length'] * params['carry_per_meter']
    auto_income = params['unit_income'] * annual_volume * params['avg_trip_distance']
    annual_income = params['annual_income'] if params.get('annual_income') else auto_income

    # 初期建造成本（万欧）转换为欧元并扣除补贴
    raw_diesel = sum(params['柴油船']) * 1e4
    raw_elec_eu = sum(params['电动船(EU)']) * 1e4 + params['battery_capacity_kWh'] * params['battery_price']
    raw_elec_cn = sum(params['电动船(CN)']) * 1e4 + params['battery_capacity_kWh'] * params['battery_price'] * 0.7
    initial_costs = {
        "STAGE V 柴油船 (EU)": raw_diesel * (1 - params['subsidy_ratio_stage_v']),
        "电动船 (EU)": raw_elec_eu * (1 - params['subsidy_ratio_electric_eu']),
        "电动船 (CN)": raw_elec_cn * (1 - params['subsidy_ratio_electric_cn']),
    }

    # 年度运营成本（含保险）
    diesel_fuel = params['diesel_consumption_per_hour'] * params['annual_hours'] * params['mgo_price']
    elec_energy = params['electric_consumption_per_hour'] * params['annual_hours'] * params['electricity_price']
    diesel_maint = params['maintenance_cost_diesel']
    elec_maint = params['maintenance_cost_electric']
    crew_cost = params['crew_num'] * params['crew_avg_cost']
    hull_rate = params['insurance_rate'] / 100.0
    disc = (params['insurance_discount'] / 100.0) if params['smart_equipment_selected'] else 0.0
    diesel_ins = raw_diesel * hull_rate
    elec_ins_eu = raw_elec_eu * hull_rate * (1 - disc)
    elec_ins_cn = raw_elec_cn * hull_rate * (1 - disc)
    port_fee = params.get('port_fee', 0)
    annual_costs = {
        "STAGE V 柴油船 (EU)": diesel_fuel + crew_cost + diesel_maint + port_fee + diesel_ins,
        "电动船 (EU)": elec_energy + crew_cost + elec_maint + elec_ins_eu,
        "电动船 (CN)": elec_energy + crew_cost + elec_maint + elec_ins_cn,
    }
    insurance_costs = {
        "STAGE V 柴油船 (EU)": diesel_ins,
        "电动船 (EU)": elec_ins_eu,
        "电动船 (CN)": elec_ins_cn,
    }

    # 周期性大修与换电周期
    cycle_ratio = (params['annual_hours'] * params['electric_consumption_per_hour'] / params['battery_capacity_kWh']) if params['battery_capacity_kWh'] else 1
    battery_cycle_yr = max(1.0, params['battery_cycle_life'] / cycle_ratio)
    overhaul_yr = max(1.0, params['overhaul_interval_years_diesel'])
    jumps_eu = set(get_jump_years(battery_cycle_yr, years[-1]))
    jumps_cn = set(jumps_eu)
    jumps_ov = set(get_jump_years(overhaul_yr, years[-1]))

    cumulative_costs: Dict[str, List[float]] = {}
    cashflow: Dict[str, List[float]] = {}
    cum_cashflow: Dict[str, List[float]] = {}
    payback: Dict[str, int] = {}

    for ship, init in initial_costs.items():
        cum_cost = init
        acc_cash = -init
        cost_list: List[float] = []
        cf_list: List[float] = []
        cumcf_list: List[float] = []
        for y in years:
            extra = 0
            if y > 0:
                cum_cost += annual_costs[ship]
                if ship == "STAGE V 柴油船 (EU)" and y in jumps_ov:
                    extra = params['overhaul_cost_per_event_diesel']
                if ship == "电动船 (EU)" and y in jumps_eu:
                    extra = params['battery_replace_cost_eu']
                if ship == "电动船 (CN)" and y in jumps_cn:
                    extra = params['battery_replace_cost_cn']
                cum_cost += extra
            cost_list.append(cum_cost)
            op_cost = annual_costs[ship] + (extra if y > 0 else 0)
            net_cf = (annual_income - op_cost) if y > 0 else -init
            cf_list.append(net_cf)
            acc_cash += net_cf
            cumcf_list.append(acc_cash)
        cumulative_costs[ship] = cost_list
        cashflow[ship] = cf_list
        cum_cashflow[ship] = cumcf_list
        payback[ship] = next((i for i, v in enumerate(cumcf_list) if v >= 0), None)

    # 年度碳排放 (吨 CO2)
    diesel_emission_factor = 3.2  # kg CO2/L
    elec_emission_factor = 0.35  # kg CO2/kWh
    annual_emissions = {
        "STAGE V 柴油船 (EU)": diesel_fuel * diesel_emission_factor / 1000.0,
        "电动船 (EU)": elec_energy * elec_emission_factor / 1000.0,
        "电动船 (CN)": elec_energy * elec_emission_factor / 1000.0,
    }

    return {
        'initial_costs': initial_costs,
        'annual_costs': annual_costs,
        'insurance_costs': insurance_costs,
        'annual_emissions': annual_emissions,
        'cumulative_costs': cumulative_costs,
        'cashflow': cashflow,
        'cum_cashflow': cum_cashflow,
        'payback_year': payback,
        'years': years,
    }