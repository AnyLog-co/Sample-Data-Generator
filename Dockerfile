# Use Python 3.12 Alpine as the base image
FROM python:3.12-alpine AS base

# Set the working directory for the application
WORKDIR /app/Sample-Data-Generator

# Create necessary directories in a single command to optimize layer caching
RUN mkdir -p blobs/car_video \
             blobs/factory_images \
             blobs/people_video \
             blobs/models \
             data_generator \
             data_publisher

# Copy necessary files and directories in a structured manner
COPY blobs/car_video blobs/car_video
COPY blobs/factory_images blobs/factory_images
COPY blobs/people_video blobs/people_video
COPY blobs/models blobs/models

COPY data_generator/ data_generator/
COPY data_publisher/ data_publisher/
COPY requirements.txt requirements.txt
COPY data_generator.py data_generator.py
COPY data_generator.sh data_generator.sh
COPY data_generator_opcua.py data_generator_opcua.py
COPY data_generator_opcua.sh data_generator_opcua.sh

# Install dependencies and optimize package installation
RUN apk add --no-cache bash python3-dev py3-pip && \
    python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || true

# Ensure scripts have execution permissions
RUN chmod +x /app/Sample-Data-Generator/*.sh

# Add environment variable (defaults to false, change based on your need)
ENV ENV_RUN_OPCUA="false"

# Deployment stage: we will set up entry point based on the condition
FROM base AS deployment

# Make the script executable if it's not already
RUN chmod +x /app/Sample-Data-Generator/*.sh

# Set volume for blobs-data
VOLUME blobs-data:/app/Sample-Data-Generator/blobs/

# Set ENTRYPOINT with conditional script execution based on ENV_RUN_OPCUA
ENTRYPOINT ["/bin/sh", "-c", "if [ \"$ENV_RUN_OPCUA\" = \"true\" ]; then /app/Sample-Data-Generator/data_generator_opcua.sh; else /app/Sample-Data-Generator/data_generator.sh; fi"]
