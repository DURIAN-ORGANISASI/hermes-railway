#!/bin/sh
set -eu

: "${USERNAME:?Set USERNAME in Railway Variables}"
: "${PASSWORD:?Set PASSWORD in Railway Variables}"
: "${SECRET:?Set SECRET in Railway Variables}"

if [ "${#SECRET}" -lt 32 ]; then
  echo "[hermes-railway] SECRET must be at least 32 characters. Generate one with: openssl rand -base64 32" >&2
  exit 1
fi

newline='
'
for value in "$USERNAME" "$PASSWORD" "$SECRET"; do
  case "$value" in
    *"$newline"*) echo "[hermes-railway] Dashboard credentials must not contain newline characters." >&2; exit 1 ;;
  esac
done

export HERMES_HOME=/opt/data
export HERMES_DASHBOARD=1
export HERMES_DASHBOARD_HOST=0.0.0.0
export HERMES_DASHBOARD_BASIC_AUTH_USERNAME="$USERNAME"
export HERMES_DASHBOARD_BASIC_AUTH_PASSWORD="$PASSWORD"
export HERMES_DASHBOARD_BASIC_AUTH_SECRET="$SECRET"
# Use Railway's assigned target port when supplied; otherwise use Hermes' default.
export HERMES_DASHBOARD_PORT="${PORT:-9119}"
mkdir -p "$HERMES_HOME"

# Preserve the upstream /init + main-wrapper startup chain so the current s6
# services supervise both gateway and dashboard in one container.
exec /init /opt/hermes/docker/main-wrapper.sh "$@"
