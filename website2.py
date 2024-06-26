import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Function to generate sample data
def generate_sample_data():
    departments = ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics']
    physicians = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown']
    
    data = {
        'Department': np.random.choice(departments, 100),
        'Physician': np.random.choice(physicians, 100),
        'Patient Wait Time': np.random.randint(5, 120, 100),
        'Bed Occupancy Rate': np.random.uniform(0.5, 1, 100),
        'Readmission Rate': np.random.uniform(0.05, 0.2, 100),
        'Available Beds': np.random.randint(0, 20, 100),
        'Date': [datetime.now() - timedelta(days=x) for x in range(100)],
    }
    return pd.DataFrame(data)

# Generate sample data
df = generate_sample_data()

# Streamlit app
st.set_page_config(layout="wide", page_title="Hospital Dashboard")

st.title("Hospital Dashboard")

# Filters
col1, col2 = st.columns(2)
with col1:
    department = st.selectbox("Select Department", ['All'] + list(df['Department'].unique()))
with col2:
    physician = st.selectbox("Select Physician", ['All'] + list(df['Physician'].unique()))

# Filter data
if department != 'All':
    df = df[df['Department'] == department]
if physician != 'All':
    df = df[df['Physician'] == physician]

# KPIs
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg. Patient Wait Time", f"{df['Patient Wait Time'].mean():.0f} min")
col2.metric("Avg. Bed Occupancy Rate", f"{df['Bed Occupancy Rate'].mean():.2%}")
col3.metric("Avg. Readmission Rate", f"{df['Readmission Rate'].mean():.2%}")
col4.metric("Available Beds", f"{df['Available Beds'].iloc[-1]}")

# Alert for low available beds
if df['Available Beds'].iloc[-1] < 10:
    st.warning("Alert: Available beds are less than 10!", icon="⚠️")
    # Here you would typically trigger a sound, but web browsers often block autoplay.
    # Instead, we'll use a more visible alert.
    st.error("URGENT: Low bed availability!")

# Charts
st.header("Charts")

# Line chart for patient wait times
fig_wait_times = px.line(df, x='Date', y='Patient Wait Time', title='Patient Wait Times Over Time')
st.plotly_chart(fig_wait_times, use_container_width=True)

# Bar chart for occupancy rates
fig_occupancy = px.bar(df, x='Date', y='Bed Occupancy Rate', title='Bed Occupancy Rates Over Time')
st.plotly_chart(fig_occupancy, use_container_width=True)

# Pie chart for patient demographics (using Department as a proxy for demographics)
fig_demographics = px.pie(df, names='Department', title='Patient Demographics by Department')
st.plotly_chart(fig_demographics, use_container_width=True)

# Table for upcoming appointments
st.header("Upcoming Appointments")
upcoming_appointments = df[['Date', 'Department', 'Physician']].sort_values('Date').head(10)
st.table(upcoming_appointments)

# Run this with `streamlit run your_script.py`