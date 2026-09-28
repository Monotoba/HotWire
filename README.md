# HotWire — Wire Temperature Calculator

[![CI](https://github.com/Monotoba/HotWire/actions/workflows/ci.yml/badge.svg)](https://github.com/Monotoba/HotWire/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Status: alpha](https://img.shields.io/badge/status-alpha-orange)](docs/model-validation.md)

A Python CLI and PySide6 desktop app for **estimating** steady-state wire temperature from current, diameter, length, and material. It also displays experimental foam cutting ranges. These ranges are **not safety limits**.

## Status and scope

This is alpha software. The wire model has been checked for physical consistency and against published room-temperature resistivity for two representative alloys; **its temperature predictions have not been calibrated against measured wire temperatures**. The foam database has not been verified against manufacturer safety data sheets. Do not use the output to determine permissible exposure, ventilation adequacy, fire safety, or a safe operating temperature. See [model validation and limitations](docs/model-validation.md).

The app supports Nichrome, Kanthal, and a generic stainless estimate; AWG, SWG, mm, mils, and inches for wire size; and mm, cm, inches, feet, metres, and yards for length. It can display a temperature chart, save/load JSON projects, and export/print a chart. The CLI can calculate one current or an explicit range, list foam types, and display preliminary foam information.

## Install from source

Python 3.10 or newer is required. From a checkout:

```bash
git clone https://github.com/Monotoba/HotWire.git
cd HotWire
python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
```

Launch the GUI with `wire-temp-gui` or `python -m wire_temp_calc.main`. A desktop session is required. Run `wire-temp-calc --help` for CLI options. No PyPI or native installer availability is promised by this source installation guide.

## Examples

```bash
wire-temp-calc --gauge 22 --material nichrome --length 2 --length-unit feet --current 1
wire-temp-calc --current-start 0.1 --current-end 5 --current-step 0.1
wire-temp-calc --list-foams
wire-temp-calc --safety-info EPS 250
```

The CLI's foam information is heuristic. Ventilation is recommended for hot-wire cutting regardless of whether the modeled temperature falls inside a listed cutting range. Read the material-specific safety data sheet and use suitable engineering controls.

## Development and release

```bash
python -m pip install -e '.[dev]'
QT_QPA_PLATFORM=offscreen pytest tests/  # Linux headless test environment
black --check src/
mypy src/ --ignore-missing-imports
python -m build
python -m twine check dist/*
```

The current GitHub Actions matrix tests Python 3.10–3.13 on Linux, Windows, and macOS and builds source and wheel artifacts. [Release preparation](docs/release-checklist.md) records the remaining checks. A green CI build is not a validation of measured thermal performance.

## Documentation and contribution

- [Installation](docs/installation/index.md)
- [User guide](docs/user-guide.md)
- [Model validation and limitations](docs/model-validation.md)
- [Release checklist](docs/release-checklist.md)
- [Contributing](CONTRIBUTING.md) and [issues](https://github.com/Monotoba/HotWire/issues)

HotWire is licensed under the [MIT License](LICENSE).
