#!/usr/bin/env python3
"""Smoke-test provider config generation without real credentials or network access."""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "variables" / "generate-config.sh"


def run_generator(values: dict[str, str], home: Path) -> subprocess.CompletedProcess[str]:
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HERMES_HOME": str(home),
        "TZ": "UTC",
    }
    env.update(values)
    return subprocess.run(
        ["sh", str(GENERATOR)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_missing_and_whitespace_keys_do_not_overwrite_existing_config() -> None:
    for values in ({}, {"GROQ_API_KEY": "   \t  "}):
        with tempfile.TemporaryDirectory(prefix="hermes-config-test-") as temp:
            home = Path(temp)
            config = home / "config.yaml"
            config.write_text("model:\n  provider: nvidia\n  default: keep-existing\n", encoding="utf-8")
            result = run_generator(values, home)
            require(result.returncode != 0, "missing/whitespace-only provider key must be rejected")
            require("No provider API key found" in result.stderr, "failure must explain the missing provider key")
            require(config.read_text(encoding="utf-8").endswith("default: keep-existing\n"),
                    "failed generation must preserve the previous config")
            require(sorted(p.name for p in home.iterdir()) == ["config.yaml"],
                    "temporary files must be cleaned after a failed generation")


def test_single_provider_configurations() -> None:
    cases = [
        (
            {"GROQ_API_KEY": "groq-test-secret"},
            'provider: "custom:groq"',
            'default: "openai/gpt-oss-20b"',
            "api: https://api.groq.com/openai/v1",
            "key_env: GROQ_API_KEY",
        ),
        (
            {"MISTRAL_API_KEY": "mistral-test-secret"},
            'provider: "custom:mistral"',
            'default: "ministral-3b-latest"',
            "api: https://api.mistral.ai/v1",
            "key_env: MISTRAL_API_KEY",
        ),
        (
            {"NVIDIA_API_KEY": "nvidia-test-secret"},
            'provider: "nvidia"',
            'default: "nvidia/nemotron-3.5-super-vl-120b-a12b"',
            None,
            None,
        ),
        (
            {"GEMINI_API_KEY": "gemini-test-secret"},
            'provider: "gemini"',
            'default: "gemini-3.8-flash"',
            None,
            None,
        ),
        (
            {"GOOGLE_API_KEY": "google-alias-test-secret"},
            'provider: "gemini"',
            'default: "gemini-3.8-flash"',
            None,
            None,
        ),
    ]
    for values, provider_line, model_line, api_line, key_env_line in cases:
        with tempfile.TemporaryDirectory(prefix="hermes-config-test-") as temp:
            home = Path(temp)
            result = run_generator(values, home)
            require(result.returncode == 0, f"valid provider rejected ({list(values)}): {result.stderr}")
            config = home / "config.yaml"
            require(config.is_file(), "config.yaml was not generated")
            text = config.read_text(encoding="utf-8")
            require(provider_line in text, f"wrong provider for {list(values)}")
            require(model_line in text, f"wrong default model for {list(values)}")
            require("fallback_providers:" not in text, "single-provider config must not have fallbacks")
            if api_line:
                require(api_line in text, "custom provider API endpoint missing")
            if key_env_line:
                require(key_env_line in text, "custom provider key_env missing")
            for secret in values.values():
                require(secret not in text, "an API key value was written into config.yaml")
            require(config.stat().st_mode & 0o777 == 0o600, "config.yaml must be private (0600)")
            require(len(list(home.iterdir())) == 1, "successful generation left temporary files")


def test_provider_priority_and_fallback_order() -> None:
    values = {
        "GEMINI_API_KEY": "gemini-test-secret",
        "NVIDIA_API_KEY": "nvidia-test-secret",
        "MISTRAL_API_KEY": "mistral-test-secret",
        "GROQ_API_KEY": "groq-test-secret",
    }
    with tempfile.TemporaryDirectory(prefix="hermes-config-test-") as temp:
        home = Path(temp)
        result = run_generator(values, home)
        require(result.returncode == 0, f"multiple provider keys rejected: {result.stderr}")
        text = (home / "config.yaml").read_text(encoding="utf-8")
        require('provider: "custom:groq"' in text, "Groq must be the highest-priority provider")
        require('default: "openai/gpt-oss-20b"' in text, "wrong primary model")
        expected_fallbacks = [
            '  - provider: "custom:mistral"\n    model: "ministral-3b-latest"',
            '  - provider: "nvidia"\n    model: "nvidia/nemotron-3.5-super-vl-120b-a12b"',
            '  - provider: "gemini"\n    model: "gemini-3.8-flash"',
        ]
        positions = [text.find(item) for item in expected_fallbacks]
        require(all(pos >= 0 for pos in positions), "one or more fallback providers are missing")
        require(positions == sorted(positions), "fallback providers are not in documented priority order")
        require("groq-test-secret" not in text and "mistral-test-secret" not in text
                and "nvidia-test-secret" not in text and "gemini-test-secret" not in text,
                "provider secret values must never be written to config.yaml")
        require(text.count("fallback_providers:") == 1, "fallback_providers must be emitted exactly once")


def main() -> int:
    tests = [
        test_missing_and_whitespace_keys_do_not_overwrite_existing_config,
        test_single_provider_configurations,
        test_provider_priority_and_fallback_order,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"All {len(tests)} Variables-mode smoke-test groups passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
