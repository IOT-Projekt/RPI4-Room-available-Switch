# File: read_button.py
# Description: Reads the state of a button attached to a Raspberry Pi and outputs a boolean value.

import RPi.GPIO as GPIO
import time

# Pin configuration
BUTTON_PIN = 3  

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the pin as an input with an internal pull-up resistor

def is_button_pressed():
    """
    Reads the button state and returns True if pressed, False otherwise.
    """
    return GPIO.input(BUTTON_PIN) == GPIO.LOW  # Assuming button press pulls the pin LOW

if __name__ == "__main__":
    try:
        while True:
            button_state = is_button_pressed()
            print(f"Button pressed: {button_state}")
            time.sleep(0.1)  # Polling delay
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        GPIO.cleanup()  # Cleanup GPIO pins before exiting
