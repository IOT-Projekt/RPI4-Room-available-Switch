FROM python:3.10-buster

# Install system dependencies for RPi.GPIO
RUN apt-get update && apt-get install -y \
    python3-rpi.gpio \
    libgpiod2 \
    && apt-get clean
    
# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY app/* requirements.txt /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Grant the container access to Raspberry Pi GPIO

# Entry point to run the button sender script
CMD ["python", "send_mqtt.py"]

