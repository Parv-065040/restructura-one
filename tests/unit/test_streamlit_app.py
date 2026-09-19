from types import SimpleNamespace
from unittest.mock import patch

from core.schemas.agent_contracts import AgentStatus
from app import render_response


def make_response(
    status=AgentStatus.SUCCESS,
    sources=None,
    actions=None,
):
    return SimpleNamespace(
        status=status,
        answer="Synthetic test response.",
        sources=sources or [],
        actions=actions or [],
    )


def test_render_response_displays_answer():
    response = make_response()

    with patch("app.st") as mock_st:
        render_response(response)

    mock_st.success.assert_called_once_with("Request completed")
    mock_st.markdown.assert_called_once_with("Synthetic test response.")


def test_render_response_displays_insufficient_evidence():
    response = make_response(status=AgentStatus.INSUFFICIENT_EVIDENCE)

    with patch("app.st") as mock_st:
        render_response(response)

    mock_st.warning.assert_called_once_with("Insufficient evidence")


def test_render_response_displays_error():
    response = make_response(status=AgentStatus.ERROR)

    with patch("app.st") as mock_st:
        render_response(response)

    mock_st.error.assert_called_once_with("Assistant error")


def test_render_response_displays_sources():
    source = SimpleNamespace(
        document_name="demo.md",
        source_id="SRC-001",
        relevance_score=0.91,
        excerpt="Synthetic evidence excerpt.",
    )
    response = make_response(sources=[source])

    with patch("app.st") as mock_st:
        mock_st.expander.return_value.__enter__.return_value = None
        render_response(response)

    mock_st.expander.assert_called_once_with("Sources (1)")


def test_render_response_displays_proposed_actions():
    action = SimpleNamespace(
        action_type="review_request",
        description="Review this proposed action.",
        status=SimpleNamespace(value="proposed"),
        requires_approval=True,
    )
    response = make_response(actions=[action])

    with patch("app.st") as mock_st:
        mock_st.container.return_value.__enter__.return_value = None
        render_response(response)

    mock_st.subheader.assert_called_once_with("Proposed actions")
    mock_st.caption.assert_any_call(
        "These are proposals only. No action is executed by this interface."
    )
