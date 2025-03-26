import paho.mqtt.client as mqtt
import json
import random
import time
from geopy.geocoders import Nominatim

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "supply_chain/iot_data"

# Define US bounding box
lat_min, lat_max = 24.5, 49.5   # US latitude range
lon_min, lon_max = -125, -66    # US longitude range
lat_step = 2.5  # Grid resolution
lon_step = 2.5

# Geolocation setup
geolocator = Nominatim(user_agent="supply_chain_ai")

def get_location(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location and location.raw:
            address = location.raw.get("address", {})
            return {
                "city": address.get("city", address.get("town", "Unknown")),
                "state": address.get("state", "Unknown"),
                "country": address.get("country", "Unknown"),
            }
    except Exception as e:
        print(f"Geocoding error: {e}")
    return {"city": "Unknown", "state": "Unknown", "country": "Unknown"}

def generate_sensor_data(lat_range, lon_range):
    latitude = round(random.uniform(lat_range[0], lat_range[1]), 6)
    longitude = round(random.uniform(lon_range[0], lon_range[1]), 6)
    
    location_info = get_location(latitude, longitude)
    
    data = {
        "device_id": f"sensor_{latitude}_{longitude}",
        "temperature": round(random.uniform(-10, 40), 2),
        "road_condition": random.choice(["clear", "wet", "icy", "blocked"]),
        "noise_level": round(random.uniform(30, 100), 2),
        "latitude": latitude,
        "longitude": longitude,
        **location_info,
        "timestamp": time.time()
    }
    return data

def publish_sensor_data():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT, 60)

    while True:
        for lat in range(int(lat_min * 10), int(lat_max * 10), int(lat_step * 10)):
            for lon in range(int(lon_min * 10), int(lon_max * 10), int(lon_step * 10)):
                lat_range = (lat / 10, (lat / 10) + lat_step)
                lon_range = (lon / 10, (lon / 10) + lon_step)
                
                sensor_data = generate_sensor_data(lat_range, lon_range)
                payload = json.dumps(sensor_data)
                client.publish(TOPIC, payload)
                print(f"Published: {payload}")
                time.sleep(5)  # Wait 5 sec before next box

if __name__ == "__main__":
    publish_sensor_data()
