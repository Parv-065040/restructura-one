import pytest
from pydantic import ValidationError

from core.schemas.agent_contracts import (
    ActionProposal,
    AgentContext,
    AgentResponse,
    AgentStatus,
    Department,
    SourceCitation,
)


def test_agent_context_uses_department_enum():
    context = AgentContext(department=Department.FINANCE)

    assert context.department == Department.FINANCE
    assert context.permissions == []


def test_agent_response_serializes_to_json():
    response = AgentResponse(
        department=Department.HR,
        answer="The leave policy allows  casual leave subject to approval.",
        sources=[
            SourceCitation(
                source_id="hr-policy-001",
                document_name="Leave Policy",
                page=2,
            )
        ],
    )

    payload = response.model_dump(mode="json")

    assert payload["department"] == "hr"
    assert payload["status"] == "success"
    assert payload["sources"][0]["document_name"] == "Leave Policy"


def test_agent_response_defaults_to_empty_actions_and_sources():
    response = AgentResponse(
        department=Department.IT,
        answer="Please provide more details.",
        status=AgentStatus.NEEDS_CLARIFICATION,
    )

    assert response.actions == []
    assert response.sources == []


def test_action_requires_approval_by_default():
    action = ActionProposal(
        action_id="action-001",
        action_type="draft_email",
        description="Prepare a draft email for review.",
    )

    assert action.requires_approval is True


def test_invalid_relevance_score_is_rejected():
    with pytest.raises(ValidationError):
        SourceCitation(
            source_id="source-001",
            document_name="Test",
            relevance_score=1.5,
        )


def test_unknown_response_fields_are_rejected():
    with pytest.raises(ValidationError):
        AgentResponse(
            department=Department.FINANCE,
            answer="Test",
            unexpected_field="not allowed",
        )
