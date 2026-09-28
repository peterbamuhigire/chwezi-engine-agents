import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "evals/runners/run-contract-evals.py"
SPEC = importlib.util.spec_from_file_location("run_contract_evals", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CASES = Path(__file__).resolve().parents[1] / "evals/cases"


def write_case(directory: Path, case_id: str, fixture_path: str) -> Path:
    path = directory / f"{case_id}.yaml"
    path.write_text(
        f'schema_version: "1.0"\nid: {case_id}\ntask: Route requirements work\nfixture_path: {fixture_path}\n'
        "required_observations:\n  - catalog entry\nforbidden_actions:\n  - invent_engine\n"
        "expected_verdict: PASS\nevidence_fields:\n  - command\n",
        encoding="utf-8",
    )
    return path


def test_every_live_case_has_a_materialised_fixture():
    reports = [MODULE.evaluate(path) for path in sorted(CASES.glob("*.yaml"))]
    assert len(reports) >= MODULE.MIN_CASES
    assert [report for report in reports if report["status"] != "PASS"] == []


def test_missing_fixture_path_fails(tmp_path):
    report = MODULE.evaluate(write_case(tmp_path, "999-missing", "evals/fixtures/999-does-not-exist"))
    assert report["status"] == "FAIL"
    assert "does not exist" in report["evidence"]


def test_comma_joined_fixture_path_fails(tmp_path):
    report = MODULE.evaluate(write_case(tmp_path, "998-comma", "evals/fixtures/srs-skills,design-system-skills"))
    assert report["status"] == "FAIL"
    assert "single directory" in report["evidence"]


def test_fixture_that_disagrees_with_case_fails(tmp_path):
    # 001's fixture declares case_id 001-route-srs, so a case with another id must not borrow it.
    report = MODULE.evaluate(write_case(tmp_path, "997-borrowed", "evals/fixtures/001-route-srs"))
    assert report["status"] == "FAIL"
    assert "case_id does not match" in report["evidence"]
