#!/bin/sh
set -eu

# Root image selector for Dashboard/Variables. Ubuntu selects its separate image
# through RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile on that service only.
case "${DEPLOY_MODE:-dashboard}" in
  dashboard)
    exec /usr/local/bin/hermes-railway-dashboard-entrypoint.sh "$@"
    ;;
  variables)
    exec /usr/local/bin/hermes-railway-variables-entrypoint.sh "$@"
    ;;
  *)
    echo "[hermes-railway] Invalid DEPLOY_MODE='${DEPLOY_MODE}'. Use 'dashboard' or 'variables'." >&2
    exit 1
    ;;
esac
