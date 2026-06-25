# Essay Hook — "Whose Keys Are in the Lock?"

Use this outline for a Substack or Medium post that drives readers to the repo.

## Working title

**Whose Keys Are in the Lock? Why Assistant vs Claw Is the Agent Decision That Actually Matters**

## One-line thesis

Building agents is easy now; **authorization** is the bottleneck — and LangSmith Fleet's Assistant vs Claw split is the first design choice that determines whether you leak data or ship something useful.

## Suggested structure

1. **The bottleneck moved** — from "can the LLM call a tool?" to "whose identity calls it?"
2. **Two stories** — Alice/Bob onboarding (Assistant) vs `@product-bot` in `#general` (Claw)
3. **The common mistake** — Claw wired with personal OAuth (include `avc-slack` output)
4. **Beyond credentials** — memory, inbox, audit (link to Fleet Engineering patterns)
5. **CTA** — clone [assistant-vs-claw](https://github.com/cobusgreyling/assistant-vs-claw), run `avc-compare`, read [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering)

## Pull quotes

> Same word — *agent*. Two completely different trust boundaries.

> Not autonomy. Not model choice. **Authorization.**

## Links to include

- Repo: https://github.com/cobusgreyling/assistant-vs-claw
- Interactive docs: https://cobusgreyling.github.io/assistant-vs-claw/
- Colab: https://colab.research.google.com/github/cobusgreyling/assistant-vs-claw/blob/main/notebooks/assistant_vs_claw.ipynb
- Substack (Fleet Engineering): https://cobusgreyling.substack.com/