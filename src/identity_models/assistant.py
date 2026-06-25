"""Assistant pattern — credentials follow the human who invoked the agent."""

from identity_models.audit import AuditEvent
from identity_models.credentials import TokenStore
from identity_models.data import notion_search
from identity_models.memory import AssistantMemory
from identity_models.types import AgentResult, Credentials, IdentityModel


def get_user_credentials(user_id: str, token_store: TokenStore) -> Credentials:
    """Look up OAuth tokens for whoever invoked the agent."""
    return token_store.get(user_id)


class AssistantAgent:
    """On-behalf-of agent: wears the user's badge for every tool call."""

    def __init__(self, name: str, token_store: TokenStore) -> None:
        self.name = name
        self.token_store = token_store
        self.memory = AssistantMemory()

    def search_notion(self, query: str, user_id: str) -> list[str]:
        creds = get_user_credentials(user_id, self.token_store)
        return notion_search(creds, query)

    def run(self, user_id: str, message: str) -> AgentResult:
        self.memory.append(user_id, message)
        pages = self.search_notion(message, user_id)
        creds = get_user_credentials(user_id, self.token_store)
        audit_event = AuditEvent(
            principal=creds.principal_id,
            model=IdentityModel.ASSISTANT,
            action="notion.search",
            query=message,
            pages=tuple(pages),
            triggered_by=user_id,
        )
        return AgentResult(
            identity_model=IdentityModel.ASSISTANT,
            actor_label=f"{creds.principal_name} (via {self.name})",
            query=message,
            pages=pages,
            audit_line=f"{creds.principal_id} searched Notion for {message!r}",
            memory_key=user_id,
            audit_event=audit_event,
        )