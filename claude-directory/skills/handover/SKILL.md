---
name: handover
description: "End a working session by writing what was done, what is unfinished and what the next session should do first into HANDOVER.md, so the next session starts from the record instead of from memory. Use when work stops, when someone says they're done for today, or before a long break."
allowed-tools: Read, Grep, Glob, LS
---

# Hand over

Review this session's changes with the `checks` skill first and report the
result honestly.

Then add one entry at the top of `HANDOVER.md`, under the title, newest first:

```
## <YYYY-MM-DD> — <one line: what this session was about>

**Done:** what changed, with file names. Only what was actually finished.
**Not done:** what was started and left open, and why.
**Review:** clean, or which rule is broken where and why.
**Next session starts with:** the one concrete first step.
**Decisions made:** links to new files in docs/decisions/, or "none".
```

Rules:

- Write facts the next session can check, not impressions. "Added retry to
  `sync.ts`, test in `sync.test.ts`" beats "improved sync".
- Never mark something done that the review shows as broken.
- A choice made during the session that later work depends on belongs in
  `docs/decisions/` too (the `decide` skill); the handover only links to it.
