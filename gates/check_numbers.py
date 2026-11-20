#!/usr/bin/env python3
"""Fixed numbers live in one place.

`watch_numbers` in anchor-core.json lists the numbers your product decides on
purpose: a free-shipping limit, a retry count, a VAT rate, a trial length. Each
may appear in the `constants` file and nowhere else in the logic. An AI agent
that types one of them straight into a comparison or a calculation creates a
second copy that nobody updates next time.

Only numbers used as thresholds are flagged: beside a comparison, or
multiplying or dividing. Tests may name the value they check.
"""
import sys, _core as C


def main():
    cfg = C.load()
    if not cfg["watch_numbers"]:
        return C.ok("no numbers to watch yet — add them to watch_numbers in anchor-core.json")
    if not cfg["constants"]:
        return C.fail("watch_numbers is set but constants is empty", ["anchor-core.json"],
                      "Name the one file or folder where these numbers are allowed to live.")
    bad = []
    for p in C.sources(cfg):
        rel = p.relative_to(cfg["root"])
        lines = p.read_text(errors="replace").splitlines()
        for line_no, n, how in C.number_hits(cfg, rel, lines):
            bad.append(f"{rel}:{line_no}  {n} {how}  ·  {lines[line_no - 1].strip()[:70]}")
    if bad:
        return C.fail(f"a fixed number written outside {cfg['constants']}", bad,
                      f"Read it from {cfg['constants']} instead. If this number is a coincidence,\n"
                      f"mark the line `{cfg['escape_marker']}: <why>`.")
    return C.ok(f"{len(cfg['watch_numbers'])} watched number(s) appear only in {cfg['constants']}")


if __name__ == "__main__":
    sys.exit(C.guard(main)())
