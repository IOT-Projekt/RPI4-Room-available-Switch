from gpiozero import Button
from signal import pause

# GPIO Pin Configuration
BUTTON_PIN = 3  # GPIO3 (pin 5)

# Setup Button
button = Button(BUTTON_PIN, pull_up=True)  # Pull-up resistor is enabled by default in gpiozero

def button_pressed():
    """
    Callback function when the button is pressed.
    """
    print("Button state: Pressed")

def button_released():
    """
    Callback function when the button is released.
    """
    print("Button state: Released")

# Attach event handlers
button.when_pressed = button_pressed
button.when_released = button_released

if __name__ == "__main__":
    print("Button collector running. Press Ctrl+C to exit.")
    try:
        pause()  # Keeps the program running to listen for button events
    except KeyboardInterrupt:
        print("Exiting button collector.")

