#!/usr/bin/env bash
# check.sh — lokale CI-Parität in EINEM Befehl. Delegiert an tools/check_all.py
# (eine Quelle der Wahrheit; deckt dieselben Gating- + informativen Checks ab wie GitHub Actions).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-python3}"

command -v "$PY" >/dev/null 2>&1 || { printf '\033[31m%s\033[0m\n' "python3 nicht gefunden — bitte installieren (brew install python)." >&2; exit 127; }

exec "$PY" "$ROOT/tools/check_all.py" "$@"
