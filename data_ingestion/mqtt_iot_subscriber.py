import paho.mqtt.client as mqtt
import json

# MQTT Broker Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "supply_chain/iot_data"

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT Broker with reason code {reason_code}")
    client.subscribe(MQTT_TOPIC)

# Callback when a message is received
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        print(f"Received IoT Data: {data}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Create MQTT client using version 2 API
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()