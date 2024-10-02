import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.markdown("""
    <style>
    .title {
        font-size: 38px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
    }
    .subtitle {
        font-size: 16px;
        font-weight: normal;
        color: #4b6584;
        text-align: center;
        margin-top: -30px;
        padding-bottom: 20px;
        font-style: italic;
    }
    </style>
    <h1 class="title">🚴‍♂️ Bike Sharing Data Visualization 🚴‍♀️</h1>
    <h2 class="subtitle">Exploring Trends and Insights from Bike Rentals</h2>
    """, unsafe_allow_html=True)

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path_day_csv = os.path.join(project_folder, "data", "day.csv")
file_path_hour_csv = os.path.join(project_folder, "data", "hour.csv")

day_data = pd.read_csv(file_path_day_csv)
hour_data = pd.read_csv(file_path_hour_csv)

dteday_column = ["dteday"]
for column in dteday_column:
    day_data[column] = pd.to_datetime(day_data[column])
    hour_data[column] = pd.to_datetime(hour_data[column])

selected_option = st.selectbox("Select Visualization Option", ["Total and Average Rentals on Daily Basis", "Total and Average Rentals per Season"])

if selected_option == "Total and Average Rentals on Daily Basis":
    st.header("Total and Average Rentals on Daily Basis")
    

    hourly_rentals = hour_data.groupby("hr")['cnt'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_rentals.plot(kind='line', ax=ax)
    
    ax.set_xlabel('Time (Hours)', fontsize=12)
    ax.set_ylabel('Total Rentals', fontsize=12)
    ax.set_title('Total Rentals on Daily Basis', fontsize=14)
    ax.grid(True)
    
    st.pyplot(fig)


    hourly_rentals_avg = hour_data.groupby("hr")['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_rentals_avg.plot(kind='line', color='red', ax=ax)
    
    ax.set_xlabel('Time (Hours)', fontsize=12)
    ax.set_ylabel('Average Rentals', fontsize=12)
    ax.set_title('Average Rentals on Daily Basis', fontsize=14)
    ax.grid(True)
    
    st.pyplot(fig)

    st.subheader("Conclusion")
    st.write("The peak of bike rentals occurs at two main times: 8 AM and 5 PM, coinciding with daily rush hours. The lowest number of rentals happens in the early morning, around 4 AM. Based on this trend, a more efficient operational strategy can focus the bike rental service from midday to the afternoon. Ensuring more bikes are available in the evening will help meet the high demand and increase profits.")

elif selected_option == "Total and Average Rentals per Season":
    st.header("Total and Average Rentals per Season")
    

    seasonal_sum = day_data.groupby("season").agg({
        "instant": "nunique",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    
    season_name = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    seasonal_sum = seasonal_sum[seasonal_sum.index.isin(season_name.keys())]
    seasonal_sum.index = seasonal_sum.index.map(season_name)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    seasonal_sum.plot(kind='bar', ax=ax)
    
    ax.set_xlabel('Season', fontsize=12)
    ax.set_ylabel('Rentals\' Count', fontsize=12)
    ax.set_title('Total Rentals per Season', fontsize=14)
    ax.set_xticklabels(season_name.values(), rotation=0, fontsize=10)
    ax.grid(True)
    
    st.pyplot(fig)
    

    seasonal_avg = day_data.groupby("season").agg({
        "instant": "nunique",
        "casual": "mean",
        "registered": "mean",
        "cnt": "mean"
    })

    seasonal_avg = seasonal_avg[seasonal_avg.index.isin(season_name.keys())]
    seasonal_avg.index = seasonal_avg.index.map(season_name)

    fig, ax = plt.subplots(figsize=(10, 6))
    seasonal_avg.plot(kind='bar', ax=ax)
    
    ax.set_xlabel('Season', fontsize=12)
    ax.set_ylabel('Rentals\' Average', fontsize=12)
    ax.set_title('Average Rentals per Season', fontsize=14)
    ax.set_xticklabels(season_name.values(), rotation=0, fontsize=10)
    ax.grid(True)
    
    st.pyplot(fig)

    st.subheader("Conclusion")
    st.write("The peak of bike rentals is observed in the fall and summer, while winter and spring experience a significant decline. Fall emerges as the season with the highest demand, followed by summer, winter, and finally spring. This data can guide a more effective rental strategy, focusing on availability and promotions during the high-demand seasons, while adjusting operations during the low-demand seasons to reduce costs.")
