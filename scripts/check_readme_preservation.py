#!/usr/bin/env python3
"""Check that a README rewrite lost nothing an interface depends on (README kaizen, 31 October 2026). Read-only.

``check_readme_preservation.py REPO BASE NEW`` compares ``README.md`` at two git revisions of REPO and
reports what the rewrite lost. BASE and NEW are any revisions ``git`` resolves (branch, tag, commit).
With BASE equal to NEW (for example ``HEAD HEAD``) the link-target and command checks are trivially
satisfied, and the two anchor checks still verify the current README.

Link targets  Every relative path or URL the old README linked must still be linked from the new README,
              or from a Markdown file the new revision added or changed (reported as moved, not lost). A
              relative target is resolved against the folder of the file that holds it, so a table moved to
              ``docs/page.md`` and linked there as ``../skills/x/SKILL.md`` is the same target as
              ``skills/x/SKILL.md`` in the README. A bare URL anywhere in the text counts, code fences included.
Commands      Every non-comment line of every fenced code block in the old README, and every inline code span
              of six or more characters that starts with a command word (``python3``, ``git``, ``npm`` and
              the others in ``COMMAND_RE``) and has an argument, must still appear in the new README or
              in a changed Markdown file. Runs of white space are treated as one space.
Anchors       Every heading anchor that a tracked file links to the README must still exist in the new
              README, and every in-page link in the new README must resolve to a heading. In Markdown files
              a link counts when its target, resolved against that file's folder, is the README
              (``](../README.md#anchor)``); in other text files (scripts, YAML, JSON) a written
              ``README.md#anchor`` counts as a link to the README at the repository root. A plain-text
              mention in Markdown that is not a link is not checked; write it as a link. Anchors are
              GitHub's: lower case, punctuation removed, spaces to hyphens, repeated headings suffixed
              ``-1``, ``-2``. Setext headings and headings in raw HTML are not read.

Also printed, without failing: heading anchors the old README had and the new one lacks. Other
repositories may link to them; this check cannot see those links.

Output never contains a path outside the repository. Exit codes: 0 nothing lost and nothing broken;
1 at least one lost link or command or broken anchor; 3 NOT_ASSESSED, REPO is not a git repository, a
revision does not resolve, or the README is missing at a revision. A check that could not run is never
a pass.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys
from dataclasses import dataclass, field
from urllib.parse import unquote

COMMAND_RE = re.compile(
    r"^(python3?|node|npm|bash|sh|git|pip3?|pytest|sudo|podman|docker|curl|claude|codex|\./|\.\\|install|powershell|pwsh)\b"
)
INLINE_CODE_RE = re.compile(r"`([^`\n]{6,200})`")
INLINE_LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[(?!\^)[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$", re.MULTILINE)
BARE_URL_RE = re.compile(r"https?://[^\s)>\]`\"']+")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
README_LINK_RE = re.compile(r"\]\(([^)\s#]*README\.md)#([^)\s]+)\)")
TEXT_ANCHOR_RE = re.compile(r"([\w./\\-]*README\.md)#([\w%-]+)")
URL_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:")
TEXT_SUFFIXES = (".md", ".py", ".js", ".mjs", ".ts", ".yaml", ".yml", ".json", ".sh", ".ps1", ".txt", ".toml")


class NotAssessed(Exception):
    """The check could not run (bad repository, revision or missing README)."""


def git(repo: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run git in REPO; output is decoded as UTF-8 with undecodable bytes replaced."""
    try:
        raw = subprocess.run(["git", "-C", repo, *args], capture_output=True, check=False)
    except OSError as error:
        raise NotAssessed(f"git could not run: {error.strerror or error}") from error
    return subprocess.CompletedProcess(
        raw.args, raw.returncode, raw.stdout.decode("utf-8", errors="replace"), raw.stderr.decode("utf-8", errors="replace")
    )


def show(repo: str, rev: str, path: str) -> str | None:
    """File content at a revision, or None when the file does not exist there."""
    result = git(repo, "show", f"{rev}:{path}")
    return result.stdout if result.returncode == 0 else None


def heading_slugs(text: str) -> set[str]:
    """GitHub-style anchors of every heading outside code fences."""
    seen: dict[str, int] = {}
    slugs: set[str] = set()
    in_code = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", match.group(1))
        title = re.sub(r"[`*_]", "", title).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", title, flags=re.UNICODE).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        slugs.add(slug if count == 0 else f"{slug}-{count}")
    return slugs


def link_targets(text: str, base_dir: str = "") -> set[str]:
    """Link targets in a Markdown text. Relative targets are resolved against BASE_DIR (the folder of the
    file holding the text, relative to the repository root); URLs and site-absolute targets are kept as written.
    Inline links, reference definitions and bare URLs count; the part after ``#`` does not."""
    targets: set[str] = set()
    written = [m.group(1) for m in INLINE_LINK_RE.finditer(text)] + [m.group(1) for m in REFERENCE_LINK_RE.finditer(text)]
    for raw in written:
        target = raw.split("#")[0]
        if not target or target.startswith("mailto:"):
            continue
        if not URL_SCHEME_RE.match(target) and not target.startswith("/"):
            target = posixpath.normpath(posixpath.join(base_dir, target))
        targets.add(target)
    for match in BARE_URL_RE.finditer(text):
        targets.add(match.group(0).rstrip(".,;:"))
    return targets


def commands(text: str) -> set[str]:
    """Commands in a Markdown text: fenced code lines (comments excluded) and command-like inline code."""
    found: set[str] = set()
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code and stripped and not stripped.startswith(("#", "//")):
            found.add(re.sub(r"\s+", " ", stripped))
    for match in INLINE_CODE_RE.finditer(text):
        command = re.sub(r"\s+", " ", match.group(1).strip())
        if COMMAND_RE.match(command) and " " in command:
            found.add(command)
    return found


def linked_readme_anchors(repo: str, rev: str, readme: str) -> dict[str, set[str]]:
    """Map each anchor that a tracked file links to README (at REV) to the files that link it."""
    result = git(repo, "grep", "-I", "-z", "--no-color", "-e", r"README\.md#", rev, "--")
    linked: dict[str, set[str]] = {}
    target_readme = posixpath.normpath(readme)
    # With -z every hit is "REV:path", a NUL, then the matching line and a newline; the next hit follows at once.
    fields = result.stdout.split("\0")
    path = fields[0]
    for chunk in fields[1:]:
        text, _, next_path = chunk.rpartition("\n")
        source = path[len(rev) + 1:]
        path = next_path
        if not source.endswith(TEXT_SUFFIXES):
            continue
        if source.endswith(".md"):
            hits, folder = README_LINK_RE.findall(text), posixpath.dirname(source)
        else:
            hits, folder = TEXT_ANCHOR_RE.findall(text), ""
        for file_part, anchor in hits:
            if posixpath.normpath(posixpath.join(folder, file_part.replace("\\", "/"))) == target_readme:
                linked.setdefault(unquote(anchor).lower(), set()).add(source)
    return linked


@dataclass
class Report:
    old_links: int = 0
    new_links: int = 0
    lost_links: list[str] = field(default_factory=list)
    moved_links: list[str] = field(default_factory=list)
    old_commands: int = 0
    lost_commands: list[str] = field(default_factory=list)
    moved_commands: list[str] = field(default_factory=list)
    linked_anchors: int = 0
    broken_anchors: dict[str, set[str]] = field(default_factory=dict)
    inpage_anchors: int = 0
    broken_inpage: list[str] = field(default_factory=list)
    removed_anchors: list[str] = field(default_factory=list)

    @property
    def problems(self) -> int:
        return len(self.lost_links) + len(self.lost_commands) + len(self.broken_anchors) + len(self.broken_inpage)


def check(repo: str, base: str, new: str, readme: str = "README.md") -> Report:
    """Compare README at BASE and NEW. Raises NotAssessed when the check cannot run."""
    if git(repo, "rev-parse", "--git-dir").returncode != 0:
        raise NotAssessed("the repository argument is not a git repository")
    for rev in (base, new):
        if git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").returncode != 0:
            raise NotAssessed(f"revision {rev!r} does not resolve in the repository")
    old_text, new_text = show(repo, base, readme), show(repo, new, readme)
    for rev, text in ((base, old_text), (new, new_text)):
        if text is None:
            raise NotAssessed(f"{readme} does not exist at {rev!r}")
    assert old_text is not None and new_text is not None

    diff = git(repo, "diff", "--name-only", "-z", "--diff-filter=AM", "--no-renames", base, new, "--")
    changed = [p for p in diff.stdout.split("\0") if p.endswith(".md")]
    changed_text = {p: show(repo, new, p) or "" for p in changed}

    report = Report()
    new_links = link_targets(new_text, posixpath.dirname(readme))
    elsewhere: set[str] = set()
    for path, text in changed_text.items():
        elsewhere |= link_targets(text, posixpath.dirname(path))
    old_links = link_targets(old_text, posixpath.dirname(readme))
    report.old_links, report.new_links = len(old_links), len(new_links)
    for target in sorted(old_links - new_links):
        (report.moved_links if target in elsewhere else report.lost_links).append(target)

    old_commands, new_commands = commands(old_text), commands(new_text)
    elsewhere_commands = commands("\n".join(changed_text.values()))
    report.old_commands = len(old_commands)
    for command in sorted(old_commands - new_commands):
        (report.moved_commands if command in elsewhere_commands else report.lost_commands).append(command)

    new_slugs = heading_slugs(new_text)
    linked = linked_readme_anchors(repo, new, readme)
    report.linked_anchors = len(linked)
    report.broken_anchors = {a: files for a, files in linked.items() if a not in new_slugs}
    inpage = {unquote(m.group(1)).lower() for m in re.finditer(r"\]\(#([^)\s]+)\)", new_text)}
    report.inpage_anchors = len(inpage)
    report.broken_inpage = sorted(a for a in inpage if a not in new_slugs)
    report.removed_anchors = sorted(heading_slugs(old_text) - new_slugs)
    return report


def print_report(report: Report, limit: int = 30) -> None:
    print(f"links: old README {report.old_links} targets; new README {report.new_links}; "
          f"moved to docs {len(report.moved_links)}; LOST {len(report.lost_links)}")
    for target in report.lost_links[:limit]:
        print(f"  LOST link target: {target}")
    kept = report.old_commands - len(report.lost_commands) - len(report.moved_commands)
    print(f"commands: old README {report.old_commands}; kept in README {kept}; "
          f"moved to docs {len(report.moved_commands)}; LOST {len(report.lost_commands)}")
    for command in report.lost_commands[:limit]:
        print(f"  LOST command: {command[:150]}")
    print(f"anchors: {report.linked_anchors} README anchor links in tracked files; BROKEN {len(report.broken_anchors)}")
    for anchor, files in sorted(report.broken_anchors.items())[:limit]:
        print(f"  BROKEN anchor #{anchor} linked from {sorted(files)[:3]}")
    print(f"in-page links: {report.inpage_anchors} anchors used; BROKEN {len(report.broken_inpage)}")
    for anchor in report.broken_inpage[:limit]:
        print(f"  BROKEN in-page link #{anchor}")
    if report.removed_anchors:
        print(f"note: {len(report.removed_anchors)} heading anchor(s) of the old README are gone; "
              f"links from other repositories cannot be checked here: {', '.join('#' + a for a in report.removed_anchors[:limit])}")
    print("RESULT:", "OK" if report.problems == 0 else f"{report.problems} problem(s)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", help="path of the git repository")
    parser.add_argument("base", help="revision that holds the old README")
    parser.add_argument("new", help="revision that holds the new README")
    parser.add_argument("--readme", default="README.md", help="README path inside the repository (default README.md)")
    args = parser.parse_args(argv)
    try:
        report = check(args.repo, args.base, args.new, args.readme)
    except NotAssessed as error:
        print(f"NOT_ASSESSED: {error}", file=sys.stderr)
        return 3
    print_report(report)
    return 1 if report.problems else 0


if __name__ == "__main__":
    sys.exit(main())
