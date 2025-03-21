import paho.mqtt.client as mqtt
import json
import random
import time
from geopy.geocoders import Nominatim

BROKER = "localhost"
PORT = 1883
TOPIC = "sensor/data"

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

def generate_sensor_data():
    latitude = round(random.uniform(40.5, 41.0), 6)
    longitude = round(random.uniform(-74.2, -73.7), 6)
    
    location_info = get_location(latitude, longitude)
    
    data = {
        "device_id": "sensor_42",
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
        sensor_data = generate_sensor_data()
        payload = json.dumps(sensor_data)
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()