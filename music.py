from google.cloud import bigquery
from google.auth import load_credentials_from_file
from google.cloud.bigquery import Client

credentials, project_id = load_credentials_from_file('service_account.json')

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

audio_features.sample(10)

# check the data types
import streamlit as st
import pandas as pd

# Load data
st.title("Spotify Music Dashboard")
st.write("Loading data from Google BigQuery...")
data = load_data("audio_features")
st.write("Data loaded successfully!")

# Display the dataset
st.dataframe(data)

# Simple visualization
st.line_chart(data['energy'])