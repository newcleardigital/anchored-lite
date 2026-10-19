#!/usr/bin/env bash
# PostToolUse hook entry point: hand the hook event (stdin) to the edit check.
exec python3 "$(dirname "${BASH_SOURCE[0]}")/guard.py"
