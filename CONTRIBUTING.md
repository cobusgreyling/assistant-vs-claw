# Contributing

Thanks for helping improve this educational repo.

## Development setup

```bash
git clone https://github.com/cobusgreyling/assistant-vs-claw.git
cd assistant-vs-claw
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Commands

```bash
make all        # lint + typecheck + test
make test       # pytest
make demo       # avc-compare
make lint       # ruff
make typecheck  # mypy
```

## What to contribute

- New scenarios that clarify Assistant vs Claw trust boundaries
- Tests that prove authorization invariants (preferred over prose-only changes)
- Docs that map patterns to [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering)

## Pull request checklist

- [ ] `make all` passes locally
- [ ] New behavior has pytest coverage
- [ ] Examples remain runnable without API keys
- [ ] README or `docs/` updated if user-facing behavior changes

## Code style

- Keep the core dependency-free (stdlib + pytest/ruff/mypy for dev only)
- Prefer small, readable modules over framework abstractions
- Match existing naming: Assistant = on-behalf-of, Claw = fixed identity