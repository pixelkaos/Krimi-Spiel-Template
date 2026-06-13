# tools/ — Validatoren & Checks

Nur Python-Standardbibliothek (kein pip nötig). Läuft lokal am Mac und in GitHub Actions.

## Eigene Checks (gating in CI)

| Skript | Zweck | Gating |
|---|---|---|
| `check_links.py` | Alle `[[Wikilinks]]` lösen auf (ignoriert `12_Templates`, `tools`). | ja |
| `check_frontmatter.py` | Frontmatter **Pflicht** in allen Inhaltsordnern `00–10` (rekursiv); `type` empfohlen (sonst Warnung); Pflichtfelder **strikt** je `type` (figur/ort/hinweis/umschlag). | ja |
| `check_tags.py` | Tag-Kollisionen (Tippfehler/Varianten) = Fehler; unbekannte Präfixe = Warnung. | ja (nur Kollisionen) |
| `check_orphans.py` | Inhalts-Notizen ohne ein-/ausgehende Links. | informativ |
| `check_duplicates.py` | Near-Duplikate via Jaccard-Shingles (keine Embeddings nötig). | informativ |
| `frontmatter_to_validator_json.py` | Brücke: `envelopes` → `tools/generated/envelope-manifest.json` (aus `08_Umschlaege`); `timeline` → `tools/generated/timeline.json` (aus `06_Zeitleisten`). | — |
| `check_all.py` | Sammel-Runner: alle Gating- + informativen Checks in einem Befehl (lokale CI-Parität). | ja (Summe) |
| `tests/run_tests.py` | Tests der Adapter-Logik (listvals/scalar + Zeitleisten-Fixtures). | — |

```bash
python3 tools/check_all.py            # alle Checks auf einmal (empfohlen)

# oder einzeln:
python3 tools/check_links.py
python3 tools/check_frontmatter.py
python3 tools/frontmatter_to_validator_json.py envelopes
python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py tools/generated/envelope-manifest.json
python3 tools/frontmatter_to_validator_json.py timeline
python3 tools/advent-crime-game-designer/scripts/validate_timeline.py tools/generated/timeline.json
```

> Hinweis: `fuehrt_zu` in Umschlägen darf Orte **und** Umschläge nennen; für den Erreichbarkeits-Check
> werten nur Verweise auf andere **Umschläge**.

## Codex-Engine (`advent-crime-game-designer/`)

Generische Methodik + Logik-Validatoren (siehe Plan §18). Templates/Beispiele in `assets/templates/`.

```bash
python3 tools/advent-crime-game-designer/scripts/validate_truth_map.py        <truth-map.json>
python3 tools/advent-crime-game-designer/scripts/validate_timeline.py         <timeline.json>
python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py <envelopes.json>
python3 tools/advent-crime-game-designer/scripts/validate_exclusion.py        <exclusion.json>
```

> **Einordnung der Logik-Validatoren:** Für den **Einzeltäter-Fall** (1 von n) ist **`validate_exclusion.py`**
> das passende Werkzeug — es prüft, dass genau eine:r übrig bleibt (alle anderen per Clue ausgeschlossen)
> und die Ausschluss-Clues erreichbar sind (Input: JSON, z. B. vom `/deduction-consistency-auditor` erzeugt).
> `validate_truth_map.py` modelliert dagegen ein **Latin-Square** (jede Kategorie 1:1) und ist nur für
> optionale Teilrätsel gedacht (ab ~7 Verdächtigen × ≥2 Kategorien über dem Suchraum-Limit).
> Maschineller Logik-Kern: **Umschlag-Erreichbarkeit** + **Tat-Zeitleiste** + **validate_exclusion** + Skill
> **`/deduction-consistency-auditor`** (argumentativ).

Die zugehörigen **Skills** (`crime-case-architect`, `sandbox-calendar-builder`,
`deduction-consistency-auditor`, `research-backed-story-planner`) sind nach `~/.claude/skills/`
kopiert und für Claude Code direkt aufrufbar. Das Plugin ist via `.claude-plugin/plugin.json`
zusätzlich als installierbares Claude-Code-Plugin verpackt.
