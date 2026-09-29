#!/usr/bin/env python3
"""Check (and, in a closed scope, render) the host files of the Chwezi portfolio.

``--check`` is read-only. For each public repository it applies:

(a) bridge      - ``CLAUDE.md`` follows the portfolio bridge contract
                  (docs/operations/claude-bridge-contract.md) and equals the file
                  rendered from ``engine-manifest.yaml`` ``claude_only_block``;
(b) invariants  - canary phrases (containment, not equality) appear in
                  ``AGENTS.md`` and any other named file;
(c) versions    - ``engine-manifest.yaml`` ``version`` agrees with
                  ``.claude-plugin/plugin.json``, ``.claude-plugin/marketplace.json``,
                  ``.codex-plugin/plugin.json`` (if present), the suite marketplace
                  entry and, with ``--tag``, the release tag;
(d) model IDs   - no ``Codex-sonnet|opus|haiku`` corruption in Markdown;
(e) BOM         - no UTF-8 byte-order mark in SKILL.md, AGENTS.md, CLAUDE.md,
                  hooks.json or hook scripts;
(f) hooks       - no single-quoted ``${CLAUDE_PLUGIN_ROOT}``, no bare .sh/.ps1
                  command without an interpreter, no heredoc, and every
                  referenced hook file exists;
(g) register    - every row of ``catalog/shared-assets.yaml`` (byte, block and
                  registered-variant modes);
(h) plugin      - every SKILL.md is listed in ``plugin.json`` or excluded in
                  ``engine-manifest.yaml`` ``plugin_exclusions`` with a reason;
(i) marketplace - the leading "N skills" count in marketplace descriptions
                  equals ``plugin.json`` ``skills[]`` length.

Exit codes: 0 clean, 1 findings (or bad input), 3 NOT_ASSESSED only (a sibling
repository is missing). A missing sibling is never a pass.

``--render --engine <path>`` writes only: ``CLAUDE.md`` (bridge plus the
manifest's ``claude_only_block``), the ``version`` fields of ``plugin.json``,
``marketplace.json`` and ``.codex-plugin/plugin.json``, and the leading count
of the engine marketplace description. It never writes ``AGENTS.md``, skills or
``plugin.json`` ``skills[]`` (those stay with ``generate-plugin-manifest.js``).
It refuses malformed YAML and writes nothing in that case.

Canary-invariant and version-consistency checks adapted from
DietrichGebert/ponytail (MIT, https://github.com/DietrichGebert/ponytail,
commit e3ba2aa); Windows hook failure modes adapted from obra/superpowers
release notes (MIT, https://github.com/obra/superpowers, commit 8ca22db).
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
COORDINATION = "chwezi-engine-agents"
BRIDGE = "# Claude Code repository memory\n\n@AGENTS.md\n"
CLAUDE_ONLY_HEADING = "## Claude-only notes"
CLAUDE_ONLY_MAX_LINES = 25
BOM = b"\xef\xbb\xbf"
MODEL_ID_RE = re.compile(r"\bCodex-(sonnet|opus|haiku)\b")
COUNT_RE = re.compile(r"^(\d+)(\s+skills\b)")
DEFAULT_INVARIANTS = ("british-english", "book-extraction-ban", "not-assessed")
ENGINE_INVARIANTS = {
    "chwezi-sdlc-documentation": ("iso-29148",),
    "chwezi-design-engine": ("banned-font-primary",),
}
TRIGGER_MARKER = "<!-- chwezi-design-engine:trigger v4 -->"
INTERPRETERS = {"node", "bash", "sh", "pwsh", "powershell", "powershell.exe", "pwsh.exe", "python", "python3", "py", "cmd", "cmd.exe"}
SKIP_PARTS = {".git", "node_modules"}


@dataclass
class Finding:
    engine: str
    rule: str
    code: str
    message: str
    path: str | None = None


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    not_assessed: list[dict] = field(default_factory=list)
    checked: list[dict] = field(default_factory=list)

    def add(self, engine: str, rule: str, code: str, message: str, path: str | None = None) -> None:
        self.findings.append(Finding(engine, rule, code, message, path))


# --------------------------------------------------------------------------- helpers

def norm(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def read_text(path: Path) -> str:
    return norm(path.read_bytes()).decode("utf-8-sig", errors="replace")


def sha256_norm(path: Path) -> str:
    return hashlib.sha256(norm(path.read_bytes())).hexdigest()


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8-sig"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def repo_files(root: Path) -> list[str]:
    """Tracked plus untracked-but-not-ignored files (POSIX paths)."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root, capture_output=True, check=True,
        ).stdout.decode("utf-8", errors="replace")
        files = [f for f in out.split("\0") if f]
    except (OSError, subprocess.CalledProcessError):
        files = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    return sorted({f for f in files if not SKIP_PARTS & set(f.split("/")) and (root / f).is_file()})


def render_claude(block: str | None) -> str:
    if not block or not block.strip():
        return BRIDGE
    body = block.replace("\r\n", "\n").strip("\n") + "\n"
    return BRIDGE + "\n" + CLAUDE_ONLY_HEADING + "\n\n" + body


def bridge_failures(text: str) -> list[str]:
    text = text.replace("\r\n", "\n")
    if text == BRIDGE:
        return []
    if not text.startswith(BRIDGE + "\n"):
        return ["CLAUDE.md does not start with the canonical bridge (heading, blank line, @AGENTS.md)"]
    remainder = text[len(BRIDGE) + 1:]
    headings = re.findall(r"^#{1,6} .*$", remainder, re.MULTILINE)
    if not remainder.startswith(CLAUDE_ONLY_HEADING + "\n") or headings != [CLAUDE_ONLY_HEADING]:
        return ["CLAUDE.md carries content other than one '## Claude-only notes' section"]
    failures = []
    if len(remainder.rstrip("\n").splitlines()) > CLAUDE_ONLY_MAX_LINES:
        failures.append("Claude-only section exceeds 25 lines")
    if re.search(r"^@\S", remainder, re.MULTILINE):
        failures.append("Claude-only section adds an @ import")
    if TRIGGER_MARKER in remainder or "chwezi-design-engine:trigger" in remainder:
        failures.append("Claude-only section carries the design trigger block (doctrine)")
    if re.search(r"never store book extractions", remainder, re.IGNORECASE):
        failures.append("Claude-only section carries the book-extraction rule (doctrine)")
    return failures


def leading_count(description: str) -> int | None:
    match = COUNT_RE.match(description or "")
    return int(match.group(1)) if match else None


def skills_length(plugin: dict) -> int | None:
    skills = plugin.get("skills")
    return len(skills) if isinstance(skills, list) else None


# --------------------------------------------------------------------------- context

@dataclass
class Engine:
    name: str
    root: Path
    repository: str
    coordination: bool = False
    manifest: dict | None = None


def catalog_engines(package_root: Path, workspace: Path) -> list[Engine]:
    catalog = load_yaml(package_root / "catalog" / "engines.yaml")
    engines = [Engine(e["path"], workspace / e["path"], e.get("repository", e["path"])) for e in catalog["engines"]]
    engines.append(Engine(COORDINATION, package_root if package_root.parent.resolve() == workspace.resolve() else workspace / COORDINATION, COORDINATION, coordination=True))
    return engines


def engine_settings(engine: Engine, register: dict) -> dict:
    """Manifest-like settings: the engine manifest, or the register's coordination block."""
    if engine.coordination:
        return dict(register.get("coordination") or {})
    return dict(engine.manifest or {})


# --------------------------------------------------------------------------- rules

def check_bridge(engine: Engine, settings: dict, report: Report) -> None:
    claude = engine.root / "CLAUDE.md"
    if not claude.is_file():
        report.add(engine.name, "bridge", "bridge-missing", "CLAUDE.md is missing", "CLAUDE.md")
        return
    if not (engine.root / "AGENTS.md").is_file():
        report.add(engine.name, "bridge", "bridge-no-agents", "AGENTS.md is missing beside the bridge", "AGENTS.md")
    text = read_text(claude)
    for failure in bridge_failures(text):
        report.add(engine.name, "bridge", "bridge-drift", failure, "CLAUDE.md")
    expected = render_claude(settings.get("claude_only_block"))
    if not bridge_failures(text) and text != expected:
        report.add(engine.name, "bridge", "bridge-render-drift",
                   "CLAUDE.md differs from the bridge rendered from claude_only_block", "CLAUDE.md")


def check_invariants(engine: Engine, settings: dict, carries_trigger: bool, report: Report) -> None:
    agents = engine.root / "AGENTS.md"
    if not agents.is_file():
        return
    declared = {}
    for item in settings.get("invariants") or []:
        if not isinstance(item, dict) or not item.get("id") or not item.get("phrase"):
            report.add(engine.name, "invariants", "invariant-malformed", f"malformed invariant entry: {item!r}")
            continue
        declared[item["id"]] = item
    exemptions = settings.get("invariant_exemptions") or {}
    required = list(DEFAULT_INVARIANTS) + list(ENGINE_INVARIANTS.get(engine.name, ()))
    for invariant_id in required:
        if invariant_id in declared:
            continue
        if invariant_id in exemptions and str(exemptions[invariant_id]).strip():
            continue
        report.add(engine.name, "invariants", "invariant-undeclared",
                   f"required invariant '{invariant_id}' is neither declared nor exempted with a reason")
    cache: dict[str, str] = {}
    for invariant_id, item in declared.items():
        for rel in item.get("files") or ["AGENTS.md"]:
            path = engine.root / rel
            if rel not in cache:
                cache[rel] = read_text(path) if path.is_file() else ""
            if item["phrase"] not in cache[rel]:
                report.add(engine.name, "invariants", "invariant-missing",
                           f"canary '{invariant_id}' not found: {item['phrase']!r}", rel)
    if carries_trigger and TRIGGER_MARKER not in cache.setdefault("AGENTS.md", read_text(agents)):
        report.add(engine.name, "invariants", "invariant-missing",
                   f"design trigger marker {TRIGGER_MARKER} not found", "AGENTS.md")


def version_sources(engine: Engine, settings: dict) -> tuple[str | None, list[tuple[str, str | None]]]:
    """Return (single source version, [(location, version)])."""
    found: list[tuple[str, str | None]] = []
    plugin = engine.root / ".claude-plugin" / "plugin.json"
    if plugin.is_file():
        found.append((".claude-plugin/plugin.json", load_json(plugin).get("version")))
    marketplace = engine.root / ".claude-plugin" / "marketplace.json"
    if marketplace.is_file():
        for entry in load_json(marketplace).get("plugins", []):
            if entry.get("source") in ("./", "."):
                found.append((f".claude-plugin/marketplace.json#{entry.get('name')}", entry.get("version")))
    codex = engine.root / ".codex-plugin" / "plugin.json"
    if codex.is_file():
        found.append((".codex-plugin/plugin.json", load_json(codex).get("version")))
    if engine.coordination:
        source = found[0][1] if found else None
    else:
        source = settings.get("version")
        found.insert(0, (".skills-engine/engine-manifest.yaml", source))
    return (str(source) if source is not None else None), found


def check_versions(engine: Engine, settings: dict, suite_versions: dict[str, str | None], tag: str | None, report: Report) -> None:
    source, found = version_sources(engine, settings)
    if source is None:
        report.add(engine.name, "versions", "version-missing", "no single-source version (engine-manifest.yaml version)")
        return
    if not re.fullmatch(r"\d+\.\d+\.\d+", source):
        report.add(engine.name, "versions", "version-not-semver", f"version {source!r} is not MAJOR.MINOR.PATCH")
    for location, version in found:
        if str(version) != source:
            report.add(engine.name, "versions", "version-mismatch", f"{location} has {version!r}, source has {source!r}", location)
    if engine.name in suite_versions and suite_versions[engine.name] != source:
        report.add(engine.name, "versions", "version-mismatch",
                   f"suite marketplace entry has {suite_versions[engine.name]!r}, source has {source!r}",
                   "chwezi-engine-agents/.claude-plugin/marketplace.json")
    if tag and tag.lstrip("v") != source:
        report.add(engine.name, "versions", "version-tag-mismatch", f"tag {tag} does not match version {source}")


def check_model_ids(engine: Engine, files: list[str], allow: set[str], report: Report) -> None:
    for rel in files:
        if not rel.lower().endswith(".md") or f"{engine.name}/{rel}" in allow:
            continue
        text = read_text(engine.root / rel)
        for match in MODEL_ID_RE.finditer(text):
            report.add(engine.name, "model-ids", "model-id-corruption", f"corrupted model ID {match.group(0)!r}", rel)


def hook_script_files(files: list[str]) -> list[str]:
    return [f for f in files if f.startswith("hooks/") and f.rsplit(".", 1)[-1] in {"js", "sh", "ps1", "py", "cjs", "mjs", "json"}]


def check_bom(engine: Engine, files: list[str], report: Report) -> None:
    targets = {f for f in files if f.endswith("SKILL.md")}
    targets |= {f for f in ("AGENTS.md", "CLAUDE.md") if (engine.root / f).is_file()}
    targets |= set(hook_script_files(files))
    for rel in sorted(targets):
        with (engine.root / rel).open("rb") as handle:
            if handle.read(3) == BOM:
                report.add(engine.name, "bom", "bom", "file starts with a UTF-8 byte-order mark", rel)


def iter_hook_commands(config) -> list[str]:
    commands = []
    if isinstance(config, dict):
        for key, value in config.items():
            if key == "command" and isinstance(value, str):
                commands.append(value)
            else:
                commands.extend(iter_hook_commands(value))
    elif isinstance(config, list):
        for item in config:
            commands.extend(iter_hook_commands(item))
    return commands


def check_hooks(engine: Engine, report: Report) -> None:
    path = engine.root / "hooks" / "hooks.json"
    if not path.is_file():
        return
    try:
        config = load_json(path)
    except json.JSONDecodeError as error:
        report.add(engine.name, "hooks", "hook-config-invalid", f"hooks.json is not valid JSON: {error}", "hooks/hooks.json")
        return
    for command in iter_hook_commands(config):
        if re.search(r"'\$\{?CLAUDE_PLUGIN_ROOT", command):
            report.add(engine.name, "hooks", "hook-single-quoted-root", f"single-quoted plugin root: {command}", "hooks/hooks.json")
        if "<<" in command:
            report.add(engine.name, "hooks", "hook-heredoc", f"heredoc in hook command: {command}", "hooks/hooks.json")
        first = command.strip().split()[0].strip("\"'") if command.strip() else ""
        if first.lower().endswith((".sh", ".ps1")) and Path(first).name.lower() not in INTERPRETERS:
            report.add(engine.name, "hooks", "hook-bare-script", f"script run without an explicit interpreter: {command}", "hooks/hooks.json")
        for ref in re.findall(r"\$\{?CLAUDE_PLUGIN_ROOT\}?/([^\"'\s]+)", command):
            if not (engine.root / ref).is_file():
                report.add(engine.name, "hooks", "hook-missing-file", f"hook file does not exist: {ref}", "hooks/hooks.json")


def check_plugin_listing(engine: Engine, settings: dict, files: list[str], report: Report) -> None:
    plugin_path = engine.root / ".claude-plugin" / "plugin.json"
    if not plugin_path.is_file():
        return
    skills = load_json(plugin_path).get("skills")
    if not isinstance(skills, list):
        return
    listed = {s[2:] if s.startswith("./") else s for s in skills}
    listed = {s.rstrip("/") for s in listed}
    present = {f.rsplit("/", 1)[0] if "/" in f else "." for f in files if f == "SKILL.md" or f.endswith("/SKILL.md")}
    exclusions = settings.get("plugin_exclusions") or []
    used = set()
    for item in exclusions:
        if not isinstance(item, dict) or not item.get("path") or not str(item.get("reason", "")).strip():
            report.add(engine.name, "plugin", "plugin-exclusion-malformed", f"exclusion needs path and reason: {item!r}")
    patterns = [(i, str(item["path"]).rstrip("/")) for i, item in enumerate(exclusions) if isinstance(item, dict) and item.get("path")]
    for skill_dir in sorted(present - listed):
        hit = [i for i, pattern in patterns if fnmatch.fnmatchcase(skill_dir, pattern)]
        if hit:
            used.update(hit)
            continue
        report.add(engine.name, "plugin", "plugin-unlisted-skill",
                   f"{skill_dir}/SKILL.md is neither in plugin.json nor in plugin_exclusions", f"{skill_dir}/SKILL.md")
    for skill_dir in sorted(listed - present):
        report.add(engine.name, "plugin", "plugin-listed-missing", f"plugin.json lists {skill_dir}/ but it has no SKILL.md", ".claude-plugin/plugin.json")
    for i, pattern in patterns:
        if i not in used:
            report.add(engine.name, "plugin", "plugin-exclusion-stale", f"exclusion {pattern!r} matches no unlisted SKILL.md", ".skills-engine/engine-manifest.yaml")


def check_marketplace_counts(engine: Engine, report: Report) -> None:
    plugin_path = engine.root / ".claude-plugin" / "plugin.json"
    market_path = engine.root / ".claude-plugin" / "marketplace.json"
    if not (plugin_path.is_file() and market_path.is_file()):
        return
    actual = skills_length(load_json(plugin_path))
    for entry in load_json(market_path).get("plugins", []):
        if entry.get("source") not in ("./", "."):
            continue
        stated = leading_count(entry.get("description", ""))
        if stated is not None and actual is not None and stated != actual:
            report.add(engine.name, "marketplace", "marketplace-count-drift",
                       f"description says {stated} skills, plugin.json lists {actual}", ".claude-plugin/marketplace.json")


def check_register(register: dict, workspace: Path, missing_repos: set[str], report: Report) -> list[dict]:
    rows = []
    for row in register.get("assets") or []:
        asset = row.get("id", "?")
        mode = row.get("mode")
        copies = list(row.get("copies") or [])
        summary = {"id": asset, "mode": mode, "copies": len(copies), "status": "ok"}
        before = len(report.findings)

        def missing_sibling(rel: str) -> bool:
            return rel.split("/", 1)[0] in missing_repos

        if mode == "byte":
            canonical = workspace / row["canonical"]
            if missing_sibling(row["canonical"]):
                summary["status"] = "NOT_ASSESSED"
            elif not canonical.is_file():
                report.add(asset, "register", "shared-asset-missing-canonical", "canonical file missing", row["canonical"])
            else:
                want = sha256_norm(canonical)
                for rel in copies:
                    if missing_sibling(rel):
                        continue
                    path = workspace / rel
                    if not path.is_file():
                        report.add(asset, "register", "shared-asset-missing-copy", "registered copy missing", rel)
                    elif sha256_norm(path) != want:
                        report.add(asset, "register", "shared-asset-byte-drift", "copy differs from canonical after CRLF normalisation", rel)
        elif mode == "block":
            start, end = row["markers"]["start"], row["markers"]["end"]
            canonical = workspace / row["canonical"]
            block = None
            if canonical.is_file():
                text = read_text(canonical)
                if start in text and end in text:
                    block = text[text.index(start):text.index(end) + len(end)]
            if block is None:
                report.add(asset, "register", "shared-asset-missing-canonical", "canonical block not found", row["canonical"])
            else:
                for rel in copies:
                    if missing_sibling(rel):
                        continue
                    path = workspace / rel
                    text = read_text(path) if path.is_file() else ""
                    if block not in text:
                        report.add(asset, "register", "shared-asset-block-drift", "text between the markers differs from the canonical block", rel)
        elif mode == "registered-variant":
            variants = row.get("variants") or {}
            for rel in copies:
                if missing_sibling(rel):
                    continue
                path = workspace / rel
                if not path.is_file():
                    report.add(asset, "register", "shared-asset-missing-copy", "registered copy missing", rel)
                    continue
                registered = variants.get(rel)
                if not isinstance(registered, dict) or not registered.get("sha256") or not registered.get("owner") or not registered.get("reason"):
                    report.add(asset, "register", "shared-asset-unregistered-variant", "copy has no registered hash, owner and reason", rel)
                elif sha256_norm(path) != registered["sha256"]:
                    report.add(asset, "register", "shared-asset-unregistered-variant", "copy hash is not the registered variant", rel)
        elif mode == "external":
            summary["status"] = f"enforced by {row.get('enforced_by')}"
        else:
            report.add(asset, "register", "shared-asset-bad-mode", f"unknown mode {mode!r}")
        for pattern in row.get("discover") or []:
            known = set(copies) | ({row["canonical"]} if row.get("canonical") else set())
            for found in sorted(workspace.glob(pattern)):
                rel = found.relative_to(workspace).as_posix()
                if SKIP_PARTS & set(rel.split("/")):
                    continue
                if rel.split("/", 1)[0] not in (register.get("public_repositories") or []):
                    continue
                if rel not in known:
                    report.add(asset, "register", "shared-asset-unregistered-copy", "copy found on disk but not in the register", rel)
        if len(report.findings) > before:
            summary["status"] = "drift"
        rows.append(summary)
    for row in register.get("exclusions") or []:
        rows.append({"id": row.get("asset"), "mode": "exclusion", "engine": row.get("engine"), "reason": row.get("reason"), "status": "excluded"})
    return rows


def suite_entries(package_root: Path, engines: list[Engine]) -> dict[str, dict]:
    """Map engine name -> suite marketplace entry."""
    path = package_root / ".claude-plugin" / "marketplace.json"
    if not path.is_file():
        return {}
    by_repo = {e.repository: e.name for e in engines}
    entries = {}
    for entry in load_json(path).get("plugins", []):
        source = entry.get("source")
        if isinstance(source, str):
            entries[COORDINATION] = entry
        elif isinstance(source, dict) and source.get("url"):
            repo = source["url"].rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
            if repo in by_repo:
                entries[by_repo[repo]] = entry
    return entries


# --------------------------------------------------------------------------- drivers

def run_check(package_root: Path, workspace: Path, only: Path | None, tag: str | None) -> Report:
    report = Report()
    register_path = package_root / "catalog" / "shared-assets.yaml"
    register = load_yaml(register_path) if register_path.is_file() else {}
    engines = catalog_engines(package_root, workspace)
    if only is not None:
        only = only.resolve()
        engines = [e for e in engines if e.root.resolve() == only] or [Engine(only.name, only, only.name)]
    trigger_rows = [r for r in register.get("assets") or [] if r.get("mode") == "block" and r.get("markers", {}).get("start") == TRIGGER_MARKER]
    trigger_repos = {c.split("/", 1)[0] for r in trigger_rows for c in r.get("copies") or [] if c.endswith("/AGENTS.md")}
    suite = suite_entries(package_root, engines)
    suite_versions = {name: entry.get("version") for name, entry in suite.items() if name != COORDINATION}
    model_id_allow = {str(item.get("path")) for item in register.get("model_id_allowlist") or []
                      if isinstance(item, dict) and str(item.get("reason", "")).strip()}
    missing: set[str] = set()
    for engine in engines:
        if not engine.root.is_dir():
            missing.add(engine.name)
            report.not_assessed.append({"engine": engine.name, "reason": f"sibling repository missing at {engine.root}"})
            continue
        manifest_path = engine.root / ".skills-engine" / "engine-manifest.yaml"
        if not engine.coordination:
            try:
                engine.manifest = load_yaml(manifest_path) if manifest_path.is_file() else {}
            except yaml.YAMLError as error:
                report.add(engine.name, "manifest", "manifest-invalid", f"engine-manifest.yaml is not valid YAML: {error}")
                continue
        settings = engine_settings(engine, register)
        files = repo_files(engine.root)
        check_bridge(engine, settings, report)
        check_invariants(engine, settings, engine.name in trigger_repos, report)
        check_versions(engine, settings, suite_versions, tag, report)
        check_model_ids(engine, files, model_id_allow, report)
        check_bom(engine, files, report)
        check_hooks(engine, report)
        check_plugin_listing(engine, settings, files, report)
        check_marketplace_counts(engine, report)
        report.checked.append({"engine": engine.name, "claude_md_bytes": (engine.root / "CLAUDE.md").stat().st_size if (engine.root / "CLAUDE.md").is_file() else None})
    if only is None:
        report.checked.append({"register": check_register(register, workspace, missing, report)})
    return report


def render_engine(engine_root: Path, dry_run: bool = False) -> tuple[int, list[str]]:
    """Write the closed list of derived fields. Returns (exit code, changed files)."""
    manifest_path = engine_root / ".skills-engine" / "engine-manifest.yaml"
    try:
        manifest = load_yaml(manifest_path)
    except (OSError, yaml.YAMLError) as error:
        print(f"refusing to render: cannot read {manifest_path}: {error}", file=sys.stderr)
        return 1, []
    if not isinstance(manifest, dict) or not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        print("refusing to render: engine-manifest.yaml needs a MAJOR.MINOR.PATCH 'version'", file=sys.stderr)
        return 1, []
    version = str(manifest["version"])
    block = manifest.get("claude_only_block")
    if block is not None and not isinstance(block, str):
        print("refusing to render: claude_only_block must be a string", file=sys.stderr)
        return 1, []
    planned: dict[Path, bytes] = {}
    claude = render_claude(block).encode("utf-8")
    claude_path = engine_root / "CLAUDE.md"
    if not claude_path.is_file() or norm(claude_path.read_bytes()) != claude:
        planned[claude_path] = claude
    plugin_path = engine_root / ".claude-plugin" / "plugin.json"
    count = None
    if plugin_path.is_file():
        count = skills_length(load_json(plugin_path))
    for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        path = engine_root / rel
        if not path.is_file():
            continue
        raw = path.read_bytes().decode("utf-8")
        data = json.loads(raw)
        text = raw
        if rel.endswith("marketplace.json"):
            roots = [e for e in data.get("plugins", []) if e.get("source") in ("./", ".")]
            for entry in roots:
                text = replace_in_entry(text, entry, version, count)
        else:
            text, n = re.subn(r'^(  "version"\s*:\s*)"[^"]*"', lambda m: f'{m.group(1)}"{version}"', text, count=1, flags=re.MULTILINE)
            if n != 1:
                print(f"refusing to render: no top-level version field in {rel}", file=sys.stderr)
                return 1, []
        if text != raw:
            json.loads(text)
            planned[path] = text.encode("utf-8")
    changed = []
    for path, data in planned.items():
        changed.append(path.relative_to(engine_root).as_posix())
        if not dry_run:
            path.write_bytes(data)
    return 0, changed


def replace_in_entry(text: str, entry: dict, version: str, count: int | None) -> str:
    """Rewrite the version and leading count of one marketplace entry in place."""
    name_token = json.dumps(entry.get("name"), ensure_ascii=False)
    anchor = text.find(f'"name": {name_token}')
    if anchor < 0:
        return text
    close = text.find("\n    }", anchor)
    close = len(text) if close < 0 else close
    segment = text[anchor:close]
    segment = re.sub(r'("version"\s*:\s*)"[^"]*"', lambda m: f'{m.group(1)}"{version}"', segment, count=1)
    description = entry.get("description") or ""
    if count is not None and leading_count(description) is not None:
        new_description = COUNT_RE.sub(lambda m: f"{count}{m.group(2)}", description, count=1)
        old_token = json.dumps(description, ensure_ascii=False)
        new_token = json.dumps(new_description, ensure_ascii=False)
        segment = segment.replace(old_token, new_token, 1)
    return text[:anchor] + segment + text[close:]


def summarise(report: Report) -> str:
    lines = []
    by_engine: dict[str, list[Finding]] = {}
    for finding in report.findings:
        by_engine.setdefault(finding.engine, []).append(finding)
    for engine, findings in sorted(by_engine.items()):
        lines.append(f"{engine}: {len(findings)} finding(s)")
        for f in findings:
            lines.append(f"  [{f.code}] {f.message}" + (f" ({f.path})" if f.path else ""))
    for item in report.not_assessed:
        lines.append(f"NOT_ASSESSED {item['engine']}: {item['reason']}")
    checked = [c["engine"] for c in report.checked if "engine" in c]
    lines.append(f"checked {len(checked)} repositories; findings {len(report.findings)}; not assessed {len(report.not_assessed)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check or render Chwezi host files.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--render", action="store_true")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--tag")
    parser.add_argument("--json", action="store_true", help="print the JSON report instead of the text summary")
    parser.add_argument("--dry-run", action="store_true", help="with --render: list files that would change")
    args = parser.parse_args(argv)
    if args.render:
        if not args.engine:
            parser.error("--render needs --engine <path>")
        code, changed = render_engine(args.engine.resolve(), args.dry_run)
        print(json.dumps({"changed": changed, "dry_run": args.dry_run}))
        return code
    try:
        report = run_check(args.package_root.resolve(), args.workspace_root.resolve(), args.engine, args.tag)
    except (OSError, yaml.YAMLError, json.JSONDecodeError, KeyError) as error:
        print(f"check could not run: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"findings": [asdict(f) for f in report.findings], "not_assessed": report.not_assessed,
                          "checked": report.checked}, indent=2, ensure_ascii=False))
    else:
        print(summarise(report))
    if report.findings:
        return 1
    if report.not_assessed:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
