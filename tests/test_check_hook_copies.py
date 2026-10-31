#!/usr/bin/env python3
"""Seeded-failure tests for scripts/check_hook_copies.py (pass-2 K3)."""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_hook_copies", PACKAGE / "scripts" / "check_hook_copies.py")
assert SPEC and SPEC.loader
C = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = C
SPEC.loader.exec_module(C)

CONTENT = {name: f"// {name}\nconsole.log('ok');\n" for name in C.SHARED_FILES}


def put_hooks(directory: Path, overrides: dict[str, str] | None = None, skip: tuple[str, ...] = ()) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for name, text in CONTENT.items():
        if name in skip:
            continue
        (directory / name).write_bytes(((overrides or {}).get(name, text)).encode("utf-8"))


class HookCopyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="hook-copies-")).resolve()
        self.package = self.tmp / "chwezi-engine-agents"
        (self.package / "catalog").mkdir(parents=True)
        (self.package / "catalog" / "engines.yaml").write_text(
            "engines:\n  - id: alpha\n    repository: alpha\n    path: alpha\n"
            "  - id: beta\n    repository: beta\n    path: beta\n    aliases: [beta-old]\n", encoding="utf-8")
        put_hooks(self.package / "hooks")
        self.engines = self.tmp / "engines"
        put_hooks(self.engines / "alpha" / "hooks")
        put_hooks(self.engines / "beta-old" / "hooks")
        self.plugins = self.tmp / "plugins"
        put_hooks(self.plugins / "cache" / "m" / "alpha" / "1.0.0" / "hooks")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_check(self, plugin_dirs: list[Path] | None = None):
        roots = C.engine_roots.roots_from([self.engines])
        return C.run(self.package, roots, [self.plugins] if plugin_dirs is None else plugin_dirs)

    def run_main(self, *extra: str) -> tuple[int, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = C.main(["--package-root", str(self.package), "--engines-root", str(self.engines), "--plugins-dir", str(self.plugins), *extra])
        return code, stream.getvalue()

    def test_identical_copies_pass_and_the_renamed_engine_is_found(self) -> None:
        rows, not_assessed, _ = self.run_check()
        self.assertEqual([r.status for r in rows if r.status != "identical"], [])
        self.assertEqual(not_assessed, [])
        self.assertEqual({r.label for r in rows if r.kind == "engine"}, {"alpha", "beta"})
        self.assertEqual(self.run_main()[0], 0)

    def test_one_changed_byte_in_an_engine_copy_fails_and_names_the_engine(self) -> None:
        gate = self.engines / "alpha" / "hooks" / "destructive-bash-gate.js"
        gate.write_bytes(gate.read_bytes().replace(b"ok", b"no"))
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("[differs] engine alpha: destructive-bash-gate.js", out)

    def test_line_ending_only_difference_is_not_drift(self) -> None:
        gate = self.engines / "alpha" / "hooks" / "destructive-bash-gate.js"
        gate.write_bytes(gate.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.run_main()[0], 0)

    def test_a_missing_hook_file_in_an_engine_fails(self) -> None:
        (self.engines / "beta-old" / "hooks" / "plugin-hook-config.js").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("[missing] engine beta: plugin-hook-config.js", out)

    def test_a_stale_installed_copy_fails_even_when_every_repository_copy_is_clean(self) -> None:
        stale = self.plugins / "cache" / "m" / "alpha" / "1.0.0" / "hooks" / "destructive-bash-gate.js"
        stale.write_text("// an older version\n", encoding="utf-8")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("[differs] installed cache/m/alpha/1.0.0: destructive-bash-gate.js", out)

    def test_trashed_plugin_copies_are_ignored(self) -> None:
        put_hooks(self.plugins / ".trash" / "x" / "old" / "hooks", {"destructive-bash-gate.js": "// removed plugin\n"})
        self.assertEqual(self.run_main()[0], 0)

    def test_a_missing_engine_is_not_assessed_never_a_pass(self) -> None:
        shutil.rmtree(self.engines / "alpha")
        code, out = self.run_main()
        self.assertEqual(code, 3)
        self.assertIn("NOT_ASSESSED alpha", out)

    def test_drift_outranks_not_assessed(self) -> None:
        shutil.rmtree(self.engines / "alpha")
        (self.engines / "beta-old" / "hooks" / "destructive-bash-gate.js").write_text("// drifted\n", encoding="utf-8")
        self.assertEqual(self.run_main()[0], 1)

    def test_missing_canonical_file_fails(self) -> None:
        (self.package / "hooks" / "destructive-bash-gate.js").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("[missing] canonical chwezi-engine-agents: destructive-bash-gate.js", out)

    def test_no_plugin_directory_is_noted_not_failed(self) -> None:
        rows, _, notes = self.run_check(plugin_dirs=[])
        self.assertEqual([r for r in rows if r.status != "identical"], [])
        self.assertIn("installed copies: no plugin directory found, not compared", notes)

    def test_output_holds_no_absolute_path(self) -> None:
        (self.plugins / "cache" / "m" / "alpha" / "1.0.0" / "hooks" / "destructive-bash-gate.js").write_text("// old\n", encoding="utf-8")
        shutil.rmtree(self.engines / "alpha")
        for flag in ((), ("--json",)):
            _, out = self.run_main(*flag)
            self.assertNotIn(str(self.tmp), out)

    def test_json_output_is_machine_readable(self) -> None:
        code, out = self.run_main("--json")
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)["rows"]), 3 * len(C.SHARED_FILES))

    def test_the_four_shared_files_exist_in_this_package(self) -> None:
        for name in C.SHARED_FILES:
            self.assertTrue((PACKAGE / "hooks" / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
