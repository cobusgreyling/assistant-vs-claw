"""Mock company data — same Notion workspace, different visibility per principal."""

from identity_models.types import Credentials

# Notion pages keyed by page id
NOTION_PAGES: dict[str, dict[str, str | list[str]]] = {
    "alice-salary": {
        "title": "Alice Chen — Compensation",
        "content": "Salary: $185k base | Start: 2024-03-01",
        "visible_to": ["alice@co"],
    },
    "bob-salary": {
        "title": "Bob Martinez — Compensation",
        "content": "Salary: $162k base | Start: 2023-09-15",
        "visible_to": ["bob@co"],
    },
    "alice-onboarding": {
        "title": "Alice — Week 1 Checklist",
        "content": "Complete Rippling profile, set up laptop",
        "visible_to": ["alice@co"],
    },
    "bob-onboarding": {
        "title": "Bob — Week 1 Checklist",
        "content": "Shadow sales calls, CRM access",
        "visible_to": ["bob@co"],
    },
    "q3-roadmap-public": {
        "title": "Q3 Roadmap (Team)",
        "content": "Ship billing v2, launch mobile beta",
        "visible_to": ["alice@co", "bob@co", "svc_product_bot"],
    },
    "q3-roadmap-exec": {
        "title": "Q3 Roadmap (Exec Only)",
        "content": "Acquisition target evaluation — CONFIDENTIAL",
        "visible_to": ["svc_product_bot"],
    },
    "competitor-acme": {
        "title": "Competitor Watch — Acme Corp",
        "content": "Acme launched enterprise tier at $49/seat",
        "visible_to": ["svc_product_bot"],
    },
    "vendor-intake-queue": {
        "title": "Vendor Intake Queue",
        "content": "3 pending NDAs, 1 security review",
        "visible_to": ["svc_vendor_intake"],
    },
}

SLACK_USER_MAP: dict[str, str] = {
    "U_ALICE": "alice@co",
    "U_BOB": "bob@co",
}


def notion_search(credentials: Credentials, query: str) -> list[str]:
    """Return page titles the given principal is allowed to see."""
    query_lower = query.lower()
    principal_aliases = {credentials.principal_id, credentials.principal_name}
    visible: list[str] = []
    for page in NOTION_PAGES.values():
        allowed = set(page["visible_to"])
        if not principal_aliases.intersection(allowed):
            continue
        title = str(page["title"])
        content = str(page["content"])
        if query_lower in title.lower() or query_lower in content.lower():
            visible.append(title)
    return visible