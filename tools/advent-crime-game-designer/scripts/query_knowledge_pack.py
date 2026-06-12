#!/usr/bin/env python3
"""Query the Qdrant-backed knowledge pack and print reusable context chunks."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_PACK_DIR = "dist/knowledge-pack"
DEFAULT_QDRANT_URL = "http://localhost:6333"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_EMBEDDING_MODEL = "qwen3-embedding:latest"


class HttpError(RuntimeError):
    pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the local Qdrant knowledge-pack index.")
    parser.add_argument("query", help="Natural-language search query.")
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to the parent of scripts/.",
    )
    parser.add_argument("--pack-dir", type=Path, default=None, help="Knowledge-pack directory.")
    parser.add_argument("--qdrant-url", default=os.getenv("QDRANT_URL", DEFAULT_QDRANT_URL))
    parser.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", DEFAULT_OLLAMA_URL))
    parser.add_argument("--embedding-model", default=None, help="Override the indexed embedding model.")
    parser.add_argument("--collection", default=None, help="Override the indexed Qdrant collection.")
    parser.add_argument("--limit", type=positive_int, default=5)
    parser.add_argument("--score-threshold", type=float, default=None)
    parser.add_argument("--timeout", type=positive_int, default=300)
    parser.add_argument("--query-prefix", default="", help="Optional prefix added before the query text.")
    parser.add_argument("--json", action="store_true", help="Print raw JSON results.")
    args = parser.parse_args()

    plugin_root = args.plugin_root.resolve()
    pack_dir = (args.pack_dir or plugin_root / DEFAULT_PACK_DIR).resolve()
    index_metadata = load_index_metadata(pack_dir)
    embedding_model = args.embedding_model or index_metadata.get("embedding_model") or DEFAULT_EMBEDDING_MODEL
    collection = args.collection or index_metadata.get("collection")
    if not collection:
        raise SystemExit("No collection was provided and qdrant-index.json is missing.")

    vector = embed_query(args.ollama_url, embedding_model, args.query_prefix + args.query, args.timeout)
    response = query_qdrant(
        qdrant_url=args.qdrant_url,
        collection=collection,
        vector=vector,
        limit=args.limit,
        score_threshold=args.score_threshold,
        timeout=args.timeout,
    )

    points = response.get("result", {}).get("points", [])
    if args.json:
        print(json.dumps(points, ensure_ascii=False, indent=2))
        return 0

    print(f"Query: {args.query}")
    print(f"Collection: {collection}")
    print(f"Embedding model: {embedding_model}")
    print("")
    for index, point in enumerate(points, start=1):
        payload = point.get("payload", {})
        print(f"## {index}. score={point.get('score')}")
        print(f"Source: {payload.get('source_path')} | Heading: {payload.get('heading')}")
        print("")
        print(payload.get("text", "").strip())
        print("")
    return 0


def load_index_metadata(pack_dir: Path) -> dict[str, Any]:
    path = pack_dir / "qdrant-index.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid qdrant-index.json: {exc}") from None
    return data if isinstance(data, dict) else {}


def embed_query(ollama_url: str, model: str, query: str, timeout: int) -> list[float]:
    payload = {"model": model, "input": query}
    response = request_json("POST", f"{trim_url(ollama_url)}/api/embed", payload, timeout)
    embeddings = response.get("embeddings")
    if not isinstance(embeddings, list) or not embeddings or not isinstance(embeddings[0], list):
        raise SystemExit("Ollama returned an invalid embeddings response.")
    return [float(value) for value in embeddings[0]]


def query_qdrant(
    *,
    qdrant_url: str,
    collection: str,
    vector: list[float],
    limit: int,
    score_threshold: float | None,
    timeout: int,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "query": vector,
        "limit": limit,
        "with_payload": True,
        "with_vector": False,
    }
    if score_threshold is not None:
        payload["score_threshold"] = score_threshold
    return request_json(
        "POST",
        f"{trim_url(qdrant_url)}/collections/{quote(collection)}/points/query",
        payload,
        timeout,
    )


def request_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise HttpError(f"HTTP {exc.code} {method} {url}: {body}") from None
    except urllib.error.URLError as exc:
        raise HttpError(f"{method} {url} failed: {exc.reason}") from None
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise HttpError(f"{method} {url} returned invalid JSON: {exc}") from None


def quote(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def trim_url(value: str) -> str:
    return value.rstrip("/")


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
