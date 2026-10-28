"""Embedding cache and persistent-index contracts; dimensions alone do not identify a model."""

import hashlib
import json
import math
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import TYPE_CHECKING

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from common.config import ROOT, Settings
from common.knowledge import corpus_digest
from common.models import get_embeddings

if TYPE_CHECKING:
    from langchain_chroma import Chroma


def embedding_identity(settings: Settings, dimensions: int) -> dict:
    return {
        "provider": "fixture" if settings.course_offline else settings.embedding_provider,
        "model": "deterministic-fake-v1" if settings.course_offline else settings.embedding_model,
        "dimensions": dimensions,
    }


class CachedEmbeddings(Embeddings):
    """A small SQLite cache isolates query/document namespaces and model identities."""

    def __init__(self, wrapped: Embeddings, path: Path, identity: dict) -> None:
        self.wrapped, self.path, self.identity = wrapped, path, identity
        if int(identity["dimensions"]) < 1:
            raise ValueError("Embedding dimensions must be positive.")
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute("CREATE TABLE IF NOT EXISTS embeddings (key TEXT PRIMARY KEY, vector TEXT)")

    def connection(self) -> closing[sqlite3.Connection]:
        return closing(sqlite3.connect(self.path))

    def _embed(self, text: str, kind: str) -> list[float]:
        key = hashlib.sha256(
            json.dumps([self.identity, kind, text], sort_keys=True).encode()
        ).hexdigest()
        with self.connection() as db:
            row = db.execute("SELECT vector FROM embeddings WHERE key=?", (key,)).fetchone()
            vector = (
                json.loads(row[0])
                if row
                else (
                    self.wrapped.embed_query(text)
                    if kind == "query"
                    else self.wrapped.embed_documents([text])[0]
                )
            )
            if len(vector) != self.identity["dimensions"] or not all(
                math.isfinite(v) for v in vector
            ):
                raise ValueError(
                    "Embedding vector violates the configured dimension/finite contract."
                )
            if row is None:
                db.execute(
                    "INSERT OR REPLACE INTO embeddings VALUES (?,?)", (key, json.dumps(vector))
                )
                db.commit()
        return vector

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text, "document") for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text, "query")


def persistent_index(
    documents: list[Document], settings: Settings, *, name: str = "policies"
) -> "Chroma":
    """Create/reopen an index only when embedding and corpus manifests match exactly."""
    from chromadb.config import Settings as ChromaSettings
    from langchain_chroma import Chroma

    if not name.replace("-", "").isalnum():
        raise ValueError("Index name must contain letters, digits or hyphens.")
    embeddings = get_embeddings(settings=settings)
    dimensions = len(embeddings.embed_query("Brightwave dimension probe"))
    identity = {
        **embedding_identity(settings, dimensions),
        "corpus": corpus_digest(documents),
        "format": 1,
        "collection": "brightwave-" + name,
    }
    directory = ROOT / settings.runtime_dir / "indexes" / name
    manifest = directory / "manifest.json"
    existed = manifest.exists()
    if existed and json.loads(manifest.read_text(encoding="utf-8")) != identity:
        raise ValueError("Stale index: embedding identity or corpus changed. Use a new index name.")
    if not existed and directory.exists() and any(directory.iterdir()):
        raise ValueError("Index has data without a manifest; use a fresh index name.")
    directory.mkdir(parents=True, exist_ok=True)
    store = Chroma(
        collection_name=identity["collection"],
        embedding_function=embeddings,
        persist_directory=str(directory),
        client_settings=ChromaSettings(anonymized_telemetry=False),
        collection_metadata={"hnsw:space": "cosine"},
    )
    if not existed:
        store.add_documents(documents, ids=[str(d.id) for d in documents])
        manifest.write_text(json.dumps(identity, sort_keys=True), encoding="utf-8")
    return store
