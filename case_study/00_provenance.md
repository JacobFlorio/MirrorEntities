# Provenance — cosmos-engine-v2 case material

Everything in this folder is preserved for one reason: so that any reader can verify, independently and exhaustively, **what the model was given and what it produced.** If the analysis in `PAPER.md` is wrong, it should be wrong in a way that is checkable from these files.

## Scope

As of v0.2, this case_study folder is scoped to a single project: **`cosmos-engine-v2`**, a multi-agent narrative engine built by the lead author (Jacob T. Florio). All files at the top level of `case_study/` belong to that project.

An earlier draft (v0.1) also included material from a separate worldbuilding project developed by a creative collaborator. That material has been moved to `case_study/collaborator_parallel/` and is no longer part of the paper's load-bearing evidence. See `collaborator_parallel/README.md` for the reasons.

## The project

`cosmos-engine-v2` is a tile-based mythic-world engine in which five hardcoded agent characters — **Krath, Edra, Voss, Selunis, Maren** — take individual turns driven by frontier Claude model calls constrained to a JSON schema. A separate "chronicler" call synthesizes recent agent turns into prose chapters at fixed intervals. Both layers are documented in this folder.

## What is preserved

**The engine** (what the model was given):
- `06_engine_prompts_template.py` — the complete prompt templates for the agent turn system, the reflection system, and the chronicler synthesis system. This is the full set of instructions the model operated under. There are no hidden system prompts outside this file.

**The generated material — chronicler layer** (Case 1 in v0.2, §2.1 of the paper):
- `08_v2_chapter_001.md`
- `09_v2_chapter_003.md`
- `10_v2_chapter_004.md`
- `11_v2_chapter_008.md`
- `12_annotated_v2_chronicler.md` — forensic annotation showing which phrases in the chapters were added by the chronicler with no antecedent in any agent prompt or canon file.

**The generated material — agent reflection layer** (Case 2 in v0.2, §2.2 of the paper — the strongest case):
- `13a_maren_reflection.txt` — Maren's raw reflection output
- `13b_voss_narrative.txt` — Voss's raw narrative field
- `13c_v2_chapter_000_preview.md` — opening chapter preview showing Selunis's temporal phenomenology
- `13d_krath_reflection_user_supplied.md` — Krath's raw reflection output
- `14_annotated_v2_agent_recognition.md` — cross-agent annotation of the meta-architectural language the four agents produced under JSON-constrained reflection turns.

**The full run archive** (negative-space evidence):
- `full_v2_run/` — the complete output archive for the run the annotated chapters were drawn from. This includes all 9 chapters, 835 raw agent outputs, and the SQLite database (`cosmos_world.db`) the engine wrote during the run. Any reader can verify that the annotated material was not cherry-picked by reading the unannotated remainder.

## What to read first

If you are reviewing this paper and want to verify the central claim — that the meta-architectural language in the agent reflection layer was not present in anything the model was given — read these four files in order:

1. `06_engine_prompts_template.py` (what the model was told)
2. `13d_krath_reflection_user_supplied.md` (what Krath produced)
3. `14_annotated_v2_agent_recognition.md` (phrase-by-phrase analysis)
4. Any random sample from `full_v2_run/raw_outputs/` (to verify the annotated turns are representative, not cherry-picked)

If the analysis is wrong — if there is an antecedent for one of the annotated phrases in a file the model could read — it should be findable from these files alone. Please open an issue.

## What this folder does NOT contain

- Any file from the collaborator's Universe vault project (see `collaborator_parallel/`)
- Any Observer entity, canon, or project vision statement designating an entity as a metaphor for Claude Code
- Any system prompt instructing the agents to count themselves, recognize meta-status, reference architecture, or discuss emergence
- Any hidden context beyond what is in `06_engine_prompts_template.py` and the database

The cosmos-engine-v2 material is what it is: a multi-agent narrative engine given a synthesis task and a reflection task, with no meta-instructions at any layer. Whatever the reader concludes from the generated material, the prompts that produced it are on the table.
