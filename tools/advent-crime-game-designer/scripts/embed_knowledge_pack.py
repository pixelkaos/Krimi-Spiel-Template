#!/usr/bin/env python3
"""Embed exported knowledge-pack chunks into a local Qdrant collection."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


DEFAULT_PACK_DIR = "dist/knowledge-pack"
DEFAULT_QDRANT_URL = "http://localhost:6333"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_EMBEDDING_MODEL = "qwen3-embedding:latest"
DISTANCE = "Cosine"
INDEX_FIELDS = ("plugin", "plugin_version", "kind", "source_path", "tags", "embedding_model")


class HttpError(RuntimeError):
    pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Embed knowledge-pack chunks into Qdrant.")
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to the parent of scripts/.",
    )
    parser.add_argument("--pack-dir", type=Path, default=None, help="Knowledge-pack directory.")
    parser.add_argument("--qdrant-url", default=os.getenv("QDRANT_URL", DEFAULT_QDRANT_URL))
    parser.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", DEFAULT_OLLAMA_URL))
    parser.add_argument(
        "--embedding-model",
        default=os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        help="Ollama embedding model.",
    )
    parser.add_argument("--collection", default=None, help="Qdrant collection name.")
    parser.add_argument("--batch-size", type=positive_int, default=16)
    parser.add_argument("--timeout", type=positive_int, default=300)
    parser.add_argument("--document-prefix", default="", help="Optional prefix added before chunk text.")
    parser.add_argument("--dry-run", action="store_true", help="Probe and report without changing Qdrant.")
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and recreate the target collection on config mismatch.",
    )
    args = parser.parse_args()

    plugin_root = args.plugin_root.resolve()
    pack_dir = (args.pack_dir or plugin_root / DEFAULT_PACK_DIR).resolve()
    chunks = load_chunks(pack_dir / "chunks.jsonl")
    manifest = load_manifest(pack_dir / "manifest.json")
    plugin = manifest["plugin"]["name"]
    plugin_version = manifest["plugin"]["version"]
    collection = args.collection or default_collection_name(plugin, args.embedding_model)

    if not chunks:
        raise SystemExit(f"No chunks found in {pack_dir / 'chunks.jsonl'}")

    dimension = len(embed_texts(args.ollama_url, args.embedding_model, ["dimension probe"], args.timeout)[0])
    print(f"Embedding model: {args.embedding_model}")
    print(f"Embedding dimension: {dimension}")
    print(f"Qdrant collection: {collection}")
    print(f"Chunks: {len(chunks)}")

    if args.dry_run:
        print("Dry run only; Qdrant was not changed.")
        return 0

    qdrant_url = trim_url(args.qdrant_url)
    ensure_collection(
        qdrant_url=qdrant_url,
        collection=collection,
        dimension=dimension,
        embedding_model=args.embedding_model,
        pack_dir=pack_dir,
        recreate=args.recreate,
        timeout=args.timeout,
    )
    ensure_payload_indexes(qdrant_url, collection, args.timeout)
    clear_previous_points(qdrant_url, collection, plugin, args.embedding_model, args.timeout)
    indexed_at = utc_now()

    total = 0
    for batch in batches(chunks, args.batch_size):
        texts = [args.document_prefix + chunk["text"] for chunk in batch]
        vectors = embed_texts(args.ollama_url, args.embedding_model, texts, args.timeout)
        points = [
            build_point(
                chunk=chunk,
                vector=vector,
                plugin=plugin,
                plugin_version=plugin_version,
                embedding_model=args.embedding_model,
                indexed_at=indexed_at,
                expected_dimension=dimension,
            )
            for chunk, vector in zip(batch, vectors, strict=True)
        ]
        upsert_points(qdrant_url, collection, points, args.timeout)
        total += len(points)
        print(f"Upserted {total}/{len(chunks)} chunks")

    update_index_metadata(
        pack_dir=pack_dir,
        manifest=manifest,
        qdrant_url=qdrant_url,
        collection=collection,
        embedding_model=args.embedding_model,
        dimension=dimension,
        indexed_at=indexed_at,
        chunk_count=len(chunks),
        document_prefix=args.document_prefix,
    )
    verify_point_count(qdrant_url, collection, len(chunks), args.timeout)
    print(f"Indexed {len(chunks)} chunks into {collection}.")
    return 0


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing manifest: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid manifest JSON: {exc}") from None
    if not isinstance(data, dict) or not isinstance(data.get("plugin"), dict):
        raise SystemExit("Manifest must contain a plugin object.")
    return data


def load_chunks(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise SystemExit(f"Missing chunks file: {path}") from None

    chunks: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSONL at line {index}: {exc}") from None
        required = {"chunk_id", "source_path", "source_hash", "content_hash", "heading", "kind", "tags", "text"}
        missing = sorted(required.difference(chunk))
        if missing:
            raise SystemExit(f"Chunk line {index} is missing fields: {', '.join(missing)}")
        chunks.append(chunk)
    return chunks


def ensure_collection(
    *,
    qdrant_url: str,
    collection: str,
    dimension: int,
    embedding_model: str,
    pack_dir: Path,
    recreate: bool,
    timeout: int,
) -> None:
    info = get_collection(qdrant_url, collection, timeout)
    if info is None:
        create_collection(qdrant_url, collection, dimension, timeout)
        return

    try:
        current_size, current_distance = parse_vector_config(info)
    except KeyError as exc:
        raise SystemExit(f"Cannot read vector config for existing collection `{collection}`: {exc}") from None

    metadata = load_index_metadata(pack_dir)
    metadata_model = metadata.get("embedding_model") if metadata.get("collection") == collection else None
    points_count = int(info.get("result", {}).get("points_count", 0))
    mismatch = current_size != dimension or current_distance != DISTANCE or (
        metadata_model is not None and metadata_model != embedding_model
    )
    unmanaged = metadata_model is None and points_count > 0

    if mismatch or unmanaged:
        if not recreate:
            details = (
                f"size={current_size}, distance={current_distance}, "
                f"metadata_model={metadata_model or 'missing'}, points={points_count}"
            )
            raise SystemExit(
                f"Existing collection `{collection}` is not a safe match ({details}). "
                "Pass --recreate to delete and rebuild it."
            )
        delete_collection(qdrant_url, collection, timeout)
        wait_for_collection_delete(qdrant_url, collection, timeout)
        create_collection(qdrant_url, collection, dimension, timeout)


def get_collection(qdrant_url: str, collection: str, timeout: int) -> dict[str, Any] | None:
    try:
        return request_json("GET", f"{qdrant_url}/collections/{quote(collection)}", timeout=timeout)
    except HttpError as exc:
        if "HTTP 404" in str(exc):
            return None
        raise


def create_collection(qdrant_url: str, collection: str, dimension: int, timeout: int) -> None:
    payload = {
        "vectors": {
            "size": dimension,
            "distance": DISTANCE,
        },
        "on_disk_payload": True,
    }
    try:
        request_json("PUT", f"{qdrant_url}/collections/{quote(collection)}", payload, timeout)
    except HttpError as exc:
        message = str(exc)
        if "File exists" in message:
            raise SystemExit(
                f"Qdrant refused to create `{collection}` because its storage directory already exists "
                "but the collection is not registered. Repair the Qdrant storage state or restart/recreate "
                "the local Qdrant container, then rerun this script."
            ) from None
        raise
    print(f"Created collection `{collection}`.")


def delete_collection(qdrant_url: str, collection: str, timeout: int) -> None:
    request_json("DELETE", f"{qdrant_url}/collections/{quote(collection)}", timeout=timeout)
    print(f"Deleted collection `{collection}`.")


def wait_for_collection_delete(qdrant_url: str, collection: str, timeout: int) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if get_collection(qdrant_url, collection, timeout) is None:
            return
        time.sleep(0.25)
    raise SystemExit(f"Timed out waiting for `{collection}` to be deleted.")


def parse_vector_config(info: dict[str, Any]) -> tuple[int, str]:
    vectors = info["result"]["config"]["params"]["vectors"]
    if "size" in vectors:
        return int(vectors["size"]), str(vectors["distance"])
    if "" in vectors:
        config = vectors[""]
        return int(config["size"]), str(config["distance"])
    raise KeyError("only unnamed/default vector collections are supported")


def ensure_payload_indexes(qdrant_url: str, collection: str, timeout: int) -> None:
    for field in INDEX_FIELDS:
        payload = {"field_name": field, "field_schema": "keyword"}
        request_json("PUT", f"{qdrant_url}/collections/{quote(collection)}/index?wait=true", payload, timeout)


def clear_previous_points(
    qdrant_url: str,
    collection: str,
    plugin: str,
    embedding_model: str,
    timeout: int,
) -> None:
    payload = {
        "filter": {
            "must": [
                {"key": "plugin", "match": {"value": plugin}},
                {"key": "embedding_model", "match": {"value": embedding_model}},
            ]
        }
    }
    request_json("POST", f"{qdrant_url}/collections/{quote(collection)}/points/delete?wait=true", payload, timeout)


def build_point(
    *,
    chunk: dict[str, Any],
    vector: list[float],
    plugin: str,
    plugin_version: str,
    embedding_model: str,
    indexed_at: str,
    expected_dimension: int,
) -> dict[str, Any]:
    if len(vector) != expected_dimension:
        raise SystemExit(
            f"Vector dimension mismatch for {chunk['chunk_id']}: "
            f"expected {expected_dimension}, got {len(vector)}"
        )
    point_id = stable_uuid(plugin, embedding_model, chunk["chunk_id"], chunk["content_hash"])
    payload = {
        "text": chunk["text"],
        "plugin": plugin,
        "plugin_version": plugin_version,
        "chunk_id": chunk["chunk_id"],
        "source_path": chunk["source_path"],
        "heading": chunk["heading"],
        "kind": chunk["kind"],
        "tags": chunk["tags"],
        "content_hash": chunk["content_hash"],
        "source_hash": chunk["source_hash"],
        "embedding_provider": "ollama",
        "embedding_model": embedding_model,
        "generated_at": indexed_at,
    }
    return {"id": point_id, "vector": vector, "payload": payload}


def upsert_points(qdrant_url: str, collection: str, points: list[dict[str, Any]], timeout: int) -> None:
    request_json(
        "PUT",
        f"{qdrant_url}/collections/{quote(collection)}/points?wait=true",
        {"points": points},
        timeout,
    )


def verify_point_count(qdrant_url: str, collection: str, expected: int, timeout: int) -> None:
    info = get_collection(qdrant_url, collection, timeout)
    if info is None:
        raise SystemExit(f"Collection `{collection}` disappeared after indexing.")
    actual = int(info.get("result", {}).get("points_count", -1))
    if actual != expected:
        raise SystemExit(f"Expected {expected} Qdrant points, found {actual}.")


def embed_texts(ollama_url: str, model: str, texts: list[str], timeout: int) -> list[list[float]]:
    payload = {"model": model, "input": texts}
    response = request_json("POST", f"{trim_url(ollama_url)}/api/embed", payload, timeout)
    embeddings = response.get("embeddings")
    if not isinstance(embeddings, list) or len(embeddings) != len(texts):
        raise SystemExit("Ollama returned an invalid embeddings response.")
    return [[float(value) for value in embedding] for embedding in embeddings]


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


def update_index_metadata(
    *,
    pack_dir: Path,
    manifest: dict[str, Any],
    qdrant_url: str,
    collection: str,
    embedding_model: str,
    dimension: int,
    indexed_at: str,
    chunk_count: int,
    document_prefix: str,
) -> None:
    metadata = {
        "provider": "ollama",
        "embedding_model": embedding_model,
        "dimension": dimension,
        "distance": DISTANCE,
        "qdrant_url": qdrant_url,
        "collection": collection,
        "chunk_count": chunk_count,
        "document_prefix": document_prefix,
        "indexed_at": indexed_at,
    }
    (pack_dir / "qdrant-index.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest["embedding"] = {
        "status": "embedded",
        "provider": "ollama",
        "model": embedding_model,
        "dimension": dimension,
        "qdrant_url": qdrant_url,
        "qdrant_collection": collection,
        "indexed_at": indexed_at,
    }
    (pack_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_index_metadata(pack_dir: Path) -> dict[str, Any]:
    path = pack_dir / "qdrant-index.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def stable_uuid(*parts: str) -> str:
    digest = hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()
    return str(uuid.UUID(digest[:32]))


def default_collection_name(plugin: str, embedding_model: str) -> str:
    model = embedding_model.split(":", 1)[0]
    return f"{slug(plugin)}__{slug(model)}"


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")


def batches(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def quote(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def trim_url(value: str) -> str:
    return value.rstrip("/")


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
