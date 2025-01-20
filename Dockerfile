# Use a lightweight Python base image
FROM python:3.10-buster

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY app/* requirements.txt /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Grant the container access to Raspberry Pi GPIO

# Entry point to run the button sender script
CMD ["python", "send_mqtt.py"]

