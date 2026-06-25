"""Illustrate Assistant (on-behalf-of) vs Claw (fixed-identity) authorization models."""

from identity_models.assistant import AssistantAgent
from identity_models.audit import AuditEvent
from identity_models.claw import ClawAgent
from identity_models.credentials import TokenStore
from identity_models.inbox import AssistantInbox, ClawInbox
from identity_models.types import AgentResult, Credentials, IdentityModel

__all__ = [
    "AssistantAgent",
    "AssistantInbox",
    "AuditEvent",
    "ClawAgent",
    "ClawInbox",
    "AgentResult",
    "Credentials",
    "IdentityModel",
    "TokenStore",
]