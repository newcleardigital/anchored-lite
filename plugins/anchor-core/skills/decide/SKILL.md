---
name: decide
description: "Record a decision that later work depends on (how money is stored, how users are identified, which library handles dates) as a file in docs/decisions, so no later session decides it again differently. Use when a choice comes up that other code will rely on, or when someone says 'let's go with…'."
---

# Record a decision

A decision is worth a file when later code will depend on it and getting it
wrong would mean rewriting that code. Naming, formatting and one-off choices are
not decisions.

1. Look in `docs/decisions/` first. If the question is already decided, follow
   that file. If it should change, write a new file that says which one it
   replaces.
2. Never record a decision the person has not made. Lay out the options in plain
   words, recommend one, and wait for their answer.
3. Write `docs/decisions/NNNN-short-name.md` with the next free number:

```
# NNNN — <the question in a few words>

- **Date:** YYYY-MM-DD
- **Decided by:** <name>

## The question

<one or two sentences>

## Decision

<what was chosen and why, in a few sentences>

## Consequences

<what this makes easy, and what it makes expensive>
```

4. Run the decisions check:

       python3 ${CLAUDE_PLUGIN_ROOT}/gates/check_decisions.py
