from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from identity_models.audit import AuditEvent


class IdentityModel(StrEnum):
    ASSISTANT = "assistant"
    CLAW = "claw"


@dataclass(frozen=True)
class Credentials:
    """OAuth or service-account credentials bound to one principal."""

    principal_id: str
    principal_name: str
    scopes: frozenset[str] = field(default_factory=frozenset)


@dataclass
class AgentResult:
    identity_model: IdentityModel
    actor_label: str
    query: str
    pages: list[str]
    audit_line: str
    memory_key: str | None = None
    audit_event: AuditEvent | None = None
    extra: dict[str, Any] = field(default_factory=dict)