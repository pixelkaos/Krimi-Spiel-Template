---
type: anleitung
status: canonical
tags: [artifact/dashboard, source/human]
---

# Validation → Check → Promotion (Step by Step)

Der Standard-Ablauf, **nachdem** ein generierender Skill (`crime-case-architect`,
`sandbox-calendar-builder`, `prose-writing` …) Entwürfe erzeugt hat — **bevor** etwas `canonical` wird.
Grundregel aus [[Entscheidungen-Designregeln]]: **Logik vor Prosa.**

---

## Phase 1 — Validation (Logik prüfen)

**A) Umschlag-Erreichbarkeit** (Sandbox-Spine):
```bash
python3 tools/frontmatter_to_validator_json.py envelopes
python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py tools/generated/envelope-manifest.json
```
Erwartet: `Envelope manifest validation passed.` → jeder kritische Umschlag ist erreichbar, jeder
Pflicht-Clue liegt in einem erreichbaren Umschlag.

**B) Truth-Map & Timeline** (Lösungs-Eindeutigkeit / Zeitlogik):
- Bequem über den Skill **`/deduction-consistency-auditor`** (argumentiert direkt über die Notizen), **oder**
- per JSON nach Vorlage (`tools/advent-crime-game-designer/assets/templates/`):
```bash
python3 tools/advent-crime-game-designer/scripts/validate_truth_map.py <truth-map.json>
python3 tools/advent-crime-game-designer/scripts/validate_timeline.py <timeline.json>
```
Erwartet: `… validation passed.` (Lösung eindeutig; niemand an zwei Orten gleichzeitig).

**C) Inhaltliches Logik-Audit:** `/deduction-consistency-auditor` → Report nach `10_QA/audit-NN.md`.
Prüft exklusive Plausibilität, Clue-Erreichbarkeit, Red-Herring-Fairness, Liar-Mechanik.

> **Bei Findings:** zurück zum Entwurf, beheben, Phase 1 wiederholen. **Erst wenn die Logik grün ist,
> geht es weiter** — eine spätere Prosa-Änderung darf die Clue-Semantik nie ohne erneuten Logik-Check ändern.

---

## Phase 2 — Check (Struktur & Konsistenz)

Dieselben Checks wie die CI, lokal:
```bash
python3 tools/check_frontmatter.py   # Pflicht: Frontmatter + Felder je type
python3 tools/check_links.py         # Pflicht: alle Wikilinks lösen auf
python3 tools/check_tags.py          # Pflicht: keine Tag-Kollisionen
python3 tools/check_orphans.py       # informativ: verwaiste Notizen
python3 tools/check_duplicates.py    # informativ: Near-Duplikate
```
Die ersten drei müssen **bestanden** melden. Häufige Fixe:
- `… kein 'type'` / `Pflichtfeld fehlt` → Frontmatter nach `12_Templates/` ergänzen.
- Meldung „unaufgelöster Wikilink" → Zielnotiz anlegen oder Linknamen korrigieren.
- `Tag-Kollision` → Schreibweise vereinheitlichen (`status/ artifact/ spoiler/ mechanic/ source/`).

---

## Phase 3 — Promotion (Entwurf → Kanon)

Pro freigegebener Notiz:
1. **Review:** `status: draft` → `status: needs-review`. Mensch prüft: Logik gegen Truth Map,
   Spoiler-Stufe korrekt (`player-safe`/`designer-only`/`finale`), Stimme passt (`stimme:`).
2. **Freigabe:** `status: needs-review` → `status: canonical`.
3. **Ort:** Atomare Entitäts-Notizen liegen schon in `04/05/07/08` → nur Status + Wikilinks prüfen,
   **kein Verschieben**. Notizen aus `11_Inbox/` oder `work/drafts/` ins Zielverzeichnis **verschieben**.
4. **Platzhalter ersetzen:** Sobald echte Figuren/Orte/Hinweise existieren, die Seeds
   (`Opfer-X`, `Verdaechtige-A`, `12-NW-Tatort`, `C001`, `T01-Start`) entfernen **und** die Verweise in
   `kb/canon.md` + den Canvas-Boards aktualisieren — sonst bricht der Link-Check.
5. **Planungs-Artefakte** (Manifest, Clue-Map aus `11_Inbox/`): als Referenz behalten oder nach `10_QA/`
   verschieben — sie sind selbst **kein** Kanon.

---

## Abschluss — Sync & CI
Obsidian Git committet/pusht automatisch (oder manuell im Source-Control-Panel). **GitHub Actions** prüft
Links/Frontmatter/Tags/Logik erneut. **Die Promotion gilt erst als abgeschlossen, wenn die CI grün ist.**

---

**Merksatz:** *Validieren (Logik) → Checken (Struktur) → Promovieren (Status + Links) → Sync (CI grün).
Nie `canonical` setzen, solange Validation oder Checks rot sind.*

Siehe auch [[Creative-Writing-Start]] · [[Projekt-Dashboard]]
