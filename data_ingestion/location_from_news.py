from transformers import pipeline
from geopy.geocoders import Nominatim
import json
import re

# Load Hugging Face NER model
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
geolocator = Nominatim(user_agent="geo_extractor")

def extract_location(text):
    """Extract and reconstruct locations using Hugging Face NER with proper token merging."""
    if not text:
        return None

    ner_results = ner_pipeline(text)
    locations = []
    current_location = ""

    for token in ner_results:
        word = token["word"].replace("##", "")  # Remove subword token artifacts

        if token["entity"] == "B-LOC":  # Start of a new location
            if current_location:
                locations.append(current_location.strip())  # Store previous location
            current_location = word
        elif token["entity"] == "I-LOC":  # Continuation of a location
            current_location += " " + word

    if current_location:
        locations.append(current_location.strip())  # Append the last detected location

    # Remove duplicates and return the first valid location
    unique_locations = list(dict.fromkeys(locations))  # Removes duplicates while keeping order
    return unique_locations[0] if unique_locations else None  # Return only the first valid location

def geocode_location(location):
    """Convert location name to latitude & longitude"""
    if not location:
        return None

    try:
        geocode = geolocator.geocode(location)
        if geocode:
            return {"name": location, "latitude": geocode.latitude, "longitude": geocode.longitude}
        else:
            print(f"⚠️ Geocoding failed for: {location}")
    except Exception as e:
        print(f"❌ Geocoding error for {location}: {e}")

    return None

def process_news_with_location():
    """Process news articles and extract locations"""
    with open("processed_news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)

    updated_articles = []
    for article in news_data:
        full_text = article.get("full_text", "") or ""
        title = article.get("title", "") or ""
        combined_text = full_text + " " + title  # Ensure non-empty text

        location_name = extract_location(combined_text)

        if location_name:
            print(f"📍 Extracted Location: {location_name}")  # Debugging output
            geo_data = geocode_location(location_name)
            if geo_data:
                article["location"] = geo_data
            else:
                article["location"] = {"name": location_name, "latitude": None, "longitude": None}
        else:
            print("⚠️ No location detected, setting to 'Unknown'")
            article["location"] = {"name": "Unknown", "latitude": None, "longitude": None}

        updated_articles.append(article)

    with open("news_with_locations.json", "w", encoding="utf-8") as f:
        json.dump(updated_articles, f, indent=4)

    print("✅ News articles updated with locations!")

# Run processing
process_news_with_location()
