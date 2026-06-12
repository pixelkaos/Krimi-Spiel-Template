#!/usr/bin/env python3
"""Export the plugin knowledge into portable Markdown and JSONL chunks."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPORT_SCHEMA_VERSION = "1.0.0"
DEFAULT_OUTPUT = "dist/knowledge-pack"
MAX_CHUNK_CHARS = 4_000


@dataclass(frozen=True)
class SourceDoc:
    path: Path
    rel_path: str
    kind: str
    text: str
    sha256: str
    tags: list[str]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_path: str
    source_hash: str
    content_hash: str
    heading: str
    kind: str
    tags: list[str]
    text: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "source_path": self.source_path,
            "source_hash": self.source_hash,
            "content_hash": self.content_hash,
            "heading": self.heading,
            "kind": self.kind,
            "tags": self.tags,
            "text": self.text,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export portable knowledge-pack artifacts.")
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to the parent of scripts/.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"Output directory. Defaults to <plugin-root>/{DEFAULT_OUTPUT}.",
    )
    args = parser.parse_args()

    plugin_root = args.plugin_root.resolve()
    output_dir = (args.output or plugin_root / DEFAULT_OUTPUT).resolve()

    manifest = load_manifest(plugin_root)
    sources = collect_sources(plugin_root)
    chunks = build_chunks(sources)
    generated_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    output_dir.mkdir(parents=True, exist_ok=True)
    write_text(output_dir / "instructions.md", render_instructions(manifest))
    write_text(output_dir / "knowledge.md", render_knowledge(manifest, sources, chunks))
    write_jsonl(output_dir / "chunks.jsonl", chunks)
    write_text(output_dir / "llms.txt", render_llms_txt(manifest, sources))
    write_json(output_dir / "manifest.json", build_manifest(plugin_root, manifest, sources, chunks, generated_at))

    print(f"Exported {len(chunks)} chunks to {output_dir}")
    return 0


def load_manifest(plugin_root: Path) -> dict[str, Any]:
    path = plugin_root / ".codex-plugin" / "plugin.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing plugin manifest: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid plugin manifest JSON: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit("Plugin manifest must be a JSON object.")
    return data


def collect_sources(plugin_root: Path) -> list[SourceDoc]:
    paths: list[Path] = []
    add_existing(paths, plugin_root / "README.md")
    paths.extend(sorted((plugin_root / "skills").glob("*/SKILL.md")))
    paths.extend(sorted((plugin_root / "references").glob("*.md")))
    paths.extend(sorted((plugin_root / "assets" / "templates").glob("*.md")))
    paths.extend(sorted((plugin_root / "assets" / "templates").glob("*.json")))

    sources: list[SourceDoc] = []
    seen: set[str] = set()
    for path in paths:
        rel_path = path.relative_to(plugin_root).as_posix()
        if rel_path in seen:
            continue
        seen.add(rel_path)
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        kind = infer_kind(rel_path)
        sources.append(
            SourceDoc(
                path=path,
                rel_path=rel_path,
                kind=kind,
                text=text,
                sha256=sha256_text(text),
                tags=infer_tags(rel_path, kind),
            )
        )
    return sources


def add_existing(paths: list[Path], path: Path) -> None:
    if path.exists():
        paths.append(path)


def infer_kind(rel_path: str) -> str:
    if rel_path == "README.md":
        return "readme"
    if rel_path.startswith("skills/"):
        return "skill"
    if rel_path.startswith("references/"):
        return "reference"
    if rel_path.startswith("assets/templates/"):
        return "template"
    return "source"


def infer_tags(rel_path: str, kind: str) -> list[str]:
    stem = Path(rel_path).name
    pieces = [kind]
    pieces.extend(part for part in re.split(r"[^a-zA-Z0-9]+", stem.lower()) if part)
    if rel_path.startswith("skills/"):
        pieces.append(Path(rel_path).parts[1])
    return sorted(set(pieces))


def build_chunks(sources: list[SourceDoc]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for source in sources:
        sections = split_source(source)
        for index, (heading, text) in enumerate(sections, start=1):
            for part_index, part_text in enumerate(split_large_section(text), start=1):
                part_heading = heading if len(text) <= MAX_CHUNK_CHARS else f"{heading} ({part_index})"
                chunk_id = make_chunk_id(source.rel_path, index, part_index, part_heading)
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        source_path=source.rel_path,
                        source_hash=source.sha256,
                        content_hash=sha256_text(part_text),
                        heading=part_heading,
                        kind=source.kind,
                        tags=source.tags,
                        text=part_text,
                    )
                )
    return chunks


def split_source(source: SourceDoc) -> list[tuple[str, str]]:
    if not source.rel_path.endswith(".md"):
        return [(Path(source.rel_path).name, source.text)]

    matches = list(re.finditer(r"^#{1,6}\s+(.+?)\s*$", source.text, flags=re.MULTILINE))
    if not matches:
        return [(Path(source.rel_path).name, source.text)]

    sections: list[tuple[str, str]] = []
    first = matches[0]
    preamble = source.text[: first.start()].strip()
    if preamble:
        sections.append((Path(source.rel_path).name, preamble))

    for pos, match in enumerate(matches):
        start = match.start()
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(source.text)
        heading = clean_heading(match.group(1)) or Path(source.rel_path).name
        body = source.text[start:end].strip()
        if body:
            sections.append((heading, body))
    return sections


def split_large_section(text: str) -> list[str]:
    if len(text) <= MAX_CHUNK_CHARS:
        return [text]

    parts: list[str] = []
    current: list[str] = []
    current_len = 0
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        proposed_len = current_len + len(block) + 2
        if current and proposed_len > MAX_CHUNK_CHARS:
            parts.append("\n\n".join(current))
            current = [block]
            current_len = len(block)
        else:
            current.append(block)
            current_len = proposed_len
    if current:
        parts.append("\n\n".join(current))
    return parts or [text]


def make_chunk_id(rel_path: str, section_index: int, part_index: int, heading: str) -> str:
    path_slug = slugify(rel_path.removesuffix(".md").removesuffix(".json"))
    heading_slug = slugify(heading)[:64] or "chunk"
    return f"{path_slug}--{section_index:03d}-{part_index:02d}--{heading_slug}"


def clean_heading(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip("#")).strip()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def build_manifest(
    plugin_root: Path,
    plugin_manifest: dict[str, Any],
    sources: list[SourceDoc],
    chunks: list[Chunk],
    generated_at: str,
) -> dict[str, Any]:
    counts = Counter(chunk.source_path for chunk in chunks)
    return {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "generated_at": generated_at,
        "plugin": {
            "name": plugin_manifest.get("name"),
            "version": plugin_manifest.get("version"),
            "description": plugin_manifest.get("description"),
            "keywords": plugin_manifest.get("keywords", []),
        },
        "source_root": plugin_root.as_posix(),
        "source_files": [
            {
                "path": source.rel_path,
                "kind": source.kind,
                "sha256": source.sha256,
                "bytes": len(source.text.encode("utf-8")),
                "chunks": counts[source.rel_path],
            }
            for source in sources
        ],
        "chunk_count": len(chunks),
        "outputs": [
            "instructions.md",
            "knowledge.md",
            "chunks.jsonl",
            "llms.txt",
            "manifest.json",
        ],
        "embedding": {
            "status": "not_embedded",
            "provider": None,
            "model": None,
            "dimension": None,
            "qdrant_url": None,
            "qdrant_collection": None,
            "indexed_at": None,
        },
    }


def render_instructions(plugin_manifest: dict[str, Any]) -> str:
    name = plugin_manifest.get("interface", {}).get("displayName") or plugin_manifest.get("name")
    prompts = plugin_manifest.get("interface", {}).get("defaultPrompt", [])
    prompt_lines = "\n".join(f"- {prompt}" for prompt in prompts)
    return f"""# {name} Instructions

Use this knowledge pack to support the design of analog crime and deduction Advent calendar games.

## Operating Mode

- Work in German by default unless the user asks otherwise.
- Treat the player-facing mystery as a closed logical system with one defensible final solution.
- Separate author-only truth from player-facing evidence.
- Prefer practical artifacts: case bible, MOCA matrix, timeline, clue ledger, envelope manifest, address book, map entries, newspapers, and playtest report.
- Flag contradictions, underdetermined deductions, unreachable clues, overloaded days, and red herrings that create alternate solutions.
- When using retrieved chunks, cite their source path and heading in the answer.

## Typical Entry Prompts

{prompt_lines}
"""


def render_knowledge(
    plugin_manifest: dict[str, Any],
    sources: list[SourceDoc],
    chunks: list[Chunk],
) -> str:
    display_name = plugin_manifest.get("interface", {}).get("displayName") or plugin_manifest.get("name")
    lines = [
        f"# {display_name} Knowledge Pack",
        "",
        "This document consolidates the portable knowledge from the Codex plugin.",
        "",
        "## Source Index",
        "",
    ]
    for source in sources:
        lines.append(f"- `{source.rel_path}` ({source.kind}, sha256 `{source.sha256}`)")

    lines.extend(["", "## Chunks", ""])
    for chunk in chunks:
        lines.extend(
            [
                f"### {chunk.heading}",
                "",
                f"Source: `{chunk.source_path}` | Kind: `{chunk.kind}` | Tags: {', '.join(chunk.tags)}",
                "",
                chunk.text,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_llms_txt(plugin_manifest: dict[str, Any], sources: list[SourceDoc]) -> str:
    display_name = plugin_manifest.get("interface", {}).get("displayName") or plugin_manifest.get("name")
    lines = [
        f"# {display_name}",
        "",
        "> Portable knowledge pack for analog crime and deduction Advent calendar design.",
        "",
        "## Core Files",
        "",
        "- [Instructions](instructions.md): Model-neutral behavior instructions.",
        "- [Knowledge](knowledge.md): Consolidated source knowledge for upload or paste.",
        "- [Chunks](chunks.jsonl): JSONL chunks for RAG ingestion.",
        "- [Manifest](manifest.json): Export metadata and source hashes.",
        "",
        "## Source Files",
        "",
    ]
    for source in sources:
        lines.append(f"- `{source.rel_path}`")
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, chunks: list[Chunk]) -> None:
    lines = [json.dumps(chunk.as_dict(), ensure_ascii=False, sort_keys=True) for chunk in chunks]
    write_text(path, "\n".join(lines) + "\n")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
