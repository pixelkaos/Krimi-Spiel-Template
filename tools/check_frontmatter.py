#!/usr/bin/env python3
"""Frontmatter-Prüfung (robust, typ-gesteuert). Nur Standardbibliothek.

- HARTER Fehler (Exit 1): eine Inhalts-.md ohne Frontmatter (fängt zerschossene Dateien).
- HARTER Fehler (Exit 1): eine Notiz vom Typ figur/ort/hinweis/umschlag, der Pflichtfelder fehlen.
- WARNUNG (Exit 0): Inhalts-.md ohne `type` (empfohlen, aber nicht erzwungen — toleriert
  KI-generierte Prosa-/Report-/Aggregat-Notizen wie Fallbibel, MOCA-Matrix, Audits).
"""
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTENT_FOLDERS = [
    "00_Dashboard", "01_Regeln", "03_Fallbibel", "04_Figuren", "05_Orte",
    "06_Zeitleisten", "07_Hinweise", "08_Umschlaege", "09_Produktion", "10_QA",
]

# Pflichtfelder je strukturiertem Typ — geprüft NUR, wenn die Notiz diesen type deklariert.
TYPE_REQUIRED = {
    "figur": ["status", "rolle", "spoiler", "tags"],
    "ort": ["status", "rolle", "zeitkosten", "tags"],
    "hinweis": ["status", "beweisart", "deduktionsfunktion", "pflicht", "tags"],
    "umschlag": ["status", "tag", "label", "tags"],
}


def frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else None


def get_type(fm):
    m = re.search(r"^type:\s*(\S+)", fm, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None


def main():
    errors, warnings = [], []
    for folder in CONTENT_FOLDERS:
        base = os.path.join(VAULT, folder)
        if not os.path.isdir(base):
            continue
        for root, _dirs, files in os.walk(base):
            for f in sorted(files):
                if not f.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(root, f), VAULT)
                fm = frontmatter(open(os.path.join(root, f), encoding="utf-8").read())
                if fm is None:
                    errors.append(f"{rel}: kein Frontmatter")
                    continue
                ntype = get_type(fm)
                if ntype is None:
                    warnings.append(f"{rel}: kein 'type' (empfohlen)")
                    continue
                if ntype in TYPE_REQUIRED:
                    for k in TYPE_REQUIRED[ntype]:
                        if not re.search(rf"^{k}:", fm, re.M):
                            errors.append(f"{rel}: Pflichtfeld '{k}' fehlt (type={ntype})")

    if warnings:
        print("⚠ Hinweise (kein Abbruch):")
        for w in sorted(set(warnings)):
            print("   ", w)
    if errors:
        print("Frontmatter-Fehler:")
        for e in sorted(set(errors)):
            print(" -", e)
        return 1
    print("Frontmatter-Check bestanden." + (" (mit Warnungen)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
