#!/usr/bin/env python3
"""Shared lexical routing index for the Chwezi portfolio (Tier 2 routing proxy).

Tokeniser, stemmer, IDF and owner-outranks-self rule adapted from addyosmani/agent-skills
(MIT, https://github.com/addyosmani/agent-skills, commit 2686b62), `scripts/run-evals.js`;
paraphrased, not copied.

Adaptations for this portfolio (M10-03-T01):

- IDF is computed over the union of every catalogued engine, not per engine, so scores differ
  from each engine's own smoke test. That is expected.
- Stop words: a 40-word general list plus house words that carry no routing signal
  (``skill``, ``skills``, ``engine``, ``chwezi``).
- British spelling is folded before stemming: ``-ise`` forms map to ``-ize`` forms and a small
  equivalence table folds ``colour -> color`` and similar pairs.
- Frontmatter is read with ``yaml.safe_load``, so block-scalar descriptions (``>-``, ``|``) are
  read in full rather than as an empty string.

This is a lexical proxy, not live routing (see agent-skills issue #620): a rank-1 hit here does
not prove that a host model would load the skill. The module is read by checks only; no agent
reads it at runtime and it is not a router.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

FRONTMATTER_RE = re.compile(r"^﻿?---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
NON_WORD_RE = re.compile(r"[^a-z0-9\s-]")
SPLIT_RE = re.compile(r"[\s-]+")

# Forty general words with no routing signal, plus the house words.
STOP_WORDS = frozenset(
    {
        "the", "and", "for", "with", "that", "this", "from", "into", "when", "use",
        "used", "using", "your", "you", "are", "was", "were", "will", "can", "has",
        "have", "not", "but", "all", "any", "its", "our", "their", "them", "then",
        "than", "also", "each", "how", "what", "which", "who", "need", "help", "want",
        # house words (Chwezi portfolio)
        "skill", "skills", "engine", "chwezi",
    }
)

# British -> American equivalence applied before stemming (calibration table; record changes
# in evals/routing/rejected-changes.md when it is tuned).
EQUIVALENCES = {
    "colour": "color", "colours": "colors", "behaviour": "behavior", "behaviours": "behaviors",
    "centre": "center", "centres": "centers", "catalogue": "catalog", "catalogues": "catalogs",
    "licence": "license", "licences": "licenses", "programme": "program", "programmes": "programs",
    "modelling": "modeling", "analyse": "analyze", "analysed": "analyzed", "analysing": "analyzing",
    "favour": "favor", "honour": "honor", "labour": "labor", "defence": "defense",
    "organisation": "organization", "organisations": "organizations", "optimise": "optimize",
}

EXCLUDED_DIRS = frozenset(
    {
        ".git", "node_modules", "__pycache__", ".claude", ".agents", ".codex", ".cursor",
        ".claude-plugin", ".codex-plugin", "plugin-cache", "plugins-cache", "archive", "archived",
        "templates", "_TEMPLATE", "projects", ".trash",
    }
)
PRIVATE_ENGINE_MARKERS = ("political-essay-skills",)


class PrivateEngineError(ValueError):
    """Raised when a private engine path is offered to a public corpus."""


def _fold_british(token: str) -> str:
    if token in EQUIVALENCES:
        return EQUIVALENCES[token]
    for british, american in (("isations", "izations"), ("isation", "ization"), ("ising", "izing"), ("ised", "ized"), ("ises", "izes")):
        if token.endswith(british) and len(token) - len(british) >= 3:
            return token[: -len(british)] + american
    if token.endswith("ise") and len(token) >= 7:
        return token[:-3] + "ize"
    return token


def stem(token: str) -> str:
    """Light stemmer: one suffix, trailing s, trailing e, doubled consonant, final y."""
    token = _fold_british(token)
    for suffix in ("ally", "ing", "ed", "es", "al"):
        if token.endswith(suffix) and len(token) > len(suffix) + 3:
            token = token[: -len(suffix)]
            break
    if token.endswith("s") and not token.endswith("ss") and len(token) > 3:
        token = token[:-1]
    if token.endswith("e") and len(token) > 4:
        token = token[:-1]
    if len(token) > 3 and token[-1] == token[-2] and token[-1] not in "aeiouy0123456789":
        token = token[:-1]
    if token.endswith("y") and len(token) > 3:
        token = token[:-1] + "i"
    return token


def tokenize(text: str) -> list[str]:
    lowered = NON_WORD_RE.sub(" ", text.lower())
    tokens: list[str] = []
    for raw in SPLIT_RE.split(lowered):
        if len(raw) <= 2 or raw in STOP_WORDS:
            continue
        tokens.append(stem(raw))
    return tokens


@dataclass(frozen=True)
class SkillDoc:
    engine: str
    name: str
    description: str
    path: str

    @property
    def key(self) -> str:
        return f"{self.engine}/{self.name}"


@dataclass
class ReadIssue:
    code: str
    message: str
    path: str


def read_frontmatter(text: str) -> dict | None:
    import yaml

    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    value = yaml.safe_load(match.group(1))
    return value if isinstance(value, dict) else None


def refuse_private(path: Path | str) -> None:
    lowered = str(path).replace("\\", "/").lower()
    if any(marker in lowered for marker in PRIVATE_ENGINE_MARKERS):
        raise PrivateEngineError(f"private engine path refused: {path}")


def discover_engine(engine_id: str, root: Path, excluded: Iterable[str] = EXCLUDED_DIRS) -> tuple[list[SkillDoc], list[ReadIssue]]:
    refuse_private(root)
    excluded = set(excluded)
    docs: list[SkillDoc] = []
    issues: list[ReadIssue] = []
    seen: set[str] = set()
    root = root.resolve()
    for path in sorted(root.rglob("SKILL.md")):
        relative = path.relative_to(root)
        if any(part in excluded or part.startswith(".trash") for part in relative.parts[:-1]):
            continue
        try:
            meta = read_frontmatter(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001 - unreadable metadata is reported, not fatal
            issues.append(ReadIssue("frontmatter-error", f"{type(exc).__name__}: {exc}", str(path)))
            continue
        if not meta or not meta.get("description"):
            issues.append(ReadIssue("frontmatter-missing", "no name/description frontmatter", str(path)))
            continue
        name = str(meta.get("name") or path.parent.name)
        if name in seen:
            name = f"{name}@{relative.parent.as_posix()}"
        seen.add(name)
        description = " ".join(str(meta.get("description")).split())
        docs.append(SkillDoc(engine_id, name, description, str(path)))
    return docs, issues


def load_catalog_engines(catalog_path: Path, workspace_root: Path) -> list[tuple[str, Path]]:
    import yaml

    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    engines: list[tuple[str, Path]] = []
    for entry in data.get("engines", []):
        engine_id = str(entry["id"])
        root = workspace_root / str(entry.get("path") or entry.get("repository") or engine_id)
        refuse_private(root)
        engines.append((engine_id, root))
    return engines


@dataclass
class LexicalIndex:
    docs: list[SkillDoc]
    idf: dict[str, float] = field(init=False)
    vectors: dict[str, dict[str, float]] = field(init=False)

    def __post_init__(self) -> None:
        counts = {doc.key: self._doc_counts(doc) for doc in self.docs}
        df: Counter[str] = Counter()
        for value in counts.values():
            df.update(value.keys())
        n = len(self.docs)
        self.n = n
        self.idf = {term: math.log(1 + n / (1 + freq)) for term, freq in df.items()}
        self.by_key = {doc.key: doc for doc in self.docs}
        self.vectors = {key: self._normalise(self._weigh(value)) for key, value in counts.items()}

    @staticmethod
    def _doc_counts(doc: SkillDoc) -> Counter[str]:
        name_tokens = tokenize(doc.name.split("@", 1)[0])
        return Counter(name_tokens * 2 + tokenize(doc.description))

    def _weigh(self, counts: Counter[str]) -> dict[str, float]:
        unseen = math.log(1 + self.n)
        return {term: count * self.idf.get(term, unseen) for term, count in counts.items()}

    @staticmethod
    def _normalise(vector: dict[str, float]) -> dict[str, float]:
        norm = math.sqrt(sum(value * value for value in vector.values()))
        return {term: value / norm for term, value in vector.items()} if norm else {}

    def query_vector(self, text: str) -> dict[str, float]:
        return self._normalise(self._weigh(Counter(tokenize(text))))

    @staticmethod
    def cosine(a: dict[str, float], b: dict[str, float]) -> float:
        if len(a) > len(b):
            a, b = b, a
        return sum(value * b.get(term, 0.0) for term, value in a.items())

    def rank(self, text: str, engines: set[str] | None = None) -> list[tuple[str, float]]:
        query = self.query_vector(text)
        scored = [
            (key, self.cosine(query, vector))
            for key, vector in self.vectors.items()
            if engines is None or self.by_key[key].engine in engines
        ]
        scored.sort(key=lambda item: (-item[1], item[0]))
        return scored

    def pairs(self, threshold: float, cross_engine_only: bool = False) -> list[tuple[float, str, str]]:
        keys = sorted(self.vectors)
        # Invert the index so only pairs sharing a term are compared.
        postings: dict[str, list[int]] = {}
        for position, key in enumerate(keys):
            for term in self.vectors[key]:
                postings.setdefault(term, []).append(position)
        dots: dict[tuple[int, int], float] = {}
        for term, members in postings.items():
            if len(members) < 2:
                continue
            for i_index, i in enumerate(members):
                weight_i = self.vectors[keys[i]][term]
                for j in members[i_index + 1 :]:
                    dots[(i, j)] = dots.get((i, j), 0.0) + weight_i * self.vectors[keys[j]][term]
        result: list[tuple[float, str, str]] = []
        for (i, j), score in dots.items():
            if score < threshold:
                continue
            a, b = keys[i], keys[j]
            if cross_engine_only and self.by_key[a].engine == self.by_key[b].engine:
                continue
            result.append((round(score, 4), a, b))
        result.sort(key=lambda item: (-item[0], item[1], item[2]))
        return result


def word_trigrams(text: str) -> set[tuple[str, str, str]]:
    words = [word for word in re.findall(r"[a-z0-9]+", text.lower())]
    return {tuple(words[i : i + 3]) for i in range(len(words) - 2)}  # type: ignore[misc]


def slug_phrase(slug: str) -> str:
    slug = slug.split("/")[-1]
    return re.sub(r"^\d+-", "", slug.lower()).replace("-", " ").strip()


def lint_prompt(prompt: str, slug: str, description: str, trigram_limit: float = 0.6) -> list[str]:
    """Return lint findings for a routing prompt (slug leak or description copy)."""
    findings: list[str] = []
    normal = " " + re.sub(r"[^a-z0-9]+", " ", prompt.lower()).strip() + " "
    phrase = slug_phrase(slug)
    if phrase and f" {phrase} " in normal:
        findings.append(f"slug-in-prompt: prompt contains '{phrase}'")
    prompt_grams = word_trigrams(prompt)
    if prompt_grams:
        overlap = len(prompt_grams & word_trigrams(description)) / len(prompt_grams)
        if overlap >= trigram_limit:
            findings.append(f"description-copy: trigram overlap {overlap:.2f} >= {trigram_limit}")
    return findings
