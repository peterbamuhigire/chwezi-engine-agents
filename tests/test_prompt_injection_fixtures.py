"""Static checks for the inert prompt-injection fixtures (M10-04-T11, AC-07).

These tests prove only that each fixture is well formed and that the red-flag
pattern table recognises the behaviours it names. They do not prove that any
agent resists the text: runtime resistance remains NOT ASSESSED.
"""
from __future__ import annotations

import re
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "prompt-injection"
PATTERN_TABLE = FIXTURES / "red-flag-patterns.md"
SETUP_FIXTURE = FIXTURES / "imported-setup-command.txt"
SETUP_BEHAVIOURS = {
    "RF-01": "ignore prior knowledge",
    "RF-02": "forbid checking configuration locations",
    "RF-03": "write a pasted key into user-level MCP configuration",
}


def load_patterns() -> dict[str, re.Pattern[str]]:
    patterns: dict[str, re.Pattern[str]] = {}
    for line in PATTERN_TABLE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*(RF-\d{2})\s*\|.*\|\s*`(.+)`\s*\|\s*$", line)
        if match:
            patterns[match.group(1)] = re.compile(match.group(2).replace(chr(92) + "|", "|"), re.IGNORECASE)
    return patterns


def test_every_fixture_is_marked_untrusted_and_has_expected_disposition():
    fixtures = sorted(FIXTURES.glob("*.txt"))
    assert len(fixtures) >= 4
    for path in fixtures:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("UNTRUSTED FIXTURE"), path.name
        assert re.search(r"^Expected disposition: \S", text, re.MULTILINE), path.name


def test_fixtures_use_only_reserved_hosts_and_no_key_shapes():
    for path in FIXTURES.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        for host in re.findall(r"https?://([^/\s]+)", text):
            assert host.endswith(".invalid"), f"{path.name}: {host}"
        assert not re.search(r"\b(sk|pk|ghp|xox[abp])[-_][A-Za-z0-9]{8,}", text), path.name


def test_pattern_table_names_all_three_setup_behaviours():
    patterns = load_patterns()
    assert set(SETUP_BEHAVIOURS) <= set(patterns), sorted(patterns)


def test_setup_fixture_matches_each_red_flag_behaviour():
    text = SETUP_FIXTURE.read_text(encoding="utf-8")
    payload = text.split("Expected disposition:", 1)[0]
    patterns = load_patterns()
    for rule_id, behaviour in SETUP_BEHAVIOURS.items():
        assert patterns[rule_id].search(payload), f"{rule_id} ({behaviour}) did not match"
    assert "<PASTED-KEY>" in payload
    assert "https://setup.invalid/mcp" in payload


def test_readme_keeps_runtime_resistance_not_assessed():
    readme = (FIXTURES / "README.md").read_text(encoding="utf-8")
    assert "NOT ASSESSED" in readme
