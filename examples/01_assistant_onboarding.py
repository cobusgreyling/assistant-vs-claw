#!/usr/bin/env python3
"""Onboarding Agent (Assistant) — each hire sees only their own data."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from identity_models.assistant import AssistantAgent
from identity_models.fixtures import build_token_store


def main() -> None:
    agent = AssistantAgent("onboarding-agent", build_token_store())

    print("=== Onboarding Agent (Assistant) ===\n")
    print("Same agent. Different users. Different trust boundaries.\n")

    for user_id, label in [("alice@co", "Alice (new hire)"), ("bob@co", "Bob (new hire)")]:
        for query in ["salary", "onboarding"]:
            result = agent.run(user_id, query)
            print(f"{label} asks: {query!r}")
            print(f"  Actor:  {result.actor_label}")
            print(f"  Pages:  {result.pages or '(none)'}")
            print(f"  Audit:  {result.audit_line}")
            print()


if __name__ == "__main__":
    main()