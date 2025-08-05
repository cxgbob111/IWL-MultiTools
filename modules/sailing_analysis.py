# sailing_analysis.py (v6.0)
"""续航能力分析模块（v6.0）。

根据充入电量与航行功率估算可航行时间和距离。
"""

import streamlit as st


def sailing_module() -> None:
    """展示续航能力分析界面。"""
    with st.expander("🚤 续航能力分析模块"):
        st.subheader("航行参数设置")
        charged_energy = st.number_input('实际充入电量(kWh)', value=2000, key='charged_energy_sailing_module')
        ship_power = st.number_input('船舶额定功率(kW)', value=300, key='ship_power_sailing_module')
        sailing_speed = st.slider('航行速度(km/h)', min_value=5, max_value=20, value=10, step=1, key='sailing_speed_sailing_module')
        sailing_hours_actual = charged_energy / ship_power if ship_power else 0
        sailing_distance = sailing_hours_actual * sailing_speed
        st.metric(label="⏱️ 实际可支撑续航时间(小时)", value=f"{sailing_hours_actual:.2f} 小时")
        st.metric(label="📏 实际可航行距离(km)", value=f"{sailing_distance:.2f} km")
        st.info(f"在当前充电量和航行功率下，船舶预计可以持续航行 {sailing_hours_actual:.2f} 小时，约合 {sailing_distance:.2f} 公里。")