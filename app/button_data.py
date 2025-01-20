import RPi.GPIO as GPIO
# GPIO Pin Configuration
BUTTON_PIN = 3  # GPIO3 (pin 5)
# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin as input with pull-up
def get_button_state():
    """
    Returns the current state of the button.
    True: Button is pressed.
    False: Button is released.
    """
    return GPIO.input(BUTTON_PIN) == GPIO.LOW  # LOW means pressed, HIGH means released
# Initialize GPIO
if __name__ == "__main__":
    print("Button collector running. Press Ctrl+C to exit.")
    try:
        while True:
            state = "Pressed" if get_button_state() else "Released"
            print(f"Button state: {state}")
    except KeyboardInterrupt:
        print("Exiting button collector.")
    finally:
        GPIO.cleanup()
