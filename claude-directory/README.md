# Anchored Lite

Keeps code written by an AI agent consistent from one session to the next.

An agent forgets everything between sessions. On a project that runs for weeks that
shows up as a fee typed into three places and updated in two, a word the team ruled
out coming back, a generated file edited by hand, or a decision from session 3
quietly reversed in session 12. Anchored Lite gives every session a written record
to start from, and has every session leave that record up to date for the next.

## Install

From the Claude plugin directory, or in Claude Code:

```
/plugin install anchored-lite --marketplace newcleardigital/anchored-lite
```

## Skills

| Skill | Say | What it does |
|---|---|---|
| `start` | "start" | Reads the project's record (settings, latest handover, decisions, recent commits) and says where things stand. The first time, sets the record up and asks three questions |
| `decide` | "record a decision" | Writes a decision file: what was chosen and why |
| `checks` | "review the rules" | Reviews the changed files against the project's own rules and explains each problem |
| `handover` | "hand over" | Writes the note the next session starts from |

Say **"start"** in your project. The first time, Claude creates `anchor-core.json`,
`HANDOVER.md`, `docs/decisions/` and a short section in `CLAUDE.md`, then asks which
numbers your product fixes on purpose, which words to avoid, and which files are
generated. At the end of a session, say **"hand over"**.

## What the project record looks like

`anchor-core.json`:

```json
{
  "constants": "fees/limits.py",
  "watch_numbers": [1.5, 0.25, 5000],
  "banned_words": { "customer": "say cardholder, the team agreed on it" },
  "generated": [{ "file": "docs/LIMITS.md", "command": "python3 tools/gen_limits.py" }],
  "decisions": "docs/decisions",
  "handover": "HANDOVER.md"
}
```

Everything is plain files in your project, readable by people and by any AI tool.

## This edition and the Claude Code edition

This edition is instructions for Claude only: no hooks, no scripts, nothing that runs
on its own. Its `checks` skill is a careful review when you ask for one, not a
guarantee.

The Claude Code edition at
[github.com/newcleardigital/anchored-lite](https://github.com/newcleardigital/anchored-lite)
uses the same files and adds checks that run automatically after every edit and in CI,
with a self-test that proves each check can fail. A project set up with one edition
works with the other. Install one or the other, not both.

## Privacy

Collects no data, makes no network calls, runs no commands. Claude reads and writes
only the files named above, inside your project. See
[PRIVACY.md](https://github.com/newcleardigital/anchored-lite/blob/main/PRIVACY.md).

## When your code has to follow someone else's rulebook

Payment rules, fees set by a regulator, pricing law, a contract: if you must show an
auditor that each rule became code, was tested and was approved by a named person,
see [Anchored](https://anchored.newcleardigital.com/?ref=lite-directory).

MIT licence · office@newcleardigital.com
