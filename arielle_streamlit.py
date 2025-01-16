import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset (assuming 'songs' is already available or loaded as a pandas DataFrame)
# Example of how to load data:
# songs = pd.read_csv('your_data.csv')

# Streamlit title and description
st.title("Trends in Danceability and Energy (2005 - Present)")
st.write("This visualization shows the trends of average danceability and energy of tracks in the top 40, from 2005 to present.")

# Filter data for tracks in list_position 1-40 and from 2005 onwards
top40 = songs[(songs['list_position'] <= 40) & (songs['chart_year'] >= 2005)]

# Group by year and calculate average danceability and energy
yearly_trends = (
    top40.groupby('chart_year')[['danceability', 'energy']]
    .mean()
    .reset_index()
)

# Plot the trends using Seaborn
sns.set(style="whitegrid")

# Create figure for Streamlit
fig, ax = plt.subplots(figsize=(12, 6))

# Plot danceability trend
sns.lineplot(
    data=yearly_trends,
    x='chart_year',
    y='danceability',
    marker='o',
    label='Danceability',
    ax=ax
)

# Plot energy trend
sns.lineplot(
    data=yearly_trends,
    x='chart_year',
    y='energy',
    marker='o',
    label='Energy',
    ax=ax
)

# Customize the plot
ax.set_title('Trends in Danceability and Energy (2005 - Present)', fontsize=16)
ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Average Value', fontsize=14)
ax.legend(fontsize=12)
ax.set_xticks(range(2005, yearly_trends['chart_year'].max() + 1, 2))
ax.set_xticklabels(range(2005, yearly_trends['chart_year'].max() + 1, 2), rotation=45)
plt.tight_layout()

# Show plot in Streamlit
st.pyplot(fig)
