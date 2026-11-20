#!/usr/bin/env python3
"""Set up anchor-core in a project: anchor-core.json, a decisions folder with
its first decision, an empty handover log, and a CLAUDE.md section that tells
every session to read them first. Never overwrites an existing file.

    python3 init.py [--constants src/config.ts] [--watch 50 3] [--ban "customer=say Buyer"]
"""
import argparse, json, pathlib, datetime, sys

TODAY = datetime.date.today().isoformat()

FIRST_DECISION = f"""# 0001 — Write decisions down

- **Date:** {TODAY}
- **Decided by:** the team

## The question

How does a project built over many AI sessions stay consistent, when no session
remembers the one before?

## Decision

Every choice that later work depends on is written here, one file per decision,
before code relies on it. Every session reads this folder and HANDOVER.md before
it writes code. A decision that changes gets a new file that replaces the old one.

## Consequences

Sessions cannot quietly contradict each other. Writing a decision takes five
minutes; rediscovering one takes a day.
"""

HANDOVER = """# Handover

Newest first. Each session ends by adding what it did, what is unfinished, and
what the next session should do first.
"""

CLAUDE_SECTION = """
## anchor-core

Before writing code in a session, read in this order and never work from memory:
`anchor-core.json`, `HANDOVER.md` (newest entry), `docs/decisions/`, `git log --oneline -10`.

- Fixed numbers listed in `watch_numbers` live only in the `constants` file.
- Names never use a word listed in `banned_words`.
- Generated files are regenerated, never edited by hand.
- A choice later work depends on is recorded in `docs/decisions/` first.
- End the session with an entry in `HANDOVER.md`.
"""


def write_once(path, text):
    if path.exists():
        print(f"  kept   {path.name} (already there)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"  wrote  {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--constants", default="")
    ap.add_argument("--watch", nargs="*", default=[], type=float)
    ap.add_argument("--ban", nargs="*", default=[], help='word=why')
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    cfg = {
        "constants": a.constants,
        "watch_numbers": [int(x) if x.is_integer() else x for x in a.watch],
        "banned_words": dict(b.split("=", 1) for b in a.ban if "=" in b),
        "generated": [],
        "decisions": "docs/decisions",
        "handover": "HANDOVER.md",
        "ignore": [],
        "escape_marker": "core-allow",
    }
    print("Setting up anchor-core:")
    write_once(root / "anchor-core.json", json.dumps(cfg, indent=2) + "\n")
    write_once(root / "docs/decisions/0001-write-decisions-down.md", FIRST_DECISION)
    write_once(root / "HANDOVER.md", HANDOVER)
    claude = root / "CLAUDE.md"
    if claude.exists() and "## anchor-core" in claude.read_text():
        print("  kept   CLAUDE.md (already has the anchor-core section)")
    else:
        with claude.open("a") as f:
            f.write(CLAUDE_SECTION)
        print(f"  added  the anchor-core section to {claude.name}")
    print("\nNext: list your fixed numbers, banned words and generated files in anchor-core.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
