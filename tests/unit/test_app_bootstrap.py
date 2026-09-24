from pathlib import Path
from unittest.mock import Mock

from core.app_bootstrap import build_orchestrator
from core.orchestrator import AgentOrchestrator
from core.rag.lazy_retriever import LazyLocalRetriever
from core.schemas.agent_contracts import Department


def test_bootstrap_registers_all_departments():
    gateway = Mock()
    retriever_factory = Mock()

    orchestrator = build_orchestrator(
        gateway=gateway,
        retriever_factory=retriever_factory,
    )

    assert isinstance(orchestrator, AgentOrchestrator)
    assert set(orchestrator.registry.registered_departments()) == set(
        Department
    )
    retriever_factory.assert_not_called()


def test_bootstrap_creates_lazy_retriever_per_department():
    gateway = Mock()
    retriever_factory = Mock()

    orchestrator = build_orchestrator(
        gateway=gateway,
        retriever_factory=retriever_factory,
    )

    for department in Department:
        agent = orchestrator.registry.get(department)
        assert isinstance(agent.retriever, LazyLocalRetriever)

    retriever_factory.assert_not_called()


def test_bootstrap_uses_department_specific_knowledge_bases():
    gateway = Mock()
    retriever_factory = Mock()

    orchestrator = build_orchestrator(
        gateway=gateway,
        retriever_factory=retriever_factory,
    )

    paths = {
        agent.retriever.documents_dir.as_posix()
        for department in Department
        for agent in [orchestrator.registry.get(department)]
    }

    for department in Department:
        assert f"data/knowledge_base/{department.value}" in paths

