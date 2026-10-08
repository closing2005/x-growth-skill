#!/usr/bin/env python3
"""
post_scorer.py — full rubric scoring for an X post draft (0-100).

    python post_scorer.py "Your draft..."
    python post_scorer.py --file draft.txt

Dimensions: hook (40) + structure (25) + value signal (20) + CTA (15).
"""
import json
import re
import sys

from hook_analyzer import analyze as analyze_hook


def score_structure(text):
    """25 pts: readable shape, no wall of text."""
    score, notes = 15, []
    lines = [ln for ln in text.strip().split("\n")]
    non_empty = [ln for ln in lines if ln.strip()]

    if len(non_empty) >= 3:
        score += 5
        notes.append("Multi-line structure — scannable")
    elif len(non_empty) == 1 and len(text) > 140:
        score -= 8
        notes.append("Wall of text — break it into lines")

    if len(text) > 280:
        score -= 5
        notes.append("Over 280 chars — will truncate; consider a thread")

    long_lines = [ln for ln in non_empty if len(ln) > 90]
    if long_lines:
        score -= 4
        notes.append(f"{len(long_lines)} line(s) over 90 chars — hard to scan on mobile")

    return max(0, min(25, score)), notes


def score_value(text):
    """20 pts: concrete signals that the post says something real."""
    score, notes = 8, []
    if re.search(r"\d+", text):
        score += 5
        notes.append("Contains numbers — concrete")
    if re.search(r"https?://", text):
        score += 3
        notes.append("Links to a source — verifiable")
    vague = len(re.findall(r"很|非常|特别|真的|really|very|amazing|incredible", text))
    if vague >= 3:
        score -= 5
        notes.append(f"{vague} vague intensifiers — replace with specifics")
    if re.search(r"我|my |we ", text, re.I) and len(text) > 60:
        score += 4
        notes.append("First-hand voice — personal beats generic")
    return max(0, min(20, score)), notes


def score_cta(text):
    """15 pts: does it invite a response?"""
    score, notes = 5, []
    last = text.strip().split("\n")[-1]
    if re.search(r"[?？]\s*$", last):
        score += 7
        notes.append("Ends with a question — invites replies")
    elif re.search(r"(评论|留言|你觉得|what do you think|thoughts\?)", text, re.I):
        score += 5
        notes.append("Has an engagement invitation")
    else:
        notes.append("No CTA — consider ending with a question")
    return max(0, min(15, score)), notes


def score_post(text):
    hook = analyze_hook(text)
    struct, struct_notes = score_structure(text)
    value, value_notes = score_value(text)
    cta, cta_notes = score_cta(text)
    total = hook["score"] + struct + value + cta

    if total >= 80:
        verdict = "Strong — ship it with micro-edits."
    elif total >= 60:
        verdict = "Decent — fix the hook or structure first."
    elif total >= 40:
        verdict = "Weak — rewrite the hook before anything else."
    else:
        verdict = "Not ready — rethink the core idea."

    return {
        "total": total,
        "max": 100,
        "verdict": verdict,
        "dimensions": {
            "hook": {"score": hook["score"], "max": 40,
                     "suggestions": hook["suggestions"]},
            "structure": {"score": struct, "max": 25, "notes": struct_notes},
            "value": {"score": value, "max": 20, "notes": value_notes},
            "cta": {"score": cta, "max": 15, "notes": cta_notes},
        },
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

    print(json.dumps(score_post(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv)
