import pandas as pd
import ast  # To safely convert string list to Python list
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from tqdm import tqdm

# Initialize Geolocator
geolocator = Nominatim(user_agent="geo_bbox_locator")

def get_location(bbox_str):
    try:
        
        bbox = ast.literal_eval(bbox_str)
        if len(bbox) != 4:
            return "Invalid BBox Format"

        min_lon, min_lat, max_lon, max_lat = bbox
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        location = geolocator.reverse((center_lat, center_lon), exactly_one=True)
        return location.address if location else "Unknown Location"
    
    except GeocoderTimedOut:
        return "Timeout Error"
    except Exception as e:
        return f"Error: {e}"


input_file = "/Users/kdn_aisashwat/Desktop/supply_chain_resillience/satellite_data/nasa_climate_data.csv"   # Replace with your filename
output_file = "updated_locations.csv"

df = pd.read_csv(input_file)

# Check if bbox column exists
if "BBox" in df.columns:
    tqdm.pandas()  # progress bar
    df["location"] = df["BBox"].progress_apply(get_location)

    # Save the updated CSV
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved as {output_file}")
else:
    print("Error: CSV must contain a 'bbox' column.")

