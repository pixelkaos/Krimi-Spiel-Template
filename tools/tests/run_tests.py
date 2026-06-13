#!/usr/bin/env python3
"""Tests für die Adapter-Logik in tools/frontmatter_to_validator_json.py.

  python3 tools/tests/run_tests.py

Unit: listvals (Inline + Blockliste, F3) und scalar (Trailing-Kommentar, F11).
Integration: Zeitleisten-Adapter → validate_timeline gegen zwei Fixtures
(widerspruchsfrei → passed; gleicher Akteur überlappend an zwei Orten → failed).
Exit 0, wenn alle Erwartungen erfüllt sind, sonst 1.
"""
import os
import subprocess
import sys
import tempfile

TESTS = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(TESTS)
PLUG = os.path.join(TOOLS, "advent-crime-game-designer")
PY = sys.executable or "python3"

sys.path.insert(0, TOOLS)
import frontmatter_to_validator_json as fv  # noqa: E402

results = []


def check(name, ok):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


# --- Unit: listvals (F3) ---
inline = 'clues: ["[[C001]]", "[[C002]]"]\n'
block = 'clues:\n  - "[[C001]]"\n  - "[[C002]]"\n'
check("listvals inline → 2 Einträge", len(fv.listvals(inline, "clues")) == 2)
check("listvals Blockliste → 2 Einträge (F3, vorher 0)", len(fv.listvals(block, "clues")) == 2)

# --- Unit: scalar (F11) ---
check("scalar Trailing-Kommentar bei leerem Quote → ''",
      fv.scalar('unlock: ""   # "[[C001]]" Beispiel\n', "unlock") == "")
check("scalar Trailing-Kommentar unquoted → Wert ohne Kommentar",
      fv.scalar("label: Start  # nur ein Hinweis\n", "label") == "Start")
check("scalar gequotet bleibt intakt",
      fv.scalar('label: "12 NW"\n', "label") == "12 NW")


# --- Integration: timeline adapter → validator ---
def adapter_then_validate(fixture):
    fd, out = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        rc = subprocess.run(
            [PY, os.path.join(TOOLS, "frontmatter_to_validator_json.py"),
             "timeline", "--source", os.path.join(TESTS, fixture), "--out", out],
            capture_output=True,
        ).returncode
        if rc != 0 or not os.path.getsize(out):
            return None
        return subprocess.run(
            [PY, os.path.join(PLUG, "scripts", "validate_timeline.py"), out],
            capture_output=True,
        ).returncode
    finally:
        if os.path.exists(out):
            os.remove(out)


check("timeline_ok.md → validate_timeline passed", adapter_then_validate("timeline_ok.md") == 0)
check("timeline_conflict.md → validate_timeline failed", adapter_then_validate("timeline_conflict.md") == 1)


# --- Integration: validate_exclusion (Beispiel + Fixtures) ---
def validate_json(script, path):
    return subprocess.run(
        [PY, os.path.join(PLUG, "scripts", script), path], capture_output=True
    ).returncode


_EX = os.path.join(PLUG, "assets", "templates", "exclusion.example.json")
_FX = os.path.join(PLUG, "scripts", "fixtures")
check("exclusion.example → passed",
      validate_json("validate_exclusion.py", _EX) == 0)
check("exclusion underdetermined → failed",
      validate_json("validate_exclusion.py", os.path.join(_FX, "failing_exclusion_underdetermined.json")) == 1)
check("exclusion culprit-excluded → failed",
      validate_json("validate_exclusion.py", os.path.join(_FX, "failing_exclusion_culprit_excluded.json")) == 1)

failed = [n for n, ok in results if not ok]
print("\n" + "=" * 40)
print(f"{len(results) - len(failed)}/{len(results)} bestanden")
sys.exit(1 if failed else 0)
