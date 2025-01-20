import time
from gpiozero import Button

# GPIO Pin Configuration
BUTTON_PIN = 3  # GPIO3 (pin 5)

# Initialize Button
button = Button(BUTTON_PIN, pull_up=True)

def read_button():
    """
    Reads the current state of the button.
    Returns:
        dict: A dictionary containing the button state and a timestamp.
              Example:
              {
                  "pressed": True,  # True if pressed, False if released
                  "timestamp": 1675809830.123456  # Current timestamp
              }
    """
    state = {
        "pressed": button.is_pressed,
        "timestamp": time.time()
    }
    return state

