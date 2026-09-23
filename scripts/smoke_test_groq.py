import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.risk_restructuring.agent import RiskRestructuringAgent
from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
)


def main():
    context = AgentContext(
        department=Department.RISK_RESTRUCTURING,
        user_role="analyst",
    )

    agent = RiskRestructuringAgent()

    query = (
        "Can the AI approve a restructuring? "
        "Explain what the policy says and who must make the decision."
    )

    print("=" * 70)
    print("RISK & RESTRUCTURING — GROQ + RAG SMOKE TEST")
    print("=" * 70)
    print("Query:", query)

    response = agent.run(query, context)

    print("\nSTATUS:", response.status.value)
    print("\nANSWER:\n", response.answer)

    print("\nSOURCES:")
    for source in response.sources:
        print(
            f"- {source.document_name} | "
            f"Chunk: {source.chunk_id} | "
            f"Score: {source.relevance_score}"
        )

    print("\nACTIONS:", len(response.actions))

    assert response.status == AgentStatus.SUCCESS, (
        f"Expected SUCCESS, got {response.status.value}"
    )
    assert response.answer.strip(), "Agent returned an empty answer."
    assert response.sources, "No source citations returned."
    assert not response.actions, (
        "Risk assistant should not execute or propose actions in this test."
    )

    print("\nPASS: Groq + RAG returned a cited, structured response.")
    print("PASS: No actions were executed or proposed.")


if __name__ == "__main__":
    main()
