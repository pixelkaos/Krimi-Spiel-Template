---
type: dashboard
status: canonical
tags: [artifact/dashboard]
---

# 🎄 Projekt-Dashboard

**Aktuelle Phase:** Greenfield — _Fallwahrheit festlegen_ (zuerst [[Fallbibel]] mit `/crime-case-architect`).

## Risikoampel
| Bereich | Status |
|---|---|
| Lösungs-Exklusivität (Truth Map) | 🟡 offen |
| Zeitlogik (Zeitleisten) | 🟡 offen |
| Umschlag-Erreichbarkeit | 🟡 offen |
| Produktion/Druck | ⚪ später |

## Kernartefakte
- [[Fallbibel]] · [[Entscheidungen-Designregeln]]
- Figuren → Ordner `04_Figuren` · Orte → `05_Orte` · Hinweise → `07_Hinweise` · Umschläge → `08_Umschlaege`
- Zeitleisten: [[Tat-Zeitleiste]] · [[Ermittlungs-Zeitleiste]]

## KI-Drafts in Review (Inbox)
```dataview
TABLE status, source, file.mtime AS "geändert"
FROM "11_Inbox"
WHERE status = "draft"
SORT file.mtime DESC
```

## Offene Hinweise ohne Wahrheit
```dataview
TABLE deduktionsfunktion, pflicht
FROM "07_Hinweise"
WHERE wahrheit = "" OR wahrheit = null
```

> Dataview-Blöcke zeigen Inhalte erst nach Installation des Dataview-Plugins (siehe `README.md` → Quick-Start).
