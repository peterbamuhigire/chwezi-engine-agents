#!/usr/bin/env bash
# scan-rules.sh <engine-root> — lists every rules/**/*.md file with its
# section headings, so a candidate principle can be checked against what
# already exists before proposing it as new.
set -euo pipefail

ROOT="${1:?Usage: scan-rules.sh <engine-root>}"
RULES_DIR="$ROOT/rules"

if [ ! -d "$RULES_DIR" ]; then
  echo "No rules/ directory at $RULES_DIR — nothing to scan." >&2
  exit 0
fi

find "$RULES_DIR" -name "*.md" | sort | while read -r f; do
  rel="${f#"$ROOT"/}"
  echo "=== $rel ==="
  grep -E '^#{1,3} ' "$f" || true
  echo
done
