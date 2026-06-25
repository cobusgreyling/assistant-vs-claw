"""Memory scoping: per-user for Assistants, shared for Claws."""


class AssistantMemory:
    """Each user gets an isolated thread — Alice's context never leaks to Bob."""

    def __init__(self) -> None:
        self._threads: dict[str, list[str]] = {}

    def append(self, user_id: str, message: str) -> None:
        self._threads.setdefault(user_id, []).append(message)

    def get_thread(self, user_id: str) -> list[str]:
        return list(self._threads.get(user_id, []))


class ClawMemory:
    """Shared team resource — one inbox, one history for the bot identity."""

    def __init__(self) -> None:
        self._shared: list[str] = []

    def append(self, message: str, sender: str | None = None) -> None:
        prefix = f"[from {sender}] " if sender else ""
        self._shared.append(f"{prefix}{message}")

    def get_thread(self) -> list[str]:
        return list(self._shared)