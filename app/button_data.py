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
last_press_time = 0
DEBOUNCE_DELAY = 0.2  # 200 milliseconds debounce delay

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
        last_press_time = current_time  # Update the last press time
        button_toggled = not button_toggled  # Toggle the button state

        # Log the state change
        logging.info(f"Button toggled state: {button_toggled}")

    # Return the current toggled state
    return button_toggled

if __name__ == "__main__":
    try:
        while True:
            # Call get_button_state() to check the button
            get_button_state()
            time.sleep(0.01)  # Polling delay (smaller delay for responsiveness)
    except KeyboardInterrupt:
        logging.info("Exiting program...")
    finally:
        GPIO.cleanup()  # Cleanup GPIO pins before exiting
