#!/usr/bin/env python3
"""Prüft, dass alle [[Wikilinks]] im Vault auf eine existierende Notiz/Datei zeigen.
Nur Standardbibliothek. Exit 1 bei defekten Links."""
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ordner, deren Dateien NICHT als gültige Link-Ziele zählen (System/Build):
NAME_SKIP = {".git", ".obsidian", ".github", "build"}
# Ordner, deren Dateien NICHT auf defekte Links gescannt werden (Scratch/Templates/Tooling
# dürfen Platzhalter-/Beispiel-Links enthalten) — sie bleiben aber gültige Link-ZIELE:
SCAN_SKIP = {".git", ".obsidian", ".github", "build", "tools", "12_Templates", "work"}
LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")


def collect_names():
    names = set()
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in NAME_SKIP and not d.startswith(".")]
        for f in files:
            if f.startswith("."):
                continue
            names.add(os.path.splitext(f)[0])
            names.add(f)
    return names


def main():
    names = collect_names()
    problems = []
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SCAN_SKIP and not d.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for m in LINK_RE.finditer(text):
                target = m.group(1).split("|")[0].split("#")[0].split("^")[0].strip()
                if not target:
                    continue
                base = os.path.splitext(os.path.basename(target))[0]
                if base not in names and os.path.basename(target) not in names:
                    problems.append(f"{os.path.relpath(path, VAULT)}: unaufgelöst [[{target}]]")
    if problems:
        print("Defekte Wikilinks:")
        for p in sorted(set(problems)):
            print(" -", p)
        return 1
    print("Link-Check bestanden: alle Wikilinks lösen auf.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
