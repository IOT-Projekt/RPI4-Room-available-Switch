# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY button_data.py send_mqtt.py requirements.txt /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Grant the container access to Raspberry Pi GPIO


# Entry point to run the button sender script
CMD ["python", "send_mqtt.py"]

