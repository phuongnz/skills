# Tools registry — a mid-2026 landscape snapshot

> **Read this first.** This is a **snapshot of the product-runtime-infrastructure tool landscape as of mid-2026**, captured from the field at the **WeAreDevelopers World Congress 2026** (Berlin, 8–10 July 2026 — 492 sessions, ~98 booths). Use it as a **reference / starting point** when searching for the right tools for a design — **not** as a current or exhaustive list, and **not** a ranking. Tools appear, merge, rename, and die fast: **verify each still exists and re-search the live landscape.** The skill's **step-5 live search stays the authoritative check** — this file only gives it a running start. No prices here (they age faster than names); fetch those live at step 5. Each entry does carry its **slow-aging fields** — *[license · hosting model]*, hosting ∈ SaaS · self-host · hybrid (both) · library — verified 2026-08-06, because they are decisive early filters: free + self-hostable candidates survive floor-stage economics that per-seat SaaS pricing does not. Slow-aging is not non-aging — licenses do change (Redis did); re-verify at step 5.

**Scope.** These are the tools that serve the *product runtime* — what the software runs *on* in production. Coding-plane infrastructure (the agents, the dev workflow, the build-time tooling) is the sibling skill `design-agentic-infrastructure`'s concern; a few **shared-substrate** tools (⇄) legitimately appear in both because one deployment serves the product backend *and* the coding agents (see [`AGENT-READY.md`](AGENT-READY.md)).

**Evidence grade.** Presence at the congress is a **market/practitioner signal** (a category with sessions *and* booths behind it is validated as real demand), not a quality verdict. Where a whole category rests on a **single vendor's product story**, it is marked **⚑ vendor-amplified** — treat those names as one data point, confirm independently at step 5.

## Compute · hosting · platform

The runtime tier the product runs on — from serverless to managed Kubernetes to the edge ([`MATRIX.md`](MATRIX.md) runtime column).

- **Vercel** *[proprietary · SaaS]* — serverless/edge hosting with agents as a first-class workload (Fluid Compute, Sandbox, Workflow).
- **Akamai** *[proprietary · SaaS]* — "cloud built for AI": managed Kubernetes + model-serving (vLLM / KServe lineage) at the edge.
- **AWS Amplify Gen2** *[open-core (Apache-2.0 tooling) · SaaS — deploys only to AWS]* — full-stack managed hosting. *(AWS Kiro seen alongside it is a **coding-plane** tool — the sibling skill's concern, not product runtime.)*
- **Azure Foundry** *[proprietary · SaaS — Foundry Local variant runs on-prem]* — managed application/AI platform. ⚑ single-vendor.
- **Upsun** *[proprietary · SaaS]* — PaaS with branch-to-production environment cloning (preview/staged exposure).
- **Kubermatic** *[open-core (Apache-2.0 CE) · self-host]*, **OpenShift** *[open-core · hybrid — OSS upstream is OKD]* — Kubernetes platform management for self-run estates.
- **Edge Impulse** *[proprietary · SaaS — models deploy on-device]* — edge / embedded / on-device runtime.

## Data tier · datastores · cache

Pick the store from the data's *shape*, not habit ([`DATA-LAYER.md`](DATA-LAYER.md)).

- **TiDB** *[Apache-2.0 · hybrid]* — distributed, scale-out relational (HTAP).
- **Percona** *[GPL-2.0 · self-host]* — managed/hardened MySQL & Postgres operations.
- **RavenDB** *[AGPL-3.0 (dual commercial) · hybrid]* — document store.
- **Neo4j** ⇄ *[open-core (GPL-3.0 CE) · hybrid]* — graph store (product data *and* agent memory/context — shared-substrate).
- **Redis** ⇄ *[AGPL-3.0 (Redis 8+, tri-licensed) · hybrid]*, **Aerospike** *[open-core (AGPL-3.0 CE) · hybrid]* — in-memory / low-latency key-value; cache, session, real-time context (Redis serves agents too — shared-substrate).
- **ClickHouse** *[Apache-2.0 · hybrid]*, **MotherDuck** *[proprietary · SaaS — on MIT DuckDB]* — columnar / analytical / timeseries.
- **OpenSearch** *[Apache-2.0 · hybrid — Linux Foundation]* — full-text / faceted search index.

## Edge · API gateway · connectivity

The surface between the product and its consumers — including agent consumers ([`AGENT-READY.md`](AGENT-READY.md)).

- **Kong** ⇄ *[open-core (Apache-2.0 gateway) · hybrid — Konnect control plane is SaaS]* — API gateway; MCP-gateway lineage that turns product APIs into agent-callable tools (the agent-ready contract). Shared-substrate where agents consume the runtime.
- **Cloudinary** *[proprietary · SaaS]* — media pipeline / CDN.
- **Twilio** *[proprietary · SaaS]* — communications APIs (messaging/voice).
- **Tailscale** *[open-core (BSD-3-Clause client) · SaaS — control plane is SaaS]* — scoped network connectivity (a control point for non-human/agent access).

## Durable execution · workflow · release

The long-running backbone and the delivery gate ([`RELEASE-GATES.md`](RELEASE-GATES.md)).

- **Temporal** ⇄ *[MIT · hybrid]* — durable execution; long-running product workflows *and* the checkpoint layer coding agents pause on (shared-substrate).
- **LaunchDarkly** ⇄ *[proprietary · SaaS]* — feature flags as the runtime release gate — and the gate on agent-shipped code (shared-substrate).
- **Harness** *[proprietary · hybrid — Harness Open Source is Apache-2.0]* — CD / release pipelines.
- **Bitrise** *[proprietary · SaaS — self-hosted build runners exist]* — mobile CI/CD.

## Observability · SLO · cost

Measure the user path and the SLO, not the health check ([`OBSERVABILITY-SLO.md`](OBSERVABILITY-SLO.md)). The evidence-backed portability anchor (**OpenTelemetry**) lives in that file; the platforms below are landscape, **not** endorsements — no verified head-to-head comparison exists.

Tracing / metrics / SLO platforms ⇄ (several carry agent-aware angles — shared-substrate where the coding plane reuses them):

| Platform | License · hosting |
|---|---|
| **Datadog** | proprietary · SaaS *(agent is Apache-2.0)* |
| **Dynatrace** | proprietary · hybrid *(managed on-prem supported)* |
| **Coralogix** | proprietary · SaaS *(BYOC: data in your S3)* |
| **Sentry** | FSL-1.1 *(→ Apache-2.0 after 2 y)* · hybrid |
| **VictoriaMetrics** | open-core (Apache-2.0 core) · hybrid |
| **Better Stack** | proprietary · SaaS |
| **Dash0** | proprietary · SaaS |

- **CloudHiro** *[proprietary · SaaS]* — cloud cost / FinOps visibility (the egress/right-sizing lines in [`COST-MODEL.md`](COST-MODEL.md)).

## Inference hosting (only if the product has its own AI features)

The model tier the product serves from — distinct from the coding agents' models.

- **AWS Bedrock** *[proprietary · SaaS]* — managed model hosting for product inference.
- **Akamai** (vLLM / KServe) *[platform proprietary · vLLM/KServe are Apache-2.0 self-host]* — self-hosted model serving at the edge (listed above under compute).

---

*Captured 2026-07-15 from `/Users/phuongnz/dev/INFO-WAD26`; slow-aging fields (license · hosting) verified 2026-08-06 by live search. No prices. Re-verify existence and re-search the live landscape at SKILL step 5 — that step, not this file, is the source of truth for what to actually use.*
