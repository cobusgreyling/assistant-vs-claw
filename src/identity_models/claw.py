"""Claw pattern — one fixed identity, always."""

from identity_models.credentials import load_agent_credentials
from identity_models.data import notion_search
from identity_models.memory import ClawMemory
from identity_models.types import AgentResult, Credentials, IdentityModel


class ClawAgent:
    """Fixed-identity agent: same credentials whether CEO or intern triggers it."""

    def __init__(self, name: str, service_account: str) -> None:
        self.name = name
        self.credentials: Credentials = load_agent_credentials(service_account)
        self.memory = ClawMemory()

    def search_notion(self, query: str) -> list[str]:
        return notion_search(self.credentials, query)

    def run(self, message: str, sender: str | None = None) -> AgentResult:
        # sender is context for the reply, NOT for auth
        self.memory.append(message, sender=sender)
        pages = self.search_notion(message)
        sender_note = f" (triggered by {sender})" if sender else ""
        return AgentResult(
            identity_model=IdentityModel.CLAW,
            actor_label=f"{self.credentials.principal_name}{sender_note}",
            query=message,
            pages=pages,
            audit_line=f"{self.credentials.principal_id} searched Notion for {message!r}",
            extra={"sender": sender},
        )