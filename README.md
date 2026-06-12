# Krimi-Spiel-Template

Eine **wiederverwendbare Greenfield-Vorlage** für ein analoges **Krimi-Adventskalender-Rätselspiel**
(SHCD-Stil, 24 Sandbox-Umschläge) — gebaut als **Obsidian-Vault + Claude-Code-Workflow + lokale KI**.

Das Template liefert die komplette **Struktur, das Tooling, die Logik-Skills und die Setup-Automatik** —
**ohne Story-Inhalte**. Du startest mit deiner eigenen Fall-Idee.

> **„Use this template"** auf GitHub (oder klonen) → `bash scripts/setup.sh` → Plugins per Obsidian-GUI
> installieren → Vault öffnen → mit `/cw-muse` + `/crime-case-architect` deinen **neuen** Fall plotten.

---

## Quick-Start

1. **Repo holen**
   - GitHub: **„Use this template" → Create a new repository**, dann klonen, **oder**
   - direkt: `git clone https://github.com/<DEIN-GITHUB>/<DEIN-PROJEKT>.git && cd <DEIN-PROJEKT>`
2. **Voraussetzungen installieren** (macOS, idempotent, fragt vor jeder Installation):
   ```bash
   bash scripts/setup.sh           # Homebrew-Pakete, Ollama-Modelle, Codex-Skills
   bash scripts/setup.sh --dry-run # vorher ansehen, was es täte
   ```
3. **Obsidian-Plugins installieren** (1 Klick je Plugin — sie sind in `.obsidian/community-plugins.json`
   vorgelistet, aktivieren sich also automatisch): Settings → *Community plugins → Browse* →
   `obsidian-git`, `smart-connections`, `smart-composer`, `templater-obsidian`, `dataview`,
   `obsidian-excalidraw-plugin`, `obsidian-linter`, `obsidian-textgenerator-plugin`, `tag-wrangler`, `smart-lookup`.
   Details/Einstellungen: `00_Dashboard/Setup-auf-anderem-Rechner.md`.
4. **Vault öffnen**: Obsidian → *Open folder as vault* → dieser Ordner → *Trust author and enable plugins*.
5. **Loslegen**: Claude Code **im Vault-Ordner** starten (`claude`), dann
   `/cw-muse` → `/crime-case-architect` (Fallwahrheit) → `/sandbox-calendar-builder` (24 Umschläge).
   Anleitung: `00_Dashboard/Creative-Writing-Start.md`.

---

## Drei-Schichten-Modell

| Schicht | Werkzeug | Aufgabe |
|---|---|---|
| **Logik** | Codex-Skills + Validatoren (`tools/advent-crime-game-designer/`) | Fallwahrheit, MOCA, Truth-Map, Umschlag-Erreichbarkeit |
| **Prosa** | `creative-writing-skills` (`/cw-muse` …) | Umschlag-/Zeitungstexte, Figurenstimmen, Kritik, Kontinuität |
| **Workspace** | Obsidian + Git + GitHub Actions | Schreiben, Verlinken, Sync, CI-Checks |

Grundregel: **erst Logik fixieren, dann Prosa.** Single Source of Truth = dein GitHub-Repo (server-frei).

---

## Ordnerstruktur

| Ordner | Inhalt |
|---|---|
| `00_Dashboard` | Einstieg, Dashboard, Anleitungen, Canvas-Boards |
| `01_Regeln` | Designregeln + Entscheidungs-Log |
| `02_Quellen` | Recherche (startet leer) |
| `03_Fallbibel` | Kanon-Wahrheit (Skelett zum Ausfüllen) |
| `04_Figuren` | eine Notiz pro Figur (MOCA) — mit generischen Beispiel-Seeds |
| `05_Orte` · `06_Zeitleisten` · `07_Hinweise` · `08_Umschlaege` | Knoten · Zeitleisten · Clues · Umschläge (T01–T24) |
| `09_Produktion` · `10_QA` | Props/Zeitungen · Playtests/Audits |
| `11_Inbox` | **alle KI-Drafts landen hier zuerst** (`status: draft`) |
| `12_Templates` · `13_Bases` · `14_attachments` | Templater-Vorlagen · Datenbank-Ansichten · kleine Bilder |
| `kb/` | Schreib-Handwerk: Stimmen (`styles/`), Vokabular, Proben, Issues, Kanon-Index |
| `work/` | Kladde: `outline/ drafts/ critique-reports/ brainstorm/` |
| `tools/` | Codex-Validatoren + `check_*.py` (Links/Frontmatter/Tags) |
| `scripts/` | Setup-/Check-/New-Case-Automatik (siehe unten) |

> **Generische Seeds** (`Opfer-X`, `Verdaechtige-A`, `12-NW-Tatort`, `C001`, `T01-Start`) zeigen das
> Frontmatter-Schema und halten Checks/Canvas grün. **Löschen, sobald echte Notizen entstehen** —
> bequem per `bash scripts/new-case.sh --blank`.

---

## Skripte (`scripts/`)

| Skript | Zweck |
|---|---|
| `setup.sh` | macOS-Bootstrap: installiert nur Fehlendes (`git`, `python`, `gh`, Obsidian, Ollama, Claude Code), zieht die Ollama-Modelle, ruft `bootstrap-skills.sh`. Flags: `--dry-run --yes --skip-ollama --skip-claude`. |
| `bootstrap-skills.sh` | Kopiert die 4 Codex-Skills nach `~/.claude/skills/` und setzt die Referenzpfade auf diesen Clone. |
| `check.sh` | Lokale CI-Parität: `check_frontmatter` / `check_links` / `check_tags` (Gating) + Orphans/Duplikate (informativ). |
| `new-case.sh` | Setzt die Story auf leere Skelette zurück (`--keep-seeds` Default · `--blank` entfernt auch die Seeds). |

`make setup` · `make check` · `make new-case` rufen dieselben Skripte.

---

## Automatisiert vs. manuell

| Schritt | Wie |
|---|---|
| Homebrew-Pakete, Ollama-Modelle, Codex-Skill-Kopie | **automatisch** (`scripts/setup.sh`) |
| Struktur/Checks lokal prüfen | **automatisch** (`scripts/check.sh`) · CI auf GitHub |
| Obsidian-Plugin-**Programmdateien** | **manuell** (GUI „Browse" — bewusst kein Code-Download per Skript) |
| Plugin-**Einstellungen** (Git-Auth, Smart Composer→Ollama, Templater-Ordner) | **manuell** (gerätelokal, nicht im Repo) |
| Fall erfinden & schreiben | **du** + `/cw-muse` & die Skills |

---

## Weiterführend
- `00_Dashboard/Creative-Writing-Start.md` — Schnellstart für den Schreib-Workflow.
- `00_Dashboard/Validation-Check-Promotion.md` — Logik validieren → Struktur prüfen → Kanon promovieren.
- `00_Dashboard/Setup-auf-anderem-Rechner.md` — vollständige (auch manuelle) Einrichtung.
- `CLAUDE.md` — Projektkonventionen, die jede:r Claude-Code-Agent liest.

Viel Spaß beim Plotten. 🕵️
