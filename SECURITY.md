# Security policy

Hermes Agent Railway is a deployment template, not a managed hosting or monitoring service. Operators are responsible for credentials, bot permissions, network exposure, upgrades, and backups.

## Never disclose secrets

Never publish model API keys, Telegram/Discord tokens, Dashboard passwords or `SECRET`, Railway credentials, cookies, active environment files, or unredacted logs/screenshots.

If a secret is exposed, revoke or rotate it immediately. Removing it in a later commit does not remove it from Git history.

## Dashboard exposure

- Dashboard is a privileged administrative interface for sensitive configuration and agent actions.
- This wrapper maps `USERNAME`, `PASSWORD`, and `SECRET` to Hermes basic username/password authentication.
- Upstream recommends basic authentication only on trusted networks or VPNs, not direct public-internet exposure. Railway public domains are internet-accessible by default.
- Before exposing Dashboard publicly, configure a supported OAuth/OIDC provider or trusted access gateway. This repository does not configure that layer automatically.
- Use a unique password and random `SECRET` of at least 32 characters. Keep it stable across redeploys and rotate it if compromised.

## Deployment hardening

- Mount a Railway Volume at `/opt/data` and verify the intended service/environment.
- Store API/bot tokens in Railway Variables and restrict who can read or edit them.
- Use minimum necessary bot permissions and restrict allowed Telegram/Discord users/channels.
- Do not expose gateway/API ports unless required and protected by authentication.
- Review upstream release notes before changing the pinned Hermes version. Keep the root Dockerfile and Ubuntu `HERMES_VERSION` aligned, then build and test both images before production rollout.
- Back up important `/opt/data` state and test restoration. A volume alone is not a backup.

## Reporting a vulnerability

Do not post exploit details, credentials, or private logs in public issues. Use GitHub private vulnerability reporting if enabled. Otherwise open a minimal issue requesting a private reporting channel without sensitive details.

## Upstream guidance

- [Hermes Docker setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/docker.md)
- [Hermes Dashboard security](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/web-dashboard.md)
- [Railway documentation](https://docs.railway.com/)


## Railway IaC migration

- Migrate the legacy `railway.json` configuration before Railway's December 1, 2026 cutoff.
- Pull and review the actual linked project's three service configurations before generating IaC. Preserve per-service Dockerfile paths, Watch Paths, restart policy, volumes, networking, and environment-specific settings.
- Never commit exported secrets, tokens, or environment files. Keep credentials in Railway Variables and inspect any generated IaC diff before applying it.
- Do not delete `railway.json` until the IaC plan has been reviewed, applied, and verified against all three services.
