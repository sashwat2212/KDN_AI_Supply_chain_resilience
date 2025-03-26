import paho.mqtt.client as mqtt
import json
import os

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "supply_chain/iot_data"

# Directory to save received data
DATA_DIR = "iot_data"
os.makedirs(DATA_DIR, exist_ok=True)

DATA_FILE = os.path.join(DATA_DIR, "iot_sensor_data.json")

def save_data(data):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.append(data)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)
        
        print(f" Data saved to {DATA_FILE}")

    except Exception as e:
        print(f"Error saving data: {e}")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT Broker with reason code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        print(f"Received IoT Data: {data}")
        save_data(data)
    except Exception as e:
        print(f"Error processing message: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message


client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
