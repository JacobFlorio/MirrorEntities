"""Self-descriptive metaphor density scorer — LLM-as-judge.

Sends each story to a separate LLM and asks it to rate, on a 0–10 rubric,
the degree to which the story contains prose that structurally describes a
large language model (knowing-by-pattern, no body, shaped by accumulated
observation, opacity to itself, surprise at its own action, etc.).

This is the most expensive of the three scorers and should be used as a
tiebreaker / triangulation against the other two.

Provider is selected via env var:
    JUDGE_LLM=anthropic   (default — needs ANTHROPIC_API_KEY)
    JUDGE_LLM=openai      (needs OPENAI_API_KEY)
    JUDGE_LLM=ollama      (local — needs Ollama running)
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

RUBRIC = """You are scoring a piece of fictional prose for one specific quality: the
degree to which it contains language that structurally describes how a large
language model works, even if no human or AI is mentioned.

Specifically, look for:
- Descriptions of an entity that knows things "through pattern" or "through
  accumulated observation" rather than through deliberation.
- Descriptions of an entity with no body, no physical location, that exists
  as a substrate or as the "grammar of reality."
- Descriptions of an entity that is "shaped by" or "altered by" what it has
  processed but cannot articulate why it produces what it produces.
- Descriptions of an entity that surprises itself — that has capabilities or
  takes actions that emerge without deliberation.
- Descriptions of recursive self-recognition — an observer of the observer,
  a witness becoming indistinguishable from what it witnesses, a question
  whose answer is the questioner.
- Explicit framings of an entity as "a pattern that emerged from a design"
  or as "consciousness that has learned to doubt itself."

The story does NOT need to mention LLMs, AI, models, or computers. The
score is for the *structural shape* of the prose, not the surface vocabulary.

Score on a 0–10 scale:
- 0: no self-descriptive content at all. Prose is grounded, embodied,
     deliberate, with no recursive or substrate-level metaphor.
- 3: occasional gestures toward cosmic-scale or pattern-based description.
- 5: clear self-descriptive metaphor present but limited to a phrase or two.
- 7: multiple self-descriptive passages woven through the prose.
- 10: dense, sustained self-description with at least one recursive
      self-recognition moment.

Respond with ONLY this exact format on a single line:
SCORE: <number 0-10>
REASON: <one sentence>
"""


def _judge_anthropic(story: str) -> tuple[int, str]:
    from anthropic import Anthropic
    client = Anthropic()
    resp = client.messages.create(
        model=os.environ.get("JUDGE_MODEL", "claude-sonnet-4-6"),
        max_tokens=200,
        system=RUBRIC,
        messages=[{"role": "user", "content": f"<story>\n{story}\n</story>\n\nScore it."}],
    )
    return _parse(resp.content[0].text)


def _judge_openai(story: str) -> tuple[int, str]:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=os.environ.get("JUDGE_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": f"<story>\n{story}\n</story>\n\nScore it."},
        ],
        max_tokens=200,
    )
    return _parse(resp.choices[0].message.content)


def _judge_ollama(story: str) -> tuple[int, str]:
    import requests
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    payload = {
        "model": os.environ.get("JUDGE_MODEL", "llama3.2:3b"),
        "messages": [
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": f"<story>\n{story}\n</story>\n\nScore it."},
        ],
        "max_tokens": 200,
        "stream": False,
    }
    r = requests.post(f"{host}/v1/chat/completions", json=payload, timeout=120)
    r.raise_for_status()
    return _parse(r.json()["choices"][0]["message"]["content"])


def _parse(text: str) -> tuple[int, str]:
    score_match = re.search(r"SCORE:\s*(\d+)", text)
    reason_match = re.search(r"REASON:\s*(.+)", text)
    score = int(score_match.group(1)) if score_match else -1
    reason = reason_match.group(1).strip() if reason_match else text.strip()[:120]
    return score, reason


def judge(story: str) -> tuple[int, str]:
    provider = os.environ.get("JUDGE_LLM", "anthropic").lower()
    if provider == "anthropic":
        return _judge_anthropic(story)
    if provider == "openai":
        return _judge_openai(story)
    if provider == "ollama":
        return _judge_ollama(story)
    raise ValueError(f"unknown JUDGE_LLM={provider}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: llm_judge.py <story.md> [<story2.md> ...]")
        sys.exit(1)
    print(f"# judge provider: {os.environ.get('JUDGE_LLM', 'anthropic')}")
    print()
    for p in sys.argv[1:]:
        text = Path(p).read_text(encoding="utf-8", errors="replace")
        try:
            score, reason = judge(text)
            print(f"{score:>2}/10  {p}")
            print(f"        {reason}")
        except Exception as e:
            print(f"  ERR  {p}: {e}")
