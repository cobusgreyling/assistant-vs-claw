"""Illustrate Assistant (on-behalf-of) vs Claw (fixed-identity) authorization models."""

from identity_models.assistant import AssistantAgent
from identity_models.claw import ClawAgent
from identity_models.credentials import Credentials, TokenStore
from identity_models.types import AgentResult, IdentityModel

__all__ = [
    "AssistantAgent",
    "ClawAgent",
    "AgentResult",
    "Credentials",
    "IdentityModel",
    "TokenStore",
]