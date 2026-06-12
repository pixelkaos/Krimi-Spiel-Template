#!/usr/bin/env bash
# bootstrap-skills.sh — kopiert die 4 Codex-Skills nach ~/.claude/skills/ und setzt
# die Referenzpfade (../../ und scripts/validate…) auf DIESEN Clone.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUG="$ROOT/tools/advent-crime-game-designer"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
SKILLS=(crime-case-architect sandbox-calendar-builder deduction-consistency-auditor research-backed-story-planner)

DRY=0

usage() { cat <<'EOF'
bootstrap-skills.sh — kopiert die 4 Codex-Skills nach ~/.claude/skills/
und setzt die Referenzpfade auf diesen Clone.

  bash scripts/bootstrap-skills.sh [--dry-run]
EOF
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unbekannte Option: $arg" >&2; usage; exit 2 ;;
  esac
done

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '\033[32m%s\033[0m\n' "$*"; }
die()  { printf '\033[31m%s\033[0m\n' "$*" >&2; exit 1; }

[ -d "$PLUG/skills" ] || die "Skill-Quelle fehlt: $PLUG/skills"

bold "Kopiere Codex-Skills → $DEST"
for s in "${SKILLS[@]}"; do
  src="$PLUG/skills/$s/SKILL.md"
  [ -f "$src" ] || die "fehlt: $src"
  if [ "$DRY" = 1 ]; then
    echo "[dry-run] $s → $DEST/$s/SKILL.md (Pfade auf $PLUG umgeschrieben)"
    continue
  fi
  mkdir -p "$DEST/$s"
  sed -e "s#\.\./\.\./#$PLUG/#g" -e "s#scripts/validate#$PLUG/scripts/validate#g" "$src" > "$DEST/$s/SKILL.md"
  ok "  ✓ $s"
done

echo
bold "Optional — creative-writing-skills (Prosa-Ebene) global installieren:"
echo "  In Claude Code:  /plugin marketplace add haowjy/creative-writing-skills"
echo "                   /plugin install creative-writing-skills"
