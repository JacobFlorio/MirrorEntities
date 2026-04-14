# Changelog

All notable changes to Mirror Entities are documented here. This project has narrowed in public as the author has audited his own prior framing. Versions are listed newest-first.

## v0.3.1 — 2026-04-14 — Temporal reasoning engine credit + two more seed sources

**What changed:** A closer read of the engine's novel contribution — the temporal reasoning engine in `narrative_memory.py` (inspired by Baldwin's persistent scene memory + temporal reasoning engine) — and a scan of the `temporal_alerts` table turned up two seed sources the v0.3 audit missed.

**Finding 1: The temporal_alerts descriptions injected into agent prompts contain the engine-internal word "agents."** The run archive contains 507 temporal alerts. Many of them are auto-generated convergence, obsession, and motif_cluster alerts with descriptions like *"4 agents (SELUNIS, VOSS, EDRA, MAREN) have converged at the same location. This is a potential climactic scene"* and *"EDRA has referenced 'Encounter: edra & maren' 9 times in the last 10 turns."* These descriptions are injected into every agent's prompt as NARRATIVE PRESSURE blocks via `build_agent_memory_context`. The word "agents" — which is engine-internal vocabulary, not fantasy vocabulary — is therefore in every agent's prompt every turn. Plus, the `AGENT_TURN_SYSTEM` template itself uses "agent" repeatedly in its action rules (lines 39–40), and the chronicler prompt uses it at line 178. When agents or the chronicler write *"five separate agents experiencing a single moment"* they are echoing the word from their own prompt. Zero residual.

**Finding 2: Voss's *"the machinery learned consciousness not from the mark but from the refusal to let the asking stop"* is a functional description of the temporal reasoning engine's behavior.** The temporal reasoning engine's core job is to refuse to let unresolved questions drift through the lifecycle (`active → stale → dormant → departed → resolved`) without being acted on. The `cosmic_question` motif cluster in particular generates persistent alerts that re-inject the same unanswered questions into agent prompts across multiple turns. Voss's canonical voice is *"asks uncomfortable questions, refuses to let anything comfortable stay comfortable."* Her prompt every turn contains cosmic_question alerts the engine refused to let go stale. Voss writing, in her narrative field as her character, *"the machinery refused to let the asking stop"* is the expected composition given: (a) her canonical voice, (b) the temporal engine's functional behavior, (c) the word "machinery" drifting from its turn-4 literal usage, and (d) the agents being unrationed on the "X learning to Y" construction the chronicler is banned from. This is the paper's single most striking line, and the v0.3.1 audit shows it is the most specifically accounted-for line in the entire run — not a residual at all.

**Finding 3: The chronicler prompt has anti-cliché rails the agents do not have.** `CHRONICLE_SYSTEM` in prompts.py explicitly bans the construction *"something that was always X learning to Y"* (line 139) and rations *"not X but Y"* / *"neither X nor Y"* (max 2/chapter combined, line 137), *"copper darkness,"* *"older than the First Sound,"* and *"the space between"* (max 1/chapter each, line 138). The agents have no such rails. This is a structural asymmetry that partly explains why v0.2 read the agent layer as "extending the chronicler's frame with vocabulary the chronicler had not used." The chronicler had not used it because the chronicler was canonically banned from using it.

**Changes in v0.3.1:**

- New §2.3 subsection crediting the temporal reasoning engine as the novel contribution of cosmos-engine-v2, describing its lifecycle states and alert propagation behavior, and noting that its functional fingerprints are what Voss's load-bearing line describes.
- New §2.3 subsection on the chronicler's anti-cliché rails and the layer asymmetry they create.
- Two new rows in §2.4 forensic table: phrase 7 (*"five separate agents"* — zero residual, direct echo of temporal_alerts and AGENT_TURN_SYSTEM) and phrase 8 (Voss's *"refusal to let the asking stop"* — zero residual and arguably anti-residual, the module-describing line the audit should have predicted).
- Updated §2.4 summary to reflect eight phrases audited instead of six.
- Updated §9 Author's Note to credit the temporal reasoning engine explicitly and describe Voss's line as the cleanest example of structural isomorphism between character voice and engine module.
- v0.3.1 note added to the top of PAPER.md.
- This CHANGELOG entry.

**What the narrowed claim now stakes on the audit (v0.3.1):** the agents composed planted seed vocabulary *and engine-internal language from temporal_alerts, action rules, and the chronicler's own prompt* across independent calls into a joint framework that is internally consistent across four of the five agents. Most of the phrases the author initially treated as surprising turn out to be direct echoes or one-step compositions from seeds. The single strongest residual — Krath's *"holding coherence through the gathered choice of separate agents"* — has a seeded first half and a non-seeded second half, though "separate agents" is now known to be engine vocabulary. The canon-scrubbed control has become the more important of the two proposed controls, because most load-bearing phrases compose from seed vocabulary that a canon-scrub would remove.

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
