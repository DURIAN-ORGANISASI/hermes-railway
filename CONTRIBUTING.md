# Contributing

Thanks for improving Hermes Agent Railway. Keep changes focused, explain their purpose, and preserve safe defaults.

## Before opening a pull request

1. Never commit active API keys, bot tokens, Dashboard passwords/secrets, environment files, or unredacted logs.
2. Update both `README.md` and `README.en.md` when setup, variables, provider behavior, security guidance, or the three-mode deployment layout changes.
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
    sh -n variables/generate-config.sh
    bash -n ubuntu/entrypoint.sh
    bash -n ubuntu/start-hermes
    bash -n ubuntu/system-banner.sh

## Pull request checklist

- [ ] Change and rationale are explained.
- [ ] No secrets or private deployment details are included.
- [ ] Indonesian and English documentation remain aligned.
- [ ] Local links, SVGs, JSON, and shell syntax pass validation.
- [ ] Sources and license notes cover new third-party material.
- [ ] Dashboard security implications are documented.
- [ ] Root and Ubuntu images use the same pinned Hermes release.
- [ ] Variables-mode model overrides are validated and documented.
- [ ] Railway IaC migration instructions preserve all three existing services.
- [ ] Ubuntu Dockerfile path variable, terminal authentication, and optional volume paths are validated.
- [ ] Ubuntu auto-start and `start-hermes` share a Gateway lock; manual startup guidance is consistent.
- [ ] Railway Watch Paths distinguish Dashboard, Variables, and Ubuntu build inputs.
- [ ] Separate-volume guidance is consistent across all three modes.

CI runs static checks only; it does not test a live Railway deployment or external provider accounts.


When upgrading Hermes Agent, verify the upstream release first and update both `Dockerfile` and `ubuntu/Dockerfile` in the same change. Do not replace the pinned tag with `latest` or an unreviewed `main` installer URL.
