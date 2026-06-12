#!/usr/bin/env python3
"""Near-Duplikat-Erkennung über Inhalts-Notizen via Jaccard auf Wort-Shingles.
Informativ (Exit 0). Nur Standardbibliothek (keine Embeddings nötig).
"""
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = ("03_Fallbibel", "04_Figuren", "05_Orte", "06_Zeitleisten", "07_Hinweise", "08_Umschlaege", "09_Produktion")
THRESHOLD = 0.6
WORD = re.compile(r"[a-zäöüß0-9]{4,}")


def body(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    return text


def shingles(text, n=3):
    words = WORD.findall(text.lower())
    if len(words) < n:
        return set(words)
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def main():
    docs = {}
    for folder in CONTENT:
        base = os.path.join(VAULT, folder)
        if not os.path.isdir(base):
            continue
        for root, _d, files in os.walk(base):
            for f in files:
                if f.endswith(".md"):
                    rel = os.path.relpath(os.path.join(root, f), VAULT)
                    docs[rel] = shingles(body(open(os.path.join(root, f), encoding="utf-8").read()))
    items = [(k, v) for k, v in docs.items() if v]
    hits = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, sa = items[i]
            b, sb = items[j]
            inter = len(sa & sb)
            if inter == 0:
                continue
            jac = inter / len(sa | sb)
            if jac >= THRESHOLD:
                hits.append((jac, a, b))
    if hits:
        print("⚠ Mögliche Duplikate (Jaccard ≥ %.2f):" % THRESHOLD)
        for jac, a, b in sorted(hits, reverse=True):
            print(f"   {jac:.2f}  {a}  <->  {b}")
    else:
        print("Duplikat-Check: keine Near-Duplikate gefunden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
