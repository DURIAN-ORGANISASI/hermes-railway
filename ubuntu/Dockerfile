FROM ubuntu:26.04
ARG DEBIAN_FRONTEND=noninteractive
ARG TTYD_VERSION=1.7.7
ARG TARGETARCH

# Keep Hermes package-manager runtimes outside HERMES_HOME. Railway's /opt/data
# volume may be only 500 MB; Python/Node/FFmpeg managed tools must not fill it.
ENV TZ=Asia/Jakarta \
    PORT=8080 \
    PATH="/root/.local/bin:/root/.local/share/uv/bin:/usr/local/bin:/usr/bin:/bin" \
    HERMES_HOME=/opt/data \
    HERMES_RUNTIME_DIR=/usr/local/share/hermes-tools \
    UV_CACHE_DIR=/tmp/uv-cache \
    HERMES_AUTOSTART=true

RUN apt-get -o Acquire::Retries=5 update && apt-get install -y --no-install-recommends \
    bash ca-certificates curl coreutils procps sed git \
    python3 python3-venv python3-pip \
    build-essential pkg-config libffi-dev libssl-dev xz-utils util-linux \
    libx11-6 libxext6 libxrender1 libxi6 libxtst6 libxkbcommon0 \
    && (apt-get install -y --no-install-recommends fastfetch || true) \
    && rm -rf /var/lib/apt/lists/*

# Download ttyd for the target architecture.
RUN set -eux; \
    case "${TARGETARCH:-amd64}" in \
      amd64) TTYD_ASSET="ttyd.x86_64" ;; \
      arm64) TTYD_ASSET="ttyd.aarch64" ;; \
      *) echo "Unsupported architecture: ${TARGETARCH}"; exit 1 ;; \
    esac; \
    curl -fsSL --retry 8 --retry-all-errors --retry-delay 5 --retry-max-time 240 --connect-timeout 20 --max-time 180 \
      "https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/${TTYD_ASSET}" -o /usr/local/bin/ttyd; \
    chmod +x /usr/local/bin/ttyd; \
    /usr/local/bin/ttyd --version

# Install Hermes into the image at build time. HERMES_HOME is only for persistent
# user config/state; HERMES_RUNTIME_DIR keeps managed tools off the small volume.
# Put dependency state and rebuildable download caches on the image filesystem BEFORE
# the installer runs. Runtime entrypoint recreates these links after Railway mounts /opt/data.
RUN set -eux; \
    mkdir -p "${HERMES_HOME}/cache" \
      "${HERMES_RUNTIME_DIR}/installs" \
      "${HERMES_RUNTIME_DIR}/cache/uv" \
      "${HERMES_RUNTIME_DIR}/cache/partials" \
      "${HERMES_RUNTIME_DIR}/tools" \
      /usr/local/share/hermes-agent; \
    ln -s "${HERMES_RUNTIME_DIR}/installs" "${HERMES_HOME}/installs"; \
    ln -s "${HERMES_RUNTIME_DIR}/cache/uv" "${HERMES_HOME}/cache/uv"; \
    ln -s "${HERMES_RUNTIME_DIR}/cache/partials" "${HERMES_HOME}/cache/partials"; \
    ln -s "${HERMES_RUNTIME_DIR}/tools" "${HERMES_HOME}/tools"; \
    if ! curl -fsSL --retry 8 --retry-all-errors --retry-delay 5 --retry-max-time 240 --connect-timeout 20 --max-time 180 \
      https://hermes-agent.nousresearch.com/install.sh -o /tmp/install-hermes.sh; then \
      echo "Primary Hermes installer unavailable; retrying from the official GitHub source."; \
      curl -fsSL --retry 8 --retry-all-errors --retry-delay 5 --retry-max-time 240 --connect-timeout 20 --max-time 180 \
        https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh -o /tmp/install-hermes.sh; \
    fi; \
    test -s /tmp/install-hermes.sh; \
    head -n 1 /tmp/install-hermes.sh | grep -Eq "^#!/(usr/bin/env bash|bin/bash|usr/bin/env sh|bin/sh)$"; \
    bash /tmp/install-hermes.sh --dir /usr/local/share/hermes-agent --hermes-home "${HERMES_HOME}" --non-interactive --skip-browser; \
    rm -f /tmp/install-hermes.sh; \
    command -v hermes

COPY ubuntu/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY ubuntu/system-banner.sh /etc/profile.d/00-system-banner.sh
COPY ubuntu/start-hermes /usr/local/bin/start-hermes

RUN chmod 0755 /usr/local/bin/entrypoint.sh /usr/local/bin/start-hermes /etc/profile.d/00-system-banner.sh \
    && mkdir -p /data /opt/data /usr/local/share/hermes-tools \
    && chmod 0777 /data \
    && chmod 0755 /opt/data /usr/local/share/hermes-tools

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
