#!/usr/bin/env python3
"""Edit hook: check the file the agent just wrote, before anyone commits it.

Exits 0 wherever it does not apply: no anchor-core.json, a file type with no
profile, an ignored path. Exit 2 hands the message back to the agent as feedback
on the edit it just made.
"""
import json, sys, pathlib, _core as C


def main():
    try:
        ev = json.load(sys.stdin)
    except Exception:
        return 0
    path = (ev.get("tool_input") or {}).get("file_path")
    if not path:
        return 0
    f = pathlib.Path(path)
    if not f.is_file():
        return 0
    try:
        cfg = C.load(f.parent)
    except C.NotCore:
        return 0
    try:
        rel = f.resolve().relative_to(cfg["root"])
    except ValueError:
        return 0
    if f.suffix not in C.profile(cfg)["ext"] or C.match_any(rel, cfg["ignore"]):
        return 0
    lines = f.read_text(errors="replace").splitlines()
    hits = [f"line {n}: {num} is a fixed number — read it from `{cfg['constants']}`"
            for n, num, _ in C.number_hits(cfg, rel, lines)]
    hits += [f"line {n}: `{name}` contains the banned word `{w}` — {why}"
             for n, name, w, why in C.word_hits(cfg, lines)]
    if not hits:
        return 0
    print(f"Anchored Lite: {rel} breaks the project's own rules:\n  " + "\n  ".join(sorted(set(hits))[:12])
          + f"\n\nFix it now, or mark a deliberate use `{cfg['escape_marker']}: <why>`.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
