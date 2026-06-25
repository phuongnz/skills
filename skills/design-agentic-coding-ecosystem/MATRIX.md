# The Decision Matrix — constraints to a starting band

*Research-backed as of mid-2026. A markdown port of the bridge's decision matrix (the `agentic-coding` repo), which synthesizes two teaching repos — `teachme-agentic-architecture` (the engine / product plane) and `teachme-agentic-software-workflow` (the drive / build plane). Re-validate before relying on it; the field moves.*

## Read it as a band, not a point

A matrix that printed one fixed design would betray the one law both repos teach — **Evidence-Gated Escalation**: you don't *predict* the final architecture, you *climb on proof*. So for each constraint the matrix sets three things, not an answer:

- **a floor** — the lightest start the constraint *permits*. Begin here.
- **a ceiling / cap** — the hard limit it *imposes* (marked **cap ·**). Never below this, whatever else you do.
- **climb triggers** — the evidence (marked **→**) that authorises moving up *inside* the band.

The matrix narrows the band; human judgement still applies within it. A decision aid, not an oracle.

## Step 1 · Translate the brief

The user's constraints are in business language; the matrix decides in **native sizing inputs**. Translate first.

| The user brings… | Reads as (native sizing input) | Lands under |
|---|---|---|
| **Requirements** (clear? stable? checkable?) | **clarity** · **testability** | Requirements |
| **Budget** (how much; metered vs. subscription) | the cost arm + **pricing regime** | Budget |
| **Tech-stack constraints** (framework, latency, on-prem, separability) | **boundaries** + tool/framework fit | Tech stack |
| **Business constraints** (money, safety, compliance, SLA, longevity) | **blast radius** · **lifespan** | Business stakes |

## Step 2 · Match the matrix

Three columns = the three outputs: the **architecture** you ship (product plane), the **workflow** you drive (build plane), and the **tools**. Read the floor, obey the caps (**cap ·**), note the climb triggers (**→**).

### Requirements

| Your reading | Architecture (rung · product plane) | Workflow (build plane) | Tools |
|---|---|---|---|
| **Clarity: fuzzy / exploratory** | Rung 1; reflection early. **→ ReAct (rung 4) if a static plan won't hold.** Don't bounded-plan what you can't yet decompose. | Explore-first — vibe to probe, then Explore→Plan→Code→Commit. Skip heavy spec until the shape emerges. | Light; keep the window in the *smart zone* as you probe. |
| **Clarity: clear & stable** | Bounded planning (rung 3) becomes viable once structure is knowable. | Spec-Driven (Spec Kit / Kiro) — the spec is the source of truth. | Generated-from-spec scaffolding; living docs. |
| **Testability: machine-checkable** | The independent critic can be *automated*; higher autonomy is safe. | TDD-with-AI — a failing test closes the loop (best ROI). Agentic loop ("ralph") becomes possible. | Runnable checks / CI as the verifier. |
| **Testability: subjective ("feel")** | Human / LLM-as-judge eval, calibrated against labels — not a green bar. | Keep a human in Verify; don't hand subjective "done" to autonomy. | Trajectory eval + human review. |

### Business stakes

| Your reading | Architecture | Workflow | Tools |
|---|---|---|---|
| **Blast radius: high** (money · safety · irreversible) | **cap ·** HITL gate on the risky action; observability on. Start rung 1; add a critic early if it computes something. | **cap ·** spec-first; **Verify & Review never cut**. Lower autonomy — gate each phase. | Independent critic + clean-context reviewer; typed, schema-validated tool calls. |
| **Blast radius: low** | Rung 1; HITL optional; climb only on proof. | Vibe → EPCC; higher autonomy is fine. | Default light toolset. |
| **Lifespan: long / maintained** | **cap ·** evaluation & observability from day one. **→ add a memory write-path when token cost bites.** | Spec-driven; living docs; Review never cut. | Durable, checkpointed state; tracing (OpenTelemetry GenAI). |
| **Lifespan: throwaway** | Rung 1; skip memory / eval scaffolding. | Vibe coding; minimal ceremony. | Minimal; no durable state needed. |

### Budget

| Your reading | Architecture | Workflow | Tools |
|---|---|---|---|
| **Metered API** (every token a marginal $) | Optimise the rung you're on *before* climbing; context thrift first (curate, compact, offload). Extra rungs sting. | Justify each heavy step; smaller / fewer crews; the one-sentence-diff rule earns real money. | Prompt caching; cheap models for sub-steps; RAG instead of stuffing the window. |
| **Flat subscription** (marginal token ≈ $0) | An extra rung, fresh-context reviewer, or fuller window is nearly free to *try* — but reliability must still earn it. **Frugality stops gating; evidence doesn't.** | Fresh-context reviewers and multi-agent crews are easy to justify here. | Fuller windows; more parallel agents — cost is no longer the gate. |

### Tech stack

| Your reading | Architecture | Workflow | Tools |
|---|---|---|---|
| **Boundaries: answering separable from acting** | A *hypothesis* for rung 5 — **don't pre-split**. **→ Multi-agent only on a proven hard boundary or single-agent limit** (single-writer if you do). | — (unchanged) | Single-writer coordinator *if* you ever split. |
| **Framework / latency / on-prem constraint** | Shapes the durable-state engine; a latency SLA **caps** how many rungs you can climb. | — (unchanged) | Framework often dictated — but they ship the *same primitives*, so pick by ecosystem fit, not hype. |

**Tie-break:** when two readings pull different ways, the **most restrictive cap wins** — the tightest ceiling across all constraints is the one you obey. (High blast radius beats a tight budget: keep the HITL gate and pay for it.)

## The non-negotiables (the ceiling, always)

These caps hold no matter where the constraints land. If a cheap, fast design violates one, it isn't the cheap option — it's the broken one. **Every design in the band, floor included, must honour all of these.**

- **The independent check is never skipped.** A model that grades its own work rubber-stamps it — the critic, reviewer, or judge must be *separate*.
- **Verify & Review are never cut** — no matter how small the diff. (The plan you *may* skip; these you may not.)
- **High blast radius ⇒ a human gate** on the risky action, designed against rubber-stamping.
- **A maintained product ⇒ evaluation & observability from day one** — or you can't see *why* a run broke.
- **If you split into multiple agents, exactly one writer** owns the plan and all state changes.

## The climb triggers (inside the band)

What moves a design up is **evidence**, and it has a fixed vocabulary. Evidence comes from Verify, Review, and production traces — the lifecycle loop. Arrows run **both ways**: the same discipline *de-escalates* when a mechanism stops earning its cost.

| Evidence you observe | Plane | The move it authorises |
|---|---|---|
| Output is wrong in a *checkable* way | product | + rung 2 — a separate critic |
| A static plan keeps breaking mid-task | product | + rung 4 — ReAct (think→act→observe) |
| A proven hard boundary, or single-agent ceiling | product | + rung 5 — multi-agent (single-writer) |
| Window fills; answers drift mid-run | both | curate / compact / offload *first* — only then a rung |
| The critic never fires across many runs | product | − **descend**: remove the rung |
| Token bill outgrows the value it buys | both | optimise / descend before climbing |
| New edge cases churn the requirements | build | heavier spec on the next loop |

## How this drives the three-design band

- **Floor** = read the floor cell of every constraint, then satisfy every binding cap. The lightest design the constraints *permit*.
- **Middle** = apply the first one or two climb triggers most likely to fire given the requirements (e.g. a checkable correctness gap → rung 2; clarity firming up → heavier spec).
- **Ceiling** = the heaviest rung/workflow any constraint's climb trigger could ever authorise, *with that trigger stated as its entry condition* — an upper bound, not a build-now recommendation.

The recommendation always **starts at the floor**. The ceiling's job is to price "more" so the cost ladder exposes need vs. nice-to-have.
