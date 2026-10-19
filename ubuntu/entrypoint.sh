#!/usr/bin/env bash
set -Eeuo pipefail

: "${TERMINAL_USER:?Set TERMINAL_USER in Railway Variables}"
: "${TERMINAL_PASSWORD:?Set TERMINAL_PASSWORD in Railway Variables}"

if [[ "${TERMINAL_USER}" == *:* ]]; then
  echo "ERROR: TERMINAL_USER must not contain a colon (:)." >&2
  exit 1
fi
if [[ ${#TERMINAL_PASSWORD} -lt 16 ]]; then
  echo "ERROR: TERMINAL_PASSWORD must be at least 16 characters." >&2
  exit 1
fi

PORT="${PORT:-8080}"
HERMES_HOME="${HERMES_HOME:-/opt/data}"
HERMES_RUNTIME_DIR="${HERMES_RUNTIME_DIR:-/usr/local/share/hermes-tools}"
UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}"
export HERMES_HOME HERMES_RUNTIME_DIR UV_CACHE_DIR
mkdir -p "${HERMES_HOME}" "${HERMES_RUNTIME_DIR}" "${UV_CACHE_DIR}" /data

# Keep large, re-downloadable Hermes tool payloads and partial downloads off
# Railway's small persistent volume. Config, sessions, logs and memory stay in
# HERMES_HOME; only the tool store and download cache are redirected.
relocate_rebuildable_dir() {
  local persistent="$1"
  local runtime="$2"
  mkdir -p "$(dirname "${persistent}")" "$(dirname "${runtime}")"

  if [[ -L "${persistent}" ]]; then
    if [[ "$(readlink "${persistent}")" == "${runtime}" ]]; then
      mkdir -p "${runtime}"
      return 0
    fi
    echo "ERROR: ${persistent} is a symlink to an unexpected location: $(readlink "${persistent}")" >&2
    return 1
  fi

  if [[ -d "${persistent}" ]]; then
    mkdir -p "${runtime}"
    # Copy to the container filesystem first, then remove the volume copy.
    # This works across Railway's separate volume/container filesystems.
    cp -a "${persistent}/." "${runtime}/" || {
      echo "ERROR: Could not migrate ${persistent} to ${runtime}; original data was kept." >&2
      return 1
    }
    rm -rf "${persistent}"
  elif [[ -e "${persistent}" ]]; then
    echo "ERROR: ${persistent} exists but is not a directory." >&2
    return 1
  else
    mkdir -p "${runtime}"
  fi

  ln -s "${runtime}" "${persistent}"
}

relocate_rebuildable_dir "${HERMES_HOME}/cache/partials" "${HERMES_RUNTIME_DIR}/cache/partials"
relocate_rebuildable_dir "${HERMES_HOME}/tools" "${HERMES_RUNTIME_DIR}/tools"

# Hermes PM's uv cache is hard-coded under HERMES_HOME/cache/uv in this
# upstream build; UV_CACHE_DIR alone does not relocate it. Move this disposable
# cache off Railway's small volume and link it to the container filesystem.
UV_PM_CACHE_DIR="${HERMES_HOME}/cache/uv"
UV_RUNTIME_CACHE_DIR="${HERMES_RUNTIME_DIR}/cache/uv"
mkdir -p "${HERMES_HOME}/cache" "${HERMES_RUNTIME_DIR}/cache"
if [[ -L "${UV_PM_CACHE_DIR}" ]]; then
  rm -f "${UV_PM_CACHE_DIR}"
elif [[ -d "${UV_PM_CACHE_DIR}" ]]; then
  if [[ -d "${UV_RUNTIME_CACHE_DIR}" ]]; then
    cp -a "${UV_PM_CACHE_DIR}/." "${UV_RUNTIME_CACHE_DIR}/" 2>/dev/null || true
    rm -rf "${UV_PM_CACHE_DIR}"
  else
    mv "${UV_PM_CACHE_DIR}" "${UV_RUNTIME_CACHE_DIR}" 2>/dev/null || {
      # uv cache is reproducible; discard only this cache if migration fails.
      rm -rf "${UV_PM_CACHE_DIR}"
      mkdir -p "${UV_RUNTIME_CACHE_DIR}"
    }
  fi
elif [[ -e "${UV_PM_CACHE_DIR}" ]]; then
  rm -f "${UV_PM_CACHE_DIR}"
fi
mkdir -p "${UV_RUNTIME_CACHE_DIR}"
ln -s "${UV_RUNTIME_CACHE_DIR}" "${UV_PM_CACHE_DIR}"

# Hermes PM stores its per-install runtime under HERMES_HOME/installs by default.
# Railway's persistent /opt/data volume is small, so move that PM-only state to
# the container filesystem and symlink it back. User config, sessions and memory
# remain under HERMES_HOME; only reinstallable package-manager state is redirected.
PM_STATE_DIR="${HERMES_HOME}/installs"
PM_RUNTIME_STATE_DIR="${HERMES_RUNTIME_DIR}/installs"
mkdir -p "${HERMES_RUNTIME_DIR}"
if [[ -L "${PM_STATE_DIR}" ]]; then
  mkdir -p "${PM_RUNTIME_STATE_DIR}"
elif [[ -d "${PM_STATE_DIR}" ]]; then
  if [[ -e "${PM_RUNTIME_STATE_DIR}" ]]; then
    cp -a "${PM_STATE_DIR}/." "${PM_RUNTIME_STATE_DIR}/" || {
      echo "ERROR: Could not migrate Hermes PM state out of ${PM_STATE_DIR}." >&2
      exit 1
    }
    rm -rf "${PM_STATE_DIR}"
  else
    mv "${PM_STATE_DIR}" "${PM_RUNTIME_STATE_DIR}" || {
      echo "ERROR: Could not move Hermes PM state out of ${PM_STATE_DIR}." >&2
      exit 1
    }
  fi
  ln -s "${PM_RUNTIME_STATE_DIR}" "${PM_STATE_DIR}"
elif [[ -e "${PM_STATE_DIR}" ]]; then
  echo "ERROR: ${PM_STATE_DIR} exists but is not a directory or symlink." >&2
  exit 1
else
  ln -s "${PM_RUNTIME_STATE_DIR}" "${PM_STATE_DIR}"
fi
cd /data

# Railway containers do not rely on systemd. Keep the Gateway in the container
# foreground lifecycle via this restart loop only after the user has configured it.
if [[ "${HERMES_AUTOSTART:-true}" == "true" || "${HERMES_AUTOSTART:-true}" == "1" ]]; then
  if [[ -f "${HERMES_HOME}/config.yaml" ]]; then
    (
      echo "Hermes config found; starting Gateway supervisor."
      while true; do
        echo "Starting Hermes Gateway..."
        hermes gateway run || true
        echo "Hermes Gateway exited; retrying in 5 seconds."
        sleep 5
      done
    ) &
  else
    echo "Hermes is installed, but setup has not created ${HERMES_HOME}/config.yaml yet."
    echo "Open the terminal, run 'hermes setup' and 'hermes gateway setup', then restart the service."
  fi
fi

echo "Starting authenticated Ubuntu + Hermes terminal on port ${PORT}."
exec /usr/local/bin/ttyd --port "${PORT}" --credential "${TERMINAL_USER}:${TERMINAL_PASSWORD}" --writable --cwd /data bash --login
