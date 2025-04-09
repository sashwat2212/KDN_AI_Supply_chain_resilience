import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")


def get_weather(city):
    params = {"key": WEATHER_API_KEY, "q": city}
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None
