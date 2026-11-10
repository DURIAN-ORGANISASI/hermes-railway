# Hermes Agent Railway — Railway Variables mode

Variables mode does not start the web Dashboard. Configure provider keys and optional Telegram/Discord credentials in Railway service Variables.

At least one provider API key is required. Set `DEPLOY_MODE=variables`; Dashboard credentials will not start the web interface in this mode.

## Minimal setup

    DEPLOY_MODE=variables
    NVIDIA_API_KEY=your_nvidia_api_key

## Provider order

1. Groq — `GROQ_API_KEY`
2. Mistral — `MISTRAL_API_KEY`
3. NVIDIA — `NVIDIA_API_KEY`
4. Gemini — `GEMINI_API_KEY`, or `GOOGLE_API_KEY` as an alias

The first non-empty key becomes the startup provider; other active keys are configured as fallbacks.

| Provider | Startup model | Optional override variable |
| --- | --- | --- |
| Groq | `openai/gpt-oss-20b` | `GROQ_MODEL` |
| Mistral | `ministral-3b-latest` | `MISTRAL_MODEL` |
| NVIDIA | `nvidia/nemotron-3.5-super-vl-120b-a12b` | `NVIDIA_MODEL` |
| Gemini | `gemini-3.8-flash` | `GEMINI_MODEL` |

Set an override only when the model ID is available to your provider account. Model catalogs, account access, pricing, and quotas can change; verify before deployment. The generator accepts only letters, digits, dot, underscore, colon, slash, and hyphen in model IDs to prevent invalid YAML. Empty override values keep the defaults.

## Persistence and security

- Mount a Railway Volume at `/opt/data`.
- Never commit API keys or bot tokens; use Railway Variables and restrict access.
- This mode regenerates `/opt/data/config.yaml` on each startup. Provider variables are the source of truth.
- Dashboard is not started, so chat-only use does not require a public Dashboard domain.
- Read the root [README](../README.md), [security policy](../SECURITY.md), and [source/licensing notes](../docs/SOURCES.md).
