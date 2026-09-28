#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -x .venv/bin/wire-temp-gui ]; then
  echo 'Run ./install.sh first, or follow docs/installation/index.md.' >&2
  exit 1
fi
exec .venv/bin/wire-temp-gui
