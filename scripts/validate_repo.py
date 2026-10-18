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
    "railway-entrypoint.sh", "dashboard-entrypoint.sh",
    "variables/README.md", "variables/railway-entrypoint.sh",
    "env-examples/dashboard.railway.example",
    "env-examples/railway-variables.example",
    "docs/SOURCES.md", "docs/brand.svg", "docs/hero.id.svg",
    "docs/hero.en.svg", "docs/architecture.svg",
    ".github/workflows/validate.yml", "scripts/check_docs.py",
    "scripts/validate_repo.py",
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
    if config.get("build", {}).get("dockerfilePath") != "Dockerfile":
        ERRORS.append("railway.json must point to the root Dockerfile")
except (json.JSONDecodeError, OSError) as exc:
    ERRORS.append(f"Invalid railway.json: {exc}")

if not re.search(r"(?m)^FROM\s+nousresearch/hermes-agent:latest\s*$", read("Dockerfile")):
    ERRORS.append("Upstream image tag changed; update source/version notes")

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

variables = read("variables/railway-entrypoint.sh")
for token in (
    "GROQ_API_KEY", "MISTRAL_API_KEY", "NVIDIA_API_KEY",
    "GEMINI_API_KEY", "GOOGLE_API_KEY", "nvidia/nemotron-3.5-super-vl-120b-a12b", "gemini-3.8-flash", "fallback_providers:", "config.yaml",
):
    if token not in variables:
        ERRORS.append(f"Missing Variables-mode behavior: {token}")

for relative in ("README.md", "README.en.md"):
    document = read(relative).lower()
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

if ERRORS:
    print("Validation FAILED:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("Validation OK: files, deployment modes, Dashboard warning, and source attribution are present.")
print("Static validation only; it does not test a live Railway deployment.")
