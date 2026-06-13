---
type: zeitleiste
zeitleiste_art: objektiv
status: draft
tags: [artifact/timeline, mechanic/truth-map, source/human]
---

# Tat-Zeitleiste (Story of the Crime — objektiv)

> Die tatsächlichen, objektiven Ereignisse. Muss zeitlich/räumlich widerspruchsfrei sein.
> Maschinelle Prüfung: `python3 tools/frontmatter_to_validator_json.py timeline`
> → `python3 tools/advent-crime-game-designer/scripts/validate_timeline.py tools/generated/timeline.json`.
>
> **Tabellen-Konvention** (der Adapter erkennt Spalten an der Überschrift — Reihenfolge egal,
> Zusatzspalten erlaubt):
> - **Start** (und optional **Ende**) als ISO: `2026-12-01T20:00`. *Ende* ist nötig, damit
>   Überlappungen (jemand gleichzeitig an zwei Orten) erkannt werden.
> - **Akteure**: mehrere mit Komma/Semikolon trennen. **Ort**: ein Ort pro Zeile.
> - Optional **ID** (sonst automatisch `E001…`) und **Overlap?** (`ja`, wenn Gleichzeitigkeit gewollt ist).
> - Beispielzeile: `| E001 | 2026-12-01T20:00 | 2026-12-01T20:30 | Person A | Ort X | … |`
> - Leere Zeilen (ohne Start) werden ignoriert — die Tabelle darf also im Aufbau leer bleiben.

| ID | Start | Ende | Akteure | Ort | Ereignis | Spur hinterlassen | Wer weiß es |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |
