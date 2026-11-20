#!/usr/bin/env python3
"""Generated files match what generates them.

Each entry in `generated` names a file and the command that produces it. The
check runs the command and compares. A difference means someone edited the
output by hand, or changed the source and never regenerated. Either way the
number or table in that file can no longer be believed.

The file is left regenerated, so the fix is: review the diff and commit it.
"""
import hashlib, sys, _core as C


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "absent"


def main():
    cfg = C.load()
    entries = cfg["generated"]
    if not entries:
        return C.ok("no generated files declared — add them to generated in anchor-core.json")
    stale, broken = [], []
    for e in entries:
        f = cfg["root"] / e["file"]
        before = digest(f)
        r = C.run(e["command"], cfg["root"])
        if r.returncode != 0:
            broken.append(f"{e['file']}: `{e['command']}` exited {r.returncode}  ·  {(r.stdout + r.stderr).strip()[:120]}")
            continue
        if digest(f) != before:
            stale.append(e["file"])
    if broken:
        return C.fail("a generator could not run", broken)
    if stale:
        return C.fail("generated file differs from what its command produces", stale,
                      "It was edited by hand, or its source changed without regenerating.\n"
                      "It has just been regenerated: review the change and commit it.")
    return C.ok(f"{len(entries)} generated file(s) match their commands")


if __name__ == "__main__":
    sys.exit(C.guard(main)())
