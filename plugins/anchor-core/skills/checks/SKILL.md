---
name: checks
description: "Run the anchor-core checks and explain any failure in plain words, or prove the checks can actually fail. Use when a check or CI goes red, before a commit, or when someone asks whether the checks are real."
allowed-tools: Bash(bash ${CLAUDE_PLUGIN_ROOT}/gates/run.sh), Bash(bash ${CLAUDE_PLUGIN_ROOT}/gates/selftest.sh)
---

# Run the checks

    bash ${CLAUDE_PLUGIN_ROOT}/gates/run.sh

| Check | Fails when |
|---|---|
| generated files in sync | a generated file differs from what its command produces |
| fixed numbers in one place | a number listed in `watch_numbers` is used in logic outside the constants file |
| agreed vocabulary | a name contains a word listed in `banned_words` |
| decisions written down | a file in the decisions folder has no real Decision text |

When one fails, say which file and line, why it matters in one sentence, and fix
it. Never silence a check to get past it; the escape marker is for a number or
word that genuinely has nothing to do with the rule, and each use needs a reason
on the line.

## Prove the checks are real

    bash ${CLAUDE_PLUGIN_ROOT}/gates/selftest.sh

It builds a throwaway project, confirms every check is green, then breaks one
thing at a time and confirms the matching check turns red. Run it in CI too: a
check that silently stops working looks exactly like a clean build.
