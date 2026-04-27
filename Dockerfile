# -----------------------------
# Base image
# -----------------------------
FROM python:3.11-slim AS base

WORKDIR /app

# Copy application files
COPY data_generator_main.py Sample-Data-Generator/
COPY requirements.txt .
COPY run.sh .

# Copy full source-original tree
COPY source-original/ Sample-Data-Generator/source/

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Runtime image
# -----------------------------
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed Python libraries and scripts from base
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /app /app

# Environment variables for all data generator options
ENV HELP="" \
    DATA="" \
    PUBLISH_FORMAT="print" \
    RIG_IDS="" \
    VESSEL_IDS="" \
    TURBINE_IDS="" \
    PROVEIT_TOPICS="" \
    CONN="" \
    DB_NAME="test" \
    REPEAT=10 \
    TIMEOUT=60 \
    SLEEP=15 \
    OFFSET_SLEEP=0.5

# Entrypoint
ENTRYPOINT ["bash", "/app/run.sh"]