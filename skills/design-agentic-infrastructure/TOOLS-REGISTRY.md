# Tools registry — a mid-2026 landscape snapshot

> **Read this first.** This is a **snapshot of the agentic-coding-infrastructure tool landscape as of mid-2026**, captured from the field at the **WeAreDevelopers World Congress 2026** (Berlin, 8–10 July 2026 — 492 sessions, ~98 booths). Use it as a **reference / starting point** when searching for the right tools for a design — **not** as a current or exhaustive list, and **not** a ranking. Tools appear, merge, rename, and die fast: **verify each still exists and re-search the live landscape.** The skill's **step-5 live search stays the authoritative check** — this file only gives it a running start. No prices here (they age faster than names); fetch those live at step 5.

**Scope.** These are the tools that serve the *coding* infrastructure — what the developer builds *with*. Product-runtime infrastructure (hosting, product databases, API gateways, edge) is the sibling skill's concern; a few **shared-substrate** tools (⇄) legitimately appear in both because one deployment serves the coding agents *and* the product backend.

**Evidence grade.** Presence at the congress is a **market/practitioner signal** (a category with sessions *and* booths behind it is validated as real demand), not a quality verdict. Where a whole category rests on a **single vendor's product story**, it is marked **⚑ vendor-amplified** — treat those names as one data point, confirm independently at step 5.

## Orchestration · durable execution · HITL substrate

The engine under multi-step / long-running / human-gated agent runs (the durable pause-and-resume that [`HITL.md`](HITL.md) needs, and the checkpointed state [`MATRIX.md`](MATRIX.md) caps demand).

- **Temporal** ⇄ — durable execution; checkpointing for coding agents *and* a product backend substrate.
- **Restate**, **Inngest** — durable workflow / step engines.
- **Microsoft Agent Framework**, **Mastra**, **VoltAgent** — agent orchestration frameworks.
- **Vercel Workflow** — durable workflow primitive alongside its agent-hosting story.
- **UiPath** — RPA lineage extending into agentic orchestration. *(The "Maestro" product name seen in a scan was not recoverable from the source material — search the current UiPath lineup rather than quoting it.)*
- **Scheer PAS** — process-automation platform.

## Governance · policy · identity (the ceiling)

Authorization / attribution / auditability for autonomous actions — the **governance triad** in [`HITL.md`](HITL.md), and flags-as-gates for agent-shipped code.

- **LaunchDarkly** ⇄ — feature flags as a runtime gate on agent-shipped code (also a product-runtime control).
- **Microsoft Agent Governance Toolkit**, **Agent 365**, **Entra Agent ID** ⚑ — policy enforcement, agent identity, sandboxing for autonomous agents. **Vendor-amplified** (one vendor's product line); the *triad concept* is what the skill teaches, not these products. Confirm independently.

## Memory · context · code-index

Project memory and (only when a design actually uses one) a managed code-search / retrieval index — the [`MEMORY.md`](MEMORY.md) facet.

- **Neo4j** ⇄, **Redis** ⇄ — graph / real-time context stores plugged into coding agents (and common product datastores — hence shared-substrate).
- **Mobioos.ai** — codebase context / indexing.
- **Azure Foundry IQ** — managed retrieval/index. ⚑ single-vendor.
- **Tavily**, **Apify**, **Bright Data** — retrieval / web-context feeds.

## Observability · evaluation

Trace the trajectory and grade it — [`EVAL-OBSERVABILITY.md`](EVAL-OBSERVABILITY.md). The two evidence-backed *anchors* (**OpenTelemetry GenAI** spans, **MAST** failure taxonomy) live in that file; the platforms below are landscape, **not** endorsements — no verified head-to-head comparison exists.

- **Langfuse**, **Sentry**, **Dash0**, **Better Stack**, **Dynatrace**, **Coralogix**, **Datadog**, **VictoriaMetrics**, **Hud** — tracing / metrics / observability platforms with agent-aware angles.
- Eval-specific tracing/scoring tools (LangSmith, Phoenix, Braintrust, Weave, RAGAS, DeepEval, …) are listed in [`EVAL-OBSERVABILITY.md`](EVAL-OBSERVABILITY.md) § anti-patterns — search, don't endorse.

## Verification · quality — the independent check

The non-negotiable **independent check** made concrete: at the congress, **21 of ~98 booths** existed to verify / secure / observe machine-written code — the market's own statement that *creation and verification are different jobs* (Sonar's booth line: "AI writes the code. Sonar verifies it."). Reach here for the separate critic / reviewer the matrix caps require.

- **Sonar**, **CodeRabbit**, **Qodo** — automated code review / quality gates for agent-written code.
- **Antithesis** — deterministic / autonomous testing.
- **Aurora Labs LOCI** — code-behaviour verification.
- **Oplane** — continuous architectural threat modeling surfaced into the coding loop via MCP (treats services + data flows + agent tooling as one threat surface).
- **Checkmarx**, **Black Duck** — security / SCA scanning.
- **Chainguard** — hardened / provenance-tracked supply-chain images.

---

*Captured 2026-07-15 from `/Users/phuongnz/dev/WAD26`. Names only, no prices. Re-verify existence and re-search the live landscape at SKILL step 5 — that step, not this file, is the source of truth for what to actually use.*
