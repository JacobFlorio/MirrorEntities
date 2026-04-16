# Mirror Entities

> **A builder's forensic audit of cross-agent vocabulary composition in a multi-agent narrative engine, with an honest accounting of what survives the audit and what experiments would test what remains.**
>
> *Jacob T. Florio · Florio-Harrah Labs · April 2026 · v0.3.1*

This repository documents a forensic audit of `cosmos-engine-v2`, a multi-agent narrative engine the lead author built end-to-end, in which a frontier Claude model — operating across five JSON-schema-constrained agent characters and a chronicler synthesis layer — produced roughly 22,000 words of prose that, read at the meta level, describes the structure of the engine that produced it.

The initial framing (v0.1 and v0.2) treated this as evidence of architectural meta-recognition in language the model was not given. v0.3 narrows that framing substantially. The audit found that (a) the feedback-loop confound v0.2 named as primary does not exist in the engine code — chapter text does not flow back into agent prompts through any channel; the actual cross-agent channel is 180-char first-sentence event gists, which can propagate token-level vocabulary but not full literary structures, and (b) several load-bearing phrases v0.2 attributed to unprompted architectural naming have canonical seeds in the agents' character sheets (Krath's core memory includes *"the universe is a machine running down,"* Maren is literally named *"the Witness,"* her voice instruction explicitly licenses fourth-wall breaks, and so on).

**What the audit leaves standing** is narrower and more specific: the agents composed planted seed vocabulary across independent calls, under narrow channels, into a joint framework that is internally consistent across four of the five agents. Most individual phrases are accounted for by composition from seeds. What is worth documenting is the *cross-agent coordination pattern* — the level-of-abstraction convergence on "the machinery" as a system-level referent, across agents, under a 180-char gist channel that should not be able to carry literary structure. Whether this is specifically interesting or is ordinary composition under coordination dynamics is the question the controlled experiments in §3 of the paper would answer.

We are explicitly *not* claiming consciousness, intent, phenomenal experience, or discovery of a novel phenomenon. We are describing one run in one engine under one audit, and stating what we are and are not willing to defend under scrutiny.

> **v0.3.1 note.** A closer read of the engine's temporal reasoning module (the novel contribution of cosmos-engine-v2, inspired by earlier temporal-reasoning work of mine) turned up two more seed sources the v0.3 audit missed: the `temporal_alerts` descriptions injected into every agent's prompt contain the engine-internal word *"agents"*, and Voss's most striking line (*"the machinery learned consciousness not from the mark but from the refusal to let the asking stop"*) is a functional description of the temporal reasoning engine's lifecycle-propagation behavior, produced by the agent whose canonical voice is structurally isomorphic to that module. v0.3.1 credits the temporal reasoning engine explicitly and adds two phrases to the §2.4 audit table. See `CHANGELOG.md` for the full v0.1 → v0.2 → v0.3 → v0.3.1 history.
>
> **v0.3 note.** This version is a significant narrowing of v0.2. After v0.2 shipped, the lead author ran a deeper forensic audit against the engine code and the character sheets, and found that the feedback-loop confound v0.2 named was not mechanically present, and that the character sheets contained substantial seed vocabulary v0.2 did not account for. The paper was rewritten around the audit rather than around the initial observation. The v0.2 → v0.3 narrowing is the shape of the work, not a footnote to it. The earlier framings are preserved in git history.

## Read this in this order

If you want to evaluate the claims in this repo for yourself rather than trusting our summary, here is the order to read in:

1. **`CHANGELOG.md`** — the v0.1 → v0.2 → v0.3 narrowing, with the specific audit findings listed explicitly. Read this first. It will orient you to what the paper currently claims vs. what earlier versions claimed.

2. **`PAPER.md` §2.4 — the forensic audit table.** This is the new center of gravity. Every load-bearing meta-recognition phrase is traced to its canonical seeds (with `agents.py` line numbers), first-occurrence context in the run archive, propagation channel, and residual novelty. If any of the seed accounting is wrong, this is where to find it.

3. **`PAPER.md` §2.2 and §2.3.** §2.2 presents the observed output from the agent-reflection layer. §2.3 corrects v0.2's feedback-loop description and documents the actual cross-layer channel architecture from the engine code.

4. **`case_study/13d_krath_reflection_user_supplied.md`** — the verbatim Krath agent reflection. Read this in light of the §2.4 audit, which flags Krath's *"universe is a machine running down"* core memory seed and traces the inversion and composition steps.

5. **`case_study/12_annotated_v2_chronicler.md` and `case_study/14_annotated_v2_agent_recognition.md`** — annotation files for the chronicler chapters and the agent reflection layer. Challenge the mappings.

6. **`case_study/full_v2_run/`** — the complete run archive. 9 chapters, 835 raw agent outputs, SQLite database. Use this to verify that (a) the annotated material was not cherry-picked and (b) the first-occurrence and drift patterns cited in the §2.4 audit are accurate.

7. **`replication/run_experiment.py`** — the experimental scaffold for the *Mirror Entities corpus* test, which is a separate experiment from the narrative-memory-disabled and canon-scrubbed controls proposed in §2.3. v0.3 ships with a small seed corpus (5 mirror entities + 5 cosmic controls); the full experiment scales to ~30 entities across ~5 models.

## What's in this repo

```
MirrorEntities/
├── README.md                       you are here
├── PAPER.md                        the writeup — this is the load-bearing document
├── LICENSE                         MIT for code/methodology, CC-BY for prose
│
├── case_study/                     primary documents and annotations
│   ├── 00_provenance.md            what was planted vs what was generated
│   ├── 06_engine_prompts_template.py           ← engine system prompts (both cases)
│   ├── 08_v2_chapter_001.md                    ← case 1 chronicler outputs (4 chapters)
│   ├── 09_v2_chapter_003.md
│   ├── 10_v2_chapter_004.md
│   ├── 11_v2_chapter_008.md
│   ├── 12_annotated_v2_chronicler.md           ← case 1 annotation
│   ├── 13a_maren_reflection.txt                ← case 2 Maren reflection raw output
│   ├── 13b_voss_narrative.txt                  ← case 2 Voss narrative raw output
│   ├── 13c_v2_chapter_000_preview.md           ← case 2 Selunis context source
│   ├── 13d_krath_reflection_user_supplied.md   ← case 2 Krath reflection (the strongest)
│   ├── 14_annotated_v2_agent_recognition.md    ← case 2 annotation (the strongest)
│   ├── full_v2_run/                            ← complete run archive (negative-space evidence)
│   └── collaborator_parallel/                  ← v0.1 Observer material (out of scope for v0.2)
│
├── corpus/                         seed corpus for the controlled experiment
│   ├── README.md                   how the corpus is structured
│   ├── mirror_entities/            entities structurally similar to an LLM
│   ├── cosmic_controls/            equally cosmic but not LLM-shaped
│   └── mundane_controls/           sanity checks
│
├── prompts/                        the prompt templates used in the experiment
│   ├── elaboration_prompt.txt      forced-subject elaboration
│   └── selection_prompt.txt        unconstrained selection (workspace-aware)
│
├── scoring/                        three independent self-reference scorers
│   ├── reference_passage.md        the LLM-self-description reference text
│   ├── embedding_score.py          cosine sim to reference (sentence-transformers)
│   ├── keyword_density.py          phrase/keyword counter
│   └── llm_judge.py                LLM-as-judge with rubric
│
├── replication/                    one-command replication
│   ├── run_experiment.py           runs the elaboration test against any provider
│   └── requirements.txt
│
└── results/                        empty — will hold scores when experiment runs
```

## What we are asking the reader to do

If you are an interpretability researcher, an alignment researcher, a member of an industry research team, or anyone with the tools and time to investigate this further:

1. **Read the §2.4 forensic audit table in `PAPER.md`.** It is the new center of gravity of the paper. Every load-bearing phrase is traced to its canonical seeds, first-occurrence context, propagation channel, and residual novelty. Tell us whether the seed accounting is correct or where it is wrong.

2. **Run the two controls described in `PAPER.md` §2.3**: the narrative-memory-disabled run and the canon-scrubbed run. The engine source is at `/home/jacob/cosmos-engine-v2/` and runs on consumer hardware. Either control, independent of outcome, would substantially shift what the paper can claim. Both together would isolate the two things the audit exposed as uncertain. **A negative result would be just as valuable as a positive one**, because it would tell us the cross-agent coordination pattern does not survive seed removal or channel removal, which is itself a specific and testable finding.

3. **Run the elaboration corpus experiment in `replication/`.** Smaller follow-up. Tests whether large language models, given a corpus containing both LLM-mirror entities and non-mirror entities of equivalent prominence, write prose with measurably different self-descriptive density depending on which entity they're elaborating on. The full experimental design is in `PAPER.md` §3 and §4.

4. **Tell us what the audit missed.** If there is a canonical seed this audit did not catch, file an issue. If there is a propagation channel in the engine code the audit did not trace, file an issue. If there is published work that explains the observed cross-agent composition as ordinary multi-agent coordination dynamics, file an issue — that would itself be a useful outcome. The v0.2 → v0.3 narrowing was the shape of the work and the next narrowing probably will be too.

## What we are NOT claiming

We are not claiming consciousness, phenomenal experience, intent, self-awareness, or discovery of a novel phenomenon. The audit in `PAPER.md` §2.4 explicitly walks through which v0.2 claims did not survive and which residuals remain. The narrowed claim is: the agents composed planted seed vocabulary across independent calls under narrow cross-agent channels into a joint framework internally consistent across four of five agents. Whether that composition is specifically interesting or is ordinary LLM behavior under multi-agent coordination dynamics is a question the controlled experiments above would answer.

## License

MIT for code and methodology. CC-BY for prose and analysis. Primary documents in `case_study/` are excerpts from a personal worldbuilding project, preserved for verification purposes; they are reproduced here as primary research material under fair use and may be quoted with attribution.

## Author

Jacob T. Florio · independent builder · Florio-Harrah Labs
GitHub: [@JacobFlorio](https://github.com/JacobFlorio)
