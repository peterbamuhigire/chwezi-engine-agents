#!/usr/bin/env bash
# scan-skills.sh <engine-root> — lists every SKILL.md under the engine with
# its name and description frontmatter, one per line, tab-separated.
# Deterministic collection step for rules-distill: exhaustive, no sampling.
set -euo pipefail

ROOT="${1:?Usage: scan-skills.sh <engine-root>}"

find "$ROOT" -name SKILL.md \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -not -path "*/_TEMPLATE/*" -not -path "*/__pycache__/*" 2>/dev/null | sort | while read -r f; do
  name=$(awk -F': *' '/^name:/{print $2; exit}' "$f" | tr -d '"')
  desc=$(awk -F': *' '/^description:/{sub(/^description: */,""); print; exit}' "$f")
  rel="${f#"$ROOT"/}"
  printf '%s\t%s\t%s\n' "$rel" "${name:-?}" "${desc:0:160}"
done
