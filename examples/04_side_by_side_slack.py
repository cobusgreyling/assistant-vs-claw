#!/usr/bin/env python3
"""Same Slack message, two authorization outcomes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from identity_models.assistant import AssistantAgent, get_user_credentials
from identity_models.claw import ClawAgent
from identity_models.data import SLACK_USER_MAP, notion_search
from identity_models.fixtures import build_token_store


def main() -> None:
    prompt = "What's our Q3 roadmap?"
    slack_user = "U_ALICE"
    user_id = SLACK_USER_MAP[slack_user]

    print("=== Side by side: one Slack message, two outcomes ===\n")
    print(f'#general: "{prompt}"')
    print(f"Posted by Slack user {slack_user} → {user_id}\n")

    token_store = build_token_store()

    # --- Assistant ---
    print("--- Assistant (on-behalf-of) ---")
    creds = get_user_credentials(user_id, token_store)
    pages = notion_search(creds, "Q3 roadmap")
    print(f"Credentials: {creds.principal_name}'s OAuth tokens")
    print(f"Notion pages: {pages}")
    print("→ Only pages Alice is allowed to see\n")

    # --- Claw ---
    print("--- Claw (fixed identity) ---")
    claw = ClawAgent("product-bot", "product-bot@company.com")
    pages = claw.search_notion("Q3 roadmap")
    print(f"Credentials: {claw.credentials.principal_name} (fixed at setup)")
    print(f"Notion pages: {pages}")
    print("→ Whatever the bot account can see — same for every asker\n")

    # --- Common mistake ---
    print("--- Common mistake: Claw with your personal OAuth ---")
    personal = get_user_credentials(user_id, token_store)
    mistaken_pages = notion_search(personal, "salary")
    print(f"If the bot used Alice's personal OAuth: {mistaken_pages}")
    print("→ Anyone who can message the bot inherits Alice's access. Don't do this.")
    print("→ Fix: give the Claw its own scoped service account.\n")


if __name__ == "__main__":
    main()