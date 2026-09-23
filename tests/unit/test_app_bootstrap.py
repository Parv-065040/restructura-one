from pathlib import Path
from unittest.mock import Mock

import pytest

from core.app_bootstrap import build_orchestrator
from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import Department


def test_bootstrap_registers_all_departments():
    gateway = Mock()
    retriever_factory = Mock(return_value=Mock())

    orchestrator = build_orchestrator(
        gateway=gateway,
        retriever_factory=retriever_factory,
    )

    assert isinstance(orchestrator, AgentOrchestrator)
    assert set(orchestrator.registry.registered_departments()) == set(
        Department
    )


def test_bootstrap_creates_one_retriever_per_department():
    gateway = Mock()
    retriever_factory = Mock(return_value=Mock())

    build_orchestrator(
        gateway=gateway,
        retriever_factory=retriever_factory,
    )

    assert retriever_factory.call_count == len(Department)


def test_bootstrap_uses_department_specific_knowledge_bases():
    gateway = Mock()
    retriever_factory = Mock(return_value=Mock())

    build_orchestrator(
        gateway=gateway,
        retriever_factory=retriever_factory,
    )

    paths = {
        Path(call.args[0]).as_posix()
        for call in retriever_factory.call_args_list
    }

    for department in Department:
        assert f"data/knowledge_base/{department.value}" in paths
