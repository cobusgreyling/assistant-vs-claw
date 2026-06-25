"""Structured audit events — Fleet-style accountability records."""

from dataclasses import asdict, dataclass
from typing import Any

from identity_models.types import IdentityModel


@dataclass(frozen=True)
class AuditEvent:
    principal: str
    model: IdentityModel
    action: str
    query: str
    pages: tuple[str, ...]
    triggered_by: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["model"] = self.model.value
        return payload