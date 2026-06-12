#!/usr/bin/env bash
# setup.sh — macOS-Bootstrap für das Krimi-Spiel-Template.
# Installiert nur Fehlendes (Homebrew-Pakete, Ollama-Modelle), ruft bootstrap-skills.sh
# und druckt die verbleibenden manuellen Schritte (Obsidian-Plugins, creative-writing).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DRY=0; YES=0; SKIP_OLLAMA=0; SKIP_CLAUDE=0
OLLAMA_MODELS=(qwen2.5:14b llama3.1:8b bge-m3)
FORMULAE=(git python gh)
CASKS=(obsidian ollama)

usage() { cat <<'EOF'
setup.sh — macOS-Bootstrap (idempotent)

  bash scripts/setup.sh [Optionen]

Optionen:
  --dry-run       nur zeigen, was getan würde
  --yes, -y       nicht nachfragen (alle Installationen bestätigen)
  --skip-ollama   Ollama-Modelle nicht ziehen
  --skip-claude   Claude-Code-Hinweis überspringen
  -h, --help      diese Hilfe
EOF
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --yes|-y) YES=1 ;;
    --skip-ollama) SKIP_OLLAMA=1 ;;
    --skip-claude) SKIP_CLAUDE=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unbekannte Option: $arg" >&2; usage; exit 2 ;;
  esac
done

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '\033[32m%s\033[0m\n' "$*"; }
warn() { printf '\033[33m%s\033[0m\n' "$*"; }
die()  { printf '\033[31m%s\033[0m\n' "$*" >&2; exit 1; }

run() { if [ "$DRY" = 1 ]; then echo "[dry-run] $*"; else "$@"; fi; }
confirm() {
  [ "$YES" = 1 ] && return 0
  [ "$DRY" = 1 ] && return 0
  local a; read -r -p "$1 [y/N] " a; [[ "$a" =~ ^[yYjJ] ]]
}

[ "$(uname -s)" = "Darwin" ] || warn "Hinweis: für macOS gebaut — auf $(uname -s) ggf. anpassen."

command -v brew >/dev/null 2>&1 || die "Homebrew fehlt. Installieren:
  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"
danach setup.sh erneut ausführen."

ensure_formula() {
  local f="$1"
  if brew list --formula "$f" >/dev/null 2>&1 || command -v "$f" >/dev/null 2>&1; then
    ok "  ✓ $f"
  elif confirm "Formel '$f' installieren?"; then
    run brew install "$f"
  else
    warn "  übersprungen: $f"
  fi
}
ensure_cask() {
  local c="$1"
  if brew list --cask "$c" >/dev/null 2>&1; then
    ok "  ✓ $c"
  elif confirm "App '$c' (Cask) installieren?"; then
    run brew install --cask "$c"
  else
    warn "  übersprungen: $c"
  fi
}

bold "1) Homebrew-Pakete"
for f in "${FORMULAE[@]}"; do ensure_formula "$f"; done
for c in "${CASKS[@]}"; do ensure_cask "$c"; done

bold "2) Ollama-Modelle"
if [ "$SKIP_OLLAMA" = 1 ]; then
  warn "  übersprungen (--skip-ollama)"
elif command -v ollama >/dev/null 2>&1 || [ "$DRY" = 1 ]; then
  for m in "${OLLAMA_MODELS[@]}"; do run ollama pull "$m"; done
else
  warn "  'ollama' noch nicht im PATH — Ollama-App starten, dann: ollama pull ${OLLAMA_MODELS[*]}"
fi

bold "3) Codex-Skills (lokal verfügbar machen)"
if [ "$DRY" = 1 ]; then
  bash "$ROOT/scripts/bootstrap-skills.sh" --dry-run
else
  bash "$ROOT/scripts/bootstrap-skills.sh"
fi

if [ "$SKIP_CLAUDE" != 1 ]; then
  bold "4) Claude Code"
  if command -v claude >/dev/null 2>&1; then
    ok "  ✓ claude im PATH"
  else
    warn "  Claude Code installieren (offizieller Installer der Anthropic-Doku) und im Vault anmelden."
  fi
fi

echo
bold "Fast fertig — manuelle Restschritte:"
cat <<EOF
  • Obsidian öffnen → „Open folder as vault" → $ROOT → „Trust author and enable plugins"
  • Community plugins → Browse → installieren:
      obsidian-git, smart-connections, smart-composer, templater-obsidian, dataview,
      obsidian-excalidraw-plugin, obsidian-linter, obsidian-textgenerator-plugin, tag-wrangler, smart-lookup
  • Plugin-Settings: Smart Composer → Ollama; Templater → Ordner 12_Templates
    (Details: 00_Dashboard/Setup-auf-anderem-Rechner.md)
  • Prosa-Skills:  /plugin marketplace add haowjy/creative-writing-skills
                   /plugin install creative-writing-skills
  • Check:  bash scripts/check.sh
EOF
