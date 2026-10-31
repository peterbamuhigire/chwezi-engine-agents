#!/usr/bin/env python3
"""Seeded-failure tests for scripts/check_public_hygiene.py (pass-2 K2).

Every rule has a case that must fail and a near-miss that must pass. Credential-shaped and
path-shaped literals are assembled from fragments so this file does not itself trip the check.
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_public_hygiene", PACKAGE / "scripts" / "check_public_hygiene.py")
assert SPEC and SPEC.loader
H = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = H
SPEC.loader.exec_module(H)

AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"
GH_TOKEN = "ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"
PRIVATE_HEADER = "-----BEGIN RSA " + "PRIVATE KEY-----"
BASE64_BODY = "MIIEowIBAAKCAQEA" + "x7Qk3JvP9sLmN2bV8cZ4tYh1uWq5rEoD6fGa0XyIjKlMnOpQrStUvWxYz"
WEBROOT = "C:" + "\\wamp64\\www\\engine"
USER_WIN = "C:" + "\\Users\\Zed\\Downloads"
USER_WIN_PLACEHOLDER = "C:" + "\\Users\\<name>\\Downloads"
USER_WIN_EXAMPLE = "C:" + "\\Users\\Alice\\Downloads"
HOME_PRIVATE = "/home/" + "peter/.config"
HOME_EXAMPLE = "/home/" + "deploy/app"
HIGH_ENTROPY = "q8Zr3KpL0vXw9TnB2mYc7HdF5gJa4SeU"

POLICY = {
    "private_user_names": ["peter"],
    "record_globs": ["docs/**", "tests/**"],
    "repositories": {"demo": {"record_path_ceiling": 1}},
}


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


class HygieneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="hygiene-"))
        self.repo = self.tmp / "demo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        self.write("README.md", "# Demo\n\nNothing sensitive here.\n")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rel: str, content: str | bytes, track: bool = True) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
        if track:
            git(self.repo, "add", "--", rel)

    def scan(self, policy: dict | None = None) -> H.RepoResult:
        return H.scan_repo("demo", self.repo, POLICY if policy is None else policy)

    def rules(self, result: H.RepoResult) -> list[str]:
        return sorted(f.rule for f in result.findings)

    def test_clean_repository_passes(self) -> None:
        self.assertEqual(self.scan().findings, [])

    # tracked local settings and environment files
    def test_tracked_local_settings_file_fails(self) -> None:
        self.write(".claude/settings.local.json", '{"permissions": {"allow": []}}\n')
        self.assertEqual(self.rules(self.scan()), ["tracked-local-settings"])

    def test_untracked_local_settings_file_is_not_a_finding(self) -> None:
        self.write(".claude/settings.local.json", "{}\n", track=False)
        self.assertEqual(self.scan().findings, [])

    def test_paths_inside_a_tracked_settings_file_are_not_listed_one_by_one(self) -> None:
        self.write(".claude/settings.local.json", f'{{"allow": ["Read({USER_WIN})", "Read({USER_WIN}\\\\x)"]}}\n')
        self.assertEqual(self.rules(self.scan()), ["tracked-local-settings"])

    def test_env_file_fails_and_example_variants_pass(self) -> None:
        self.write(".env", "MODE=development\n")
        self.write("config/.env.production", "MODE=production\n")
        self.write(".env.example", "MODE=\n")
        self.write(".env.sample", "MODE=\n")
        result = self.scan()
        self.assertEqual(self.rules(result), ["tracked-env-file", "tracked-env-file"])
        self.assertEqual(sorted(f.path for f in result.findings), [".env", "config/.env.production"])

    def test_private_key_files_fail(self) -> None:
        self.write("deploy/id_ed25519", "not really a key\n")
        self.write("certs/site.pem", "not really a certificate\n")
        self.assertEqual(self.rules(self.scan()), ["tracked-env-file", "tracked-env-file"])

    # key-shaped strings
    def test_cloud_and_source_host_keys_fail_and_are_redacted(self) -> None:
        self.write("src/config.py", f'KEY = "{AWS_KEY}"\nTOKEN = "{GH_TOKEN}"\n')
        result = self.scan()
        self.assertEqual(self.rules(result), ["key-shaped-string", "key-shaped-string"])
        for finding in result.findings:
            self.assertNotIn(AWS_KEY, finding.detail)
            self.assertNotIn(GH_TOKEN, finding.detail)
        stream = io.StringIO()
        with redirect_stdout(stream):
            print(H.summarise([result], []))
        self.assertNotIn(AWS_KEY, stream.getvalue())
        self.assertNotIn(GH_TOKEN, stream.getvalue())

    def test_private_key_with_a_body_fails_but_a_quoted_header_passes(self) -> None:
        self.write("keys/leak.txt", f"{PRIVATE_HEADER}\n{BASE64_BODY}\n")
        self.write("docs/howto.md", f"Scanners look for the line `{PRIVATE_HEADER}` in a diff.\n")
        self.assertEqual([f.path for f in self.scan().findings], ["keys/leak.txt"])

    def test_high_entropy_assignment_fails_and_placeholders_pass(self) -> None:
        self.write("src/a.py", f'api_key = "{HIGH_ENTROPY}"\n')
        self.write("src/b.py", 'api_key = "your-api-key-goes-here-please"\npassword = "changeme-changeme-changeme"\n')
        self.write("src/c.py", 'password = data.vault_generic_secret.rds.data["password"]\ntoken = os.environ["API_TOKEN_VALUE_FOR_X"]\n')
        self.assertEqual([f.path for f in self.scan().findings], ["src/a.py"])

    def test_low_entropy_values_are_not_secrets(self) -> None:
        self.write("src/d.py", 'password = "mmmmmmmmmmnnnnnnnnnn1111"\n')
        self.assertEqual(self.scan().findings, [])

    # machine paths and user-profile paths
    def test_web_root_path_in_a_live_file_fails(self) -> None:
        self.write("AGENTS.md", f"Resolve engines under `{WEBROOT}`.\n")
        result = self.scan()
        self.assertEqual(self.rules(result), ["machine-path"])
        self.assertEqual((result.findings[0].path, result.findings[0].line), ("AGENTS.md", 1))

    def test_same_path_in_a_dated_record_is_counted_not_failed(self) -> None:
        self.write("docs/old-plan.md", f"Ran from {WEBROOT}.\n")
        result = self.scan()
        self.assertEqual(result.findings, [])
        self.assertEqual(result.record_path_lines, 1)

    def test_record_lines_over_the_ceiling_fail_and_at_the_ceiling_pass(self) -> None:
        self.write("docs/a.md", f"{WEBROOT}\n")
        self.assertEqual(self.scan().findings, [])
        self.write("docs/b.md", f"{WEBROOT}\n")
        self.assertEqual(self.rules(self.scan()), ["path-ceiling"])

    def test_user_profile_paths(self) -> None:
        self.write("README.md", f"Saved to {USER_WIN}.\n")
        self.write("scripts/run.sh", f"cd {HOME_PRIVATE}\n")
        self.assertEqual(self.rules(self.scan()), ["user-profile-path", "user-profile-path"])

    def test_placeholders_and_example_users_pass(self) -> None:
        self.write("README.md", f"Saved to {USER_WIN_PLACEHOLDER} or {USER_WIN_EXAMPLE} or {HOME_EXAMPLE}.\n")
        self.write("scripts/x.sh", "cd $HOME/work && ls /home/$USER\n")
        self.assertEqual(self.scan().findings, [])

    def test_standard_operating_system_folders_are_not_machine_paths(self) -> None:
        self.write("docs/win.md", "Run `C:" + "\\Windows\\System32\\whoami.exe` and open `C:" + "\\Program Files\\App`.\n")
        self.write("scripts/win.ps1", "$p = 'C:" + "\\Windows\\Temp'\n")
        self.assertEqual(self.scan().findings, [])

    # exceptions
    def test_allow_entry_with_a_reason_excuses_one_rule_on_one_path(self) -> None:
        self.write("scripts/guard.py", f"BAD = '{WEBROOT}'\n")
        policy = {**POLICY, "allow": [{"rule": "machine-path", "path": "scripts/guard.py", "reason": "guard code quotes the pattern it rejects"}]}
        self.assertEqual(self.scan(policy).findings, [])

    def test_allow_entry_without_a_reason_is_void(self) -> None:
        self.write("scripts/guard.py", f"BAD = '{WEBROOT}'\n")
        policy = {**POLICY, "allow": [{"rule": "machine-path", "path": "scripts/guard.py", "reason": " "}]}
        self.assertEqual(self.rules(self.scan(policy)), ["machine-path"])

    def test_allow_entry_never_excuses_a_different_rule(self) -> None:
        self.write("scripts/guard.py", f"KEY = '{AWS_KEY}'\n")
        policy = {**POLICY, "allow": [{"rule": "machine-path", "path": "scripts/guard.py", "reason": "guard code"}]}
        self.assertEqual(self.rules(self.scan(policy)), ["key-shaped-string"])

    def test_secrets_in_a_record_folder_still_fail(self) -> None:
        self.write("docs/notes.md", f"token {GH_TOKEN}\n")
        self.assertEqual(self.rules(self.scan()), ["key-shaped-string"])

    # file handling
    def test_binary_and_oversized_files_are_skipped(self) -> None:
        self.write("assets/blob.dat", b"\0\0\0" + WEBROOT.encode())
        self.write("assets/logo.png", WEBROOT.encode())
        self.assertEqual(self.scan().findings, [])


class CommandLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="hygiene-cli-"))
        self.package = self.tmp / "chwezi-engine-agents"
        (self.package / "catalog").mkdir(parents=True)
        (self.package / "catalog" / "engines.yaml").write_text(
            "engines:\n  - id: demo-engine\n    repository: demo-engine\n    path: demo-engine\n    aliases: [old-demo]\n", encoding="utf-8")
        (self.package / "catalog" / "hygiene-policy.yaml").write_text(yaml.safe_dump(POLICY), encoding="utf-8")
        git(self.tmp, "init", "-q", str(self.package))
        (self.package / "README.md").write_text("# Package\n", encoding="utf-8")
        git(self.package, "add", "--", "README.md")
        self.engine = self.tmp / "old-demo"
        self.engine.mkdir()
        git(self.engine, "init", "-q")
        (self.engine / "README.md").write_text("# Engine\n", encoding="utf-8")
        git(self.engine, "add", "--", "README.md")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_main(self, *args: str) -> tuple[int, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = H.main(["--package-root", str(self.package), "--workspace-root", str(self.tmp), *args])
        return code, stream.getvalue()

    def test_clean_portfolio_exits_zero_and_finds_the_engine_by_its_former_name(self) -> None:
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("checked 2 repositories", out)

    def test_a_planted_settings_file_makes_the_run_fail(self) -> None:
        (self.engine / ".claude").mkdir()
        (self.engine / ".claude" / "settings.local.json").write_text("{}\n", encoding="utf-8")
        git(self.engine, "add", "--", ".claude/settings.local.json")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("[tracked-local-settings]", out)

    def test_a_missing_engine_is_not_assessed_never_a_pass(self) -> None:
        shutil.rmtree(self.engine)
        code, out = self.run_main()
        self.assertEqual(code, 3)
        self.assertIn("NOT_ASSESSED demo-engine", out)
        self.assertNotIn(str(self.tmp), out)

    def test_json_output_has_no_secret_values(self) -> None:
        (self.engine / "x.py").write_text(f'K = "{AWS_KEY}"\n', encoding="utf-8")
        git(self.engine, "add", "--", "x.py")
        code, out = self.run_main("--json")
        self.assertEqual(code, 1)
        self.assertNotIn(AWS_KEY, out)
        self.assertEqual(json.loads(out)["results"][0]["findings"][0]["rule"], "key-shaped-string")

    def test_the_shipped_policy_loads_and_every_ceiling_is_an_integer(self) -> None:
        policy = H.load_policy(PACKAGE / "catalog" / "hygiene-policy.yaml")
        catalog = yaml.safe_load((PACKAGE / "catalog" / "engines.yaml").read_text(encoding="utf-8"))
        ids = {e["id"] for e in catalog["engines"]} | {"chwezi-engine-agents"}
        self.assertEqual(set(policy["repositories"]), ids)
        for name, item in policy["repositories"].items():
            self.assertIsInstance(item["record_path_ceiling"], int, name)
        for item in policy.get("allow", []):
            self.assertTrue(str(item.get("reason", "")).strip(), item)


if __name__ == "__main__":
    unittest.main()
