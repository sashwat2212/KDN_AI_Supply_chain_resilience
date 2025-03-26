import pandas as pd
import json
import os

# Function to load JSON data
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Function to save DataFrame as CSV
def save_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f" Data saved to {file_path}")


news_json_path = "extracted_news.json"
news_csv_path = "extracted_news.csv"

if os.path.exists(news_json_path):
    news_data = load_json(news_json_path)
    save_csv(news_data, news_csv_path)


us_risk_json_path = "satellite_data/us_risk_data.json"
us_risk_csv_path = "satellite_data/us_risk_data.csv"

if os.path.exists(us_risk_json_path):
    us_risk_data = load_json(us_risk_json_path)
    save_csv(us_risk_data, us_risk_csv_path)


nasa_climate_json_path = "satellite_data/nasa_climate_data.json"
nasa_climate_csv_path = "satellite_data/nasa_climate_data.csv"

if os.path.exists(nasa_climate_json_path):
    climate_data = load_json(nasa_climate_json_path)


    rows = []
    for entry in climate_data:
        bbox = entry["bbox"]
        climate_info = entry["climate_data"]["properties"]["parameter"]

        for date, temp in climate_info["T2M"].items():
            row = {
                "Date": date,
                "BBox": bbox,
                "Temperature (°C)": temp,
                "Humidity (%)": climate_info["RH2M"].get(date, None),
                "Precipitation (mm)": climate_info.get("PRECTOTCORR", {}).get(date, None),
                "Wind Speed (m/s)": climate_info["WS10M"].get(date, None),
            }
            rows.append(row)

    save_csv(rows, nasa_climate_csv_path)
