# Privacy — Anchored Lite

Anchored Lite collects no data. This covers both editions: the Claude Code edition
(the `anchor-core` plugin) and the edition in Claude's plugin directory (the
`anchored-lite` plugin, folder `claude-directory/`).

- It makes no network calls and sends no telemetry, analytics or crash reports.
- It reads and writes only files inside the project you open it in: its settings
  (`anchor-core.json`), the handover note, decision files and the files it checks.
- The Claude Code edition runs only its own checks and the generator commands you
  list under `generated` in `anchor-core.json`. The directory edition runs no
  commands at all: it is instructions for Claude only.
- Nothing is stored outside your project, and newcleardigital receives nothing.

Like any Claude Code plugin, its skills (and, in the Claude Code edition, its hook output) become part of your Claude
session, which is governed by your agreement with Anthropic, not by this plugin.

Questions: office@newcleardigital.com · newcleardigital
