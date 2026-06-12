#!/usr/bin/env python3
"""Tag-Konsistenz. Nur Standardbibliothek.
- Fehler (Exit 1): zwei Tags, die normalisiert (Klein-/Leerzeichen) kollidieren -> Tippfehler/Variante.
- Warnung (Exit 0): Tag ohne bekanntes Taxonomie-Präfix.
"""
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".obsidian", "tools", ".github", "build", "12_Templates"}
ALLOWED_PREFIXES = ("status/", "artifact/", "spoiler/", "mechanic/", "source/")

FM_TAGS_INLINE = re.compile(r"^tags:\s*\[(.*)\]", re.M)
FM_TAGS_BLOCK = re.compile(r"^tags:\s*\n((?:\s*-\s*.+\n)+)", re.M)
BODY_TAG = re.compile(r"(?<!\S)#([A-Za-z0-9_/\-]+)")


def collect():
    tags = {}  # tag -> set(files)
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, VAULT)
            text = open(path, encoding="utf-8").read()
            fm = text[3:text.find("\n---", 3)] if text.startswith("---") and text.find("\n---", 3) != -1 else ""
            found = set()
            m = FM_TAGS_INLINE.search(fm)
            if m:
                found |= {t.strip().strip('"').strip("'") for t in m.group(1).split(",") if t.strip()}
            m = FM_TAGS_BLOCK.search(fm)
            if m:
                found |= {ln.strip()[1:].strip().strip('"').strip("'") for ln in m.group(1).splitlines() if ln.strip().startswith("-")}
            body = text[len(fm) + 6:] if fm else text
            found |= set(BODY_TAG.findall(body))
            for t in found:
                if t:
                    tags.setdefault(t, set()).add(rel)
    return tags


def main():
    tags = collect()
    # Kollisionen (normalisiert gleich, aber unterschiedlich geschrieben)
    norm = {}
    collisions = []
    for t in tags:
        key = t.lower().strip().replace(" ", "")
        norm.setdefault(key, set()).add(t)
    for key, variants in norm.items():
        if len(variants) > 1:
            collisions.append(sorted(variants))
    # Unbekannte Präfixe (Warnung)
    unknown = sorted(t for t in tags if "/" in t and not t.startswith(ALLOWED_PREFIXES))

    if unknown:
        print("⚠ Tags ohne bekanntes Taxonomie-Präfix (status/artifact/spoiler/mechanic/source):")
        for t in unknown:
            print(f"   {t}  ({', '.join(sorted(tags[t]))})")
    if collisions:
        print("Tag-Kollisionen (vereinheitlichen!):")
        for v in collisions:
            print(" -", " == ".join(v))
        return 1
    print("Tag-Check bestanden." + (" (mit Warnungen)" if unknown else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
