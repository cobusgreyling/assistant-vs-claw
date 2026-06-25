from identity_models.assistant import AssistantAgent
from identity_models.claw import ClawAgent
from identity_models.fixtures import build_token_store
from identity_models.types import IdentityModel


def test_assistant_audit_event_shape() -> None:
    agent = AssistantAgent("onboarding-agent", build_token_store())
    result = agent.run("alice@co", "salary")
    assert result.audit_event is not None
    payload = result.audit_event.to_dict()
    assert payload == {
        "principal": "alice@co",
        "model": "assistant",
        "action": "notion.search",
        "query": "salary",
        "pages": ("Alice Chen — Compensation",),
        "triggered_by": "alice@co",
    }


def test_claw_audit_event_records_sender_as_context() -> None:
    agent = ClawAgent("email-agent", "you@company.com")
    result = agent.run("meeting request", sender="stranger@competitor.com")
    assert result.audit_event is not None
    assert result.audit_event.principal == "svc_email_agent"
    assert result.audit_event.model == IdentityModel.CLAW
    assert result.audit_event.triggered_by == "stranger@competitor.com"