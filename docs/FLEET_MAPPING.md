# Fleet Mapping

How the mock patterns in this repo map to [LangSmith Fleet](https://www.langchain.com/langsmith/fleet) and the [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) stack.

| This repo | LangSmith Fleet | Fleet Engineering concern |
|-----------|-----------------|---------------------------|
| `TokenStore.get(user_id)` | Per-user OAuth + channel user mapping | Identity & credentials |
| `load_agent_credentials(...)` | Claw provisioning at agent creation | Identity & credentials |
| `AssistantMemory` | Per-user threads | Identity & credentials |
| `ClawMemory` + `sender` | Shared resource; sender is context only | Identity & credentials |
| `AssistantInbox` | Private per-user inbox for sensitive work | Inbox / HITL |
| `ClawInbox` | Editor-only review before sensitive actions ship | Inbox / HITL |
| `AuditEvent.to_dict()` | Cross-agent audit trail | Accountability |
| `notion_search(creds, query)` | Tool call scoped to principal | Permissions |

## Assistant flow (pseudocode)

```python
slack_user = event["user"]
user_id = fleet.map_channel_user(slack_user)  # U_ALICE → alice@co
creds = token_store.get(user_id)                # OAuth per human
pages = notion_search(creds, query)             # only that human's scope
audit.emit(principal=user_id, model="assistant", action="notion.search", ...)
```

## Claw flow (pseudocode)

```python
creds = agent.credentials                 # fixed at provisioning
pages = notion_search(creds, query)     # same scope for every asker
inbox.submit_if_sensitive(action, sender=event["user"])
audit.emit(principal=creds.id, model="claw", triggered_by=event["user"], ...)
```

## Related fleet docs

- [Five Concerns](https://github.com/cobusgreyling/fleet-engineering/blob/main/docs/five-concerns.md) — identity is concern #3
- [Shared Inbox HITL](https://github.com/cobusgreyling/fleet-engineering/blob/main/patterns/shared-inbox-hitl.md) — Claw editor review
- [Failure Modes](https://github.com/cobusgreyling/fleet-engineering/blob/main/docs/failure-modes.md) — mixed claw/assistant semantics
- [Cross-Agent Audit](https://github.com/cobusgreyling/fleet-engineering/blob/main/patterns/cross-agent-audit.md) — structured accountability