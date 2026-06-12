.PHONY: help setup check new-case

help:
	@echo "make setup     — macOS-Bootstrap (scripts/setup.sh)"
	@echo "make check     — Struktur-/Logik-Checks (scripts/check.sh)"
	@echo "make new-case  — Vault für neuen Fall zurücksetzen (scripts/new-case.sh)"

setup:
	@bash scripts/setup.sh

check:
	@bash scripts/check.sh

new-case:
	@bash scripts/new-case.sh
