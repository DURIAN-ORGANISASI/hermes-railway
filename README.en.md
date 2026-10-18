<div align="center">

<img src="docs/brand.svg" alt="Hermes Agent Railway" width="84" height="84">

# Hermes Agent Railway

<p><a href="https://github.com/DURIAN-ORGANISASI/hermes-railway/actions/workflows/validate.yml"><img alt="Validation workflow configured; see Actions for live status" src="https://img.shields.io/badge/validation-configured-2088FF?logo=githubactions&amp;logoColor=white"></a> <a href="LICENSE"><img alt="Project license: MIT" src="https://img.shields.io/badge/project_license-MIT-blue.svg"></a> <img alt="Railway" src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway&amp;logoColor=white"> <img alt="Docker" src="https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&amp;logoColor=white"></p>

<p><a href="README.md">🇮🇩 Bahasa Indonesia</a> · <a href="README.en.md">🇬🇧 English</a></p>

<p><strong>Run Hermes Agent on Railway.</strong><br>
Two modes are available: Dashboard or Railway Variables.</p>

<p><a href="#features">Features</a> · <a href="#choose-a-mode">Deployment modes</a> · <a href="#deploy-to-railway">Deploy</a> · <a href="#dashboard-security">Security</a> · <a href="#sources-attribution-and-licensing">Sources &amp; license</a></p>

</div>

![Hermes Agent Railway overview](docs/hero.en.svg)
<p align="center"><sub>Original documentation illustration — not an official Hermes Agent or Railway asset or screenshot.</sub></p>

<p align="center"><sub>The validation badge means the workflow is configured; it does not show live pass/fail status. Open <a href="https://github.com/DURIAN-ORGANISASI/hermes-railway/actions">Actions</a> for the latest run.</sub></p>

> [!WARNING]
> **Dashboard on a public domain:** Dashboard mode uses basic username/password authentication. Official Hermes documentation recommends this only for a trusted network or VPN, not direct public-internet exposure. Railway public domains are internet-accessible. Configure OAuth/OIDC or a trusted access gateway before exposing the Dashboard; this repository does not configure OAuth/OIDC automatically. See [Dashboard security](#dashboard-security).

## Overview

This repository wraps the upstream `nousresearch/hermes-agent` image with startup scripts for two modes. Choose one mode per Railway service.

| Mode | Purpose | Main variables |
| --- | --- | --- |
| **Dashboard** | Web interface for managing Hermes. | `USERNAME`, `PASSWORD`, `SECRET` |
| **Railway Variables** | Telegram/Discord gateway without a web Dashboard. | At least one provider API key; optional chat tokens |

## Features

- **One wrapper, two modes:** `DEPLOY_MODE` selects the mode at startup.
- **Persistent state:** a Railway Volume mounted at `/opt/data` stores Hermes configuration, sessions, skills, and data.
- **Automatic model selection:** Variables mode prioritizes Groq → Mistral → NVIDIA → Gemini and configures later active providers as fallbacks.
- **Chat integrations:** Telegram/Discord variables with user and channel allowlists.
- **Maintained docs:** sources, license scope, security policy, examples, and static CI checks.

## Choose a mode

### 1. Dashboard

This is the default when `DEPLOY_MODE` is unset. Add under **Railway → Hermes service → Variables**:

    DEPLOY_MODE=dashboard
    USERNAME=admin
    PASSWORD=replace-with-a-strong-unique-password
    SECRET=replace-with-a-random-secret-at-least-32-characters-long

- Use a unique password and random `SECRET` at least 32 characters long; for example, generate one with `openssl rand -base64 32`.
- Add a Railway Volume mounted at `/opt/data`.
- The script uses `PORT` if provided; otherwise Dashboard uses port `9119`. The Railway target port must match.
- After securing access, configure providers/models and chat integrations using the official Hermes docs.

> [!IMPORTANT]
> Basic username/password is not a substitute for OAuth/OIDC on an internet-facing Dashboard. For a public domain, use OAuth/OIDC or a properly configured access gateway that restricts access.

### 2. Railway Variables

This mode does not start the Dashboard. Set variables under **Railway → Hermes service → Variables**. At least one provider API key is required; other providers may be empty or omitted.

    DEPLOY_MODE=variables
    GROQ_API_KEY=
    MISTRAL_API_KEY=
    NVIDIA_API_KEY=
    GEMINI_API_KEY=
    GOOGLE_API_KEY=
    TELEGRAM_BOT_TOKEN=
    TELEGRAM_ALLOWED_USERS=
    DISCORD_BOT_TOKEN=
    DISCORD_ALLOWED_USERS=
    DISCORD_ALLOWED_CHANNELS=
    DISCORD_FREE_RESPONSE_CHANNELS=
    DISCORD_AUTO_THREAD=false

Minimal NVIDIA-only setup:

    DEPLOY_MODE=variables
    NVIDIA_API_KEY=your_nvidia_api_key

`GOOGLE_API_KEY` is accepted as a Gemini alias when `GEMINI_API_KEY` is empty.

#### Provider order and startup models

| Priority | Variable | Default startup model |
| ---: | --- | --- |
| 1 | `GROQ_API_KEY` | `openai/gpt-oss-20b` |
| 2 | `MISTRAL_API_KEY` | `ministral-3b-latest` |
| 3 | `NVIDIA_API_KEY` | `nvidia/nemotron-3.5-super-vl-120b-a12b` |
| 4 | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | `gemini-3.8-flash` |

Default model IDs were reviewed against provider documentation on October 18, 2026. Pricing, quotas, and availability can change; verify model access in your provider account before deploying. Fallbacks only apply to failure types supported by Hermes/provider; not every quota or authentication error will be rerouted.

> [!NOTE]
> Variables mode regenerates `/opt/data/config.yaml` at startup from active API keys. Treat Railway Variables as the source of truth rather than manually editing the generated file.

#### Telegram and Discord variables

| Variable | Purpose |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Bot token from [BotFather](https://core.telegram.org/bots#botfather). |
| `TELEGRAM_ALLOWED_USERS` | Allowed Telegram user IDs; follow the format supported by your Hermes version. |
| `DISCORD_BOT_TOKEN` | Official Discord application bot token, not a personal user token. |
| `DISCORD_ALLOWED_USERS` | Allowed Discord user IDs. |
| `DISCORD_ALLOWED_CHANNELS` | Allowed Discord channel IDs. |
| `DISCORD_FREE_RESPONSE_CHANNELS` | Channels where the bot may reply without a mention. |
| `DISCORD_AUTO_THREAD` | Set to `false` to disable automatic threads. |

Enable **Message Content Intent** in Discord Developer Portal only if required. Restrict users/channels and grant minimum permissions. Do not use a self-bot.

## Deploy to Railway

1. Fork this repository or use your own copy.
2. On [Railway](https://railway.com/), create a project and deploy through **New → GitHub Repo**. Leave Root Directory empty so Railway detects the root Dockerfile.
3. Add a Railway Volume to the Hermes service at `/opt/data`.
4. Choose one mode and set its variables. Never commit API keys or tokens to GitHub.
5. Deploy and inspect Deploy Logs. In Dashboard mode, match the Railway target port to the app port.
6. Test with an allowlisted user/channel and inspect logs if the gateway does not respond.

## Architecture and repository layout

![Hermes Agent Railway architecture](docs/architecture.svg)

| Path | Purpose |
| --- | --- |
| `Dockerfile`, `railway.json` | Image build and Railway configuration. |
| `railway-entrypoint.sh` | Selects the startup mode. |
| `dashboard-entrypoint.sh` | Validates credentials and starts Dashboard. |
| `variables/railway-entrypoint.sh` | Generates provider/fallback configuration. |
| `env-examples/` | Variable examples without active credentials. |
| `docs/SOURCES.md` | Upstream references, artwork attribution, and license scope. |
| `CONTRIBUTING.md`, `SECURITY.md` | Contribution and security guidance. |
| `scripts/` | Static configuration, documentation, and shell checks. |

## Dashboard security

- **Do not expose the Dashboard directly to the internet using only a shared password.** Upstream recommends basic authentication only on trusted networks/VPNs. Use OAuth/OIDC or a properly configured access gateway for public access.
- Dashboard is an administrative interface for sensitive configuration and agent actions.
- Keep passwords, API keys, bot tokens, and `SECRET` in Railway Variables—not in code, README files, screenshots, or public logs.
- `SECRET` signs sessions. Use a strong random value and keep it stable across redeploys; rotate it if compromised.
- Ensure the `/opt/data` Volume is mounted, restrict access to Variables, and back up important data.
- The Dockerfile uses upstream `latest`. Rebuilds may pull a different version; pin a tested version or digest for reproducible production deployments.
- Monitor provider API costs and bot permissions.

## Troubleshooting

| Problem | Check |
| --- | --- |
| Container exits at startup | Inspect Deploy Logs and `DEPLOY_MODE`. |
| Dashboard will not open | Check `USERNAME`, `PASSWORD`, `SECRET` (at least 32 characters), and target port. |
| Dashboard login fails | Check credentials and keep `SECRET` stable across redeploys. |
| Variables mode fails at startup | Set at least one Groq, Mistral, NVIDIA, or Gemini/Google API key. |
| Model unavailable | Check model ID, quota/balance, provider status, and account permissions. |
| Telegram does not respond | Check BotFather token, allowed IDs, and gateway logs. |
| Discord does not respond | Check bot token, permissions, Message Content Intent if required, and allowlists. |
| Data disappears after redeploy | Ensure the Volume is mounted at `/opt/data` on the correct service/environment. |

## Development and validation

    python scripts/validate_repo.py
    python scripts/check_docs.py
    python -m json.tool railway.json
    sh -n railway-entrypoint.sh
    sh -n dashboard-entrypoint.sh
    sh -n variables/railway-entrypoint.sh

CI checks configuration, local links, SVGs, JSON, and shell syntax. It does not test a live Docker image, Railway deployment, provider account, or message delivery.

## Sources, attribution, and licensing

See [`docs/SOURCES.md`](docs/SOURCES.md) for official references, artwork attribution, and license boundaries.

- **Repository license:** [MIT](LICENSE) applies to covered project-owned material, including the wrapper and documentation created here.
- **Hermes Agent upstream:** upstream source and image have their own license; the upstream repository currently includes an MIT License. This does not automatically relicense dependencies, API services, or trademarks.
- **Third parties:** Railway, Docker, Telegram, Discord, and model providers retain their own terms.

This independent project is not officially affiliated with or endorsed by Nous Research, Railway, Telegram, Discord, Groq, Mistral, NVIDIA, or Google.

## Contributing

Bug reports and pull requests are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md). Never include active tokens, environment files, API keys, or personal data in issues or commits.
