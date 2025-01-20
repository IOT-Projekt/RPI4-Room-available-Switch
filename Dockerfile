# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY app/button_data.py app/send_mqtt.py requirements.txt /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Grant the container access to Raspberry Pi GPIO
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    python3-rpi.gpio \
    && apt-get clean

# Entry point to run the button sender script
CMD ["python", "send_mqtt.py"]

