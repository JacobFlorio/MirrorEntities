# Full cosmos-engine-v2 run archive

This folder contains the **complete primary record** of the cosmos-engine-v2 run that produced the chapter and reflection material analyzed in Cases 2 and 3 of `PAPER.md`. It is preserved here in full — not curated, not selected, not filtered — so any reader who wants to verify the case-study analysis against the *negative space* (chapters and turns where nothing meta-architectural happens) can do so without trusting our curation.

## What's in here

```
full_v2_run/
├── chapters/                    9 chapter files synthesized by the chronicler
│   ├── chapter_000_preview.md       seed preview chapter
│   ├── chapter_001.md
│   ├── chapter_002.md
│   ├── chapter_003.md
│   ├── chapter_004.md
│   ├── chapter_005.md
│   ├── chapter_006.md
│   ├── chapter_007.md
│   └── chapter_008.md
│
├── raw_outputs/                 835 turn-by-turn raw model outputs
│   ├── 00001_agent_*.txt            agent JSON outputs from turn 1
│   ├── ...
│   ├── 00161_agent_*.txt            agent JSON outputs from turn 161+
│   ├── ...                          (160+ turns × 5 agents per turn)
│   └── 00060_chronicle_maren_*.txt  chronicle synthesis raw outputs
│
└── cosmos_world.db              the engine's SQLite state at end of run
                                  contains entities, events, narrative_memory,
                                  reflection records, etc. — the full state the
                                  chronicler and agents were reading from
```

## Why we are including the negative space

The annotations in `case_study/12_annotated_v2_chronicler.md` and `case_study/14_annotated_v2_agent_recognition.md` discuss specific chapters (1, 3, 4, 8) and specific raw outputs (Krath reflection, Maren turn 150, Voss turn 108). A skeptical reader could reasonably ask: *"What about the chapters and turns you didn't quote? Were those equally meta-architectural? Or did you cherry-pick the strongest few?"*

**That is the right question to ask, and we want any reader who wants to ask it to be able to answer it themselves without having to trust our summary.** The full archive is here so:

- **Chapter 0, 2, 5, 6, 7** are also in this folder. Read them. Compare against the annotated chapters. Form your own judgment about how cherry-picked our selection was. (Our honest read is that the meta-architectural language is *most concentrated* in chapters 1 and 8 but *present to varying degrees* throughout the run — but you should not have to take our word for that.)
- **All 835 raw outputs** are here. The Krath reflection we annotated is one of many reflection turns. The Maren and Voss turns we quoted are also two of many. If you want to grep the entire raw output archive for self-referential phrases and see how often they actually appear vs how often we cited them, you can do that.
- **The SQLite database** (`cosmos_world.db`) contains the full state of the engine at the end of the run — entities, events, narrative memory, reflection records, relationships. If you want to reconstruct what each agent could see in their context window at any given turn, the data is here.

## Sizing

About 9 MB total. Trivial for git but worth knowing if you're cloning over a slow connection.

## What this archive is NOT

It is not a complete record of every cosmos-engine-v2 run the author has ever done. It is the record of **one run** — the run that produced the chapters and reflections the case study analyzes. Other runs may have produced similar material, similar to a different degree, or no material like it at all. We have not preserved or analyzed other runs in this repo. Adding more runs is on the v0.2 roadmap.

## Honesty caveat

The author has been running cosmos-engine-v2 for a while and has multiple runs across multiple worlds. The choice to include *this specific run* and not other runs is itself a curation decision and a confound. The honest reader should treat this archive as **one example of a phenomenon the author noticed across multiple runs**, not as a controlled sample of all runs. The right way to address this confound is to run the engine systematically across many worlds, with and without the narrative-memory feedback loop, and report the rate at which meta-architectural language appears. That is the v0.2 experimental work.
