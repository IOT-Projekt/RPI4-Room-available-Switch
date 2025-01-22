# File: read_button.py
# Description: Toggles a boolean variable when the button is pressed and logs the state.

import RPi.GPIO as GPIO
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]  # Send logs to stdout for Docker
)

# Pin configuration
BUTTON_PIN = 3  # Replace with the GPIO pin number where your button is connected

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN)  # No pull-up/down resistor since there's a physical pull-up

# Initialize variables
button_toggled = False

def get_button_state():
    """
    Toggles and returns the button state when pressed, only if it changes.
    The state will only toggle on button press (not release).
    Logs the state change to Docker logs.
    """


    # Read the current button state
    current_button_state = GPIO.input(BUTTON_PIN)

    # Detect button press (transition from not pressed to pressed)
    if current_button_state ==  GPIO.LOW:
        # Button was pressed, toggle the variable
        button_toggled = not button_toggled

        # Log the state change
        logging.info(f"Button toggled state: {button_toggled}")

    # Update the last button state


    # Return the current toggled state
    return button_toggled

if __name__ == "__main__":
    try:
        while True:
            # Call get_button_state() to check the button
            get_button_state()
            time.sleep(0.05)  # Polling delay
    except KeyboardInterrupt:
        logging.info("Exiting program...")
    finally:
        GPIO.cleanup()  # Cleanup GPIO pins before exiting
