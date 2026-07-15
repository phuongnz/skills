# The Decision Matrix — constraints to a starting band

*A field capture as of mid-2026 (WeAreDevelopers World Congress 2026). A self-contained decision matrix that maps a product's constraints to a starting band for its **runtime infrastructure** — the compute, data, delivery, and observability the product runs *on*. The band-of-three method is inherited from the sibling skill `design-agentic-infrastructure`; the tiers and tools below are the market landscape captured at the congress. Re-validate before relying on it; the field moves.*

## Read it as a band, not a point

A matrix that printed one fixed runtime would betray the one law every design here keeps — **Evidence-Gated Escalation**: you don't *predict* the final runtime, you *climb on proof*. So for each constraint the matrix sets three things, not an answer:

- **a floor** — the lightest runtime the constraint *permits*. Launch here.
- **a ceiling / cap** — the hard limit it *imposes* (marked **cap ·**). Never below this, whatever else you do.
- **climb triggers** — the evidence (marked **→**) that authorises moving up *inside* the band.

Evidence comes in **two timings**, and the band is built from both. **A-priori** evidence is read straight from the constraints, *before a request is served* — it sets the **floor** and the **caps** (Step 2 below). **A-posteriori** evidence is produced by the running product — real traffic, latency percentiles, error-budget burn, cost-per-request — and it is what fires the **climb triggers** that move you up *or* down later. Same currency; they differ only in *when* the justification arrives. The cheap structural rungs (a managed host, one database, a rollback flag) can be justified a-priori; the expensive ones (read replicas, a dedicated cache tier, multi-region, a durable-execution backbone) almost always need a-posteriori proof — which is why you *don't pre-scale*.

The matrix narrows the band; human judgement still applies within it. A decision aid, not an oracle.

## Step 1 · Translate the brief

The user's constraints are in business language; the matrix decides in **native sizing inputs**. Translate first.

| The user brings… | Reads as (native sizing input) | Lands under |
|---|---|---|
| **Requirements** (shape? traffic? latency SLO?) | **shape** · **traffic profile** · **latency SLO** | Requirements |
| **Budget** (how much; usage-metered / provisioned / mix) | the cost arm + **scaling regime** | Budget |
| **Tech-stack constraints** (cloud, residency, on-prem, compliance, agents-as-consumers) | **boundaries** + platform fit + **agent-readiness** | Tech stack |
| **Business constraints** (money, safety, compliance, SLA, data-loss, longevity) | **blast radius** · **lifespan** | Business stakes |

## Step 2 · Match the matrix

Three columns = the three design surfaces of the runtime: the **runtime** (the production topology — from one managed host to a distributed, multi-region estate — plus where state lives), the **delivery** you release and roll back with, and the **tools**. None of these is the topology of the coding agents that built the product — that is the sibling skill's concern. Read the floor, obey the caps (**cap ·**), note the climb triggers (**→**).

### Requirements

| Your reading | Runtime (production topology) | Delivery (release process) | Tools |
|---|---|---|---|
| **Shape: stateless request/response** | One managed runtime (serverless / a PaaS host); state in one managed store. **→ horizontal replicas behind a load balancer when a single instance saturates.** | Push-to-deploy; a health check + one rollback path is enough. | Serverless / PaaS host; one managed datastore. |
| **Shape: stateful / long-running** | **cap ·** durable, checkpointed state — a job that dies mid-run must resume, not restart. **→ a durable-execution backbone (e.g. Temporal) when workflows outgrow a request timeout.** | Migrations gated; drain-and-resume on deploy, never kill-in-flight. | Durable-execution / queue substrate; a state store with backups. |
| **Shape: data-heavy** | The **data tier is the design** — pick the store from the data's shape ([`DATA-LAYER.md`](DATA-LAYER.md)), size it first. **→ read replicas / a cache tier when read latency or DB load climbs.** | Schema migrations are the risky release — expand/contract, never a destructive one-shot. | Store matched to shape (relational · document · graph · timeseries · vector); a cache. |
| **Shape: real-time / streaming** | Persistent connections / an event backbone; back-pressure by design. **→ partition / shard when a single broker or region can't hold the fan-out.** | Progressive rollout — a bad build reaches a slice, not the whole stream. | Streaming / pub-sub substrate; edge close to users. |
| **Traffic: spiky / bursty** | **cap ·** the runtime must absorb the peak *or* shed load gracefully — a design that falls over at the spike is broken, not cheap. Prefer scale-to-zero + autoscale, or a reserved baseline + burst. | Canary before a full rollout so a bad build doesn't meet the peak. | Autoscaling compute; a queue to flatten bursts. |
| **Latency SLO: strict** | **cap ·** the SLO caps how far the request can travel — edge/CDN, a read path that avoids the origin, a cache. Measure p95/p99, not the mean. | Shadow traffic / canary with a **latency gate** — a release that breaches p99 rolls back. | CDN / edge; a cache tier; the SLO wired into the release gate. |

### Business stakes

| Your reading | Runtime | Delivery | Tools |
|---|---|---|---|
| **Blast radius: high** (money · safety · irreversible · data-loss) | **cap ·** durable state with **backups + a tested restore path**; redundancy on the tier whose failure loses money/data; observability on. Start at the lowest tier that carries these, not below. | **cap ·** every irreversible release ships **behind a reversible gate** — flag / canary / staged rollout with pre-registered rollback criteria; migrations expand/contract. **Verify in production, watch after deploy.** | Feature flags as the runtime gate (e.g. LaunchDarkly); backup/restore tooling; identity + policy + audit on privileged actions. |
| **Blast radius: low** | Single tier; no redundancy until proof; scale-to-zero fine. | Push-to-deploy; a simple rollback; climb only on proof. | Default light stack. |
| **Lifespan: long / maintained** | **cap ·** observability & SLOs from day one; backups from day one. **→ add a cache / read-replica tier when a-posteriori load data shows the origin is the bottleneck — not before (a managed platform *looks like* scalability; the bottleneck is usually the query, not the compute).** | Repeatable, auditable releases; migrations versioned; rollback rehearsed. | Tracing + SLO tooling (OpenTelemetry); backup/restore; IaC so the estate is reproducible. |
| **Lifespan: throwaway / prototype** | Single managed host; skip redundancy, backups-lite, minimal state. | Deploy by hand or one command; minimal ceremony. | Minimal; a free-tier host; no durable backbone. |

### Budget

| Your reading | Runtime | Delivery | Tools |
|---|---|---|---|
| **Usage-metered** (serverless / per-request; scales to zero) | Cheapest at low/spiky traffic — you pay for what you serve. Watch the **crossover**: past a steady-load threshold, per-request billing overtakes a reserved instance. **→ move a hot, steady path to provisioned when metered cost per request stops falling.** | Deploy-per-change is cheap; keep functions warm only where cold-start breaks the SLO. | Serverless platform; managed data with per-op pricing; **watch egress — the metered surprise line.** |
| **Provisioned** (reserved instances/nodes; flat capacity) | You pay for the peak even when idle — right for **steady** load, wrong for spiky. Right-size against real utilization, don't over-provision "to be safe." | Rolling deploys across the fleet; capacity headroom absorbs a bad node. | Reserved compute; committed-use / savings-plan discounts; a load balancer. |
| **Mixed** (reserved baseline + burst to usage-metered) | Reserved capacity carries the steady floor of traffic; burst to serverless/on-demand at the peaks — the spiky tail doesn't pay peak-capacity rent all month. | Default to the reserved fleet; route overflow to the metered burst tier. | Reserved baseline + autoscaling burst; a queue so the burst is absorbed, not dropped. |

> **Egress note.** Across every regime the line that surprises budgets is **data egress** — bytes leaving the network (to users, across regions, to another cloud). It is often billed separately from compute and storage, and a chatty API or a cross-region replica can make it the largest line. Size it explicitly in step 6; don't let it hide.

### Tech stack

| Your reading | Runtime | Delivery | Tools |
|---|---|---|---|
| **Boundaries: data residency / on-prem / compliance regime** | **cap ·** region/tenancy is dictated — the data physically stays where the regime says. A residency rule *caps* which managed services and regions you may use. | Deploys must respect the boundary (no build artifact or backup crossing it uncontrolled). | Region-locked / on-prem-capable platforms; a store that supports the residency guarantee. |
| **Brownfield estate / platform lock** | Shaped by what exists — reuse the running datastore/cloud unless it's the proven bottleneck. A latency or platform constraint **caps** how many tiers you can add. | Fits the existing pipeline; don't rebuild delivery to add one service. | Platform often dictated — but they ship the *same primitives*, so pick by ecosystem fit, not hype. Favour tools that speak **open standards** (MCP · Kubernetes · OpenTelemetry): *open protocols outlive products*, so an open-standard runtime survives a vendor/cloud change without a rewrite (vendor-mortality is a real tool-fit risk). |
| **Agent-readiness: agents will consume or operate this** | The runtime gains a surface: **MCP-wrapped APIs** (the agent, not a human UI, is the consumer), **agent identity** at the edge (a distinct credential, not a shared human key), and **flags-as-gates** an agent's action can be held behind. See [`AGENT-READY.md`](AGENT-READY.md). | An agent-shipped change rides the same reversible gate as any risky release — the flag *is* the runtime HITL. | API gateway that speaks MCP (e.g. Kong); an identity/policy layer for non-human actors; audit on every agent action. |

**Tie-break:** when two readings pull different ways, the **most restrictive cap wins** — the tightest ceiling across all constraints is the one you obey. (High blast radius beats a tight budget: keep the backups and the rollback gate and pay for them. A residency rule beats the cheapest region.)

## The non-negotiables (the ceiling, always)

These caps hold no matter where the constraints land. If a cheap, fast runtime violates one, it isn't the cheap option — it's the broken one. **Every design in the band, floor included, must honour all of these.**

- **Every irreversible release ships behind a reversible gate.** A flag, a canary, or a staged rollout with pre-registered rollback criteria — never a one-way door pushed straight to 100%. *(A successful deploy is not a successful release; see [`RELEASE-GATES.md`](RELEASE-GATES.md).)*
- **A maintained product ⇒ observability & SLOs from day one** — or you can't see *why* it's degrading, and you can't tell a green health check from real health. *(See [`OBSERVABILITY-SLO.md`](OBSERVABILITY-SLO.md).)*
- **Durable state survives failure.** Stateful/long-running work is checkpointed (resumes, not restarts); a maintained datastore has **backups and a *tested* restore path**. An untested backup is not a backup.
- **Privileged actions are authorized, attributed, and auditable.** Who or *what* (agent or human) did this, was it allowed, can you prove it after the fact — the governance triad. This *rises in force* as agents become consumers/operators of the runtime. *(See [`AGENT-READY.md`](AGENT-READY.md).)*

## The climb triggers (inside the band) — a-posteriori evidence

Step 2 set the floor and caps from **a-priori** evidence. What moves a design up or down *after* you launch is **a-posteriori** evidence — produced by the running product (traffic, latency percentiles, error budget, cost-per-request, the trace of a real incident) — and it has a fixed vocabulary. Arrows run **both ways**: the same discipline *de-provisions* when a tier stops earning its cost.

| Evidence you observe | Surface | The move it authorises |
|---|---|---|
| Read latency (p95/p99) climbs under load | runtime | + a cache tier, then a read replica — origin offload before a bigger box |
| A single instance/broker saturates at peak | runtime | + horizontal replicas / partitioning behind a balancer |
| Workflows outgrow a request timeout / die mid-run | runtime | + a durable-execution backbone (checkpoint-and-resume) |
| One region's outage or latency hurts the SLO | runtime | + multi-region / failover — the ceiling, and it stings |
| Metered cost per request stops falling as volume grows | runtime | move the hot steady path to **provisioned** (or the reverse) |
| Error budget burning; a release caused a regression | delivery | tighten the gate — canary %, longer bake, a latency/error auto-rollback |
| A tier is provisioned but sits near-idle for weeks | both | − **de-provision**: drop the replica / shrink the box / scale to zero |
| Egress becomes a top-two line item | both | a CDN / cache at the edge, or move the chatty path in-network |

## How this drives the three-design band

- **Floor** = read the floor cell of every constraint, then satisfy every binding cap. The lightest runtime the constraints *permit* — one managed tier that still has its rollback gate, its backups, and its day-one observability where the caps demand them.
- **Middle** = apply the first one or two climb triggers most likely to fire given the traffic and stakes (e.g. a strict SLO under growing read load → a cache tier; a maintained product finding its first regression → a tighter canary gate).
- **Ceiling** = the heaviest tier/delivery any constraint's climb trigger could ever authorise (multi-region, dedicated data tier, durable-execution backbone), *with that trigger stated as its entry condition* — an upper bound, not a build-now recommendation.

The recommendation always **starts at the floor**. The ceiling's job is to price "more" so the cost ladder exposes need vs. nice-to-have.
