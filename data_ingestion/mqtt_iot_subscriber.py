# # # import paho.mqtt.client as mqtt
# # # import json
# # # import os

# # # # MQTT Configuration
# # # MQTT_BROKER = "localhost"
# # # MQTT_PORT = 1883
# # # MQTT_TOPIC = "supply_chain/iot_data"

# # # # Directory to save received data
# # # DATA_DIR = "iot_data"
# # # os.makedirs(DATA_DIR, exist_ok=True)

# # # DATA_FILE = os.path.join(DATA_DIR, "iot_sensor_data.json")

# # # def save_data(data):
# # #     try:
# # #         if os.path.exists(DATA_FILE):
# # #             with open(DATA_FILE, "r", encoding="utf-8") as f:
# # #                 existing_data = json.load(f)
# # #         else:
# # #             existing_data = []

# # #         existing_data.append(data)

# # #         with open(DATA_FILE, "w", encoding="utf-8") as f:
# # #             json.dump(existing_data, f, indent=4)
        
# # #         print(f" Data saved to {DATA_FILE}")

# # #     except Exception as e:
# # #         print(f"Error saving data: {e}")

# # # def on_connect(client, userdata, flags, reason_code, properties):
# # #     print(f"Connected to MQTT Broker with reason code {reason_code}")
# # #     client.subscribe(MQTT_TOPIC)

# # # def on_message(client, userdata, msg):
# # #     try:
# # #         data = json.loads(msg.payload.decode("utf-8"))
# # #         print(f"Received IoT Data: {data}")
# # #         save_data(data)
# # #     except Exception as e:
# # #         print(f"Error processing message: {e}")


# # # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# # # # Assign callbacks
# # # client.on_connect = on_connect
# # # client.on_message = on_message


# # # client.connect(MQTT_BROKER, MQTT_PORT, 60)
# # # client.loop_forever()


# # import paho.mqtt.client as mqtt
# # import json
# # import os

# # # MQTT Configuration
# # MQTT_BROKER = "localhost"
# # MQTT_PORT = 1883
# # MQTT_TOPIC = "supply_chain/cybersecurity_events"

# # # Directory to save received data
# # DATA_DIR = "cybersecurity_logs"
# # os.makedirs(DATA_DIR, exist_ok=True)

# # DATA_FILE = os.path.join(DATA_DIR, "cybersecurity_events.json")

# # def save_data(data):
# #     try:
# #         if os.path.exists(DATA_FILE):
# #             with open(DATA_FILE, "r", encoding="utf-8") as f:
# #                 existing_data = json.load(f)
# #         else:
# #             existing_data = []

# #         existing_data.append(data)

# #         with open(DATA_FILE, "w", encoding="utf-8") as f:
# #             json.dump(existing_data, f, indent=4)
        
# #         print(f" Data saved to {DATA_FILE}")

# #     except Exception as e:
# #         print(f"Error saving data: {e}")

# # def on_connect(client, userdata, flags, reason_code, properties):
# #     print(f"Connected to MQTT Broker with reason code {reason_code}")
# #     client.subscribe(MQTT_TOPIC)

# # def on_message(client, userdata, msg):
# #     try:
# #         data = json.loads(msg.payload.decode("utf-8"))
# #         print(f"Received Cybersecurity Event: {data}")

# #         # Save event
# #         save_data(data)

# #         # Alert if high-severity attack detected
# #         if data["severity"] == "high":
# #             print(f"🚨 ALERT: High-severity cybersecurity incident detected! {data}")

# #     except Exception as e:
# #         print(f"Error processing message: {e}")

# # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# # # Assign callbacks
# # client.on_connect = on_connect
# # client.on_message = on_message

# # client.connect(MQTT_BROKER, MQTT_PORT, 60)
# # client.loop_forever()


# import json
# import paho.mqtt.client as mqtt
# from py2neo import Graph

# # Connect to Neo4j
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sashwat@22"))

# # MQTT Broker Configuration
# MQTT_BROKER = "localhost"
# MQTT_PORT = 1883
# MQTT_TOPIC = "supply_chain/iot"

# def on_connect(client, userdata, flags, rc):
#     print(f"✅ Connected to MQTT broker with result code {rc}")
#     client.subscribe(MQTT_TOPIC)

# def on_message(client, userdata, msg):
#     """Process received MQTT message and store it in Neo4j"""
#     try:
#         payload = json.loads(msg.payload.decode("utf-8"))
#         truck_id = payload.get("truck_id")
#         motion = payload.get("motion")
#         location = payload.get("location")
#         timestamp = payload.get("timestamp")

#         query = """
#         MERGE (v:Vehicle {id: $truck_id})
#         SET v.motion = $motion, v.location = $location, v.timestamp = $timestamp
#         RETURN v
#         """
#         graph.run(query, truck_id=truck_id, motion=motion, location=str(location), timestamp=timestamp)

#         print(f"✅ Stored IoT data for {truck_id} in Neo4j")

#     except Exception as e:
#         print(f"Error processing message: {e}")

# # Start MQTT Client
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(MQTT_BROKER, MQTT_PORT, 60)
# client.loop_forever()



import paho.mqtt.client as mqtt
import sqlite3
import json



DB_PATH = "decision_making/iot_weather.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Modify the table schema to include precipitation
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        topic TEXT,
        temperature REAL,
        humidity REAL,
        wind_speed REAL,
        precipitation REAL
    )
""")
conn.commit()
conn.close()


# MQTT Callback Function
def on_message(client, userdata, message):
    payload = message.payload.decode()
    topic = message.topic
    print(f"Received IoT Data: {topic} -> {payload}")

    try:
        data = json.loads(payload)  # Convert JSON string to dictionary
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        wind_speed = data.get("wind_speed")
        precipitation = data.get("precipitation")  # NEW FIELD
    except json.JSONDecodeError:
        print("Error: Received invalid JSON payload.")
        return

    # Store in DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (topic, temperature, humidity, wind_speed, precipitation)
        VALUES (?, ?, ?, ?, ?)
    """, (topic, temperature, humidity, wind_speed, precipitation))
    conn.commit()
    conn.close()

# MQTT Client Setup
BROKER = "test.mosquitto.org"
TOPIC = "iot/sensor/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

print(f"Subscribed to topic: {TOPIC}")
client.loop_forever()