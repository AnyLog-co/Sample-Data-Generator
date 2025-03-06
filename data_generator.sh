#!/bin/bash

# Set default values if not already set
export HELP=${HELP:-false}
export DATA_GENERATOR=${DATA_GENERATOR:-rand}
export CONN=${CONN:-127.0.0.1:32149}
export PUBLISHER=${PUBLISHER:-put}
export BATCH_SIZE=${BATCH_SIZE:-10}
export TOTAL_ROWS=${TOTAL_ROWS:-10}
export SLEEP=${SLEEP:-0.5}
export DB_NAME=${DB_NAME:-test}
export TOPIC=${TOPIC:-anylog-demo}
export TIMEOUT=${TIMEOUT:-30}
export QOS=${QOS:-0}
export EXCEPTION=${EXCEPTION:-false}
export IS_AGGREGATED=${IS_AGGREGATED:-false}
export TOLERANCE_LEVEL=${TOLERANCE_LEVEL:-0}
export EXAMPLES=${EXAMPLES:-false}

# Display help or examples if requested
if [[ "$HELP" == "true" ]]; then
  python3 /app/Sample-Data-Generator/data_generator.py --help
  exit 1
fi

if [[ "$EXAMPLES" == "true" ]]; then
  python3 /app/Sample-Data-Generator/data_generator.py rand 127.0.0.1:32149 put --examples
  exit 1
fi

# Install dependencies for specific data generators
if [[ "$DATA_GENERATOR" == "cars" ]]; then
  python3 -m pip install --upgrade tensorflow numpy
  apk add --no-cache py3-opencv
fi

# Install dependencies for specific publishers
if [[ "$PUBLISHER" == "mqtt" ]]; then
  python3 -m pip install --upgrade paho-mqtt==1.5.1
fi

if [[ "$PUBLISHER" == "kafka" ]]; then
  python3 -m pip install --upgrade kafka-python
fi

# Run the data generator script with appropriate arguments
CMD=(
  python3 /app/Sample-Data-Generator/data_generator.py "$DATA_GENERATOR" "$CONN" "$PUBLISHER"
  --db-name "$DB_NAME"
  --batch-size "$BATCH_SIZE"
  --total-rows "$TOTAL_ROWS"
  --sleep "$SLEEP"
  --topic "$TOPIC"
  --timeout "$TIMEOUT"
  --qos "$QOS"
)

if [[ "$EXCEPTION" == "true" ]]; then
  CMD+=(--exception)
fi

if [[ "$IS_AGGREGATED" == "true" ]]; then
  CMD+=(--is-aggregated)
fi

if [[ "$TOLERANCE_LEVEL" != "0" ]]; then
  CMD+=(--tolerance-level "$TOLERANCE_LEVEL")
fi

"${CMD[@]}"
