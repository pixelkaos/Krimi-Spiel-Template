#!/usr/bin/env python3
"""Verwaiste Notizen: Inhalts-Notizen ohne ein- UND ausgehende Wikilinks.
Informativ (Exit 0). Nur Standardbibliothek.
"""
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".obsidian", "tools", ".github", "build", "12_Templates"}
CONTENT = ("03_Fallbibel", "04_Figuren", "05_Orte", "06_Zeitleisten", "07_Hinweise", "08_Umschlaege", "09_Produktion", "10_QA")
LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")


def stem(target):
    return os.path.splitext(os.path.basename(target.split("|")[0].split("#")[0].strip()))[0]


def main():
    notes = {}  # stem -> rel
    text_of = {}
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), VAULT)
            s = os.path.splitext(f)[0]
            notes[s] = rel
            text_of[s] = open(os.path.join(root, f), encoding="utf-8").read()

    inbound = {s: 0 for s in notes}
    outbound = {s: 0 for s in notes}
    for s, text in text_of.items():
        targets = {stem(m.group(1)) for m in LINK_RE.finditer(text)}
        targets.discard(s)
        outbound[s] = len(targets & set(notes))
        for t in targets:
            if t in inbound:
                inbound[t] += 1

    orphans = [notes[s] for s in notes
               if inbound[s] == 0 and outbound[s] == 0
               and any(notes[s].startswith(c) for c in CONTENT)]
    if orphans:
        print("⚠ Verwaiste Notizen (keine ein-/ausgehenden Links):")
        for o in sorted(orphans):
            print("   ", o)
    else:
        print("Orphan-Check: keine verwaisten Inhalts-Notizen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
