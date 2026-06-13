#!/usr/bin/env python3
"""Lokaler Sammel-Runner — CI-Parität in einem Befehl. Nur Standardbibliothek.

  python3 tools/check_all.py

Gating (Exit≠0 bei Fehler): check_frontmatter / check_links / check_tags +
Codex-Beispiel-Validatoren (truth-map/timeline). Informativ (nie blockierend):
orphans, duplicates, Umschlag- und Tat-Zeitleisten-Adapter + zugehörige Validatoren.
"""
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(TOOLS)
PLUG = os.path.join(TOOLS, "advent-crime-game-designer")
PY = sys.executable or "python3"

try:  # Labels und Subprozess-Ausgabe sauber verzahnen
    sys.stdout.reconfigure(line_buffering=True)
except (AttributeError, ValueError):
    pass

ADAPTER = os.path.join(TOOLS, "frontmatter_to_validator_json.py")
GENERATED = os.path.join(TOOLS, "generated")


def run(*args):
    return subprocess.run([PY, *args], cwd=VAULT).returncode


def gate(label, *args):
    print(f"\n▶ {label}")
    rc = run(*args)
    print(("  ✓ " if rc == 0 else "  ✗ ") + label)
    return rc == 0


def info(label, *args):
    print(f"\n▶ {label} (informativ)")
    run(*args)


def adapter_then_validate(label, subcmd, generated_name, validator):
    """Adapter laufen lassen; nur wenn er ein JSON erzeugt hat, den Validator anstoßen."""
    print(f"\n▶ {label} (informativ)")
    if run(ADAPTER, subcmd) == 0:
        path = os.path.join(GENERATED, generated_name)
        if os.path.isfile(path):
            run(os.path.join(PLUG, "scripts", validator), path)


def main():
    ok = True
    print("== Gating-Checks ==")
    ok &= gate("Frontmatter-Schema", os.path.join(TOOLS, "check_frontmatter.py"))
    ok &= gate("Wikilinks", os.path.join(TOOLS, "check_links.py"))
    ok &= gate("Tag-Konsistenz", os.path.join(TOOLS, "check_tags.py"))
    ok &= gate("Truth-Map (Beispiel)",
               os.path.join(PLUG, "scripts", "validate_truth_map.py"),
               os.path.join(PLUG, "assets", "templates", "truth-map.example.json"))
    ok &= gate("Timeline (Beispiel)",
               os.path.join(PLUG, "scripts", "validate_timeline.py"),
               os.path.join(PLUG, "assets", "templates", "timeline.example.json"))
    ok &= gate("Ausschluss (Beispiel)",
               os.path.join(PLUG, "scripts", "validate_exclusion.py"),
               os.path.join(PLUG, "assets", "templates", "exclusion.example.json"))

    print("\n== Informative Checks ==")
    info("Verwaiste Notizen", os.path.join(TOOLS, "check_orphans.py"))
    info("Near-Duplikate", os.path.join(TOOLS, "check_duplicates.py"))
    adapter_then_validate("Umschlag-Manifest", "envelopes",
                          "envelope-manifest.json", "validate_envelope_manifest.py")
    adapter_then_validate("Tat-Zeitleiste", "timeline",
                          "timeline.json", "validate_timeline.py")

    print("\n" + "=" * 40)
    if not ok:
        print("✗ Mindestens ein Gating-Check ist rot.")
        return 1
    print("✓ Alle Gating-Checks bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
