#!/usr/bin/env python3
"""Brücke: erzeugt aus dem Frontmatter der Vault-Notizen das Eingabe-JSON
für die Codex-Validatoren. Aktuell: Umschlag-Manifest aus 08_Umschlaege.
Nur Standardbibliothek. Ausgabe nach tools/generated/.

Nutzung:
  python3 tools/frontmatter_to_validator_json.py envelopes
  python3 tools/advent-crime-game-designer/scripts/validate_envelope_manifest.py tools/generated/envelope-manifest.json
"""
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(VAULT, "tools", "generated")


def fm_block(text):
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def scalar(fm, key, default=None):
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    if not m:
        return default
    return m.group(1).strip().strip('"').strip("'")


def listvals(fm, key):
    m = re.search(rf"^{key}:\s*\[(.*)\]", fm, re.M)
    if not m:
        return []
    return [x.strip().strip('"').strip("'") for x in m.group(1).split(",") if x.strip()]


def linkbase(s):
    m = re.match(r"\[\[([^\]]+)\]\]", s.strip())
    s = m.group(1) if m else s
    return s.split("|")[0].split("#")[0].strip()


def to_int(v, default):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return default


def build_envelopes():
    env_dir = os.path.join(VAULT, "08_Umschlaege")
    if not os.path.isdir(env_dir):
        print("kein 08_Umschlaege/ gefunden")
        return 1
    md_files = [f for f in sorted(os.listdir(env_dir)) if f.endswith(".md")]
    env_ids = {os.path.splitext(f)[0].lower() for f in md_files}
    envelopes, critical_clues, final_env = [], set(), ""
    for f in md_files:
        fm = fm_block(open(os.path.join(env_dir, f), encoding="utf-8").read())
        eid = os.path.splitext(f)[0].lower()
        clues = [linkbase(x) for x in listvals(fm, "clues")]
        crit = scalar(fm, "kritisch", "false") == "true"
        if crit:
            critical_clues.update(clues)
            final_env = eid
        # Nur Verweise auf andere Umschläge zählen für den Erreichbarkeits-Check
        # (fuehrt_zu darf auch Orte nennen; die werden hier ausgefiltert).
        leads = [linkbase(x).lower() for x in listvals(fm, "fuehrt_zu")]
        leads = [t for t in leads if t in env_ids]
        envelopes.append({
            "id": eid,
            "label": scalar(fm, "label", eid),
            "unlock_day": to_int(scalar(fm, "tag", "1"), 1),
            "time_cost": to_int(scalar(fm, "zeitkosten", "1"), 1),
            "entry_point": scalar(fm, "entry_point", "false") == "true",
            "clues": clues,
            "leads_to": leads,
            "critical": crit,
        })
    manifest = {
        "daily_time_budget": 3,
        "final_envelope": final_env,
        "critical_clues": sorted(critical_clues),
        "envelopes": envelopes,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "envelope-manifest.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(f"geschrieben: {os.path.relpath(out, VAULT)} ({len(envelopes)} Umschläge)")
    return 0


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "envelopes"
    if kind == "envelopes":
        return build_envelopes()
    print("Nur 'envelopes' implementiert. Truth-Map/Timeline: Grid im Fall definieren "
          "(siehe tools/advent-crime-game-designer/assets/templates/).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
