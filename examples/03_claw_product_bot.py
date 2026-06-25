#!/usr/bin/env python3
"""Product Agent (Claw) — one curated Notion account for the whole team."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from identity_models.claw import ClawAgent


def main() -> None:
    agent = ClawAgent("product-bot", "product-bot@company.com")

    print("=== Product Agent (Claw) ===\n")
    print("@product-bot in Slack — same scope for CEO and intern.\n")

    for sender in ["U_CEO", "U_INTERN"]:
        result = agent.run("Q3 roadmap", sender=sender)
        print(f"Asked by Slack user {sender}")
        print(f"  Pages: {result.pages}")
        print(f"  Audit: {result.audit_line}")
        print()

    result = agent.run("competitor Acme", sender="U_PM")
    print("Asked by PM: 'competitor Acme'")
    print(f"  Pages: {result.pages}")
    print()


if __name__ == "__main__":
    main()