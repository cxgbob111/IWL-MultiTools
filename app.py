# app.py (v6.0)
"""
BOTIX 荷兰内河船全周期成本分析工具

这是升级版主程序入口文件（v6.0），负责初始化页面、加载
输入参数、执行成本计算并调度各功能模块。文件控制
UI 排版，确保各分析模块按照顺序展示，同时嵌入
品牌 LOGO。每个程序文件保持在 100 行以内，便于维护
与迭代。
"""

import streamlit as st

from inputs import sidebar_inputs
from cost_calculations import calculate_costs
from visualizations import (
    show_cost_charts,
    show_opex_piecharts,
    show_roi_analysis,
    show_carbon_emissions,
)
from modules.cemt_reference import cemt_reference_module
from modules.charging_analysis import charging_module
from modules.power_calculation import power_module
from modules.sailing_analysis import sailing_module
from modules.sensitivity_analysis import sensitivity_module


def main() -> None:
    """主函数，配置页面并渲染所有模块。"""
    st.set_page_config(
        page_title="BOTIX 荷兰内河船全周期成本分析工具",
        layout="wide",
    )
    # 显示 LOGO
    st.image("assets/botix_logo.png", width=150)
    st.title("BOTIX 荷兰内河船全周期成本与收益分析")
    st.markdown("---")

    # 1. 获取用户输入
    params = sidebar_inputs()
    # 2. 执行成本计算
    try:
        costs = calculate_costs(params)
    except Exception as ex:
        st.error(f"🚨 成本计算出错: {ex}")
        st.stop()
    # 3. 模块展示
    st.markdown("## 📈 模块 M2 - 成本累计与对比分析")
    show_cost_charts(costs, params)
    st.markdown("---")

    st.markdown("## 📊 模块 M8 - 运营成本占比分析")
    show_opex_piecharts(costs, params)
    st.markdown("---")

    st.markdown("## 💹 模块 M9 - ROI与回本周期分析")
    show_roi_analysis(costs, params)
    st.markdown("---")

    st.markdown("## ♻️ 模块 M11 - 碳排放与减排效益分析")
    show_carbon_emissions(costs)
    st.markdown("---")

    st.markdown("## 📊 模块 M10 - 成本敏感性分析")
    sensitivity_module(costs, params)
    st.markdown("---")

    st.markdown("## 📑 模块 M12 - CEMT 船型快速查询")
    cemt_reference_module()
    st.markdown("---")

    st.markdown("## 🔌 岸电充电能力分析模块")
    charging_module()
    st.markdown("---")

    st.markdown("## 🛠️ 船舶功率需求计算模块")
    power_module()
    st.markdown("---")

    st.markdown("## 🚤 续航能力分析模块")
    sailing_module()
    st.markdown("---")


if __name__ == "__main__":
    main()