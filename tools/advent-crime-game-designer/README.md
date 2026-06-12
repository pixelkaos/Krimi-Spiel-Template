# Advent Crime Game Designer

Local Codex plugin for building an analog crime and deduction game in Advent calendar form.

The plugin is German-facing and optimized for a Sherlock-Holmes-Consulting-Detective-style sandbox calendar: coordinate envelopes, a map, an address book, staged newspapers, daily time budgets, clue networks, red herrings, and a final exclusive solution.

## Included Skills

- `crime-case-architect` - reverse-plot the case, suspects, MOCA matrix, crime timeline, alibis, and reveal logic.
- `research-backed-story-planner` - apply selected LLM-era story-generation research to practical crime-game planning.
- `sandbox-calendar-builder` - package the case into 24 coordinate envelopes, directory entries, newspapers, hints, and production lists.
- `deduction-consistency-auditor` - audit clues, truth maps, timelines, red herrings, liar mechanics, and playtest readiness.

## Included Scripts

All scripts use only the Python standard library.

```bash
python3 scripts/validate_truth_map.py assets/templates/truth-map.example.json
python3 scripts/validate_timeline.py assets/templates/timeline.example.json
python3 scripts/validate_envelope_manifest.py assets/templates/envelope-manifest.example.json
```

Portable knowledge-pack export and local Qdrant indexing:

```bash
python3 scripts/export_knowledge_pack.py
python3 scripts/embed_knowledge_pack.py --dry-run
python3 scripts/embed_knowledge_pack.py
python3 scripts/query_knowledge_pack.py "Wie verteile ich Hinweise auf 24 Umschlaege?"
```

Defaults:

- Qdrant: `http://localhost:6333`
- Ollama: `http://localhost:11434`
- Embedding model: `qwen3-embedding:latest`
- Collection: `advent_crime_game_designer__qwen3_embedding`

The Qdrant script creates only the dedicated collection above unless `--collection` is passed. It refuses to reuse a populated unmanaged collection and only deletes/recreates a collection when `--recreate` is explicitly passed.

If Qdrant reports that a collection is missing but collection creation fails with `File exists`, the local Qdrant storage has an orphaned directory. Repair or restart/recreate the Qdrant container before rerunning the embedding script; the plugin will not delete unknown Qdrant storage directories automatically.

Generated portable artifacts are written to `dist/knowledge-pack/`:

- `instructions.md` - provider-neutral behavior instructions.
- `knowledge.md` - consolidated upload/paste knowledge.
- `chunks.jsonl` - RAG-ready chunks with stable IDs and source metadata.
- `manifest.json` - source hashes, chunk count, and embedding metadata.
- `llms.txt` - discovery index for LLM tooling.
- `qdrant-index.json` - local Qdrant index metadata after embedding.

## Primary Sources

- Upstream research map: <https://github.com/yingpengma/Awesome-Story-Generation>
- Game outline source: `/Users/pixelkaos/Documents/Anleitungen/Adventskalender/Adventskalender-Raetselspiel-Entwicklung.md`

The plugin keeps a curated research playbook rather than copying full papers or datasets.
