#!/usr/bin/env python3
"""Validate YAML or JSON instances against repository JSON Schemas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_yaml_or_json(path: Path) -> Any:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("PyYAML is unavailable") from exc
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def error_path(error: Any) -> str:
    parts = [str(part) for part in error.absolute_path]
    return ".".join(parts) if parts else "<root>"


def validate_catalog(instance: Any) -> list[str]:
    errors: list[str] = []
    engines = instance.get("engines", []) if isinstance(instance, dict) else []
    ids = [engine.get("id") for engine in engines if isinstance(engine, dict)]
    duplicates = sorted({engine_id for engine_id in ids if ids.count(engine_id) > 1})
    if duplicates:
        errors.append(f"<root>: duplicate engine IDs: {', '.join(duplicates)}")
    for index, engine in enumerate(engines):
        if not isinstance(engine, dict):
            continue
        for field in ("path", "router"):
            value = engine.get(field)
            if isinstance(value, str) and (Path(value).is_absolute() or ".." in Path(value).parts):
                errors.append(f"engines.{index}.{field}: path must be relative and stay within the checkout")
        repository = engine.get("repository")
        if isinstance(repository, str) and not re.fullmatch(r"[A-Za-z0-9_.-]+", repository):
            errors.append(f"engines.{index}.repository: invalid repository identifier")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--instance", required=True, type=Path)
    args = parser.parse_args()
    if not args.schema.is_file() or not args.instance.is_file():
        missing = args.schema if not args.schema.is_file() else args.instance
        print(f"NOT ASSESSED: missing file {missing}", file=sys.stderr)
        return 3
    try:
        from jsonschema import Draft202012Validator

        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        instance = load_yaml_or_json(args.instance)
        validator = Draft202012Validator(schema)
        failures = sorted(validator.iter_errors(instance), key=lambda error: (list(error.absolute_path), error.message))
        failures_text = [f"{error_path(error)}: {error.message}" for error in failures]
        if args.schema.name == "engine-catalog.schema.json" and not failures:
            failures_text.extend(validate_catalog(instance))
    except (ImportError, ModuleNotFoundError) as exc:
        print(f"NOT ASSESSED: dependency unavailable: {exc}", file=sys.stderr)
        return 3
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"INVALID: schema={args.schema} instance={args.instance}: {exc}", file=sys.stderr)
        return 2
    if failures_text:
        print(f"FAIL: schema={args.schema} instance={args.instance}")
        for failure in failures_text:
            print(f"- {failure}")
        return 2
    print(f"PASS: schema={args.schema} instance={args.instance}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
