#!/usr/bin/env python3
"""Erwartungs-Orakel für die Obsidian-Bases.

Spiegelt die Filter jeder Base in Python und druckt pro Base/View die erwartete
Dateiliste + Anzahl. Vergleiche die Ausgabe mit der Anzeige in Obsidian (dort „X results"),
um zu prüfen, ob eine Base wirklich die richtigen Dateien lädt.

  python3 tools/base_expectations.py

Nur Standardbibliothek (nutzt die Frontmatter-Helfer aus frontmatter_to_validator_json.py).
Grenze: prüft die **Treffermenge** (welche Dateien), nicht das visuelle Rendering
(Spalten/Formeln/Gruppierung) — dafür gibt es keinen Headless-Bases-Renderer.
"""
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import frontmatter_to_validator_json as fv  # noqa: E402


def notes_in(folder):
    base = os.path.join(VAULT, folder)
    rows = []
    if not os.path.isdir(base):
        return rows
    for root, _dirs, files in os.walk(base):
        for f in sorted(files):
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    rows.append((os.path.relpath(path, VAULT), fv.fm_block(fh.read())))
    return rows


def show(title, rows):
    print(f"\n▶ {title}  →  {len(rows)} Treffer")
    for rel, _fm in rows:
        print(f"    {rel}")


def main():
    print("== Base-Erwartungs-Orakel (Soll-Treffermengen; vergleiche mit Obsidian „X results\") ==")

    figuren = [(r, fm) for r, fm in notes_in("04_Figuren") if fv.scalar(fm, "type") == "figur"]
    show("Figuren.base / Figuren  (type==figur)", figuren)
    show("Figuren.base / Verdächtige  (rolle==verdaechtige)",
         [(r, fm) for r, fm in figuren if fv.scalar(fm, "rolle") == "verdaechtige"])

    hinweise = [(r, fm) for r, fm in notes_in("07_Hinweise") if fv.scalar(fm, "type") == "hinweis"]
    show("Hinweise.base / Clue Ledger  (type==hinweis)", hinweise)
    show("Hinweise.base / Player-safe  (spoiler==player-safe)",
         [(r, fm) for r, fm in hinweise if fv.scalar(fm, "spoiler") == "player-safe"])
    show("Hinweise.base / Ohne Wahrheit  (wahrheit leer/fehlt)",
         [(r, fm) for r, fm in hinweise if not (fv.scalar(fm, "wahrheit") or "").strip()])

    umsch = [(r, fm) for r, fm in notes_in("08_Umschlaege") if fv.scalar(fm, "type") == "umschlag"]
    show("Umschlaege.base / Manifest  (type==umschlag)", umsch)
    show("Umschlaege.base / Offen  (produktionsstatus != fertig)",
         [(r, fm) for r, fm in umsch if fv.scalar(fm, "produktionsstatus") != "fertig"])
    pacing = {}
    for _r, fm in umsch:
        tag = fv.to_int(fv.scalar(fm, "tag", "0"), 0)
        pacing[tag] = pacing.get(tag, 0) + fv.to_int(fv.scalar(fm, "zeitkosten", "0"), 0)
    print(f"\n▶ Umschlaege.base / Pacing  →  Sum(zeitkosten) gesamt = {sum(pacing.values())}")
    for tag in sorted(pacing):
        print(f"    Tag {tag}: {pacing[tag]}")

    orte = [(r, fm) for r, fm in notes_in("05_Orte") if fv.scalar(fm, "type") == "ort"]
    show("Orte.base / Knoten-Register  (type==ort)", orte)
    print(f"    Sum(zeitkosten) = {sum(fv.to_int(fv.scalar(fm, 'zeitkosten', '0'), 0) for _r, fm in orte)}")

    show("QA.base / Audits  (type==audit)",
         [(r, fm) for r, fm in notes_in("10_QA") if fv.scalar(fm, "type") == "audit"])
    show("QA.base / Playtests  (type==playtest)",
         [(r, fm) for r, fm in notes_in("10_QA") if fv.scalar(fm, "type") == "playtest"])

    show("Produktion.base  (inFolder 09_Produktion)", notes_in("09_Produktion"))

    show("Inbox-Review.base  (inFolder 11_Inbox & status==draft)",
         [(r, fm) for r, fm in notes_in("11_Inbox") if fv.scalar(fm, "status") == "draft"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
