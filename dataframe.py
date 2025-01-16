from google.cloud import bigquery
from google.auth import load_credentials_from_file
from google.cloud.bigquery import Client
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# load BigQuery credentials and data
credentials, project_id = load_credentials_from_file('service_account.json')

client = Client(
    project=project_id,
    credentials=credentials
)

# load data function
def load_data(table):
    query = f"SELECT * FROM `da26-python.music_data.{table}`"
    load_job = client.query(query)
    return load_job.to_dataframe()

# Data Processing Functions
def load_and_merge_data():
    # Load all dataframes
    audio_features = load_data("audio_features")
    chart_positions = load_data("chart_positions")
    artists = load_data("artists")
    tracks = load_data("tracks")
    tracks_artists = load_data("tracks_artists_mapping")
    
   
    
    # merge songs data with audio features and chart positions
    songs = (
        tracks
        .merge(audio_features, on='track_id', how='left')
        .merge(chart_positions, on='track_id', how='left')
    )
    
    # convert release_date to datetime
    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str)
        except:
            try:
                if len(str(date_str)) >= 4:
                    year = int(str(date_str)[:4])
                    return pd.to_datetime(f"{year}-01-01")
            except:
                return pd.NaT

    songs['release_date'] = songs['release_date'].apply(parse_date)
    songs['release_year'] = songs['release_date'].dt.year
    
    # convert chart_week to datetime
    songs['chart_week'] = pd.to_datetime(songs['chart_week'])
    songs['chart_year'] = songs['chart_week'].dt.year
    
    
    # add 0s to missing values
    songs['list_position'] = songs['list_position'].fillna(0)
    
    # build a dataframe of artists
    singers = (
        artists
        .merge(tracks_artists, on='artist_id', how='left')
        .groupby('artist_id')
        .agg({
            'name': 'first',
            'popularity': 'first',
            'followers': 'first',
            'track_id': 'count'
        })
        .rename(columns={'track_id': 'total_tracks'})
        .reset_index()
    )
    
    return singers, songs

singers, songs = load_and_merge_data()
#if you want to run this function, you need to run the load_data function first
print(songs.sample(10))
print(singers.sample(10))