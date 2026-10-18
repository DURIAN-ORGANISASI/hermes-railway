# Sources, attribution, and licensing

This repository wraps the upstream Hermes Agent container for Railway deployment. These are technical/policy references, not endorsements.

## Hermes Agent upstream

- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — upstream source, releases, image details, and current license.
- [Upstream MIT License](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE) — the upstream repository currently includes an MIT License; its license file is authoritative for upstream code.
- [Hermes Docker setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/docker.md) — image tags, startup, gateway mode, persistence, and Dashboard deployment.
- [Hermes Web Dashboard guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/web-dashboard.md) — authentication providers and security recommendations, including basic-auth limitations on public networks.
- [Hermes environment variables](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/environment-variables.md) — configuration and credentials.
- [Official Hermes documentation](https://hermes-agent.nousresearch.com/docs/) — usage, model providers, and messaging.

## Platforms and APIs

- [Railway documentation](https://docs.railway.com/) / [Railway](https://railway.com/) — services, variables, networking, and volumes.
- [Docker documentation](https://docs.docker.com/) — container image and runtime concepts.
- [Telegram Bot API](https://core.telegram.org/bots/api) / [BotFather](https://core.telegram.org/bots#botfather) — official bot API and token setup.
- [Discord Developer Documentation](https://discord.com/developers/docs/intro) — bot tokens, permissions, intents, and API.
- [Groq documentation](https://console.groq.com/docs), [Mistral](https://docs.mistral.ai/), [NVIDIA API Catalog](https://build.nvidia.com/), and [Google Gemini API](https://ai.google.dev/gemini-api/docs) — provider APIs and model availability.

The default model IDs in `variables/railway-entrypoint.sh` are wrapper configuration choices, not guarantees of continued availability, free usage, quota, or provider support. Verify current prices and terms with each provider.

## Project files and original artwork

- `Dockerfile` uses the mutable `nousresearch/hermes-agent:latest` image and adds this repository's startup wrappers.
- `railway-entrypoint.sh` selects Dashboard or Variables mode.
- `dashboard-entrypoint.sh` validates Dashboard variables and maps them to Hermes basic-auth variables.
- `variables/railway-entrypoint.sh` generates provider/fallback configuration from Railway Variables.
- `docs/brand.svg`, `docs/hero.*.svg`, and `docs/architecture.svg` are original illustrations for this repository, not official Hermes Agent or Railway assets/screenshots.

## License scope and trademarks

The root [`LICENSE`](../LICENSE) is this repository's MIT License. It applies to project-owned scripts, configuration examples, and documentation covered by that license. It does not relicense the upstream image or included software, grant trademark rights, or override Railway, Telegram, Discord, provider, or other service terms.

The upstream Hermes Agent repository currently includes its own MIT License. Verify the upstream license and image version independently. Because this repository uses the mutable `latest` tag, rebuilding can change upstream software even if this repository's source does not change.

Nous Research, Hermes Agent, Railway, Docker, Telegram, Discord, Groq, Mistral, NVIDIA, Google, and related marks belong to their respective owners. This is an independent deployment wrapper and is not affiliated with or endorsed by those organizations.
