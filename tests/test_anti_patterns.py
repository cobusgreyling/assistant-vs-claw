"""Tests for the common mistake: Claw wired with personal OAuth."""

from identity_models.assistant import get_user_credentials
from identity_models.data import notion_search
from identity_models.fixtures import build_token_store


def test_personal_oauth_exposes_private_data_to_shared_bot() -> None:
    """Simulates a Claw mistakenly using the invoker's personal tokens."""
    token_store = build_token_store()
    personal = get_user_credentials("alice@co", token_store)
    pages = notion_search(personal, "salary")

    assert pages == ["Alice Chen — Compensation"]
    assert any("Compensation" in page for page in pages)


def test_scoped_claw_does_not_inherit_user_salary() -> None:
    from identity_models.claw import ClawAgent

    claw = ClawAgent("product-bot", "product-bot@company.com")
    pages = claw.search_notion("salary")
    assert pages == []