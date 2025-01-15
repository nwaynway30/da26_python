import streamlit as st
from google.cloud import bigquery
from google.auth import load_credentials_from_file
from google.cloud.bigquery import Client

# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

credentials, project_id = load_credentials_from_file('/Users/thyneminhtetaungaung/Music Project All file /service_account.json')

# Load data from BigQuery
client = Client(
    project = project_id,
    credentials=credentials
)

# This is how to list the tables
database_id = "music_data"
tables = client.list_tables(database_id)

print(f"Tables contained in '{database_id}':")
for table in tables:
    print(f"{table.project}.{table.dataset_id}.{table.table_id}")

query = "SELECT * FROM `da26-python.music_data.tracks`"
load_job = client.query(query)
data = load_job.to_dataframe()

@st.cache_data
def load_data(table):
    query = f"SELECT * FROM `da26-python.music_data.{table}`"
    load_job = client.query(query)
    data = load_job.to_dataframe()
    return data

#  Load data 
audio_features = load_data("audio_features")
chart_positions = load_data("chart_positions")
artists = load_data("artists")
tracks = load_data("tracks")
tracks_artists_mapping = load_data("tracks_artists_mapping")

#extract year, month, date 
# release date data to year colum
def func(item):
    day = item.split("-")
    if len(day) == 1:
        return int(day[0]),0,0
    elif len(day) == 2:
        return int(day[0]), int(day[1]), 0
    else:
        return int(day[0]), int(day[1]), int(day[2])

tracks[["year","month","day"]] = tracks["release_date"].apply(lambda x:pd.Series(func(x)))
print(tracks[["year","month","day"]])

# Merge Data for all data sets. 
master_data = tracks.merge(tracks_artists_mapping, on="track_id").merge(artists, on="artist_id").merge(chart_positions, on="track_id").merge(audio_features, on="track_id")

#remove dublicate from combine data
master_data.drop_duplicates(inplace=True)
master_data.reset_index(inplace=True)


# Rename for "name"
master_data.rename(columns={'name_x': 'track_name', 'name_y': 'artist_name'}, inplace=True)

# Drop Index Column
master_data.drop(columns= "index", inplace = True)
master_data = master_data.reset_index(drop=True)

# Change Datetime at Chart_week
master_data.chart_week = pd.to_datetime(master_data.chart_week)

# Monthly song analysis _Filter by year 

st.header("The Most Popular Song in Month_Filter by Year")
year = st.selectbox("Select Year",[x for x in range(2000,2025)])
Monthly_Data = master_data.loc[master_data.chart_week.dt.year == year].groupby([master_data.chart_week.dt.month,'track_name'])['list_position'].sum().unstack().idxmin(axis=1)
st.dataframe(Monthly_Data)

# Which tracks with high popularity scores also have high danceability values, making them suitable for live performances?
st.header("Popular Track_Artist and its Feature")
Feature = st.selectbox("Select Features",["danceability","energy"])
Track_Feature_Dancebility = master_data.groupby(["track_name","artist_name"])[["popularity",Feature]].sum().sort_values(ascending = False,by = ["popularity",Feature]).head(20)
st.dataframe(Track_Feature_Dancebility)

# track information by list position_one to five/ and counting to chart week
st.header("Popular Track_Position 1 ")
input_year = st.selectbox("year_list",[x for x in range(2000,2025)])
# getting track information by list_position = one to five, only for track_name
track_dominace = master_data.loc[master_data.list_position ==1, ["track_name","artist_name", "chart_week", "list_position","year"]]
# track information by list position one to give and filter by year. / how long chart week by list position one
 # Ensure the 'chart_week' is processed correctly by extracting the year
track_dominance = track_dominace.copy()  # Ensure track_dominace is properly defined
track_dominance['chart_week_year'] = track_dominance['chart_week'].dt.year
# Group by track_name, artist_name, and year, then count unique chart weeks
result = (
    track_dominance.groupby(['track_name', 'artist_name', 'chart_week_year'])['chart_week']
    .nunique()
    .reset_index()
    .rename(columns={'chart_week': 'count_chart_week'})
    .sort_values(by=['chart_week_year', 'count_chart_week'], ascending=False)
)
popular_track_one = result.loc[result.chart_week_year == input_year]
st.dataframe(popular_track_one)

# getting track information by list_position = one to five, only for track_name
st.header("Popular Track_Position 1-5 ")
input_year = st.selectbox("year_list1",[x for x in range(2000,2025)])
track_dominace1 = master_data.loc[master_data.list_position.isin([1,2,3,4,5]), ["track_name", "artist_name", "chart_week", "list_position"]]
# Ensure the 'chart_week' is processed correctly by extracting the year
track_dominance1 = track_dominace1.copy()  # Ensure track_dominace is properly defined
track_dominance1['chart_week_year'] = track_dominance1['chart_week'].dt.year

# Group by track_name, artist_name, and year, then count unique chart weeks
result1 = (
    track_dominance1.groupby(['track_name', 'chart_week_year', 'list_position'])['chart_week']
    .nunique()
    .reset_index()
    .rename(columns={'chart_week': 'count_chart_week'})
    .sort_values(by=['list_position', 'count_chart_week'], ascending=False)
)
popular_track_one1 = result1.loc[result1.chart_week_year == input_year]
st.dataframe(popular_track_one1)