# Anchored Lite (anchor-core)

Keeps code written by an AI agent consistent from one session to the next.

An agent forgets everything between sessions. On a project that runs for weeks that
shows up as a fee typed into three places and updated in two, a word the team ruled
out coming back, a generated file edited by hand, or a decision from session 3
quietly reversed in session 12. Anchored Lite gives the agent a written record to
start from and checks every file it writes, the moment it writes it.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `start` | "start" | Reads the project's record (settings, latest handover, decisions, recent commits), says where things stand, sets the plugin up the first time |
| `checks` | "run the checks" | Runs the checks and explains any failure |
| `decide` | "record a decision" | Writes a decision file: what was chosen and why |
| `handover` | "hand over" | Writes the note the next session starts from |

## The check on every edit

A `PostToolUse` hook runs after each Edit or Write. If the file now contains a number
from `watch_numbers` outside the constants file, or a name using a banned word, the
agent is told on the spot and fixes it. The same checks run in CI with
`gates/run.sh`; `gates/selftest.sh` breaks each check on purpose and confirms it
catches the break (18 of 18).

## Settings: `anchor-core.json`

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

## Requirements and privacy

Python 3, standard library only. Everything runs on your machine. The plugin makes no
network calls and sends no telemetry; the only commands it runs are the generator
commands you list under `generated`. The hook and checks are Claude Code
features; on claude.ai and in Cowork only the skills apply.

## When your code has to follow someone else's rulebook

Payment rules, fees set by a regulator, pricing law, a contract: if you must show an
auditor that each rule became code, was tested and was approved by a named person,
see [Anchored](https://anchored.newcleardigital.com/?ref=lite-plugin).

MIT licence · office@newcleardigital.com
