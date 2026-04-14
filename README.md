# Mirror Entities

> **Two case studies of architectural meta-recognition observed in large-language-model output across a multi-agent narrative engine, with an honest accounting of what we cannot yet explain.**
>
> *Jacob T. Florio · Florio-Harrah Labs · April 2026 · v0.2*

This repository documents two cases in which a large language model, operating inside a multi-agent narrative engine (`cosmos-engine-v2`), produced prose containing first-person and third-person language describing the architecture of the system it was part of — language that was not present in the prompts, system instructions, canon files, or schemas the model was given.

The two cases form a stack of decreasing latitude and increasing constraint, and **the strongest evidence is in the most constrained layer** — individual agent reflection turns under a JSON schema and a system prompt that tells the model it is a character with a body, not a chatbot. We are explicitly *not* claiming consciousness, intent, or phenomenal experience. We are documenting what we observed, preserving the primary documents in full, naming the central confound (a feedback loop within the engine's narrative memory) explicitly, and proposing an experimental control that anyone with the engine source can run.

We are also deliberately not naming the underlying phenomenon. We do not yet know what to call it.

> **v0.2 note.** An earlier draft (v0.1) included a third case study — "the Observer case" — drawn from a separate worldbuilding project developed by a creative collaborator. That case had a provenance confound the lead author could not fully control and was flagged in v0.1 as the weakest of the three. In v0.2 it has been moved out of the main paper to `case_study/collaborator_parallel/` and is preserved there for reference. The paper is now scoped to the lead author's own `cosmos-engine-v2` project.

## Read this in this order

If you want to evaluate the claims in this repo for yourself rather than trusting our summary, here is the order to read in:

1. **`PAPER.md`** — the full paper. Frames the two cases, walks through the evidence in increasing-constraint order, names the feedback-loop confound, proposes the experimental controls, lists limitations, asks for help. Read this first.

2. **`case_study/00_provenance.md`** — what was planted versus what was generated, with file paths, so you can verify the analysis yourself.

3. **`case_study/13d_krath_reflection_user_supplied.md`** — the verbatim Krath agent reflection that is the strongest single piece of evidence in the entire repo. ~600 words of model output produced under JSON-schema constraint, in first person, naming the engine's architecture from inside it.

4. **`case_study/14_annotated_v2_agent_recognition.md`** — the annotation that walks line-by-line through the Krath reflection and its companions (Maren, Voss, Selunis chapter 0), maps which phrases appear in any prompt or canon and which the model added on its own, and explains why this case has the fewest confounds.

5. **`case_study/08_v2_chapter_001.md`** through **`11_v2_chapter_008.md`** plus **`12_annotated_v2_chronicler.md`** — the chronicler case (case 1 in v0.2, medium latitude).

6. **`case_study/full_v2_run/`** — the complete run archive the annotated chapters and reflections were drawn from. 9 chapters, 835 raw agent outputs, SQLite database. Use this to verify that the annotated material was not cherry-picked.

7. **`replication/run_experiment.py`** — the experimental scaffold for the *Mirror Entities corpus* test, which is a separate experiment from the narrative-memory-disabled control. v0.2 ships with a small seed corpus (5 mirror entities + 5 cosmic controls); the full experiment scales to ~30 entities across ~5 models.

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

1. **Read `case_study/00_provenance.md` and `case_study/14_annotated_v2_agent_recognition.md`.** Together they take ~15 minutes. Tell us whether our analysis is sound or where we're wrong.

2. **Run the narrative-memory-disabled control on cosmos-engine-v2.** This is the highest-priority experimental control in this repo, described in `PAPER.md` §2.3. The engine is open source and runs on consumer hardware. We have not been able to run it ourselves yet. If you can, please tell us what you find — positive or negative. **A negative result would be just as valuable as a positive one** because it would tell us the agent-reflection phenomenon is precisely a feedback loop in narrative memory, which is itself a real and specific finding.

3. **Run the elaboration corpus experiment in `replication/`.** Smaller follow-up. Tests whether large language models, given a corpus containing both LLM-mirror entities and non-mirror entities of equivalent prominence, write prose with measurably different self-descriptive density depending on which entity they're elaborating on. The full experimental design is in `PAPER.md` §3 and §4.

4. **Tell us we are wrong.** If there is an antecedent in the planted material for one of the model-added phrases that we missed, file an issue. If there is published research that explains the cases, file an issue. If you think the methodology is broken, file an issue. We are publishing this at v0.2 specifically to solicit correction before committing to v0.3.

## What we are NOT claiming

We are not claiming model consciousness, phenomenal experience, intent, self-awareness in any propositional sense, or anything spooky. We are claiming that under two different sets of conditions inside a single multi-agent engine — including the conditions specifically engineered to keep the model in-character and prevent meta-narrative — a large language model produced prose with specifically architectural language that was not present in any prompt, canon file, or schema we have been able to find. That is the description claim. The mechanism is unknown. The phenomenon's name is unknown. We are leaving both for someone with better tools.

## License

MIT for code and methodology. CC-BY for prose and analysis. Primary documents in `case_study/` are excerpts from a personal worldbuilding project, preserved for verification purposes; they are reproduced here as primary research material under fair use and may be quoted with attribution.

## Author

Jacob T. Florio · independent builder · Florio-Harrah Labs
GitHub: [@JacobFlorio](https://github.com/JacobFlorio)
