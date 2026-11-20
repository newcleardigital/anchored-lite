#!/usr/bin/env bash
# The anchor-core checks. The same checks locally, in the editor and in CI.
set -uo pipefail

GATES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$ROOT" 2>/dev/null || { echo "cannot enter $ROOT"; exit 1; }

if [ ! -f "$ROOT/anchor-core.json" ]; then
  echo "anchor-core is not set up here — no anchor-core.json at $ROOT."
  echo "Set it up:  python3 \"$GATES/init.py\""
  exit 0
fi

fail=0 n=0 total=4
run() {
  n=$((n + 1))
  printf '\n\033[1m▸ %d/%d  %s\033[0m\n' "$n" "$total" "$1"
  shift
  # Never pipe a check's output: in a pipeline $? is the last command's status,
  # which is exactly how a broken check comes to report success.
  python3 "$@"
  local st=$?
  if [ $st -ne 0 ]; then
    fail=1
    printf '\033[31m  ✗ check failed (exit %d)\033[0m\n' "$st"
  fi
}

run "generated files in sync"   "$GATES/check_generated.py"
run "fixed numbers in one place" "$GATES/check_numbers.py"
run "agreed vocabulary"         "$GATES/check_words.py"
run "decisions written down"    "$GATES/check_decisions.py"

echo
if [ $fail -ne 0 ]; then
  printf '\033[31mCHECKS FAILED\033[0m\n'
  exit 1
fi
printf '\033[32mALL CHECKS GREEN\033[0m\n'
