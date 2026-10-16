"""Writes docs/LIMITS.md from fees/limits.py. Never edit the output by hand."""
import pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from fees import limits

rows = [(n, getattr(limits, n)) for n in dir(limits) if n.isupper()]
out = ["# Limits", "", "Generated from `fees/limits.py`. Do not edit.", "", "| Setting | Value |", "| --- | --- |"]
out += [f"| `{n}` | {v} |" for n, v in rows]
(root / "docs" / "LIMITS.md").write_text("\n".join(out) + "\n")
