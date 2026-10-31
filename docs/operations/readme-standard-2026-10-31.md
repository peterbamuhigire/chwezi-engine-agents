# README standard, 31 October 2026

This standard sets how every Chwezi README is structured, measured and changed. It applies to the root `README.md` of the eleven domain engines and of this package. It does not replace an engine's router (`AGENTS.md`), and it never overrides a validator.

It was written after a README kaizen on all twelve repositories. Section 6 holds the measured results. The tools that enforce it are in this package: [`scripts/readme_metrics.py`](../../scripts/readme_metrics.py) and [`scripts/check_readme_preservation.py`](../../scripts/check_readme_preservation.py). Both are listed in the [README](../../README.md#find-the-right-tool) and in the [package tools reference](package-tools-reference.md).

Review it after the next README kaizen cycle, or sooner if a limit stops fitting.

## 1. Why a standard

Before the kaizen the eleven engine READMEs ran from 5,500 to 12,579 words. Each had five to seven top-level sections, and the largest section held 2,347 to 6,019 words. Only one README had a contents list. Each had 33 to 55 lines over 300 characters. Reading ease was 31 to 47, which is difficult.

The reader's problem was a wall of detail between the front door and the thing they came for. The standard fixes that with three things: a fixed structure, limits anyone can measure, and rules that keep every command, link and anchor that something else depends on.

## 2. The structure

Use this order. Adapt names only where a validator or another file needs a heading to stay as it is.

| # | Section | What it holds |
|---|---|---|
| 1 | Title and purpose | Two or three plain sentences: what it is, who it is for, when to use it. |
| 2 | At a glance | Five or six measured facts, each with a date or a command behind it. |
| 3 | Start here | Three numbered steps with exact commands: install or load, check, first use. |
| 4 | Contents | A list of in-page links to the H2 sections. Every link resolves. |
| 5 | When to use it, and Find the right skill | Six to twelve rows from task to skill, with real names. A coordination package lists tasks and tools. |
| 6 | How it works | Routing and architecture, short. |
| 7 | What is inside | Counts and categories, with a link to the full catalogue if there is one. |
| 8 | Install and update | Each route, with the findings from running it. |
| 9 | Validate | Commands, dependencies, dated results and what ran where. A check that could not run is `NOT_ASSESSED`. |
| 10 | Quality and improvement | Status, what improved, open items, date gates. |

Then come the engine's own sections, a References or Cited sources section, and Contributing, author and licence. Sections 1 to 3 belong at the top: aim to end the three Start here steps by line 40. The first fenced command block must start by line 40, and `--check` tests that.

A README that is also the engine's router keeps its routing text exactly as it is. Add the front door and the contents list around it.

**Known conflict.** `scripts/validate-portfolio-craft.ps1` (lines 49 and 50) still expects the layout of 20 September 2026: a `## Capability map` or `## Capabilities` heading among the first four H2 headings. Ten of the eleven engine READMEs lack it now. The script is Windows-only and no CI job runs it. Until the maintainer changes the rule or the READMEs, a Windows run of that script reports ten failures. The standard does not override it.

## 3. The limits

### What each measure says

`readme_metrics.py` prints eleven measures. Six have absolute limits that `--check` tests. Two are compared with the README's own baseline.

| Measure | Limit | Means | Does not mean |
|---|---|---|---|
| `toc` | 1 | Four or more in-page links appear before the third H2: a contents list exists. | That the list is good, or that its links resolve. The preservation check tests the links. |
| `first_cmd` | 1 to 40 | The first fenced code block starts by line 40. | That the command works. It also counts a block that holds only output. |
| `longest_sec` | 1,500 words or fewer (aim for 1,200) | No H2 section, with its H3 content, is a wall. The text before the first H2 counts as a section. | That each H3 is short. Aim for 600 words or fewer per section. |
| `long_lines` | 20 or fewer | Few paragraphs, bullets or table rows run past 300 characters. The baseline should halve at least. | That the text is short. A long line can be split without cutting a word. |
| `max_line` | 700 characters or fewer | No cell or paragraph is unreadable. | That a row under the limit is easy. Table cells should stay near 35 words. |
| `sent_len` | 16.5 or fewer (aim for 16) | Mean words per sentence in prose. | Anything about bullets, table cells or headings. Prose only. |
| `fre` | No lower than the baseline (aim for 5 more) | Flesch reading ease of the prose. 30 to 50 is difficult and 60 to 70 is plain. | A score for the whole page. It reads prose only, and technical terms lower it. |
| `words` | At most the baseline plus 5% (aim for 10% fewer) | The README did not grow. | That it is shorter to read. Moving a table to `docs/` lowers it without removing a word. |

`h2`, `bullets` and `tables` are information, not limits.

### How the measures count

- Text inside fenced code blocks is never counted. A heading line adds no words. Bullets, table rows and prose all count towards `words`.
- `sent_len` and `fre` read prose only: not headings, bullets, table rows, blank lines or lines that start with `<`, `[` or `!`. Inline code is removed and a link keeps its text.
- A sentence needs three words to count as one. A shorter fragment adds its words to the sum but no sentence. That quirk is kept so that the new numbers match the baseline.
- `long_lines` and `max_line` look at headings and table rows as well as prose.
- The sentence splitter is crude. It splits after any full stop that ends an abbreviation.

### What the measures do not show

- Whether a reader finds the README clearer. No reader test was run. The measures are proxies.
- Bullets and table cells can hold long sentences that `sent_len` never sees. Keep bullets and cells short by rule: no paragraph over 90 words and no table cell over 35 words.
- Lines of 300 characters or fewer can still be dense. Count the facts per line, not only the characters.

### Writing rules the tools do not test

- British English, plain words, active voice. Define a term at first use.
- Say each fact once and link to the record that holds the detail.
- Keep process narrative (cycle diaries, "pass 2 did X") in the linked records. Keep the "What the October 2026 kaizen improved" section: it was asked for, and it follows these limits like any other.
- Every number, command, link, repository name and date stays true. Re-measure any number you touch. A deliberate correction is allowed and goes in the record.

### Running the tools

```sh
python3 -X utf8 scripts/readme_metrics.py README.md
python3 -X utf8 scripts/readme_metrics.py --check README.md
python3 -X utf8 scripts/readme_metrics.py --json README.md
```

The first prints the table. The second also exits 1 when a limit is missed and names each miss. The third prints one JSON object per file. An unreadable file exits 3 (`NOT_ASSESSED`), never 0.

## 4. Preservation rules

### What is an interface

A README is read by people and by other files. Three things in it are interfaces:

- **Commands.** Every non-comment line of a fenced code block, and every inline code span that starts with a command word and has an argument.
- **Links.** Every relative path and every URL. A relative link is compared by the file it points to, not by how it is written, so `./docs/a.md` and `docs/a.md` are one target.
- **Anchors.** Every heading anchor that another file links to. The check reads links to the root README from Markdown files (resolved against each file's folder) and from scripts, YAML and JSON.

Treat a fourth group as an interface too: any section a script, test, manifest or router reads in the README itself.

### When to move bulk and when never to

Move bulky reference material to a `docs/` page when all of these hold:

1. No script, test, manifest or router reads that section. Search for the README path and for the heading text, and run the validators.
2. The README keeps a short summary and a link.
3. The preservation check reports the material as moved, not lost.

Typical candidates are a skill catalogue of more than about 50 rows, a long calendar, and a long source list.

Never move:

- content that a validator checks in the README itself, such as skill totals, a "Checks" paragraph or a citation ceiling;
- routing content in a README that is the engine's router;
- a heading that another file links, unless the same commit updates those links and the link checks run again;
- the date-gate calendar, the open findings or the validation results of a package whose readers act on them.

### Reading the preservation output

`check_readme_preservation.py REPO BASE NEW` prints four lines and a result:

```text
links: old README 129 targets; new README 75; moved to docs 62; LOST 0
commands: old README 48; kept in README 47; moved to docs 1; LOST 0
anchors: 4 README anchor links in tracked files; BROKEN 0
in-page links: 20 anchors used; BROKEN 0
RESULT: OK
```

- **LOST** means the old README linked or ran something that the new README and every changed docs page lack. Restore it or explain it in the record. It exits 1.
- **moved** means the target or command now appears in a Markdown file that the branch added or changed. Add `-v` to list them.
- **BROKEN anchor** means a tracked file links a heading that no longer exists. **BROKEN in-page link** means the new README links to a heading it lacks. Both exit 1.
- **note** lists heading anchors that the old README had and the new one lacks. Other repositories may link them. The check cannot see those links, so search the sibling repositories before you merge.
- A deliberate replacement, such as `python` becoming `python3`, is reported as a loss. Explain each one in the record.
- An unknown revision, a folder that is not a git repository, or a missing README exits 3 (`NOT_ASSESSED`). It is never a pass.

### What the check does not see

- Links from other repositories, and plain-text mentions of an anchor in Markdown that are not links.
- Setext headings and headings written as HTML.
- A README anchor link written out in a script or test fixture is read as a real link. Build such fixtures in pieces, as `tests/test_readme_preservation.py` does.
- Links and commands that were wrong before the rewrite.

## 5. Procedure for an engine README kaizen

The procedure is the Portfolio Kaizen cycle scoped to one file. It changes no skill body, script or test. Work only in the engine's repository, and publish no score.

1. **Observe.**
   - Record `git status --porcelain`, the branch and HEAD. Start from a clean `main`.
   - Find what reads the README: search scripts, tests, manifests and routers for the README path and for each heading you may move.
   - Save the baseline: `python3 -X utf8 scripts/readme_metrics.py <engine>/README.md`, run from this package.
2. **Select.** Choose from the structure and the limits above. Write down each item you skip and why.
3. **Experiment.**
   - Branch `kaizen/<date>-readme-kaizen` from `main`.
   - Commit by theme with explicit `git add <paths>`: front door and structure, plain English, relocation, record. Relocate verbatim first and fix links second.
   - Do not push, tag, merge or open a pull request unless asked.
4. **Check.**
   - Run the engine's registered validators before and after. The exit codes must match.
   - Run `check_readme_preservation.py <engine> main <branch>`. It must report no LOST and no BROKEN, or each one must be explained.
   - Run `readme_metrics.py --check`, and compare the relative limits with the baseline.
   - Confirm every contents link and every sibling-repository link to a moved anchor.
5. **Standardise and teach.**
   - Write `docs/kaizen/<date>-readme-kaizen/readme-kaizen-record.md`: observe, select, experiment, check, the conventions for the next editor, and the next cycle.
   - Update the `docs/README.md` index lines and the changelog entry, where the engine keeps one.
6. **Re-measure.** After the merge, run the metrics once more and add the row to the table below.

## 6. Measured result on 31 October 2026

### How it was measured

- **Before** is the README at each engine's pinned `released_commit` in `catalog/engines.yaml`. Each pin is the commit that engine's README kaizen started from, as its record states. The figures equal the baseline taken before the kaizen, row for row.
- **After** is the README at each engine's `main` on 31 October 2026. Each checkout was clean and its README equalled `main`.
- The tool is `scripts/readme_metrics.py`. The checkouts are the eleven engines and this package.

### Size and structure

Each cell reads "before to after".

| Engine | Words | H2 sections | Contents list | First command at line | Longest section (words) |
|---|---|---|---|---|---|
| Accounting Doctrine | 7,216 to 6,049 | 7 to 14 | 0 to 1 | 13 to 24 | 2,347 to 1,050 |
| Digital Research | 8,202 to 5,483 | 6 to 15 | 0 to 1 | 17 to 22 | 2,940 to 977 |
| Dev engine | 12,579 to 4,685 | 5 to 12 | 0 to 1 | 15 to 37 | 5,567 to 1,288 |
| Design engine | 8,666 to 5,832 | 5 to 14 | 0 to 1 | 15 to 22 | 2,462 to 1,154 |
| SDLC documentation | 8,995 to 5,663 | 6 to 14 | 0 to 1 | 34 to 22 | 2,951 to 1,445 |
| Linux | 6,202 to 5,710 | 5 to 19 | 1 to 1 | 105 to 20 | 2,570 to 869 |
| Windows administration | 5,500 to 4,394 | 5 to 11 | 0 to 1 | 88 to 24 | 2,832 to 1,010 |
| Proposal | 7,719 to 5,086 | 6 to 14 | 0 to 1 | 13 to 26 | 2,376 to 1,050 |
| Business plan | 11,588 to 5,835 | 5 to 17 | 0 to 1 | 13 to 20 | 4,242 to 906 |
| Website | 9,334 to 4,421 | 6 to 12 | 0 to 1 | 13 to 22 | 3,500 to 1,000 |
| Social media | 11,393 to 5,731 | 6 to 18 | 0 to 1 | 15 to 24 | 6,019 to 833 |
| **Eleven engines** | 97,394 to 58,889 | 62 to 160 | 1 of 11 to 11 of 11 | latest 105 to 37 | largest 6,019 to 1,445 |
| This package | 7,470 to 7,538 | 8 to 23 | 0 to 1 | 13 to 20 | 3,100 to 1,136 |

### Readability

| Engine | Lines over 300 characters | Longest line (characters) | Words per sentence | Reading ease |
|---|---|---|---|---|
| Accounting Doctrine | 43 to 15 | 1,342 to 451 | 18.2 to 11.4 | 37 to 47 |
| Digital Research | 44 to 0 | 1,983 to 300 | 16.7 to 10.2 | 43 to 57 |
| Dev engine | 55 to 9 | 1,524 to 372 | 20.1 to 11.7 | 39 to 59 |
| Design engine | 41 to 6 | 1,297 to 377 | 16.9 to 11.8 | 47 to 55 |
| SDLC documentation | 44 to 5 | 1,240 to 374 | 15.5 to 11.6 | 43 to 53 |
| Linux | 44 to 1 | 1,380 to 364 | 16.4 to 12.3 | 42 to 52 |
| Windows administration | 33 to 1 | 1,386 to 357 | 14.1 to 12.1 | 46 to 54 |
| Proposal | 42 to 6 | 1,291 to 362 | 16.8 to 10.2 | 44 to 61 |
| Business plan | 44 to 0 | 1,276 to 296 | 19.8 to 12.6 | 39 to 56 |
| Website | 54 to 16 | 1,171 to 458 | 18.0 to 12.3 | 45 to 61 |
| Social media | 39 to 12 | 1,783 to 542 | 20.7 to 11.3 | 31 to 57 |
| **Eleven engines** | 483 to 71 | worst 1,983 to 542 | mean 17.6 to 11.6 | mean 41.5 to 55.6 |
| This package | 61 to 7 | 1,461 to 416 | 19.6 to 12.1 | 44 to 59 |

### What the results show

- At the pinned commits the eleven engines missed the six absolute limits 53 times: contents list 10, longest section 11, long lines 11, longest line 11, sentence length 8 and first command 2. On 31 October none of the eleven missed one, and this package missed none.
- The word count fell by 38,505, about 40%. Most of that is relocation, not deletion. The kaizen added 26 pages under `docs/` for catalogues, source lists and October-kaizen detail. They hold about 52,800 words, counted by splitting on white space, so the count differs from `words`.
- The earlier figure of 58,890 words was one word higher. The social-media README changed by one word after that count.
- The first command moved later in eight engines, because six facts now come first. It moved earlier in the SDLC, Linux and Windows engines. The latest is line 37 of the dev engine, inside the 40-line limit.
- The Linux README already had a contents list. This package's README stayed near its baseline (7,470 to 7,538 words, plus 1%). It gained a front door, a contents list and tables while it moved its tool detail and reference lists to `docs/`. It missed the aim of 10% fewer words and met the 5% ceiling.
- Reading ease and sentence length cover prose only. The kaizen sections of several READMEs still hold bullets with long sentences, commit hashes and figures. The mean of 55.6 is therefore not a reading-ease score for the whole page.

## 7. Where the records are

- This package: [`docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md`](../kaizen/2026-10-readme-kaizen/readme-kaizen-record.md).
- Each engine: `docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md` in its own repository.
- The tool reference row for the two scripts: [`package-tools-reference.md`](package-tools-reference.md).
