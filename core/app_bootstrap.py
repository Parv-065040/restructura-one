"""Application bootstrap for Restructura One."""

from pathlib import Path

from agents.customer_support.agent import CustomerSupportAgent
from agents.finance.agent import FinanceAgent
from agents.hr.agent import HRAgent
from agents.it.agent import ITAgent
from agents.legal_compliance.agent import LegalComplianceAgent
from agents.marketing.agent import MarketingAgent
from agents.risk_restructuring.agent import RiskRestructuringAgent
from agents.sales.agent import SalesAgent
from core.agent_registry import AgentRegistry
from core.llm.groq_gateway import GroqGateway
from core.orchestrator import AgentOrchestrator
from core.rag.retriever import LocalRetriever
from core.schemas.agent_contracts import Department


KNOWLEDGE_BASE_ROOT = Path("data/knowledge_base")


def build_orchestrator(
    gateway=None,
    retriever_factory=LocalRetriever,
) -> AgentOrchestrator:
    """Build and return an orchestrator with all 8 agents registered.

    A shared gateway is used across agents. Each agent receives a
    retriever built exclusively from its own department's documents.
    Dependencies can be injected for tests.
    """
    shared_gateway = gateway if gateway is not None else GroqGateway()
    registry = AgentRegistry()

    agent_config = [
        (
            Department.RISK_RESTRUCTURING,
            RiskRestructuringAgent,
            "risk_restructuring",
        ),
        (Department.FINANCE, FinanceAgent, "finance"),
        (Department.SALES, SalesAgent, "sales"),
        (Department.IT, ITAgent, "it"),
        (Department.HR, HRAgent, "hr"),
        (Department.MARKETING, MarketingAgent, "marketing"),
        (
            Department.LEGAL_COMPLIANCE,
            LegalComplianceAgent,
            "legal_compliance",
        ),
        (
            Department.CUSTOMER_SUPPORT,
            CustomerSupportAgent,
            "customer_support",
        ),
    ]

    for department, agent_class, folder in agent_config:
        retriever = retriever_factory(KNOWLEDGE_BASE_ROOT / folder)
        agent = agent_class(
            retriever=retriever,
            gateway=shared_gateway,
        )
        registry.register(department, agent)

    return AgentOrchestrator(registry)
