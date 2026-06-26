# The Decision Matrix — constraints to a starting band

*Research-backed as of mid-2026. A self-contained decision matrix that maps a software build's constraints to a starting band for its **agentic coding ecosystem** — the coding agents, the workflow, and the tools the developer builds *with*. Re-validate before relying on it; the field moves.*

## Read it as a band, not a point

A matrix that printed one fixed design would betray the one law every design here keeps — **Evidence-Gated Escalation**: you don't *predict* the final design, you *climb on proof*. So for each constraint the matrix sets three things, not an answer:

- **a floor** — the lightest start the constraint *permits*. Begin here.
- **a ceiling / cap** — the hard limit it *imposes* (marked **cap ·**). Never below this, whatever else you do.
- **climb triggers** — the evidence (marked **→**) that authorises moving up *inside* the band.

Evidence comes in **two timings**, and the band is built from both. **A-priori** evidence is read straight from the constraints, *before a line of code* — it sets the **floor** and the **caps** (Step 2 below). **A-posteriori** evidence is produced by the running build — Verify, Review, run traces — and it is what fires the **climb triggers** that move you up *or* down later. Same currency; they differ only in *when* the justification arrives. The cheap structural rungs can be justified a-priori; the risky ones (ReAct, multi-agent) almost always need a-posteriori proof — which is why you *don't pre-split*.

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

Three columns = the three design surfaces of the coding ecosystem: the **architecture** of the coding agents (the rung topology you run them on — from one supervised agent to a multi-agent crew), the **workflow** you drive them with, and the **tools**. None of these is the architecture of the product being built — that is the user's to build, not yours to design. Read the floor, obey the caps (**cap ·**), note the climb triggers (**→**).

### Requirements

| Your reading | Architecture (coding-agent rung) | Workflow (dev process) | Tools |
|---|---|---|---|
| **Clarity: fuzzy / exploratory** | Rung 1; reflection early. **→ ReAct (rung 4) if a static plan won't hold.** Don't bounded-plan what you can't yet decompose. | Explore-first — vibe to probe, then Explore→Plan→Code→Commit. Skip heavy spec until the shape emerges. | Light; keep the window in the *smart zone* as you probe. |
| **Clarity: clear & stable** | Bounded planning (rung 3) becomes viable once structure is knowable. | Spec-Driven (Spec Kit / Kiro) — the spec is the source of truth. | Generated-from-spec scaffolding; living docs. |
| **Testability: machine-checkable** | The independent critic can be *automated*; higher autonomy is safe. | TDD-with-AI — a failing test closes the loop (best ROI). Agentic loop ("ralph") becomes possible. | Runnable checks / CI as the verifier. |
| **Testability: subjective ("feel")** | Human / LLM-as-judge eval, calibrated against labels — not a green bar. | Keep a human in Verify; don't hand subjective "done" to autonomy. | Trajectory eval + human review. |

### Business stakes

| Your reading | Architecture | Workflow | Tools |
|---|---|---|---|
| **Blast radius: high** (money · safety · irreversible) | **cap ·** HITL gate on the risky change — the agent never merges money / auth / irreversible code unreviewed; observability on. Start rung 1; add a critic agent early if correctness is machine-checkable. | **cap ·** spec-first; **Verify & Review never cut**. Lower autonomy — gate each phase. | Independent critic + clean-context reviewer; typed, schema-validated tool calls. |
| **Blast radius: low** | Rung 1; HITL optional; climb only on proof. | Vibe → EPCC; higher autonomy is fine. | Default light toolset. |
| **Lifespan: long / maintained** | **cap ·** CI evaluation & run-trace observability from day one. **→ add a persistent project-memory file (e.g. a `CLAUDE.md`/notes doc the agent updates) when re-establishing context starts to cost too much.** | Spec-driven; living docs; Review never cut. | Durable, checkpointed state; tracing (OpenTelemetry GenAI). |
| **Lifespan: throwaway** | Rung 1; skip memory / eval scaffolding. | Vibe coding; minimal ceremony. | Minimal; no durable state needed. |

### Budget

| Your reading | Architecture | Workflow | Tools |
|---|---|---|---|
| **Metered API** (every token a marginal $) | Optimise the rung you're on *before* climbing; context thrift first (curate, compact, offload). Extra rungs sting. | Justify each heavy step; smaller / fewer crews; the one-sentence-diff rule earns real money. | Prompt caching; cheap models for sub-steps; retrieval / code-search instead of stuffing the whole codebase into the window. |
| **Flat subscription** (marginal token ≈ $0) | An extra rung, fresh-context reviewer, or fuller window is nearly free to *try* — but reliability must still earn it. **Frugality stops gating; evidence doesn't.** | Fresh-context reviewers and multi-agent crews are easy to justify here. | Fuller windows; more parallel agents — cost is no longer the gate. |

### Tech stack

| Your reading | Architecture | Workflow | Tools |
|---|---|---|---|
| **Boundaries: the build splits into separable sub-tasks** | A *hypothesis* for rung 5 — **don't pre-split**. **→ Multi-agent only on a proven hard boundary or single-agent limit** (single-writer if you do). | — (unchanged) | Single-writer coordinator *if* you ever split. |
| **Framework / latency / on-prem constraint** | Shapes the durable-state engine; a latency SLA **caps** how many rungs you can climb. | — (unchanged) | Framework often dictated — but they ship the *same primitives*, so pick by ecosystem fit, not hype. |

**Tie-break:** when two readings pull different ways, the **most restrictive cap wins** — the tightest ceiling across all constraints is the one you obey. (High blast radius beats a tight budget: keep the HITL gate and pay for it.)

## The non-negotiables (the ceiling, always)

These caps hold no matter where the constraints land. If a cheap, fast design violates one, it isn't the cheap option — it's the broken one. **Every design in the band, floor included, must honour all of these.**

- **The independent check is never skipped.** A model that grades its own work rubber-stamps it — the critic, reviewer, or judge must be *separate*.
- **Verify & Review are never cut** — no matter how small the diff. (The plan you *may* skip; these you may not.)
- **High blast radius ⇒ a human gate** on the risky action, designed against rubber-stamping.
- **A maintained product ⇒ evaluation & observability from day one** — or you can't see *why* a run broke.
- **If you split into multiple agents, exactly one writer** owns the plan and all state changes.

## The climb triggers (inside the band) — a-posteriori evidence

Step 2 set the floor and caps from **a-priori** evidence. What moves a design up or down *after* you build is **a-posteriori** evidence — produced by the running build (Verify, Review, the agents' own run traces) — and it has a fixed vocabulary. Arrows run **both ways**: the same discipline *de-escalates* when a mechanism stops earning its cost.

| Evidence you observe | Surface | The move it authorises |
|---|---|---|
| Agent output is wrong in a *checkable* way | architecture | + rung 2 — a separate reviewer/critic agent |
| A static plan keeps breaking mid-task | architecture | + rung 4 — ReAct (think→act→observe) |
| A proven hard boundary, or single-agent ceiling | architecture | + rung 5 — multi-agent crew (single-writer) |
| Context window fills; output drifts mid-run | both | curate / compact / offload *first* — only then a rung |
| The critic never fires across many runs | architecture | − **descend**: remove the rung |
| Token bill outgrows the value it buys | both | optimise / descend before climbing |
| New edge cases churn the requirements | workflow | heavier spec on the next loop |

## How this drives the three-design band

- **Floor** = read the floor cell of every constraint, then satisfy every binding cap. The lightest design the constraints *permit*.
- **Middle** = apply the first one or two climb triggers most likely to fire given the requirements (e.g. a checkable correctness gap → rung 2; clarity firming up → heavier spec).
- **Ceiling** = the heaviest rung/workflow any constraint's climb trigger could ever authorise, *with that trigger stated as its entry condition* — an upper bound, not a build-now recommendation.

The recommendation always **starts at the floor**. The ceiling's job is to price "more" so the cost ladder exposes need vs. nice-to-have.
