# Anchored Lite

**Keeps code written by an AI agent consistent from one session to the next.**

A free plugin for Claude Code, plus plain Python checks you can run anywhere. MIT licence.

## Try it in two minutes

No install, no account. Needs bash and Python 3:

```bash
git clone https://github.com/newcleardigital/anchored-lite
cd anchored-lite
bash try.sh
```

It copies a small card-fees project to a temporary folder, lets an "AI agent" type
the 1.5% fee straight into the code and name a variable `customer_id` when the team
says *cardholder*, and shows what the agent is told the moment it saves the file:

```
Anchored Lite: fees/charge.py breaks the project's own rules:
  line 15: `customer_id` contains the banned word `customer` — say cardholder, the team agreed on it
  line 16: 1.5 is a fixed number — read it from `fees/limits.py`
```

## The problem it solves

An AI agent forgets everything between sessions. On a project that runs for weeks,
that shows up as:

- a fee or limit typed into three places, and only two of them updated next time
- the team says *cardholder*, the agent writes `customerId`
- a generated document edited by hand, so its numbers stop being true
- something decided in session 3 quietly decided differently in session 12

Anchored Lite gives the agent a written record to start from and checks every file it
writes, the moment it writes it.

## What it does

| | |
|---|---|
| **Starts every session from the record** | Reads your settings, the latest handover note, your recorded decisions and recent commits before writing code. |
| **Checks every edit as it happens** | A number that belongs in your settings file, typed straight into the code, or a name using a word your team ruled out, is sent back to the agent on the spot. |
| **Catches hand-edited generated files** | Runs the command that makes each generated file and fails if the file differs. |
| **Keeps decisions written down** | Every decision file must say what was chosen and why. |
| **Proves its own checks work** | The self-test breaks each check on purpose and confirms it catches the break: 18 of 18. |

## Install in Claude Code

```bash
claude plugin marketplace add newcleardigital/anchored-lite
claude plugin install anchor-core@anchored-lite
```

Open Claude in your project and say **"start"**. The first time, it sets itself up and
asks three questions: which numbers your product fixes on purpose, which words to
avoid, and which files are generated. At the end of a session, say **"hand over"**.

## Use the checks without Claude

Plain Python 3, no packages:

```bash
python3 anchored-lite/plugins/anchor-core/gates/init.py      # in your project
bash anchored-lite/plugins/anchor-core/gates/run.sh          # run the checks
bash anchored-lite/plugins/anchor-core/gates/selftest.sh     # prove they can fail
```

Add `run.sh` and `selftest.sh` to CI. A check that silently stops working looks exactly
like a clean build.

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

Works with TypeScript, JavaScript, Python, Java, Kotlin, C#, Go, Rust, Ruby and PHP.

## When your code has to follow a rulebook

If your code must match rules someone else wrote (payment rules, pricing law, a
contract) and you have to show an auditor that each rule became code, was tested and
was approved by a named person, see **[Anchored](https://anchored.newcleardigital.com/?ref=lite)**.
It adds one requirement per rule, approval by a named person, a test for every rule and
a traceability export.

Questions: office@newcleardigital.com
