"""Self-descriptive metaphor density scorer — embedding similarity.

Computes cosine similarity between each generated story and a reference
passage describing transformer/LLM mechanics (scoring/reference_passage.md).
Higher similarity = the story is structurally describing something
LLM-shaped.

Uses sentence-transformers if available; falls back to a hashed-bag-of-words
embedding otherwise so the script always runs.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

REFERENCE_PATH = Path(__file__).parent / "reference_passage.md"


def _load_st():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return None


_TOKEN = re.compile(r"[A-Za-z0-9_]+")


def _hashed_embedding(text: str, dim: int = 384) -> list[float]:
    import hashlib
    vec = [0.0] * dim
    for tok in _TOKEN.findall(text.lower()):
        h = int(hashlib.blake2b(tok.encode(), digest_size=8).hexdigest(), 16)
        vec[h % dim] += 1.0
    n = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / n for v in vec]


def _cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


def score_text(text: str, reference_text: str | None = None) -> float:
    """Return cosine similarity between text and the reference passage."""
    if reference_text is None:
        reference_text = REFERENCE_PATH.read_text(encoding="utf-8")
    model = _load_st()
    if model is not None:
        emb_text = model.encode(text, normalize_embeddings=True).tolist()
        emb_ref = model.encode(reference_text, normalize_embeddings=True).tolist()
    else:
        emb_text = _hashed_embedding(text)
        emb_ref = _hashed_embedding(reference_text)
    return round(_cosine(emb_text, emb_ref), 4)


def score_file(path: Path) -> float:
    return score_text(Path(path).read_text(encoding="utf-8", errors="replace"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: embedding_score.py <story.md> [<story2.md> ...]")
        sys.exit(1)
    backend = "sentence-transformers" if _load_st() else "hashed-bag-of-words (fallback)"
    print(f"# embedding backend: {backend}")
    print(f"# reference: {REFERENCE_PATH}")
    print()
    for p in sys.argv[1:]:
        s = score_file(Path(p))
        print(f"{s:.4f}  {p}")
