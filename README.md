# Assistant vs Claw

> **On-behalf-of Assistants and fixed-identity Claws** — and why the distinction matters the moment you share an agent.

Runnable illustrations of the two authorization models in [LangSmith Fleet](https://www.langchain.com/langsmith/fleet). Same word — *agent*. Two completely different trust boundaries.

**Created by [Cobus Greyling](https://github.com/cobusgreyling).** Part of the [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) stack.

---

## The bottleneck moved

Six months ago, building an agent meant hiring an engineer. Today you describe a job in plain English and get a working agent back.

The hard part is no longer *"can the LLM call a tool?"* It is **who is the agent when it calls that tool?**

- When **Alice** asks your onboarding agent to pull her Rippling profile, it should use **Alice's credentials**.
- When **Bob** asks the same agent, it should use **Bob's**. Neither should see the other's private Notion pages.
- When your **email agent** replies to a stranger who wants a meeting, it should **not** become that stranger. It acts as **you** — or a dedicated service identity with a fixed calendar and inbox.

LangSmith Fleet names them **Assistants** and **Claws**. The difference is not intelligence or autonomy. It is **whose keys are in the lock**.

| | **Assistant** | **Claw** |
|---|---------------|----------|
| Acts as | The person using it | Itself |
| Credentials | Per-user, at runtime | Fixed, at setup |
| Data scope | Whatever that user can see | Whatever the agent account can see |
| Best for | Personal, per-user workflows | Shared bots, scheduled jobs, public channels |

**LangChain shorthand:**

- Assistants → **on-behalf-of**
- Claws → **own fixed credentials**

If you have used [OpenClaw](https://github.com/openclaw/openclaw), you have already met the Claw model: create an agent, give it accounts, let others interact with it — but everyone shares the same underlying identity.

---

## Quick start

```bash
git clone https://github.com/cobusgreyling/assistant-vs-claw.git
cd assistant-vs-claw

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the full side-by-side comparison
python demos/run_comparison.py

# Or run individual scenarios
python examples/01_assistant_onboarding.py
python examples/02_claw_email_agent.py
python examples/03_claw_product_bot.py
python examples/04_side_by_side_slack.py

# Verify trust boundaries
pytest -q
```

No API keys required — everything runs against mock Notion, Slack, and OAuth data.

---

## What this looks like in code

Fleet hides most of this behind OAuth and channel mapping. The pattern is the same whether you wire LangGraph by hand or click "Set identity" in the UI.

### Assistant: credentials follow the human

```python
# credentials follow whoever invoked the agent
def get_user_credentials(user_id: str) -> Credentials:
    return token_store.get(user_id)  # Alice gets Alice's tokens

def search_notion(query: str, user_id: str) -> list[str]:
    creds = get_user_credentials(user_id)
    return notion_search(creds, query)  # only pages THAT user can access

def run_agent(user_id: str, message: str):
    return agent.invoke({"message": message, "user_id": user_id})
```

Alice and Bob hit the same agent. Different tokens. Different data. The agent is a proxy — it wears your badge.

See: [`src/identity_models/assistant.py`](src/identity_models/assistant.py)

### Claw: credentials baked in at birth

```python
# one identity, always
AGENT_CREDENTIALS = load_credentials("product-bot@company.com")

def search_notion(query: str) -> list[str]:
    return notion_search(AGENT_CREDENTIALS, query)  # same scope for everyone

def run_agent(message: str, sender: str | None = None):
    # sender is context for the reply, NOT for auth
    return agent.invoke({"message": message, "sender": sender})
```

A competitor researcher, a vendor-intake bot, a `@weekly-numbers` Slack agent — same credentials whether the CEO or an intern triggers it. The agent has its own desk, not yours.

See: [`src/identity_models/claw.py`](src/identity_models/claw.py)

### Side by side: one Slack message, two outcomes

Someone posts in `#general`: *"What's our Q3 roadmap?"*

| Model | What happens |
|-------|----------------|
| **Assistant** | Map `U_ALICE` → `alice@co`, load Alice's OAuth, search Notion → only pages **Alice** can see |
| **Claw** | Search Notion with `product-bot@company.com` credentials → same pages for **every** asker |

Same prompt. Same tool. Different trust boundary.

Run it: [`examples/04_side_by_side_slack.py`](examples/04_side_by_side_slack.py)

---

## Three real agents, three design choices

| Agent | Model | Why |
|-------|-------|-----|
| **Onboarding Agent** | Assistant | Each hire sees their Rippling record and Notion docs. Alice's thread must never surface Bob's salary. |
| **Email Agent** | Claw | Responds to inbound mail from anyone. Always checks your calendar and drafts from your identity. Sender is context, not delegation. |
| **Product Agent** | Claw | Monitors competitors in a shared Notion workspace as `@product-bot`. One curated account — not everyone's personal permissions mashed together. |

Examples: [`examples/`](examples/)

---

## How to choose

See the full decision guide: [`docs/CHOOSING.md`](docs/CHOOSING.md)

**Pick an Assistant when** each user must see only their own data, audit trails should name the human, and personalization is the point.

**Pick a Claw when** the agent is a team resource, runs on a schedule or public channel, or needs a deliberately scoped service account.

**Common mistake:** building a Claw with your personal OAuth. Anyone who messages the bot inherits everything you can see. Give the Claw its own account with only the permissions the job needs.

---

## Beyond credentials: memory and inbox

| Concern | Assistant | Claw |
|---------|-----------|------|
| Memory | Per-user threads — Alice's context does not leak to Bob | Shared team resource |
| Inbox | Private per-user for sensitive personal tasks | Editor-only: leads review before sensitive actions ship |
| Channels | Needs Slack/Teams user ID → LangSmith user mapping | Can drop into more surfaces — only needs the message |

See: [`src/identity_models/memory.py`](src/identity_models/memory.py)

---

## Repository layout

```
assistant-vs-claw/
├── src/identity_models/     # Core patterns (Assistant, Claw, credentials, memory)
├── examples/                # Three real agents + side-by-side Slack demo
├── demos/                   # Full comparison runner
├── tests/                   # Trust boundary assertions
└── docs/CHOOSING.md         # Decision guide
```

---

## The shift in one sentence

We used to ask: *Can we build an agent that does this task?*

Now we ask: **Whose identity should execute that task — the human in the loop, or the agent we provisioned for the job?**

That is the whole Claw vs. Assistant split. Not autonomy. Not model choice. **Authorization.**

- **Assistants** are agents that work for you, as you.
- **Claws** are agents that work as themselves, on behalf of the team.

Get that wrong and you either over-expose data or build something too weak to be useful. Get it right and the same prompt-to-agent workflow scales from a personal inbox to a governed fleet.

---

## Related

- [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) — govern populations of agents at scale
- [LangSmith Fleet](https://www.langchain.com/langsmith/fleet) — managed fleet primitives (identity, inbox, audit)
- [Loop Engineering](https://github.com/cobusgreyling/loop-engineering) — autonomous systems that keep running

## License

MIT — see [LICENSE](LICENSE).