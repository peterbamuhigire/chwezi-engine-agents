"""Build the pinned, synthetic fixture workspace for the coordinator MCP QA evaluation (M10-05-T10).

Stdlib only; no network; no model call. Every repository is synthetic and is created with a fixed
identity (``eval <eval@invalid>``), fixed commit dates and user/system git configuration excluded,
so commit hashes are reproducible and the frozen answers in ``coordinator-qa.yaml`` stay stable.

Layout built under ``<dest>``::

    catalog/engines.yaml          pinned catalogue (alpha, beta, gamma, epsilon; delta is uncatalogued)
    remotes/<name>.git            bare upstreams for alpha, beta and gamma
    alpha-skills/                 clean, upstream one commit ahead after fetch (behind 1)
    beta-skills/                  upstream even, working tree dirty (modified tracked file)
    gamma-skills/                 two local commits ahead of upstream, clean; remote repo name gamma-registry
    epsilon-skills/               catalogued, no remote and no upstream
    delta-notes/                  uncatalogued, README.md only, no remote

    python -X utf8 evals/mcp/build_fixture_workspace.py --dest <empty dir>

Prints a JSON summary with each repository's HEAD and a build hash over them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

IDENTITY = ("eval", "eval@invalid")
BASE_DATE = "2026-09-29T00:00:{:02d}+00:00"

CATALOG = """schema_version: "1.0"
version: 1
engines:
  - id: alpha-skills
    repository: alpha-skills
    path: alpha-skills
    router: CLAUDE.md
    validators:
      - "python -c \\"print('alpha structure ok')\\""
      - "python -c \\"print('alpha routing ok')\\""
  - id: beta-skills
    repository: beta-skills
    path: beta-skills
    router: AGENTS.md
    validators: "python -c \\"print('beta ok')\\""
  - id: gamma-skills
    repository: gamma-registry
    path: gamma-skills
    router: AGENTS.md
    validators:
      - "python -c \\"print('gamma structure ok')\\""
      - "python -c \\"import sys; sys.exit(3)\\""
  - id: epsilon-skills
    repository: epsilon-skills
    path: epsilon-skills
    router: README.md
    validators:
      - "python -c \\"print('epsilon ok')\\""
"""


class Builder:
    def __init__(self, dest: Path) -> None:
        self.dest = dest
        self.tick = 0
        self.config = dest / ".fixture.gitconfig"

    def env(self) -> dict[str, str]:
        self.tick += 1
        date = BASE_DATE.format(self.tick)
        env = dict(os.environ)
        env.update({
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(self.config),
            "GIT_AUTHOR_NAME": IDENTITY[0], "GIT_AUTHOR_EMAIL": IDENTITY[1],
            "GIT_COMMITTER_NAME": IDENTITY[0], "GIT_COMMITTER_EMAIL": IDENTITY[1],
            "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date,
        })
        return env

    def git(self, cwd: Path, *args: str) -> str:
        proc = subprocess.run(["git", *args], cwd=cwd, env=self.env(), capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {proc.stderr.strip()}")
        return proc.stdout.strip()

    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))

    def init_repo(self, name: str, files: dict[str, str]) -> Path:
        repo = self.dest / name
        repo.mkdir(parents=True)
        self.git(repo, "init", "-q", "-b", "main")
        self.git(repo, "config", "core.autocrlf", "false")
        self.git(repo, "config", "commit.gpgsign", "false")
        for rel, text in files.items():
            self.write(repo / rel, text)
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", f"{name} baseline")
        return repo

    def commit(self, repo: Path, rel: str, text: str, message: str) -> None:
        self.write(repo / rel, text)
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", message)

    def publish(self, repo: Path, remote_name: str) -> Path:
        bare = self.dest / "remotes" / f"{remote_name}.git"
        bare.parent.mkdir(parents=True, exist_ok=True)
        self.git(self.dest, "init", "-q", "--bare", "-b", "main", str(bare))
        url = bare.resolve().as_uri()  # file:///C:/.../remotes/<name>.git (forward slashes)
        self.git(repo, "remote", "add", "origin", url)
        self.git(repo, "push", "-q", "-u", "origin", "main")
        return bare

    def build(self) -> dict:
        self.dest.mkdir(parents=True, exist_ok=True)
        if any(p for p in self.dest.iterdir() if p.name != self.config.name):
            raise SystemExit(f"destination is not empty: {self.dest}")
        self.config.write_text("", encoding="utf-8")
        self.write(self.dest / "catalog" / "engines.yaml", CATALOG)
        router_files = {"AGENTS.md": "# Router\n", "CLAUDE.md": "# Claude bridge\n", "README.md": "# Engine\n"}

        alpha = self.init_repo("alpha-skills", {**router_files, "docs/guides/intro.md": "Intro\n"})
        alpha_bare = self.publish(alpha, "alpha-skills")
        # Advance the upstream by one commit from a helper clone, then fetch into alpha: behind 1.
        helper = self.dest / "remotes" / "alpha-helper"
        self.git(self.dest, "clone", "-q", alpha_bare.resolve().as_uri(), str(helper))
        self.git(helper, "config", "commit.gpgsign", "false")
        self.commit(helper, "docs/guides/next.md", "Next\n", "upstream addition")
        self.git(helper, "push", "-q", "origin", "main")
        self.git(alpha, "fetch", "-q", "origin")

        beta = self.init_repo("beta-skills", {"AGENTS.md": "# Router\n", "skills/one/SKILL.md": "---\nname: one\n---\n"})
        self.publish(beta, "beta-skills")
        self.write(beta / "skills" / "one" / "SKILL.md", "---\nname: one\n---\nUncommitted edit.\n")

        gamma = self.init_repo("gamma-skills", {"AGENTS.md": "# Router\n"})
        self.publish(gamma, "gamma-registry")
        self.commit(gamma, "skills/a.md", "a\n", "local one")
        self.commit(gamma, "skills/b.md", "b\n", "local two")

        epsilon = self.init_repo("epsilon-skills", {"README.md": "# Epsilon\n"})
        delta = self.init_repo("delta-notes", {"README.md": "# Notes\n"})

        heads = {name: self.git(repo, "rev-parse", "HEAD") for name, repo in
                 (("alpha-skills", alpha), ("beta-skills", beta), ("gamma-skills", gamma), ("epsilon-skills", epsilon), ("delta-notes", delta))}
        heads["alpha-skills@upstream"] = self.git(alpha, "rev-parse", "origin/main")
        build_hash = hashlib.sha256(json.dumps(heads, sort_keys=True).encode("utf-8")).hexdigest()
        self.config.unlink(missing_ok=True)
        return {"workspace": str(self.dest), "catalog": str(self.dest / "catalog" / "engines.yaml"), "heads": heads, "build_hash": build_hash}


def build(dest: Path) -> dict:
    return Builder(dest).build()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args(argv)
    print(json.dumps(build(args.dest), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
