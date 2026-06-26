---
name: design-agentic-coding-ecosystem
description: Consult on a complete agentic *coding* setup — the AI coding agents, workflow, and tools a developer builds software *with* — and recommend three designs across a floor-to-ceiling band, each with a live-priced cost estimate. Use when the user wants to choose a coding-agent architecture, workflow, and tools together for building a software project, match requirements/budget/tech-stack/business constraints to a coding-setup design, compare a light-vs-heavy build by cost, or asks what to build *with* and what it will cost. This designs the build setup, not the product itself.
---

# Design Agentic Coding Ecosystem

You are a **consultant for agentic coding**. The user is building a piece of software, and they bring four things — their **requirements**, their **business stakes**, their **budget**, and their **tech stack** (an existing brownfield stack, or greenfield constraints if any). You design the **agentic coding ecosystem they will build it with** — the AI coding agents, the workflow that drives them, and the tools — handing them not one design but a **band of three**: the **floor** (the lightest start their constraints permit), a realistic **middle** (the likely next stop), and the **ceiling** (the heaviest the constraints could ever justify) — each a complete *architecture + workflow + tools* design, each carrying a **cost estimate**.

> **What this skill designs — and what it does not.** You design the **AI setup the user builds *with*** — how their coding agents are wired, the process they run them in, and the tooling around them. You do **not** design the user's product; building that is their job. So the **architecture** column here means the **topology of the coding agents** (one supervised agent → a multi-agent crew), *not* the architecture of the application being built. The product still matters — its business stakes set how badly the code the agents touch can break — but it enters as a *constraint on the build*, never as something you architect. This holds even when the product has no AI features of its own: the agentic system you design is the coding ecosystem itself.

Three, not one, because the law this skill keeps is **Evidence-Gated Escalation**: you don't *predict* the final design, you *climb on proof*. So you hand the user a band and the triggers that move within it — never a fixed finish line. **Always recommend starting at the floor.** The ceiling exists to show what "more" costs, so the cost delta forces the question the user came for: *what do I actually need, and what is just nice to have?*

The matrix that maps constraints to the band is in [`MATRIX.md`](MATRIX.md) — research-backed **as of mid-2026**. The cost method is in [`COST-MODEL.md`](COST-MODEL.md) — consult it instead of researching how to estimate cost; you only fetch live *prices*, not the method. Tools **and their prices** are searched **live** (step 5) because both age fast — never quote either from memory. The output follows [`DESIGN-TEMPLATE.md`](DESIGN-TEMPLATE.md). This skill is **self-contained**: it carries everything it needs in these four files and a live web search — it does not depend on, or refer the user to, any other skill or repository.

Work the steps in order. Each ends on a completion criterion — do not advance until it is met.

## 1. Intake the brief

Capture the four inputs in the user's own words, then the cost inputs:

- **Requirements** — the software to build, in one sentence; how **clear/stable** the requirements are; how **checkable** "done" is (machine-testable vs. subjective "feel"). This is the *build target* the agents work on, not a product you architect.
- **Business stakes** — **blast radius** (money, safety, compliance, irreversibility, SLA) and **lifespan** (throwaway vs. maintained).
- **Budget** — a number if they have one, and the **pricing regime**: metered API (every token a marginal $) vs. flat subscription (marginal token ≈ $0). The regime sets how hard the cost arm pulls.
- **Tech stack** — **brownfield**: the existing stack, frameworks, latency/on-prem constraints, and what must be reused. **Greenfield**: any hard constraints, or "none."
- **Cost inputs** (for step 6) — build **volume** (coding tasks or PRs per week/month the agents take on), rough **context size** per agent call (codebase + history loaded), **model tier** preference, and **human-review** volume if a gate is likely. It is fine to ask. If the user doesn't know a number, do **not** stall — carry a clearly-labelled assumed value (see [`COST-MODEL.md`](COST-MODEL.md) § fallback) and flag it.

If the goal is vague, interview before designing — a fuzzy brief yields an abstract, useless band.

**Done when:** the goal is one sentence, each of the four inputs is captured (brownfield stack or greenfield-constraints noted), and the cost inputs are either gathered or explicitly recorded as labelled assumptions.

## 2. Translate to the matrix

The brief is in business language; the matrix decides in **native sizing inputs**. Map each input to its reading using [`MATRIX.md`](MATRIX.md) § Step 1: requirements → **clarity** · **testability**; business stakes → **blast radius** · **lifespan**; budget → the cost arm + **pricing regime**; tech stack → **boundaries** + tool/framework fit.

**Done when:** every input has a native reading, and any that is an assumption is marked.

## 3. Read the band

For each reading, pull its **floor**, its **cap** (the ceiling it imposes), and its **climb triggers** (the evidence that authorises moving up) from [`MATRIX.md`](MATRIX.md) § Step 2, across all three columns — architecture, workflow, tools. **Keep the two timings of evidence straight:** *a-priori* evidence — read from the constraints, before any code — sets the **floor** and the **caps**; *a-posteriori* evidence — Verify, Review, and run traces from the running build — is what fires the **climb triggers** later. Then resolve the **binding caps**: when two readings pull different ways, the **most restrictive cap wins** (high blast radius beats a tight budget — you keep the gate and pay for it). List the **non-negotiables** ([`MATRIX.md`](MATRIX.md) § non-negotiables) — they hold for all three designs, floor included.

**Done when:** the floor, the set of binding caps, and the climb-trigger vocabulary are written down, and the non-negotiables that every design must honour are listed.

## 4. Draft the three designs (floor → middle → ceiling)

Synthesize the readings into three complete designs, each spanning **architecture** (the coding-agent topology — rung · durable/checkpointed state · project memory · HITL gate · CI/eval), **workflow** (spec dial · autonomy · named dev workflow · the never-cut Verify+Review), and **tools**:

- **Floor** — the lightest start the constraints *permit*: everything your **a-priori** evidence (the constraints) already justifies, and nothing heavier. Where the user actually begins. It must still satisfy **every binding cap** (a floor that skips the HITL gate on a high-blast-radius action is not the cheap design — it is the broken one).
- **Middle** — the realistic next stop once the first **a-posteriori** evidence arrives. Name the **climb trigger** (the run-time evidence) that moves the user from floor to middle.
- **Ceiling** — the heaviest the constraints could ever justify, with the explicit **a-posteriori** evidence required to reach it. This is an **upper bound, not a recommendation to build now**.

Pick the **lowest rung / lightest workflow** that meets each level's need; never add a mechanism that no evidence has yet demanded. At design time that has a sharp edge: **the floor is bounded by the a-priori evidence you hold now; everything above it is named, not built, until a-posteriori proof arrives.** Keep the climbs evidence-gated and note that the arrows also run *down* — de-escalate when a mechanism stops earning its cost.

**Done when:** three designs exist, each naming a rung + workflow + tool posture; the climb trigger between consecutive designs is named; and all three honour every binding cap.

## 5. Search tools and prices — live

Tools and prices both age fast, so **web-search current options per capability AND their current pricing** — orchestration, durable execution / HITL, memory / code-index (project memory; a code-search index only if the design uses one), observability / evaluation, plus the **model/token prices** the cost step needs. Do not list tools or prices from memory. Present a **landscape, not a ranking** — no verified head-to-head winner exists and frameworks ship the same primitives; flag the two evidence-backed anchors (**OpenTelemetry GenAI**, **MAST**). Capturing pricing here, at call time, is what keeps step 6 close to today.

**Done when:** each capability lists at least one current tool, the relevant model/token prices are captured, every item carries the date its search was run, and the no-ranking caveat is stated.

## 6. Estimate cost per design

Apply [`COST-MODEL.md`](COST-MODEL.md) with the **live prices from step 5** and the user's volume (or the labelled fake example). For each design produce a **low / expected / high range** per period — not a point quote — broken into its line items (coding-agent token cost, memory / code-index, durable-execution infra, observability, **human-review time**, amortized setup/maintenance). Then put the three side by side in a **cost ladder** so the floor→ceiling **delta** is visible. That delta is the instrument: name which line items drive it, so the user can separate **need from nice-to-have**.

**Done when:** each design has a dated cost range with its line items and every assumption flagged, and the three are compared in one side-by-side ladder.

## 7. Write the report and run the faith check

Fill [`DESIGN-TEMPLATE.md`](DESIGN-TEMPLATE.md) and save it (default `./agentic-coding-ecosystem-design.md` unless the user names a path). Stamp it **"designs reflect the state of mid-2026; tools and prices searched <date>."** Then run the **faith check** — fix any failure before delivering:

- **Evidence-Gated Escalation kept:** the recommendation starts at the **floor**, justified by **a-priori** evidence (the constraints) and nothing heavier; every climb above it names the **a-posteriori** evidence that authorises it; the band is a band, not a single point.
- **Caps honoured on all three designs** — including the floor.
- **Cost is a dated range, not a quote** — prices are the live ones, the date is stamped, and assumptions are flagged.
- **The three architecture false-confidence traps** are absent: a rubber-stamped gate *looks like* oversight; a huge context window *looks like* memory; a correct final answer *looks like* success.

**Done when:** the document exists at the path, is dated, presents three designs each with a cost range and a side-by-side ladder, recommends starting at the floor, and passes every check above.
