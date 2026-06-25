"""Deterministic comparison scenarios for demos, CLI, and snapshot tests."""

from identity_models.assistant import AssistantAgent
from identity_models.claw import ClawAgent
from identity_models.fixtures import build_token_store
from identity_models.types import AgentResult


def comparison_queries() -> list[tuple[str, str]]:
    return [
        ("salary", "alice@co"),
        ("salary", "bob@co"),
        ("Q3 roadmap", "alice@co"),
        ("Q3 roadmap", "bob@co"),
    ]


def run_comparison() -> list[dict[str, object]]:
    assistant = AssistantAgent("onboarding-agent", build_token_store())
    claw = ClawAgent("product-bot", "product-bot@company.com")
    results: list[dict[str, object]] = []

    for query, user_id in comparison_queries():
        a_result = assistant.run(user_id, query)
        c_result = claw.run(query, sender=user_id)
        results.append(
            {
                "query": query,
                "user_id": user_id,
                "assistant": result_to_dict(a_result),
                "claw": result_to_dict(c_result),
            }
        )

    results.append(
        {
            "memory": {
                "assistant_alice": assistant.memory.get_thread("alice@co"),
                "assistant_bob": assistant.memory.get_thread("bob@co"),
                "claw": claw.memory.get_thread(),
            }
        }
    )
    return results


def result_to_dict(result: AgentResult) -> dict[str, object]:
    payload: dict[str, object] = {
        "identity_model": result.identity_model.value,
        "actor_label": result.actor_label,
        "query": result.query,
        "pages": result.pages,
        "audit_line": result.audit_line,
        "memory_key": result.memory_key,
        "extra": result.extra,
    }
    if result.audit_event is not None:
        payload["audit_event"] = result.audit_event.to_dict()
    return payload