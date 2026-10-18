# Contributing

Thanks for improving Hermes Agent Railway. Keep changes focused, explain their purpose, and preserve safe defaults.

## Before opening a pull request

1. Never commit active API keys, bot tokens, Dashboard passwords/secrets, environment files, or unredacted logs.
2. Update both `README.md` and `README.en.md` when setup, variables, provider behavior, or security guidance changes.
3. Update `docs/SOURCES.md` when adding upstream projects, providers, dependencies, copied material, screenshots, or artwork.
4. Keep this repository's MIT license distinct from the upstream Hermes Agent license.
5. Do not claim a live deployment was tested unless it was tested in a disposable Railway environment.
6. Review Dashboard exposure; upstream recommends basic authentication only on trusted networks or VPNs.

## Local checks

    python scripts/validate_repo.py
    python scripts/check_docs.py
    python -m json.tool railway.json
    sh -n railway-entrypoint.sh
    sh -n dashboard-entrypoint.sh
    sh -n variables/railway-entrypoint.sh

## Pull request checklist

- [ ] Change and rationale are explained.
- [ ] No secrets or private deployment details are included.
- [ ] Indonesian and English documentation remain aligned.
- [ ] Local links, SVGs, JSON, and shell syntax pass validation.
- [ ] Sources and license notes cover new third-party material.
- [ ] Dashboard security implications are documented.

CI runs static checks only; it does not test a live Railway deployment or external provider accounts.
