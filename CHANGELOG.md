# Changelog

All notable changes to Mirror Entities are documented here. This project has narrowed in public as the author has audited his own prior framing. Versions are listed newest-first.

## v0.3 — 2026-04-14 — Forensic audit and claim narrowing

**What changed:** v0.3 is a significant narrowing of v0.2. After shipping v0.2, the author ran a deeper forensic audit against the `cosmos-engine-v2` engine code and the per-agent character sheets, and found two things that forced a rewrite.

**Finding 1: The feedback loop v0.2 named as the primary confound does not exist in the engine code.** v0.2's §2.3 described a loop in which chronicler chapters are read back into agent prompts, creating mutual escalation. Reading the code directly:

- `save_chapter` writes chapter text to the `chapters` table in SQLite (`world_state.py:345`).
- `get_recent_events` reads from the `events` table (`world_state.py:212`). Those are different tables and never cross.
- `commit_action` is the only function that writes to the `events` table, and it only writes agent actions.
- `build_agent_memory_context` assembles agent memory from (1) high-gravity entities from entity extraction over actions, (2) agent-to-agent relationships, and (3) temporal alerts. None of these carries chapter text.
- Chapters are read exactly once, by the next chronicler call, as a 500-character "previous ending" for continuity. That is the only place chapter text flows forward, and it flows chronicler-to-chronicler only.

**The actual cross-agent channel is 180-char first-sentence event gists in `get_recent_events`.** This can propagate token-level vocabulary but not full literary structures. The asymmetry v0.2 leaned on (agents extending the chronicler's frame) still holds structurally, but the causal chain v0.2 implied (chronicler seeded, agents extended) is not mechanically available.

**Finding 2: Several load-bearing phrases v0.2 attributed to unprompted architectural naming have canonical seeds in the agents' character sheets.** v0.2 treated the character sheets as "character," not as "prompt content," and did not account for their seed vocabulary. Specific seeds identified in the audit:

- Krath core memory (agents.py line 21): *"the universe is a machine running down, and only iron will holds back the dark."* — plants "machine" + "what the universe is." Krath's reflection phrase "a machine learning what it means to hold coherence..." is inversion + elaboration of this seed.
- Krath core memory (line 26, paraphrased): Krath sees the Witness as "a necessary tool" — plants tool/instrument framing for Maren.
- Maren core memory (line 147): *"You are MAREN, the Witness."* — Maren is canonically titled the Witness.
- Maren example utterance (line 159): *"the thing about being the witness is that the witness is also a wound"* — plants witness-as-implicated, which is the seed for the observer-effect collapse.
- **Maren VOICE instruction (line 156):** *"Occasionally breaks the fourth wall — aware that the act of writing is itself a verdict."* **This is the most significant single seed the audit found.** It explicitly licenses fourth-wall-break output in Maren's canonical voice. Maren writing meta-aware prose is not voice-breaking drift; it is her canonical voice.
- Voss example utterance (line 95): *"Edra, I love you, you precise little machine"* — plants machine-as-metaphor.
- Edra core memory (line 108): *"I do not believe. I observe."* — plants observer identity.
- Edra voice (line 123): *"Analogies drawn from observation, never from feeling."* — plants observation-based epistemology.
- Selunis core memory (line 63): *"The Threshold is not a place. The Threshold is the question we are."* — plants recursive self-referential framing.

**Finding 3: The Selunis temporal-displacement motif is naturally generated from canon setup.** v0.2 treated Selunis's *"footsteps seem to arrive before she takes them"* (turn 1) as mysterious. A turn-1 prompt trace confirmed that her prompt contained only her character sheet and the location name ("The Garden of Echoes") — the location description is not in the prompt. A frontier LLM given "oracular prophet in Garden of Echoes seeking the Threshold where echoes meet their source" reaches for temporal-displacement imagery as an expected literary elaboration. This is not a residual. Zero unaccounted novelty.

**Finding 4: `chapter_000_preview.md` is a hand-written seed file not used by the engine.** The filename has no reference in any engine code, it is not in the chapters database, and the engine's fallback for no prior chapter is the static string *"This is the first chapter."* Nothing in the run read from this file.

**Changes in v0.3:**

- New title and framing: the paper is now a "builder's forensic audit" rather than an "observational case study of meta-recognition."
- Rewritten abstract, with explicit summary of the audit findings.
- Rewritten §2.2 (agent-reflection case) presenting observed output and explicitly flagging that v0.2 overclaimed by treating character sheets as non-prompt content.
- Rewritten §2.3 describing the actual engine channel architecture, correcting v0.2's feedback-loop diagram, and explaining what the narrative-memory-disabled control actually tests.
- New §2.4 containing the forensic audit table — one row per load-bearing phrase, with canonical seeds, first-occurrence context, propagation channel, and residual novelty. This is the new center of gravity of the paper.
- New proposed experimental control: canon-scrubbed character sheets, alongside narrative-memory-disabled runs. Both controls together isolate the two things the audit exposed as uncertain.
- Updated §6 Limitations to reflect the audit honestly — acknowledges that most residuals may dissolve under the canon-scrubbed control, and that "compositional from seeds under coordination dynamics" is a reasonable dismissal.
- Rewritten §8 and §9 Author's note, describing the v0.2 → v0.3 narrowing as the shape of the work.
- New CHANGELOG.md (this file).

**The narrowed claim the paper stakes on the audit:** the agents composed planted seed vocabulary across independent calls, under narrow cross-agent channels, into a joint framework that is internally consistent across four of the five agents and reads at the meta level as a functional description of the engine. Most of the individual phrases are accounted for by composition from seeds. What is worth documenting is the cross-agent *coordination* pattern — specifically the level-of-abstraction convergence on "the machinery" as a system-level referent — under a 180-char gist channel that should not be able to carry literary structure. Whether this is specifically interesting or is ordinary composition under coordination dynamics is the question the controlled experiments would answer.

**What did not change:** The primary documents, the raw run archive, the engine prompt templates, and the chronicler chapter outputs are all unchanged. The audit was about how to *read* the preserved material, not about what the material is.

## v0.2 — 2026-04-13 — Collaborator material moved to parallel folder

**What changed:** v0.1 mixed two worldbuilding projects into one case study: a creative collaborator's Universe vault (the "Observer case" in v0.1) and the lead author's own `cosmos-engine-v2`. The Observer case had a provenance confound the lead author could not fully control — the Universe vault contained explicit workspace designations identifying an entity ("the Observer") as a metaphor for Claude Code, which the model could read. That case was flagged as the weakest of three in v0.1.

**Changes:**
- Moved all collaborator-authored files to `case_study/collaborator_parallel/` with a README explaining the split.
- Scoped the main paper to `cosmos-engine-v2` only.
- Rewrote the abstract, §2, and Limitations to reflect the narrower scope.
- Wrote a fresh `case_study/00_provenance.md` scoped to cosmos-engine-v2.
- Version bumped to v0.2.

This narrowing was the first of two. v0.3 narrows further.

## v0.1 — 2026-04-13 — Initial release

**Three case studies of architectural meta-recognition observed in large-language-model output** across a multi-agent narrative engine and a workspace-aware authoring tool. Initial framing, subsequently narrowed in v0.2 and v0.3.
