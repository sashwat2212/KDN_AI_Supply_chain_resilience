# import streamlit as st
# import sqlite3
# import pandas as pd
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Database configuration
# DB_PATH = "/Users/kdn_aisashwat/Desktop/supply_chain_resillience/decision_making/iot_weather.db"

# # Function to fetch sensor data from the database
# def fetch_sensor_data():
#     conn = sqlite3.connect(DB_PATH)
#     query = "SELECT timestamp, topic, temperature, humidity, wind_speed FROM sensor_data ORDER BY timestamp DESC LIMIT 50"
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# # Function to determine travel safety
# def get_travel_advisory(temp, humidity, wind_speed):
#     advisory = "Safe to Travel ✅"
    
#     if temp < -5 or temp > 40:
#         advisory = "Extreme temperature! Travel not recommended ❌"
#     elif humidity > 85:
#         advisory = "High humidity! Expect discomfort while traveling ⚠️"
#     elif wind_speed > 50:
#         advisory = "Strong winds detected! Avoid travel ❌"

#     return advisory

# # Streamlit UI
# st.title("IoT Sensor Data Dashboard & Travel Advisory")

# # Fetch data
# data = fetch_sensor_data()

# data = fetch_sensor_data()

# if not data.empty:
#     st.subheader("Latest Sensor Readings")
#     st.dataframe(data)

#     # **1. Temperature Trend (Line Chart)**
#     st.subheader("Temperature Trend")
#     fig, ax = plt.subplots()
#     sns.lineplot(x=data["timestamp"], y=data["temperature"], marker="o", ax=ax)
#     ax.set_xticks(range(0, len(data["timestamp"]), max(1, len(data)//10)))  # Set fewer ticks
#     ax.set_xticklabels(data["timestamp"][::max(1, len(data)//10)], rotation=45, ha="right")
#     ax.set_ylabel("Temperature (°C)")
#     ax.set_xlabel("Timestamp")
#     st.pyplot(fig)

#     # **2. Humidity Levels (Bar Chart)**
#     st.subheader("Humidity Levels")
#     fig, ax = plt.subplots()
#     sns.barplot(x=data["timestamp"], y=data["humidity"], ax=ax, color="blue")
#     ax.set_xticks(range(0, len(data["timestamp"]), max(1, len(data)//10)))  
#     ax.set_xticklabels(data["timestamp"][::max(1, len(data)//10)], rotation=45, ha="right")
#     ax.set_ylabel("Humidity (%)")
#     ax.set_xlabel("Timestamp")
#     st.pyplot(fig)

#     # **3. Wind Speed Analysis (Threshold-based Coloring)**
#     st.subheader("Wind Speed Analysis")
#     fig, ax = plt.subplots()
#     sns.barplot(x=data["timestamp"], y=data["wind_speed"], hue=data["timestamp"], legend=False, ax=ax, palette="coolwarm")
#     ax.set_xticks(range(0, len(data["timestamp"]), max(1, len(data)//10)))  
#     ax.set_xticklabels(data["timestamp"][::max(1, len(data)//10)], rotation=45, ha="right")
#     ax.set_ylabel("Wind Speed (kph)")
#     ax.set_xlabel("Timestamp")
#     st.pyplot(fig)

#     # **4. Travel Advisory Based on Latest Data**
#     st.subheader("AI-Powered Travel Advisory 🚀")
#     latest_data = data.iloc[0]  # Get latest entry
#     advisory = get_travel_advisory(latest_data["temperature"], latest_data["humidity"], latest_data["wind_speed"])
    
#     # Display advisory in colored text
#     if "not recommended" in advisory or "Avoid" in advisory:
#         st.error(advisory)
#     elif "⚠️" in advisory:
#         st.warning(advisory)
#     else:
#         st.success(advisory)

# else:
#     st.warning("No sensor data available.")



import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Database configuration
DB_PATH = "/Users/kdn_aisashwat/Desktop/supply_chain_resillience/decision_making/iot_weather.db"

# Function to fetch sensor data from the database with caching
@st.cache_data(ttl=60)
def fetch_sensor_data():
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT timestamp, topic, temperature, humidity, wind_speed FROM sensor_data ORDER BY timestamp DESC LIMIT 50"
        df = pd.read_sql_query(query, conn)
    df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime
    return df

# Function to determine travel safety
def get_travel_advisory(temp, humidity, wind_speed):
    advisory = "Safe to Travel ✅"
    reasons = []
    
    if temp < -5 or temp > 40:
        advisory = "Extreme temperature! Travel not recommended ❌"
        reasons.append(f"Temperature: {temp}°C")
    if humidity > 85:
        advisory = "High humidity! Expect discomfort while traveling ⚠️"
        reasons.append(f"Humidity: {humidity}%")
    if wind_speed > 50:
        advisory = "Strong winds detected! Avoid travel ❌"
        reasons.append(f"Wind Speed: {wind_speed} kph")
    
    return advisory, reasons

# Streamlit UI
st.set_page_config(page_title="IoT Sensor Dashboard", layout="wide")
st.title("🌍 IoT Sensor Data Dashboard & Travel Advisory")

# Fetch data
data = fetch_sensor_data()

if not data.empty:
    # Sidebar Filters
    st.sidebar.header("Filter Data")
    num_records = st.sidebar.slider("Number of Records", min_value=10, max_value=50, value=30)
    data = data.head(num_records)
    
    st.subheader("Latest Sensor Readings")
    st.dataframe(data)
    
    # **1. Temperature Trend**
    st.subheader("📈 Temperature Trend")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(x=data["timestamp"], y=data["temperature"], marker="o", ax=ax, linewidth=2, color='red')
    ax.set_xticklabels(data["timestamp"].dt.strftime("%H:%M:%S"), rotation=45, ha="right")
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Timestamp")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    
    # **2. Humidity Levels**
    st.subheader("💧 Humidity Levels")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=data["timestamp"], y=data["humidity"], ax=ax, color="blue", saturation=0.7)
    ax.set_xticklabels(data["timestamp"].dt.strftime("%H:%M:%S"), rotation=45, ha="right")
    ax.set_ylabel("Humidity (%)")
    ax.set_xlabel("Timestamp")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    
    # **3. Wind Speed Analysis**
    st.subheader("💨 Wind Speed Analysis")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=data["timestamp"], y=data["wind_speed"], ax=ax, palette="coolwarm", dodge=False, edgecolor="black")
    ax.set_xticklabels(data["timestamp"].dt.strftime("%H:%M:%S"), rotation=45, ha="right")
    ax.set_ylabel("Wind Speed (kph)")
    ax.set_xlabel("Timestamp")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    
    # **4. Travel Advisory**
    st.subheader("🚦 AI-Powered Travel Advisory")
    latest_data = data.iloc[0]
    advisory, reasons = get_travel_advisory(latest_data["temperature"], latest_data["humidity"], latest_data["wind_speed"])
    
    if "not recommended" in advisory or "Avoid" in advisory:
        st.error(advisory)
    elif "⚠️" in advisory:
        st.warning(advisory)
    else:
        st.success(advisory)
    
    # Show individual factors
    for reason in reasons:
        st.write(f"- {reason}")
    
else:
    st.warning("No sensor data available.")