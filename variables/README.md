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

| Provider | Startup model |
| --- | --- |
| Groq | `openai/gpt-oss-20b` |
| Mistral | `ministral-3b-latest` |
| NVIDIA | `nvidia/nemotron-3-super-120b-a12b` |
| Gemini | `gemini-2.5-flash` |

Model availability, pricing, quotas, and provider support may change. Verify them before deployment.

## Persistence and security

- Mount a Railway Volume at `/opt/data`.
- Never commit API keys or bot tokens; use Railway Variables and restrict access.
- This mode regenerates `/opt/data/config.yaml` on each startup. Provider variables are the source of truth.
- Dashboard is not started, so chat-only use does not require a public Dashboard domain.
- Read the root [README](../README.md), [security policy](../SECURITY.md), and [source/licensing notes](../docs/SOURCES.md).
