#!/usr/bin/env sh
set -eu

host=codex
destination=
force=0
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
while [ "$#" -gt 0 ]; do
  case "$1" in
    --host) host=$2; shift 2 ;;
    --destination) destination=$2; shift 2 ;;
    --force) force=1; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done
[ -n "$destination" ] || destination="$HOME/.local/share/skills-engine-agents"
python3 "$source_dir/scripts/resolve-install-target.py" --host "$host" --destination "$destination" --source "$source_dir" >/dev/null
destination=$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).expanduser().resolve())' "$destination")
manifest="$destination/.skills-engine-agents-install.json"
if [ -e "$destination" ] && [ "$(find "$destination" -mindepth 1 -maxdepth 1 -print -quit)" ] && [ ! -f "$manifest" ] && [ "$force" -ne 1 ]; then
  echo "Destination is non-empty and unmanaged; use --force after review: $destination" >&2
  exit 1
fi
stage="${destination}.staging.$$"
mkdir -p "$stage"
cleanup() { rm -rf "$stage"; }
trap cleanup EXIT HUP INT TERM
paths=".codex-plugin agents catalog core schemas scripts skills adapters/$host README.md CONTRIBUTING.md docs/distribution.md"
for relative in $paths; do
  mkdir -p "$stage/$(dirname "$relative")"
  cp -R "$source_dir/$relative" "$stage/$relative"
done
if [ "$host" = mcp ]; then
  mkdir -p "$stage/mcp-server"
  cp "$source_dir/mcp-server/package.json" "$source_dir/mcp-server/package-lock.json" "$source_dir/mcp-server/tsconfig.json" "$source_dir/mcp-server/README.md" "$source_dir/mcp-server/.mcp.json.example" "$stage/mcp-server/"
  cp -R "$source_dir/mcp-server/src" "$stage/mcp-server/src"
fi
commit=$(git -C "$source_dir" rev-parse HEAD 2>/dev/null || true)
remote=$(git -C "$source_dir" remote get-url origin 2>/dev/null || true)
python3 - "$stage/.skills-engine-agents-install.json" "$host" "$destination" "$commit" "$remote" <<'PY'
import json, sys
from datetime import datetime, timezone
from pathlib import Path
manifest, host, destination, commit, remote = sys.argv[1:]
root = Path(manifest).parent
files = sorted(str(p.relative_to(root)).replace('\\', '/') for p in root.rglob('*') if p.is_file())
data = {'source_repository': remote, 'source_commit': commit, 'adapter_id': host, 'adapter_version': '1.0.0', 'core_version': '1.0.0', 'destination': destination, 'installed_files': files + ['.skills-engine-agents-install.json'], 'installed_at': datetime.now(timezone.utc).isoformat(), 'installer_version': '1.0.0'}
Path(manifest).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
PY
if [ -e "$destination" ]; then backup="${destination}.backup.$$"; mv "$destination" "$backup"; else backup=; fi
mkdir -p "$(dirname "$destination")"
if ! mv "$stage" "$destination"; then [ -n "$backup" ] && mv "$backup" "$destination"; exit 1; fi
[ -n "$backup" ] && rm -rf "$backup" || true
trap - EXIT HUP INT TERM
echo "Installed skills-engine-agents host=$host to $destination"
