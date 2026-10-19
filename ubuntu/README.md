# Ubuntu Terminal mode

Ubuntu Terminal mode is part of the combined Hermes Agent Railway repository. It preserves the Ubuntu 26.04 browser terminal, `ttyd` authentication, system banner, Hermes CLI installation, and optional Gateway auto-start. Set `RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile` only on the Ubuntu service to choose this image.

## Configure the Railway service

1. Connect the service to `DURIAN-ORGANISASI/hermes-railway` on the intended branch.
2. Leave **Root Directory** empty.
3. Add `RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile` in that service's Variables. This selects the Ubuntu Dockerfile while keeping the build context at repository root. Set the Railway restart policy to **On Failure** with up to 10 retries.
4. Add service-scoped variables:

       TERMINAL_USER=durianadmin
       TERMINAL_PASSWORD=unique-password-at-least-16-characters
       TZ=Asia/Jakarta
       HERMES_AUTOSTART=true
       RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile

5. Attach a dedicated Railway Volume to this service at `/opt/data`. If terminal-created files must persist, attach a different Volume at `/data`.
6. Generate the service domain for `ttyd` and open it in the browser.

## First-time setup

Inside the authenticated terminal, run:

```bash
hermes setup
hermes gateway setup
```

Choose provider/model and messaging channels interactively. When `/opt/data/config.yaml` exists, `HERMES_AUTOSTART=true` (default) starts the Gateway in the background with a restart loop. The auto-start supervisor and `start-hermes` use the same lock file at `/opt/data/.gateway.lock`, so the supported wrapper will not start a second Gateway while one already holds the lock. For manual startup, set `HERMES_AUTOSTART=false` and restart the Railway service before running `start-hermes`. Avoid running `hermes gateway run` directly while auto-start is active because a direct CLI command bypasses this guard.

## Storage boundaries

- `/opt/data`: persistent Hermes configuration, session/history, memory, and logs. This must be a unique volume for this Ubuntu service; it must not be shared with Dashboard or Variables.
- `/data`: optional persistent user files created in the general terminal. Use a separate volume if you need these files to survive container replacement.
- `/usr/local/share/hermes-agent` and `/usr/local/share/hermes-tools`: image/runtime files, not persistent user data. A redeploy rebuilds these paths.

## Security and limitations

The shell runs as root inside the container and the web terminal is reachable through the service domain. Use a strong unique `TERMINAL_PASSWORD`, restrict domain access, and do not expose terminal credentials or API keys in GitHub or logs. This is a Railway container, not a full VPS/systemd host; processes follow the container lifecycle.

See the [combined repository README](../README.md) for the full three-service deployment plan.