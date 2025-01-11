import streamlit as st
from data_processing import load_data
from visualisations import bar_chart

st.title("Music Dashboard")

data = load_data()
bar_chart(data, "Artist")
