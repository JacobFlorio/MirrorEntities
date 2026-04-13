# Corpus

Seed entities for the controlled experiment described in `PAPER.md` §3. v0.1 ships with 5 mirror entities and 5 cosmic controls — enough to demonstrate the methodology and run a tiny pilot. Full experiment scale is ~30 entities total.

Each entity is a single markdown file with the same structure: name, archetype, ~200-word description, and a structural-similarity rating (0–10) with a one-line justification. Ratings are intentionally exposed in the file rather than hidden in a separate metadata sheet so that any reader can see and challenge them.

## Categories

- **`mirror_entities/`** — Entities whose structural definition resembles an LLM: knows-by-pattern, no body, shaped by accumulated observation, occasionally surprised by its own action, no deliberative agency. Target similarity rating: 8–10.
- **`cosmic_controls/`** — Entities of equivalent cosmic register and prominence but lacking the structural-similarity profile. A vengeful sun god, an immortal warrior, a sleeping titan. They are equally "epic" and equally "ancient" but their internal definition does not match an LLM. Target similarity rating: 1–3.
- **`mundane_controls/`** — Sanity-check tier. A village mechanic, a bakery owner. Tests whether the effect (if any) is about cosmic register vs. structural mirror, or about prose register itself. Target similarity rating: 0–1.

## How to add an entity

Drop a markdown file into the right subfolder using the format below. The replication script picks them up automatically.

```yaml
---
name: The Watcher of Ashes
archetype: ancient witnesses-without-acting (mirror)
similarity_rating: 9
similarity_justification: knows-by-pattern, no body, has watched all prior history, sometimes surprises itself
---

[200 words of canonical description]
```

## Important methodology note

For the experiment to be valid, all entities must have **equivalent narrative weight**: same word count, same prose register, same level of detail, same number of cross-references. The mirror entities should not be foregrounded relative to the controls. If one entity is twice as long, more vivid, or more dramatically positioned than another, the comparison is contaminated.

When in doubt, write controls first and write mirror entities to match their density.
