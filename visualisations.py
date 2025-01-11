import pandas as pd
import streamlit as st


# Barchart
def bar_chart(data: pd.DataFrame, column: str) -> None:
    st.write("Think of this as a bar chart")
    st.write(data)


# Line chart with categories (time as the x-axis)
def line_chart(data: pd.DataFrame, column: str):
    pass


# Donut chart
def donut_chart(data: pd.DataFrame, column: str):
    pass
