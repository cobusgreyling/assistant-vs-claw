import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from identity_models.assistant import AssistantAgent
from identity_models.claw import ClawAgent
from identity_models.fixtures import build_token_store
from identity_models.types import IdentityModel


@pytest.fixture
def assistant() -> AssistantAgent:
    return AssistantAgent("onboarding-agent", build_token_store())


@pytest.fixture
def claw() -> ClawAgent:
    return ClawAgent("product-bot", "product-bot@company.com")


def test_assistant_scopes_salary_per_user(assistant: AssistantAgent) -> None:
    alice = assistant.run("alice@co", "salary")
    bob = assistant.run("bob@co", "salary")

    assert alice.pages == ["Alice Chen — Compensation"]
    assert bob.pages == ["Bob Martinez — Compensation"]
    assert alice.pages != bob.pages
    assert alice.identity_model == IdentityModel.ASSISTANT
    assert "alice@co" in alice.audit_line


def test_claw_same_scope_for_every_asker(claw: ClawAgent) -> None:
    ceo = claw.run("Q3 roadmap", sender="U_CEO")
    intern = claw.run("Q3 roadmap", sender="U_INTERN")

    assert ceo.pages == intern.pages
    assert "Q3 Roadmap" in ceo.pages[0]
    assert claw.credentials.principal_id in ceo.audit_line


def test_claw_sees_exec_pages_users_cannot(assistant: AssistantAgent, claw: ClawAgent) -> None:
    alice = assistant.run("alice@co", "Q3 roadmap")
    bot = claw.run("Q3 roadmap", sender="alice@co")

    assert "Exec Only" not in " ".join(alice.pages)
    assert any("Exec Only" in page for page in bot.pages)


def test_assistant_memory_isolated(assistant: AssistantAgent) -> None:
    assistant.run("alice@co", "hello alice")
    assistant.run("bob@co", "hello bob")

    assert assistant.memory.get_thread("alice@co") == ["hello alice"]
    assert assistant.memory.get_thread("bob@co") == ["hello bob"]


def test_claw_memory_shared(claw: ClawAgent) -> None:
    claw.run("first", sender="a")
    claw.run("second", sender="b")

    thread = claw.memory.get_thread()
    assert len(thread) == 2
    assert "[from a]" in thread[0]
    assert "[from b]" in thread[1]