# charging_analysis.py (v6.0)
"""岸电充电分析模块（v6.0）。

计算岸电三相充电功率和可充入的电量，展示结果。
"""

import streamlit as st
import math


def charging_module() -> None:
    """展示岸电充电分析。"""
    with st.expander("🔌 岸电充电分析模块"):
        st.subheader("岸电充电参数设置")
        voltage = st.number_input('岸电电压(V)', value=400)
        current = st.number_input('岸电电流(A)', value=125)
        docking_hours = st.number_input('靠岸可用时间(小时)', value=10.0, step=0.5)
        battery_capacity = st.number_input('船载电池总容量(kWh)', value=2000)
        power_factor = st.number_input('功率因数（PF）', value=0.9, min_value=0.8, max_value=1.0, step=0.01)
        charged_power = voltage * current * math.sqrt(3) * power_factor / 1000.0  # kW
        charged_energy = min(charged_power * docking_hours, battery_capacity)
        st.metric(label="🔋 充电功率(kW)", value=f"{charged_power:.2f} kW")
        st.metric(label="⚡ 实际充入电量(kWh)", value=f"{charged_energy:.2f} kWh")
        st.info(f"根据当前岸电（交流三相）设置，船舶实际充入电量为 {charged_energy:.2f} kWh。")