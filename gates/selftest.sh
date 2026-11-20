#!/usr/bin/env bash
# Prove the checks can fail. Builds a throwaway project, confirms every check is
# green, then breaks one thing at a time and confirms the matching check turns
# red. A check nobody has watched fail is decoration.
set -uo pipefail

GATES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT
pass=0 bad=0

say()  { printf '\n\033[1m%s\033[0m\n' "$1"; }
good() { printf '  \033[32m✓\033[0m %s\n' "$1"; pass=$((pass+1)); }
err()  { printf '  \033[31m✗\033[0m %s\n' "$1"; bad=$((bad+1)); }

# expect <exit> <label> <check> — no pipe, so the exit status is the check's own
expect() {
  ( cd "$FIX" && CLAUDE_PROJECT_DIR="$FIX" python3 "$GATES/$3" ) >"$FIX/.out" 2>&1
  local got=$?
  if [ "$got" -eq "$1" ]; then good "$2"; else err "$2 — wanted exit $1, got $got"; sed 's/^/      /' "$FIX/.out" | head -5; fi
}

fixture() {
  rm -rf "$FIX"/* "$FIX"/.[!.]* 2>/dev/null
  mkdir -p "$FIX/src" "$FIX/docs/decisions" "$FIX/tools"
  cat > "$FIX/anchor-core.json" <<'JSON'
{
  "languages": ["typescript"],
  "constants": "src/config.ts",
  "watch_numbers": [50, 3, 0.19],
  "banned_words": { "customer": "say Buyer — the team agreed on it" },
  "generated": [ { "file": "docs/LIMITS.md", "command": "python3 tools/gen.py" } ],
  "decisions": "docs/decisions",
  "escape_marker": "core-allow"
}
JSON
  cat > "$FIX/src/config.ts" <<'TS'
export const FREE_SHIPPING_FROM = 50;
export const MAX_RETRIES = 3;
export const VAT = 0.19;
TS
  cat > "$FIX/src/cart.ts" <<'TS'
import { FREE_SHIPPING_FROM, VAT } from "./config";
export const shipping = (total: number) => (total >= FREE_SHIPPING_FROM ? 0 : 4.9);
export const gross = (net: number) => net * (1 + VAT);
TS
  cat > "$FIX/src/cart.test.ts" <<'TS'
it("ships free from 50", () => expect(shipping(50)).toBe(0));
TS
  cat > "$FIX/tools/gen.py" <<'PY'
import re, pathlib
src = pathlib.Path("src/config.ts").read_text()
rows = re.findall(r"export const (\w+) = ([\d.]+);", src)
pathlib.Path("docs/LIMITS.md").write_text("# Limits\n\n" + "".join(f"- {k}: {v}\n" for k, v in rows))
PY
  ( cd "$FIX" && python3 tools/gen.py )
  cat > "$FIX/docs/decisions/0001-money.md" <<'MD'
# 0001 — Money

## Decision

Amounts are whole cents in the database; display divides once.
MD
}

say "1 · a clean project: every check green"
fixture
expect 0 "generated files in sync"     check_generated.py
expect 0 "fixed numbers in one place"  check_numbers.py
expect 0 "agreed vocabulary"           check_words.py
expect 0 "decisions written down"      check_decisions.py
( cd "$FIX" && CLAUDE_PROJECT_DIR="$FIX" bash "$GATES/run.sh" ) >/dev/null 2>&1 && good "run.sh passes" || err "run.sh failed on a clean project"

say "2 · each check must turn red on its own break"
fixture; echo 'export const free = (t: number) => t >= 50;' >> "$FIX/src/cart.ts"
expect 1 "numbers catches a fixed number compared inline"   check_numbers.py
fixture; echo 'export const g = (n: number) => n * 0.19;' >> "$FIX/src/cart.ts"
expect 1 "numbers catches a decimal used as a multiplier"   check_numbers.py
fixture; echo 'const customerId = "x";' >> "$FIX/src/cart.ts"
expect 1 "vocabulary catches a banned word in a name"       check_words.py
fixture; echo '- EXTRA: 99' >> "$FIX/docs/LIMITS.md"
expect 1 "generated catches a hand-edited file"             check_generated.py
fixture; printf '# 0002 — Auth\n\n## Decision\n\n<!-- todo -->\n' > "$FIX/docs/decisions/0002-auth.md"
expect 1 "decisions catches an empty decision"              check_decisions.py
fixture; echo 'export const free = (t: number) => t >= 50;' >> "$FIX/src/cart.ts"
( cd "$FIX" && CLAUDE_PROJECT_DIR="$FIX" bash "$GATES/run.sh" ) >/dev/null 2>&1 && err "run.sh passed a broken project" || good "run.sh fails when one check fails"

say "3 · and stays quiet where it should"
fixture; echo 'export const retries = (n: number) => n < 3; // core-allow: unrelated 3' >> "$FIX/src/cart.ts"
expect 0 "the escape marker is honoured"                    check_numbers.py
fixture; echo 'it("caps at 3", () => expect(MAX_RETRIES >= 3).toBe(true));' >> "$FIX/src/cart.test.ts"
expect 0 "a test may name the value it checks"              check_numbers.py
fixture; rm "$FIX/anchor-core.json"
expect 0 "a project without anchor-core.json is left alone" check_numbers.py

say "4 · the edit hook"
hook() { echo "{\"tool_input\":{\"file_path\":\"$1\"}}" | python3 "$GATES/guard.py" >/dev/null 2>&1; echo $?; }
fixture; echo 'export const free = (t: number) => t >= 50;' >> "$FIX/src/cart.ts"
[ "$(hook "$FIX/src/cart.ts")" = 2 ] && good "the hook stops an edit with a fixed number" || err "the hook let a fixed number through"
fixture
[ "$(hook "$FIX/src/cart.ts")" = 0 ] && good "the hook lets a clean edit through" || err "the hook blocked a clean edit"
[ "$(hook "$FIX/src/config.ts")" = 0 ] && good "the hook allows numbers in the constants file" || err "the hook blocked the constants file"
O="$(mktemp -d)"; echo 'const customer = 50 > 3;' > "$O/x.ts"
[ "$(hook "$O/x.ts")" = 0 ] && good "the hook ignores projects without anchor-core" || err "the hook fired outside anchor-core"; rm -rf "$O"

echo
total=$((pass + bad))
if [ $bad -eq 0 ]; then
  printf '\033[32m%d/%d checks passed — the checks can fail.\033[0m\n' "$pass" "$total"
else
  printf '\033[31m%d of %d checks failed — do not trust these checks.\033[0m\n' "$bad" "$total"
  exit 1
fi
