#!/bin/sh
# Generate a valid Hermes config from Railway provider variables.
# This helper deliberately does not print or persist API key values.
set -eu

HERMES_HOME="${HERMES_HOME:-/opt/data}"
export HERMES_HOME
mkdir -p "$HERMES_HOME"

has_value() {
  [ -n "$(printf '%s' "$1" | tr -d '[:space:]')" ]
}

fallback_file="$(mktemp "$HERMES_HOME/.fallback-providers.XXXXXX")"
config_tmp=''
cleanup() {
  rm -f "$fallback_file"
  if [ -n "$config_tmp" ]; then
    rm -f "$config_tmp"
  fi
}
trap cleanup 0
trap 'exit 1' HUP INT TERM

primary_provider=''
primary_model=''
fallback_count=0
groq_active=no
mistral_active=no

validate_model_id() {
  provider_name="$1"
  model_id="$2"
  case "$model_id" in
    ''|*[!A-Za-z0-9._:/-]*)
      echo "[hermes-railway] Invalid model ID for ${provider_name}. Use only letters, digits, dot, underscore, colon, slash, and hyphen." >&2
      exit 1
      ;;
  esac
}

add_provider() {
  hermes_provider="$1"
  model_id="$2"
  validate_model_id "$hermes_provider" "$model_id"
  if [ -z "$primary_provider" ]; then
    primary_provider="$hermes_provider"
    primary_model="$model_id"
  else
    printf '  - provider: "%s"\n    model: "%s"\n' "$hermes_provider" "$model_id" >> "$fallback_file"
    fallback_count=$((fallback_count + 1))
  fi
}

if has_value "${GROQ_API_KEY:-}"; then
  groq_active=yes
  add_provider custom:groq "${GROQ_MODEL:-openai/gpt-oss-20b}"
fi

if has_value "${MISTRAL_API_KEY:-}"; then
  mistral_active=yes
  add_provider custom:mistral "${MISTRAL_MODEL:-ministral-3b-latest}"
fi

if has_value "${NVIDIA_API_KEY:-}"; then
  add_provider nvidia "${NVIDIA_MODEL:-nvidia/nemotron-3.5-super-vl-120b-a12b}"
fi

gemini_key="${GEMINI_API_KEY:-}"
if ! has_value "$gemini_key"; then
  gemini_key="${GOOGLE_API_KEY:-}"
fi
if has_value "$gemini_key"; then
  add_provider gemini "${GEMINI_MODEL:-gemini-3.8-flash}"
fi

if [ -z "$primary_provider" ]; then
  echo "[hermes-railway] No provider API key found. Set at least one non-empty key: GROQ_API_KEY, MISTRAL_API_KEY, NVIDIA_API_KEY, GEMINI_API_KEY, or GOOGLE_API_KEY." >&2
  exit 1
fi

# Write to a temporary file and rename only after the full config is ready.
# An invalid/missing key must never truncate a previously working config.
config_tmp="$(mktemp "$HERMES_HOME/.config.yaml.XXXXXX")"
cat > "$config_tmp" <<EOF_CONFIG
model:
  provider: "$primary_provider"
  default: "$primary_model"
EOF_CONFIG

# Only named OpenAI-compatible providers need custom endpoint definitions.
if [ "$groq_active" = yes ] || [ "$mistral_active" = yes ]; then
  printf '\nproviders:\n' >> "$config_tmp"
  if [ "$groq_active" = yes ]; then
    cat >> "$config_tmp" <<'EOF_GROQ'
  groq:
    api: https://api.groq.com/openai/v1
    key_env: GROQ_API_KEY
EOF_GROQ
  fi
  if [ "$mistral_active" = yes ]; then
    cat >> "$config_tmp" <<'EOF_MISTRAL'
  mistral:
    api: https://api.mistral.ai/v1
    key_env: MISTRAL_API_KEY
EOF_MISTRAL
  fi
fi

if [ "$fallback_count" -gt 0 ]; then
  printf '\nfallback_providers:\n' >> "$config_tmp"
  cat "$fallback_file" >> "$config_tmp"
fi

chmod 0600 "$config_tmp"
mv -f "$config_tmp" "$HERMES_HOME/config.yaml"
config_tmp=''
echo "[hermes-railway] Hermes provider configuration generated successfully."
