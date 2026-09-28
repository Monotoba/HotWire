# Alpha release preparation

Proposed version: `2.0.0a1`. Release scope: a **GitHub alpha source archive and Python wheel/source distribution**, with an explicit experimental-model notice. No PyPI publication or native desktop installer is included.

## Gates

- [x] Fix advertised CLI commands and cover success/error exits with command tests.
- [x] Smoke-test GUI chart, project round trip, and PDF output offscreen.
- [x] Check model monotonicity, unit equivalence, heat balance, and published room-temperature resistivity for representative alloys.
- [x] Document unvalidated temperature and foam safety claims.
- [ ] Confirm the release commit passes the complete Linux/Windows/macOS CI matrix.
- [x] Build sdist and wheel, pass `twine check`, and install the wheel in a clean Linux Python 3.12 environment; run CLI and headless GUI smoke checks.
- [ ] Manually test Windows installation and printing on an actual printer, if those paths are promoted as supported.
- [ ] Review release notes and tag `v2.0.0a1` after approval.

No measured thermal or foam-exposure validation is claimed for this alpha. Any subsequent production-oriented release needs material-specific measurements and safety review. See [model validation](model-validation.md).
