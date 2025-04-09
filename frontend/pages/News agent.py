import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000/classified-news"

st.set_page_config(page_title="Supply Chain Risk Dashboard", layout="wide")

st.title("📊 Supply Chain Risk Sentiment Analysis")

# Fetch classified news from API
st.sidebar.write("🔄 Refresh Data")
if st.sidebar.button("Fetch Latest News"):
    response = requests.get(API_URL)
    if response.status_code == 200:
        news_data = response.json()["news"]
        df = pd.DataFrame(news_data)
    else:
        st.error("Failed to fetch news. Check backend.")
else:
    df = pd.DataFrame()

if not df.empty:
    st.subheader("📰 Latest Classified News")
    st.dataframe(df[["title", "source", "published_at", "risk_type"]])

    # Risk Distribution Chart
    st.subheader("📊 Risk Type Distribution")
    fig = px.bar(df["risk_type"].value_counts(), x=df["risk_type"].value_counts().index, y=df["risk_type"].value_counts().values, title="Risk Classification Distribution", labels={"x": "Risk Type", "y": "Count"})
    st.plotly_chart(fig)
else:
    st.warning("Click 'Fetch Latest News' to load data.")
