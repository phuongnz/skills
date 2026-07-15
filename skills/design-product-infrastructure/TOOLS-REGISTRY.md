# Tools registry — a mid-2026 landscape snapshot

> **Read this first.** This is a **snapshot of the product-runtime-infrastructure tool landscape as of mid-2026**, captured from the field at the **WeAreDevelopers World Congress 2026** (Berlin, 8–10 July 2026 — 492 sessions, ~98 booths). Use it as a **reference / starting point** when searching for the right tools for a design — **not** as a current or exhaustive list, and **not** a ranking. Tools appear, merge, rename, and die fast: **verify each still exists and re-search the live landscape.** The skill's **step-5 live search stays the authoritative check** — this file only gives it a running start. No prices here (they age faster than names); fetch those live at step 5.

**Scope.** These are the tools that serve the *product runtime* — what the software runs *on* in production. Coding-plane infrastructure (the agents, the dev workflow, the build-time tooling) is the sibling skill `design-agentic-infrastructure`'s concern; a few **shared-substrate** tools (⇄) legitimately appear in both because one deployment serves the product backend *and* the coding agents (see [`AGENT-READY.md`](AGENT-READY.md)).

**Evidence grade.** Presence at the congress is a **market/practitioner signal** (a category with sessions *and* booths behind it is validated as real demand), not a quality verdict. Where a whole category rests on a **single vendor's product story**, it is marked **⚑ vendor-amplified** — treat those names as one data point, confirm independently at step 5.

## Compute · hosting · platform

The runtime tier the product runs on — from serverless to managed Kubernetes to the edge ([`MATRIX.md`](MATRIX.md) runtime column).

- **Vercel** — serverless/edge hosting with agents as a first-class workload (Fluid Compute, Sandbox, Workflow).
- **Akamai** — "cloud built for AI": managed Kubernetes + model-serving (vLLM / KServe lineage) at the edge.
- **AWS Amplify Gen2** — full-stack managed hosting. *(AWS Kiro seen alongside it is a **coding-plane** tool — the sibling skill's concern, not product runtime.)*
- **Azure Foundry** — managed application/AI platform. ⚑ single-vendor.
- **Upsun** — PaaS with branch-to-production environment cloning (preview/staged exposure).
- **Kubermatic**, **OpenShift** — Kubernetes platform management for self-run estates.
- **Edge Impulse** — edge / embedded / on-device runtime.

## Data tier · datastores · cache

Pick the store from the data's *shape*, not habit ([`DATA-LAYER.md`](DATA-LAYER.md)).

- **TiDB** — distributed, scale-out relational (HTAP).
- **Percona** — managed/hardened MySQL & Postgres operations.
- **RavenDB** — document store.
- **Neo4j** ⇄ — graph store (product data *and* agent memory/context — shared-substrate).
- **Redis** ⇄, **Aerospike** — in-memory / low-latency key-value; cache, session, real-time context (Redis serves agents too — shared-substrate).
- **ClickHouse**, **MotherDuck** — columnar / analytical / timeseries.
- **OpenSearch** — full-text / faceted search index.

## Edge · API gateway · connectivity

The surface between the product and its consumers — including agent consumers ([`AGENT-READY.md`](AGENT-READY.md)).

- **Kong** ⇄ — API gateway; MCP-gateway lineage that turns product APIs into agent-callable tools (the agent-ready contract). Shared-substrate where agents consume the runtime.
- **Cloudinary** — media pipeline / CDN.
- **Twilio** — communications APIs (messaging/voice).
- **Tailscale** — scoped network connectivity (a control point for non-human/agent access).

## Durable execution · workflow · release

The long-running backbone and the delivery gate ([`RELEASE-GATES.md`](RELEASE-GATES.md)).

- **Temporal** ⇄ — durable execution; long-running product workflows *and* the checkpoint layer coding agents pause on (shared-substrate).
- **LaunchDarkly** ⇄ — feature flags as the runtime release gate — and the gate on agent-shipped code (shared-substrate).
- **Harness** — CD / release pipelines.
- **Bitrise** — mobile CI/CD.

## Observability · SLO · cost

Measure the user path and the SLO, not the health check ([`OBSERVABILITY-SLO.md`](OBSERVABILITY-SLO.md)). The evidence-backed portability anchor (**OpenTelemetry**) lives in that file; the platforms below are landscape, **not** endorsements — no verified head-to-head comparison exists.

- **Datadog**, **Dynatrace**, **Coralogix**, **Sentry**, **VictoriaMetrics**, **Better Stack**, **Dash0** ⇄ — tracing / metrics / SLO platforms (several also carry agent-aware angles — shared-substrate where the coding plane reuses them).
- **CloudHiro** — cloud cost / FinOps visibility (the egress/right-sizing lines in [`COST-MODEL.md`](COST-MODEL.md)).

## Inference hosting (only if the product has its own AI features)

The model tier the product serves from — distinct from the coding agents' models.

- **AWS Bedrock** — managed model hosting for product inference.
- **Akamai** (vLLM / KServe) — self-hosted model serving at the edge (listed above under compute).

---

*Captured 2026-07-15 from `/Users/phuongnz/dev/WAD26`. Names only, no prices. Re-verify existence and re-search the live landscape at SKILL step 5 — that step, not this file, is the source of truth for what to actually use.*
