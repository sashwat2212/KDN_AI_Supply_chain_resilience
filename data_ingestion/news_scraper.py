import requests
import json
import os
from dotenv import load_dotenv
from newspaper import Article
import time

load_dotenv()
API_KEY = os.getenv("newsapi_api")

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

def extract_full_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None

def scrape_and_store_news():
    news_articles = fetch_news()
    
    extracted_articles = []
    for article in news_articles:
        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown Source")
        published_at = article.get("publishedAt", "No Date")
        url = article.get("url", "")

        if url:
            print(f"Extracting article: {title} from {source}")
            full_text = extract_full_article(url)
            time.sleep(2)  # To prevent rate limiting
        
            extracted_articles.append({
                "title": title,
                "source": source,
                "published_at": published_at,
                "url": url,
                "full_text": full_text
            })
    

    with open("extracted_news.json", "w", encoding="utf-8") as f:
        json.dump(extracted_articles, f, indent=4)
    
    print(f"Successfully saved {len(extracted_articles)} articles to extracted_news.json")


scrape_and_store_news()
