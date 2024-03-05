import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

df = pd.read_csv("main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Capital Bikeshare: Bike-sharing Dashboard",
                   page_icon="chart_with_upwards_trend",
                   layout="wide")

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='ME', on='dteday').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    })

    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    return monthly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby('weekday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })

    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    weekday_users_df = pd.melt(weekday_users_df, id_vars="weekday", var_name="type", value_name="Count of bikeshare rides")

    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby('hr').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })

    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    hourly_users_df = pd.melt(hourly_users_df, id_vars="hr", var_name="type", value_name="Count of bikeshare rides")

    return hourly_users_df

def create_seasonal_users_df(df):
    seasonal_users_df = df.groupby('season').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })

    seasonal_users_df = seasonal_users_df.reset_index()
    seasonal_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    seasonal_users_df = pd.melt(seasonal_users_df, id_vars="season", var_name="type", value_name="Count of bikeshare rides")

    return seasonal_users_df

def create_weather_users_df(df):
    weather_users_df = df.groupby('weathersit').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })

    weather_users_df = weather_users_df.reset_index()
    weather_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    weather_users_df = pd.melt(weather_users_df, id_vars="weathersit", var_name="type", value_name="Count of bikeshare rides")

    return weather_users_df

# make filter components (komponen filter)

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# ----- SIDEBAR -----

with st.sidebar:
    st.sidebar.header("Filter:")
    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = df[(df["dteday"] >= start_date) & 
             (df["dteday"] <= end_date)]

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)
seasonal_users_df = create_seasonal_users_df(main_df)
weather_users_df = create_weather_users_df(main_df)

# ----- MAIN PAGE -----
st.title(":chart_with_upwards_trend: Capital Bikeshare: Bike-sharing Dashboard")
st.markdown("---")


total_all_rides = main_df['cnt'].sum()
total_casual_rides = main_df['casual'].sum()
total_registered_rides = main_df['registered'].sum()

fig = px.pie(main_df, names=['Casual', 'Registered'], values=[total_casual_rides, total_registered_rides], title="Total Bikeshare Rides by Type")

left_column, right_column = st.columns((1,3))
left_column.markdown(
    """
    <style>
    .vertical-line {
        border-right: 1px solid #ccc;
        padding-right: 10px;
        margin-right: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
right_column.plotly_chart(fig, use_container_width=True)
with left_column:
    st.markdown("##")
    st.markdown("##")
    st.metric("Total Rides", value="{:,}".format(total_all_rides))
    st.markdown("##")
    st.metric("Total Casual Rides", value="{:,}".format(total_casual_rides))
    st.markdown("##")
    st.metric("Total Registered Rides", value="{:,}".format(total_registered_rides))

# plot hourly
fig = px.bar(hourly_users_df,
                x='hr',
                y='Count of bikeshare rides',
                color='type',
                barmode='group',
                title="Count of Bikeshare Rides by Hour").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

# plot monthly
fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["red", "blue", "purple"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

# plot weekday
fig = px.bar(weekday_users_df,
                x='weekday',
                y='Count of bikeshare rides',
                color='type',
                barmode='group',
                title="Count of Bikeshare Rides by Weekday").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

# plot seasonal and weather
fig1 = px.bar(seasonal_users_df,
                x='season',
                y='Count of bikeshare rides',
                color='type',
                barmode='group',
                title="Count of Bikeshare Rides by Season").update_layout(xaxis_title='', yaxis_title='Total Rides')

fig2 = px.bar(weather_users_df,
                x='weathersit',
                y='Count of bikeshare rides',
                color='type',
                barmode='group',
                title="Count of Bikeshare Rides by Weather").update_layout(xaxis_title='(1: Clear, 2: Slightly Bad, 3: Bad, 4: Very Bad)', yaxis_title='Total Rides')
                
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig1 = px.scatter(main_df, x='temp', y='cnt', color='season', title='Clusters of bikeshare rides count by temp')
fig2 = px.scatter(main_df, x='atemp', y='cnt', color='season', title='Clusters of bikeshare rides count by atemp')
fig3 = px.scatter(main_df, x='hum', y='cnt', color='season', title='Clusters of bikeshare rides count by hum')
fig4 = px.scatter(main_df, x='windspeed', y='cnt', color='season', title='Clusters of bikeshare rides count by windspeed')

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_container_width=True)

st.markdown("---")