# import requests
# import json
# import os
# import time
# from dotenv import load_dotenv
# from newspaper import Article
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# load_dotenv()
# API_KEY = os.getenv("newsapi_api")
# analyzer = SentimentIntensityAnalyzer()

# # Define risk categories based on keywords
# RISK_CATEGORIES = {
#     "geopolitical": ["war", "conflict", "sanctions", "political", "trade"],
#     "cyber": ["cyberattack", "hacking", "data breach", "malware", "ransomware"],
#     "climate": ["storm", "flood", "hurricane", "wildfire", "drought"]
# }

# def fetch_news():
#     """Fetch news articles from NewsAPI related to supply chain risks."""
#     url = f"https://newsapi.org/v2/everything?q=geopolitical OR cyber OR climate&language=en&sortBy=publishedAt&apiKey={API_KEY}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         news_data = response.json()
#         return news_data.get("articles", [])
#     else:
#         print(f"Error fetching news: {response.status_code}")
#         return []

# def extract_full_article(url):
#     """Extract full text from the article URL."""
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         return article.text
#     except Exception as e:
#         print(f"Error extracting article from {url}: {e}")
#         return None

# def categorize_article(title, content):
#     """Categorize article into geopolitical, cyber, or climate risk based on keywords."""
#     text = (title + " " + content).lower()
#     for category, keywords in RISK_CATEGORIES.items():
#         if any(keyword in text for keyword in keywords):
#             return category
#     return "uncategorized"

# def analyze_sentiment(text):
#     """Analyze sentiment to determine risk severity (-1 to +1)."""
#     sentiment_score = analyzer.polarity_scores(text)["compound"]
#     return sentiment_score

# def scrape_and_store_news():
#     """Fetch, extract, analyze, and store news data."""
#     news_articles = fetch_news()
    
#     processed_articles = []
#     for article in news_articles:
#         title = article.get("title", "No Title")
#         source = article.get("source", {}).get("name", "Unknown Source")
#         published_at = article.get("publishedAt", "No Date")
#         url = article.get("url", "")

#         if url:
#             print(f"Extracting: {title} from {source}")
#             full_text = extract_full_article(url)
#             time.sleep(2)  # Prevent rate limiting
            
#             if full_text:
#                 category = categorize_article(title, full_text)
#                 severity_score = analyze_sentiment(full_text)

#                 processed_articles.append({
#                     "title": title,
#                     "source": source,
#                     "published_at": published_at,
#                     "url": url,
#                     "category": category,
#                     "severity_score": severity_score,
#                     "full_text": full_text
#                 })

#     # Save to JSON
#     with open("processed_news.json", "w", encoding="utf-8") as f:
#         json.dump(processed_articles, f, indent=4)
    
#     print(f"Saved {len(processed_articles)} processed articles to processed_news.json")

# if __name__ == "__main__":
#     scrape_and_store_news()

import requests
import os
import time
from dotenv import load_dotenv
from newspaper import Article
from news_processing import classify_news

load_dotenv()
API_KEY = os.getenv("newsapi_api")

def fetch_news():
    """Fetch news articles from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q=geopolitical OR cyber OR climate&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

def extract_full_article(url):
    """Extract full content using newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception:
        return None

def scrape_and_classify_news():
    """Fetch, extract, classify news articles."""
    news_articles = fetch_news()
    processed_articles = []
    
    for article in news_articles[:10]:  # Limit to 10 articles per run
        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown Source")
        url = article.get("url", "")
        published_at = article.get("publishedAt", "No Date")

        full_text = extract_full_article(url)
        time.sleep(2)  # Avoid rate limiting

        risk_type = classify_news(title, full_text)
        
        processed_articles.append({
            "title": title,
            "source": source,
            "published_at": published_at,
            "url": url,
            "full_text": full_text,
            "risk_type": risk_type
        })
    
    return processed_articles


# from py2neo import Graph, Node, Relationship
# import json

# # Connect to Neo4j
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sashwat@22"))

# def load_news_with_locations(file_path="news_with_locations.json"):
#     """Load news articles with extracted locations."""
#     with open("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/news_with_locations.json", "r", encoding="utf-8") as f:
#         return json.load(f)

# def insert_news_with_locations(news_data):
#     """Insert news articles and locations into Neo4j."""
#     for article in news_data:
#         title = article["title"]
#         category = article["category"]
#         severity = article["severity_score"]
#         timestamp = article["published_at"]
#         source = article["source"]
#         url = article["url"]
#         location_name = article["location"]["name"]
#         latitude = article["location"]["latitude"]
#         longitude = article["location"]["longitude"]

#         # Create RiskEvent node
#         risk_event = Node("RiskEvent",
#                           title=title,
#                           type=category.capitalize(),
#                           severity=severity,
#                           timestamp=timestamp,
#                           source=source,
#                           url=url)
#         graph.create(risk_event)

#         # Create Location node
#         if location_name and location_name != "Unknown":
#             location_node = Node("Location",
#                                  name=location_name,
#                                  latitude=latitude,
#                                  longitude=longitude)
#             graph.merge(location_node, "Location", "name")

#             # Link RiskEvent to Location
#             graph.create(Relationship(risk_event, "OCCURRED_AT", location_node))

#         print(f"Inserted: {title} ({category}) - Location: {location_name}")

# # Load and insert into Neo4j
# news_data = load_news_with_locations()
# insert_news_with_locations(news_data)

# print("✅ News Data with Locations Ingested into Neo4j!")
