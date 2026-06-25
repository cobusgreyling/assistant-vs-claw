"""Seed data for demos and tests."""

from identity_models.credentials import TokenStore
from identity_models.types import Credentials


def build_token_store() -> TokenStore:
    store = TokenStore()
    store.register(
        "alice@co",
        Credentials(
            principal_id="alice@co",
            principal_name="Alice Chen",
            scopes=frozenset({"notion:read", "rippling:read:self"}),
        ),
    )
    store.register(
        "bob@co",
        Credentials(
            principal_id="bob@co",
            principal_name="Bob Martinez",
            scopes=frozenset({"notion:read", "rippling:read:self"}),
        ),
    )
    return store