#!/usr/bin/env python3
"""Static checks for the Hermes Agent Railway deployment wrapper."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
REQUIRED = [
    ".gitignore", "CONTRIBUTING.md", "Dockerfile", "LICENSE",
    "README.md", "README.en.md", "SECURITY.md", "railway.json",
    "docs/RAILWAY-IAC-MIGRATION.md",
    "railway-entrypoint.sh", "dashboard-entrypoint.sh",
    "variables/README.md", "variables/railway-entrypoint.sh",
    "variables/generate-config.sh",
    "env-examples/dashboard.railway.example",
    "env-examples/railway-variables.example",
    "docs/SOURCES.md", "docs/brand.svg", "docs/hero.id.svg",
    "docs/hero.en.svg", "docs/architecture.svg",
    ".github/workflows/validate.yml", "scripts/check_docs.py",
    "scripts/test_deploy_modes.py", "scripts/validate_repo.py",
    "ubuntu/Dockerfile", "ubuntu/entrypoint.sh",
    "ubuntu/start-hermes", "ubuntu/system-banner.sh", "ubuntu/README.md",
]
for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        ERRORS.append(f"Missing required file: {relative}")


def read(relative: str) -> str:
    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


try:
    config = json.loads(read("railway.json"))
    if config.get("build", {}).get("builder") != "DOCKERFILE":
        ERRORS.append("railway.json must use the DOCKERFILE builder")
    if "dockerfilePath" in config.get("build", {}):
        ERRORS.append("Root railway.json must leave dockerfilePath unset for per-service RAILWAY_DOCKERFILE_PATH selection")
except (json.JSONDecodeError, OSError) as exc:
    ERRORS.append(f"Invalid railway.json: {exc}")

HERMES_VERSION = "0.23.1"
if f"FROM nousresearch/hermes-agent:v{HERMES_VERSION}" not in read("Dockerfile"):
    ERRORS.append("Root Dockerfile must pin the approved Hermes Agent release")
ubuntu_version_match = re.search(r"(?m)^ARG HERMES_VERSION=(\S+)$", read("ubuntu/Dockerfile"))
if not ubuntu_version_match or ubuntu_version_match.group(1) != HERMES_VERSION:
    ERRORS.append("Ubuntu Dockerfile Hermes version must match the root Dockerfile pin")
if "COPY variables/generate-config.sh /usr/local/bin/hermes-railway-generate-config.sh" not in read("Dockerfile"):
    ERRORS.append("Root Dockerfile must install the Variables-mode config generator")

for token in ("dashboard", "variables", "Invalid DEPLOY_MODE"):
    if token not in read("railway-entrypoint.sh"):
        ERRORS.append(f"Missing mode selector token: {token}")

dashboard = read("dashboard-entrypoint.sh")
for token in (
    "USERNAME", "PASSWORD", "SECRET", "-lt 32",
    "HERMES_DASHBOARD_BASIC_AUTH_USERNAME",
    "HERMES_DASHBOARD_BASIC_AUTH_PASSWORD",
    "HERMES_DASHBOARD_BASIC_AUTH_SECRET",
):
    if token not in dashboard:
        ERRORS.append(f"Missing Dashboard guard/configuration: {token}")

variables_entrypoint = read("variables/railway-entrypoint.sh")
variables_generator = read("variables/generate-config.sh")
for token in (
    "GROQ_API_KEY", "MISTRAL_API_KEY", "NVIDIA_API_KEY",
    "GEMINI_API_KEY", "GOOGLE_API_KEY",
    "openai/gpt-oss-20b", "ministral-3b-latest",
    "nvidia/nemotron-3.5-super-vl-120b-a12b", "gemini-3.8-flash",
    "GROQ_MODEL", "MISTRAL_MODEL", "NVIDIA_MODEL", "GEMINI_MODEL",
    "validate_model_id", "fallback_providers:", "config.yaml", "No provider API key found",
):
    if token not in variables_generator:
        ERRORS.append(f"Missing Variables-mode behavior: {token}")
for token in ("HERMES_HOME", "GOOGLE_API_KEY", "export GEMINI_API_KEY",
              "hermes-railway-generate-config.sh", "/init /opt/hermes/docker/main-wrapper.sh"):
    if token not in variables_entrypoint:
        ERRORS.append(f"Missing Variables-mode startup behavior: {token}")
if "mktemp" not in variables_generator or "mv -f" not in variables_generator:
    ERRORS.append("Variables-mode config must be written to a temporary file and atomically renamed")
if "chmod 0600" not in variables_generator:
    ERRORS.append("Variables-mode config must be restricted to owner read/write")

for relative in ("README.md", "README.en.md"):
    document = read(relative).lower()
    if relative == "README.md" and "volume berbeda untuk setiap service" not in document:
        ERRORS.append("README.md must require a different volume per service")
    if relative == "README.en.md" and "different railway volume for each service" not in document:
        ERRORS.append("README.en.md must require a different volume for each service")
    if "internet" not in document or "password" not in document:
        ERRORS.append(f"{relative} must warn about public Dashboard exposure")
    if "<h1>hermes agent railway</h1>" not in document:
        ERRORS.append(f"{relative} must use an explicit title element inside its HTML header")
    if "docs/sources.md" not in document:
        ERRORS.append(f"{relative} must link docs/SOURCES.md")
    if "img.shields.io/github/actions/workflow/status/" in document:
        ERRORS.append(f"{relative} must not use a public Shields.io workflow-status endpoint for this private repository")
    if "img.shields.io/github/license/" in document:
        ERRORS.append(f"{relative} must not use a public Shields.io license endpoint for this private repository")
    if "img.shields.io/badge/validation-configured-" not in document:
        ERRORS.append(f"{relative} must include the private-repository-compatible validation badge")
    if "img.shields.io/badge/project_license-mit-" not in document or 'href="license"' not in document:
        ERRORS.append(f"{relative} must show a static MIT badge linked to the root LICENSE file")

ubuntu_dockerfile = read("ubuntu/Dockerfile")
for token in (
    "FROM ubuntu:26.04", "ttyd",
    "raw.githubusercontent.com/NousResearch/hermes-agent/v${HERMES_VERSION}/scripts/install.sh",
    '--branch "v${HERMES_VERSION}"',
    "HERMES_HOME=/opt/data", "--retry 8", "--retry-all-errors",
    "--retry-max-time 240", "Acquire::Retries=5", "test -s /tmp/install-hermes.sh",
    "sync_venv(['all', 'messaging'], explicit=True)",
):
    if token not in ubuntu_dockerfile:
        ERRORS.append(f"Missing Ubuntu image behavior: {token}")

for token in ("util-linux", "FROM ubuntu:26.04"):
    if token not in ubuntu_dockerfile:
        ERRORS.append(f"Ubuntu image must include Gateway lock dependency: {token}")

for relative in ("README.md", "README.en.md"):
    document = read(relative).lower()
    if "watch paths" not in document or "railway-entrypoint.sh" not in document:
        ERRORS.append(f"{relative} must document per-service Watch Paths")
    exclusive_owner_phrase = "satu service" if relative == "README.md" else "one service"
    if "token" not in document or exclusive_owner_phrase not in document:
        ERRORS.append(f"{relative} must warn against assigning one bot token to multiple services")

for relative in ("ubuntu/entrypoint.sh", "ubuntu/start-hermes"):
    content = read(relative)
    if "flock" not in content or ".gateway.lock" not in content:
        ERRORS.append(f"{relative} must use the shared Gateway process lock")

ubuntu_readme = read("ubuntu/README.md")
if "RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile" not in ubuntu_readme:
    ERRORS.append("Ubuntu README must document its service-specific Dockerfile path variable")
if "RAILWAY_DOCKERFILE_PATH=/ubuntu/Dockerfile" not in read("README.md"):
    ERRORS.append("Root README must document the Ubuntu service Dockerfile path variable")

ubuntu_entrypoint = read("ubuntu/entrypoint.sh")
for token in ("TERMINAL_USER", "TERMINAL_PASSWORD", "HERMES_AUTOSTART", "ttyd", "/opt/data", "/data"):
    if token not in ubuntu_entrypoint:
        ERRORS.append(f"Missing Ubuntu terminal behavior: {token}")
if ">(sed -u -E" not in ubuntu_entrypoint or "credential:[[:space:]]*" not in ubuntu_entrypoint or "[redacted]" not in ubuntu_entrypoint:
    ERRORS.append("Ubuntu ttyd stderr must redact the encoded Basic Auth credential before it reaches deployment logs")

for token in (
    "NousResearch/hermes-agent", "MIT License", "Web Dashboard",
    "Railway", "Telegram Bot API", "Discord Developer Documentation",
    "License scope and trademarks", "brand.svg",
):
    if token not in read("docs/SOURCES.md"):
        ERRORS.append(f"Missing source or attribution topic: {token}")

if ".env" not in read(".gitignore"):
    ERRORS.append(".gitignore must exclude local environment files")

for relative in ("env-examples/dashboard.railway.example", "env-examples/railway-variables.example"):
    content = read(relative)
    if re.search(r"(?im)^(?:GROQ|MISTRAL|NVIDIA|GEMINI|GOOGLE)_API_KEY=.{8,}$", content):
        ERRORS.append(f"Possible live provider API key in {relative}")
    if re.search(r"(?im)^TELEGRAM_BOT_TOKEN=\S{20,}$", content):
        ERRORS.append(f"Possible live Telegram token in {relative}")

test_source = read("scripts/test_deploy_modes.py")
for token in ("test_missing_and_whitespace_keys", "test_single_provider_configurations",
              "test_provider_priority_and_fallback_order", "test_model_override_is_applied",
              "test_unsafe_model_id_is_rejected", "google-alias-test-secret"):
    if token not in test_source:
        ERRORS.append(f"Missing Variables-mode smoke test: {token}")

if ERRORS:
    print("Validation FAILED:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("Validation OK: three deployment modes, pinned Hermes release parity, safe model overrides, atomic provider config, storage isolation, Railway IaC migration notes, security guidance, and source attribution are present.")
print("Static validation only; runtime/provider access still requires real Railway secrets.")
