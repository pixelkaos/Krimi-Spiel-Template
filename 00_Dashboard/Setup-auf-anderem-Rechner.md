---
type: anleitung
status: canonical
tags: [artifact/dashboard, source/human]
---

# Projekt auf einem (anderen) Mac einrichten

> ⚙️ Vieles davon erledigt **`bash scripts/setup.sh`** für dich (Homebrew-Pakete, Ollama-Modelle,
> Codex-Skill-Kopie). Diese Seite erklärt den vollständigen, auch manuellen Weg. Ersetze
> `<DEIN-GITHUB>` / `<DEIN-PROJEKT>`.

## Was automatisch mitkommt vs. was neu nötig ist
- **Mit dem `git clone`:** alle Inhalte (00–14, `kb/`, `work/`, `tools/`, `CLAUDE.md`, Anleitungen,
  `scripts/`), Obsidian-Grundkonfig (Plugin-Liste, Appearance, Graph, Templates-Ordner), Codex-Tooling, CI.
- **Neu auf dem Rechner (gerätelokal, nicht im Repo):** die Plugin-Programmdateien **+ ihre
  Einstellungen** (Obsidian-Git-Auth, Smart Composer→Ollama, Templater-Ordner), Ollama-Modelle,
  Claude-Code-Plugin/Skills. Die KI-Indizes bauen sich automatisch neu.

---

# Teil A — Basis: Vault lesen/bearbeiten/syncen

## A1 · Software installieren (macOS)
```bash
# Homebrew (falls nicht vorhanden)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Git (oder via Xcode Command Line Tools: xcode-select --install)
brew install git
# Obsidian
brew install --cask obsidian
# (optional, erleichtert GitHub-Login)
brew install gh
```
> Kürzer: `bash scripts/setup.sh` installiert nur Fehlendes (nach Rückfrage).

## A2 · GitHub-Zugang
- **Einfach:** `gh auth login` (im Browser bestätigen) → danach `gh auth setup-git`.
- **Oder PAT** (falls dein Repo privat ist): GitHub → Settings → Developer settings → *Fine-grained token*
  (nur dieses Repo, Contents: Read/Write). Beim ersten Push/Pull als Passwort eingeben.

## A3 · Repo klonen
```bash
cd ~/Documents            # oder Wunschort
git clone https://github.com/<DEIN-GITHUB>/<DEIN-PROJEKT>.git
```

## A4 · Vault in Obsidian öffnen
Obsidian → **„Open folder as vault"** → den geklonten `<DEIN-PROJEKT>`-Ordner → **„Trust author and enable plugins"**.

## A5 · Community-Plugins installieren
Die Aktivierungs-Liste ist schon im Repo (`.obsidian/community-plugins.json`); nur die Programmdateien fehlen.
Settings → **Community plugins → Browse** → installieren:
`obsidian-git`, `smart-connections`, `smart-composer`, `templater-obsidian`, `dataview`,
`obsidian-excalidraw-plugin`, `obsidian-linter`, `obsidian-textgenerator-plugin`, `tag-wrangler`, `smart-lookup`.
(Nach Installation aktivieren sie sich automatisch, da in `community-plugins.json` gelistet.)

## A6 · Obsidian Git einrichten (Sync)
Der Clone ist bereits ein Git-Repo mit Remote → Obsidian Git nutzt das direkt.
Settings → **Obsidian Git**: *Auto commit-and-sync* ~10 min · *Push on commit* an · *Pull on startup* an.
Auth wie A2. Test: Befehl **„Obsidian Git: Pull"** und **„…: Commit-and-sync"**.

## A7 · Templater
Settings → **Templater** → *Template folder* = `12_Templates`.

> Damit kannst du Inhalte lesen, bearbeiten und mit anderen Geräten synchronisieren.

---

# Teil B — Optional: Voller KI-Workflow (Content-Erstellung)

## B1 · Ollama + Modelle
```bash
brew install --cask ollama        # danach Ollama starten (App)
ollama pull qwen2.5:14b           # Chat
ollama pull llama3.1:8b           # Apply-Edits
ollama pull bge-m3                # Embeddings (Smart Composer)
```
> `scripts/setup.sh` zieht diese Modelle ebenfalls (außer mit `--skip-ollama`).

## B2 · In-Vault-KI-Plugins konfigurieren (Einstellungen sind NICHT mitsynct)
- **Smart Composer** → Settings: Provider **Ollama** (`http://localhost:11434`), Chat `qwen2.5:14b`,
  Apply `llama3.1:8b`, Embedding `bge-m3`; Excludes: `tools/`, `14_attachments/`, `build/`.
- **Smart Connections** → Offline-Embedding (Default, lokal) oder Ollama.
- **Text Generator** (optional) → Provider Ollama.

## B3 · Claude Code + Skills
- Claude Code installieren (offizieller Installer/Brew-Cask), dann im Vault anmelden.
- **creative-writing-skills** (global): in Claude Code
  `/plugin marketplace add haowjy/creative-writing-skills` → `/plugin install creative-writing-skills`.
- **Codex-Skills** aus dem Repo global verfügbar machen — am einfachsten:
```bash
bash scripts/bootstrap-skills.sh
```
  (Kopiert die 4 Skills nach `~/.claude/skills/` und setzt die Referenzpfade auf diesen Clone.)

## B4 · Python (für lokale Checks/Validatoren — optional, CI läuft ohnehin auf GitHub)
macOS bringt `python3` mit (sonst `brew install python`). Es ist **nur die Standardbibliothek** nötig.

## B5 · Arbeiten
Claude Code **im Vault-Ordner** öffnen (`cd ~/Documents/<DEIN-PROJEKT> && claude`, lädt `CLAUDE.md`), dann
`/cw-muse` + Phasen-Skills. Ablauf: siehe `00_Dashboard/Creative-Writing-Start.md` und
`00_Dashboard/Validation-Check-Promotion.md`.

---

# Verifikation
```bash
cd ~/Documents/<DEIN-PROJEKT>
bash scripts/check.sh                 # check_frontmatter / check_links / check_tags „bestanden"
git pull --no-rebase && git status    # Sync ok, sauber
```
In Obsidian: Smart-Composer-Chat gegen Ollama (kein API-Key-Fehler) · Obsidian Git „Pull/Commit-and-sync" ·
Templater „Insert template" zeigt `12_Templates` · Bases-Ansichten (`13_Bases`) rendern.

# Wichtige Hinweise
- **Nie gleichzeitig** dieselbe Notiz offline auf zwei Rechnern ändern → vor dem Editieren `pull`, danach
  `push` (vermeidet Git-Konflikte). Im Zweifel ein Rechner pro Session.
- Plugin-**Einstellungen** (`data.json`) und KI-**Indizes** sind bewusst gerätelokal (gitignored) →
  pro Rechner einmal konfigurieren; Indizes bauen sich automatisch neu.
- Die `.obsidian`-Grundkonfig kommt mit dem Clone → du musst nur die Plugins **installieren** und die
  KI-/Git-Settings setzen.
