#!/usr/bin/env python3
"""Marketplace relevance signals stay within the documented limits (M10-03-T14).

Limits from https://code.claude.com/docs/en/plugins/relevance (accessed 29 Sep 2026): topic at most
64 characters; cwd and filesRead at most 10 patterns of 256 characters; cli at most 10 entries of
64 characters; hosts at most 20 entries of 128 characters; manifestDeps at most 10 entries.
"""

from __future__ import annotations

import json
from pathlib import Path

MARKETPLACE = Path(__file__).resolve().parents[1] / ".claude-plugin" / "marketplace.json"
LIMITS = {"cwd": (10, 256), "filesRead": (10, 256), "cli": (10, 64), "hosts": (20, 128)}


def test_every_domain_entry_carries_relevance_within_limits():
    plugins = json.loads(MARKETPLACE.read_text(encoding="utf-8"))["plugins"]
    domain = [entry for entry in plugins if entry["source"] not in ("./", ".")]
    assert len(domain) == 11
    for entry in domain:
        relevance = entry.get("relevance")
        assert isinstance(relevance, dict), entry["name"]
        assert 0 < len(relevance.get("topic", "")) <= 64
        signals = relevance.get("signals")
        assert isinstance(signals, dict) and signals, entry["name"]
        assert set(signals) <= set(LIMITS) | {"manifestDeps"}, entry["name"]
        for field, values in signals.items():
            count, length = LIMITS.get(field, (10, 256))
            assert 0 < len(values) <= count, (entry["name"], field)
            if field != "manifestDeps":
                assert all(isinstance(value, str) and 0 < len(value) <= length for value in values)
