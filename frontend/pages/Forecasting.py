# import streamlit as st
# import requests
# import numpy as np

# st.title("LSTM Time-Series Prediction Dashboard")

# # User input for time-series data
# st.sidebar.header("Input Data")
# n_steps = st.sidebar.number_input("Number of Time Steps", min_value=1, max_value=50, value=10)

# data = []
# for i in range(n_steps):
#     values = st.sidebar.text_input(f"Step {i+1} (comma-separated)", "0.1,0.2,0.3,0.4")
#     try:
#         data.append([float(v) for v in values.split(",")])
#     except ValueError:
#         st.sidebar.warning("Invalid input format! Use comma-separated numbers.")

# if st.sidebar.button("Get Prediction"):
#     response = requests.post("http://127.0.0.1:8000/predict/", json={"input_data": data})
#     if response.status_code == 200:
#         prediction = response.json()["prediction"]
#         st.success(f"Prediction: {prediction}")
#     else:
#         st.error(f"Error: {response.json()['detail']}")




import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000/predict"

st.title("🌤 Weather Forecast Dashboard (LSTM-Based)")

# Sidebar for User Inputs
st.sidebar.header("Enter Weather Conditions")

temperature = st.sidebar.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
humidity = st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
precipitation = st.sidebar.number_input("Precipitation (mm)", min_value=0.0, max_value=100.0, value=5.0)
wind_speed = st.sidebar.number_input("Wind Speed (km/h)", min_value=0.0, max_value=200.0, value=10.0)

if st.sidebar.button("Predict Forecast"):
    # Prepare input data
    input_data = {"features": [temperature, humidity, precipitation, wind_speed]}
    
    try:
        # Send request to FastAPI
        response = requests.post(API_URL, json=input_data)
        forecast = response.json()["forecast"]

        # Convert forecast to a DataFrame
        df = pd.DataFrame([forecast])
        
        # Display forecasted values
        st.subheader("📊 Forecasted Weather Parameters")
        st.write(df)

        # Plot results
        fig = px.line(df.T, title="Forecasted Weather Trends", markers=True, labels={"index": "Parameter", "value": "Value"})
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error fetching forecast: {e}")

st.markdown("💡 This LSTM-based forecast predicts future weather conditions based on input parameters.")
