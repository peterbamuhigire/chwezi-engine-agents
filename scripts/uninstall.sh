#!/usr/bin/env sh
set -eu
[ "$1" = --destination ] || { echo 'Usage: uninstall.sh --destination PATH --force' >&2; exit 2; }
destination=$2
[ "${3:-}" = --force ] || { echo 'Uninstall requires --force.' >&2; exit 2; }
manifest="$destination/.skills-engine-agents-install.json"
[ -f "$manifest" ] || { echo "Managed install manifest not found: $manifest" >&2; exit 1; }
python3 - "$manifest" <<'PY'
import json, pathlib, sys
manifest = pathlib.Path(sys.argv[1]).resolve()
root = manifest.parent
data = json.loads(manifest.read_text(encoding='utf-8'))
for relative in data.get('installed_files', []):
    target = (root / relative).resolve()
    if root not in target.parents and target != root:
        raise SystemExit(f'Manifest path escapes destination: {relative}')
    if target.is_file():
        target.unlink()
PY
echo "Removed managed files from $destination; user-created files were retained."
