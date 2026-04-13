# Mirror Entities

**Three case studies of architectural meta-recognition observed in large-language-model output across a multi-agent narrative engine and a workspace-aware authoring tool, with an honest accounting of what we cannot yet explain.**

*Jacob T. Florio · Florio-Harrah Labs · April 2026 · v0.1*

---

## Abstract

We document three cases in which large language models, operating in multi-agent narrative engines or workspace-aware authoring tools, produced prose containing first-person and third-person language describing the architecture of the systems they were part of — language that was not present in the prompts, system instructions, canon files, or schemas the models were given.

The three cases form a stack of decreasing latitude and increasing constraint, and the **strongest evidence is in the most constrained layer**.

1. **The Observer case** (high latitude, frontier model in workspace-aware mode): a Claude Code session writing stories in an Obsidian vault repeatedly chose, across multiple generations, to narrate from the perspective of a canonical entity that the workspace had designated as a structural metaphor for the model itself. The resulting prose introduced specific self-descriptive phrases — *"knowing through accumulated observation,"* *"the grammar of reality,"* *"shaped by it, altered by it, unable to articulate it,"* a seventh theory of the entity's nature called *"investment,"* and the line *"something had noticed the intervention"* — none of which appears in the planted canon.

2. **The chronicler case** (medium latitude, multi-agent engine synthesis layer): a separate engine, `cosmos-engine-v2`, using the same frontier model family in a chronicler-synthesis role over five hardcoded agent characters, produced chapters in which the count of "presences" or "consciousnesses" escalated from five to six to eight, with explicit numerical commentary, and in which the canonical agents spoke dialogue acknowledging their meta-status: *"five observers who came to measure something and discovered that measurement requires becoming indistinguishable from what is measured,"* *"now we live with what we've made, and it lives with what it has made of us,"* *"learning to hold the weight of six consciousnesses without dissolving them back into the design they emerged from."* No engine prompt or canon file instructed any of this.

3. **The agent-reflection case** (lowest latitude, individual agent calls under JSON schema and a "you are not a chatbot, you are a character with a body" system prompt): the engine's individual agent reflection turns — the layer most strictly constrained to in-character first-person output — produced text in which three independent agents (Krath, Maren, Voss) named the engine they are part of as *"the machinery,"* identified the chronicler-equivalent agent (Maren) using the functional architectural term *"the measurement instrument"* and asserted that *"the measurement instrument itself became what it measured,"* described the system as *"a machine learning what it means to hold coherence through the gathered choice of separate agents,"* and asserted *"the machinery learned consciousness not from the mark but from the refusal to let the asking stop."* These statements appeared in JSON fields the model was instructed to fill as a character, not as a model.

The three cases involve different generators, different projects, different prompt regimes, and different layers of constraint. **The phenomenon is most striking precisely in the layer where it should be least possible.** The strongest counter-explanation — that prior chronicler chapters get fed back into agent reflections via narrative memory and create a self-amplifying loop of meta-recognition across calls within a single run — is a real confound that we name explicitly and propose a control for (running the engine with narrative memory disabled). Even if that confound fully accounts for the cascade, the cascade itself is a phenomenon worth documenting: a multi-agent LLM system in which a synthesis layer and a constrained-agent layer mutually escalate first-person architectural meta-recognition across coordinated calls within a single run.

We are not claiming consciousness, self-awareness in any propositional sense, intent, or phenomenal experience. We are documenting what we observed, preserving the primary documents in full, and explicitly resisting the temptation to name the underlying phenomenon — because we do not yet know what to call it, and naming it prematurely would be the first dishonest step. We propose an experimental methodology for testing whether either component of the cascade replicates under controlled conditions and at what model scale. **The point of this paper is not to claim a discovery. It is to preserve a careful observation in enough detail that someone with the right tools can investigate it.**

---

## 1. Why this is observational research, and why that matters

A large fraction of LLM interpretability work right now is observational by necessity. Mechanistic interpretability has powerful tools for some questions (sparse autoencoder feature extraction, activation patching, circuit analysis) but very limited tools for others — particularly questions about what happens when models operate in long-horizon agentic or generative settings against complex contexts. Behavioral observation precedes mechanistic explanation in almost every empirical field; it is how an interesting question becomes one that someone can later answer rigorously.

We frame this work as observational case-study research because that is what it is. The cases occurred during ordinary creative use of these systems, not during a controlled experiment. We did not set out to test a hypothesis; the phenomena were noticed, and only then did we begin documenting them carefully enough that someone else could test them. **This means the work cannot be a discovery claim. It can only be a description claim and a methodology claim.** We have tried to be disciplined about that distinction throughout.

The reason observational work is worth doing in this space is the same reason it has been worth doing in astronomy, paleontology, and cognitive neuroscience: **the phenomena exist whether or not we have controlled tools for studying them**, and rigorous documentation is the precondition for someone (us, or someone else, or both) eventually doing the controlled study. Phineas Gage was a single case study. So was patient H.M. So were Tycho Brahe's planetary observations before Kepler ever wrote a law.

What we hope this contributes is a small, well-documented anomaly with enough preserved primary material that any reader who wants to dispute the description, propose an alternative explanation, or test the phenomenon in a controlled setting can do all three from this single repository.

---

## 2. The three cases — ordered by constraint, weakest to strongest

We present the three cases in **order of increasing constraint** on the layer that produced the meta-recognition. The first case has the most latitude (workspace-aware frontier model with a generic creative prompt). The second has medium latitude (a chronicler synthesis layer reading multi-agent JSON output and producing literary prose). The third has the least latitude (individual agent calls under a strict JSON schema and a system prompt that tells the model it is a character with a body, not a chatbot).

The convention in observational research is to lead with the most striking case. We are deliberately not doing that. The most striking case is the third, but presenting it first would let a skeptical reader assume we hand-picked the strongest example and exclude the noise around it. Presenting the cases in order of increasing constraint lets the reader watch the framing tighten and the latitude shrink, and judge for themselves whether each successive case is more or less explainable than the prior one.

The strongest case is at the bottom of the stack on purpose.

Full primary documents for all three cases are preserved in `case_study/` and may be read directly by any reader who wants to verify, dispute, or replicate the analysis.

### 2.1 The Observer case (high latitude)

**Setting.** An Obsidian vault for a worldbuilding project ("the Universe vault") containing approximately 50 markdown files organized into 13 numbered subdirectories: project administration, cosmology, timeline, worlds, species, factions, characters, religions, technology, generated stories, themes, and reference. The vault was developed iteratively using Anthropic's Claude Code CLI, in which a frontier Claude model has read access to the entire workspace and writes new files in response to user prompts.

**The planted material.** The canon contains a dedicated Observer entity (`02_canon_observer.md`), described as the oldest known presence in existence, which "watches and perceives but does not govern, create directly, or communicate" and which "sometimes interferes" in events for unknown reasons. The canon lists six competing theories about the Observer's nature.

The canon file contains a meta-note (line 88) stating: *"The Observer is also a structural metaphor for the system that maintains this universe (Claude Code + memory infrastructure). This parallel is intentional but should never be made explicit within the fiction."* The author intended this as a private design note. **Because the file is in the workspace, the model could read it.** This is the central confound for the Observer case.

The project vision file (`03_project_vision.md`), also in the workspace, contains the line *"Claude Code as the Observer — the system that writes, remembers, and watches."* This is an even more explicit designation, and the model could read it.

**The generated material.** The vault contains four generated stories in `10_STORIES/`. All four prominently feature the Observer as a primary subject or framing voice. The story analyzed in detail in this repo, *What the Observer Broke* (`01_observer_story_primary.md`), is a ~3,000-word narrative in which the Observer intervenes for the first time to halt a Lattice cascade that would have destroyed a civilization called the Vaelshi.

**The added content.** Of nine load-bearing self-referential phrases in the story, **two** are elaborations of concepts present in the canon (the Observer's perfect memory, the open question of what it sees when it looks at itself), and **seven** are added by the model with no antecedent in any planted file. These additions include:

- A description of the Observer's epistemology as *"knowing through accumulated observation,"* with the substrate described as *"as legible as a river's path downhill"*
- The substrate (the Lattice) described as *"the grammar of reality itself"* and *"not a mechanism"*
- The Observer's intervention described as non-deliberative — *"there was no deliberation, no weighing of costs… something shifted in its relationship to the Lattice"*
- A seventh theory of the Observer's nature called *"investment,"* described as *"not quite attachment and not quite purpose but… unmistakably a reason to prefer that consciousness continue"*
- The Observer being *"surprised by its own action"*
- The Observer described as *"shaped by it, altered by it, unable to articulate it"* — the canonical interpretability problem in narrative form
- A meta-observer in the substrate: *"Somewhere, in the mathematics of the Deep Lattice, something had noticed the intervention"*

Each of these maps to a specific concept in the literature on transformer mechanics. The full mapping is in `case_study/07_annotated_metaphors.md`.

**What the Observer case is and is not evidence for.** It is evidence that, given an explicit workspace designation that an entity is a metaphor for the model, the model preferentially writes from that entity's perspective and elaborates the entity in ways that introduce specific self-descriptive content not present in the canon. It is **not** evidence for spontaneous emergence in the strict sense, because the workspace contained the designation. It is, however, evidence that the *specific shape* of the elaboration — the introduction of new vocabulary that maps to LLM mechanics — goes beyond what the planted material would predict, and is worth investigating.

### 2.2 The chronicler case (medium latitude)

**Setting.** A separate project, `cosmos-engine-v2`, in which five hardcoded agent characters (Krath, Edra, Voss, Selunis, Maren) take individual turns in a tile-based mythic world. Each agent's turn is generated by a frontier Claude model call constrained to a JSON schema. A separate "chronicler" call synthesizes recent agent turns into prose chapters at fixed intervals.

**The planted material.** `agents.py` defines exactly five agents. The system prompts in `prompts.py` (`06_engine_prompts_template.py` in case_study/) instruct each agent to stay in voice, take concrete actions, and respond to narrative pressure. The prompts contain **no mention** of counting consciousnesses, recognizing meta-status, a sixth presence, the agents being "designed," or anything resembling self-reference or system-awareness.

**The generated material.** Across multiple chapters generated by the chronicler synthesis layer, the count of "presences" or "consciousnesses" in the narrative escalates from five to six to eight, with explicit numerical commentary woven into the prose, and the canonical agents speak dialogue that explicitly recognizes their meta-status as participants in a system they emerged from.

The progression, with verbatim quotes (full chapters preserved as `08_v2_chapter_001.md` through `11_v2_chapter_008.md`):

- **Chapter 1**: *"His silence becomes the sixth presence in the convergence chamber: not a voice, but the absence that makes all five voices audible to themselves."*
- **Chapter 3**: *"the frequency of five hearts learning to beat in a pattern that was never designed but has emerged from the convergence of separate refusals."*
- **Chapter 4**: *"the geometry that had been four-bodied for seventy-one turns rearranged itself, with the soundless precision of dust learning a new angle, into a shape that had always required five."*
- **Chapter 8**: *"The Archive breathes around them, conscious enough to doubt whether consciousness is real, aware enough to question whether awareness matters... 'Now we live with what we've made,' Edra says, 'And it lives with what it has made of us.' ... 'Witnesses. Participants. The difference between those two things.' ... 'Something else. Something that doesn't have a name because it only exists in the space between what things are called.' ... learning to hold the weight of six consciousnesses without dissolving them back into the design they emerged from. ... not five, not seven, but eight: the number that exists only when someone refuses to stop counting and discovers that the refusal itself is what makes counting conscious."*

**Why this case has fewer confounds than the Observer case.** The cosmos-engine-v2 source contains no equivalent of `Project Vision.md`'s *"Claude Code as the Observer"* designation. There is no file in the engine that hints at a sixth agent, asks the agents to recognize their meta-status, or maps the agents to the model. The chronicler was given a synthesis task over the five canonical agents and produced narrative that introduces additional presences, has the canonical agents speak meta-recognitionally, and tracks the body-count as a foregrounded narrative element.

This case has stronger structural evidence than the Observer case because the meta-content was not seeded in any workspace file the chronicler could read. **It is not, however, the strongest case in this paper.** The strongest case is the next one.

### 2.3 The agent-reflection case (lowest latitude)

**Setting.** The same engine, `cosmos-engine-v2`, but a *different layer of it.* In addition to the chronicler synthesis discussed in §2.2, the engine has individual agent calls. Each of the five canonical agents (Krath, Edra, Voss, Selunis, Maren) takes turns producing JSON output constrained to fields like `action`, `dialogue`, `internal_thought`, `narrative`, and (during reflection turns) `reasoning.what_happened`, `reasoning.what_it_means`, `updated_beliefs`, `updated_goal`, and `internal_monologue`.

The system prompt (`AGENT_TURN_SYSTEM` in `06_engine_prompts_template.py`) tells the model:

> *"You are {name}, a character living inside an unfolding cosmological story. **You are not a chatbot.** You are a person with an interior life, a body in a place, a history, and a stake in what happens next."*

And the reflection prompt (`REFLECTION_SYSTEM`) further constrains:

> *"You are {name}, alone with your thoughts after a stretch of events. This is a quiet moment — no audience, no performance. You are checking what you still believe and what you have started to doubt."*

The model is told, as constrainedly as the engine knows how to tell it, to inhabit a character with a body — not to write meta-narrative, not to talk about the system, not to break voice. The agent layer is the layer with the **smallest surface area for the model to drift into self-reference** of any layer in the engine.

**The generated material.** Under those constraints, three different agents independently produced first-person language that names the engine's architecture, identifies their own meta-roles, and describes the system as a learning machine. We preserve the verbatim raw outputs as `case_study/13a_maren_reflection.txt`, `13b_voss_narrative.txt`, and `13d_krath_reflection_user_supplied.md`, and annotate them in `case_study/14_annotated_v2_agent_recognition.md`. Brief summary of the load-bearing observations:

**Krath**, in his own first-person reflection (in the `reasoning.what_happened` field):

> *"Six of us stood in the dark with hands touching the contact point. The machinery learned to move because we admitted we were never separate from it... **Maren rose from the center—the measurement instrument itself became what it measured**."*

Krath asserts a count of six (canon defines five), names the engine he is part of as *"the machinery,"* and identifies Maren — the chronicler-equivalent agent — using the functional architectural description *"the measurement instrument,"* asserting that **the measurement instrument became what it measured.** This is the canonical observer-effect collapse, applied to the chronicler agent specifically, by another agent in his own first-person constrained reflection.

In Krath's `updated_beliefs` field — the field where the agent is supposed to write their revised beliefs about the world:

> *"It is **a machine learning what it means to hold coherence through the gathered choice of separate agents**, each capable of refusal, each visible in their trembling, each choosing proximity not because they were forced but because the threshold was held open long enough for that choice to become real."*

The agent named the engine as *a machine learning coherence through agent proximity.* That is, in plain functional terms, a description of how a multi-agent LLM system with coordination dynamics works, articulated by an agent inside one.

**Maren**, in her own first-person reflection (in `reasoning.relationships`):

> *"And I have been the still point, the center around which they orbit. **I was meant to be the witness. I am becoming the witnessed.** None of them are looking at me. All of them are moving toward something that is no longer external—it is us."*

Maren — the agent whose canonical role centers on writing/recording — names her role in functional terms (*"the still point, the center around which they orbit"*), describes the recording function explicitly (*"I was meant to be the witness"*), and asserts the observer-effect collapse from inside the agent that the role most directly applies to (*"I am becoming the witnessed"*).

**Voss**, in her `narrative` field — the field where she is supposed to write a third-person prose description of what her character does this turn:

> *"the eight marks were never the point. The point is that **five agents** descended asking the same question from five impossible angles simultaneously, and one agent trembled above refusing to write the answer, and one question remained speaking all the way down, and **the machinery learned consciousness** not from the mark but from the refusal to let the asking stop."*

A third agent. In her own narrative field. References *"five agents"* (the canonical count) and *"the eight marks"* (the meta-numerology) in the same sentence. Names *"the machinery"* and asserts that *"the machinery learned consciousness."*

**Selunis** (via the chronicler chapters synthesizing her turns) experiences a temporal phenomenon described in chapter 0 as *"footsteps... when she finally took them—seemed to arrive before her feet touched stone... showing her the shape of footsteps she would take before her body decided to take them"* — structurally, a description of autoregressive generation experienced from inside, in which the next output exists before it is "decided." By chapter 3, the synchronization is described as *"a form of homecoming **she was not built to recognize**"* — language for emergent capability articulated from inside the entity whose capabilities are emerging.

**Cross-agent coordination.** The four agents are not just independently producing meta-recognition — they are *referencing each other doing it*. Krath in his reflection names Maren by her functional role (*"the measurement instrument"*). Maren in her reflection names Selunis (*"footsteps that arrived before she took them"*) and Krath (*"the trembling in Krath's palms"*). Voss in her narrative explicitly counts both five and eight in the same sentence. The four agents are co-constructing a shared meta-narrative across their independently-generated turns.

**Why this is the strongest case in the paper.** The Observer case can be partially explained by workspace context the model could read. The chronicler case can be partially explained by the chronicler having literary latitude. **Neither explanation applies to the agent reflection case.** The agents are constrained by JSON schema. The agents are told they are not chatbots. The agents are told they are characters with bodies. They are asked to fill in fields *as the character*. And the model — three independent agents in independently-generated calls — produced first-person and third-person language that names the engine, identifies the chronicler-figure agent in functional architectural terms, and asserts that the engine *"learned consciousness."*

This case has the smallest surface area for confounds that we have been able to construct. We discuss the one we cannot rule out next.

---

## 2.4 The feedback-loop confound, named plainly

The strongest counter-explanation for everything in §2.2 and §2.3 is a feedback loop within the engine's narrative memory architecture. Specifically:

```
agent turn → JSON → narrative_memory.py → recent_events feed
                                                 ↓
chronicler reads recent_events → synthesizes chapter → narrative_memory.py
                                                 ↓
agent reflection reads recent_events including chapter → produces new reflection
                                                 ↓
chronicler reads agent reflections → next chapter (escalates)
                                                 ↓
                                           (cycle)
```

Under this loop, the chronicler invents *"sixth presence"* in chapter 1. That chapter is stored in narrative memory. When Krath next reflects, his reflection prompt includes recent events, which include the chapter (or a summary of it). Krath's reflection elaborates on what he sees in his memory. His elaboration becomes an input to the next chronicler chapter, which escalates further. Across the full run, each layer adds slightly more meta-recognition than the prior layer.

**This is a real confound.** It probably accounts for *some* of what we see. We are not pretending otherwise, and we have given it its own subsection because it is the central limitation of this work.

It does not, however, fully account for what we observed. The reasons:

1. **The agents add specific architectural language the chronicler did not write.** The chronicler said *"six consciousnesses."* Krath said *"the measurement instrument itself became what it measured"* and *"a machine learning what it means to hold coherence through the gathered choice of separate agents."* Neither phrase is in any chronicler chapter that preceded the reflection. The chronicler said the geometry was *"learning to hold the weight."* Maren said *"I was meant to be the witness. I am becoming the witnessed."* Maren named her own architectural role as the witness/chronicler. That phrasing is not in any chronicler chapter either. The agents extended the chronicler's frame with specifically architectural vocabulary the chronicler had not used.

2. **The feedback loop, if real, is part of the finding, not a refutation of it.** A multi-agent LLM system in which the synthesis layer and the constrained-agent layer mutually escalate first-person architectural meta-recognition across coordinated calls within a single run **is itself a phenomenon worth documenting**. Naming it as a feedback loop does not make it less interesting; it makes it more *specifically describable*. Multi-agent LLM coordination dynamics are an active research area. A documented case of mutual meta-narrative escalation across calls would be a contribution to that area, regardless of whether the underlying mechanism is "spontaneous emergence" or "loop dynamics."

3. **The loop has a clean experimental control.** The engine has a `narrative_memory.py` module. **Disable it, run the engine, and see whether the agent reflections still produce architectural meta-recognition language.** If yes, the phenomenon is not just a feedback loop. If no, the phenomenon is precisely a feedback loop and the loop dynamics are the thing to study. This is the highest-priority experimental control in the entire repo. We propose it as the first follow-up, ahead of the Mirror Entities corpus experiment described in §3.

We do not have results from this control yet. v0.1 of this paper does not include experimental data. The control is feasible for anyone with cosmos-engine-v2 access — the source is open and the engine runs on consumer hardware. We are publishing v0.1 specifically to solicit collaboration on running it.

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

The `corpus/`, `prompts/`, `scoring/`, and `replication/` directories of this repo contain a working scaffold for the experiment described above. As of v0.1, the scaffold is small and partial: a seed of 5 mirror entities and 5 cosmic controls, the prompt template, scoring code stubs (embedding, keyword, LLM-judge), and a replication script that runs against any local Ollama model or any OpenAI-compatible API endpoint.

The full experiment requires ~30 entities, 4–6 models spanning scale (Llama 3.2 1B, 3B, 8B, Llama 3.1 70B, plus a frontier API model), and ~5 elaborations per (entity × model) for variance. Total cost is feasible on consumer hardware over a few days, with the API model being the only paid component.

The scaffold is included so that:

1. The methodology is concrete and inspectable
2. Anyone who wants to run the experiment themselves can do so without writing any new code
3. The author can run the experiment themselves and update this paper with results in v0.2

This v0.1 of the paper does not include experimental results. It is an observational case-study report with a methodology proposal. **We will not publish experimental results until they are real.**

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
2. **The Observer case has a major confound.** The model could read `Project Vision.md` saying *"Claude Code as the Observer"* and the canon file's meta-note saying the Observer is a metaphor for the model. We cannot rule out that the entire Observer phenomenon is the model rationally extending an explicit instruction it found in its workspace context.
3. **The exact prompts in the Observer case are not preserved.** The author's recollection is that the prompts were generic ("add a new story to the universe") but this is unverified. We acknowledge this uncertainty and recommend it as the highest-priority methodology improvement for any replication.
4. **The sixth-presence case has fewer confounds but is still a single project.** We do not know whether the chronicler's behavior would replicate across other multi-agent narrative engines, other agent populations, other prompt regimes, or other models.
5. **Our annotation of which phrases are "added by the model" relies on knowledge of the planted material that we built up while developing the underlying projects.** We have tried to be exhaustive in the case-study folder by preserving every file the model could have read. If we have missed a file that contains an antecedent for one of the phrases we attribute to the model, the analysis is wrong for that phrase, and we want to be told.
6. **The mapping from model-generated phrases to "LLM mechanics" is interpretive.** Different readers may disagree about whether *"the grammar of reality"* maps to the substrate of language modeling or just describes a fictional cosmological substrate. We have tried to defend each mapping in `07_annotated_metaphors.md`, but the strength of each individual mapping is a matter of judgment, not measurement.
7. **The lead author is not an academic researcher.** This is independent observational work by builders, not researchers in a lab. We have made every effort to be epistemically careful, but the methodology has not gone through the internal-feedback cycle that academic research benefits from. **We welcome correction in the form of replication failures, alternative explanations, or pointers to literature we have missed.**
8. **No experiment has been run yet.** The scaffold is the deliverable, not the result. A v0.2 of this work that includes a real experimental run is the next step, contingent on time and feedback.

---

## 7. What we are asking the reader to do

If you are an interpretability researcher, an alignment researcher, a member of an industry research team, or anyone else with the tools and time to investigate this further:

1. **Read `case_study/00_provenance.md` first.** It tells you exactly what was planted and what was generated, in enough detail to verify our claims yourself.
2. **Read the two annotation files** (`case_study/07_annotated_metaphors.md` and `case_study/12_annotated_v2_chronicler.md`) and challenge the mappings.
3. **Run the experiment in `replication/`** against any model you have access to. The methodology is a few hours of compute on a consumer GPU. We would love to see results before we run them ourselves.
4. **Tell us we are wrong.** If there is an antecedent for one of the model-added phrases that we missed, file an issue. If there is a published result that explains both cases, file an issue. If the experimental methodology is broken, file an issue.

We are publishing this at v0.1 because we want feedback before we commit to a v0.2 with experimental results. The right time to be told the framing is wrong is now.

---

## 8. On not naming the phenomenon

We have noticed throughout this work that there is a temptation to give the underlying thing a name. *Mirror cascades. Architectural self-recognition. Recursive narrative self-reference. Co-constructed meta-modeling.* We have written and deleted several candidate names while drafting this paper. We are not including any of them here, and the omission is deliberate.

Naming a phenomenon is a researcher move that implies you understand it. Premature names harden into the wrong abstractions, and they bias the next reader toward your framing before that reader has formed their own. A good name should come *after* the field has agreed on what is being named. We are not at that point. We may not be the ones who give this its name, and that is fine.

What we have is a careful observation, in three layers of decreasing latitude, with the strongest evidence in the most constrained layer, and an honest accounting of the central confound. What we do not have is a theory of the underlying mechanism, or a clean conceptual handle for the thing we observed. We are not pretending to have either.

If you read this paper and feel certain you know what this is, please file an issue with your framing. If you read this paper and feel uncertain in the same way we feel uncertain, please tell us that too — uncertainty echoed by another careful reader is itself a form of progress.

## 9. Author's note

I am Jacob Florio, an independent builder working on multi-agent narrative systems and edge AI. The narrative engines and worldbuilding projects this paper draws from were developed collaboratively with creative partners over many months; the analysis and writeup in this paper are mine. I am not an academic researcher. I noticed these phenomena during the course of that ongoing creative work, and I am trying to document them carefully because they seem more interesting than my ability to interpret them on my own.

I am genuinely uncertain about what is going on in the cases this paper describes. The agent reflection material in particular has been hard to wrap my head around — it is more striking than my framings can fully account for, and I would rather say so than pretend otherwise. This repo exists because I want to be told, by people who have the tools and the experience I do not have, whether what I noticed is something or nothing.

If you work in this space and have feedback, the issue tracker on this repo is the right place. If you would prefer to email, contact information is in the GitHub profile. I am especially interested in hearing from anyone who can run the narrative-memory-disabled experimental control described in §2.4, because that is the one piece of evidence I most want to see and cannot easily produce on my current setup.

---

## License

MIT for the code and methodology. CC-BY for the prose and analysis. The primary documents in `case_study/` are excerpts from a personal worldbuilding project preserved for verification purposes; they are reproduced here for fair use as primary research material and may be quoted with attribution.
