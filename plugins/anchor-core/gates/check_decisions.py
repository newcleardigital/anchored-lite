#!/usr/bin/env python3
"""Every recorded decision is actually decided.

An AI agent working across many sessions only stays consistent if what was
decided is written down where the next session reads it. A decision file with a
heading and nothing under it is an intention, and the next session will decide
again, differently.

Each file in the decisions folder must have a `## Decision` section with real
text in it (not a template comment).
"""
import re, sys, _core as C


def body_of(text):
    m = re.search(r"^##\s*Decision\s*$(.*?)(?=^##\s|\Z)", text, flags=re.M | re.S | re.I)
    if not m:
        return None
    body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()
    return body


def main():
    cfg = C.load()
    d = cfg["root"] / cfg["decisions"]
    files = sorted(d.glob("*.md")) if d.is_dir() else []
    if not files:
        return C.ok(f"no decisions recorded yet in {cfg['decisions']}/")
    bad = []
    for f in files:
        body = body_of(f.read_text(errors="replace"))
        if body is None:
            bad.append(f"{f.relative_to(cfg['root'])}: no `## Decision` section")
        elif len(body) < 15:
            bad.append(f"{f.relative_to(cfg['root'])}: the Decision section is empty")
    if bad:
        return C.fail("a decision file without a decision", bad,
                      "Write what was chosen and why, in a few sentences, or delete the file.")
    return C.ok(f"{len(files)} decision(s) recorded, each with its reason")


if __name__ == "__main__":
    sys.exit(C.guard(main)())
