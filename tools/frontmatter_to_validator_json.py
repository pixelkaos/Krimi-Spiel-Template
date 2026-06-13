#!/usr/bin/env python3
"""Brücke: erzeugt aus Vault-Inhalten das Eingabe-JSON für die Codex-Validatoren.

Subcommands:
  envelopes  – Umschlag-Manifest aus 08_Umschlaege  → tools/generated/envelope-manifest.json
  timeline   – Tat-Zeitleiste aus 06_Zeitleisten     → tools/generated/timeline.json

Nur Standardbibliothek.

  python3 tools/frontmatter_to_validator_json.py envelopes
  python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py tools/generated/envelope-manifest.json
  python3 tools/frontmatter_to_validator_json.py timeline
  python3 tools/advent-crime-game-designer/scripts/validate_timeline.py tools/generated/timeline.json
"""
import argparse
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(VAULT, "tools", "generated")


# --------------------------------------------------------------------------- #
# Frontmatter-Parsing (regex, stdlib-only — bewusst kein PyYAML)
# --------------------------------------------------------------------------- #
def fm_block(text):
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def _clean_scalar(raw):
    """Wert säubern: gequotete Werte exakt zurückgeben (Kommentar ignorieren),
    ungequotete um einen Trailing-Kommentar `␠#…` kürzen (außerhalb von [[…]])."""
    s = raw.strip()
    mq = re.match(r'^"([^"]*)"|^\'([^\']*)\'', s)
    if mq:
        return mq.group(1) if mq.group(1) is not None else mq.group(2)
    hashpos = s.find(" #")  # nur `␠#` gilt als Kommentar; `[[C001#h]]` bleibt heil
    if hashpos != -1:
        s = s[:hashpos]
    return s.strip()


def scalar(fm, key, default=None):
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    if not m:
        return default
    return _clean_scalar(m.group(1))


def _clean_item(v):
    v = v.strip().strip('"').strip("'")
    hp = v.find(" #")
    if hp != -1:
        v = v[:hp].strip().strip('"').strip("'")
    return v


def listvals(fm, key):
    """Liest sowohl Inline-Arrays (`key: [a, b]`) als auch YAML-Blocklisten:
        key:
          - a
          - b
    Blocklisten wurden vorher still als [] gelesen (stille Datenverluste)."""
    m = re.search(rf"^{key}:\s*\[(.*)\]", fm, re.M)
    if m:
        return [_clean_item(x) for x in m.group(1).split(",") if x.strip()]
    mb = re.search(rf"^{key}:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)", fm, re.M)
    if mb:
        items = []
        for ln in mb.group(1).splitlines():
            ln = ln.strip()
            if ln.startswith("-"):
                v = _clean_item(ln[1:])
                if v:
                    items.append(v)
        return items
    return []


def linkbase(s):
    m = re.match(r"\[\[([^\]]+)\]\]", s.strip())
    s = m.group(1) if m else s
    return s.split("|")[0].split("#")[0].strip()


def to_int(v, default):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return default


# --------------------------------------------------------------------------- #
# envelopes
# --------------------------------------------------------------------------- #
def build_envelopes():
    env_dir = os.path.join(VAULT, "08_Umschlaege")
    if not os.path.isdir(env_dir):
        print("kein 08_Umschlaege/ gefunden")
        return 0
    md_files = [f for f in sorted(os.listdir(env_dir)) if f.endswith(".md")]
    env_ids = {os.path.splitext(f)[0].lower() for f in md_files}
    envelopes, critical_clues = [], set()
    crit_meta, finale_meta = [], []  # (unlock_day, id)
    for f in md_files:
        with open(os.path.join(env_dir, f), encoding="utf-8") as fh:
            fm = fm_block(fh.read())
        eid = os.path.splitext(f)[0].lower()
        clues = [linkbase(x) for x in listvals(fm, "clues")]
        tag = to_int(scalar(fm, "tag", "1"), 1)
        crit = scalar(fm, "kritisch", "false") == "true"
        if crit:
            critical_clues.update(clues)
            crit_meta.append((tag, eid))
        if scalar(fm, "finale", "false") == "true":
            finale_meta.append((tag, eid))
        # Nur Verweise auf andere Umschläge zählen für die Erreichbarkeit
        # (fuehrt_zu darf auch Orte nennen; die werden hier ausgefiltert).
        leads = [linkbase(x).lower() for x in listvals(fm, "fuehrt_zu")]
        leads = [t for t in leads if t in env_ids]
        envelopes.append({
            "id": eid,
            "label": scalar(fm, "label", eid),
            "unlock_day": tag,
            "time_cost": to_int(scalar(fm, "zeitkosten", "1"), 1),
            "entry_point": scalar(fm, "entry_point", "false") == "true",
            "clues": clues,
            "leads_to": leads,
            "critical": crit,
        })
    # Finale: explizites `finale: true` gewinnt, sonst der kritische Umschlag
    # mit dem höchsten `tag` (passt zum 24-Tage-Kalender), Tie-Break per id.
    if finale_meta:
        final_env = max(finale_meta)[1]
    elif crit_meta:
        final_env = max(crit_meta)[1]
    else:
        final_env = ""
    manifest = {
        "daily_time_budget": daily_time_budget(),
        "final_envelope": final_env,
        "critical_clues": sorted(critical_clues),
        "envelopes": envelopes,
    }
    return _write(manifest, "envelope-manifest.json", f"{len(envelopes)} Umschläge")


def daily_time_budget():
    """Optionales Tages-Zeitbudget aus 00_Dashboard/Projekt-Dashboard.md
    (`zeitbudget: N` im Frontmatter); Default 3."""
    dash = os.path.join(VAULT, "00_Dashboard", "Projekt-Dashboard.md")
    if os.path.isfile(dash):
        with open(dash, encoding="utf-8") as fh:
            return to_int(scalar(fm_block(fh.read()), "zeitbudget", "3"), 3)
    return 3


# --------------------------------------------------------------------------- #
# timeline
# --------------------------------------------------------------------------- #
TIME_KEYS = ("start", "zeit")
END_KEYS = ("ende", "bis", "end")
ACTOR_KEYS = ("akteure", "actors", "personen")
LOC_KEYS = ("ort", "location")
ID_KEYS = ("id",)
OVERLAP_KEYS = ("overlap?", "overlap", "parallel")
ACTOR_SPLIT = re.compile(r"\s*(?:,|;|/|&|\bund\b)\s*")
TRUE_WORDS = {"ja", "yes", "true", "x", "✓"}


def _strip_links(s):
    return re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("|")[0], s).strip()


def _is_separator(line):
    body = line.strip().strip("|")
    return bool(body) and set(body) <= set("-: |")


def _find_col(header, keys):
    for idx, name in enumerate(header):  # exakte Treffer bevorzugen
        if name in keys:
            return idx
    for idx, name in enumerate(header):  # dann Teilstring
        if any(k in name for k in keys):
            return idx
    return None


def parse_timeline_table(text):
    """Erste Markdown-Tabelle finden und in Events übersetzen.
    Spalten werden per Überschrift erkannt (Reihenfolge egal, Zusatzspalten erlaubt)."""
    lines = text.splitlines()
    header = rows = None
    for i in range(len(lines) - 1):
        ln = lines[i].strip()
        if ln.startswith("|") and _is_separator(lines[i + 1]):
            header = [c.strip().lower() for c in ln.strip("|").split("|")]
            rows = []
            for row_line in lines[i + 2:]:
                if not row_line.strip().startswith("|"):
                    break
                rows.append([c.strip() for c in row_line.strip().strip("|").split("|")])
            break
    if not header:
        return []

    ci = {k: _find_col(header, v) for k, v in (
        ("time", TIME_KEYS), ("end", END_KEYS), ("actors", ACTOR_KEYS),
        ("loc", LOC_KEYS), ("id", ID_KEYS), ("overlap", OVERLAP_KEYS))}

    def cell(row, key):
        idx = ci[key]
        return row[idx].strip() if idx is not None and idx < len(row) else ""

    events, n = [], 0
    for row in rows:
        start = cell(row, "time")
        if not start:
            continue  # Leerzeile / Platzhalter
        n += 1
        actors = [a for a in (x.strip() for x in ACTOR_SPLIT.split(_strip_links(cell(row, "actors")))) if a]
        event = {
            "id": cell(row, "id") or f"E{n:03d}",
            "time": start,
            "actors": actors,
            "location": _strip_links(cell(row, "loc")),
            "truth_status": "objective",
        }
        end = cell(row, "end")
        if end:
            event["end_time"] = end
        if cell(row, "overlap").lower() in TRUE_WORDS:
            event["allows_overlap"] = True
        events.append(event)
    return events


def build_timeline(source=None, out=None):
    src = source or os.path.join(VAULT, "06_Zeitleisten", "Tat-Zeitleiste.md")
    if not os.path.isfile(src):
        print(f"keine Tat-Zeitleiste gefunden: {os.path.relpath(src, VAULT)}")
        return 0
    with open(src, encoding="utf-8") as fh:
        events = parse_timeline_table(fh.read())
    if not events:
        print("Tat-Zeitleiste: keine Ereigniszeilen (Tabelle leer) — nichts zu prüfen.")
        return 0
    return _write({"events": events}, out or "timeline.json", f"{len(events)} Ereignisse")


# --------------------------------------------------------------------------- #
def _write(payload, name, summary):
    out = name if os.path.isabs(name) else os.path.join(OUT_DIR, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"geschrieben: {os.path.relpath(out, VAULT)} ({summary})")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Frontmatter→JSON-Brücke für die Codex-Validatoren.")
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True
    sub.add_parser("envelopes", help="Umschlag-Manifest aus 08_Umschlaege erzeugen")
    pt = sub.add_parser("timeline", help="Tat-Zeitleiste aus 06_Zeitleisten erzeugen")
    pt.add_argument("--source", help="Quelldatei (Default: 06_Zeitleisten/Tat-Zeitleiste.md)")
    pt.add_argument("--out", help="Zieldatei (Default: tools/generated/timeline.json)")
    args = parser.parse_args()
    if args.cmd == "envelopes":
        return build_envelopes()
    if args.cmd == "timeline":
        return build_timeline(args.source, args.out)
    return 2


if __name__ == "__main__":
    sys.exit(main())
