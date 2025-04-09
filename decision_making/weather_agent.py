import streamlit as st
import requests
import ollama

# WeatherAPI Configuration
WEATHER_API_KEY = "de2eedce73364c49ba863535252303"  # Replace with your API key
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

# Function to fetch weather data
def get_weather(city):
    params = {"key": WEATHER_API_KEY, "q": city}
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to generate AI recommendations using Ollama
def get_ai_recommendation(weather_data):
    prompt = f"""
    Given the following weather conditions:
    - Location: {weather_data['location']['name']}, {weather_data['location']['country']}
    - Temperature: {weather_data['current']['temp_c']}°C
    - Condition: {weather_data['current']['condition']['text']}
    - Wind Speed: {weather_data['current']['wind_kph']} kph
    - Humidity: {weather_data['current']['humidity']}%
    
    Provide an assessment of the risks for transport and recommend alternative routes if necessary.
    """
    response = ollama.chat(model="deepseek-r1:14b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Streamlit UI
st.set_page_config(page_title="Weather & IoT Dashboard", layout="wide")
st.title("AI-Powered Weather & Transport Agent")

st.sidebar.title("Navigation")
st.sidebar.page_link("weather_agent.py", label="Weather Dashboard")
st.sidebar.page_link("iot_agent.py", label="IoT Sensor Data")

# City selection
city = st.selectbox("Select a city:", ["New York", "London", "Tokyo", "Sydney", "Berlin"])

if st.button("Get Weather & AI Insights"):
    weather_data = get_weather(city)
    if weather_data:
        st.subheader("Current Weather")
        st.write(f"**Temperature:** {weather_data['current']['temp_c']}°C")
        st.write(f"**Condition:** {weather_data['current']['condition']['text']}")
        st.write(f"**Wind Speed:** {weather_data['current']['wind_kph']} kph")
        st.write(f"**Humidity:** {weather_data['current']['humidity']}%")
        
        # AI Recommendations
        st.subheader("AI Transportations Recommendations")
        ai_recommendation = get_ai_recommendation(weather_data)
        st.write(ai_recommendation)
    else:
        st.error("Failed to fetch weather data. Please try again.")
