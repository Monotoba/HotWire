#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || {
  echo 'Python 3.10 or newer is required' >&2
  exit 1
}
python3 -m venv .venv
.venv/bin/python -m pip install -e .
echo 'Installed. Run ./activate_and_run.sh for the GUI or .venv/bin/wire-temp-calc --help for CLI.'
