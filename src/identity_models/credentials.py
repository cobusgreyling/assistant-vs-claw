from identity_models.types import Credentials


class TokenStore:
    """Per-user OAuth token store — the backbone of the Assistant model."""

    def __init__(self, tokens: dict[str, Credentials] | None = None) -> None:
        self._tokens = tokens or {}

    def get(self, user_id: str) -> Credentials:
        if user_id not in self._tokens:
            raise KeyError(f"No OAuth tokens for user_id={user_id!r}")
        return self._tokens[user_id]

    def register(self, user_id: str, credentials: Credentials) -> None:
        self._tokens[user_id] = credentials


def load_agent_credentials(service_account: str) -> Credentials:
    """Load fixed service credentials — baked in at Claw creation time."""
    presets = {
        "vendor-intake-bot@company.com": Credentials(
            principal_id="svc_vendor_intake",
            principal_name="Vendor Intake Bot",
            scopes=frozenset({"notion:read", "notion:write:intake"}),
        ),
        "product-bot@company.com": Credentials(
            principal_id="svc_product_bot",
            principal_name="Product Bot",
            scopes=frozenset({"notion:read:competitors", "slack:post"}),
        ),
        "you@company.com": Credentials(
            principal_id="svc_email_agent",
            principal_name="You (Email Agent)",
            scopes=frozenset({"gmail:send", "calendar:read", "calendar:write"}),
        ),
    }
    if service_account not in presets:
        raise KeyError(f"Unknown service account: {service_account!r}")
    return presets[service_account]