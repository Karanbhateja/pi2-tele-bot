# Use the official Python image based on Alpine Linux
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies needed for building packages
RUN apk add --no-cache gcc musl-dev linux-headers

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the alert script into the container
COPY alert_bot.py .

# Run the alert script
CMD ["python", "alert_bot.py"]
