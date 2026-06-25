# Security Policy

This repository is an **educational illustration** of agent authorization patterns. It uses mock data only — no real OAuth tokens, API keys, or production credentials.

## Reporting a vulnerability

If you find a security issue in this repository (for example, accidental secret exposure in commits), please open a private report via [GitHub Security Advisories](https://github.com/cobusgreyling/assistant-vs-claw/security/advisories/new) or email the maintainer through their GitHub profile.

## Scope

- In scope: accidental credential leaks, unsafe defaults that could mislead production deployments
- Out of scope: theoretical attacks against the mock `notion_search` implementation

## Production guidance

Do not copy mock patterns directly into production without:

1. Real OAuth token storage with encryption at rest
2. Explicit principal scoping on every tool call
3. Audit logging aligned with your compliance requirements
4. Editor-only inbox review for sensitive Claw actions

See [Fleet Engineering failure modes](https://github.com/cobusgreyling/fleet-engineering/blob/main/docs/failure-modes.md) for incident-style guidance.