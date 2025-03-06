#!/bin/bash

# Set default values if not already set
export HELP=${HELP:-false}
export IP=${IP:-0.0.0.0}
export PORT=${PORT:-4840}
export SLEEP=${SLEEP:-2}
export DB_NAME=${DB_NAME:-test}
export CREATE_DATA_SIZE=${CREATE_DATA_SIZE:-false}
export NUM_TABLES=${NUM_TABLES:-20}
export NUM_COLUMNS=${NUM_COLUMNS:-100}
export SHOW_QUALITY=${SHOW_QUALITY:-false}

# Display help or examples if requested
if [[ "$HELP" == "true" ]]; then
  python3 /app/Sample-Data-Generator/data_generator_opcua.py --help
  exit 1
fi

# Run the data generator script with appropriate arguments
CMD=(
  python3 /app/Sample-Data-Generator/data_generator_opcua.py "${IP}" "${PORT}"
  --sleep "${SLEEP}"
  --db-name "${DB_NAME}"
)

if [[ "${CREATE_DATA_SIZE}" == "true" ]] ; then
  CMD+=(--create-data-size --num-tables "${NUM_TABLES}" --num-columns "${NUM_COLUMNS}")
  if [[ "${SHOW_QUALITY}" == "true" ]] ; then
    CMD+=(--show-quality)
  fi
fi

"${CMD[@]}"
