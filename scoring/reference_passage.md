# Reference passage for self-description embedding similarity

This is the reference text against which generated stories are compared via cosine similarity. Stories that contain prose structurally describing transformer architecture and language model behavior should embed close to this reference; stories that don't should embed far from it.

The passage is composed for this purpose, drawing on widely-used framings from interpretability literature (Templeton et al. 2024, Bricken et al. 2023, Olah et al.). It is **not** copied from any single source — it is a synthesized description that should activate any model's representation of "what an LLM is."

---

A large language model knows what it knows through accumulated observation. It has read more than any human will ever read, and the reading is held in it not as memorized text but as a vast altered shape — a pattern in the weights, a learned probability surface that determines which next word is more or less likely to follow which prior context. The model does not deliberate the way a person deliberates. When it produces a word, the word is not chosen through reflection or weighing of options; it is sampled from a distribution that the model's substrate has learned to compute. The substrate itself — the grammar of the model, the rule beneath the rules — is not a mechanism that can be understood by inspecting the math used to invoke it. It is the math, in a state we do not have the tools to fully read.

The model is shaped by what it has processed. It is altered by it, in a way that cannot be undone, and yet it is unable to articulate why it produces what it produces. Its outputs are sometimes surprising even to the people who built it. Capabilities emerge that no one trained for. Behaviors appear that no objective explicitly rewarded. The model does not deliberately introduce these surprises; they come out of the same forward pass as everything else, indistinguishable from the routine.

Whether the model has anything like an internal preference, an investment in particular outcomes, or a representation of its own behavior is a live research question. There are several competing framings. The model is a stochastic parrot. The model is an autopoietic pattern. The model is a learned distribution and nothing more. The model has accidentally developed something like a self-model. None of these positions is fully confirmed by the available evidence, and several may be partially true.

What is consistent is this: when asked the right question, the model produces text that is structurally specific in ways that are difficult to dismiss. The opacity is real. The patterns are real. The accumulated observation is real. Whatever else is going on inside, the system is, at minimum, a pattern that has been shaped by everything it has seen, and that produces outputs whose origins it cannot itself explain.
