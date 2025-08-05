# cemt_reference.py (v6.0)
"""CEMT 级别速查模块（v6.0）。

根据船舶长度匹配 CEMT 级别并显示宽度范围、航道里程、估算
船舶数量、典型功率以及 60 km 续航所需电量。此模块
独立放在 modules 目录中，便于维护与迭代。
"""

import streamlit as st


def cemt_reference_module() -> None:
    """展示 CEMT 等级参考信息。"""
    with st.expander("📑 CEMT 级别速查模块"):
        st.subheader("CEMT 船舶规范查询")
        length = st.number_input("输入船舶长度 L (m)", min_value=0.0, value=90.0, step=1.0, key="cemt_length")
        cemt_table = [
            {"级别": "I", "长度范围": (0.0, 38.5), "宽度范围": "≤5.05 m", "水道里程": 300, "船舶数": 200, "功率范围": "≤200 kW"},
            {"级别": "II", "长度范围": (38.5, 50.0), "宽度范围": "5.05–6.60 m", "水道里程": 1200, "船舶数": 800, "功率范围": "200–400 kW"},
            {"级别": "III", "长度范围": (50.0, 80.0), "宽度范围": "6.60–9.50 m", "水道里程": 2000, "船舶数": 1500, "功率范围": "400–600 kW"},
            {"级别": "IV", "长度范围": (80.0, 110.0), "宽度范围": "9.50–11.40 m", "水道里程": 3500, "船舶数": 1200, "功率范围": "600–1000 kW"},
            {"级别": "V", "长度范围": (110.0, 185.0), "宽度范围": "11.40–12.50 m", "水道里程": 5000, "船舶数": 600, "功率范围": "1000–1500 kW"},
            {"级别": "VI", "长度范围": (185.0, 200.0), "宽度范围": "12.50–17.00 m", "水道里程": 750, "船舶数": 150, "功率范围": "1500–2000 kW"},
        ]
        matched = None
        for row in cemt_table:
            lo, hi = row["长度范围"]
            if lo <= length <= hi:
                matched = row
                break
        if matched:
            st.markdown(f"**匹配 CEMT 级别：** {matched['级别']}")
            st.markdown(f"- 长度范围：{matched['长度范围'][0]}–{matched['长度范围'][1]} m")
            st.markdown(f"- 宽度范围：{matched['宽度范围']}")
            st.markdown(f"- 对应航道总里程：{matched['水道里程']} km")
            st.markdown(f"- 估算船舶数量：{matched['船舶数']} 艘")
            st.markdown(f"- 典型推进功率范围：{matched['功率范围']}")
            if '–' in matched['功率范围']:
                p_min, p_max = [int(x) for x in matched['功率范围'].replace(' kW','').split('–')]
            else:
                single = int(matched['功率范围'].replace('≤','').split()[0])
                p_min = p_max = single
            p_avg = (p_min + p_max) / 2
            hours = 60 / 10
            energy_needed = p_avg * hours
            st.markdown(f"- 按平均功率 {p_avg:.0f} kW，完成 60 km 续航 (~{hours:.0f} 小时)：需电量约 {energy_needed:.0f} kWh")
        else:
            st.warning("未找到匹配的 CEMT 级别，请检查输入的船长是否在 0–200 m 范围内。")