"""Local FAISS retrieval over Markdown knowledge-base documents."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=4)
def _load_embedding_model(model_name: str) -> SentenceTransformer:
    """Load and reuse an embedding model by model name."""
    return SentenceTransformer(model_name)


@dataclass
class RetrievedChunk:
    source_id: str
    document_name: str
    excerpt: str
    chunk_id: str
    relevance_score: float


class LocalRetriever:
    def __init__(
        self,
        documents_dir: str | Path,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_words: int = 180,
        overlap_words: int = 35,
    ):
        self.documents_dir = Path(documents_dir)
        self.model = _load_embedding_model(model_name)
        self.chunk_words = chunk_words
        self.overlap_words = overlap_words
        self.chunks: list[RetrievedChunk] = []
        self.index = None
        self._build_index()

    def _split_text(self, text: str) -> list[str]:
        words = text.split()
        if not words:
            return []

        step = max(1, self.chunk_words - self.overlap_words)
        return [
            " ".join(words[i : i + self.chunk_words])
            for i in range(0, len(words), step)
        ]

    def _build_index(self) -> None:
        files = sorted(self.documents_dir.glob("*.md"))
        if not files:
            raise ValueError(
                f"No Markdown documents found in {self.documents_dir}"
            )

        texts = []
        for file_path in files:
            content = file_path.read_text(encoding="utf-8-sig")
            for number, excerpt in enumerate(self._split_text(content)):
                self.chunks.append(
                    RetrievedChunk(
                        source_id=file_path.stem,
                        document_name=file_path.name,
                        excerpt=excerpt,
                        chunk_id=f"{file_path.stem}-{number}",
                        relevance_score=0.0,
                    )
                )
                texts.append(excerpt)

        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype("float32")

        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

    def search(
        self,
        query: str,
        top_k: int = 4,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            return []

        query_vector = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype("float32")

        scores, indices = self.index.search(
            query_vector,
            min(top_k, len(self.chunks)),
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            chunk = self.chunks[int(idx)]
            results.append(
                RetrievedChunk(
                    source_id=chunk.source_id,
                    document_name=chunk.document_name,
                    excerpt=chunk.excerpt,
                    chunk_id=chunk.chunk_id,
                    relevance_score=float(score),
                )
            )

        return results
