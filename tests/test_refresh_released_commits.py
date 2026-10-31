#!/usr/bin/env python3
"""Seeded-failure tests for scripts/refresh_released_commits.py and the pin rule of
scripts/render_host_files.py (pass-2 K4). Engines are real throw-away git repositories."""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, PACKAGE / rel)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R = load("refresh_released_commits", "scripts/refresh_released_commits.py")
RC = R.RC
H = load("render_host_files_pins", "scripts/render_host_files.py")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=root,
                            check=True, capture_output=True, text=True)
    return result.stdout.strip()


def make_repo(path: Path, commits: int, branch: str = "main") -> list[str]:
    path.mkdir(parents=True)
    git(path, "init", "-q", "-b", branch)
    shas = []
    for number in range(commits):
        (path / "f.txt").write_text(f"{path.name} {number}\n", encoding="utf-8")
        git(path, "add", "--", "f.txt")
        git(path, "commit", "-q", "-m", f"{path.name} c{number}")
        shas.append(git(path, "rev-parse", "--short=7", "HEAD"))
    return shas


CATALOG = """# Catalogue fixture: comments and flow style must survive a rewrite.
schema_version: "1.0"
version: 1
engines:
  - id: alpha
    repository: alpha
    path: alpha
    router: AGENTS.md
    integration: {manifest: .skills-engine/engine-manifest.yaml, contract_version: "1.0", status: available, released_commit: "%s"}
    validators:
      - "python x.py"
  - id: beta
    repository: beta
    path: beta
    aliases: [beta-old]
    router: AGENTS.md
    integration: {manifest: .skills-engine/engine-manifest.yaml, contract_version: "1.0", status: available, released_commit: "%s"}
    validators:
      - "python y.py"
"""


class RefreshTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="pins-")).resolve()
        self.engines = self.tmp / "engines"
        self.engines.mkdir()
        self.alpha = make_repo(self.engines / "alpha", 3)
        self.beta = make_repo(self.engines / "beta-old", 2)
        self.package = self.tmp / "chwezi-engine-agents"
        (self.package / "catalog").mkdir(parents=True)
        self.catalog = self.package / "catalog" / "engines.yaml"
        self.catalog.write_text(CATALOG % (self.alpha[0], self.beta[0]), encoding="utf-8", newline="")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_main(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = R.main(["--package-root", str(self.package), "--workspace-root", str(self.tmp), "--engines-root", str(self.engines), *args])
        return code, out.getvalue(), err.getvalue()

    def pins(self) -> dict[str, str]:
        data = yaml.safe_load(self.catalog.read_text(encoding="utf-8"))
        return {e["id"]: e["integration"]["released_commit"] for e in data["engines"]}

    def test_check_reports_how_far_each_pin_lags(self) -> None:
        code, out, _ = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn(f"alpha: pin {self.alpha[0]} is 2 commits behind HEAD {self.alpha[2]}", out)
        self.assertIn(f"beta: pin {self.beta[0]} is 1 commits behind HEAD {self.beta[1]}", out)
        self.assertNotIn(str(self.tmp), out)

    def test_check_passes_when_every_pin_is_head(self) -> None:
        self.catalog.write_text(CATALOG % (self.alpha[2], self.beta[1]), encoding="utf-8")
        self.assertEqual(self.run_main()[0], 0)

    def test_write_updates_only_the_pin_values_and_keeps_comments_and_quoting(self) -> None:
        before = self.catalog.read_text(encoding="utf-8")
        code, out, _ = self.run_main("--write")
        self.assertEqual(code, 0, out)
        after = self.catalog.read_text(encoding="utf-8")
        self.assertEqual(after, before.replace(self.alpha[0], self.alpha[2]).replace(self.beta[0], self.beta[1]))
        self.assertEqual(self.pins(), {"alpha": self.alpha[2], "beta": self.beta[1]})
        self.assertTrue(after.startswith("# Catalogue fixture"))

    def test_write_is_idempotent_and_the_check_then_passes(self) -> None:
        self.run_main("--write")
        first = self.catalog.read_bytes()
        code, out, _ = self.run_main("--write")
        self.assertEqual(code, 0)
        self.assertIn("nothing to change", out)
        self.assertEqual(self.catalog.read_bytes(), first)
        self.assertEqual(self.run_main()[0], 0)

    def test_crlf_line_endings_are_preserved(self) -> None:
        self.catalog.write_bytes((CATALOG % (self.alpha[0], self.beta[0])).replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(self.run_main("--write")[0], 0)
        data = self.catalog.read_bytes()
        self.assertEqual(data.count(b"\r\n"), data.count(b"\n"))
        self.assertIn(self.alpha[2].encode(), data)

    def test_a_modified_tracked_file_refuses_and_writes_nothing(self) -> None:
        (self.engines / "alpha" / "f.txt").write_text("local edit\n", encoding="utf-8")
        before = self.catalog.read_bytes()
        code, out, _ = self.run_main("--write")
        self.assertEqual(code, 2)
        self.assertIn("alpha: pin", out)
        self.assertIn("working tree is not clean", out)
        self.assertEqual(self.catalog.read_bytes(), before)

    def test_an_untracked_file_refuses_and_writes_nothing(self) -> None:
        (self.engines / "beta-old" / "scratch.txt").write_text("x\n", encoding="utf-8")
        before = self.catalog.read_bytes()
        self.assertEqual(self.run_main("--write")[0], 2)
        self.assertEqual(self.catalog.read_bytes(), before)

    def test_an_ignored_file_does_not_block(self) -> None:
        (self.engines / "alpha" / ".gitignore").write_text("*.log\n", encoding="utf-8")
        git(self.engines / "alpha", "add", "--", ".gitignore")
        git(self.engines / "alpha", "commit", "-q", "-m", "ignore logs")
        (self.engines / "alpha" / "run.log").write_text("noise\n", encoding="utf-8")
        self.assertEqual(self.run_main("--write")[0], 0)

    def test_a_missing_engine_refuses_and_writes_nothing(self) -> None:
        shutil.rmtree(self.engines / "alpha")
        before = self.catalog.read_bytes()
        code, out, _ = self.run_main("--write")
        self.assertEqual(code, 2)
        self.assertIn("alpha:", out)
        self.assertEqual(self.catalog.read_bytes(), before)
        self.assertNotIn(str(self.tmp), out)

    def test_check_mode_reports_a_missing_engine_as_not_assessed(self) -> None:
        shutil.rmtree(self.engines / "alpha")
        self.assertEqual(self.run_main()[0], 3)

    def test_a_feature_branch_is_refused_unless_allowed(self) -> None:
        git(self.engines / "alpha", "switch", "-q", "-c", "kaizen/test")
        before = self.catalog.read_bytes()
        code, out, _ = self.run_main("--write")
        self.assertEqual(code, 2)
        self.assertIn("branch is kaizen/test, not main", out)
        self.assertEqual(self.catalog.read_bytes(), before)
        self.assertEqual(self.run_main("--write", "--any-branch")[0], 0)

    def test_a_stale_copy_under_the_old_name_is_ambiguous_and_refused(self) -> None:
        make_repo(self.engines / "beta", 1)
        before = self.catalog.read_bytes()
        code, out, _ = self.run_main("--write")
        self.assertEqual(code, 2)
        self.assertIn("ambiguous", out)
        self.assertEqual(self.catalog.read_bytes(), before)

    def test_an_engine_without_a_pin_field_makes_the_rewrite_refuse(self) -> None:
        text = (CATALOG % (self.alpha[0], self.beta[0])).replace(', released_commit: "%s"' % self.beta[0], "")
        self.catalog.write_text(text, encoding="utf-8")
        before = self.catalog.read_bytes()
        code, _, err = self.run_main("--write")
        self.assertEqual(code, 2)
        self.assertIn("beta", err)
        self.assertEqual(self.catalog.read_bytes(), before)

    def test_json_output(self) -> None:
        code, out, _ = self.run_main("--json")
        self.assertEqual(code, 1)
        self.assertEqual([r["engine"] for r in json.loads(out)["engines"]], ["alpha", "beta"])


class PinRuleInDriftCheckTests(unittest.TestCase):
    """The drift check reports pin lag through the same git facts."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="pins-drift-")).resolve()
        self.engine = self.tmp / "demo"
        self.shas = make_repo(self.engine, 4)
        self.engine_obj = H.Engine("demo", self.engine, "demo")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def codes(self, pin: str | None, lag_max: int = 0) -> list[str]:
        report = H.Report()
        H.check_released_commit(self.engine_obj, pin, lag_max, report)
        return [f.code for f in report.findings]

    def test_pin_at_head_passes(self) -> None:
        self.assertEqual(self.codes(self.shas[3]), [])

    def test_lagging_pin_is_a_finding_and_the_allowance_excuses_it(self) -> None:
        self.assertEqual(self.codes(self.shas[0]), ["released-commit-lag"])
        self.assertEqual(self.codes(self.shas[0], lag_max=3), [])
        self.assertEqual(self.codes(self.shas[0], lag_max=2), ["released-commit-lag"])

    def test_a_pin_that_is_not_in_the_history_is_a_finding(self) -> None:
        self.assertEqual(self.codes("0000000"), ["released-commit-unknown"])

    def test_a_pin_on_another_line_of_history_is_diverged(self) -> None:
        git(self.engine, "switch", "-q", "-c", "side", self.shas[0])
        (self.engine / "g.txt").write_text("side\n", encoding="utf-8")
        git(self.engine, "add", "--", "g.txt")
        git(self.engine, "commit", "-q", "-m", "side")
        side = git(self.engine, "rev-parse", "--short=7", "HEAD")
        git(self.engine, "switch", "-q", "main")
        self.assertEqual(self.codes(side), ["released-commit-diverged"])

    def test_shallow_clone_lacking_the_pin_is_skipped_not_guessed(self) -> None:
        clone = self.tmp / "clone"
        subprocess.run(["git", "clone", "-q", "--depth", "1", self.engine.as_uri(), str(clone)], check=True, capture_output=True)
        report = H.Report()
        H.check_released_commit(H.Engine("demo", clone, "demo"), self.shas[0], 0, report)
        self.assertEqual(report.findings, [])

    def test_no_pin_or_a_non_repository_is_skipped(self) -> None:
        self.assertEqual(self.codes(None), [])
        plain = self.tmp / "plain"
        plain.mkdir()
        report = H.Report()
        H.check_released_commit(H.Engine("demo", plain, "demo"), self.shas[0], 0, report)
        self.assertEqual(report.findings, [])

    def test_coordination_package_is_never_pinned(self) -> None:
        report = H.Report()
        H.check_released_commit(H.Engine("chwezi-engine-agents", self.engine, "x", coordination=True), self.shas[0], 0, report)
        self.assertEqual(report.findings, [])


if __name__ == "__main__":
    unittest.main()
