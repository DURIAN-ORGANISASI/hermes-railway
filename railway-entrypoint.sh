#!/bin/sh
set -eu

# One image/repository, two startup modes. Dashboard remains the default so a
# fresh deployment needs only USERNAME, PASSWORD and SECRET.
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
