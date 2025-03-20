import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("newsapi_api")
#API_KEY = "ab04954cc9ee40138a713937dc4f235b"

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q=geopolitical OR cyber OR climate&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        return articles
    else:
        print(f"Error fetching news: {response.status_code}")
        return []


news_articles = fetch_news()
print(json.dumps(news_articles[:2], indent=2))  # Show first 2 articles
