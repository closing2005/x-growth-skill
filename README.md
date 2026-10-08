# x-growth-skill

A Claude Code skill for drafting better X/Twitter posts. Hook analysis,
a 0–100 engagement rubric, and a bilingual (中文/EN) workflow.

## Install

Copy this directory to your Claude Code skills folder:

```bash
cp -r x-growth-skill ~/.claude/skills/
```

Or reference it per-project. No dependencies beyond Python 3.

## Usage

**In Claude Code** — the skill auto-activates when you draft or review X content:

> "Score this draft: …"

**Standalone scripts:**

```bash
# Hook analysis (0-40)
python scripts/hook_analyzer.py "为什么你的帖子总是没人看？"

# Full rubric (0-100)
python scripts/post_scorer.py --file draft.txt
```

## How it works

| Dimension | Weight | What it checks |
|-----------|--------|----------------|
| Hook | 40 | First-line patterns: question, number, bold claim, curiosity gap, how-to, story, data |
| Structure | 25 | Line breaks, mobile scannability, length |
| Value signal | 20 | Concrete numbers, sources, first-hand voice |
| CTA | 15 | Ends with a question or invitation |

See [references/hook_patterns.md](references/hook_patterns.md) for the
pattern library with Chinese + English examples.

## Why this exists

Built from a daily X writing practice (@TesAcesas) — every rule here survived
contact with real posting data. Dogfooded, not theorized.

## License

MIT
