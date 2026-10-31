#!/usr/bin/env python3
"""Portfolio public-repository hygiene check (pass-2 K2). Read-only.

All twelve Chwezi repositories are public. For each one this check reads the *tracked* files
(``git ls-files``) and reports:

``tracked-local-settings``  a tracked per-user settings file (``.claude/settings.local.json``,
                            ``*.local.json``). Always a finding.
``tracked-env-file``        a tracked ``.env`` or ``.env.<name>`` file, or a private-key file
                            (``id_rsa``, ``*.pem`` ...). Example files (``.env.example``) pass.
``key-shaped-string``       a string shaped like a credential (cloud, source-host, chat, payment
                            and AI-provider keys, private-key blocks, JSON web tokens, and
                            high-entropy ``secret = ...`` assignments). Always a finding.
``user-profile-path``       a path inside a person's profile folder: a Windows or macOS user folder with a
                            real name, or a Linux home folder whose name is listed in the policy's
                            ``private_user_names``.
``machine-path``            a local development web-root (the WAMP, XAMPP and Laragon default folders) or a
                            WSL drive mount. Both path rules fail in *live* files. In dated *record* files
                            (``catalog/hygiene-policy.yaml`` ``record_globs``) their lines are counted
                            against a per-repository ceiling that may only fall (a ratchet).

Secrets, settings and environment files are never excused by the record list.

Placeholders (``<name>``, ``$USER``, ``/home/user``, ``C:\\Users\\<you>``) and standard operating-system
folders (``C:\\Windows``, ``/home/deploy`` in an administration example) are not machine paths.
Output never prints a matched secret: it shows the rule, ``path:line`` and a redacted shape
(first four characters and the length). The check never edits a repository and never rewrites
history; removing a tracked file from history needs a separate, authorised decision.

Exit codes: 0 clean, 1 findings, 3 NOT_ASSESSED only (an engine checkout is missing or
ambiguous). A missing engine is never a pass.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import engine_roots  # noqa: E402

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 2_000_000
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".bz2", ".xz", ".7z", ".woff", ".woff2",
    ".ttf", ".otf", ".eot", ".xlsx", ".docx", ".pptx", ".odt", ".mp3", ".mp4", ".mov", ".wav", ".jar", ".class",
}

LOCAL_SETTINGS_GLOBS = ("*/.claude/settings.local.json", ".claude/settings.local.json", "*.local.json")
ENV_NAME_RE = re.compile(r"^\.env(\..+)?$")
ENV_SAFE_SUFFIXES = (".example", ".sample", ".template", ".dist", ".tpl")
KEY_FILE_NAMES = {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
KEY_FILE_SUFFIXES = (".pem", ".p12", ".pfx", ".ppk")

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("stripe-key", re.compile(r"\b[sr]k_(?:live|test)_[0-9A-Za-z]{16,}\b")),
    ("provider-secret-key", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{32,}\b")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----")),
    ("json-web-token", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")),
)
ASSIGNMENT_RE = re.compile(
    r"""(?ix)\b(?:api[_-]?key|secret(?:[_-]?key)?|access[_-]?token|auth[_-]?token|client[_-]?secret|password|passwd)\b
        ["']?\s*[:=]\s*["']?([A-Za-z0-9/+_\-=]{20,})["']?""")
PLACEHOLDER_WORDS = ("example", "placeholder", "changeme", "change-me", "your", "xxxx", "dummy", "sample", "redacted",
                     "fake", "test", "token_here", "insert", "todo", "<", "${", "$(", "{{", "env.", "process.env", "os.environ",
                     "abcdef", "123456", "000000", "aaaaaa")
BASE64_BODY_RE = re.compile(r"^[A-Za-z0-9+/=]{40,}$")

WIN_USER_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]{1,2}Users[\\/]+([A-Za-z0-9_.\-]+)", re.IGNORECASE)
WEBROOT_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]{1,2}(?:wamp64|xampp|laragon)\b", re.IGNORECASE)
MAC_USER_RE = re.compile(r"(?<![A-Za-z0-9_./-])/Users/([A-Za-z0-9_.\-<>{}$%]+)")
HOME_RE = re.compile(r"(?<![A-Za-z0-9_./-])/home/([A-Za-z0-9_.\-<>{}$%]+)")
WSL_RE = re.compile(r"(?<![A-Za-z0-9_./-])/mnt/[a-z](?=/)")
PATH_RULES = ('machine-path', 'user-profile-path')
PLACEHOLDER_USERS = {"user", "username", "youruser", "your-user", "you", "name", "yourname", "me", "example", "foo", "bar",
                     "runner", "ubuntu", "vagrant", "admin", "public", "default", "all users", "shared", "guest", "alice", "bob",
                     "carol", "john", "jane", "jdoe", "johndoe", "jsmith", "tester", "dev", "developer", "deploy", "appuser"}


@dataclass
class Finding:
    repo: str
    rule: str
    path: str
    line: int | None
    detail: str
    record: bool = False


@dataclass
class RepoResult:
    repo: str
    files_scanned: int = 0
    findings: list[Finding] = field(default_factory=list)
    record_path_lines: int = 0
    ceiling: int | None = None


def entropy(value: str) -> float:
    counts = Counter(value)
    total = len(value)
    return -sum(n / total * math.log2(n / total) for n in counts.values())


def redact(value: str) -> str:
    return f"{value[:4]}...({len(value)} characters)"


def is_placeholder_user(name: str) -> bool:
    lowered = name.strip().lower()
    return (not lowered or lowered in PLACEHOLDER_USERS or lowered[0] in "<${%" or lowered.startswith("..")
            or lowered.startswith("<"))


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files failed in {root.name}")
    return [item for item in result.stdout.decode("utf-8", errors="replace").split("\0") if item]


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(path, pattern.rstrip("/") + "/*")
               or (pattern.endswith("/**") and path.startswith(pattern[:-2])) for pattern in patterns)


def path_findings(rel: str) -> list[tuple[str, str]]:
    name = rel.rsplit("/", 1)[-1]
    out: list[tuple[str, str]] = []
    if any(fnmatch.fnmatchcase(rel, pattern) for pattern in LOCAL_SETTINGS_GLOBS):
        out.append(("tracked-local-settings", "a per-user settings file is tracked in a public repository"))
    if ENV_NAME_RE.match(name) and not name.endswith(ENV_SAFE_SUFFIXES):
        out.append(("tracked-env-file", "an environment file is tracked; only .example, .sample or .template variants may be"))
    if name in KEY_FILE_NAMES or name.endswith(KEY_FILE_SUFFIXES):
        out.append(("tracked-env-file", "a private-key or certificate-bundle file is tracked"))
    return out


def line_findings(text: str, private_users: frozenset[str] = frozenset()) -> list[tuple[str, int, str]]:
    """Return (rule, line number, detail) for secrets and machine paths in one file."""
    found: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        if len(line) > 4000:
            line = line[:4000]
        for rule, pattern in SECRET_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            # A private-key header quoted in a scanner pattern or a how-to is documentation; a key
            # has a base64 body on the next line.
            if rule == "private-key-block" and not (number < len(lines) and BASE64_BODY_RE.match(lines[number].strip())):
                continue
            found.append(("key-shaped-string", number, f"{rule}: {redact(match.group(0))}"))
        for match in ASSIGNMENT_RE.finditer(line):
            value = match.group(1)
            lowered = value.lower()
            if any(word in lowered for word in PLACEHOLDER_WORDS) or entropy(value) < 3.6 or value.isalpha():
                continue
            found.append(("key-shaped-string", number, f"secret-assignment: {redact(value)}"))
        win_user = next((m for m in WIN_USER_RE.finditer(line) if not is_placeholder_user(m.group(1))), None)
        mac_user = next((m for m in MAC_USER_RE.finditer(line) if not is_placeholder_user(m.group(1))), None)
        home_user = next((m for m in HOME_RE.finditer(line) if m.group(1).strip().lower() in private_users), None)
        if win_user or mac_user or home_user:
            found.append(("user-profile-path", number, "path inside a person's profile folder"))
        elif WEBROOT_RE.search(line) or WSL_RE.search(line):
            found.append(("machine-path", number, "local web-root or drive-mount path"))
    return found


def scan_repo(name: str, root: Path, policy: dict) -> RepoResult:
    repo_policy = (policy.get("repositories") or {}).get(name) or {}
    record_globs = list(policy.get("record_globs") or []) + list(repo_policy.get("record_globs") or [])
    allow = [item for item in (policy.get("allow") or []) + (repo_policy.get("allow") or []) if isinstance(item, dict)]
    result = RepoResult(name, ceiling=repo_policy.get("record_path_ceiling"))
    private_users = frozenset(str(n).lower() for n in (policy.get("private_user_names") or []))

    def allowed(rule: str, rel: str) -> bool:
        return any(item.get("rule") == rule and matches_any(rel, [str(item.get("path", ""))]) and str(item.get("reason", "")).strip()
                   for item in allow)

    for rel in tracked_files(root):
        for rule, detail in path_findings(rel):
            if not allowed(rule, rel):
                result.findings.append(Finding(name, rule, rel, None, detail))
        if Path(rel).suffix.lower() in BINARY_SUFFIXES:
            continue
        text = read_text(root / rel)
        if text is None:
            continue
        result.files_scanned += 1
        settings_file = any(rule == "tracked-local-settings" for rule, _ in path_findings(rel))
        is_record = matches_any(rel, record_globs)
        seen_lines: set[tuple[str, int]] = set()
        for rule, number, detail in line_findings(text, private_users):
            if allowed(rule, rel) or (rule, number) in seen_lines:
                continue
            if settings_file and rule in PATH_RULES:
                continue  # the file-level finding already stands; do not list every path inside it
            seen_lines.add((rule, number))
            if rule in PATH_RULES and is_record:
                result.record_path_lines += 1
                continue
            result.findings.append(Finding(name, rule, rel, number, detail))
    if result.ceiling is not None and result.record_path_lines > int(result.ceiling):
        result.findings.append(Finding(name, "path-ceiling", "(dated records)", None,
                                       f"{result.record_path_lines} machine or user-profile path lines in dated records exceed the ceiling of {result.ceiling}",
                                       record=True))
    return result


def load_policy(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must be a mapping")
    return data


def summarise(results: list[RepoResult], not_assessed: list[dict]) -> str:
    lines: list[str] = []
    for result in results:
        if result.findings:
            lines.append(f"{result.repo}: {len(result.findings)} finding(s)")
            for f in result.findings:
                where = f"{f.path}:{f.line}" if f.line else f.path
                lines.append(f"  [{f.rule}] {where}: {f.detail}")
    for item in not_assessed:
        lines.append(f"NOT_ASSESSED {item['repo']}: {item['reason']}")
    total = sum(len(r.findings) for r in results)
    records = sum(r.record_path_lines for r in results)
    lines.append(f"checked {len(results)} repositories; findings {total}; path lines in dated records {records}; not assessed {len(not_assessed)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--engines-root", type=Path, action="append", default=[],
                        help="folder that holds engine checkouts (repeatable; also CHWEZI_ENGINES_ROOT)")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--repo", type=Path, action="append", default=[], help="check only this checkout (repeatable)")
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    package = args.package_root.resolve()
    policy = load_policy(args.policy or package / "catalog" / "hygiene-policy.yaml")
    targets: list[tuple[str, Path]] = []
    not_assessed: list[dict] = []
    if args.repo:
        targets = [(path.resolve().name, path.resolve()) for path in args.repo]
    else:
        catalog = yaml.safe_load((package / "catalog" / "engines.yaml").read_text(encoding="utf-8"))
        roots = engine_roots.roots_from(args.engines_root, fallback=args.workspace_root)
        for entry in catalog["engines"]:
            resolution = engine_roots.resolve_engine(entry, roots)
            if resolution.found:
                targets.append((str(entry["id"]), resolution.path))
            else:
                not_assessed.append({"repo": str(entry["id"]), "reason": engine_roots.describe(resolution)})
        targets.append((engine_roots.COORDINATION, package))
    results: list[RepoResult] = []
    for name, root in targets:
        try:
            results.append(scan_repo(name, root, policy))
        except RuntimeError as error:
            not_assessed.append({"repo": name, "reason": str(error)})
    if args.json:
        print(json.dumps({"results": [{"repo": r.repo, "files_scanned": r.files_scanned,
                                       "record_path_lines": r.record_path_lines,
                                       "findings": [asdict(f) for f in r.findings]} for r in results],
                          "not_assessed": not_assessed}, indent=2))
    else:
        print(summarise(results, not_assessed))
    if any(r.findings for r in results):
        return 1
    return 3 if not_assessed else 0


if __name__ == "__main__":
    raise SystemExit(main())
