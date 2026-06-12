---
type: regeln
status: canonical
tags: [artifact/design-rule, source/human]
---

# Designregeln (kanonisch)

## Kern-Designprinzipien
- **Geschlossener Kreis:** 3–8 Verdächtige, isoliertes Umfeld.
- **Exklusive Plausibilität:** Die beabsichtigte Lösung ist die *einzige* widerspruchsfreie Erklärung.
- **Rückwärts plotten:** zuerst die objektive Tat, dann der Ermittlungspfad.
- **Zwei Zeitleisten:** [[Tat-Zeitleiste]] (objektiv) + [[Ermittlungs-Zeitleiste]] (Spielersicht).
- **Branch-and-Bottleneck:** freie Reihenfolge innerhalb kontrollierter Pacing-Gates.
- **Jeder Hinweis hat eine Funktion** (beweist/widerlegt/verbindet/öffnet) oder ist als red-herring/atmosphere markiert.
- **Rote Heringe brauchen einen fairen Exit.**

## Arbeitsregeln (gegen KI-Wildwuchs)
- KI-Entwürfe landen **immer** in `11_Inbox` mit `status: draft`, `source: ai`.
- **Promotion-Ritual:** `needs-review` → `canonical` + Verschieben in Zielordner + Wikilinks.
- Eine Prosa-Änderung darf nie die Clue-Semantik ändern, ohne die Logik-Checks erneut laufen zu lassen.
- CI-Gates (GitHub Actions) müssen grün sein, bevor `canonical` gesetzt wird.

## Entscheidungs-Log
Eine Notiz pro Entscheidung in `01_Regeln/Entscheidungs-Log/` (Template: `entscheidung`).
