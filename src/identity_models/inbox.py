"""Inbox patterns — per-user private queues vs editor-only Claw review."""

from dataclasses import dataclass
from enum import StrEnum
from uuid import uuid4


class InboxStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class InboxItem:
    item_id: str
    agent_name: str
    action: str
    principal: str
    status: InboxStatus
    owner: str | None = None
    sender: str | None = None


class AssistantInbox:
    """Private per-user inbox for sensitive personal Assistant work."""

    def __init__(self) -> None:
        self._items: dict[str, list[InboxItem]] = {}

    def submit(self, user_id: str, agent_name: str, action: str, principal: str) -> InboxItem:
        item = InboxItem(
            item_id=uuid4().hex[:8],
            agent_name=agent_name,
            action=action,
            principal=principal,
            status=InboxStatus.PENDING,
            owner=user_id,
        )
        self._items.setdefault(user_id, []).append(item)
        return item

    def get_items(self, user_id: str) -> list[InboxItem]:
        return list(self._items.get(user_id, []))


class ClawInbox:
    """Editor-only review queue before sensitive Claw actions ship."""

    def __init__(self, editors: set[str]) -> None:
        self._editors = editors
        self._queue: list[InboxItem] = []

    def submit(
        self,
        agent_name: str,
        action: str,
        principal: str,
        sender: str | None = None,
    ) -> InboxItem:
        item = InboxItem(
            item_id=uuid4().hex[:8],
            agent_name=agent_name,
            action=action,
            principal=principal,
            status=InboxStatus.PENDING,
            sender=sender,
        )
        self._queue.append(item)
        return item

    def approve(self, item_id: str, editor: str) -> InboxItem:
        if editor not in self._editors:
            raise PermissionError(f"{editor!r} is not an inbox editor")
        for item in self._queue:
            if item.item_id == item_id:
                item.status = InboxStatus.APPROVED
                return item
        raise KeyError(f"No inbox item {item_id!r}")

    def pending(self) -> list[InboxItem]:
        return [item for item in self._queue if item.status == InboxStatus.PENDING]