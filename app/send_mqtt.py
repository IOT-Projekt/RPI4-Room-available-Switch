import os
import time
import json
import paho.mqtt.client as mqtt
from button_data import is_button_pressed

# MQTT Configuration

DEFAULT_BROKER = "localhost"
DEFAULT_PORT = 1883
DEFAULT_TOPIC_BUTTON = "iot/devices/room_status"
DEFAULT_USERNAME = None
DEFAULT_PASSWORD = None
SEND_MQTT_INTERVAL = 1  # Send button data every second

BROKER = os.getenv("BROKER_IP", DEFAULT_BROKER)
PORT = int(os.getenv("BROKER_PORT", DEFAULT_PORT))
TOPIC_BUTTON = os.getenv("TOPIC_BUTTON", DEFAULT_TOPIC_BUTTON)
MQTT_USERNAME = os.getenv("MQTT_USERNAME", DEFAULT_USERNAME)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", DEFAULT_PASSWORD)
CLIENT_ID = os.getenv("CLIENT_ID", "button-sensor")

# Initialize MQTT client
client = mqtt.Client()
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

def send_mqtt(button_state):
    """
    Sends the button state to the MQTT broker.
    """
    if button_state is None:
        return

    # Prepare payload
    payload = json.dumps({
        "source": "mqtt",
        "device_id": CLIENT_ID,
        "button_pressed": button_state,
        "timestamp": time.time()
    })

    # Publish to MQTT broker
    client.publish(TOPIC_BUTTON, payload)
    print(f"Button state sent: {payload}")

if __name__ == "__main__":
    try:
        while True:
            button_state = is_button_pressed()
            send_mqtt(button_state)
            time.sleep(0.1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        client.disconnect()
