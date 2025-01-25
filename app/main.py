import os
import time
import json
import paho.mqtt.client as mqtt
from button_data import get_button_state  

# MQTT Configuration
BROKER = os.getenv("BROKER_IP", "localhost")
PORT = int(os.getenv("BROKER_PORT", 1883))
TOPIC_BUTTON = os.getenv("TOPIC_BUTTON", "iot/devices/room_status")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
CLIENT_ID = os.getenv("CLIENT_ID", "button-sensor")

# Initialize MQTT client
client = mqtt.Client(CLIENT_ID)

# Set username and password if available
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# callback function for connection logging
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
    else:
        print(f"Failed to connect. Code: {rc}")

# callback function for publish logging
def on_publish(client, userdata, mid):
    print(f"Message with ID {mid} published")

# set the callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Initialize the previous state variable
last_sent_state = None

def send_mqtt(button_state):
    """Sends the button state to the MQTT broker."""
    # Connect to MQTT broker
    client.connect(BROKER, PORT, keepalive=60)
    
    # Create the payload for MQTT message
    payload = json.dumps({
        "source": "mqtt",
        "device_id": CLIENT_ID,
        "button_toggled": button_state,
        "timestamp": time.time()
    })

    # Publish the message to the MQTT broker
    client.publish(TOPIC_BUTTON, payload)
    print(f"Button state sent: {payload}")

if __name__ == "__main__":
    while True:
        # Get the current button state
        button_state = get_button_state()

        # If the state has changed, send it to the MQTT
        if button_state != last_sent_state:
            send_mqtt(button_state)
            last_sent_state = button_state

        # Polling delay
        time.sleep(0.1)
