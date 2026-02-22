#!/usr/bin/env bash
# -----------------------------
# Entrypoint wrapper for Data Generator
# Converts ENV variables into proper CLI arguments
# -----------------------------

# Show help if HELP is set
if [[ -n "${HELP}" ]]; then
    python /app/data_generator_main.py --help
    exit 0
fi

# Exit if required variables are missing
if [[ -z "${DATA}" ]] || [[ -z "${PUBLISH_FORMAT}" ]]; then
    echo "ERROR: DATA and PUBLISH_FORMAT must be set."
    python /app/data_generator_main.py --help
    exit 1
fi

# Initialize argument array
ARGS=("$DATA" "$PUBLISH_FORMAT")

# Optional IDs (comma-separated -> space-separated)
[[ -n "${RIG_IDS}" ]] && ARGS+=("--rig-ids" ${RIG_IDS//,/ })
[[ -n "${VESSEL_IDS}" ]] && ARGS+=("--vessel-ids" ${VESSEL_IDS//,/ })
[[ -n "${TURBINE_IDS}" ]] && ARGS+=("--turbine-ids" ${TURBINE_IDS//,/ })
[[ -n "${PROVEIT_TOPICS}" ]] && ARGS+=("--proveit-topics" ${PROVEIT_TOPICS//,/ })

# Global arguments
[[ -n "${CONN}" ]] && ARGS+=("--conn" "$CONN")
[[ -n "${DB_NAME}" ]] && ARGS+=("--db-name" "$DB_NAME")
[[ -n "${REPEAT}" ]] && ARGS+=("--repeat" "$REPEAT")
[[ -n "${TIMEOUT}" ]] && ARGS+=("--timeout" "$TIMEOUT")
[[ -n "${SLEEP}" ]] && ARGS+=("--sleep" "$SLEEP")
[[ -n "${OFFSET_SLEEP}" ]] && ARGS+=("--offset-sleep" "$OFFSET_SLEEP")

# Execute the data generator
exec python /app/data_generator_main.py "${ARGS[@]}"