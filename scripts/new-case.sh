#!/usr/bin/env bash
# new-case.sh — setzt den Vault für einen NEUEN Fall zurück:
#   • löscht Story-/Scratch-Notizen (Figuren/Orte/Hinweise/Umschläge jenseits der Seeds,
#     03_Fallbibel/06_Zeitleisten-Extras, 02_Quellen, 09_Produktion, 10_QA, 11_Inbox, work/)
#   • stellt die Skelette wieder her (Fallbibel, kb/canon, Dashboard, Sandbox-Prompt, Zeitleisten)
# Default: --keep-seeds (generische Beispiel-Notizen bleiben, Checks bleiben grün).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

KEEP_SEEDS=1; DRY=0; YES=0
SEEDS=(04_Figuren/Opfer-X.md 04_Figuren/Verdaechtige-A.md 05_Orte/12-NW-Tatort.md 07_Hinweise/C001.md 08_Umschlaege/T01-Start.md)
SKELETONS=(03_Fallbibel/Fallbibel.md kb/canon.md 00_Dashboard/Projekt-Dashboard.md 00_Dashboard/Sandbox-Calendar-Builder.md 06_Zeitleisten/Tat-Zeitleiste.md 06_Zeitleisten/Ermittlungs-Zeitleiste.md)
SCAN_DIRS=(03_Fallbibel 04_Figuren 05_Orte 06_Zeitleisten 07_Hinweise 08_Umschlaege 02_Quellen 09_Produktion 10_QA 11_Inbox work)

usage() { cat <<'EOF'
new-case.sh — Vault für einen neuen Fall zurücksetzen

  bash scripts/new-case.sh [--keep-seeds|--blank] [--dry-run] [--yes]

  --keep-seeds  generische Beispiel-Notizen behalten (Default; Checks bleiben grün)
  --blank       auch die Seeds entfernen (Vault wird komplett leer)
  --dry-run     nur anzeigen, nichts ändern
  --yes, -y     nicht nachfragen
  -h, --help    diese Hilfe
EOF
}

for arg in "$@"; do
  case "$arg" in
    --keep-seeds) KEEP_SEEDS=1 ;;
    --blank) KEEP_SEEDS=0 ;;
    --dry-run) DRY=1 ;;
    --yes|-y) YES=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unbekannte Option: $arg" >&2; usage; exit 2 ;;
  esac
done

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '\033[32m%s\033[0m\n' "$*"; }
warn() { printf '\033[33m%s\033[0m\n' "$*"; }

# Behalten = Skelette (immer) + Seeds (außer --blank). Space-gepolsterte Liste für Substring-Match.
keep_list=" ${SKELETONS[*]} "
[ "$KEEP_SEEDS" = 1 ] && keep_list="${keep_list}${SEEDS[*]} "
is_kept() { case " $keep_list " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

TO_DELETE=()
while IFS= read -r f; do
  is_kept "$f" || TO_DELETE+=("$f")
done < <(find "${SCAN_DIRS[@]}" -type f -name '*.md' 2>/dev/null | sort)

bold "Skelette zurücksetzen (${#SKELETONS[@]}):"
printf '  %s\n' "${SKELETONS[@]}"
echo
bold "Story/Scratch löschen (${#TO_DELETE[@]}):"
if [ "${#TO_DELETE[@]}" -gt 0 ]; then printf '  %s\n' "${TO_DELETE[@]}"; else echo "  (nichts)"; fi
if [ "$KEEP_SEEDS" = 0 ]; then
  echo; bold "Seeds entfernen (--blank, ${#SEEDS[@]}):"; printf '  %s\n' "${SEEDS[@]}"
fi
echo

if [ "$DRY" = 1 ]; then warn "[dry-run] nichts geändert."; exit 0; fi

if [ "$YES" != 1 ]; then
  read -r -p "Fortfahren? Löscht obige Dateien unwiderruflich. [y/N] " a
  [[ "$a" =~ ^[yYjJ] ]] || { warn "Abgebrochen."; exit 0; }
fi

# 1) löschen
for f in "${TO_DELETE[@]}"; do rm -f "$f"; done
if [ "$KEEP_SEEDS" = 0 ]; then for f in "${SEEDS[@]}"; do rm -f "$f"; done; fi
rm -rf tools/generated   # generierte Validator-Inputs (gitignored)

# 2) Skelette aus dem Wurzel-Commit des Templates wiederherstellen
if git rev-parse --git-dir >/dev/null 2>&1; then
  root_commit="$(git rev-list --max-parents=0 HEAD 2>/dev/null | head -1)"
  if [ -n "${root_commit:-}" ] && git checkout "$root_commit" -- "${SKELETONS[@]}" 2>/dev/null; then
    ok "Skelette aus Template-Wurzel ($root_commit) wiederhergestellt."
  else
    warn "Skelette nicht aus Git wiederherstellbar — bitte von Hand prüfen."
  fi
else
  warn "Kein Git-Repo — Skelette nicht automatisch wiederhergestellt (von Hand bearbeiten)."
fi

ok "Fertig. Nächster Schritt:  bash scripts/check.sh   →   dann /cw-muse + /crime-case-architect"
