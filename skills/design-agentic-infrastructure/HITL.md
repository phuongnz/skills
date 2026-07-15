# Human-in-the-loop — how to design the gate

*The design knowledge, so the skill never hand-waves "add a human" — it places the gate from evidence here, and fetches only live **durable-execution / HITL tools** at SKILL step 5. Research-backed as of mid-2026; re-validate before relying on it — the field moves.*

HITL is a **step-4 architecture facet** (the "HITL gate" line of each design) and the mechanism behind two hard rules: the matrix cap **high blast radius ⇒ a human gate on the risky action**, and the non-negotiable that that gate is **designed against rubber-stamping**. Consult this the way step 6 consults `COST-MODEL.md`. The one thing to internalize: **"add a human" is the *start* of the design problem, not the conclusion** — a badly built gate is the face of the faith-check trap **"a rubber-stamped gate *looks like* oversight."**

## HITL is a state-management requirement, not a UI feature

The one verified mechanism is **durable pause-and-resume**: the agent reaches a decision point → **persists full state** (parked indefinitely, burning *no* compute) → a human reviews and acts → the **same run resumes** with the human's input injected. This is why HITL rides on the same **durable, checkpointed state** as everything else — without it you have only *synchronous blocking*, which doesn't survive a restart.

> **Placement caveat:** if the framework re-runs the paused step from its start on resume, the checkpoint must sit at a **safe point** or any side effects already fired will fire **twice**. Gate *before* the irreversible action, not after it has partially run.

## The four control points a human can execute

Pick the one the situation needs — they are not interchangeable.

| Control point | What the human does | Use when |
|---|---|---|
| **Approve / reject** | authorizes or blocks the proposed action | high-risk writes, payments, irreversible merges |
| **Edit-state** | rewrites the action (or the memory) before it proceeds | the action is *mostly* right, needs a fix |
| **Respond (human-as-tool)** | answers a question the agent asked | missing info, genuine ambiguity |
| **Review-and-feedback** | critiques the output and feeds it back | reflection-style quality loops |

## The oversight spectrum — set it per action, never globally

- **In-the-loop** — human approves *before* each gated action. Max control, max latency.
- **On-the-loop** — human supervises and *can* intervene; the agent acts by default.
- **Out-of-the-loop** — full autonomy. Routine, reversible, low-blast-radius actions.

A single design mixes all three: the refund/merge/deploy is in-the-loop, the lint fix is out-of-the-loop. Choosing globally is the mistake.

## The other end: govern the actions you *don't* gate (the ceiling)

Out-of-the-loop is not un-governed. When an agent acts autonomously — no human at each step — three questions must still be answerable *after the fact*, the **governance triad**:

- **Authorization** — *is this action allowed?* The agent has a scope of permitted actions enforced by policy, independent of what it decides to attempt.
- **Attribution** — *which agent did this?* Each agent carries its own **identity** — a first-class requirement here, distinct from (not a reuse of) the human's credential — so every action traces to an actor.
- **Auditability** — *can you prove what happened?* A durable record of what was attempted, by which agent, and whether it was allowed — riding the same durable state the gate already needs.

This is the ceiling's counterpart to the gate: the more autonomy you grant (higher rung, more actions running out-of-the-loop), the more the triad — *policy + identity + audit*, not a human at each step — is what keeps that autonomy accountable. State it concretely per design: the permission scope, the agent identity, and where the audit record lands. *(Resist over-speccing the mechanism — cryptographic delegation chains, kill-switches, Merkle audit trails and per-tool interception are vendor-specific product claims, not a required part of the design. Name the three questions your design answers and how, then search live governance tools at step 5.)*

## The gate rule — one line

**Gate when expected error-cost > review-latency cost.** Score each action on four risk dimensions, then sort:

- **Irreversibility** — can you undo it?
- **Blast radius** — how many downstream effects?
- **Compliance** — is it regulatory?
- **Confidence** — *combined with risk only* (see the trap below), never used raw.

Sort actions into three buckets: **rule-based** (auto, out-of-the-loop) → **exceptions** (route to a human) → **regulatory** (human, always).

### Gate placement

Place gates at **chain boundaries** — between major steps — **not sprinkled mid-reasoning**. Blocking on a human adds *unbounded* latency, so use **few, well-placed, async/batched** gates. Sprinkle them and the human becomes the bottleneck and starts rubber-stamping out of fatigue — the placement *causes* the failure mode below.

### The confidence trap

Do **not** escalate on the model's *confidence* alone — LLMs are **systematically overconfident**, so a confidence threshold gates the wrong things. Combine a **trust score + risk score**; raw model confidence is never the trigger.

## Rubber-stamping is the center of HITL, not a footnote

The mechanism works; the **human fails predictably**. Three failure modes:

- **Automation bias** (the dominant one) — people approve reflexively; the gate becomes theater.
- **Cognitive atrophy** — reviewers who rarely need to act lose the skill to catch the error when it finally comes.
- **Opacity → notional oversight** — with no insight into *how* the agent decided, review degrades to a signature.

The sharp consequence: **a poorly designed gate is *worse* than no gate.** You pay the review cost *and* believe you have oversight while having none — false confidence, accountability theater. So designing *against* rubber-stamping is an **architecture decision**, and a real gate requires:

- **Few gates** — so each one still commands attention.
- **Explainability** — the reviewer can see *what* they're approving and *why* the agent chose it.
- **Genuine engagement designed in** — not a signature line the reviewer clicks through.

## Durable execution is the prerequisite (search tools live)

The gate needs a substrate that survives a restart. Current options to search at step 5 (present as a landscape, don't quote from memory): **LangGraph** (`interrupt()` + a checkpointer), **OpenAI Agents SDK** (a `needsApproval` flag returning resumable, serializable state), or a **durable-execution platform** (e.g. Temporal) / a framework checkpointer on Postgres. Cross-check the cost: the gate's **real** cost is the **human-review-time** line in `COST-MODEL.md` (`reviews × minutes × loaded rate`) — often the dominant line for a high-blast-radius design, and the cost the cap *imposes*. Make it explicit; a gate is not free.

## What the design must state (the checkpoint)

For the HITL facet of each of the three designs, name:

1. **Which actions are gated, and at which oversight level** — in/on/out-of-the-loop, decided *per action* by the gate rule (error-cost vs. latency-cost), not globally.
2. **Where the gate sits** — at a safe chain boundary, *before* the irreversible action, on durable state so a paused run resumes cleanly.
3. **The anti-rubber-stamp design** — few gates, what the reviewer is shown (explainability), and how the trigger combines trust + risk (never raw confidence).
4. **The human-review cost line** — carried into the cost ladder, since a gate the design relies on but never budgets for is a fiction.

**Floor default:** **low blast radius ⇒ no gate** (out-of-the-loop, climb only on evidence). A gate that isn't earning its latency should be *removed* — the arrow runs down too. But **high blast radius ⇒ the gate is a cap**, present on the floor design, and it must be a *real* one, not a signature line.
