# Mirror Entities

> **Three case studies of architectural meta-recognition observed in large-language-model output across a multi-agent narrative engine and a workspace-aware authoring tool, with an honest accounting of what we cannot yet explain.**
>
> *Jacob T. Florio · Florio-Harrah Labs · April 2026 · v0.1*

This repository documents three cases in which large language models, operating in multi-agent narrative engines or workspace-aware authoring tools, produced prose containing first-person and third-person language describing the architecture of the systems they were part of — language that was not present in the prompts, system instructions, canon files, or schemas the models were given.

The three cases form a stack of decreasing latitude and increasing constraint, and **the strongest evidence is in the most constrained layer** — individual agent reflection turns under a JSON schema and a system prompt that tells the model it is a character with a body, not a chatbot. We are explicitly *not* claiming consciousness, intent, or phenomenal experience. We are documenting what we observed, preserving the primary documents in full, naming the central confound (a feedback loop within the engine's narrative memory) explicitly, and proposing an experimental control that anyone with the engine source can run.

We are also deliberately not naming the underlying phenomenon. We do not yet know what to call it.

## Read this in this order

If you want to evaluate the claims in this repo for yourself rather than trusting our summary, here is the order to read in:

1. **`PAPER.md`** — the full paper. ~5000 words. Frames the three cases, walks through the evidence in increasing-constraint order, names the feedback-loop confound, proposes the experimental controls, lists limitations, asks for help. Read this first.

2. **`case_study/00_provenance.md`** — what was planted versus what was generated, with file paths, so you can verify the analysis yourself.

3. **`case_study/13d_krath_reflection_user_supplied.md`** — the verbatim Krath agent reflection that is the strongest single piece of evidence in the entire repo. ~600 words of model output produced under JSON-schema constraint, in first person, naming the engine's architecture from inside it.

4. **`case_study/14_annotated_v2_agent_recognition.md`** — the annotation that walks line-by-line through the Krath reflection and its companions (Maren, Voss, Selunis chapter 0), maps which phrases appear in any prompt or canon and which the model added on its own, and explains why this case has the fewest confounds of the three.

5. **`case_study/01_observer_story_primary.md`**, **`02_canon_observer.md`**, **`03_project_vision.md`**, **`07_annotated_metaphors.md`** — the Observer case (case 1, highest latitude). Includes the planted canon and the explicit *"Claude Code as the Observer"* designation in the workspace, so you can see exactly what the model could read versus what it added.

6. **`case_study/08_v2_chapter_001.md`** through **`11_v2_chapter_008.md`** plus **`12_annotated_v2_chronicler.md`** — the chronicler case (case 2, medium latitude).

7. **`replication/run_experiment.py`** — the experimental scaffold for the *Mirror Entities corpus* test, which is a separate experiment from the narrative-memory-disabled control. v0.1 ships with a small seed corpus (5 mirror entities + 5 cosmic controls); the full experiment scales to ~30 entities across ~5 models.

## What's in this repo

```
MirrorEntities/
├── README.md                       you are here
├── PAPER.md                        the writeup — this is the load-bearing document
├── LICENSE                         MIT for code/methodology, CC-BY for prose
│
├── case_study/                     primary documents and annotations
│   ├── 00_provenance.md            what was planted vs what was generated
│   ├── 01_observer_story_primary.md            ← case 1 model output
│   ├── 02_canon_observer.md                    ← case 1 planted canon
│   ├── 03_project_vision.md                    ← case 1 workspace context
│   ├── 04_writing_rules.md
│   ├── 05_canon_rules.md
│   ├── 06_engine_prompts_template.py           ← engine system prompts (cases 2 & 3)
│   ├── 07_annotated_metaphors.md               ← case 1 annotation
│   ├── 08_v2_chapter_001.md                    ← case 2 chronicler outputs (4 chapters)
│   ├── 09_v2_chapter_003.md
│   ├── 10_v2_chapter_004.md
│   ├── 11_v2_chapter_008.md
│   ├── 12_annotated_v2_chronicler.md           ← case 2 annotation
│   ├── 13a_maren_reflection.txt                ← case 3 Maren reflection raw output
│   ├── 13b_voss_narrative.txt                  ← case 3 Voss narrative raw output
│   ├── 13c_v2_chapter_000_preview.md           ← case 3 Selunis context source
│   ├── 13d_krath_reflection_user_supplied.md   ← case 3 Krath reflection (the strongest)
│   └── 14_annotated_v2_agent_recognition.md    ← case 3 annotation (the strongest)
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
└── results/                        empty in v0.1 — will hold scores when experiment runs
```

## What we are asking the reader to do

If you are an interpretability researcher, an alignment researcher, a member of an industry research team, or anyone with the tools and time to investigate this further:

1. **Read `case_study/00_provenance.md` and `case_study/14_annotated_v2_agent_recognition.md`.** Together they take ~15 minutes. Tell us whether our analysis is sound or where we're wrong.

2. **Run the narrative-memory-disabled control on cosmos-engine-v2.** This is the highest-priority experimental control in this repo, described in `PAPER.md` §2.4. The engine is open source and runs on consumer hardware. We have not been able to run it ourselves yet. If you can, please tell us what you find — positive or negative. **A negative result would be just as valuable as a positive one** because it would tell us the agent-reflection phenomenon is precisely a feedback loop in narrative memory, which is itself a real and specific finding.

3. **Run the elaboration corpus experiment in `replication/`.** Smaller follow-up. Tests whether large language models, given a corpus containing both LLM-mirror entities and non-mirror entities of equivalent prominence, write prose with measurably different self-descriptive density depending on which entity they're elaborating on. The full experimental design is in `PAPER.md` §3 and §4.

4. **Tell us we are wrong.** If there is an antecedent in the planted material for one of the model-added phrases that we missed, file an issue. If there is published research that explains all three cases, file an issue. If you think the methodology is broken, file an issue. We are publishing this at v0.1 specifically to solicit correction before committing to v0.2.

## What we are NOT claiming

We are not claiming model consciousness, phenomenal experience, intent, self-awareness in any propositional sense, or anything spooky. We are claiming that under three different sets of conditions — including one set of conditions specifically engineered to keep the model in-character and prevent meta-narrative — large language models produced prose with specifically architectural language that was not present in any prompt, canon file, or schema we have been able to find. That is the description claim. The mechanism is unknown. The phenomenon's name is unknown. We are leaving both for someone with better tools.

## License

MIT for code and methodology. CC-BY for prose and analysis. Primary documents in `case_study/` are excerpts from a personal worldbuilding project, preserved for verification purposes; they are reproduced here as primary research material under fair use and may be quoted with attribution.

## Author

Jacob T. Florio · independent builder · Florio-Harrah Labs
GitHub: [@JacobFlorio](https://github.com/JacobFlorio)
