"""Canonical data contracts shared by all Restructura One agents."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class Department(str, Enum):
    RISK_RESTRUCTURING = "risk_restructuring"
    FINANCE = "finance"
    SALES = "sales"
    IT = "it"
    HR = "hr"
    MARKETING = "marketing"
    LEGAL_COMPLIANCE = "legal_compliance"
    CUSTOMER_SUPPORT = "customer_support"


class AgentStatus(str, Enum):
    SUCCESS = "success"
    NEEDS_CLARIFICATION = "needs_clarification"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    ERROR = "error"


class ActionStatus(str, Enum):
    PROPOSED = "proposed"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class SourceCitation(BaseModel):
    """A source retrieved from the department's knowledge base."""

    model_config = ConfigDict(extra="forbid")

    source_id: str
    document_name: str
    excerpt: str | None = None
    page: int | None = Field(default=None, ge=1)
    chunk_id: str | None = None
    relevance_score: float | None = Field(default=None, ge=0, le=1)


class ActionProposal(BaseModel):
    """A proposed action; this contract does not execute it."""

    model_config = ConfigDict(extra="forbid")

    action_id: str
    action_type: str
    description: str
    requires_approval: bool = True
    status: ActionStatus = ActionStatus.PROPOSED
    parameters: dict[str, Any] = Field(default_factory=dict)


class AgentContext(BaseModel):
    """Request context passed to every departmental agent."""

    model_config = ConfigDict(extra="forbid")

    department: Department
    session_id: str | None = None
    user_role: str = "employee"
    permissions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Standardized response returned by every departmental agent."""

    model_config = ConfigDict(extra="forbid")

    department: Department
    answer: str
    status: AgentStatus = AgentStatus.SUCCESS
    sources: list[SourceCitation] = Field(default_factory=list)
    actions: list[ActionProposal] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
