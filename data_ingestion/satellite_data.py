import requests
import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NASA_API_KEY = os.getenv("NASA_API_KEY")
SENTINEL_CLIENT_ID = os.getenv("SENTINEL_CLIENT_ID")
SENTINEL_CLIENT_SECRET = os.getenv("SENTINEL_CLIENT_SECRET")

# Create directory for storing satellite data
os.makedirs("satellite_data", exist_ok=True)

# Load US grid bounding boxes from file
with open("us_grid_bboxes.json", "r") as f:
    us_bboxes = json.load(f)

# Fetch NASA climate data
def fetch_nasa_climate_data():
    climate_data = []
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    for bbox in us_bboxes:
        if isinstance(bbox, dict) and "bbox" in bbox:
            bbox = bbox["bbox"]

        if isinstance(bbox, list) and len(bbox) == 4:
            lat, lon = (bbox[1] + bbox[3]) / 2, (bbox[0] + bbox[2]) / 2
        else:
            print(f"[❌] Invalid BBox format: {bbox}")
            return  # Skip this location

        params = {
            "parameters": "T2M,RH2M,PRECTOT,WS10M",
            "community": "SB",
            "longitude": lon,
            "latitude": lat,
            "format": "JSON",
            "start": "20240101",
            "end": "20240301",
            "api_key": NASA_API_KEY
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            climate_data.append({"bbox": bbox, "climate_data": data})
            print(f"[✅] NASA Climate Data Saved for BBox {bbox}")
        else:
            print(f"[❌] NASA API Error {response.status_code} for BBox {bbox}: {response.text}")
    
    with open("satellite_data/nasa_climate_data.json", "w") as f:
        json.dump(climate_data, f, indent=4)
    
    print("[✅] All NASA Climate Data Saved!")

# Authenticate with Sentinel Hub API
def get_sentinel_access_token():
    response = requests.post("https://services.sentinel-hub.com/oauth/token", data={
        "grant_type": "client_credentials",
        "client_id": SENTINEL_CLIENT_ID,
        "client_secret": SENTINEL_CLIENT_SECRET
    })
    
    if response.status_code == 200:
        return response.json().get("access_token")
    
    print(f"[❌] Sentinel Hub Auth Error {response.status_code}: {response.text}")
    return None

# Fetch Sentinel-2 images
def fetch_sentinel_images():
    access_token = get_sentinel_access_token()
    if not access_token:
        return

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    for bbox_dict in us_bboxes:
        if isinstance(bbox_dict, dict) and "bbox" in bbox_dict:
            bbox = bbox_dict["bbox"]  # Extract only the list
        else:
            print(f"[❌] Invalid BBox format: {bbox_dict}")
            continue  # Skip this bbox

        payload = {
            "input": {
                "bounds": {"bbox": bbox, "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}},
                "data": [{
                    "type": "S2L2A",
                    "dataFilter": {"timeRange": {"from": "2024-03-01T00:00:00Z", "to": "2024-03-19T23:59:59Z"}}
                }]
            },
            "evalscript": """
            function setup() {
                return { input: ["B08", "B04", "B03", "B02", "B11"], output: [{ id: "NDVI", bands: 1 }, { id: "NDWI", bands: 1 }] };
            }
            function evaluatePixel(sample) {
                return { NDVI: [(sample.B08 - sample.B04) / (sample.B08 + sample.B04)], NDWI: [(sample.B03 - sample.B11) / (sample.B03 + sample.B11)] };
            }
            """,
            "output": {
                "width": 512, "height": 512,
                "responses": [{"identifier": "NDVI", "format": {"type": "image/png"}}, {"identifier": "NDWI", "format": {"type": "image/png"}}]
            }
        }
        
        response = requests.post("https://services.sentinel-hub.com/api/v1/process", headers=headers, json=payload)
        
        if response.status_code == 200:
            file_path = f"satellite_data/bbox_{us_bboxes.index(bbox_dict)}_NDVI.png"
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"[✅] Sentinel NDVI & NDWI Image Saved for BBox {bbox}")
        else:
            print(f"[❌] Sentinel API Error {response.status_code} for BBox {bbox}: {response.text}")


# Save results in JSON
def save_results():
    results = [{
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "bbox": bbox,
        "ndvi_image": f"satellite_data/bbox_{us_bboxes.index(bbox)}_NDVI.png",
        "ndwi_image": f"satellite_data/bbox_{us_bboxes.index(bbox)}_NDWI.png"
    } for bbox in us_bboxes]
    
    with open("satellite_data/us_risk_data.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("[✅] US Risk Data Saved!")

# Execute functions
fetch_nasa_climate_data()
fetch_sentinel_images()
save_results()
