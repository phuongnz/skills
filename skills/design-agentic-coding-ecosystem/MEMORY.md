# Memory — how to design the memory layer of a coding ecosystem

*The design knowledge, so the skill never defaults to a shallow memory recommendation — it decides the memory layer from evidence here, and fetches only live memory **tools/prices** at SKILL step 5. Research-backed as of mid-2026; re-validate before relying on it — the field moves.*

Memory is a **step-4 architecture facet** (the "project memory" line of each design). Consult this the way step 6 consults `COST-MODEL.md`: it carries the *how*, so the design is reasoned from the tradeoff below — **not** hand-waved to "the agent keeps a `CLAUDE.md`." That default is the trap this file exists to prevent (see *The context tax* below); it is also the exact face of the faith-check trap **"a huge context window *looks like* memory."**

## The two layers, and the one tradeoff

Every piece of knowledge the agents hold sits in one of two layers. Deciding **which layer holds what** *is* the memory design.

| Layer | What it is | Cost shape | Fails by |
|---|---|---|---|
| **Working / short-term** | what's in the context window *right now* — the plan scratchpad, the reflection critique, the ReAct trail, any always-loaded file | **re-read every turn → linear token cost**; perfect recall, low latency; resets when the session ends | overstuffing → quality *drops* while cost climbs (context rot) |
| **Long-term** | persistent external store, reached by **retrieval** | **flat-rate**; effectively unlimited scale | retrieval misses, stale/wrong facts, added latency |

The whole discipline hangs on that contrast: in-context is a per-turn bill you pay on *every* turn whether the turn needs the content or not; external is flat but can fail to retrieve. There is **no universal winner** — the right layer is workload-specific, and it is a *decision*, not a default.

## Start in-context. Context is a budget, not a dumping ground

The floor is **in-context only** — no external memory subsystem until evidence demands one (a-priori, this is what the matrix's "start in-context" cell means). But the in-context layer is a **budget with a sweet spot** (the "smart zone"): past it, answer quality degrades *and* cost rises. Keep it in the zone with three moves — the field's "context engineering":

- **Curate** — put the right things in (tight instructions, only the relevant retrieved slice), keep junk out.
- **Compact** — trim or summarize old turns so the signal survives without the token pile.
- **Offload** — push durable facts to an external store, pull them on demand; the window holds the *working set*, not the whole history.

## The context tax — why an always-loaded file is not "free memory"

The single most common bad recommendation is *"give the agent a `CLAUDE.md` it updates"* as the long-term-memory answer. It is wrong on its own terms:

**An always-loaded file (a `CLAUDE.md`, a `NOTES` doc, a persistent system-prompt block) is part of the *working* layer, not the long-term one.** It is re-read on *every* turn at linear token cost — doing no work on the turns that don't need it, yet billed on all of them, and pushing the window toward rot as it grows. That is a **per-turn context tax masquerading as recall.**

So the design rule is **progressive disclosure**:

- Keep the always-loaded surface **as small as possible** — ideally a short *index/pointer* ("the auth rules live in `docs/auth.md`; the deploy runbook in …"), not the content itself.
- Push the detail to **load-on-demand** — a file the agent opens *when a task touches it*, or a retrieved slice — so context cost is paid only when the knowledge is actually used.
- A growing always-loaded notes file is the anti-pattern: it silently taxes every turn and drifts stale.

This holds **even under a flat subscription** where marginal tokens ≈ $0: the cost that bites there isn't dollars, it's **quality** — an overstuffed window still rots and still hallucinates on buried detail. Frugality stops gating; the smart zone doesn't.

## When external long-term memory earns its place

Climb to an external store only on **a-posteriori evidence**, never as an a-priori default:

- **The trigger:** re-establishing context across sessions, or the working set, *actually costs too much* — the window is under pressure or the token bill is climbing (the matrix's "add a memory write-path when token cost bites").
- **Order of operations:** window under pressure → **curate / compact / offload first**; only if that's not enough do you stand up an external memory subsystem. Don't add a rung the cheaper move would have fixed.
- **De-escalation runs too:** if a store is rarely retrieved from, it isn't earning its flat cost — remove it.

Cross-check the cost line in `COST-MODEL.md`: a project-memory *file* is ≈ free; a **managed vector / code-search index** adds a real line (monthly DB + one-time embedding pass over the codebase + per-query embed). Only price it when the design actually runs one.

## Two separate axes: content type vs. storage flavour

Do **not** collapse these into a 1:1 map — that mistake picks heavy storage for no reason.

- **Content type** (conceptual — the CoALA vocabulary): **episodic** = what happened (events, past interactions), **semantic** = what's true (facts), **procedural** = how to do things. (Also parametric = baked into weights; shared = across agents.)
- **Storage flavour** (implementation): **RAG / vector DB** — semantic similarity, the **cheap default**; **knowledge graph** — reach for it *only* when relationships or change-over-time genuinely matter, not because the content is "semantic"; **managed memory layer** (Mem0, Zep, LangMem, Letta — search live at step 5) — buy the whole external subsystem, including its write path, instead of building it.

Default to RAG/vector. Escalate storage flavour on the same evidence discipline as everything else.

## The 2026 shift: mature memory has a write path

Classic RAG is **read-only**. Memory that maintains itself actively decides what to **store, update, and forget** — the ADD / UPDATE / DELETE / NOOP pattern (Mem0's framing). It's the difference between a notebook you only read and one you keep correct: crossing out what's wrong, updating what changed. For a **maintained** product whose facts drift, a read-only store silently rots; that's when the write path is worth its complexity. For throwaway work, skip it.

## Anti-patterns (and the faith-check trap this arms)

- **Huge context window *as* memory.** On the LoCoMo long-conversation benchmark both RAG and long-context lifted Q&A quality (+22–66%), but long-context models **hallucinate on adversarial recall** — confidently inventing buried details. A bigger window is not a memory strategy. *(This is the faith-check trap "a huge context window looks like memory" — the design must not rely on window size for recall.)*
- **Always-loaded file as long-term memory** — the context tax above; it *looks like* persistent recall but is billed every turn and drifts stale.
- **Trusting vendor memory leaderboards.** Managed-memory marketing is contested (e.g. a widely-cited ">90% token reduction" claim did not hold up under scrutiny). Present tools as a landscape, verify prices/claims live at step 5, don't quote a leaderboard.

## What the design must state (the checkpoint)

For the memory facet of each of the three designs, name:

1. **Which layer holds what** — what stays in-context (the working set) vs. what, if anything, is externalized.
2. **The always-loaded surface, kept minimal** — a small pointer/index, with detail on load-on-demand (progressive disclosure), *not* a growing always-read file.
3. **The climb trigger to external memory** — the specific evidence (context cost biting) that would move this design up, and the curate/compact/offload steps tried first.
4. **Storage flavour + its cost line, only if used** — RAG/vector by default, graph or managed layer only on stated need; cross-referenced to the memory line in `COST-MODEL.md`.

**Floor default:** in-context first, minimal always-loaded pointer, no external store — and that is a *complete* memory design for most throwaway and low-context builds, not an omission.
