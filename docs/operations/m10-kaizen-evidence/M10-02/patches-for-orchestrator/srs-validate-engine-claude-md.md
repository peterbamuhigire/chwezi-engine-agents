# srs-skills `scripts/validate_engine.py` — one-line follow-up for the SRS executor

After the M10-02-T02 bridge conversion, `validate_root_pathing()` (about line 42) still requires the
string `projects/<ProjectName>/` in `CLAUDE.md`. The text now lives in `AGENTS.md`, which `CLAUDE.md`
imports, so the check reports `CLAUDE.md missing required text: projects/<ProjectName>/`.

Fix (not applied by the M10-02 executor, because another executor holds `srs-skills/scripts/`):

```diff
-    for rel_path in ["README.md", "AGENTS.md", "CLAUDE.md"]:
+    for rel_path in ["README.md", "AGENTS.md"]:
```

The other three `validate_engine.py` findings concern `README.md` and pre-date the conversion.
