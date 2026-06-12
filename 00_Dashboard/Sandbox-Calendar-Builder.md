---
type: anleitung
status: canonical
tags: [artifact/dashboard, source/human]
---

# Sandbox-Calendar-Builder — Start-Prompt (generisch)

> ⚙️ **Vorlage.** Kopiere diesen Prompt in eine Claude-Code-Session (im Vault) und führe ihn mit
> `/sandbox-calendar-builder` aus, **nachdem** die Fallwahrheit in [[Fallbibel]] steht. Ersetze die
> `<…>`-Platzhalter. Alle Ausgaben auf Deutsch.

---

Fall: „<Arbeitstitel>". Format: Sandbox-Kalender — 24 koordinaten-/institutionsbasierte Umschläge,
Spieler:innen wählen die Reihenfolge frei, mit Tages-Zeitbudget. Alle Ausgaben auf Deutsch.

Lies als verbindliche Grundlage:
- Kanon (Wahrheit): `03_Fallbibel/Fallbibel.md` — inkl. eures Designprinzips
- Verdächtige/MOCA: Ordner `04_Figuren/`
- Dramaturgie: euer Spannungsbogen in `work/outline/`
- Schauplätze/Atmosphäre: Recherche in `02_Quellen/`
- Logik-Audit: zuletzt erzeugter Report in `10_QA/`
- Konventionen/Schema: `CLAUDE.md`, `12_Templates/` (figur/ort/hinweis/umschlag), `kb/vocab.md`

Erzeuge:
1. START-PAKET (Tag 1):
   Regelheft, Stadtplan-Konzept (Koordinaten-Quadranten), Adressbuch-Logik,
   erste Zeitung, Fall-Briefing, Notizblatt.
2. 24-UMSCHLAG-MANIFEST:
   pro Umschlag → ID (T01–T24), Label (Koordinate oder Institution),
   Unlock-Tag, Zeitkosten, Inhalt/Beilagen, enthaltene Clue-IDs, „führt-zu" (Folge-Knoten),
   entry_point? (Start), kritisch? (Teil des Pflicht-Spine).
3. PACING/BOTTLENECKS:
   Tages-Zeitbudget; Zeitungs-Erscheinungstage als Gates, gekoppelt an die Wendepunkte
   aus eurem Spannungsbogen (Midpoint ~Tag 12, Krise ~Tag 20–22); Meilenstein-Checks.
4. CLUE-DEPENDENCY-MAP:
   jeder kritische Hinweis ist erreichbar; kein Pflicht-Hinweis hinter
   optionalem Lock; jeder Rote Hering hat einen fairen Exit-Hinweis.
5. HINT-LEITER:
   3 gestaffelte, spoilerarme Tipps pro Rätsel + separater, versiegelter
   AUFLÖSUNGS-Umschlag (erst nach Tippabgabe zu öffnen).
6. ATOMARE NOTIZEN anlegen (exakt nach `12_Templates/` + Frontmatter-Schema; status: draft, source: ai):
   - 04_Figuren/:
     eine Notiz pro Verdächtigem/Zeugen (type: figur, Pflichtfelder rolle/status/spoiler/…) —
     ersetzt die Platzhalter Opfer-X/Verdaechtige-A.
   - 05_Orte/:
     eine Notiz pro Schauplatz/Knoten (type: ort, Rolle H=Pflicht/S=Bonus/R=Red-Herring,
     unlock, beweise, exit_hinweis bei Red Herrings).
   - 07_Hinweise/:
     eine Notiz pro Hinweis (Dateiname = C001…, type: hinweis, beweisart, deduktionsfunktion,
     quelle_knoten, moca_zelle, pflicht).
   - 08_Umschlaege/:
     eine Notiz pro Umschlag (T01–T24, type: umschlag, tag, label, entry_point,
     kritisch, zeitkosten, clues, fuehrt_zu, spoiler, produktionsstatus).

   Wikilinks zwischen Umschlag → Ort → Hinweis → Figur durchgängig setzen.

Zwingend beachten:
- **Exklusive Plausibilität** wahren: Die beabsichtigte Lösung bleibt die einzige widerspruchsfreie
  Erklärung. Falls ihr mit „Restunsicherheit" arbeitet, liefert KEIN Umschlag den letzten,
  unwiderlegbaren Beweis — der entscheidende Schritt bleibt Spieler-Synthese.
- Die Unschuldigen bleiben sauber ausschließbar (harte Alibis / fehlender Zugang zum echten Tatort).
- Spoiler: player-facing Umschläge & Zeitung verraten NIE Täter:in/Methode/heikle Hintergründe vor
  dem geplanten Reveal (spoiler: player-safe für Spielertexte, designer-only/finale für den Rest).
- Tägliche Spielzeit ~10–20 Minuten.

Ausgabe-Orte:
- Planungs-Artefakte (Manifest, Clue-Dependency-Map, Pacing, Hint-Leiter) → 11_Inbox/ (status: draft, source: ai)
- Atomare Notizen → direkt in 04/05/07/08 (status: draft, source: ai)

Zum Schluss:
- Liste offener Design-Risiken.
- Sag mir, welche Checks als Nächstes laufen sollten:
  python3 tools/frontmatter_to_validator_json.py envelopes
  python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py tools/generated/envelope-manifest.json
  + /deduction-consistency-auditor (Re-Audit) — erst danach Promotion zu status: canonical.
