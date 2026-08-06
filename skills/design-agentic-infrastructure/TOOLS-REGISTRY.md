# Tools registry — a mid-2026 landscape snapshot

> **Read this first.** This is a **snapshot of the agentic-coding-infrastructure tool landscape as of mid-2026**, captured from the field at the **WeAreDevelopers World Congress 2026** (Berlin, 8–10 July 2026 — 492 sessions, ~98 booths). Use it as a **reference / starting point** when searching for the right tools for a design — **not** as a current or exhaustive list, and **not** a ranking. Tools appear, merge, rename, and die fast: **verify each still exists and re-search the live landscape.** The skill's **step-5 live search stays the authoritative check** — this file only gives it a running start. No prices here (they age faster than names); fetch those live at step 5. Each entry does carry its **slow-aging fields** — *[license · hosting model]*, hosting ∈ SaaS · self-host · hybrid (both) · library — verified 2026-08-06, because they are decisive early filters: free + self-hostable candidates survive floor-stage economics that per-seat SaaS pricing does not. Slow-aging is not non-aging — licenses do change (Redis did); re-verify at step 5.

**Scope.** These are the tools that serve the *coding* infrastructure — what the developer builds *with*. Product-runtime infrastructure (hosting, product databases, API gateways, edge) is the sibling skill's concern; a few **shared-substrate** tools (⇄) legitimately appear in both because one deployment serves the coding agents *and* the product backend.

**Evidence grade.** Presence at the congress is a **market/practitioner signal** (a category with sessions *and* booths behind it is validated as real demand), not a quality verdict. Where a whole category rests on a **single vendor's product story**, it is marked **⚑ vendor-amplified** — treat those names as one data point, confirm independently at step 5.

## Orchestration · durable execution · HITL substrate

The engine under multi-step / long-running / human-gated agent runs (the durable pause-and-resume that [`HITL.md`](HITL.md) needs, and the checkpointed state [`MATRIX.md`](MATRIX.md) caps demand).

- **Temporal** ⇄ *[MIT · hybrid]* — durable execution; checkpointing for coding agents *and* a product backend substrate.
- **Restate** *[BUSL-1.1 · hybrid]*, **Inngest** *[SSPL-1.0 (→ Apache-2.0 after 3 y) · hybrid]* — durable workflow / step engines.
- **Microsoft Agent Framework** *[MIT · library]*, **Mastra** *[Apache-2.0 · library]*, **VoltAgent** *[MIT · library]* — agent orchestration frameworks.
- **Vercel Workflow** *[Apache-2.0 · library — runs anywhere, not only Vercel]* — durable workflow primitive alongside its agent-hosting story.
- **UiPath** *[proprietary · hybrid]* — RPA lineage extending into agentic orchestration. *(The "Maestro" product name seen in a scan was not recoverable from the source material — search the current UiPath lineup rather than quoting it.)*
- **Scheer PAS** *[proprietary · hybrid]* — process-automation platform.

## Governance · policy · identity (the ceiling)

Authorization / attribution / auditability for autonomous actions — the **governance triad** in [`HITL.md`](HITL.md), and flags-as-gates for agent-shipped code.

- **LaunchDarkly** ⇄ *[proprietary · SaaS]* — feature flags as a runtime gate on agent-shipped code (also a product-runtime control).
- **Microsoft Agent Governance Toolkit**, **Agent 365**, **Entra Agent ID** ⚑ *[proprietary · SaaS — the M365/Entra line, not standalone products]* — policy enforcement, agent identity, sandboxing for autonomous agents. **Vendor-amplified** (one vendor's product line); the *triad concept* is what the skill teaches, not these products. Confirm independently.

## Memory · context · code-index

Project memory and (only when a design actually uses one) a managed code-search / retrieval index — the [`MEMORY.md`](MEMORY.md) facet.

- **Neo4j** ⇄ *[open-core (GPL-3.0 CE) · hybrid]*, **Redis** ⇄ *[AGPL-3.0 (Redis 8+, tri-licensed) · hybrid]* — graph / real-time context stores plugged into coding agents (and common product datastores — hence shared-substrate).
- **Mobioos.ai** *[proprietary · SaaS — code indexed locally]* — codebase context / indexing.
- **Azure Foundry IQ** *[proprietary · SaaS]* — managed retrieval/index. ⚑ single-vendor.
- **Tavily** *[proprietary · SaaS — SDKs are MIT]*, **Apify** *[proprietary · SaaS — Crawlee crawler is Apache-2.0]*, **Bright Data** *[proprietary · SaaS]* — retrieval / web-context feeds.

## Observability · evaluation

Trace the trajectory and grade it — [`EVAL-OBSERVABILITY.md`](EVAL-OBSERVABILITY.md). The two evidence-backed *anchors* (**OpenTelemetry GenAI** spans, **MAST** failure taxonomy) live in that file; the platforms below are landscape, **not** endorsements — no verified head-to-head comparison exists.

Tracing / metrics / observability platforms with agent-aware angles:

| Platform | License · hosting |
|---|---|
| **Langfuse** | open-core (MIT core) · hybrid |
| **Sentry** | FSL-1.1 *(→ Apache-2.0 after 2 y)* · hybrid |
| **Dash0** | proprietary · SaaS |
| **Better Stack** | proprietary · SaaS |
| **Dynatrace** | proprietary · hybrid *(managed on-prem supported)* |
| **Coralogix** | proprietary · SaaS *(BYOC: data in your S3)* |
| **Datadog** | proprietary · SaaS *(agent is Apache-2.0)* |
| **VictoriaMetrics** | open-core (Apache-2.0 core) · hybrid |
| **Hud** | proprietary · SaaS |

- Eval-specific tracing/scoring tools (LangSmith, Phoenix, Braintrust, Weave, RAGAS, DeepEval, …) are listed in [`EVAL-OBSERVABILITY.md`](EVAL-OBSERVABILITY.md) § anti-patterns — search, don't endorse.

## Verification · quality — the independent check

The non-negotiable **independent check** made concrete: at the congress, **21 of ~98 booths** existed to verify / secure / observe machine-written code — the market's own statement that *creation and verification are different jobs* (Sonar's booth line: "AI writes the code. Sonar verifies it."). Reach here for the separate critic / reviewer the matrix caps require.

- **Sonar** *[open-core (LGPL-3.0 Community Build) · hybrid]*, **CodeRabbit** *[proprietary · hybrid — self-host is enterprise-only]*, **Qodo** *[open-core (Apache-2.0 PR-Agent) · hybrid]* — automated code review / quality gates for agent-written code.
- **Antithesis** *[proprietary · hybrid — self-host runs in your AWS VPC]* — deterministic / autonomous testing.
- **Aurora Labs LOCI** *[proprietary · hybrid]* — code-behaviour verification.
- **Oplane** *[proprietary · SaaS]* — continuous architectural threat modeling surfaced into the coding loop via MCP (treats services + data flows + agent tooling as one threat surface).
- **Checkmarx** *[proprietary · hybrid]*, **Black Duck** *[proprietary · hybrid]* — security / SCA scanning.
- **Chainguard** *[proprietary · SaaS — registry-delivered, built on Apache-2.0 Wolfi]* — hardened / provenance-tracked supply-chain images.

---

*Captured 2026-07-15 from `/Users/phuongnz/dev/INFO-WAD26`; slow-aging fields (license · hosting) verified 2026-08-06 by live search. No prices. Re-verify existence and re-search the live landscape at SKILL step 5 — that step, not this file, is the source of truth for what to actually use.*
