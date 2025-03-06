FROM python:3.12-alpine as base

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
COPY blobs/factory_images.json blobs/factory_images.json

COPY data_generator/ data_generator/
COPY data_publisher/ data_publisher/
COPY requirements.txt requirements.txt
COPY data_generator.py data_generator.py
COPY data_generator.sh data_generator.sh

# Optimize package installation
RUN apk add --no-cache bash python3-dev py3-pip
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt || true

FROM base AS deployment

# Ensure script has execution permissions
RUN chmod +x data_generator.sh

ENTRYPOINT ["/bin/bash", "data_generator.sh"]
