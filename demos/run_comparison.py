#!/usr/bin/env python3
"""Interactive demo: Assistant vs Claw on the same queries."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from identity_models.assistant import AssistantAgent
from identity_models.claw import ClawAgent
from identity_models.fixtures import build_token_store


def print_result(label: str, result) -> None:
    print(f"\n{label}")
    print(f"  Model:  {result.identity_model.value}")
    print(f"  Actor:  {result.actor_label}")
    print(f"  Pages:  {result.pages or '(none)'}")
    print(f"  Audit:  {result.audit_line}")


def main() -> None:
    assistant = AssistantAgent("onboarding-agent", build_token_store())
    claw = ClawAgent("product-bot", "product-bot@company.com")

    queries = [
        ("salary", "alice@co"),
        ("salary", "bob@co"),
        ("Q3 roadmap", "alice@co"),
        ("Q3 roadmap", "bob@co"),
    ]

    print("=" * 60)
    print("Assistant vs Claw — same prompt, different trust boundary")
    print("=" * 60)

    for query, user_id in queries:
        print(f"\n{'─' * 60}")
        print(f'Query: {query!r}  |  User: {user_id}')
        a_result = assistant.run(user_id, query)
        c_result = claw.run(query, sender=user_id)
        print_result("Assistant", a_result)
        print_result("Claw", c_result)

    print(f"\n{'─' * 60}")
    print("\nMemory isolation (Assistant):")
    print(f"  Alice thread: {assistant.memory.get_thread('alice@co')}")
    print(f"  Bob thread:   {assistant.memory.get_thread('bob@co')}")
    print("\nShared memory (Claw):")
    print(f"  Bot thread:   {claw.memory.get_thread()}")
    print()


if __name__ == "__main__":
    main()