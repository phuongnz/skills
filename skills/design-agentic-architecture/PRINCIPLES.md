# Principles — research-backed, as of mid-2026

The rules behind `design-agentic-architecture`, distilled from four adversarially fact-checked research runs (≈90 sources, 100 claims verified, 89 confirmed). Status flags: **[confirmed]** survived 3-vote verification; **[contested]** credible sources disagree; **[refuted]** did not survive — do not assert it.

> Re-verify before relying on anything time-sensitive. The field moves; this reflects mid-2026.

## The master tradeoff

Every design choice moves along one axis: **reliability / quality** vs. **cost / latency / non-determinism / complexity.** Every added pattern, agent, memory store, or gate must earn its place against it. **[confirmed]**

## The complexity ladder (climb on evidence)

Start at the bottom; climb only when the rung below provably fails. Each rung answers a different *need*, so jump to the rung the need points to — it is not a strict march. **[confirmed]**

| Rung | Pattern | Trigger | Cost |
|---|---|---|---|
| 1 | Single agent + tool use | Always start here | Baseline |
| 2 | Reflection (separate critic) | Correctness > speed | +calls, +latency |
| 3 | Bounded planning | Multi-step, structure knowable | Rigidity |
| 4 | ReAct (think→act→observe) | Static plans fail mid-task | Latency, error propagation |
| 5 | Multi-agent | Hard org boundaries or proven single-agent limits | 4–220× tokens, hard debugging |

- **Reflection needs a *separate* critic** — self-critique rubber-stamps its own errors. **[confirmed]**
- Before climbing past rung 1, exhaust single-agent optimization: prompting, retrieval, caching, bigger context, model upgrade. **[confirmed]**
- Go multi-agent only for **hard boundaries** — security/compliance separation, multiple owning teams, scale past 3–5 distinct functions. Not for parallelism alone. **[confirmed]**

## Multi-agent

- **Single-writer principle:** one coordinator owns the plan and all state changes; sub-agents contribute *intelligence and full traces*, not *actions*. **[confirmed]**
- **Clean-context reviewer:** a reviewer agent sharing no prior context with the author catches more bugs (reflection, scaled up). **[confirmed]**
- **Parallel vs. single-threaded is unsettled.** Parallel earns its keep for read-heavy, parallelizable work (research); single-threaded wins for write-heavy/coupled work (coding). **[contested]**
- "Parallel sub-agents are inherently unreliable." **[refuted]**
- "Fixed roles (Planner/Retriever/Validator…) improve reliability." **[refuted]** — a role is a prompt on the same model, not a new competence.

## Durable state (the through-line)

Durable, checkpointed state is the shared foundation: multi-agent coordination, persistent memory, and human-in-the-loop all require it, and observability is a *view into* it. Stand it up early (a framework checkpointer on Postgres, or Temporal-style durable execution). **[confirmed]**

## Memory

- Two layers: **working** (context window — perfect recall, low latency, linear token cost, bounded) and **long-term external** (scales, but retrieval error + a hop). Decide which slice of knowledge lives where. **[confirmed]**
- Content types: **episodic** (what happened), **semantic** (what's true, often a knowledge graph), **procedural** (how to do things). Useful labels — but no single tidy taxonomy is canonical. **[refuted]** (the "one neat taxonomy" claim)
- Start in-context; default RAG/vector; knowledge graph only for relationships/temporal. **[confirmed]**
- Long-context LLMs hallucinate on adversarial recall — bigger context is not a memory strategy. **[confirmed]**
- Mature memory needs a **write path** (store/update/forget), not just a retriever. Buy it (Mem0/Zep/Letta) to skip building it — but vendor benchmarks are contested marketing. **[confirmed]**
- Content type and storage flavour are **two separate axes** — do not force a 1:1 mapping.
- "Memory sharing by type (shared episodic / isolated semantic / agent-specific procedural)." **[refuted]**

## Human-in-the-loop

- One mechanism: **durable pause-and-resume** — pause at a checkpoint, persist state (indefinitely, no compute), human acts, the *same* run resumes. HITL is a state-management requirement, not a UI feature. **[confirmed]**
- Gate when **expected error cost > review-latency cost.** Score on irreversibility, blast radius, compliance, confidence. **[confirmed]**
- Never escalate on raw model confidence (LLMs overconfident) — combine trust + risk. **[confirmed]**
- Gates at **chain boundaries**, few, async/batched — or the human becomes the bottleneck. Oversight is a per-action dial (in / on / out of the loop). **[confirmed]**
- **Rubber-stamping is the dominant failure.** A human gate does not automatically add safety; a poorly designed one is accountability theater. Design for genuine engagement. **[confirmed]**

## Evaluation & observability

- **Evaluate process, not just output** — failures hide in the middle. Grade the trajectory (tool selection, tool-call parameters, retrieval groundedness, handoffs) at step level *and* end-to-end. **[confirmed]**
- **LLM-as-judge is a biased instrument** (position, length, concreteness, scoring-prompt biases). Calibrate against human labels first; position-swap; consider label-free debiasing. You reduce, not remove, bias. **[confirmed]**
- "Pairwise judging is inherently more reliable than scoring." **[refuted]**
- **MAST** attributes multi-agent failures — 14 modes in 3 categories (system design, inter-agent misalignment, task verification). **[confirmed]** (the "1600+ traces" provenance was **[refuted]**)
- Instrument on **OpenTelemetry GenAI** conventions (`invoke_agent → chat → execute_tool`) for portability — still experimental, keep content capture opt-in (PII). **[confirmed]**
- **Close the loop:** production traces become regression/golden eval datasets in CI. **[confirmed]**

## Tools & build-vs-buy

- **No verified head-to-head tool comparison exists** — only the *standard* (OpenTelemetry) and the *taxonomy* (MAST) are evidence-backed. Present tools as a landscape, choose on operational fit, test against the user's own stack. **[confirmed]**
- Framework choice matters less than the architecture decisions — the frameworks ship the same primitives. **[confirmed]**
- Truly all-in-one platforms are rare; most frameworks are orchestration-only and you stitch the rest. Build-vs-buy = assemble best-of-breed parts, or adopt one connected ecosystem and accept its choices.
- Always **search live** for current tools (step 7) — names and capabilities shift faster than this document.

## The unifying check: false-confidence traps

The deepest thread across all four areas — the thing that *looks* fine is where the danger hides:

- a rubber-stamped gate **looks like** oversight,
- a huge context window **looks like** memory,
- a correct final answer **looks like** success.

Audit every design against these three before shipping it.
