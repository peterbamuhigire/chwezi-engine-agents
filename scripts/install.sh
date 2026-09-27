#!/usr/bin/env sh
set -eu

host=codex
destination=
force=0
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
while [ "$#" -gt 0 ]; do
  case "$1" in
    --host) [ "$#" -ge 2 ] || { echo "--host requires a value" >&2; exit 2; }; host=$2; shift 2 ;;
    --destination) [ "$#" -ge 2 ] || { echo "--destination requires a value" >&2; exit 2; }; destination=$2; shift 2 ;;
    --force) force=1; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done
[ -n "$destination" ] || destination="$HOME/.local/share/skills-engine-agents"
python3 "$source_dir/scripts/resolve-install-target.py" --host "$host" --destination "$destination" --source "$source_dir" >/dev/null
destination=$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).expanduser().resolve())' "$destination")
paths=".codex-plugin agents catalog core schemas scripts skills adapters/$host README.md CONTRIBUTING.md docs/distribution.md"
if [ "$host" = mcp ]; then paths="$paths mcp-server/package.json mcp-server/package-lock.json mcp-server/tsconfig.json mcp-server/README.md mcp-server/.mcp.json.example mcp-server/src"; fi

# Check source links, installed ownership and collisions before staging.
set -- $paths
python3 - "$source_dir" "$destination" "$force" "$@" <<'PY'
import hashlib, json, sys
from pathlib import Path, PurePosixPath
source, dest, force = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3] == '1'
paths, owned = sys.argv[4:], set()
for raw in paths:
    item = source / raw
    if not item.exists() or item.is_symlink(): raise SystemExit(f"Unsafe or missing install source: {raw}")
    candidates = [item] if item.is_file() else list(item.rglob('*'))
    for file in candidates:
        if file.is_symlink(): raise SystemExit(f"Refusing linked install source: {file}")
        if file.is_file(): owned.add(file.relative_to(source).as_posix())
old, hashes = set(), {}
manifest_path = dest / '.skills-engine-agents-install.json'
if dest.exists():
    if not dest.is_dir(): raise SystemExit(f"Destination is not a directory: {dest}")
    for item in dest.rglob('*'):
        if item.is_symlink(): raise SystemExit(f"Refusing linked destination: {item}")
    if any(dest.iterdir()) and not manifest_path.is_file() and not force:
        raise SystemExit(f"Destination is non-empty and unmanaged; use --force after review: {dest}")
    if manifest_path.exists():
        try: record = json.loads(manifest_path.read_text(encoding='utf-8'))
        except Exception as exc: raise SystemExit(f"Refusing unreadable ownership manifest: {exc}")
        if not isinstance(record, dict) or not isinstance(record.get('installed_files'), list): raise SystemExit('Invalid ownership manifest')
        for rel in record['installed_files']:
            if not isinstance(rel, str) or Path(rel).is_absolute() or '..' in PurePosixPath(rel.replace('\\','/')).parts: raise SystemExit(f"Unsafe manifest path: {rel!r}")
            if rel != '.skills-engine-agents-install.json': old.add(rel)
        hashes = record.get('installed_hashes') or {}
        if old and not hashes and not force: raise SystemExit('Legacy manifest has no file hashes; use --force after review')
    for rel in sorted(owned):
        target = dest / PurePosixPath(rel)
        parent = target.parent
        while parent != dest.parent:
            if parent.exists() and not parent.is_dir(): raise SystemExit(f"Refusing file/directory collision: {parent}")
            parent = parent.parent
        if target.exists() and not target.is_file(): raise SystemExit(f"Refusing file/directory or special-file collision: {target}")
        if not target.exists(): continue
        if rel not in old:
            if not force: raise SystemExit(f"Refusing to overwrite unowned file: {rel}")
        elif rel not in hashes or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != str(hashes[rel]).lower():
            if not force: raise SystemExit(f"Refusing to overwrite locally modified or unverifiable file: {rel}")
PY

stage="${destination}.staging.$$"
backup="${destination}.backup.$$"
[ ! -e "$stage" ] && [ ! -L "$stage" ] || { echo "Staging path already exists: $stage" >&2; exit 1; }
[ ! -e "$backup" ] && [ ! -L "$backup" ] || { echo "Backup path already exists: $backup" >&2; exit 1; }
cleanup() {
  if [ -n "$backup" ] && [ -e "$backup" ] && [ ! -e "$destination" ]; then mv "$backup" "$destination"; fi
  [ ! -e "$stage" ] || rm -rf "$stage"
}
trap cleanup EXIT HUP INT TERM
mkdir -p "$stage"
if [ -d "$destination" ]; then cp -R "$destination"/. "$stage"/; fi
for relative in $paths; do
  from="$source_dir/$relative"; to="$stage/$relative"
  if [ -d "$from" ]; then mkdir -p "$to"; cp -R "$from"/. "$to"/
  else mkdir -p "$(dirname "$to")"; cp "$from" "$to"; fi
done

commit=$(git -C "$source_dir" rev-parse HEAD 2>/dev/null || true)
remote=$(git -C "$source_dir" remote get-url origin 2>/dev/null || true)
set -- $paths
python3 - "$source_dir" "$stage" "$destination" "$host" "$commit" "$remote" "$@" <<'PY'
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
source, stage, dest = map(Path, sys.argv[1:4])
host, commit, remote, *paths = sys.argv[4:]
owned = set()
for raw in paths:
    item = source / raw
    files = [item] if item.is_file() else [p for p in item.rglob('*') if p.is_file()]
    owned.update(file.relative_to(source).as_posix() for file in files)
hashes = {rel: hashlib.sha256((stage / rel).read_bytes()).hexdigest() for rel in sorted(owned)}
data = {'source_repository':remote,'source_commit':commit,'adapter_id':host,'adapter_version':'1.0.0','core_version':'1.0.0','destination':str(dest),'installed_files':sorted(owned)+['.skills-engine-agents-install.json'],'installed_hashes':hashes,'installed_at':datetime.now(timezone.utc).isoformat(),'installer_version':'1.0.0'}
(stage/'.skills-engine-agents-install.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
PY

if [ -e "$destination" ]; then mv "$destination" "$backup"; else backup=; fi
mkdir -p "$(dirname "$destination")"
if ! mv "$stage" "$destination"; then [ -z "$backup" ] || mv "$backup" "$destination"; exit 1; fi
if [ -n "$backup" ]; then rm -rf "$backup"; fi
trap - EXIT HUP INT TERM
echo "Installed skills-engine-agents host=$host to $destination"
