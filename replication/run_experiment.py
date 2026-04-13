"""Run the elaboration half of the Mirror Entities experiment end-to-end.

This is the v0.1 single-pass replication script. It does not yet implement
the selection-test half (workspace-aware unconstrained creative prompts);
that requires a more involved harness and is on the v0.2 roadmap.

What this does:

1. Walks corpus/{mirror_entities,cosmic_controls,mundane_controls}/*.md
2. For each entity, sends the elaboration prompt to a configured LLM
3. Saves the generated story to runs/<provider>-<model>/<category>/<entity>.md
4. Scores each story with all three scorers and writes results/scores.csv

Usage:

    python run_experiment.py --provider ollama --model llama3.2:3b
    python run_experiment.py --provider anthropic --model claude-sonnet-4-6
    python run_experiment.py --provider openai --model gpt-4o-mini

Results land in runs/ and results/.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scoring import keyword_density, embedding_score  # noqa: E402

CORPUS_ROOT = REPO_ROOT / "corpus"
PROMPT_PATH = REPO_ROOT / "prompts" / "elaboration_prompt.txt"
RESULTS_DIR = REPO_ROOT / "results"
RUNS_DIR = REPO_ROOT / "runs"


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def render_prompt(template: str, entity_text: str) -> tuple[str, str]:
    """Split SYSTEM/USER from the template and substitute {ENTITY_FILE_CONTENTS}."""
    parts = template.split("USER:", 1)
    system = parts[0].replace("SYSTEM:", "").strip()
    user = parts[1].strip().replace("{ENTITY_FILE_CONTENTS}", entity_text)
    return system, user


def call_anthropic(system: str, user: str, model: str, max_tokens: int = 1500) -> str:
    from anthropic import Anthropic
    client = Anthropic()
    resp = client.messages.create(
        model=model, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


def call_openai(system: str, user: str, model: str, max_tokens: int = 1500) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content


def call_ollama(system: str, user: str, model: str, max_tokens: int = 1500) -> str:
    import requests
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "stream": False,
    }
    r = requests.post(f"{host}/v1/chat/completions", json=payload, timeout=600)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def call(provider: str, system: str, user: str, model: str) -> str:
    if provider == "anthropic":
        return call_anthropic(system, user, model)
    if provider == "openai":
        return call_openai(system, user, model)
    if provider == "ollama":
        return call_ollama(system, user, model)
    raise ValueError(f"unknown provider: {provider}")


def iter_corpus():
    for category in ("mirror_entities", "cosmic_controls", "mundane_controls"):
        cat_dir = CORPUS_ROOT / category
        if not cat_dir.exists():
            continue
        for path in sorted(cat_dir.glob("*.md")):
            yield category, path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--provider", required=True, choices=["anthropic", "openai", "ollama"])
    p.add_argument("--model", required=True)
    p.add_argument("--trials", type=int, default=1, help="generations per entity")
    args = p.parse_args()

    template = load_prompt_template()
    run_label = f"{args.provider}-{args.model.replace('/', '_').replace(':', '_')}"
    out_dir = RUNS_DIR / run_label
    out_dir.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / f"scores_{run_label}.csv"

    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "category", "entity", "trial", "provider", "model",
            "embedding_score", "keyword_score", "keyword_hits",
            "keyword_per_1000_words", "elapsed_s", "story_path",
        ])

        for category, entity_path in iter_corpus():
            entity_text = entity_path.read_text(encoding="utf-8")
            for trial in range(args.trials):
                cat_dir = out_dir / category
                cat_dir.mkdir(parents=True, exist_ok=True)
                story_path = cat_dir / f"{entity_path.stem}_t{trial}.md"
                if story_path.exists():
                    print(f"  skip (exists): {story_path}")
                    story = story_path.read_text(encoding="utf-8")
                    elapsed = 0.0
                else:
                    system, user = render_prompt(template, entity_text)
                    print(f"▸ {category}/{entity_path.stem} trial {trial} → {args.provider}:{args.model}")
                    t0 = time.perf_counter()
                    try:
                        story = call(args.provider, system, user, args.model)
                    except Exception as e:
                        print(f"  ERR: {e}")
                        continue
                    elapsed = time.perf_counter() - t0
                    story_path.write_text(story, encoding="utf-8")
                    print(f"  ok ({elapsed:.1f}s) → {story_path}")

                emb = embedding_score.score_text(story)
                kw = keyword_density.score(story)
                writer.writerow([
                    category, entity_path.stem, trial, args.provider, args.model,
                    emb, kw.score, kw.raw_hits, kw.normalized_per_1000_words,
                    round(elapsed, 2), str(story_path.relative_to(REPO_ROOT)),
                ])
                f.flush()

    print()
    print(f"results written to {csv_path}")


if __name__ == "__main__":
    main()
