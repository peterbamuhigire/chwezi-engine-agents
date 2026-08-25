#!/usr/bin/env sh
set -eu
[ "$1" = --destination ] || { echo 'Usage: update.sh --destination PATH [--force]' >&2; exit 2; }
destination=$2
shift 2
force=
[ "${1:-}" = --force ] && force=--force
manifest="$destination/.skills-engine-agents-install.json"
[ -f "$manifest" ] || { echo "Managed install manifest not found: $manifest" >&2; exit 1; }
host=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["adapter_id"])' "$manifest")
"$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/install.sh" --host "$host" --destination "$destination" --force ${force:-}
