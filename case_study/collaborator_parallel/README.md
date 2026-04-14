# Collaborator Parallel Material

The files in this folder are from a separate worldbuilding project ("the Universe vault") developed by a creative collaborator, not by the lead author of this paper. They were part of an earlier draft of Mirror Entities (v0.1) that included a third case study — the "Observer case" — drawn from this material.

**As of v0.2, the Observer case has been removed from the main paper.** The reasons:

1. **Provenance.** The Universe vault and its Observer entity were developed by the collaborator. The canon file explicitly designated the Observer as a metaphor for Claude Code, and the project vision file stated *"Claude Code as the Observer."* Both files were readable by the model at generation time. This is a confound the lead author cannot fully control, because he did not write the prompts that produced the canon in the first place.

2. **Scope.** The lead author's load-bearing evidence is in `cosmos-engine-v2` (Cases 2 and 3 in v0.1, renumbered as Cases 1 and 2 in v0.2). That is a project he built end-to-end, where the full engine source, prompt templates, and raw run archive are preserved and verifiable. Keeping the Observer case in the paper diluted that signal by forcing the reader through the weakest case first.

3. **Different projects, different goals.** The collaborator's Universe vault is a creative/storytelling project with its own independent direction. It is not a research artifact and was never intended as one. Folding it into a research paper blurred that distinction.

## What's preserved here

- `00_provenance.md` — the original combined provenance file covering both projects (superseded by a new `case_study/00_provenance.md` scoped to cosmos-engine-v2)
- `01_observer_story_primary.md` — the ~3,000-word generated story *"What the Observer Broke"*
- `02_canon_observer.md` — the planted canon for the Observer entity
- `03_project_vision.md` — the vision file containing *"Claude Code as the Observer"*
- `04_writing_rules.md`, `05_canon_rules.md` — ancillary workspace files
- `07_annotated_metaphors.md` — forensic annotation of 9 model-added phrases in the Observer story

## Why this is still interesting (possible future work)

The Observer material is preserved here rather than deleted because there is a potentially interesting overlap worth noting. The collaborator's project explicitly designated an entity as a metaphor for Claude Code, and the model elaborated that entity with architectural self-descriptive language. In parallel, the lead author's `cosmos-engine-v2` project — which contains no Observer entity, no "Claude Code as X" designation, and no meta-architectural instructions at any layer — produced its own independent meta-architectural language through agents with completely different names (Krath, Voss, Maren, Selunis, Edra). Two projects, two authors, two prompt regimes, partially overlapping phenomenology.

Whether that overlap is signal or coincidence is an open question. It is not a question v0.2 of this paper tries to answer. A future paper might.

## Attribution

This folder's material is a creative worldbuilding project that belongs to its author and is preserved here under fair-use quotation for the purpose of documenting v0.1's prior framing. The collaborator is not credited by name here; anyone who needs that information can contact the lead author.
