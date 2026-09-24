"""Lazy initialization wrapper for department retrievers."""

from pathlib import Path
from threading import Lock
from typing import Callable

from core.rag.retriever import LocalRetriever, RetrievedChunk


class LazyLocalRetriever:
    """Initialize a LocalRetriever only when search is first called."""

    def __init__(
        self,
        documents_dir: str | Path,
        retriever_factory: Callable[..., LocalRetriever] = LocalRetriever,
    ) -> None:
        self.documents_dir = Path(documents_dir)
        self._retriever_factory = retriever_factory
        self._retriever: LocalRetriever | None = None
        self._lock = Lock()

    def _get_retriever(self) -> LocalRetriever:
        if self._retriever is None:
            with self._lock:
                if self._retriever is None:
                    self._retriever = self._retriever_factory(
                        self.documents_dir
                    )

        return self._retriever

    def search(
        self,
        query: str,
        top_k: int = 4,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            return []

        return self._get_retriever().search(query, top_k=top_k)
