#!/usr/bin/env python3
"""Banned words in names.

When the team has agreed that a thing is called a Buyer, an AI agent that names
a variable `customerId` starts a second vocabulary. Found in month four, that is
a database migration. `banned_words` maps each word to the reason.
"""
import sys, _core as C


def main():
    cfg = C.load()
    if not cfg["banned_words"]:
        return C.ok("no banned words yet — add them to banned_words in anchor-core.json")
    bad = []
    files = C.sources(cfg)
    for p in files:
        rel = p.relative_to(cfg["root"])
        for line_no, name, w, why in C.word_hits(cfg, p.read_text(errors="replace").splitlines()):
            bad.append(f"{rel}:{line_no}  `{name}` contains `{w}` — {why}")
    if bad:
        return C.fail("banned word in a name", bad,
                      f"Rename it. If the word is unavoidable here, mark the line `{cfg['escape_marker']}: <why>`.")
    return C.ok(f"no banned word in {len(files)} source file(s)")


if __name__ == "__main__":
    sys.exit(C.guard(main)())
