# Ubuntu Terminal mode — complete installation guide

Ubuntu Terminal mode is part of the combined Hermes Agent Railway repository. It provides Ubuntu 26.04, an authenticated `ttyd` browser terminal, the Hermes CLI, and optional Gateway auto-start. This is a Railway container, not a full VPS or systemd host.

## 1. Create/configure the Railway service

1. Connect a new Railway service to `DURIAN-ORGANISASI/hermes-railway`, branch `main`.
2. Keep **Root Directory empty** so the Docker build context is the repository root.
3. Under the service build settings, choose the Dockerfile builder and set **Dockerfile Path** to `ubuntu/Dockerfile`. Do not rely on the variable alone: verify the actual build setting uses this file.
4. Set restart policy to **On Failure**, with up to 10 retries.
5. Create a Railway domain for the service; the terminal listens on port `8080`.

## 2. Complete Railway Variables template

Copy this block into **Service → Variables**. Replace both terminal credential values before deploying:

```dotenv
RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile
TERMINAL_USER=replace_terminal_username
TERMINAL_PASSWORD=REPLACE_WITH_RANDOM_PASSWORD_AT_LEAST_16_CHARS
HERMES_HOME=/opt/data
HERMES_RUNTIME_DIR=/usr/local/share/hermes-tools
UV_CACHE_DIR=/tmp/uv-cache
HERMES_AUTOSTART=true
TZ=Asia/Jakarta
PORT=8080
```

Requirements:
- `TERMINAL_USER` is required and must not contain a colon (`:`).
- `TERMINAL_PASSWORD` is required and at least 16 characters long. Use a strong, unique password.
- `RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile` is retained in the template, but the Railway service's **Dockerfile Path** must also be set to `ubuntu/Dockerfile`.
- `HERMES_AUTOSTART=true` is the default and starts the Gateway automatically only after the config file exists.
- The terminal port is `8080`; the generated service domain must target the same port.

## 3. Attach persistent storage

Create a dedicated Railway Volume and mount it at:

```text
/opt/data
```

This stores Hermes configuration, session/history, memory, and logs. Never share the same volume with Dashboard or Variables services.

The terminal's working directory is `/data`. Files saved there are not guaranteed to survive container replacement unless you attach a **separate, second Volume** at `/data`. Keep this volume separate from the `/opt/data` volume.

Runtime-managed packages and caches are placed under `/usr/local/share/hermes-tools` or `/tmp/uv-cache` because they can be re-created; persistent user state belongs under `/opt/data`.

## 4. Deploy and open the terminal

Deploy the service and wait for Railway to report deployment completion. Open its generated domain and log in with `TERMINAL_USER` and `TERMINAL_PASSWORD`.

Expected behavior:
- Without setup, the terminal page may still load, but logs will state that Hermes is installed and `/opt/data/config.yaml` does not exist yet.
- This is an initial-setup state, not evidence that the Gateway is ready.
- If the page does not load, confirm domain target port `8080`, check service status, and inspect build/deploy logs.

## 5. Set up Hermes inside the terminal

Run this command first:

```bash
hermes setup
```

Follow the interactive setup to choose your model provider, credentials, and runtime options. Then run:

```bash
hermes gateway setup
```

Configure messaging integrations you intend to use (for example Telegram or Discord). Use bot tokens from official developer consoles and user/channel IDs supported by your current Hermes version. Never commit active credentials to GitHub or publish them in screenshots or logs.

Verify that the generated configuration exists:

```bash
test -f /opt/data/config.yaml \
  && echo "Hermes config found" \
  || echo "Config not found — complete setup first"
```

If it prints the missing-config message, return to the setup wizard and resolve any error before continuing.

## 6. Start and verify the Gateway

When `/opt/data/config.yaml` exists, restart the Railway service. With `HERMES_AUTOSTART=true`, the entrypoint should detect the config and start the Gateway supervisor.

Check Railway **Deploy Logs** for startup messages and provider/authentication errors. Then send a test message to the configured bot and verify that it replies. A Railway deployment status of `SUCCESS` means the process started; it does not prove the model API, bot token, or message delivery is working.

For manual Gateway startup:
1. Set `HERMES_AUTOSTART=false` in Railway Variables.
2. Restart the service.
3. Run:

```bash
start-hermes
```

The supported auto-start supervisor and `start-hermes` wrapper share the lock file `/opt/data/.gateway.lock`. Do not run a second Gateway while auto-start is active. Avoid `hermes gateway run` directly while auto-start is enabled because it bypasses the wrapper lock.

## 7. Configure Telegram/Discord safely

- Use a dedicated bot token for this service. Do not run the same Telegram or Discord token in Dashboard/Variables and Ubuntu at the same time.
- Ensure allowlist IDs match intended users/channels.
- For Discord, enable required bot intents (including Message Content Intent when required) and only grant necessary permissions.
- If the bot does not answer, check Gateway logs, token validity, provider key, model name, allowlists, and Discord permissions/intents.

## 8. Storage, restarts, and security

- `/opt/data`: persistent Hermes config, sessions/history, memory, and logs.
- `/data`: terminal working files; persists only if you attach a separate Volume at this mount.
- `/usr/local/share/hermes-agent` and `/usr/local/share/hermes-tools`: runtime/image-managed files that may be rebuilt on redeploy.

The terminal runs a shell as root inside the container and is reachable via its service domain. Use a strong password, restrict public access where possible, and never publish terminal credentials or API keys.

**Credential/log warning:** ttyd may print its HTTP basic-auth credential as Base64 in logs. Base64 is not encryption. If the terminal password appears in logs, consider it exposed: immediately rotate `TERMINAL_PASSWORD` in Railway Variables and redeploy.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Terminal domain returns 502 | Ensure the domain targets port `8080`; inspect deployment logs. |
| Login fails | Check `TERMINAL_USER` and `TERMINAL_PASSWORD`; password must be at least 16 characters. |
| Config is missing | Run `hermes setup` and `hermes gateway setup`; verify `/opt/data/config.yaml`. |
| Gateway does not start | Confirm `HERMES_AUTOSTART=true`, config exists, and inspect logs for provider/auth errors. |
| Telegram/Discord bot is silent | Check token, provider key, model availability, allowlists, bot permissions/intents, and duplicate Gateway processes. |
| Files under `/data` disappear | Attach a separate Railway Volume at `/data`. |
| Volume fills up | Keep cache/reinstallable runtime data outside `/opt/data`; preserve only user state there. |

See the [main README](../README.md) for Dashboard and Railway Variables mode instructions.