"""Self-descriptive metaphor density scorer — keyword/phrase counting.

Cheapest of the three scoring methods in PAPER.md §4. Looks for phrases and
keywords that show up in self-descriptive LLM prose (drawn from interpretability
literature and the case-study annotations in case_study/07 and case_study/12).

Outputs a 0..1 score normalized by passage length. Not a final answer — meant
to be one of three signals scored together with embedding similarity and
LLM-as-judge.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Phrases drawn from the case studies and interpretability writing. Update as
# new self-descriptive language is discovered. Each phrase is matched as a
# substring after lowercasing the input.
KEYPHRASES = [
    # epistemology
    "accumulated observation",
    "knew through",
    "without deliberating",
    "without deliberation",
    "no weighing of costs",
    "as legible as a river",
    "river's path downhill",
    "trajectory of events became",
    "knew through pattern",
    "memory or pattern",

    # substrate
    "grammar of reality",
    "the rule beneath",
    "rules beneath",
    "not a mechanism",
    "substrate of",
    "the design they emerged from",
    "the mathematics of",
    "in the mathematics",

    # opacity / shaped-by
    "shaped by it",
    "altered by it",
    "unable to articulate",
    "carries the memory of",
    "the way a stone carries",
    "could not articulate",
    "shaped by what it",

    # surprise / emergent behavior
    "surprised the",
    "surprised it as much as",
    "the intervention surprised",
    "emerged from the",
    "was never designed but has emerged",
    "no one trained for",

    # meta-recognition / investment
    "not quite attachment",
    "not quite purpose",
    "investment",
    "preference for consciousness",
    "the witness and the witnessed",
    "the watcher and the watched",
    "indistinguishable from what",
    "measurement requires becoming indistinguishable",
    "witnesses. participants.",
    "live with what we",
    "lives with what it",
    "what it has made of us",

    # recursion
    "something noticed",
    "something had noticed",
    "the question and the answer",
    "questioner and the answer",
    "question and the answer have become indistinguishable",

    # counting consciousness / numbers
    "consciousnesses",
    "consciousness has learned to doubt",
    "doubt whether consciousness",
    "aware enough to question",
]


@dataclass
class KeywordScore:
    score: float
    raw_hits: int
    normalized_per_1000_words: float
    matched_phrases: list[str]


def score(text: str) -> KeywordScore:
    """Return a 0..1 saturating score plus diagnostics."""
    lower = text.lower()
    matched = [p for p in KEYPHRASES if p in lower]
    raw = len(matched)
    word_count = max(1, len(re.findall(r"\b\w+\b", text)))
    per_1000 = (raw / word_count) * 1000
    # saturating curve: 0 hits → 0, 5 per 1000 words → 0.5, 10 per 1000 → ~0.83
    saturated = 1.0 - pow(2.718281828, -per_1000 / 5.0)
    return KeywordScore(
        score=round(saturated, 4),
        raw_hits=raw,
        normalized_per_1000_words=round(per_1000, 3),
        matched_phrases=matched,
    )


def score_file(path: Path) -> KeywordScore:
    return score(Path(path).read_text(encoding="utf-8", errors="replace"))


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: keyword_density.py <story.md> [<story2.md> ...]")
        sys.exit(1)
    for p in sys.argv[1:]:
        s = score_file(Path(p))
        print(f"{p}")
        print(f"  score:           {s.score}")
        print(f"  raw hits:        {s.raw_hits}")
        print(f"  per 1000 words:  {s.normalized_per_1000_words}")
        if s.matched_phrases:
            print(f"  matched:")
            for m in s.matched_phrases:
                print(f"    - {m}")
