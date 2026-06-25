import pytest

from identity_models.inbox import AssistantInbox, ClawInbox, InboxStatus


def test_assistant_inbox_is_private_per_user() -> None:
    inbox = AssistantInbox()
    alice_item = inbox.submit("alice@co", "onboarding-agent", "rippling.read", "alice@co")
    bob_item = inbox.submit("bob@co", "onboarding-agent", "rippling.read", "bob@co")

    assert alice_item.owner == "alice@co"
    assert bob_item.owner == "bob@co"
    assert inbox.get_items("alice@co") == [alice_item]
    assert inbox.get_items("bob@co") == [bob_item]
    assert inbox.get_items("alice@co") != inbox.get_items("bob@co")


def test_claw_inbox_requires_editor_approval() -> None:
    inbox = ClawInbox(editors={"ops-lead@co"})
    item = inbox.submit(
        "vendor-intake-bot",
        "notion.write:intake",
        "svc_vendor_intake",
        sender="U_PROCUREMENT",
    )
    assert item.status == InboxStatus.PENDING
    assert inbox.pending() == [item]

    approved = inbox.approve(item.item_id, "ops-lead@co")
    assert approved.status == InboxStatus.APPROVED
    assert inbox.pending() == []


def test_claw_inbox_rejects_non_editors() -> None:
    inbox = ClawInbox(editors={"ops-lead@co"})
    item = inbox.submit("vendor-intake-bot", "notion.write:intake", "svc_vendor_intake")
    with pytest.raises(PermissionError, match="not an inbox editor"):
        inbox.approve(item.item_id, "intern@co")