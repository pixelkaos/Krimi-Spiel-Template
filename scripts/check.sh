#!/usr/bin/env bash
# check.sh — lokale CI-Parität: dieselben Checks wie GitHub Actions.
# Gating (müssen bestehen): check_frontmatter / check_links / check_tags + Codex-Beispiel-Validatoren.
# Informativ: orphans / duplicates / Umschlag-Manifest.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY="${PYTHON:-python3}"
PLUG="tools/advent-crime-game-designer"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '\033[32m%s\033[0m\n' "$*"; }
err()  { printf '\033[31m%s\033[0m\n' "$*"; }

command -v "$PY" >/dev/null 2>&1 || { err "python3 nicht gefunden — bitte installieren (brew install python)."; exit 127; }

fail=0
gate() {
  local label="$1"; shift
  bold "▶ $label"
  if "$PY" "$@"; then ok "  ✓ $label"; else err "  ✗ $label"; fail=1; fi
  echo
}
info() {
  local label="$1"; shift
  bold "▶ $label (informativ)"
  "$PY" "$@" || true
  echo
}

bold "== Gating-Checks =="
gate "Frontmatter-Schema"   tools/check_frontmatter.py
gate "Wikilinks"            tools/check_links.py
gate "Tag-Konsistenz"       tools/check_tags.py
gate "Truth-Map (Beispiel)" "$PLUG/scripts/validate_truth_map.py" "$PLUG/assets/templates/truth-map.example.json"
gate "Timeline (Beispiel)"  "$PLUG/scripts/validate_timeline.py"  "$PLUG/assets/templates/timeline.example.json"

bold "== Informative Checks =="
info "Verwaiste Notizen" tools/check_orphans.py
info "Near-Duplikate"    tools/check_duplicates.py

bold "▶ Umschlag-Manifest (informativ)"
if "$PY" tools/frontmatter_to_validator_json.py envelopes >/dev/null 2>&1; then
  "$PY" "$PLUG/scripts/validate_envelope_manifest.py" tools/generated/envelope-manifest.json || true
else
  echo "  (übersprungen — kein Manifest erzeugbar)"
fi
echo

if [ "$fail" -ne 0 ]; then
  err "✗ Mindestens ein Gating-Check ist rot."
  exit 1
fi
ok "✓ Alle Gating-Checks bestanden."
