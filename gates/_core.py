#!/usr/bin/env python3
"""Shared configuration for the anchor-core checks.

Every check is driven by `anchor-core.json` at the project root. A project
without one is not using anchor-core: every check exits 0 and says so, because a
check that fires where nobody asked for it gets switched off.

Standard library only. A plugin does not install Python packages for you.
"""
import json, os, re, sys, fnmatch, pathlib, subprocess

CONFIG_NAME = "anchor-core.json"

PROFILES = {
    "typescript": dict(ext=[".ts", ".tsx", ".mts", ".cts"], line_comment="//",
                       ident=[r"\b(?:const|let|var|function|class|interface|type|enum)\s+(\w+)", r"(\w+)\s*:"],
                       skip=["dist", "build", "node_modules", "coverage"]),
    "javascript": dict(ext=[".js", ".jsx", ".mjs", ".cjs"], line_comment="//",
                       ident=[r"\b(?:const|let|var|function|class)\s+(\w+)", r"(\w+)\s*:"],
                       skip=["dist", "build", "node_modules", "coverage"]),
    "python": dict(ext=[".py"], line_comment="#",
                   ident=[r"\b(?:def|class)\s+(\w+)", r"^\s*(\w+)\s*[:=]"],
                   skip=["__pycache__", ".venv", "venv", "build", "dist"]),
    "kotlin": dict(ext=[".kt", ".kts"], line_comment="//",
                   ident=[r"\b(?:val|var|fun|class|object|interface|enum|typealias)\s+(\w+)"],
                   skip=["build", "out", ".gradle"]),
    "java": dict(ext=[".java"], line_comment="//",
                 ident=[r"\b(?:class|interface|enum|record|void|var)\s+(\w+)", r"\b[A-Z]\w*\s+(\w+)\s*[;=)]"],
                 skip=["build", "target", "out"]),
    "go": dict(ext=[".go"], line_comment="//",
               ident=[r"\b(?:func|type|var|const)\s+(\w+)", r"(\w+)\s*:="],
               skip=["vendor", "bin"]),
    "csharp": dict(ext=[".cs"], line_comment="//",
                   ident=[r"\b(?:class|interface|enum|record|struct|void|var)\s+(\w+)"],
                   skip=["bin", "obj"]),
    "rust": dict(ext=[".rs"], line_comment="//",
                 ident=[r"\b(?:fn|struct|enum|trait|type|let|const|static)\s+(?:mut\s+)?(\w+)"],
                 skip=["target"]),
    "ruby": dict(ext=[".rb"], line_comment="#",
                 ident=[r"\b(?:def|class|module)\s+(\w+)", r"(\w+)\s*="], skip=["vendor", "tmp"]),
    "php": dict(ext=[".php"], line_comment="//",
                ident=[r"\b(?:function|class|interface|trait)\s+(\w+)", r"\$(\w+)"], skip=["vendor"]),
}

DEFAULTS = {
    "languages": [],
    "source": ["."],
    "ignore": [],
    "constants": "",
    "watch_numbers": [],
    "banned_words": {},
    "generated": [],
    "decisions": "docs/decisions",
    "handover": "HANDOVER.md",
    "escape_marker": "core-allow",
}

NUM = r"(\d{1,6}(?:\.\d+)?)"


class NotCore(Exception):
    pass


def find_root(start=None):
    p = pathlib.Path(start or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
    for d in [p, *p.parents]:
        if (d / CONFIG_NAME).is_file():
            return d
    raise NotCore(f"no {CONFIG_NAME} at or above {p}")


def load(start=None):
    root = find_root(start)
    cfg = dict(DEFAULTS)
    cfg.update(json.loads((root / CONFIG_NAME).read_text()))
    cfg["root"] = root
    if not cfg["languages"]:
        cfg["languages"] = detect_languages(root)
    return cfg


def detect_languages(root):
    counts = {}
    for name, p in PROFILES.items():
        n = sum(1 for e in p["ext"] for x in root.rglob("*" + e) if "node_modules" not in x.parts)
        if n:
            counts[name] = n
    return [k for k, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:3]]


def profile(cfg):
    ps = [PROFILES[n] for n in cfg["languages"] if n in PROFILES] or list(PROFILES.values())
    merged = dict(ext=[], ident=[], skip=[], line_comment="//")
    for p in ps:
        for k in ("ext", "ident", "skip"):
            merged[k] += [x for x in p[k] if x not in merged[k]]
    if len(ps) == 1:
        merged["line_comment"] = ps[0]["line_comment"]
    return merged


def match_any(rel, patterns):
    s = str(rel)
    for pat in patterns:
        if fnmatch.fnmatch(s, pat) or fnmatch.fnmatch(s, pat.rstrip("/") + "/*"):
            return True
        if "/" not in pat and "*" not in pat and pat in rel.parts:
            return True
    return False


def in_constants(cfg, rel):
    c = cfg["constants"]
    if not c:
        return False
    return str(rel) == c or str(rel).startswith(c.rstrip("/") + "/") or c in rel.parts


def is_test(rel):
    parts = {x.lower() for x in rel.parts}
    stem = rel.stem.lower()
    return bool(parts & {"test", "tests", "__tests__", "spec", "specs", "fixtures"}) \
        or "test" in stem or "spec" in stem


def sources(cfg):
    """Source files, sorted so every machine reports the same order."""
    root, prof = cfg["root"], profile(cfg)
    skip = set(prof["skip"]) | {".git", "node_modules"}
    exts = set(prof["ext"])
    out = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in exts:
            continue
        rel = p.relative_to(root)
        if skip & set(rel.parts) or match_any(rel, cfg["ignore"]):
            continue
        if cfg["source"] != ["."] and not match_any(rel, cfg["source"]):
            continue
        out.append(p)
    return sorted(out)


def strip_code(line, comment="//"):
    """Drop comments and string literals, so a number in a message is not a finding."""
    if comment and comment in line:
        line = line.split(comment)[0]
    line = re.sub(r"/\*.*?\*/", "", line)
    return re.sub(r"`[^`]*`|\"[^\"]*\"|'[^']*'", '""', line)


def escaped(cfg, lines, i):
    m = cfg["escape_marker"]
    return m in lines[i] or (i >= 1 and m in lines[i - 1])


def number_patterns():
    return [(re.compile(rf"(?:[<>]=?|===|!==|==|!=)\s*{NUM}(?![\w.])"), "compared against"),
            (re.compile(rf"(?<![\w.]){NUM}\s*(?:[<>]=?|===|!==|==|!=)"), "compared against"),
            (re.compile(rf"\*\s*{NUM}(?![\w.])"), "used as a multiplier"),
            (re.compile(rf"(?<![\w.]){NUM}\s*\*(?!\*)"), "used as a multiplier"),
            (re.compile(rf"(?<![/*])/\s*{NUM}(?![\w.])"), "used as a divisor")]


def watched(cfg):
    return {float(x) for x in cfg["watch_numbers"]}


def number_hits(cfg, rel, lines):
    """Watched numbers used in logic, outside the constants file. Shared by the
    check and the edit hook so the two can never disagree."""
    if in_constants(cfg, rel) or is_test(rel):
        return []
    watch, comment, hits = watched(cfg), profile(cfg)["line_comment"], []
    if not watch:
        return hits
    for i, line in enumerate(lines):
        if escaped(cfg, lines, i):
            continue
        code = strip_code(line, comment)
        for rx, how in number_patterns():
            for m in rx.finditer(code):
                if float(m.group(1)) in watch:
                    hits.append((i + 1, m.group(1), how))
    return hits


def word_hits(cfg, lines):
    banned, hits = cfg["banned_words"], []
    if not banned:
        return hits
    prof = profile(cfg)
    idents = [re.compile(p) for p in prof["ident"]]
    for i, line in enumerate(lines):
        if escaped(cfg, lines, i):
            continue
        code = strip_code(line, prof["line_comment"])
        for rx in idents:
            for m in rx.finditer(code):
                name = next((g for g in m.groups() if g), "")
                low = re.sub(r"[\W\d_]+", "", name.lower())
                for w, why in banned.items():
                    if low and w.lower() in low:
                        hits.append((i + 1, name, w, why))
    return hits


def ok(msg):
    print(f"OK  {msg}")
    return 0


def fail(title, rows, hint=""):
    print(f"FAIL  {title} — {len(rows)}:")
    for r in rows:
        print(f"  {r}")
    if hint:
        print(f"\n{hint}")
    return 1


def guard(fn):
    def wrapped():
        try:
            return fn()
        except NotCore as e:
            print(f"skip  anchor-core is not set up here ({e})")
            return 0
    return wrapped


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=300)
