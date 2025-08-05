# power_calculation.py (v6.0)
"""船舶功率需求专业计算模块（v6.0）。

通过经验系数与排水量计算推荐安装功率和连续巡航功率。
"""

import streamlit as st


def power_module() -> None:
    """展示功率需求计算界面。"""
    with st.expander("🛠️ 船舶功率需求专业计算模块"):
        st.subheader("基于排水量的功率经验估算")
        displacement = st.number_input('排水量 Δ (t)', value=1800.0, min_value=0.0, step=10.0, key='disp')
        k_disp = st.slider('经验系数 k_disp (0.5–0.7 kW/t)', min_value=0.1, max_value=1.0, value=0.6, step=0.05, key='k_disp')
        P_inst = k_disp * displacement
        P_cruise = P_inst * 0.7
        st.metric("⚡ 推荐安装功率 P_inst (kW)", f"{P_inst:.0f} kW")
        st.metric("⏱️ 估算连续巡航功率 P_cruise (kW)", f"{P_cruise:.0f} kW")
        st.markdown(f"""
        **公式说明：**  
        - 安装功率：\(P_{{inst}} = k_{{disp}} \times Δ\)  
        - 连续功率：\(P_{{cruise}} = 0.7 \times P_{{inst}}\)  

        **推荐取值：**  
        - 排水量 Δ = {displacement:.0f} t  
        - 经验系数 k_disp = {k_disp:.2f} kW/t  
        - 安装功率 ≈ {P_inst:.0f} kW  
        - 连续巡航功率 ≈ {P_cruise:.0f} kW  
        """)