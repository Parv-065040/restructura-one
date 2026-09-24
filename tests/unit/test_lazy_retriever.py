from pathlib import Path
from unittest.mock import Mock

from core.rag.lazy_retriever import LazyLocalRetriever


def test_retriever_is_not_created_until_search():
    factory = Mock()
    lazy = LazyLocalRetriever("knowledge/hr", retriever_factory=factory)

    factory.assert_not_called()


def test_first_search_creates_retriever_and_caches_it():
    expected = [Mock()]
    retriever = Mock()
    retriever.search.return_value = expected
    factory = Mock(return_value=retriever)

    lazy = LazyLocalRetriever("knowledge/hr", retriever_factory=factory)

    first_result = lazy.search("leave policy")
    second_result = lazy.search("leave policy")

    assert first_result == expected
    assert second_result == expected
    factory.assert_called_once_with(Path("knowledge/hr"))
    assert retriever.search.call_count == 2


def test_blank_query_does_not_initialize_retriever():
    factory = Mock()
    lazy = LazyLocalRetriever("knowledge/hr", retriever_factory=factory)

    assert lazy.search("   ") == []
    factory.assert_not_called()
