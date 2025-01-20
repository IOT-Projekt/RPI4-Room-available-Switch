import os
import json
import time
import paho.mqtt.client as mqtt
from button_data import read_button

# MQTT Configuration
DEFAULT_BROKER = "localhost"
DEFAULT_PORT = 1883
DEFAULT_TOPIC_BUTTON = "iot/devices/button"
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
client.loop_start()  # Start MQTT communication in the background

def send_mqtt(data):
    """
    Sends button data to the MQTT broker.
    Args:
        data (dict): The button state data. Example:
                     {
                         "pressed": True,  # True if pressed, False if released
                         "timestamp": 1675809830.123456
                     }
    """
    if data is None:
        return

    button_payload = json.dumps({
        "source": "mqtt",
        "device_id": CLIENT_ID,
        "pressed": data["pressed"],
        "timestamp": data["timestamp"]
    })

    client.publish(TOPIC_BUTTON, button_payload)
    print(f"Button data sent: {button_payload}")

if __name__ == "__main__":
    print("Button MQTT collector running. Press Ctrl+C to exit.")
    try:
        previous_state = None
        while True:
            button_data = read_button()  # Get the button data
            if button_data["pressed"] != previous_state:  # Only send if state changes
                send_mqtt(button_data)
                previous_state = button_data["pressed"]
            time.sleep(SEND_MQTT_INTERVAL)
    except KeyboardInterrupt:
        print("Exiting button MQTT collector.")
        client.loop_stop()
        client.disconnect()

