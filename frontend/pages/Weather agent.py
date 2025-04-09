import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Weather & IoT Dashboard", layout="wide")
st.title("AI-Powered Weather & Transport Agent")

# City selection
city = st.selectbox("Select a city:", ["New York", "London", "Tokyo", "Sydney", "Berlin"])

if st.button("Get Weather & AI Insights"):
    weather_response = requests.get(f"{BACKEND_URL}/weather/{city}")
    
    if weather_response.status_code == 200:
        weather_data = weather_response.json()["weather"]
        
        st.subheader("Current Weather")
        st.write(f"**Temperature:** {weather_data['current']['temp_c']}°C")
        st.write(f"**Condition:** {weather_data['current']['condition']['text']}")
        st.write(f"**Wind Speed:** {weather_data['current']['wind_kph']} kph")
        st.write(f"**Humidity:** {weather_data['current']['humidity']}%")
        
        # Fetch AI Recommendations
        ai_response = requests.get(f"{BACKEND_URL}/ai-recommendation/{city}")
        if ai_response.status_code == 200:
            ai_recommendation = ai_response.json()["recommendation"]
            st.subheader("AI Transportations Recommendations")
            st.write(ai_recommendation)
        else:
            st.error("Failed to fetch AI recommendations.")
    else:
        st.error("Failed to fetch weather data.")
