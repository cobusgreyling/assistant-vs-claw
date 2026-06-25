"""Console entry points for demos and examples."""

from identity_models.assistant import AssistantAgent, get_user_credentials
from identity_models.claw import ClawAgent
from identity_models.data import SLACK_USER_MAP, notion_search
from identity_models.fixtures import build_token_store
from identity_models.types import AgentResult


def _print_result(label: str, result: AgentResult) -> None:
    print(f"\n{label}")
    print(f"  Model:  {result.identity_model.value}")
    print(f"  Actor:  {result.actor_label}")
    print(f"  Pages:  {result.pages or '(none)'}")
    print(f"  Audit:  {result.audit_line}")
    if result.audit_event is not None:
        print(f"  Event:  {result.audit_event.to_dict()}")


def run_comparison_main() -> None:
    assistant = AssistantAgent("onboarding-agent", build_token_store())
    claw = ClawAgent("product-bot", "product-bot@company.com")

    print("=" * 60)
    print("Assistant vs Claw — same prompt, different trust boundary")
    print("=" * 60)

    for query, user_id in [
        ("salary", "alice@co"),
        ("salary", "bob@co"),
        ("Q3 roadmap", "alice@co"),
        ("Q3 roadmap", "bob@co"),
    ]:
        print(f"\n{'─' * 60}")
        print(f"Query: {query!r}  |  User: {user_id}")
        _print_result("Assistant", assistant.run(user_id, query))
        _print_result("Claw", claw.run(query, sender=user_id))

    print(f"\n{'─' * 60}")
    print("\nMemory isolation (Assistant):")
    print(f"  Alice thread: {assistant.memory.get_thread('alice@co')}")
    print(f"  Bob thread:   {assistant.memory.get_thread('bob@co')}")
    print("\nShared memory (Claw):")
    print(f"  Bot thread:   {claw.memory.get_thread()}")
    print()


def run_assistant_onboarding() -> None:
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


def run_claw_email() -> None:
    agent = ClawAgent("email-agent", "you@company.com")
    print("=== Email Agent (Claw) ===\n")
    print("Inbound mail from anyone. Identity never changes.\n")
    for sender, message in [
        ("stranger@competitor.com", "Can we grab 30 minutes next week?"),
        ("recruiter@agency.io", "Interested in a VP role?"),
    ]:
        result = agent.run(message, sender=sender)
        print(f"From: {sender}")
        print(f"  Message: {message}")
        print(f"  Actor:   {result.actor_label}")
        print(f"  Audit:   {result.audit_line}")
        print(f"  Note:    Calendar checked as {agent.credentials.principal_name}, not as sender")
        print()


def run_claw_product() -> None:
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


def run_side_by_side_slack() -> None:
    prompt = "What's our Q3 roadmap?"
    slack_user = "U_ALICE"
    user_id = SLACK_USER_MAP[slack_user]
    print("=== Side by side: one Slack message, two outcomes ===\n")
    print(f'#general: "{prompt}"')
    print(f"Posted by Slack user {slack_user} → {user_id}\n")
    token_store = build_token_store()
    print("--- Assistant (on-behalf-of) ---")
    creds = get_user_credentials(user_id, token_store)
    pages = notion_search(creds, "Q3 roadmap")
    print(f"Credentials: {creds.principal_name}'s OAuth tokens")
    print(f"Notion pages: {pages}")
    print("→ Only pages Alice is allowed to see\n")
    print("--- Claw (fixed identity) ---")
    claw = ClawAgent("product-bot", "product-bot@company.com")
    pages = claw.search_notion("Q3 roadmap")
    print(f"Credentials: {claw.credentials.principal_name} (fixed at setup)")
    print(f"Notion pages: {pages}")
    print("→ Whatever the bot account can see — same for every asker\n")
    print("--- Common mistake: Claw with your personal OAuth ---")
    personal = get_user_credentials(user_id, token_store)
    mistaken_pages = notion_search(personal, "salary")
    print(f"If the bot used Alice's personal OAuth: {mistaken_pages}")
    print("→ Anyone who can message the bot inherits Alice's access. Don't do this.")
    print("→ Fix: give the Claw its own scoped service account.\n")


def run_claw_vendor_intake() -> None:
    agent = ClawAgent("vendor-intake-bot", "vendor-intake-bot@company.com")
    print("=== Vendor Intake Bot (Claw) ===\n")
    print("Shared queue. Scoped service account. Editor reviews before action.\n")
    for sender in ["U_PROCUREMENT", "U_LEGAL"]:
        result = agent.run("vendor intake queue", sender=sender)
        print(f"Asked by Slack user {sender}")
        print(f"  Pages: {result.pages}")
        print(f"  Audit: {result.audit_line}")
        print()