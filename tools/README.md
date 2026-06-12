# tools/ — Validatoren & Checks

Nur Python-Standardbibliothek (kein pip nötig). Läuft lokal am Mac und in GitHub Actions.

## Eigene Checks (gating in CI)

| Skript | Zweck | Gating |
|---|---|---|
| `check_links.py` | Alle `[[Wikilinks]]` lösen auf (ignoriert `12_Templates`, `tools`). | ja |
| `check_frontmatter.py` | Frontmatter + `type` in `00/01/03/06/09/10` (rekursiv) + Pflichtfelder je Typ in `04/05/07/08`. | ja |
| `check_tags.py` | Tag-Kollisionen (Tippfehler/Varianten) = Fehler; unbekannte Präfixe = Warnung. | ja (nur Kollisionen) |
| `check_orphans.py` | Inhalts-Notizen ohne ein-/ausgehende Links. | informativ |
| `check_duplicates.py` | Near-Duplikate via Jaccard-Shingles (keine Embeddings nötig). | informativ |
| `frontmatter_to_validator_json.py` | Brücke: erzeugt `tools/generated/envelope-manifest.json` aus `08_Umschlaege`. | — |

```bash
python3 tools/check_links.py
python3 tools/check_frontmatter.py
python3 tools/frontmatter_to_validator_json.py envelopes
python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py tools/generated/envelope-manifest.json
```

> Hinweis: `fuehrt_zu` in Umschlägen darf Orte **und** Umschläge nennen; für den Erreichbarkeits-Check
> werten nur Verweise auf andere **Umschläge**.

## Codex-Engine (`advent-crime-game-designer/`)

Generische Methodik + Logik-Validatoren (siehe Plan §18). Templates/Beispiele in `assets/templates/`.

```bash
python3 tools/advent-crime-game-designer/scripts/validate_truth_map.py        <truth-map.json>
python3 tools/advent-crime-game-designer/scripts/validate_timeline.py         <timeline.json>
python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py <envelopes.json>
```

Die zugehörigen **Skills** (`crime-case-architect`, `sandbox-calendar-builder`,
`deduction-consistency-auditor`, `research-backed-story-planner`) sind nach `~/.claude/skills/`
kopiert und für Claude Code direkt aufrufbar. Das Plugin ist via `.claude-plugin/plugin.json`
zusätzlich als installierbares Claude-Code-Plugin verpackt.
