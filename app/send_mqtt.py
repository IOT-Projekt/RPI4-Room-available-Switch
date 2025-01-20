# File: send_button_state.py
# Description: Sends the button toggled state via MQTT, only if it changes.

import os
import time
import json
import paho.mqtt.client as mqtt
from button_data import get_button_state  # Import the function from read_button.py

# MQTT Configuration
DEFAULT_BROKER = "localhost"
DEFAULT_PORT = 1883
DEFAULT_TOPIC_BUTTON = "iot/devices/room_status"
DEFAULT_USERNAME = None
DEFAULT_PASSWORD = None

BROKER = os.getenv("BROKER_IP", DEFAULT_BROKER)
PORT = int(os.getenv("BROKER_PORT", DEFAULT_PORT))
TOPIC_BUTTON = os.getenv("TOPIC_BUTTON", DEFAULT_TOPIC_BUTTON)
MQTT_USERNAME = os.getenv("MQTT_USERNAME", DEFAULT_USERNAME)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", DEFAULT_PASSWORD)
CLIENT_ID = os.getenv("CLIENT_ID", "button-sensor")

# Initialize MQTT client
client = mqtt.Client(CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
    else:
        print(f"Failed to connect. Code: {rc}")

def on_publish(client, userdata, mid):
    print(f"Message with ID {mid} published")

client.on_connect = on_connect
client.on_publish = on_publish

# Connect to MQTT broker
client.connect(BROKER, PORT, keepalive=60)

# Initialize the previous state variable
last_sent_state = None

def send_mqtt(button_state):
    """
    Sends the button toggled state to the MQTT broker.
    """
    # Prepare payload
    payload = json.dumps({
        "source": "mqtt",
        "device_id": CLIENT_ID,
        "button_toggled": button_state,
        "timestamp": time.time()
    })

    # Publish to MQTT broker
    client.publish(TOPIC_BUTTON, payload)
    print(f"Button state sent: {payload}")

if __name__ == "__main__":
    try:
        while True:
            # Get the current button state
            button_state = get_button_state()

            # Send MQTT message only if the state has changed
            if button_state != last_sent_state:
                send_mqtt(button_state)
                last_sent_state = button_state

            # Polling delay
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        client.disconnect()
