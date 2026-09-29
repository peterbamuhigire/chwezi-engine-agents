#!/usr/bin/env python3
"""Skill-graph spike (M10-12-T08, GR-01). Report-only; never a router, loader or gate (P04).

Nodes: engine, router, skill. Edges carry provenance:
  EXTRACTED  links_to (Markdown link), routes_to (router lists the skill), alias_of (alias registry)
  INFERRED   mentions (exact slug), defers_to (slug on a line with a hand-off phrase)
  AMBIGUOUS  similar_trigger (cross-engine union TF-IDF pair >= 0.75, M10-03 lexical_routing)

Report: most-deferred-to skills, cross-engine bridges, heavily mentioned but unrouted skills,
mentions of retired aliases, and mentions of non-existent skills or engines (with path:line).
Never invents an edge: every edge names the file that produced it. Shrink guard: refuses to
overwrite a previous graph whose edge count would fall by more than 20 % unless --allow-shrink.

Provenance-tagged edges, the never-invent-an-edge rule and the shrink guard are adapted from
Graphify-Labs/graphify (Apache-2.0, https://github.com/Graphify-Labs/graphify, commit
d6eaa8aae8df155874ebb1044302c055c286342a); no code is copied. Standard library plus the
package's own modules (skill_fanin, lexical_routing) only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, PACKAGE_ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


FANIN = load("skill_fanin")
LEX = load("lexical_routing")

DEFER_RE = re.compile(r"\b(defer(s|red)? to|hand(s)? (off|over) to|route(s|d)? (it |this |work )?to|owned by|belongs? (to|in)|use .{0,40} instead|see also)\b", re.I)
SKILL_PATH_RE = re.compile(r"(?<![\w./-])((?:[a-z0-9-]+/)?skills/(?:[a-z0-9-]+/){1,3}[a-z0-9-]+)(?:/SKILL\.md)?(?![\w.-])")
RENAMED_ENGINES = {"skills-web-dev": "chwezi-dev-engine"}
RETIREMENT_WORDS = re.compile(r"alias|retired|migrated|inactive|redirect|superseded|merged into|absorbed|deprecated", re.I)
FOLDER_ONLY = {"digital-research-skills": "digital-research-engine"}  # catalogue id is valid; a folder path is not


def GENERATOR_HEAD(root: Path) -> str:
    import subprocess
    try:
        return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True,
                              timeout=20, check=False).stdout.strip() or "not-a-git-checkout"
    except (OSError, subprocess.SubprocessError):
        return "not-a-git-checkout"


def dump_compact(graph: dict) -> str:
    """One node and one edge per line, so diffs stay readable and the file stays small."""
    head = {k: v for k, v in graph.items() if k not in {"nodes", "edges"}}
    lines = ["{"]
    for key, value in sorted(head.items()):
        lines.append(f"{json.dumps(key)}: {json.dumps(value, sort_keys=True)},")
    lines.append('"nodes": [')
    lines.append(",\n".join(json.dumps(n) for n in graph["nodes"]))
    lines.append("],")
    lines.append('"edges": [')
    lines.append(",\n".join(json.dumps(e, separators=(",", ":")) for e in graph["edges"]))
    lines.append("]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def lines_of(path: Path) -> list[str]:
    return FANIN.read_text(path).split("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report-only skill graph spike (GR-01).")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--inventory", type=Path, default=FANIN.DEFAULT_INVENTORY,
                        help="P01 inventory (accepted for the phase command; reachability is not recomputed)")
    parser.add_argument("--engine", action="append", default=[], help="Engine folder (repeatable; default: all catalogued)")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--allow-shrink", action="store_true")
    parser.add_argument("--report", type=Path, help="Report path (default: <out>/skill-graph-report.json)")
    args = parser.parse_args(argv)
    ws = args.workspace_root.resolve()
    folders = sorted(args.engine) if args.engine else sorted(FANIN.catalog_paths(ws))
    for folder in folders:
        FANIN.refuse_private(folder)
    roots = {f: (ws / f).resolve() for f in folders if (ws / f).is_dir()}
    skills = []
    for engine, root in roots.items():
        skills.extend(FANIN.discover(engine, root))
    FANIN.scan(skills, roots)
    FANIN.scan_aliases(skills, roots)
    FANIN.scan_router(skills, roots)
    active_slugs = defaultdict(list)
    for s in skills:
        active_slugs[s.slug].append(s)
    folder_index = {FANIN.norm_key(s.folder): s for s in skills}

    nodes = [{"id": f"engine:{e}", "type": "engine"} for e in roots]
    nodes += [{"id": f"router:{e}", "type": "router"} for e in roots]
    nodes += [{"id": f"skill:{s.key}", "type": "skill", "engine": s.engine} for s in skills]
    edges = []
    for s in skills:
        for src in sorted(s.links):
            edges.append({"from": f"skill:{src}", "to": f"skill:{s.key}", "type": "links_to", "provenance": "EXTRACTED"})
        for src in sorted(s.mentions):
            edges.append({"from": f"skill:{src}", "to": f"skill:{s.key}", "type": "mentions", "provenance": "INFERRED"})
        for src in sorted(s.aliases):
            edges.append({"from": f"alias:{src}", "to": f"skill:{s.key}", "type": "alias_of", "provenance": "EXTRACTED"})
        if s.router != "none":
            edges.append({"from": f"router:{s.engine}", "to": f"skill:{s.key}", "type": "routes_to", "provenance": "EXTRACTED", "mode": s.router})

    # defers_to, plus candidate-defect scans over every active skill document and router.
    defers = Counter()
    retired_hits, missing_paths, renamed_hits = [], [], []
    retired: dict[str, str] = {}
    for engine, root in roots.items():
        data = FANIN.load_yaml(root / "docs" / "skill-aliases.yml")
        if isinstance(data, dict):
            for src, target in (data.get("inactive_skill_aliases") or {}).items():
                slug = PurePosixPath(str(src)).name.lower()
                if slug not in active_slugs:
                    retired[slug] = f"{engine}:{src} -> {target}"
    documents: list[tuple[str, Path, object]] = []
    for s in skills:
        for doc in FANIN.skill_documents(s, folder_index):
            documents.append((s.engine, doc, s))
    for engine, root in roots.items():
        for name in ("AGENTS.md", "README.md", "SKILL.md"):
            if (root / name).is_file():
                documents.append((engine, root / name, None))
    catalog_folders = set(roots)
    for engine, doc, owner in documents:
        root = roots[engine]
        rel = doc.relative_to(ws).as_posix()
        for number, line in enumerate(lines_of(doc), 1):
            low = line.lower()
            tokens = set(FANIN.TOKEN_RE.findall(low))
            if owner is not None and DEFER_RE.search(line):
                for token in tokens:
                    for target in active_slugs.get(token, ()):
                        if target is not owner and "-" in token:
                            edges.append({"from": f"skill:{owner.key}", "to": f"skill:{target.key}", "type": "defers_to",
                                          "provenance": "INFERRED", "evidence": f"{rel}:{number}"})
                            defers[target.key] += 1
            for token in (tokens & set(retired)) if not RETIREMENT_WORDS.search(line) else ():
                # Named as a skill: `slug` on its own, or a skills/<category>/slug path. A consolidated
                # reference folder (references/<slug>/) is the retirement working as designed.
                if "-" in token and re.search(rf"`{re.escape(token)}`|skills/(?:[a-z0-9-]+/)+{re.escape(token)}\b", low):
                    retired_hits.append({"at": f"{rel}:{number}", "slug": token, "alias": retired[token], "line": line.strip()[:200]})
            for match in SKILL_PATH_RE.finditer(line):
                value = match.group(1)
                if "<" in value or "*" in value or "example" in value or value.endswith("-"):
                    continue
                head = value.split("/", 1)[0]
                if head in catalog_folders or head in FOLDER_ONLY or head in RENAMED_ENGINES:
                    base, sub = ws / FOLDER_ONLY.get(head, RENAMED_ENGINES.get(head, head)), value.split("/", 1)[1]
                elif head == "skills":
                    base, sub = root, value
                else:
                    continue
                def found(b: Path, rel_path: str) -> bool:
                    return (b / rel_path).exists() or (b / (rel_path + ".md")).exists()
                if head == "skills" and not found(base, sub):
                    # An engine-less path may name a sibling engine's skill; only a path that
                    # resolves in no catalogued engine is a candidate defect.
                    if any(found(other, sub) for other in roots.values()):
                        continue
                if not found(base, sub):
                    missing_paths.append({"at": f"{rel}:{number}", "reference": value, "line": line.strip()[:200]})
            for old, new in {**RENAMED_ENGINES}.items():
                if old in low:
                    renamed_hits.append({"at": f"{rel}:{number}", "name": old, "current": new, "line": line.strip()[:200]})
            for old, new in FOLDER_ONLY.items():
                if re.search(rf"(www[\\/]|\.\./){re.escape(old)}", low):
                    renamed_hits.append({"at": f"{rel}:{number}", "name": old, "current": new, "line": line.strip()[:200]})

    # similar_trigger (AMBIGUOUS) from the M10-03 union index.
    docs = []
    for engine, root in roots.items():
        found, _ = LEX.discover_engine(engine, root)
        docs.extend(found)
    index = LEX.LexicalIndex(docs)
    pairs = index.pairs(0.75, cross_engine_only=True)
    def skill_node(lexical_key: str) -> str:
        owner = folder_index.get(FANIN.norm_key(Path(index.by_key[lexical_key].path).parent))
        return f"skill:{owner.key}" if owner is not None else f"lexical:{lexical_key}"

    for score, a, b in pairs:
        edges.append({"from": skill_node(a), "to": skill_node(b), "type": "similar_trigger", "provenance": "AMBIGUOUS", "score": score})

    edges.sort(key=lambda e: (e["type"], e["from"], e["to"], e.get("evidence", "")))
    bridges = Counter()
    for e in edges:
        if e["type"] in {"links_to", "mentions", "defers_to"}:
            a = e["from"].split(":", 1)[1].split("/", 1)[0]
            b = e["to"].split(":", 1)[1].split("/", 1)[0]
            if a != b:
                bridges[f"{a} -> {b}"] += 1
    unrouted = sorted(
        ({"skill": s.key, "mentions": len(s.mentions)} for s in skills if s.router == "none" and len(s.mentions) >= 5),
        key=lambda r: (-r["mentions"], r["skill"]))
    node_ids = sorted({n["id"] for n in nodes} | {e["from"] for e in edges} | {e["to"] for e in edges})
    position = {node: i for i, node in enumerate(node_ids)}
    edge_types = sorted({e["type"] for e in edges})
    compact = sorted({(position[e["from"]], position[e["to"]], edge_types.index(e["type"])) for e in edges})
    graph = {
        "schema_version": "1.0",
        "note": "Report-only skill graph (M10-12 GR-01). Never a routing input or a CI gate (P04).",
        "generated_from_commits": {engine: GENERATOR_HEAD(root) for engine, root in sorted(roots.items())},
        "edge_types": edge_types,
        "provenance": {"links_to": "EXTRACTED", "routes_to": "EXTRACTED", "alias_of": "EXTRACTED",
                       "mentions": "INFERRED", "defers_to": "INFERRED", "similar_trigger": "AMBIGUOUS"},
        "nodes": node_ids,
        "edges": [list(edge) for edge in compact],
    }
    report = {
        "counts": {"nodes": len(nodes), "edges": len(edges), "by_type": dict(sorted(Counter(e["type"] for e in edges).items()))},
        "most_deferred_to": [{"skill": k, "defers_to_inbound": v} for k, v in sorted(defers.items(), key=lambda kv: (-kv[1], kv[0]))[:10]],
        "cross_engine_bridges": [{"pair": k, "edges": v} for k, v in sorted(bridges.items(), key=lambda kv: (-kv[1], kv[0]))],
        "mentioned_but_unrouted": unrouted,
        "retired_alias_mentions": sorted(retired_hits, key=lambda r: json.dumps(r, sort_keys=True)),
        "missing_skill_paths": sorted(missing_paths, key=lambda r: json.dumps(r, sort_keys=True)),
        "renamed_engine_mentions": sorted(renamed_hits, key=lambda r: json.dumps(r, sort_keys=True)),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    graph_path = args.out / "skill-graph.json"
    if graph_path.is_file() and not args.allow_shrink:
        previous = json.loads(graph_path.read_text(encoding="utf-8"))
        if len(graph["edges"]) < 0.8 * len(previous.get("edges", [])):
            print(f"REFUSED (shrink guard): edges {len(previous['edges'])} -> {len(graph['edges'])}; pass --allow-shrink after review")
            return 2
    graph_path.write_text(dump_compact(graph), encoding="utf-8", newline="\n")
    report_path = args.report or (args.out / "skill-graph-report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps(report["counts"]))
    print(f"retired={len(retired_hits)} missing_paths={len(missing_paths)} renamed={len(renamed_hits)} unrouted={len(unrouted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
