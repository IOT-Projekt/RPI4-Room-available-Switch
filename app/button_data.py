# File: read_button.py
# Description: Toggles a boolean variable when the button is pressed.

import RPi.GPIO as GPIO
import time

# Pin configuration
BUTTON_PIN = 3  # Replace with the GPIO pin number where your button is connected

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor

# Initialize variables
button_toggled = False
last_button_state = GPIO.HIGH  # Assume the button is not pressed at start

def get_button_state():
    """
    Toggles and returns the button state when pressed, only if it changes.
    """
    global button_toggled, last_button_state

    # Read the current button state
    current_button_state = GPIO.input(BUTTON_PIN)

    # Detect button press (transition from not pressed to pressed)
    if last_button_state == GPIO.HIGH and current_button_state == GPIO.LOW:
        # Toggle the variable
        button_toggled = not button_toggled

    # Update the last button state
    last_button_state = current_button_state

    # Return the current toggled state
    return button_toggled

if __name__ == "__main__":
    try:
        while True:
            # Call get_button_state() for testing
            print(f"Button toggled state: {get_button_state()}")
            time.sleep(0.1)  # Polling delay
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        GPIO.cleanup()  # Cleanup GPIO pins before exiting
