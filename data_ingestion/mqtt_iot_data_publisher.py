# # import paho.mqtt.client as mqtt
# # import json
# # import random
# # import time
# # from geopy.geocoders import Nominatim

# # # MQTT Configuration
# # BROKER = "localhost"
# # PORT = 1883
# # TOPIC = "supply_chain/iot_data"

# # # Define US bounding box
# # lat_min, lat_max = 24.5, 49.5   # US latitude range
# # lon_min, lon_max = -125, -66    # US longitude range
# # lat_step = 2.5  # Grid resolution
# # lon_step = 2.5

# # # Geolocation setup
# # geolocator = Nominatim(user_agent="supply_chain_ai")

# # def get_location(lat, lon):
# #     try:
# #         location = geolocator.reverse((lat, lon), exactly_one=True)
# #         if location and location.raw:
# #             address = location.raw.get("address", {})
# #             return {
# #                 "city": address.get("city", address.get("town", "Unknown")),
# #                 "state": address.get("state", "Unknown"),
# #                 "country": address.get("country", "Unknown"),
# #             }
# #     except Exception as e:
# #         print(f"Geocoding error: {e}")
# #     return {"city": "Unknown", "state": "Unknown", "country": "Unknown"}

# # def generate_sensor_data(lat_range, lon_range):
# #     latitude = round(random.uniform(lat_range[0], lat_range[1]), 6)
# #     longitude = round(random.uniform(lon_range[0], lon_range[1]), 6)
    
# #     location_info = get_location(latitude, longitude)
    
# #     data = {
# #         "device_id": f"sensor_{latitude}_{longitude}",
# #         "temperature": round(random.uniform(-10, 40), 2),
# #         "road_condition": random.choice(["clear", "wet", "icy", "blocked"]),
# #         "noise_level": round(random.uniform(30, 100), 2),
# #         "latitude": latitude,
# #         "longitude": longitude,
# #         **location_info,
# #         "timestamp": time.time()
# #     }
# #     return data

# # def publish_sensor_data():
# #     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# #     client.connect(BROKER, PORT, 60)

# #     while True:
# #         for lat in range(int(lat_min * 10), int(lat_max * 10), int(lat_step * 10)):
# #             for lon in range(int(lon_min * 10), int(lon_max * 10), int(lon_step * 10)):
# #                 lat_range = (lat / 10, (lat / 10) + lat_step)
# #                 lon_range = (lon / 10, (lon / 10) + lon_step)
                
# #                 sensor_data = generate_sensor_data(lat_range, lon_range)
# #                 payload = json.dumps(sensor_data)
# #                 client.publish(TOPIC, payload)
# #                 print(f"Published: {payload}")
# #                 time.sleep(5)  # Wait 5 sec before next box

# # if __name__ == "__main__":
# #     publish_sensor_data()


# # import paho.mqtt.client as mqtt
# # import json
# # import random
# # import time
# # from datetime import datetime

# # # MQTT Configuration
# # BROKER = "localhost"
# # PORT = 1883
# # TOPIC = "supply_chain/cybersecurity_events"

# # # Cybersecurity Events
# # CYBER_EVENTS = [
# #     "unauthorized_access",
# #     "DDoS_attack",
# #     "malware_detected",
# #     "phishing_attempt",
# #     "data_breach",
# #     "ransomware_attack",
# #     "network_intrusion",
# # ]

# # SEVERITY_LEVELS = ["low", "medium", "high"]

# # def generate_cyber_event():
# #     """Generate a simulated cybersecurity event log."""
# #     event = {
# #         "device_id": f"sensor_{random.randint(1000, 9999)}",
# #         "event_type": random.choice(CYBER_EVENTS),
# #         "severity": random.choice(SEVERITY_LEVELS),
# #         "affected_system": random.choice(["SCADA", "ERP", "Warehouse_Server", "Router"]),
# #         "timestamp": datetime.utcnow().isoformat(),
# #         "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
# #     }
# #     return event

# # def publish_cyber_events():
# #     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# #     client.connect(BROKER, PORT, 60)

# #     while True:
# #         cyber_event = generate_cyber_event()
# #         payload = json.dumps(cyber_event)
# #         client.publish(TOPIC, payload)
# #         print(f"Published Cybersecurity Event: {payload}")
# #         time.sleep(2)  # Send event every 2 seconds

# # if __name__ == "__main__":
# #     publish_cyber_events()


# # import json
# # import paho.mqtt.client as mqtt
# # import time
# # import random

# # # MQTT Broker Configuration
# # MQTT_BROKER = "localhost"  # Change this if using a remote broker
# # MQTT_PORT = 1883
# # MQTT_TOPIC = "supply_chain/iot"

# # # Create MQTT Client
# # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# # client.connect(MQTT_BROKER, MQTT_PORT, 60)

# # def publish_iot_data():
# #     """Publish real or simulated IoT sensor data."""
# #     truck_ids = ["T101", "T102", "T103", "T104", "T105"]
# #     locations = ["Berlin", "London", "New York", "Mumbai", "Shanghai"]

# #     while True:
# #         # Simulated sensor data (Replace with actual sensor readings)
# #         data = {
# #             "truck_id": random.choice(truck_ids),
# #             "delayed": random.choice([True, False]),
# #             "location": random.choice(locations),
# #             "ETA": time.strftime("%Y-%m-%d %H:%M:%S")
# #         }

# #         # Convert to JSON and publish
# #         payload = json.dumps(data)
# #         client.publish(MQTT_TOPIC, payload)
# #         print(f"📡 Published: {payload}")

# #         time.sleep(5)  # Adjust interval as needed

# # # Run Publisher
# # if __name__ == "__main__":
# #     try:
# #         print("🚚 IoT Data Publisher Started...")
# #         publish_iot_data()
# #     except KeyboardInterrupt:
# #         print("❌ Publisher Stopped.")
# #         client.disconnect()



# import json
# import time
# import paho.mqtt.client as mqtt
# from gpsdclient import GPSDClient

# # MQTT Configuration
# MQTT_BROKER = "localhost"
# MQTT_PORT = 1883
# MQTT_TOPIC = "supply_chain/iot"

# # Function to get GPS data
# def get_gps_data():
#     with GPSDClient(host="127.0.0.1") as client:
#         for result in client.dict_stream(filter=["TPV"]):
#             if "lat" in result and "lon" in result:
#                 return {"latitude": result["lat"], "longitude": result["lon"]}
#             time.sleep(1)

# # Initialize MQTT Publisher
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# client.connect(MQTT_BROKER, MQTT_PORT, 60)

# while True:
#     try:
#         gps_data = get_gps_data()
        
#         if gps_data:
#             iot_data = {
#                 "truck_id": "T123",
#                 "location": gps_data,
#                 "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#             }

#             client.publish(MQTT_TOPIC, json.dumps(iot_data))
#             print(f"📡 Published: {iot_data}")
        
#         time.sleep(5)  # Adjust frequency

#     except Exception as e:
#         print(f"Error: {e}")
#         time.sleep(5)




# import paho.mqtt.client as mqtt
# import json
# import time

# # MQTT Configuration
# MQTT_BROKER = "test.mosquitto.org"
# MQTT_PORT = 1883
# MQTT_TOPIC = "iot/sensor/data"

# # Initialize MQTT client
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# client.connect(MQTT_BROKER, MQTT_PORT, 60)

# # Simulated IoT sensor data
# def publish_mock_data():
#     while True:
#         sensor_data = {
#             "temperature": round(20 + (5 * (0.5 - time.time() % 1)), 2),
#             "humidity": round(50 + (10 * (0.5 - time.time() % 1)), 2),
#             "wind_speed": round(10 + (2 * (0.5 - time.time() % 1)), 2),
#             "timestamp": time.time()
#         }
#         payload = json.dumps(sensor_data)
#         client.publish(MQTT_TOPIC, payload)
#         print(f"Published: {payload}")
#         time.sleep(5)  # Send data every 5 seconds

# publish_mock_data()


import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPICS = ["iot/weather/temperature", "iot/weather/humidity", "iot/weather/wind_speed", "iot/environment/air_quality", "iot/sensors/light_intensity", "iot/weather/precipitation"]

def on_message(client, userdata, message):
    print(f"{message.topic}: {message.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, 1883, 60)

for topic in TOPICS:
    client.subscribe(topic)

print("Subscribed to IoT Weather & Environment Topics")
client.loop_forever()
