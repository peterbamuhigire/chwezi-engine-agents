#!/usr/bin/env python3
"""Seeded-failure tests for scripts/check_readme_contract.py (README kaizen, 31 October 2026)."""

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
SPEC = importlib.util.spec_from_file_location("check_readme_contract", PACKAGE / "scripts" / "check_readme_contract.py")
assert SPEC and SPEC.loader
C = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = C
SPEC.loader.exec_module(C)

GOOD = "# Alpha\n\n## At a glance\n\n## Start here\n\n## Capabilities\n\nText.\n\n## How it works\n"


class ReadmeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="readme-contract-")).resolve()
        self.package = self.tmp / "chwezi-engine-agents"
        (self.package / "catalog").mkdir(parents=True)
        (self.package / "catalog" / "engines.yaml").write_text(
            "engines:\n  - id: alpha\n    repository: alpha\n    path: alpha\n"
            "  - id: beta\n    repository: beta\n    path: beta\n    aliases: [beta-old]\n", encoding="utf-8")
        self.engines = self.tmp / "engines"
        self.write("alpha", GOOD)
        self.write("beta-old", GOOD)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, folder: str, text: str, newline: str = "\n") -> None:
        directory = self.engines / folder
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "README.md").write_bytes(text.replace("\n", newline).encode("utf-8"))

    def main(self, *extra: str) -> tuple[int, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = C.main(["--package-root", str(self.package), "--engines-root", str(self.engines), *extra])
        return code, stream.getvalue()

    def test_a_capabilities_heading_in_the_lead_passes_and_the_renamed_engine_is_found(self) -> None:
        code, out = self.main()
        self.assertEqual(code, 0, out)
        self.assertIn("checked 2 engine READMEs; findings 0; not assessed 0", out)

    def test_capability_map_is_accepted_too(self) -> None:
        self.write("alpha", GOOD.replace("## Capabilities", "## Capability map"))
        self.assertEqual(self.main()[0], 0)

    def test_case_is_ignored_as_the_powershell_in_operator_ignores_it(self) -> None:
        self.write("alpha", GOOD.replace("## Capabilities", "## capabilities"))
        self.assertEqual(self.main()[0], 0)

    def test_the_heading_as_the_fifth_h2_fails_and_names_the_engine(self) -> None:
        text = "# Alpha\n\n## One\n\n## Two\n\n## Three\n\n## Four\n\n## Capabilities\n"
        self.write("alpha", text)
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn("[capabilities-in-lead-h2] alpha:", out)
        self.assertIn("One | ## Two | ## Three | ## Four", out.replace("## One", "One"))

    def test_the_heading_as_the_fourth_h2_passes(self) -> None:
        self.write("alpha", "## One\n\n## Two\n\n## Three\n\n## Capabilities\n\n## Five\n")
        self.assertEqual(self.main()[0], 0)

    def test_an_h3_is_not_a_capabilities_heading(self) -> None:
        self.write("alpha", "## One\n\n### Capabilities\n\n## Two\n")
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn("alpha", out)

    def test_a_longer_heading_is_not_accepted(self) -> None:
        self.write("alpha", "## One\n\n## Capabilities and limits\n")
        self.assertEqual(self.main()[0], 1)

    def test_trailing_spaces_fail_exactly_as_in_the_powershell_comparison(self) -> None:
        self.write("alpha", "## One\n\n## Capabilities \n")
        self.assertEqual(self.main()[0], 1)

    def test_crlf_line_endings_and_a_byte_order_mark_do_not_matter(self) -> None:
        self.write("alpha", GOOD, newline="\r\n")
        (self.engines / "beta-old" / "README.md").write_bytes(b"\xef\xbb\xbf" + GOOD.encode("utf-8"))
        self.assertEqual(self.main()[0], 0)

    def test_a_byte_order_mark_before_a_heading_on_the_first_line_does_not_hide_it(self) -> None:
        (self.engines / "alpha" / "README.md").write_bytes(b"\xef\xbb\xbf## Capabilities\n\n## Two\n")
        self.assertEqual(self.main()[0], 0)

    def test_a_fenced_line_counts_as_an_h2_as_the_powershell_rule_reads_it(self) -> None:
        text = "## One\n\n```text\n## Two\n## Three\n## Four\n```\n\n## Capabilities\n"
        self.write("alpha", text)
        self.assertEqual(self.main()[0], 1)

    def test_a_readme_with_no_h2_headings_fails_with_a_clear_message(self) -> None:
        self.write("alpha", "# Alpha\n\nJust text.\n")
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn("found: no H2 headings", out)

    def test_a_missing_readme_fails(self) -> None:
        (self.engines / "alpha" / "README.md").unlink()
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn("[readme-missing] alpha", out)

    def test_a_missing_engine_checkout_is_not_assessed_and_never_a_pass(self) -> None:
        shutil.rmtree(self.engines / "beta-old")
        code, out = self.main()
        self.assertEqual(code, 3)
        self.assertIn("NOT_ASSESSED beta", out)

    def test_a_failure_wins_over_not_assessed(self) -> None:
        shutil.rmtree(self.engines / "beta-old")
        self.write("alpha", "## One\n")
        self.assertEqual(self.main()[0], 1)

    def test_json_output_lists_findings_and_the_count_checked(self) -> None:
        self.write("alpha", "## One\n")
        code, out = self.main("--json")
        self.assertEqual(code, 1)
        data = json.loads(out)
        self.assertEqual(data["checked"], 2)
        self.assertEqual([f["engine"] for f in data["findings"]], ["alpha"])

    def test_output_contains_no_absolute_path(self) -> None:
        self.write("alpha", "## One\n")
        _, out = self.main()
        self.assertNotIn(str(self.tmp), out)


if __name__ == "__main__":
    unittest.main()
