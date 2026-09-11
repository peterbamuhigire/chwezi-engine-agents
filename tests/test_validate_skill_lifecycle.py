import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate-skill-lifecycle.py"
SPEC = importlib.util.spec_from_file_location("skill_lifecycle", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def write_skill(root: Path, name: str, metadata: str = "", description: str = "Use when testing a lifecycle fixture."):
    directory = root / name
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\nmetadata:\n  portable: true\n{metadata}---\n# Fixture\n",
        encoding="utf-8",
    )
    return directory


def test_promoted_default_and_explicit_contract(tmp_path):
    root = tmp_path / "skills"
    write_skill(root, "normal")
    write_skill(root, "manual", "  invocation: explicit\n", "Use when the user explicitly requests manual setup.")
    assert MODULE.inspect_root(root) == []


def test_non_promoted_skill_is_rejected_from_runtime_root(tmp_path):
    root = tmp_path / "skills"
    write_skill(root, "draft", "  lifecycle: experimental\n")
    assert any("exposed through a promoted runtime root" in item for item in MODULE.inspect_root(root))


def test_invalid_invocation_and_hidden_explicit_trigger_fail(tmp_path):
    root = tmp_path / "skills"
    write_skill(root, "invalid", "  invocation: automatic\n")
    write_skill(root, "hidden", "  invocation: explicit\n")
    findings = MODULE.inspect_root(root)
    assert any("unsupported invocation" in item for item in findings)
    assert any("explicit invocation is not stated" in item for item in findings)


def test_alias_cannot_coexist_with_active_skill(tmp_path):
    root = tmp_path / "skills"
    directory = write_skill(root, "duplicate")
    (directory / "ALIAS.md").write_text("# Alias\n", encoding="utf-8")
    assert any("cannot both be exposed" in item for item in MODULE.inspect_root(root))
