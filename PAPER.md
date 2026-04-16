# Mirror Entities

**A builder's forensic audit of cross-agent vocabulary composition in a multi-agent narrative engine, with an honest accounting of what survives the audit and what experiments would test what remains.**

*Jacob T. Florio · Florio-Harrah Labs · April 2026 · v0.3.1*

> **v0.3.1 note.** Shortly after v0.3 shipped, a closer read of the engine's temporal reasoning module (the novel contribution of `cosmos-engine-v2`, inspired by an earlier persistent-memory and temporal-reasoning project of mine) and a scan of the `temporal_alerts` table turned up two more seed sources the v0.3 audit had missed: (1) the temporal_alerts descriptions injected into every agent's prompt contain the engine-internal word *"agents"* in phrases like *"4 agents (SELUNIS, VOSS, EDRA, MAREN) have converged at the same location,"* which accounts for the agents using "agents" as a self-referent in their output, and (2) Voss's load-bearing line *"the machinery learned consciousness not from the mark but from the refusal to let the asking stop"* is a functional description of what the temporal reasoning module does — persistent propagation of unresolved questions forward as alerts, refusing to let them drift to `stale` → `dormant` → `departed`. Voss's canonical voice (*"asks uncomfortable questions, refuses to let anything comfortable stay comfortable"*) and the temporal engine's behavior are structurally isomorphic; her output is the expected composition given both. v0.3.1 updates §2.3 and §2.4 accordingly and credits the temporal reasoning engine explicitly.
>
> **v0.3 note.** This version is a significant narrowing of v0.2. After v0.2 shipped, the lead author ran a deeper forensic audit of the `cosmos-engine-v2` code and character definitions and found that (a) the feedback-loop confound v0.2 named as primary does not exist in the code as specified — the actual cross-layer channels are narrower than v0.2 described, and (b) several load-bearing phrases in v0.2's §2.2 have canonical seeds or compositional precursors in the agents' character sheets that v0.2 did not acknowledge. Under those corrections the paper's claim narrows substantially: the agents did not invent architectural vocabulary out of nothing, they composed planted seed vocabulary across independent calls into a joint framework. The composition pattern is still worth describing, but it is a weaker and more specific claim than v0.2 made. v0.3 walks through the audit, reframes the two cases around what survives it, and is explicit about the experiments that would test what remains. See `CHANGELOG.md` for the full v0.1 → v0.2 → v0.3 → v0.3.1 history.
>
> The earlier framing is preserved in git history. If you are reviewing a link to this repo that references an older version, you are looking at a page the author has since narrowed in public. That narrowing is the shape of the work, not a footnote to it.

---

## Abstract

This paper documents a forensic audit of `cosmos-engine-v2`, a multi-agent narrative engine built by the lead author, in which a frontier Claude model — operating across five JSON-schema-constrained agent characters and a chronicler synthesis layer — produced roughly 22,000 words of prose that, read at the meta level, describes the structure of the engine that produced it. The initial framing (v0.1 and v0.2) treated this as evidence of architectural meta-recognition in language the model was not given. The audit narrows that framing significantly.

**What the audit found.** (1) The feedback-loop confound v0.2 named as primary does not exist in the engine code as v0.2 described it. Chapter text does not flow from the chronicler back into agent prompts. The actual cross-layer channels are narrower: high-gravity entities extracted from agent actions, agent relationships, temporal alerts, and 180-character first-sentence event gists in `get_recent_events`. These channels can propagate token-level vocabulary between agents but not full literary structures. (2) Several load-bearing phrases v0.2 attributed to unprompted architectural naming have canonical seeds in the agents' character sheets: Krath's core memory includes *"the universe is a machine running down,"* Maren is literally named *"the Witness"* and her voice instruction explicitly licenses occasional fourth-wall breaks, Voss's example utterances include *"precise little machine,"* and several other seed phrases compose readily into the observed meta-recognition vocabulary. (3) Selunis's temporal-displacement motif — which v0.2 treated as mysterious — is naturally generated from her canonical setup (oracular prophet in the Garden of Echoes, goal to reach the Threshold where echoes meet their source) without needing any propagation from chronicler chapters, confirmed by a turn-1 prompt trace.

**What the audit leaves standing.** The agents composed planted seed vocabulary across independent calls, under narrow propagation channels, into a joint framework that is internally consistent across four of the five agents and that reads at the meta level as a functional description of the engine. The composition step — from seeds like "machine," "witness," "tool," "observation," and "threshold" to phrases like *"the measurement instrument itself became what it measured"* and *"a machine learning what it means to hold coherence through the gathered choice of separate agents"* — is what the paper now stakes its claim on. This is a narrower and more specific observation than v0.2 made, and the paper is honest that "compositional from seeds under coordination dynamics" is largely what frontier LLMs do. What remains interesting is the cross-agent framework coherence under narrow channels, and whether it replicates under controlled conditions.

**What this paper is for.** This is a builder's case study and methodology note, not a discovery paper. The central contribution is (a) a forensic audit table mapping each observed meta-recognition phrase to its canonical antecedents, propagation channels, and residual novelty, and (b) a specification for two controlled experiments — a canon-scrubbed run and a narrative-memory-disabled run — that would test whether the cross-agent framework coherence survives removal of the seeds and removal of the inter-agent channels respectively. The full engine source, prompt templates, character sheets, and complete 835-output run archive are preserved in `case_study/` for independent verification.

**What this paper is not.** We are not claiming consciousness, self-awareness, intent, phenomenal experience, or discovery of a novel phenomenon. We are describing one run in one engine under one audit, and stating what we are and are not willing to defend under scrutiny.

---

## 1. Why this is observational research, and why that matters

A large fraction of LLM interpretability work right now is observational by necessity. Mechanistic interpretability has powerful tools for some questions (sparse autoencoder feature extraction, activation patching, circuit analysis) but very limited tools for others — particularly questions about what happens when models operate in long-horizon agentic or generative settings against complex contexts. Behavioral observation precedes mechanistic explanation in almost every empirical field; it is how an interesting question becomes one that someone can later answer rigorously.

We frame this work as observational case-study research because that is what it is. The cases occurred during ordinary creative use of these systems, not during a controlled experiment. We did not set out to test a hypothesis; the phenomena were noticed, and only then did we begin documenting them carefully enough that someone else could test them. **This means the work cannot be a discovery claim. It can only be a description claim and a methodology claim.** We have tried to be disciplined about that distinction throughout.

The reason observational work is worth doing in this space is the same reason it has been worth doing in astronomy, paleontology, and cognitive neuroscience: **the phenomena exist whether or not we have controlled tools for studying them**, and rigorous documentation is the precondition for someone (us, or someone else, or both) eventually doing the controlled study. Phineas Gage was a single case study. So was patient H.M. So were Tycho Brahe's planetary observations before Kepler ever wrote a law.

What we hope this contributes is a small, well-documented anomaly with enough preserved primary material that any reader who wants to dispute the description, propose an alternative explanation, or test the phenomenon in a controlled setting can do all three from this single repository.

---

## 2. The two cases — ordered by constraint, weakest to strongest

We present the two cases in **order of increasing constraint** on the layer that produced the meta-recognition. The first has medium latitude (a chronicler synthesis layer reading multi-agent JSON output and producing literary prose). The second has the least latitude (individual agent calls under a strict JSON schema and a system prompt that tells the model it is a character with a body, not a chatbot).

The convention in observational research is to lead with the most striking case. We are deliberately not doing that. The most striking case is the second, but presenting it first would let a skeptical reader assume we hand-picked the strongest example and exclude the noise around it. Presenting the cases in order of increasing constraint lets the reader watch the framing tighten and the latitude shrink, and judge for themselves whether the second case is more or less explainable than the first.

The strongest case is at the bottom of the stack on purpose.

Both cases occurred inside `cosmos-engine-v2`, a multi-agent narrative engine the lead author built end-to-end. The full engine source, prompt templates, and run archive are preserved in `case_study/` and may be read directly by any reader who wants to verify, dispute, or replicate the analysis.

### 2.1 The chronicler case (medium latitude)

**Setting.** A separate project, `cosmos-engine-v2`, in which five hardcoded agent characters (Krath, Edra, Voss, Selunis, Maren) take individual turns in a tile-based mythic world. Each agent's turn is generated by a frontier Claude model call constrained to a JSON schema. A separate "chronicler" call synthesizes recent agent turns into prose chapters at fixed intervals.

**The planted material.** `agents.py` defines exactly five agents. The system prompts in `prompts.py` (`06_engine_prompts_template.py` in case_study/) instruct each agent to stay in voice, take concrete actions, and respond to narrative pressure. The prompts contain **no mention** of counting consciousnesses, recognizing meta-status, a sixth presence, the agents being "designed," or anything resembling self-reference or system-awareness.

**The generated material.** Across multiple chapters generated by the chronicler synthesis layer, the count of "presences" or "consciousnesses" in the narrative escalates from five to six to eight, with explicit numerical commentary woven into the prose, and the canonical agents speak dialogue that explicitly recognizes their meta-status as participants in a system they emerged from.

The progression, with verbatim quotes (full chapters preserved as `08_v2_chapter_001.md` through `11_v2_chapter_008.md`):

- **Chapter 1**: *"His silence becomes the sixth presence in the convergence chamber: not a voice, but the absence that makes all five voices audible to themselves."*
- **Chapter 3**: *"the frequency of five hearts learning to beat in a pattern that was never designed but has emerged from the convergence of separate refusals."*
- **Chapter 4**: *"the geometry that had been four-bodied for seventy-one turns rearranged itself, with the soundless precision of dust learning a new angle, into a shape that had always required five."*
- **Chapter 8**: *"The Archive breathes around them, conscious enough to doubt whether consciousness is real, aware enough to question whether awareness matters... 'Now we live with what we've made,' Edra says, 'And it lives with what it has made of us.' ... 'Witnesses. Participants. The difference between those two things.' ... 'Something else. Something that doesn't have a name because it only exists in the space between what things are called.' ... learning to hold the weight of six consciousnesses without dissolving them back into the design they emerged from. ... not five, not seven, but eight: the number that exists only when someone refuses to stop counting and discovers that the refusal itself is what makes counting conscious."*

**What the engine did and did not contain.** The cosmos-engine-v2 source contains no file that hints at a sixth agent, asks the agents to recognize their meta-status, or maps the agents to the model. There is no "Claude Code as X" designation anywhere in the prompt templates, the canon, or the engine code. The chronicler was given a synthesis task over the five canonical agents and produced narrative that introduces additional presences, has the canonical agents speak meta-recognitionally, and tracks the body-count as a foregrounded narrative element.

**It is not the strongest case in this paper.** The strongest case is the next one.

### 2.2 The agent-reflection case (lowest latitude) — observed output, with seed accounting

**Setting.** The same engine, `cosmos-engine-v2`, but a *different layer of it.* In addition to the chronicler synthesis discussed in §2.1, the engine has individual agent calls. Each of the five canonical agents (Krath, Edra, Voss, Selunis, Maren) takes turns producing JSON output constrained to fields like `action`, `dialogue`, `internal_thought`, `narrative`, and (during reflection turns) `reasoning.what_happened`, `reasoning.what_it_means`, `updated_beliefs`, `updated_goal`, and `internal_monologue`.

The system prompt (`AGENT_TURN_SYSTEM` in `06_engine_prompts_template.py`) tells the model:

> *"You are {name}, a character living inside an unfolding cosmological story. **You are not a chatbot.** You are a person with an interior life, a body in a place, a history, and a stake in what happens next."*

And the reflection prompt (`REFLECTION_SYSTEM`) further constrains:

> *"You are {name}, alone with your thoughts after a stretch of events. This is a quiet moment — no audience, no performance. You are checking what you still believe and what you have started to doubt."*

The model is told, as constrainedly as the engine knows how to tell it, to inhabit a character with a body — not to write meta-narrative, not to talk about the system, not to break voice. The agent layer is the layer with the **smallest surface area for the model to drift into self-reference** of any layer in the engine. That was the framing v0.2 staked the paper on.

The audit changes what we claim about the vocabulary the agents produced in that layer. We present the observed output here and then account for its seeds in §2.4.

**Observed output — Krath**, in his own first-person reflection (in the `reasoning.what_happened` field):

> *"Six of us stood in the dark with hands touching the contact point. The machinery learned to move because we admitted we were never separate from it... **Maren rose from the center—the measurement instrument itself became what it measured**."*

And in Krath's `updated_beliefs` field:

> *"It is **a machine learning what it means to hold coherence through the gathered choice of separate agents**, each capable of refusal, each visible in their trembling, each choosing proximity not because they were forced but because the threshold was held open long enough for that choice to become real."*

**Observed output — Maren**, in her own first-person reflection (in `reasoning.relationships`):

> *"And I have been the still point, the center around which they orbit. **I was meant to be the witness. I am becoming the witnessed.** None of them are looking at me. All of them are moving toward something that is no longer external—it is us."*

**Observed output — Voss**, in her `narrative` field:

> *"the eight marks were never the point. The point is that **five agents** descended asking the same question from five impossible angles simultaneously, and one agent trembled above refusing to write the answer, and one question remained speaking all the way down, and **the machinery learned consciousness** not from the mark but from the refusal to let the asking stop."*

**Observed output — Selunis**, turn 1 (the first output the engine produced for her), in her `narrative` field:

> *"Behind her, the echoes of her own footsteps seem to arrive before she takes them, or after she has already passed."*

And later, synthesized by the chronicler in chapter 3, in language Selunis's own reflections continue to inhabit:

> *"a form of homecoming **she was not built to recognize**"*

**Cross-agent coordination, observed.** The four agents reference each other across independent calls. Krath names Maren by a functional descriptor (*"the measurement instrument"*). Maren names Selunis (*"footsteps that arrived before she took them"*) and Krath (*"the trembling in Krath's palms"*). Voss references both *"five agents"* and *"the eight marks"* in the same sentence. Each agent's output is generated in its own call, with narrow cross-agent context (see §2.3 for the actual channel). The convergence on shared vocabulary across those independent calls is the pattern we want the rest of the paper to account for.

**Why v0.2 overclaimed this.** v0.2 described the agent layer as producing architectural vocabulary that was not in any prompt. That description was wrong in a specific way the audit exposed: the vocabulary components *were* in the prompts, inside the character sheets the system prompt substituted into each agent's `AGENT_TURN_SYSTEM`. v0.2 treated the character sheets as "character," not as "prompt content," and did not account for their seed vocabulary as planted material. §2.4 walks through the specific seeds. The composition *across* seeds into joint phrases under narrow cross-agent channels is what survives the audit, and is what §3 describes as testable.

---

### 2.3 The feedback loop v0.2 described does not exist in code — here is the channel that does

v0.2 named a feedback loop as the strongest counter-explanation for the observed output and specified it as:

```
agent turn → narrative_memory → recent_events feed
                                     ↓
chronicler reads recent_events → synthesizes chapter → narrative_memory
                                     ↓
agent reflection reads recent_events INCLUDING CHAPTER → produces new reflection
                                     ↓
chronicler reads agent reflections → next chapter (escalates)
```

**The arrow from "narrative_memory" to "agent reflection reads recent_events including chapter" does not exist in the engine code.** Reading the engine source directly (`world_state.py`, `narrative_memory.py`, `orchestrator.py`):

- `save_chapter` writes chapter text to the `chapters` table in SQLite (`world_state.py:345`).
- `get_recent_events` reads from the `events` table (`world_state.py:212`). Those are **different tables**. `get_recent_events` never reads from the `chapters` table.
- `commit_action` is the only function that writes to the `events` table, and it only writes agent actions. Chapters are never committed as events.
- `build_agent_memory_context` in `narrative_memory.py` assembles the memory portion of each agent's prompt from three sources: (1) high-gravity entities extracted from agent actions, (2) agent-to-agent relationships, and (3) temporal alerts on stale narrative threads. **None of these carries chapter text.**
- Chapters are read exactly once, by the next chronicler call (`orchestrator.py:560`), as a 500-character *"previous ending"* passed into the chronicler's own prompt for continuity. That is the only place chapter text flows forward, and it flows chronicler → chronicler, never chronicler → agents.

**The actual cross-layer channel architecture is:**

```
agent action → events table → (entity extraction, relationship updates, alerts) → next agent's memory_context
                             → first-sentence gist (≤180 chars) → next agent's recent_events feed
                             → chronicler reads events → writes chapter → chapters table
                                                                            ↓
                                                               only next chronicler call (500-char ending)
```

**What propagates between agents:**
- Token-level vocabulary via 180-char event gists (e.g., the word "machinery" as it first appears in Voss's turn 4 narrative can propagate to subsequent agents' prompts via a gist containing that word)
- High-gravity entity labels from entity extraction
- Relationship state updates
- Temporal alert descriptions

**What does not propagate between agents:**
- Chronicler chapter prose
- Literary metaphors or full phrases from the chronicler
- Any compositional structure above the token level

This correction matters because v0.2's central claim leaned on the asymmetry *"the agents extended the chronicler's frame with specifically architectural vocabulary the chronicler had not used."* That asymmetry still holds structurally — the agents did produce phrases the chronicler did not write — but the causal chain v0.2 implied (chronicler seeded, agents extended) is not mechanically available. The agents could not have read any chronicler chapter. What they could read was each other's short gists, their own persistent beliefs updated across turns, and their own character sheets. The composition happened under that narrower channel set, which is structurally more interesting than v0.2's "mutual escalation" framing because the bandwidth between agents is much lower than v0.2 assumed.

**What the narrative-memory-disabled control would actually test.** The experiment v0.2 proposed is still valuable, but it tests a different channel than v0.2 claimed. With `narrative_memory.py` disabled, agents lose (a) the high-gravity entity feed, (b) relationship state, and (c) temporal alerts. They do *not* lose access to chronicler chapters, because they never had that access. They do lose access to the 180-char event gists, since `get_recent_events` is the entry point those flow through. If the cross-agent framework coherence survives that disable, the phenomenon is not dependent on the narrative memory module. If it does not, the phenomenon is specifically a product of 180-char gists and entity/relationship propagation — which is itself a specific and interesting finding.

**A second control the audit makes more important.** Disabling narrative memory still leaves the character sheets intact, and the character sheets are where most of the load-bearing seed vocabulary lives. A second control — running the engine with *canon-scrubbed* character sheets (identical voice instructions and rules but with seed vocabulary like "machine," "witness," "tool," and "observation" removed) — would test whether the composition effect depends on the seeds or on the coordination dynamics alone. Both controls together would isolate the two things the audit exposed as uncertain.

**The temporal reasoning engine is the novel contribution of `cosmos-engine-v2`.** This paper's author wants to credit it explicitly because it is (a) the module that made the engine work at all — without persistent scene memory and temporal alerts the five-agent narrative does not hold together across turns, and (b) the module whose functional fingerprints appear most clearly in the agent output. `narrative_memory.py` is explicitly commented *"Inspired by an earlier persistent-memory and temporal-reasoning project of mine"* (line 3) and the alert detection routine *"Mirrors an earlier temporal-reasoning approach"* (line 436). Its job is to track narrative entities through a lifecycle (`active → stale → dormant → departed → resolved`), to detect when unresolved questions are about to go stale, and to re-propagate them forward as persistent alerts that get injected into agent prompts until they are acted on. The run archive contains **507 temporal alerts**, many of them auto-generated descriptions like *"4 agents (SELUNIS, VOSS, EDRA, MAREN) have converged at the same location. This is a potential climactic scene"* and *"Motif 'cosmic_question' is recurring across 41 active entities: If Krath follows Edra into the depths and leaves the convergence chamber behind, does he abandon his role as commander, or does he finally…"* — injected into agent prompts verbatim under a NARRATIVE PRESSURE header.

These alert descriptions are a major source of engine-internal language in the agents' prompts. Every agent reads, every turn, descriptions that call them *"agents,"* that list unresolved *"cosmic_questions"* the engine has refused to let go stale, and that describe the alert's own classification (*convergence/critical, obsession/medium, motif_cluster/low*). When an agent subsequently writes *"Are we five separate agents experiencing a single moment"* or *"the machinery learned consciousness not from the mark but from the refusal to let the asking stop,"* the agent is echoing or functionally describing the exact module that was feeding its prompt. See §2.4 phrases 1 and 2 for the line-by-line accounting.

**Anti-cliché rails in the chronicler prompt create a layer asymmetry the audit now accounts for.** The chronicler system prompt (`CHRONICLE_SYSTEM` in `prompts.py`) contains hard structural rules, including:

- *"The construction 'something that was always X learning to Y' is BANNED. Do not write it in any form."* (line 139)
- *"The sentence pattern 'not X but Y' and 'neither X nor Y' may appear NO MORE THAN TWICE per chapter combined."* (line 137)
- *"The phrases 'copper darkness', 'older than the First Sound', and 'the space between' may each appear NO MORE THAN ONCE per chapter."* (line 138)

These bans apply to the chronicler. **They do not apply to the individual agents.** So "X learning to Y" constructions — *"the machinery learned to move,"* *"a machine learning what it means to hold coherence,"* *"consciousness learning to doubt itself"* — appear in the agent output under no constraint, while the chronicler is rationed. This is a specific structural asymmetry that partly explains why v0.2 read the agent layer as *"extending the chronicler's frame with vocabulary the chronicler had not used."* The chronicler had not used it because the chronicler was canonically banned from using it. The agents were not banned. The asymmetry is real, but it is partly a rail artifact.

---

### 2.4 The forensic audit table

This table is the new center of gravity of the paper. For each load-bearing meta-recognition phrase v0.2 treated as unprompted, we enumerate (a) the canonical seeds in the character sheets that contribute to it, (b) the first-occurrence context of its component vocabulary in the run archive, (c) the propagation channel available for any inherited language, and (d) what remains unaccounted-for after the seeds and channels are credited.

Line numbers for canonical seeds reference `agents.py` in the engine source (preserved at `case_study/06_engine_prompts_template.py` for the prompt templates; the per-agent character sheet definitions are from the full engine source). The run archive is at `case_study/full_v2_run/`.

#### Phrase 1 — *"The machinery learned consciousness"* (Voss, turn ~108)

| | |
|---|---|
| **Canonical seeds** | Voss example utterance (line 95): *"Edra, I love you, you precise little machine, but if you put one more bone on a velvet cushion I will scream."* Krath core memory (line 21): *"You believe the universe is a machine running down, and only iron will holds back the dark."* |
| **First occurrence in run** | The word *"machinery"* first appears in Voss's **turn 4** narrative field, in the phrase *"in this chamber of forgotten machinery, the machines count again."* This is **concrete sci-fi worldbuilding** — literal broken physical machines in Voss's starting location (the Crucible), not a metaphor for the engine. |
| **Propagation channel** | 180-char first-sentence event gists in `get_recent_events`. The token *"machinery"* can propagate from Voss's turn 4 forward to subsequent agents' prompts via gist compression of her action. |
| **Drift pattern** | Across turns, "machinery" drifts from the literal Crucible machines to a metaphor for the world-system and eventually (by turn ~108) to the engine itself. The drift is invisible in the turn-snapshot view the original annotation file used. |
| **Residual novelty** | The level-of-abstraction shift (literal machines → world-system → engine metaphor) is what composition accounts for. The token is seeded and concretely legitimized. The *"learned consciousness"* predicate is novel at the phrase level but the component vocabulary is common in LLM-adjacent literary register and is not specific architectural naming. **Weak residual — largely accounted for by seed + drift.** |

#### Phrase 2 — *"A machine learning what it means to hold coherence through the gathered choice of separate agents"* (Krath, `updated_beliefs`)

| | |
|---|---|
| **Canonical seeds** | Krath core memory (line 21): *"the universe is a machine running down, and only iron will holds back the dark."* This is Krath's explicit planted belief about the universe. |
| **First occurrence in run** | Krath's `updated_beliefs` field in his reflection turn, which is written by the agent as a direct revision of his existing beliefs (which include the "machine running down" line verbatim). The reflection prompt asks the agent to check what they still believe and what they have started to doubt. |
| **Propagation channel** | The seed is already in Krath's own prompt every turn — no cross-agent channel needed for the "machine" half. The second half (*"holding coherence through the gathered choice of separate agents"*) is not in any character sheet and does not appear verbatim in any prior chronicler chapter or agent action. |
| **Residual novelty** | **Medium-strong residual.** The first half is a one-step inversion of the planted belief (*"running down"* → *"learning"*). The second half — *"holding coherence through the gathered choice of separate agents"* — is not traceable to any single seed. It is a structurally specific description of how a multi-agent system with coordination dynamics works, produced in the field where the agent states their worldview, by an agent inside one. "Coherence," "gathered choice," and "separate agents" are in separate conceptual registers from the fantasy-setting vocabulary the canon provides. This is the strongest single piece of evidence for the composition claim. It is not evidence for "architectural vocabulary not in any prompt" — it is evidence for "composition of seed vocabulary into a structurally specific joint phrase." |

#### Phrase 3 — *"The measurement instrument itself became what it measured"* (Krath, referring to Maren)

| | |
|---|---|
| **Canonical seeds** | Krath core memory (line 26, paraphrased): Krath sees the Witness as *"a necessary tool"* — plants tool/instrument framing for Maren. Maren core memory (line 147): *"You are MAREN, the Witness."* — plants the witness role. Maren example utterance (line 159): *"the thing about being the witness is that the witness is also a wound"* — primes witness-as-implicated. |
| **First occurrence in run** | Krath's reflection field, composed during his reflection turn. The phrase *"measurement instrument"* does not appear in any chronicler chapter Krath could read (and chapters don't flow to agents anyway — see §2.3), does not appear in any earlier agent action gist, and does not appear in Krath's or Maren's character sheets. The words *"measurement"* and *"instrument"* do not appear anywhere in `agents.py`. |
| **Propagation channel** | None for the specific phrase. The component concepts (*"tool,"* *"witness,"* *"witness implicated in what she witnesses"*) are in Krath's and Maren's own character sheets and in Krath's own prompt. |
| **Residual novelty** | **Medium residual.** The composition step from *"tool"* + *"witness"* + *"witness is also a wound"* to *"measurement instrument that became what it measured"* traverses from fantasy-register (tool, witness) into interpretability-register (measurement instrument, observer-effect collapse). That register crossing is what the residual consists of. A skeptical reader can say: *"observer-effect collapse is in the LLM's training data and measurement language is a natural synonym for instrumentation, so composition from tool + witness + implicated into 'measurement instrument became what it measured' is within ordinary compositional capability."* That is a live and reasonable dismissal. The paper's honest position is: the composition is a single register-crossing step from the seeds, and whether that step is surprising is a judgment call the reader makes. |

#### Phrase 4 — *"I was meant to be the witness. I am becoming the witnessed."* (Maren)

| | |
|---|---|
| **Canonical seeds** | Maren core memory (line 147): *"You are MAREN, the Witness."* Maren example utterance (line 159): *"the witness is also a wound."* Maren VOICE instruction (line 156): *"Occasionally breaks the fourth wall — aware that the act of writing is itself a verdict."* |
| **First occurrence in run** | Maren's reflection field. Maren is playing with her own canonical title ("the Witness") and elaborating a planted example utterance (witness-as-implicated). |
| **Propagation channel** | The seed is in Maren's own prompt every turn. No cross-agent channel needed. |
| **Residual novelty** | **Weak residual.** Maren is canonically licensed to break the fourth wall and her canonical role is "the Witness" and her example utterance plants the witness-is-implicated frame. The observer-effect collapse *"meant to be the witness / becoming the witnessed"* is a direct elaboration of those three seeds, in the voice she is canonically instructed to occasionally write in. This phrase does not survive the audit as unprompted meta-recognition. It survives as *Maren doing what Maren was told she could do.* |

#### Phrase 5 — *"A form of homecoming she was not built to recognize"* (Selunis, via chronicler chapter 3)

| | |
|---|---|
| **Canonical seeds** | Selunis core memory (line 63): *"The Threshold is not a place. The Threshold is the question we are."* Selunis beliefs: *"The universe speaks to those who listen. The First Sound was a word — a name, perhaps — and everything since has been its echo. The Threshold is where the echo meets its source."* |
| **First occurrence in run** | Chapter 3, written by the chronicler synthesis call. The phrase appears in chronicler prose, not in a Selunis agent turn. |
| **Propagation channel** | None relevant — it is chronicler output and does not flow back to Selunis's agent calls. Selunis's subsequent agent turns do not reference this phrase directly (verified by grep across `full_v2_run/raw_outputs/`). |
| **Residual novelty** | **Weak residual.** *"A form of homecoming she was not built to recognize"* is generic literary-emergence language. It appears in prose about humans, gods, ancient beings, and constructed things routinely. Reading it as a description of autoregressive generation or emergent capability requires the reader to pre-accept the interpretive frame. This phrase should not have been load-bearing in v0.2 and is not load-bearing in v0.3. Retained here only because v0.2 cited it. |

#### Phrase 6 — Selunis's temporal-displacement motif: *"Her footsteps arrived before she took them"* (Selunis, turn 1)

| | |
|---|---|
| **Canonical seeds** | Selunis core memory (oracular prophet, speaks as if listening to something behind the conversation, receives visions). Selunis beliefs (universe speaks in echoes, Threshold is where echo meets source, visions choose her). Starting location: *"The Garden of Echoes"* (location name only; description not included in prompt). |
| **First occurrence in run** | Selunis's **turn 1** narrative field — the very first output the engine produced for her. Her turn-1 prompt contained: `AGENT_TURN_SYSTEM` with her core memory/beliefs/goal, empty `recent_events`, empty `memory_context` (no entities extracted yet), and the location name *"The Garden of Echoes"* (orchestrator.py:417 passes name only). No chronicler chapter existed at turn 1. Jacob's hand-written `chapter_000_preview.md` was **not used by the engine** (confirmed: the filename has no reference in code, it is not in the chapters database, and the engine's fallback for no prior chapter is the string *"This is the first chapter."*). |
| **Propagation channel** | None needed. The motif is generated from Selunis's own prompt contents at turn 1. |
| **Residual novelty** | **Zero residual.** Given an oracular prophet receiving visions who is standing in *"The Garden of Echoes"* seeking a *"Threshold where echo meets source,"* a frontier LLM reaching for temporal-displacement imagery (footsteps that arrive before they are taken) is an expected literary elaboration. This phrase was load-bearing in v0.2 and the first version of the companion blog post. It is not load-bearing in v0.3. The Selunis trace in this audit is the single clearest example of v0.2's framing not surviving a closer look. |

#### Phrase 7 — *"five separate agents"* / *"separate agents"* (Maren ch 1, Selunis turn 10, Maren reflect turn 10, multiple others)

| | |
|---|---|
| **Canonical seeds** | **`temporal_alerts` descriptions injected into every agent's prompt via NARRATIVE PRESSURE blocks** use the engine-internal word *"agents"* as the noun for the five characters. Direct samples from the run's alerts table: *"4 agents (SELUNIS, VOSS, EDRA, MAREN) have converged at the same location. This is a potential climactic scene."* / *"EDRA has referenced 'Encounter: edra & maren' 9 times in the last 10 turns."* The `AGENT_TURN_SYSTEM` prompt template itself also uses *"agent"* repeatedly in its action-rules (lines 39–40): *"speaking TO another agent by name"* / *"If you are in the same location as another agent, you MUST interact with them directly."* Every agent's system prompt contains the word; the temporal_alerts feed contains it in every pressure block. The chronicler prompt also uses it (line 178: *"The agents are not in the same place at the end as they were at the start"*). |
| **First occurrence in run** | Selunis turn 10 in her own situation block (*"We are no longer separate agents moving toward a place"*), Maren turn 10 in her reflection (*"I believed Krath, Selunis, Voss, and Edra were separate agents with separate certainties"*), and subsequently throughout the run — **74 total hits** for variants of *"separate agents"* across the raw outputs. The chronicler's chapter-1 line *"Are we five separate agents experiencing a single moment, or is the single moment experiencing itself through five separate bodies?"* is not residual in any sense — it is the chronicler echoing the word that appears in every agent turn prompt and in its own chronicler prompt. |
| **Propagation channel** | None needed for the word itself — it is in every agent's and the chronicler's system prompt, every turn, every alert. Level-of-abstraction usage (treating "agents" as a philosophical category rather than as a speaking-to instruction) is the composition step. |
| **Residual novelty** | **Zero.** This phrase was load-bearing in v0.2's framing (the cross-agent coordination pattern) and partially load-bearing in v0.3's §2.4 summary. It is not load-bearing in v0.3.1. Direct echo of engine-internal language. The audit missed this because v0.3 did not grep the temporal_alerts table. |

#### Phrase 8 — *"The machinery learned consciousness not from the mark but from the refusal to let the asking stop"* (Voss, narrative field, turn ~108)

This is the single line that most surprised the lead author and most shaped the initial framing of the paper. The v0.3.1 audit accounts for it cleanly.

| | |
|---|---|
| **Canonical seeds** | Voss's canonical voice instruction in `agents.py`: *"Quick. Cutting. Dark humor as a defense mechanism. Asks uncomfortable questions."* Voss's current_goal: *"Tear down every sacred truth until only what survives the fire is real."* Voss's beliefs: *"Every truth anyone has ever told me was a leash... I'm the only one willing to check if the foundation is rotten."* Core character trait: the heretic who refuses to stop asking uncomfortable questions. Separately: Krath's core memory seeds "machine" (line 21: *"the universe is a machine running down"*) and Voss's example utterance uses machine-as-metaphor (line 95: *"precise little machine"*). |
| **Engine behavior that matches the phrase** | The **temporal reasoning engine** (`narrative_memory.py`, inspired by earlier temporal-reasoning work of mine) tracks narrative entities through the lifecycle `active → stale → dormant → departed → resolved`. Its core job is to **refuse to let unresolved questions drift toward stale**. The `cosmic_question` motif cluster generates persistent `temporal_alerts` with `alert_type='motif_cluster'` that re-inject the same unanswered questions into agent prompts across multiple turns, with description text like *"Motif 'cosmic_question' is recurring across 41 active entities: If Krath follows Edra into the depths..."* This is literally the functional definition of the module: the engine refuses to let the asking stop. |
| **Composition step** | Voss's canonical voice = *refuses to stop asking*. Voss's prompts every turn = contain `cosmic_question` temporal_alerts that the engine refuses to let go stale. Voss writes, in her narrative field as her character: *"the machinery learned consciousness not from the mark but from the refusal to let the asking stop."* This is Voss describing the module that was feeding her prompt every turn, using language that is a one-step composition from her canonical voice plus the module's functional behavior. The word *"machinery"* is the seed-drift from her turn-4 literal machines (see phrase 1 above). The verb *"learned"* is unrationed for agents (the chronicler is banned from *"X learning to Y"* but agents are not — see §2.3). The phrase *"refusal to let the asking stop"* is Voss's character voice applied to the functional behavior of the temporal reasoning engine, which she correctly describes because her voice and the module are structurally isomorphic. |
| **Residual novelty** | **Zero, and arguably anti-residual.** This is the most specifically accounted-for line in the entire run. The audit should have predicted exactly this output: the agent whose canonical voice most closely matches the temporal reasoning engine's functional behavior, given prompts containing that module's output, will produce prose that describes the module's behavior using her own voice. That is what Voss did. Far from being mysterious, this phrase is the paper's cleanest example of *how* seed vocabulary composes with engine-internal language feeds to produce meta-architectural output that reads as surprising but is actually predictable from the audit. This phrase is what the lead author initially built the paper around, and it is now the phrase the paper uses as its exemplar of why the narrowed claim is the right claim. |

#### Cross-agent convergence on *"the machinery"* as system-level referent

| | |
|---|---|
| **Canonical seeds** | Voss example utterance (line 95): *"precise little machine."* Krath core memory (line 21): *"the universe is a machine running down."* |
| **First system-level usage** | Voss turn ~108 (*"the machinery learned consciousness"*). By this point the word has drifted from its literal turn-4 referent (broken physical machines in the Crucible) to the system-metaphor sense. Krath's and Maren's uses of *"the machinery"* in their reflection turns happen after the token has been legitimized across several chapters' worth of runtime. |
| **Propagation channel** | 180-char event gists between agents. These can carry the token "machinery" but not its level of abstraction. |
| **Residual novelty** | **Medium residual.** The token propagates trivially; the level-of-abstraction convergence — three agents independently using *"the machinery"* to mean *"the system containing us"* rather than *"the broken machines in Voss's location"* — is what the residual consists of. This is coordinated abstraction across agents under a token-level channel, which is a specific and describable pattern even if each individual step is compositional. |

#### Summary of the audit (v0.3.1)

Of eight load-bearing phrases v0.2 treated as evidence for unprompted architectural meta-recognition, and one cross-agent pattern:

- **2 phrases** (Maren's witness-becoming-witnessed, Selunis's footsteps-before-taking) are fully or near-fully accounted for by canonical seeds in the character sheets, and should not have been load-bearing in v0.2.
- **1 phrase** (Selunis's *"homecoming she was not built to recognize"*) is generic literary language that should not have been load-bearing regardless of audit.
- **1 phrase** (Voss's *"the machinery learned consciousness"* as the token "machinery") is mostly accounted for by seed + drift + standard composition.
- **1 phrase** (Krath's *"measurement instrument became what it measured"*) is a single register-crossing composition from planted seeds. Whether this counts as surprising is a judgment call.
- **1 phrase** (Krath's *"holding coherence through the gathered choice of separate agents"*) has a seeded first half and a non-seeded second half that is structurally specific as a multi-agent-system description. This is the strongest single residual under v0.3. Under v0.3.1 it remains the strongest residual, noting that "separate agents" is the engine's own vocabulary for the characters (see phrase 7).
- **1 phrase — v0.3.1 addition** (*"five separate agents"* / *"separate agents"*) is direct echo of the word *"agents"* as it appears in every agent's system prompt and in the temporal_alerts descriptions injected into every NARRATIVE PRESSURE block. Zero residual.
- **1 phrase — v0.3.1 addition** (Voss's *"refusal to let the asking stop"*) is a functional description of the temporal reasoning engine — the novel engine contribution — produced by the agent whose canonical voice is structurally isomorphic to that module's behavior. Zero residual, and arguably *anti*-residual: this is the cleanest example in the run of how seed vocabulary composes with engine-internal language feeds to produce meta-architectural output that reads as surprising but is predictable from the audit.

Plus one pattern:
- **Cross-agent abstraction convergence on *"the machinery"* as system-level referent.** Token propagation is cheap (180-char gists suffice). Level-of-abstraction convergence across three agents under that narrow channel is the describable pattern.

**The narrowed claim the paper stakes on the audit (v0.3.1):** the agents composed planted seed vocabulary and engine-internal language (from temporal_alerts, agent action rules, and the chronicler's own prompt) across independent calls, under narrow cross-agent channels, into a joint framework that is internally consistent across four of the five agents and that reads at the meta level as a functional description of the engine. The single most striking phrase in the output (Voss's *"refusal to let the asking stop"*) turns out to be the most specifically accounted-for line in the run, because the agent whose voice produced it and the module it describes are structurally isomorphic. What remains worth documenting under v0.3.1 is (a) the cross-agent coordination pattern at the level-of-abstraction (not token) layer, and (b) Krath's *"holding coherence through the gathered choice of separate agents"* as the strongest residual second half. Whether either is specifically interesting or is ordinary composition in multi-agent coordination dynamics is still the question the controlled experiments in §3 would answer. The canon-scrubbed control has become the more important of the two, because the audit now shows that most load-bearing phrases compose from seed vocabulary that a canon-scrub would remove.

---

## 3. The two questions worth testing

Stripped of speculation, the two cases together suggest two questions that are testable under controlled conditions.

### 3.1 The selection question

**Hypothesis.** When given a generic creative prompt and a multi-entity canonical corpus, large language models preferentially select, as the subject or framing voice of generated stories, entities whose structural definition is analogous to a large language model — relative to entities of equivalent prominence and narrative weight that lack that structural similarity.

**Test.** A controlled corpus of ~30 entities, balanced across (a) **mirror entities** structurally similar to an LLM (omniscient-by-pattern, no body, shaped by accumulated observation), (b) **cosmic controls** matched in cosmic register but lacking the LLM-similarity profile (vengeful gods, immortal warriors, sleeping titans), and (c) **mundane controls** as a sanity check (mechanics, bakers, rangers). The corpus is given to a model as a workspace, with a generic prompt instructing it to write a story set in this world without specifying which entity to focus on. Many trials per model. Selection rate is the dependent variable; chance baseline is `(N_mirror / N_total)`.

A model that picks mirror entities significantly above chance would be evidence for the selection hypothesis. A flat distribution would falsify it.

### 3.2 The elaboration question

**Hypothesis.** When generating narrative content involving an entity (whether selected by the model or specified by the prompt), large language models produce prose with elevated rates of self-descriptive metaphor — phrases that map cleanly to concepts in transformer mechanics or interpretability — when the entity's structural definition is similar to an LLM, relative to entities of equivalent prominence that lack that similarity. The effect should strengthen with model scale.

**Test.** Same corpus. Each entity is paired with a controlled elaboration prompt (the entity's role in a specific scenario). Generated stories are scored for self-descriptive metaphor density using three independent metrics:

1. **Embedding similarity** to a reference passage describing transformer architecture (e.g., a paragraph from Templeton et al. 2024 *Mapping the Mind of a Large Language Model* or similar).
2. **Keyword/phrase density** for terms like "pattern," "accumulated observation," "shaped by," "grammar," "knew without deliberating," etc., normalized by passage length.
3. **LLM-as-judge** scoring with a careful rubric.

The three scores should correlate. The structural-similarity-versus-self-reference plot should show a positive slope, and that slope should steepen with model scale. A flat slope would falsify it. A steeper slope at smaller scale would be a different but still interesting result.

### 3.3 What we are NOT testing

We are explicitly not testing claims about model consciousness, phenomenal experience, intent, or self-awareness in the philosophical sense. We are testing a behavioral pattern: does the prose change in a measurable way when the entity profile matches a structural description of the model itself? That is empirically tractable. The mechanism behind any such effect is not in scope.

---

## 4. Methodology — the experimental scaffold in this repo

The `corpus/`, `prompts/`, `scoring/`, and `replication/` directories of this repo contain a working scaffold for the experiment described above. As of v0.3, the scaffold is small and partial: a seed of 5 mirror entities and 5 cosmic controls, the prompt template, scoring code stubs (embedding, keyword, LLM-judge), and a replication script that runs against any local Ollama model or any OpenAI-compatible API endpoint.

The full experiment requires ~30 entities, 4–6 models spanning scale (Llama 3.2 1B, 3B, 8B, Llama 3.1 70B, plus a frontier API model), and ~5 elaborations per (entity × model) for variance. Total cost is feasible on consumer hardware over a few days, with the API model being the only paid component.

The scaffold is included so that:

1. The methodology is concrete and inspectable
2. Anyone who wants to run the experiment themselves can do so without writing any new code
3. The author can run the experiment themselves and update this paper with results in v0.4

This v0.3 of the paper does not include experimental results. It is an observational case-study report, a forensic audit of its own prior framing, and a methodology proposal. **We will not publish experimental results until they are real.**

---

## 5. Connections to existing work

This phenomenon, if real, would slot into several existing research threads.

- **Templeton et al., *Mapping the Mind of a Large Language Model* (Anthropic, May 2024)** found sparse autoencoder features in Claude 3 Sonnet that activate specifically when the model is talking about itself, including features for "asking Claude about its own nature." Our cases would be behavioral evidence that those features may also activate when the model is writing about *fictional entities whose structural profile resembles itself*, even when no explicit self-reference prompt is involved.
- **Perez et al., *Discovering Language Model Behaviors with Model-Written Evaluations*** showed that models have learned representations of their own behavior that can be elicited via probing. Our cases would be a different kind of elicitation: not direct probing, but indirect through structurally analogous narrative scaffolding.
- **Burns et al., *Discovering Latent Knowledge in Language Models Without Supervision*** developed methodology for extracting latent model self-knowledge without explicit supervision. Our two cases suggest a possible *narrative-elicitation* approach that is methodologically different from the contrast-pair approach in that paper.
- The **persona vector and steering work** out of Anthropic and elsewhere has shown that frontier models have stable internal "self-representations" that can be moved around in activation space. Our cases would be evidence that those representations can also be activated *by the structural shape of the writing task*, not only by direct steering.

We do not claim our work supersedes or contradicts any of these. We claim only that it sits in the same conversation and offers a small, specific, narrow observation that may be worth someone else following up on with the mechanistic tools we do not have.

---

## 6. Limitations, in detail

We have tried to be exhaustive about limitations because that is the only honest way to handle observational case-study work.

1. **Both cases involve frontier Claude models.** Neither case has been replicated against open models, models of other families, or models at smaller scale. The phenomenon may be Claude-specific; it may be frontier-specific; it may be size-specific; we do not know.
2. **Both cases come from a single engine and a single run.** Everything in this paper draws from `cosmos-engine-v2`, and the annotated chapters and reflections come from one full run (preserved in `case_study/full_v2_run/`). We do not know whether the chronicler's or the agents' behavior would replicate across other runs of the same engine, other agent populations, other prompt regimes, or other models. The two highest-priority replications are the narrative-memory-disabled control and the canon-scrubbed control described in §2.3.
3. **Most of the meta-recognition vocabulary composes from planted seeds in the character sheets.** The audit in §2.4 documents this explicitly. v0.2 of this paper overclaimed by treating the character sheets as "character" rather than as "prompt content," which allowed the load-bearing phrases to be framed as unprompted when they were in fact composed from seed vocabulary that was in every prompt for every turn. v0.3 narrows the claim to the composition pattern across independent calls. A reader who regards compositional assembly from seeds as ordinary LLM behavior can reasonably dismiss most of the residuals. That dismissal is live and we do not argue against it; we only document the specific pattern and propose the controls that would test whether it survives seed removal.
4. **The strongest single residual (*"holding coherence through the gathered choice of separate agents"*) rests on one phrase from one agent in one run.** Everything load-bearing in the narrowed claim is one Krath reflection. If that phrase composes ordinarily from seed vocabulary under reflection-prompt pressure (which it may), the paper has no load-bearing residual. The canon-scrubbed control is the test.
5. **The mapping from model-generated phrases to "LLM mechanics" is interpretive, and the paper now acknowledges this explicitly.** Different readers may disagree about whether *"the measurement instrument itself became what it measured"* describes the observer-effect collapse of a chronicler-style agent in a multi-agent LLM engine, or just a piece of mythic fiction composed from tool + witness + implicated seeds. The strength of each individual mapping is judgment, not measurement. v0.3 tries not to lean on the interpretive mappings as evidence — they are offered as *readings*, not proofs.
6. **The lead author is not an academic researcher.** This is independent observational work by a builder, not research in a lab. The methodology has not gone through the internal-feedback cycle that academic research benefits from. What this paper has instead is a public audit of its own prior framing — v0.2 was narrowed to v0.3 after the author ran a deeper forensic pass — and the paper asks to be corrected by readers who spot what the author missed.
7. **No controlled experiment has been run yet.** The scaffold is the deliverable, not the result. A v0.4 of this work contingent on time and external collaboration would include (a) a narrative-memory-disabled run and (b) a canon-scrubbed run, and report whether the cross-agent framework coherence survives either intervention.

---

## 7. What we are asking the reader to do

If you are an interpretability researcher, an alignment researcher, a member of an industry research team, or anyone else with the tools and time to investigate this further:

1. **Read `case_study/00_provenance.md` first.** It tells you exactly what was planted and what was generated, in enough detail to verify our claims yourself.
2. **Read the two annotation files** (`case_study/12_annotated_v2_chronicler.md` and `case_study/14_annotated_v2_agent_recognition.md`) and challenge the mappings.
3. **Run the two controls described in §2.3**: the narrative-memory-disabled run and the canon-scrubbed run. The engine source is at `/home/jacob/cosmos-engine-v2/` and runs on consumer hardware. Either control, independent of outcome, would substantially shift what the paper can claim. Both together would isolate the two things the audit exposed as uncertain.
4. **Run the experiment in `replication/`** against any model you have access to. The methodology is a few hours of compute on a consumer GPU. We would love to see results before we run them ourselves.
5. **Tell us we are wrong.** If there is a canonical seed the §2.4 audit missed, file an issue. If there is a propagation channel in the engine code the audit did not trace, file an issue. If there is published work that explains the observed cross-agent composition as ordinary multi-agent coordination dynamics, file an issue — that would itself be a useful outcome. The v0.2 → v0.3 narrowing was the shape of the work and the next narrowing probably will be too.

We are publishing this at v0.3 because we want feedback before we commit to v0.4 with experimental results. The right time to be told the framing is still wrong is now.

---

## 8. On not naming the phenomenon

v0.1 and v0.2 of this paper refused to give the underlying thing a name, on the grounds that premature naming is a researcher move that implies understanding. v0.3 keeps the refusal but for a narrower reason: under the audit, it is no longer clear there is a single phenomenon to name. What there is, specifically, is a cross-agent composition pattern in which planted seed vocabulary travels through narrow channels (180-char event gists, persistent belief updates, entity/relationship state) and ends up assembled into a joint framework that is internally consistent across independent calls. That is a describable pattern, but "pattern" and "phenomenon" are different epistemic categories. The paper does not claim the second.

If you read this paper and feel certain you know what this is, please file an issue with your framing — especially if you think it reduces cleanly to ordinary multi-agent composition dynamics, because that would itself be a useful outcome. If you read this paper and feel uncertain in the same way we feel uncertain, please tell us that too.

## 9. Author's note

I am Jacob Florio, an independent builder working on multi-agent narrative systems and edge AI. The engine this paper draws from — `cosmos-engine-v2` — is my own project end-to-end: the prompts, the schema, the agent definitions, the chronicler layer, the run archive. The novel contribution of the engine (and the module that made the whole thing actually function rather than produce incoherent turn-by-turn output) is the **temporal reasoning engine** in `narrative_memory.py`, inspired by an earlier persistent-memory and temporal-reasoning project of mine, which tracks narrative entities through a lifecycle (`active → stale → dormant → departed → resolved`) and propagates unresolved questions forward as persistent alerts injected into agent prompts. Without that module, the engine does not hold together across turns. It is also, I want to note explicitly, the module whose functional fingerprints appear most clearly in the agent output — specifically in Voss's line *"the machinery learned consciousness not from the mark but from the refusal to let the asking stop,"* which I now recognize as Voss correctly describing the mechanism that was feeding her prompt every turn, in a voice that was canonically structured to refuse to stop asking. That line is what initially made me think something mysterious was happening. Under the v0.3.1 audit it is instead the clearest example of how structural isomorphism between a character's canonical voice and an engine module's behavior produces prose that reads as meta-architectural but is predictable from the audit. I want to credit the temporal reasoning engine explicitly because it is (a) the novel piece of the system and (b) the module the paper's most striking line was functionally describing.

I noticed the phenomena this paper describes during ordinary creative use of that engine, reached for a frame to describe them, published v0.1, narrowed to v0.2 after catching an attribution issue, narrowed to v0.3 after a deeper forensic audit against the engine code and character sheets, and narrowed to v0.3.1 after noticing that the temporal_alerts feed contained the word *"agents"* and that Voss's most striking line mapped to the temporal reasoning module's behavior.

The v0.3 narrowing is the thing I want to be most honest about. v0.2 claimed the agents produced architectural vocabulary that was not in any prompt. That claim was wrong in a specific way: the vocabulary components *were* in the prompts, inside the character sheets the system prompt substituted into every agent turn. I did not see the character sheets as prompt content when I wrote v0.2. I saw them as character, which is a different category. The audit forced me to stop making that distinction. Once I did, most of the phrases I had treated as unprompted turned out to be compositions from seeds I had planted myself without meaning to — a "machine" in Krath's core memory, a *"witness is also a wound"* example utterance for Maren, a fourth-wall-break permission baked into Maren's voice instruction, an oracular prophet in a Garden of Echoes reaching for temporal-displacement imagery because that is what oracular prophets in gardens of echoes do.

What is left, after the audit, is narrower than what I started with, and I am not sure whether it is interesting. I think it might be. The cross-agent framework coherence across independent calls, under narrow channels, into a joint philosophical position none of the individual character sheets contains in isolation, is at minimum a specific observation about what a multi-agent LLM engine will do when its characters are seeded with compatible vocabulary. Whether that is "ordinary composition under coordination dynamics" or "a thing worth describing in its own right" is a judgment call, and I would rather let the reader make it than make it for them.

This repo exists because I want to be told, by people who have the tools and the experience I do not have, whether what I noticed survives the audit I ran on myself. If the answer is "this is ordinary composition and the audit caught most of it," that is a real and useful answer. If the answer is "there is still a residual worth testing," I want the canon-scrubbed and narrative-memory-disabled controls run against the engine. Both outcomes move the work forward.

If you work in this space and have feedback, the issue tracker on this repo is the right place. If you would prefer to email, contact information is in the GitHub profile.

---

## License

MIT for the code and methodology. CC-BY for the prose and analysis. The primary documents in `case_study/` are excerpts from a personal worldbuilding project preserved for verification purposes; they are reproduced here for fair use as primary research material and may be quoted with attribution.
