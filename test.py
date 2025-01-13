# 导入库
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 设置侧边栏背景颜色
sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        background-color: #f5f5dc;
    }
    </style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

# 设置标题
st.title("Spotify 2000s Music Analysis")

# 模拟数据加载（替换为实际数据）
# 合并数据代码省略，请参考前面步骤完成合并后的 `artist_tracks`
# 示例模拟表格：
chart_positions = pd.DataFrame({"list_position": [1, 1, 2], "track_id": [101, 102, 103], "chart_week": ["2001-01-01", "2002-02-02", "2003-03-03"]})
artist_tracks = pd.DataFrame({"track_id": [101, 102, 103], "track_name": ["Song A", "Song B", "Song C"], "artist_name": ["Artist X", "Artist Y", "Artist Z"]})

# 模拟分析数据
number_one_songs = pd.DataFrame({"track_name": ["Song A", "Song B"], "weeks_at_number_one": [10, 8]})
number_one_artists = pd.DataFrame({"artist_name": ["Artist X", "Artist Y"], "weeks_at_number_one": [10, 8]})

# 侧边栏小标题
with st.sidebar:
    st.header("Analysis Options")
    with st.expander("🎵 Songs by Weeks at #1"):
        st.write("Analyze the performance of songs that reached the #1 spot.")
    with st.expander("🎤 Artists by Weeks at #1"):
        st.write("Analyze the performance of artists by total weeks at #1.")
    with st.expander("📊 Tracks by #1 Entries"):
        st.write("Analyze the tracks that have appeared the most at #1.")

# 显示内容
st.subheader("🎵 Songs by Weeks at #1")
st.dataframe(number_one_songs)

st.subheader("🎤 Artists by Weeks at #1")
st.dataframe(number_one_artists)