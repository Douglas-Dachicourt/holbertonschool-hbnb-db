# Use the latest Python alpine image as base
FROM python:3.11-alpine

# Update and install necessary packages
RUN apk update && apk upgrade && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev bash

# Create a non-root user for security purposes
RUN adduser -D -s /bin/bash hbnb

# Switch to the newly created user and create necessary directories
USER hbnb
WORKDIR /home/hbnb

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app ./app

# Create a directory for hbnb_data and set permissions
RUN mkdir -p /home/hbnb/hbnb_data \
    && chmod -R 774 /home/hbnb/hbnb_data

# Expose the application port
EXPOSE 8000

# Set the working directory and the command to run the application
WORKDIR /home/hbnb/app
CMD ["python", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
