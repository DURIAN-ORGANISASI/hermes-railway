# Sources, attribution, and licensing

This repository wraps the upstream Hermes Agent container for Dashboard/Variables modes and keeps an independent Ubuntu 26.04 + ttyd image for Ubuntu Terminal mode. These are technical/policy references, not endorsements.

## Hermes Agent upstream

- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — upstream source, releases, image details, and current license.
- [Hermes Agent v0.23.1 release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.1) — the release currently pinned by both runtime modes.
- [Upstream MIT License](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE) — the upstream repository currently includes an MIT License; its license file is authoritative for upstream code.
- [Hermes Docker setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/docker.md) — image tags, startup, gateway mode, persistence, and Dashboard deployment.
- [Hermes Web Dashboard guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/web-dashboard.md) — authentication providers and security recommendations, including basic-auth limitations on public networks.
- [Hermes environment variables](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/environment-variables.md) — configuration and credentials.
- [Official Hermes documentation](https://hermes-agent.nousresearch.com/docs/) — usage, model providers, and messaging.

## Platforms and APIs

- [Railway documentation](https://docs.railway.com/) / [Railway](https://railway.com/) — services, variables, networking, and volumes.
- [Docker documentation](https://docs.docker.com/) — container image and runtime concepts.
- [Ubuntu](https://ubuntu.com/) — Ubuntu base image used by the terminal service.
- [ttyd](https://github.com/tsl0922/ttyd) — browser-based terminal used by Ubuntu mode.
- [Telegram Bot API](https://core.telegram.org/bots/api) / [BotFather](https://core.telegram.org/bots#botfather) — official bot API and token setup.
- [Discord Developer Documentation](https://discord.com/developers/docs/intro) — bot tokens, permissions, intents, and API.
- [Groq supported models](https://console.groq.com/docs/models), [Mistral model selection](https://docs.mistral.ai/getting-started/models/compare), [NVIDIA Nemotron 3.5 Super VL](https://build.nvidia.com/nvidia/nemotron-3.5-super-vl-120b-a12b), and [Google Gemini models](https://ai.google.dev/gemini-api/docs/models) — official model APIs and availability.

Variables mode uses the following configurable starting presets, depending on the first configured provider key: `openai/gpt-oss-20b` (Groq), `ministral-3b-latest` (Mistral), `nvidia/nemotron-3.5-super-vl-120b-a12b` (NVIDIA), and `gemini-3.8-flash` (Gemini). Operators can override them with `GROQ_MODEL`, `MISTRAL_MODEL`, `NVIDIA_MODEL`, and `GEMINI_MODEL`. These are project defaults, not a guarantee of current availability, free usage, quota, or provider support; verify model IDs, prices, and terms with each provider before deployment.

## Project files and original artwork

- `Dockerfile` pins `nousresearch/hermes-agent:v0.23.1` and adds this repository's startup wrappers.
- `railway-entrypoint.sh` selects Dashboard or Variables mode.
- `dashboard-entrypoint.sh` validates Dashboard variables and maps them to Hermes basic-auth variables.
- `variables/railway-entrypoint.sh` generates provider/fallback configuration from Railway Variables.
- `ubuntu/Dockerfile`, `ubuntu/entrypoint.sh`, `ubuntu/start-hermes`, and `ubuntu/system-banner.sh` implement the Ubuntu browser terminal and optional Gateway startup.
- `docs/brand.svg`, `docs/hero.*.svg`, and `docs/architecture.svg` are original illustrations for this repository, not official Hermes Agent or Railway assets/screenshots.

## License scope and trademarks

The root [`LICENSE`](../LICENSE) is this repository's MIT License. It applies to project-owned scripts, configuration examples, and documentation covered by that license. It does not relicense the upstream image or included software, grant trademark rights, or override Railway, Telegram, Discord, provider, or other service terms.

The upstream Hermes Agent repository currently includes its own MIT License. Verify the upstream license and image version independently. The root image and Ubuntu installer are pinned to the same release tag (`v0.23.1`) so rebuilding this repository does not silently move to a different upstream commit.

Nous Research, Hermes Agent, Railway, Docker, Telegram, Discord, Groq, Mistral, NVIDIA, Google, and related marks belong to their respective owners. This is an independent deployment wrapper and is not affiliated with or endorsed by those organizations.


## Railway configuration migration

- [Railway Infrastructure as Code](https://docs.railway.com/infrastructure-as-code) — the project-level configuration system used to replace legacy Config-as-Code files.
- [Railway Config-as-Code migration](https://docs.railway.com/config-as-code) — deprecation timeline, CLI migration, and compatibility details.
