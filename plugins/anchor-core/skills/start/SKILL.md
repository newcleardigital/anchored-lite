---
name: start
description: "Begin every working session here. Reads the project's own record (settings, latest handover, decisions, recent commits) so this session cannot contradict an earlier one, says where things stand, then gets on with the work. Use at the start of a session, when someone asks what's next, or to set anchor-core up in a project."
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/gates/*), Bash(bash ${CLAUDE_PLUGIN_ROOT}/gates/*)
---

# Start a session

An AI session remembers nothing of the last one. The project's files do. Read
them first, every time, even when the topic feels familiar.

## If anchor-core.json does not exist

Offer to set it up in one sentence, and on a yes run:

    python3 ${CLAUDE_PLUGIN_ROOT}/gates/init.py

Then ask three plain questions and write the answers into `anchor-core.json`:

1. Which numbers does the product decide on purpose (prices, limits, rates,
   retry counts)? → `watch_numbers`, and the one file they live in → `constants`.
2. Which words has the team agreed not to use for a thing, and what to say
   instead? → `banned_words`.
3. Which files are produced by a command and must never be edited by hand?
   → `generated`, each with its command.

## Every session, in this order

1. `anchor-core.json`
2. `HANDOVER.md` — the newest entry only
3. `docs/decisions/` — every file's Decision section
4. `git log --oneline -10` and any failing check:

       bash ${CLAUDE_PLUGIN_ROOT}/gates/run.sh

Then say, in two plain sentences, what the last session finished and what is
next. If a decision the work depends on is missing, say so and record it with
the `decide` skill before writing code.

## While working

- A number listed in `watch_numbers` is read from the constants file, never typed.
- No name uses a banned word.
- Generated files are regenerated, never edited.
- When a check goes red twice on the same work, stop and report. A third try is
  where code stops being fixed and the check starts being argued with.

End the session with the `handover` skill.
