---
type: anleitung
status: canonical
tags: [artifact/dashboard, source/human]
---

# Creative-Writing — Schnellstart (Step by Step)

Kurzanleitung, um mit dem `creative-writing-skills`-Plugin Inhalte zu erstellen.

## 0. Voraussetzung (einmal pro Session)
Claude Code **im Vault-Ordner** starten — sonst findet es `CLAUDE.md`, `kb/`, `work/` & Kanon nicht:
```bash
cd ~/Documents/<DEIN-PROJEKT> && claude
```
Beim Start lädt Claude automatisch `CLAUDE.md` (Projektregeln + Stimmen-Modell).

## 1. Kreativ-Lead aktivieren
Tippe: **`/cw-muse`** — das ist der Einstiegs-Agent. Er brainstormt, entwirft, kritisiert, überarbeitet
und pflegt die `kb/`. Sag ihm in einem Satz, was du willst (z. B. „Lass uns die Fallbibel anlegen").

## 2. Erst Logik, dann Prosa (wichtig!)
Bevor Text geschrieben wird, die **Fallwahrheit** festlegen:
- Skill **`/crime-case-architect`** → Opfer · Täter:in · Methode · Motiv (rückwärts geplottet) → MOCA → Truth Map.
- Ergebnis landet in [[Fallbibel]] + `04_Figuren`/`05_Orte`/`07_Hinweise`.

## 3. Prosa entwerfen (in die Kladde)
- Muse/`writer` schreibt Entwürfe nach **`work/drafts/`** (Scratch, wird nicht geprüft).
- **Stimme wählen** (Frontmatter `stimme:`): `spielleiter` (ihr als Erzähler), `dokument` (Zeitung/Brief/Protokoll), `erzaehler3` (3. Person). Details: `kb/styles/`.
- Ton: gemütlich-ironisch, Anrede **Du** (steht in `CLAUDE.md`).

## 4. Kritik & Überarbeitung
- **`/prose-critique`** bzw. der `critic`/`reader-sim`-Agent liest gegen die vier Leser-Kanäle.
- **`continuity-checker`** prüft gegen den Kanon (Widersprüche/Timeline).
- Iterieren, bis es sitzt.

## 5. Logik-Gegencheck (vor „canonical")
- **`/deduction-consistency-auditor`** + Validatoren:
```bash
python3 tools/frontmatter_to_validator_json.py envelopes
python3 tools/advent-crime-game-designer/scripts/validate_truth_map.py <truth-map.json>
```
- Regel: Eine Prosa-Änderung darf **nie** die Clue-Semantik ändern, ohne diese Checks erneut laufen zu lassen.

## 6. Promotion (Entwurf → Kanon)
Wenn gut: `status: needs-review` → nach Freigabe `status: canonical`, Notiz aus `work/`/`11_Inbox` in den
Zielordner verschieben (z. B. `08_Umschlaege`), **Wikilinks** setzen.

## 7. Speichern & synchen
- Obsidian Git committet/pusht automatisch (alle 10 min + beim Schließen) — oder im Source-Control-Panel manuell.
- GitHub Actions prüft danach Links/Frontmatter/Tags/Logik.

## 8. Wissen sichern (optional)
- **`/style-analysis`** aus ersten echten Texten → verfeinert die Stil-Dateien in `kb/styles/`.
- **`/kb-management`** hält `kb/` (Vokabular, Stil) sauber. Prosa-Probleme → `kb/issues/`, Logikfehler → `10_QA`.

---
**Merksatz:** im Vault starten → `/cw-muse` → erst Logik (`crime-case-architect`) → Prosa in `work/` (Stimme wählen) → Kritik → Logik-Recheck → Promotion → Sync.
Siehe auch [[Projekt-Dashboard]].
