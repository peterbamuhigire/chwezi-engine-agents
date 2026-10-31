#!/usr/bin/env python3
"""Objective readability measures for Markdown READMEs (README kaizen, 31 October 2026). Read-only.

The measures are proxies. They show whether a README is a wall of text; they do not show whether a
person finds it clear. The shared limits and what each measure does and does not mean are in
``docs/operations/readme-standard-2026-10-31.md``.

What is counted. Text inside fenced code blocks (lines that start with three backticks) is never
counted, and a heading line adds no words. Everything else is counted: bullets, table rows and prose.

``words``        words outside code fences
``h2``           second-level headings (``## ``) outside code fences
``toc``          1 when four or more in-page links (``](#anchor)``) appear before the third H2, else 0
``first_cmd``    line number of the first fenced code block (0 when there is none); lower is faster to
                 something runnable
``longest_sec``  words in the longest H2 section, headings below it included. The text before the first
                 H2 counts as a section of its own
``long_lines``   lines over 300 characters outside code fences; a proxy for paragraphs and table cells
                 that nobody reads
``max_line``     characters in the longest line outside code fences
``sent_len``     mean words per sentence in prose
``fre``          Flesch reading ease of the prose (higher is easier; 30 to 50 is difficult, 60 to 70 plain)
``bullets``      list items
``tables``       table rows, the separator row included

Prose means lines that are not headings, bullets, table rows, blank lines or lines starting with ``<``,
``[`` or ``!`` (HTML, link-first lines, images). Inline code is removed and a link keeps its text. So
``sent_len`` and ``fre`` say nothing about bullets or table cells. A sentence needs three words to count.
The sentence splitter is crude: it also splits after an abbreviation that ends in a full stop.

``--check`` compares a README with the absolute limits in ``LIMITS`` (the numbers in the standard).
Limits that depend on the README's own history (word count, reading ease against a baseline) are not
checked here; compare two runs instead.

Exit codes: 0 measured (and, with ``--check``, every limit met); 1 a limit missed under ``--check``;
3 NOT_ASSESSED, a file could not be read. An unreadable file is never a pass.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MEASURES = ("words", "h2", "toc", "first_cmd", "longest_sec", "long_lines", "max_line", "sent_len", "fre", "bullets", "tables")

LONG_LINE_CHARS = 300      # a line over this many characters is "long"
TOC_MIN_LINKS = 4          # in-page links before the third H2 that make a contents list
MIN_SENTENCE_WORDS = 3     # a shorter fragment is not a sentence

# measure: (lowest allowed, highest allowed); None means no bound on that side.
LIMITS: dict[str, tuple[float | None, float | None]] = {
    "toc": (1, None),
    "first_cmd": (1, 40),
    "longest_sec": (None, 1500),
    "long_lines": (None, 20),
    "max_line": (None, 700),
    "sent_len": (None, 16.5),
}

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")
ALPHA_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")
LIST_ITEM_RE = re.compile(r"^\s*([-*+]|\d+[.)]) ")
HEADING_RE = re.compile(r"^#{1,6} ")
INPAGE_LINK_RE = re.compile(r"\]\(#[a-z0-9-]+\)")


def syllables(word: str) -> int:
    """Rough syllable count: vowel groups, less a silent final ``e``. Always at least 1 for a word."""
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and count > 1 and not word.endswith(("le", "ee")):
        count -= 1
    return max(1, count)


def measure_text(text: str) -> dict[str, float]:
    """Return the measures of one README given as text."""
    lines = text.splitlines()
    in_code = False
    first_cmd: int | None = None
    prose_lines: list[str] = []
    words_total = bullets = tables = 0
    sections: list[int] = []
    current = 0
    long_lines = max_line = 0
    h2_lines: list[int] = []
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            if not in_code and first_cmd is None:
                first_cmd = number
            in_code = not in_code
            continue
        if in_code:
            continue
        max_line = max(max_line, len(line))
        if len(line) > LONG_LINE_CHARS:
            long_lines += 1
        if line.startswith("## "):
            h2_lines.append(number)
            sections.append(current)
            current = 0
            continue
        if HEADING_RE.match(line):
            continue
        count = len(WORD_RE.findall(line))
        words_total += count
        current += count
        if LIST_ITEM_RE.match(line):
            bullets += 1
        elif line.lstrip().startswith("|"):
            tables += 1
        elif line.strip() and not line.startswith(("<", "[", "!")):
            prose_lines.append(line.strip())
    sections.append(current)

    prose = " ".join(prose_lines)
    prose = re.sub(r"`[^`]*`", " ", prose)
    prose = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", prose)
    prose = re.sub(r"[*_#>]", "", prose)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) >= MIN_SENTENCE_WORDS]
    prose_words = ALPHA_WORD_RE.findall(prose)
    sent_len = len(prose_words) / len(sentences) if sentences else 0.0
    syllable_total = sum(syllables(w) for w in prose_words)
    fre = 206.835 - 1.015 * sent_len - 84.6 * (syllable_total / len(prose_words)) if prose_words and sentences else 0.0

    cut = h2_lines[2] - 1 if len(h2_lines) >= 3 else len(lines)
    toc = 1 if len(INPAGE_LINK_RE.findall("\n".join(lines[:cut]))) >= TOC_MIN_LINKS else 0
    return {
        "words": words_total, "h2": len(h2_lines), "toc": toc, "first_cmd": first_cmd or 0,
        "longest_sec": max(sections), "long_lines": long_lines, "max_line": max_line,
        "sent_len": round(sent_len, 1), "fre": round(fre), "bullets": bullets, "tables": tables,
    }


def measure(path: Path) -> dict[str, float]:
    """Return the measures of one README file, decoded as UTF-8 with undecodable bytes replaced."""
    return measure_text(path.read_text(encoding="utf-8", errors="replace"))


def limit_misses(metrics: dict[str, float]) -> list[str]:
    """Describe every absolute limit the measures miss; an empty list means all are met."""
    misses = []
    for name, (low, high) in LIMITS.items():
        value = metrics[name]
        if low is not None and value < low:
            misses.append(f"{name} is {value}, below the minimum {low:g}")
        if high is not None and value > high:
            misses.append(f"{name} is {value}, above the maximum {high:g}")
    return misses


def format_table(rows: list[tuple[str, dict[str, float]]]) -> str:
    out = [f"{'file':34}" + "".join(f"{name:>12}" for name in MEASURES)]
    for label, metrics in rows:
        out.append(f"{label[:33]:34}" + "".join(f"{metrics[name]:>12}" for name in MEASURES))
    return "\n".join(out)


def label_for(path: Path) -> str:
    """The folder that holds the file: READMEs of different engines are told apart by their folder name."""
    return path.resolve().parent.name or path.name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path, metavar="README", help="Markdown file(s) to measure")
    parser.add_argument("--json", action="store_true", help="print one JSON object per file instead of the table")
    parser.add_argument("--check", action="store_true", help="exit 1 when a measure misses an absolute limit")
    args = parser.parse_args(argv)

    rows: list[tuple[str, dict[str, float]]] = []
    unreadable = False
    for path in args.files:
        try:
            rows.append((label_for(path), measure(path)))
        except OSError as error:
            print(f"NOT_ASSESSED {path.name}: {error.strerror or error}", file=sys.stderr)
            unreadable = True
    if args.json:
        for label, metrics in rows:
            print(json.dumps({"file": label, **metrics}, sort_keys=True))
    elif rows:
        print(format_table(rows))

    missed = False
    if args.check:
        for label, metrics in rows:
            for miss in limit_misses(metrics):
                print(f"LIMIT {label}: {miss}")
                missed = True
        if not missed and rows:
            print(f"limits: {len(LIMITS)} checked on {len(rows)} file(s); all met")
    if unreadable:
        return 3
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
