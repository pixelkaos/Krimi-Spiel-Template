# <DEIN-PROJEKT> — Projektkonventionen

_Liest jede:r Claude-Code-Agent (inkl. `cw-muse` & creative-writing-skills) für projektspezifische Regeln._

> ⚙️ Aus der Vorlage **Krimi-Spiel-Template**. Ersetze `<DEIN-PROJEKT>` / `<DEIN-GITHUB>` und passe
> Überblick, Stimme & Ton an deinen Fall an. Struktur, Workflow und Logik-Layer können so bleiben.

## Projektüberblick
Analoger **Krimi-Adventskalender** (SHCD-Stil, 24 Sandbox-Umschläge), **deutschsprachig**.
Greenfield-Obsidian-Vault aus dem Template **Krimi-Spiel-Template**. Single Source of Truth =
GitHub-Repo `<DEIN-GITHUB>/<DEIN-PROJEKT>` (privat oder öffentlich).

## ⚠️ Arbeitsverzeichnis
Dieses Projekt **ist** der Vault-Ordner (der geklonte Repo-Ordner, z. B. `~/Documents/<DEIN-PROJEKT>`).
`cw-muse` und alle Agenten **müssen mit diesem Ordner als Arbeitsverzeichnis laufen** (Claude Code hier
öffnen) — sonst finden sie `kb/`, `work/` und den Kanon nicht.

## Sprache
Alle Prosa & Inhalte auf **Deutsch**. (Die Skill-Methodik ist intern englisch — der Output ist immer Deutsch.)

## Struktur — wo liegt was (WICHTIG: nicht duplizieren!)
**Kanon** liegt in den nummerierten Ordnern, **nicht** in `kb/`:

| Inhalt | Autoritativer Ort |
|---|---|
| Fallwahrheit / Kanon | `03_Fallbibel` |
| Figuren / MOCA | `04_Figuren` |
| Orte / Knoten | `05_Orte` |
| Zeitleisten (Tat + Ermittlung) | `06_Zeitleisten` |
| Hinweise / Clue Ledger | `07_Hinweise` |
| Umschläge (Spielmaterial) | `08_Umschlaege` |
| Produktion (Zeitungen/Props) | `09_Produktion` |
| QA / Playtest (Logik) | `10_QA` |

**Schreib-Handwerks-Ebene** (für die cw-Agenten):

| Ort | Zweck |
|---|---|
| `kb/styles/` | Stil-/**Stimmen**-Dateien (Voice) |
| `kb/samples/` | Schreibproben → Input für `style-analysis` |
| `kb/vocab.md` | gemeinsames Vokabular / Begriffe |
| `kb/issues/` | **Prosa-/Craft**-Probleme (`writing-issues`) — Logikfehler dagegen → `10_QA` |
| `kb/canon.md` | Index/Verweis auf den Kanon oben (keine Kopie!) |
| `work/` | Kladde: `outline/ drafts/ critique-reports/ brainstorm/` |

**Manuskript/Prosa** = die Texte in `08_Umschlaege` (Umschlag-Bodies) + `09_Produktion` (Zeitungen).
Es gibt bewusst **kein** separates `story/`.

## Stimme & Ton
> Sinnvoller Default — **nach Geschmack anpassen.**

Grundton: **gemütlich-ironisch, SHCD-nah, erwachsen, nie brutal, fair-play.** Spieleransprache: **Du / Ihr.**

**Mehrere Erzählperspektiven — umschaltbar pro Artefakt** (Details + Beispiele in `kb/styles/`):
1. **Spielleiter-Wir** (`stimme: spielleiter`) — 1. Person Plural, „wir" = die Spielleitung, adressiert „ihr/Du". Für Begrüßung, Tagesintros, Hinweis-Leiter, Auflösung, Zwischenkommentare.
2. **Dokument/diegetisch** (`stimme: dokument`) — In-World-Artefakte mit eigenem Register (Zeitung journalistisch, Brief persönlich, Protokoll behördlich), meist 3. Person/neutral. Der **Beweis-Kern**: spoiler-sicher & clue-präzise.
3. **Erzähler 3. Person** (`stimme: erzaehler3`) — neutral-atmosphärische Verbindungsszenen/Ortsbeschreibungen.

Jede **Prosa**-Notiz markiert ihre Stimme im Frontmatter: `stimme: spielleiter | dokument | erzaehler3`.

## Workflow & Konventionen
- **KI-Entwürfe** zuerst in die Kladde: Spiel-Entitäten → `11_Inbox` (`status: draft`, `source: ai`); reine **Prosa** → `work/drafts/`.
- **Promotion-Ritual:** Review → `status: needs-review` → nach Freigabe `status: canonical` + in Zielordner verschieben + Wikilinks setzen. **Nichts wird Kanon ohne diesen Schritt.**
- **Logik vor Prosa:** Eine Prosa-Änderung darf **nie** die Clue-Semantik ändern, ohne die Logik-Checks erneut laufen zu lassen (Codex-Layer unten).
- **Spoiler:** Frontmatter `spoiler: player-safe | designer-only | finale`. Player-facing Texte verraten **nie** Täter:in/Methode/heikle Hintergründe vor dem geplanten Reveal.
- **Tags:** `status/ · artifact/ · spoiler/ · mechanic/ · source/` (Schema in `01_Regeln`).
- **Naming:** Hinweise `C0xx`, Umschläge `T01–T24`, Figuren lesbar, Orte „`<KnotenID> – <Ort>`".
- **Frontmatter `type` (Pflicht):** Jede Notiz trägt ein `type:` — `figur/ort/hinweis/umschlag` für Spiel-Entitäten (mit Pflichtfeldern, siehe `12_Templates/`), sonst frei (z. B. `fallbibel`, `moca`, `audit`, `zeitleiste`, `regeln`, `anleitung`). Verhindert CI-Warnungen und speist Bases/Graph.

## Logik-/QA-Layer (Codex) — vor „canonical" für Fall-Logik
- **Skills:** `crime-case-architect`, `deduction-consistency-auditor`, `sandbox-calendar-builder`, `research-backed-story-planner`.
- **Validatoren:** `tools/advent-crime-game-designer/scripts/validate_{truth_map,timeline,envelope_manifest}.py` + `tools/check_*.py`. **CI:** GitHub Actions (`.github/workflows/checks.yml`).

## Drei-Schichten-Zusammenspiel
**Logik** (Codex: Wahrheit/MOCA/Truth-Map/Erreichbarkeit) → **Prosa** (creative-writing: Umschlag-/Zeitungstext, Figurenstimmen, Kritik/Kontinuität) → **Workspace** (Obsidian + Git/CI). Reihenfolge im Zweifel: erst Logik fixieren, dann Prosa.

Gemeinsames Vokabular: siehe `kb/vocab.md`.
