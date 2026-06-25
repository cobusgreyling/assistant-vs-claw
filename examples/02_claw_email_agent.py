#!/usr/bin/env python3
"""Email Agent (Claw) — always acts as you, sender is just context."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from identity_models.claw import ClawAgent


def main() -> None:
    agent = ClawAgent("email-agent", "you@company.com")

    print("=== Email Agent (Claw) ===\n")
    print("Inbound mail from anyone. Identity never changes.\n")

    strangers = [
        ("stranger@competitor.com", "Can we grab 30 minutes next week?"),
        ("recruiter@agency.io", "Interested in a VP role?"),
    ]

    for sender, message in strangers:
        result = agent.run(message, sender=sender)
        print(f"From: {sender}")
        print(f"  Message: {message}")
        print(f"  Actor:   {result.actor_label}")
        print(f"  Audit:   {result.audit_line}")
        print(f"  Note:    Calendar checked as {agent.credentials.principal_name}, not as sender")
        print()


if __name__ == "__main__":
    main()