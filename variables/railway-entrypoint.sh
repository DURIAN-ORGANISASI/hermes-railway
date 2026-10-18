#!/bin/sh
set -eu

# Railway Variables mode: each provider uses its ordinary dedicated env var.
# Automatic priority/fallback order when multiple keys are present:
# Groq -> Mistral -> NVIDIA -> Gemini.
export HERMES_HOME=/opt/data
mkdir -p "$HERMES_HOME"
fallback_file="$HERMES_HOME/.fallback-providers.tmp"
: > "$fallback_file"

primary_provider=''
primary_model=''
fallback_count=0
groq_active=no
mistral_active=no

add_provider() {
  provider="$1"
  hermes_provider="$2"
  model_id="$3"
  if [ -z "$primary_provider" ]; then
    primary_provider="$hermes_provider"
    primary_model="$model_id"
  else
    printf '  - provider: "%s"\n    model: "%s"\n' "$hermes_provider" "$model_id" >> "$fallback_file"
    fallback_count=$((fallback_count + 1))
  fi
}

# Groq
if [ -n "${GROQ_API_KEY:-}" ]; then
  groq_active=yes
  add_provider groq custom:groq openai/gpt-oss-20b
fi

# Mistral
if [ -n "${MISTRAL_API_KEY:-}" ]; then
  mistral_active=yes
  add_provider mistral custom:mistral ministral-3b-latest
fi

# NVIDIA
if [ -n "${NVIDIA_API_KEY:-}" ]; then
  add_provider nvidia nvidia nvidia/nemotron-3.5-super-vl-120b-a12b
fi

# Gemini: accept GEMINI_API_KEY or the common GOOGLE_API_KEY alias.
gemini_key="${GEMINI_API_KEY:-${GOOGLE_API_KEY:-}}"
if [ -n "$gemini_key" ]; then
  export GEMINI_API_KEY="$gemini_key"
  export GOOGLE_API_KEY="$gemini_key"
  add_provider gemini gemini gemini-3.8-flash
fi

[ -n "$primary_provider" ] || {
  echo "[hermes-railway] No provider API key found. Set at least one of GROQ_API_KEY, MISTRAL_API_KEY, NVIDIA_API_KEY, or GEMINI_API_KEY (GOOGLE_API_KEY is also accepted)." >&2
  exit 1
}

cat > "$HERMES_HOME/config.yaml" <<EOF_CONFIG
model:
  provider: "$primary_provider"
  default: "$primary_model"
EOF_CONFIG

# Register custom OpenAI-compatible endpoints only when their keys exist.
if [ "$groq_active" = yes ]; then
  cat >> "$HERMES_HOME/config.yaml" <<'EOF_GROQ'
providers:
  groq:
    api: https://api.groq.com/openai/v1
    key_env: GROQ_API_KEY
EOF_GROQ
fi
if [ "$mistral_active" = yes ]; then
  if [ "$groq_active" != yes ]; then
    printf 'providers:\n' >> "$HERMES_HOME/config.yaml"
  fi
  cat >> "$HERMES_HOME/config.yaml" <<'EOF_MISTRAL'
  mistral:
    api: https://api.mistral.ai/v1
    key_env: MISTRAL_API_KEY
EOF_MISTRAL
fi

if [ "$fallback_count" -gt 0 ]; then
  printf '\nfallback_providers:\n' >> "$HERMES_HOME/config.yaml"
  cat "$fallback_file" >> "$HERMES_HOME/config.yaml"
fi
rm -f "$fallback_file"

# Do not expose secrets in logs; official Hermes reads the key env vars directly.
exec /init /opt/hermes/docker/main-wrapper.sh "$@"
