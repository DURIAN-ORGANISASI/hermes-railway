#!/bin/sh
set -eu

# Railway Variables mode: emit config atomically from the provider keys attached
# to this service. Keep the variables as the source of truth for this mode.
export HERMES_HOME=/opt/data
mkdir -p "$HERMES_HOME"

has_value() {
  [ -n "$(printf '%s' "$1" | tr -d '[:space:]')" ]
}

# Hermes uses GEMINI_API_KEY. Accept GOOGLE_API_KEY as a convenience alias,
# but make sure the normalized name is present in the environment of /init.
if ! has_value "${GEMINI_API_KEY:-}" && has_value "${GOOGLE_API_KEY:-}"; then
  export GEMINI_API_KEY="$GOOGLE_API_KEY"
fi

/usr/local/bin/hermes-railway-generate-config.sh

# Preserve the upstream /init + main-wrapper startup chain so the Gateway is
# supervised by the official Hermes container runtime.
exec /init /opt/hermes/docker/main-wrapper.sh "$@"
