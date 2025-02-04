import RPi.GPIO as GPIO
import time
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()] 
)

# Pin configuration
BUTTON_PIN = os.getenv("BUTTON_PIN", 17)

# GPIO setup
GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_PIN, GPIO.IN) 

# Initialize variables and constant
button_toggled = False
last_press_time = 0
DEBOUNCE_DELAY = 0.2 

def get_button_state():
    """
    Toggles and returns the button state when pressed, with software debouncing.
    The state will only toggle on button press (not release).
    Logs the state change to Docker logs.
    """
    global button_toggled, last_press_time

    # Read the current button state
    current_button_state = GPIO.input(BUTTON_PIN)
    current_time = time.time()

    # Detect button press (transition from not pressed to pressed) with debounce
    if current_button_state == GPIO.LOW and (current_time - last_press_time > DEBOUNCE_DELAY):
        last_press_time = current_time  
        button_toggled = not button_toggled # Toggle the state

        # Log the state change
        logging.info(f"Button toggled state: {button_toggled}")

    # Return the current toggled state
    return button_toggled
