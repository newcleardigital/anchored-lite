#!/usr/bin/env bash
# Two-minute demo: a small card-fees project, an AI-style edit that breaks its rules,
# and the checks catching it. Needs only bash and Python 3. Changes nothing outside /tmp.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATES="$HERE/plugins/anchor-core/gates"
WORK="$(mktemp -d)/card-fees"
cp -R "$HERE/examples/card-fees" "$WORK"
cd "$WORK"
b() { printf '\n\033[1m%s\033[0m\n' "$1"; }

b "1. A small card-fees project. Its fixed numbers live in fees/limits.py:"
grep -E "^[A-Z_]+ =" fees/limits.py
b "2. All checks are green:"
bash "$GATES/run.sh" | tail -1

b "3. Now an AI agent 'improves' the code. It types the fee straight in and names a variable customer_id:"
cat >> fees/charge.py <<'PY'


def fx_fee_quick(amount_eur: float) -> float:
    customer_id = "unknown"
    return amount_eur * 1.5 / 100
PY
tail -4 fees/charge.py

b "4. What the agent sees in Claude Code, the moment it saves the file:"
printf '{"tool_input":{"file_path":"%s"}}' "$WORK/fees/charge.py" | python3 "$GATES/guard.py"
echo "(exit code $? = the edit is sent back to the agent to fix)"

b "5. The same rules in your build:"
bash "$GATES/run.sh" | grep -E "FAIL|✗|·|CHECKS" | head -8

b "6. The checks prove they can fail:"
bash "$GATES/selftest.sh" | tail -1
echo
echo "Next: install it in Claude Code (see README) or add run.sh to your CI."
