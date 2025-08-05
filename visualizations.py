# visualizations.py (v6.0)
"""可视化模块（v6.0）：成本对比曲线、运营占比、ROI与碳排放。"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from utils.helpers import get_jump_years

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']; plt.rcParams['axes.unicode_minus'] = False


def show_cost_charts(costs, params) -> None:
    st.subheader("📈 模块 M2 - 成本累计与对比分析")
    labels = list(costs['cumulative_costs'])
    checks = [params.get('show_stage_v', True), params.get('show_electric_eu', True), params.get('show_electric_cn', True)]
    colors = ['#636EFA', '#00CC96', '#EF553B']
    years = costs['years']
    fig = go.Figure()
    for idx, (label, check) in enumerate(zip(labels, checks)):
        if not check:
            continue
        y_data = costs['cumulative_costs'][label]
        fig.add_trace(go.Scatter(x=years, y=[v/1e4 for v in y_data], mode='lines+markers', name=label, line=dict(color=colors[idx])))
        # 标注周期性节点
        if '电动船' in label:
            cycle_ratio = (params['annual_hours'] * params['electric_consumption_per_hour'] / params['battery_capacity_kWh']) if params['battery_capacity_kWh'] else 0
            battery_cycle = params['battery_cycle_life'] / cycle_ratio if cycle_ratio else 0
            for jump in get_jump_years(battery_cycle, years[-1]):
                fig.add_trace(go.Scatter(x=[jump], y=[y_data[jump]/1e4], mode='markers+text', marker=dict(color='black', size=10, symbol='diamond'), text=["电池更换"], textposition="top right", showlegend=False))
        else:
            overhaul_int = params.get('overhaul_interval_years_diesel', 10)
            for jump in get_jump_years(overhaul_int, years[-1]):
                fig.add_trace(go.Scatter(x=[jump], y=[y_data[jump]/1e4], mode='markers+text', marker=dict(color='black', size=10, symbol='x'), text=["大修"], textposition="bottom right", showlegend=False))
    fig.update_layout(title='累计成本对比 (10k €)', xaxis_title='运营年数', yaxis_title='累计成本 (10k €)', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
def show_opex_piecharts(costs, params) -> None:
    st.subheader("📊 模块 M8 - 运营成本占比分析")
    ship_type = st.radio("选择船型：", ["电动船 (EU)", "电动船 (CN)", "STAGE V 柴油船 (EU)"], horizontal=True, key="opex_ship")
    view_type = st.radio("选择成本视图：", ["年度运营成本", "全生命周期成本"], horizontal=True, key="opex_view")
    years = params.get('lifecycle_years', 25)
    crew = params['crew_num'] * params['crew_avg_cost']
    # 计算各项
    if "柴油" in ship_type:
        energy = params['diesel_consumption_per_hour'] * params['annual_hours'] * params['mgo_price']
        port = params['port_fee']
        maint = params['maintenance_cost_diesel']
        overhaul = params['overhaul_cost_per_event_diesel'] * (years // params['overhaul_interval_years_diesel'])
        battery = 0
    else:
        energy = params['electric_consumption_per_hour'] * params['annual_hours'] * params['electricity_price']
        port = 0
        maint = params['maintenance_cost_electric']
        replace = params['battery_replace_cost_eu'] if "EU" in ship_type else params['battery_replace_cost_cn']
        cycle = params['battery_cycle_life'] / (params['annual_hours'] * params['electric_consumption_per_hour'] / params['battery_capacity_kWh']) if params['battery_capacity_kWh'] else float('inf')
        battery = replace * (years // cycle)
        overhaul = 0
    insurance = costs['insurance_costs'][ship_type]
    if view_type == "全生命周期成本":
        energy *= years
        maint *= years
        crew *= years
        port *= years
        battery *= years
        insurance *= years
    labels = ['能源', '维护', '船员', '港口费', '大修费', '保险', '电池更换费']
    sizes = [energy, maint, crew, port, overhaul, insurance, battery]
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, *_ = ax.pie(sizes, labels=None, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', startangle=90, pctdistance=0.75)
    ax.legend(wedges, labels, title='成本分项', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), frameon=False)
    title = f"{ship_type} — {view_type} 占比图"
    ax.set_title(title, y=1.05)
    ax.axis('equal')
    plt.tight_layout(); st.pyplot(fig)
def show_roi_analysis(costs, params) -> None:
    st.subheader("💹 模块 M9 - ROI与回本周期分析")
    ship_types = ["电动船 (EU)", "电动船 (CN)", "STAGE V 柴油船 (EU)"]
    ship = st.radio("选择船型：", ship_types, horizontal=True, key="roi_ship")
    years = costs['years']
    cashflow = costs['cum_cashflow'][ship]
    payback = costs['payback_year'][ship]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=cashflow, mode='lines+markers', name='累计净现金流'))
    if payback is not None:
        fig.add_vline(x=payback, line_dash='dash', line_color='red', annotation_text=f"回本年限: {payback}年")
    fig.update_layout(title="累计净现金流与回本周期", xaxis_title="运营年数", yaxis_title="累计净现金流 (€)"); st.plotly_chart(fig, use_container_width=True)
def show_carbon_emissions(costs) -> None:
    st.subheader("♻️ 模块 M11 - 碳排放与减排效益分析")
    annual_emissions = costs.get('annual_emissions', {})
    labels = list(annual_emissions.keys())
    values = [annual_emissions[k] for k in labels]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=['#EF553B', '#00CC96', '#636EFA']))
    fig.update_layout(title='年度碳排放量 (吨CO₂)', yaxis_title="碳排放 (吨CO₂/年)")
    st.plotly_chart(fig, use_container_width=True)