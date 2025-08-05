# data_loader.py (v6.0)
"""数据加载模块（v6.0）。

提供读取 Excel 数据的函数。使用 Streamlit 的缓存机制
避免重复加载文件。
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(file_path: str = 'detailed_ship_cost_analysis_updated.xlsx'):
    """读取 Excel 文件并返回所有工作表的字典。"""
    return pd.read_excel(file_path, sheet_name=None)