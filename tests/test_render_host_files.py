#!/usr/bin/env python3
"""Seeded-failure tests for scripts/render_host_files.py (M10-02-T04/T05/T07)
and the --check-marketplace flag of scripts/generate-plugin-manifest.js (T09)."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "render_host_files.py"
SPEC = importlib.util.spec_from_file_location("render_host_files", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BRIDGE = "# Claude Code repository memory\n\n@AGENTS.md\n"
MARKER_START = "<!-- design-system-skills:trigger v3 -->"
MARKER_END = "<!-- /design-system-skills:trigger -->"
BLOCK = f"{MARKER_START}\n### Design\n\nConsult the design engine.\n{MARKER_END}\n"
AGENTS = (
    "# Engine\n\nUse British English for every output.\n\n"
    "Book extractions must never be stored in this repository.\n\n"
    "Missing evidence is `NOT ASSESSED`, never a pass.\n\n" + BLOCK
)
MANIFEST = """schema_version: "1.0"
engine_id: demo-engine
version: "1.2.3"
claude_only_block: |
  - Read SKILL.md files directly.
invariants:
  - id: british-english
    phrase: "Use British English for every output."
  - id: book-extraction-ban
    phrase: "Book extractions must never be stored in this repository."
  - id: not-assessed
    phrase: "Missing evidence is `NOT ASSESSED`, never a pass."
plugin_exclusions:
  - path: "templates/skill"
    reason: "authoring template"
"""
HOOKS = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
    {"type": "command", "command": 'node "${CLAUDE_PLUGIN_ROOT}/hooks/gate.js"', "timeout": 5}]}]}}
VARIANT = "print('variant')\n"
CORRUPT_ID = "Codex" + "-opus"  # built at runtime so this file never trips the scan itself


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_bytes(content.encode("utf-8"))


def build_workspace(root: Path) -> tuple[Path, Path]:
    package = root / "chwezi-engine-agents"
    engine = root / "demo-engine"
    # engine
    write(engine / "AGENTS.md", AGENTS)
    write(engine / "CLAUDE.md", BRIDGE + "\n## Claude-only notes\n\n- Read SKILL.md files directly.\n")
    write(engine / ".skills-engine" / "engine-manifest.yaml", MANIFEST)
    write(engine / "skills" / "one" / "SKILL.md", "---\nname: one\ndescription: Use when testing.\n---\n")
    write(engine / "templates" / "skill" / "SKILL.md", "---\nname: template\ndescription: Template.\n---\n")
    write(engine / ".claude-plugin" / "plugin.json", json.dumps({"name": "demo", "version": "1.2.3", "skills": ["./skills/one/"]}, indent=2) + "\n")
    write(engine / ".claude-plugin" / "marketplace.json", json.dumps({"name": "demo", "plugins": [
        {"name": "demo", "source": "./", "description": "1 skills for testing", "version": "1.2.3"}]}, indent=2) + "\n")
    write(engine / "hooks" / "hooks.json", json.dumps(HOOKS, indent=2) + "\n")
    write(engine / "hooks" / "gate.js", "// gate\n")
    write(engine / "hooks" / "shared.js", "// shared\n")
    write(engine / "scripts" / "variant.py", VARIANT)
    # package
    write(package / "AGENTS.md", AGENTS.replace("# Engine", "# Package"))
    write(package / "CLAUDE.md", BRIDGE)
    write(package / "hooks" / "shared.js", "// shared\n")
    write(package / "design-block.md", "intro\n" + BLOCK)
    write(package / "catalog" / "engines.yaml", "engines:\n  - id: demo-engine\n    repository: demo-engine\n    path: demo-engine\n")
    write(package / ".claude-plugin" / "plugin.json", json.dumps({"name": "chwezi-suite", "version": "2.0.0", "skills": []}, indent=2) + "\n")
    write(package / ".claude-plugin" / "marketplace.json", json.dumps({"name": "chwezi", "plugins": [
        {"name": "chwezi-suite", "source": "./", "description": "Coordination core.", "version": "2.0.0"},
        {"name": "demo", "source": {"source": "url", "url": "https://github.com/example/demo-engine.git", "ref": "main"},
         "description": "1 skills for testing", "version": "1.2.3"}]}, indent=2) + "\n")
    register = f"""schema_version: "1.0"
public_repositories: [chwezi-engine-agents, demo-engine]
coordination:
  invariants:
    - id: british-english
      phrase: "Use British English for every output."
    - id: book-extraction-ban
      phrase: "Book extractions must never be stored in this repository."
    - id: not-assessed
      phrase: "Missing evidence is `NOT ASSESSED`, never a pass."
assets:
  - id: shared-hook
    mode: byte
    canonical: chwezi-engine-agents/hooks/shared.js
    copies: [demo-engine/hooks/shared.js]
    reason: test
  - id: trigger
    mode: block
    canonical: chwezi-engine-agents/design-block.md
    markers: {{start: "{MARKER_START}", end: "{MARKER_END}"}}
    copies: [demo-engine/AGENTS.md, chwezi-engine-agents/AGENTS.md]
    reason: test
  - id: variant
    mode: registered-variant
    copies: [demo-engine/scripts/variant.py]
    discover: ["*/scripts/variant.py"]
    variants:
      demo-engine/scripts/variant.py: {{sha256: {sha(VARIANT)}, owner: demo-engine, reason: test}}
    reason: test
"""
    write(package / "catalog" / "shared-assets.yaml", register)
    return package, engine


class HostFileCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.package, self.engine = build_workspace(self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def check(self) -> tuple[int, set[str]]:
        report = MODULE.run_check(self.package, self.tmp, None, None)
        code = 1 if report.findings else (3 if report.not_assessed else 0)
        return code, {f.code for f in report.findings}

    def assert_seeded(self, expected_code: str) -> None:
        code, codes = self.check()
        self.assertEqual(code, 1, codes)
        self.assertIn(expected_code, codes)

    def test_clean_fixture_passes(self) -> None:
        self.assertEqual(self.check(), (0, set()))

    def test_drifted_claude_md(self) -> None:
        write(self.engine / "CLAUDE.md", BRIDGE + "\n## Routing\n\n- duplicated doctrine\n")
        self.assert_seeded("bridge-drift")

    def test_claude_md_differs_from_rendered_block(self) -> None:
        write(self.engine / "CLAUDE.md", BRIDGE + "\n## Claude-only notes\n\n- Hand-edited note.\n")
        self.assert_seeded("bridge-render-drift")

    def test_missing_canary(self) -> None:
        write(self.engine / "AGENTS.md", AGENTS.replace("Use British English for every output.", "Use plain English."))
        self.assert_seeded("invariant-missing")

    def test_undeclared_invariant(self) -> None:
        manifest = MANIFEST.replace('  - id: not-assessed\n    phrase: "Missing evidence is `NOT ASSESSED`, never a pass."\n', "")
        write(self.engine / ".skills-engine" / "engine-manifest.yaml", manifest)
        self.assert_seeded("invariant-undeclared")

    def test_mismatched_version(self) -> None:
        plugin = json.loads((self.engine / ".claude-plugin" / "plugin.json").read_text())
        plugin["version"] = "1.2.4"
        write(self.engine / ".claude-plugin" / "plugin.json", json.dumps(plugin, indent=2) + "\n")
        self.assert_seeded("version-mismatch")

    def test_tag_mismatch(self) -> None:
        report = MODULE.run_check(self.package, self.tmp, None, "v9.9.9")
        self.assertIn("version-tag-mismatch", {f.code for f in report.findings})

    def test_bom(self) -> None:
        write(self.engine / "skills" / "one" / "SKILL.md", b"\xef\xbb\xbf---\nname: one\ndescription: x\n---\n")
        self.assert_seeded("bom")

    def test_model_id_corruption(self) -> None:
        write(self.engine / "docs" / "note.md", f"Use {CORRUPT_ID}-4 for this.\n")
        self.assert_seeded("model-id-corruption")

    def set_hook(self, command: str) -> None:
        hooks = json.loads(json.dumps(HOOKS))
        hooks["hooks"]["PreToolUse"][0]["hooks"][0]["command"] = command
        write(self.engine / "hooks" / "hooks.json", json.dumps(hooks, indent=2))

    def test_single_quoted_plugin_root(self) -> None:
        self.set_hook("node '${CLAUDE_PLUGIN_ROOT}/hooks/gate.js'")
        self.assert_seeded("hook-single-quoted-root")

    def test_sh_hook_without_interpreter(self) -> None:
        write(self.engine / "hooks" / "gate.sh", "echo ok\n")
        self.set_hook('"${CLAUDE_PLUGIN_ROOT}/hooks/gate.sh"')
        self.assert_seeded("hook-bare-script")

    def test_heredoc_in_hook(self) -> None:
        self.set_hook('bash -c "cat <<EOF\nx\nEOF"')
        self.assert_seeded("hook-heredoc")

    def test_missing_hook_file(self) -> None:
        self.set_hook('node "${CLAUDE_PLUGIN_ROOT}/hooks/absent.js"')
        self.assert_seeded("hook-missing-file")

    def test_byte_drifted_shared_asset(self) -> None:
        write(self.engine / "hooks" / "shared.js", "// shared, edited\n")
        self.assert_seeded("shared-asset-byte-drift")

    def test_crlf_only_difference_is_not_drift(self) -> None:
        write(self.engine / "hooks" / "shared.js", b"// shared\r\n")
        self.assertEqual(self.check(), (0, set()))

    def test_block_drift(self) -> None:
        write(self.engine / "AGENTS.md", AGENTS.replace("Consult the design engine.", "Consult design."))
        self.assert_seeded("shared-asset-block-drift")

    def test_unregistered_variant(self) -> None:
        write(self.engine / "scripts" / "variant.py", VARIANT + "# local change\n")
        self.assert_seeded("shared-asset-unregistered-variant")

    def test_unregistered_copy_found_on_disk(self) -> None:
        write(self.package / "scripts" / "variant.py", VARIANT)
        self.assert_seeded("shared-asset-unregistered-copy")

    def test_unlisted_skill(self) -> None:
        write(self.engine / "skills" / "two" / "SKILL.md", "---\nname: two\ndescription: Use when testing.\n---\n")
        self.assert_seeded("plugin-unlisted-skill")

    def test_marketplace_count_drift(self) -> None:
        market = json.loads((self.engine / ".claude-plugin" / "marketplace.json").read_text())
        market["plugins"][0]["description"] = "7 skills for testing"
        write(self.engine / ".claude-plugin" / "marketplace.json", json.dumps(market, indent=2))
        self.assert_seeded("marketplace-count-drift")

    def test_missing_sibling_is_not_assessed(self) -> None:
        shutil.rmtree(self.engine)
        report = MODULE.run_check(self.package, self.tmp, None, None)
        self.assertEqual(report.findings, [])
        self.assertEqual([item["engine"] for item in report.not_assessed], ["demo-engine"])
        self.assertEqual(MODULE.main(["--check", "--workspace-root", str(self.tmp), "--package-root", str(self.package)]), 3)

    def test_exit_codes(self) -> None:
        args = ["--check", "--workspace-root", str(self.tmp), "--package-root", str(self.package)]
        self.assertEqual(MODULE.main(args), 0)
        write(self.engine / "CLAUDE.md", "# Old router\n")
        self.assertEqual(MODULE.main(args), 1)


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.package, self.engine = build_workspace(self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_render_is_idempotent_on_clean_engine(self) -> None:
        self.assertEqual(MODULE.render_engine(self.engine), (0, []))

    def test_render_restores_hand_edited_fields_and_check_catches_them(self) -> None:
        plugin_path = self.engine / ".claude-plugin" / "plugin.json"
        plugin_path.write_text(plugin_path.read_text().replace('"1.2.3"', '"0.0.1"'))
        market_path = self.engine / ".claude-plugin" / "marketplace.json"
        market_path.write_text(market_path.read_text().replace('"1 skills for testing"', '"9 skills for testing"'))
        write(self.engine / "CLAUDE.md", BRIDGE)
        codes = {f.code for f in MODULE.run_check(self.package, self.tmp, None, None).findings}
        self.assertTrue({"version-mismatch", "marketplace-count-drift", "bridge-render-drift"} <= codes, codes)
        code, changed = MODULE.render_engine(self.engine)
        self.assertEqual(code, 0)
        self.assertEqual(sorted(changed), [".claude-plugin/marketplace.json", ".claude-plugin/plugin.json", "CLAUDE.md"])
        self.assertEqual(MODULE.render_engine(self.engine), (0, []))
        self.assertEqual(MODULE.run_check(self.package, self.tmp, None, None).findings, [])

    def test_render_never_touches_agents_or_skills(self) -> None:
        before = {p: p.read_bytes() for p in (self.engine / "AGENTS.md", self.engine / "skills" / "one" / "SKILL.md")}
        write(self.engine / "CLAUDE.md", "# drifted\n")
        MODULE.render_engine(self.engine)
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data)

    def test_malformed_manifest_writes_nothing(self) -> None:
        write(self.engine / ".skills-engine" / "engine-manifest.yaml", "version: [unclosed\n")
        write(self.engine / "CLAUDE.md", "# drifted\n")
        code, changed = MODULE.render_engine(self.engine)
        self.assertEqual((code, changed), (1, []))
        self.assertEqual((self.engine / "CLAUDE.md").read_text(), "# drifted\n")


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class MarketplaceFlagTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.package, self.engine = build_workspace(self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_node(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["node", str(PACKAGE / "scripts" / "generate-plugin-manifest.js"), "--check-marketplace",
             "--workspace-root", str(self.tmp), "--suite-root", str(self.package)],
            capture_output=True, text=True, check=False,
        )

    def test_consistent_counts_pass(self) -> None:
        result = self.run_node()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_count_drift_fails(self) -> None:
        path = self.package / ".claude-plugin" / "marketplace.json"
        path.write_text(path.read_text().replace('"1 skills for testing"', '"5 skills for testing"'))
        result = self.run_node()
        self.assertEqual(result.returncode, 1)
        self.assertIn("description says 5 skills", result.stderr)

    def test_missing_relative_source_fails(self) -> None:
        path = self.engine / ".claude-plugin" / "marketplace.json"
        path.write_text(path.read_text().replace('"source": "./"', '"source": "./missing-plugin"'))
        result = self.run_node()
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not exist", result.stderr)

    def test_missing_sibling_is_not_assessed(self) -> None:
        shutil.rmtree(self.engine)
        result = self.run_node()
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
