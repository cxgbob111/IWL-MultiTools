# sensitivity_analysis.py (v6.0)
"""敏感性分析模块（v6.0）。

分析关键参数变化对船舶累计成本的影响，通过选择敏感因素并对其取值
进行±20%变化，绘制累计成本曲线对比图。
"""

import streamlit as st
import plotly.graph_objects as go
from copy import deepcopy
from cost_calculations import calculate_costs


def sensitivity_module(costs, params) -> None:
    """展示敏感性分析。"""
    with st.expander("📊 敏感性分析模块"):
        st.subheader("敏感因素选择")
        factor = st.selectbox(
            "选择敏感因素",
            ["柴油价格", "电价", "电池价格", "年度运营小时数", "保险优惠比例"],
        )
        variations = [-20, -10, 0, 10, 20]
        results = {}
        for var in variations:
            adj = 1 + var / 100.0
            new_params = deepcopy(params)
            # 根据敏感因素调整参数
            if factor == "柴油价格":
                new_params['mgo_price'] = params['mgo_price'] * adj
            if factor == "电价":
                new_params['electricity_price'] = params['electricity_price'] * adj
            if factor == "电池价格":
                new_params['battery_price'] = params['battery_price'] * adj
            if factor == "年度运营小时数":
                new_params['annual_hours'] = params['annual_hours'] * adj
            if factor == "保险优惠比例":
                new_params['insurance_discount'] = params['insurance_discount'] * adj
            # 调整换电成本
            new_params['battery_replace_cost_eu'] = new_params['battery_capacity_kWh'] * new_params['battery_price'] * new_params['battery_replace_ratio_eu']
            new_params['battery_replace_cost_cn'] = new_params['battery_capacity_kWh'] * new_params['battery_price'] * 0.7 * new_params['battery_replace_ratio_cn']
            # 重新计算成本
            adj_costs = calculate_costs(new_params)
            results[f"{var}%"] = adj_costs['cumulative_costs']
        # 绘图
        fig = go.Figure()
        base_labels = {"STAGE V 柴油船 (EU)": "EU D", "电动船 (EU)": "EU E", "电动船 (CN)": "CN E"}
        colors = ['blue', 'green', 'orange']
        # 基准曲线
        for idx, name in enumerate(base_labels):
            fig.add_trace(go.Scatter(
                x=costs['years'],
                y=[v/1e4 for v in costs['cumulative_costs'][name]],
                mode='lines+markers',
                name=f"{base_labels[name]} (基准)",
                line=dict(width=3, color=colors[idx]),
            ))
        # 敏感性曲线
        for var, data in results.items():
            for idx, name in enumerate(base_labels):
                fig.add_trace(go.Scatter(
                    x=costs['years'],
                    y=[v/1e4 for v in data[name]],
                    mode='lines',
                    name=f"{base_labels[name]} ({factor} {var})",
                    line=dict(width=1.5, dash='dot', color=colors[idx]),
                ))
        fig.update_layout(
            title='船舶成本敏感性分析 (单位: 10k €)',
            xaxis_title='运营年数',
            yaxis_title='累计成本 (10k €)',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)