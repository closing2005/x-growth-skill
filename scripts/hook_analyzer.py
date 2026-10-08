#!/usr/bin/env python3
"""
hook_analyzer.py — score the opening line of an X post draft.

Usage:
    python hook_analyzer.py "Your draft post here..."
    python hook_analyzer.py --file draft.txt

Prints a JSON report: hook score (0-40), matched patterns, flags, suggestions.
"""
import json
import re
import sys

HOOK_PATTERNS = [
    ("question",
     re.compile(r"[?？]\s*$"),
     "Ends with a question — invites replies", 8),
    ("number",
     re.compile(r"\d+"),
     "Contains a concrete number — specificity boosts click-through", 7),
    ("bold_claim",
     re.compile(r"暴论|没人告诉你|unpopular opinion|hot take|nobody talks about", re.I),
     "Bold claim — strong curiosity trigger", 8),
    ("curiosity_gap",
     re.compile(r"但是|但|然而|however|but |until |直到|结果"),
     "Curiosity gap — the reader wants the resolution", 6),
    ("how_to",
     re.compile(r"怎么|如何|how to|how i |教程|guide|step", re.I),
     "How-to promise — clear value proposition", 6),
    ("story",
     re.compile(r"昨天|今天|刚才|^我|yesterday|last night|^i ",
                re.I),
     "Story opening — narrative pull", 5),
    ("data_led",
     re.compile(r"%|％|数据|stats|study|report", re.I),
     "Data-led — borrowed credibility", 6),
]

NEGATIVE_FLAGS = [
    ("too_long",
     lambda h: len(h) > 80,
     "Hook is over 80 chars — it will truncate in the feed"),
    ("too_short",
     lambda h: len(h.strip()) < 8,
     "Hook is under 8 chars — too vague to earn the click"),
    ("emoji_stuffing",
     lambda h: len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", h)) > 3,
     "More than 3 emojis in the hook — looks spammy"),
    ("hashtag_lead",
     lambda h: h.strip().startswith("#"),
     "Leading with a hashtag — kills curiosity"),
    ("all_caps",
     lambda h: len(re.findall(r"[A-Za-z]", h)) > 10 and h == h.upper(),
     "ALL CAPS — reads as shouting"),
]


def analyze(text):
    hook = text.strip().split("\n")[0]
    score = 10  # base for showing up
    matched, flags, suggestions = [], [], []

    for name, rx, desc, pts in HOOK_PATTERNS:
        if rx.search(hook):
            matched.append({"pattern": name, "why": desc, "points": pts})
            score += pts

    for name, fn, msg in NEGATIVE_FLAGS:
        if fn(hook):
            flags.append({"flag": name, "message": msg})
            score -= 6
            suggestions.append(msg)

    score = max(0, min(40, score))

    if not matched:
        suggestions.append(
            "No strong hook pattern detected — try a question, a number, or a "
            "bold claim (see references/hook_patterns.md)."
        )

    return {
        "hook": hook,
        "score": score,
        "max": 40,
        "patterns": matched,
        "flags": flags,
        "suggestions": suggestions,
    }


def main(argv):
    if len(argv) >= 3 and argv[1] == "--file":
        with open(argv[2], encoding="utf-8") as f:
            text = f.read()
    elif len(argv) >= 2:
        text = argv[1]
    else:
        text = sys.stdin.read()

    if not text.strip():
        print(json.dumps({"error": "empty draft"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(analyze(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv)
