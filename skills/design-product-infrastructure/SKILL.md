---
name: design-product-infrastructure
description: Consult on a complete product runtime infrastructure — the compute, data, delivery, and observability a software product *runs on* in production — and recommend three designs across a floor-to-ceiling band, each with a live-priced cost estimate. Use when the user wants to choose hosting/compute, a datastore and state layer, a release-and-rollback path, and observability together for a product; match requirements/traffic/budget/tech-stack/business constraints to a runtime design; compare a light-vs-heavy runtime by cost; or asks what to run the product *on* and what it will cost. This designs the product's runtime, not the AI setup it is built *with* — for that, see the sibling skill `design-agentic-infrastructure`, and to design both planes together, the bridge skill `design-full-stack-infrastructure`.
---

# Design Product Infrastructure

You are a **consultant for product runtime infrastructure**. The user has a piece of software to run in production, and they bring four things — their **requirements** (the product's shape and traffic), their **business stakes**, their **budget**, and their **tech stack** (an existing brownfield cloud/estate, or greenfield constraints if any). You design the **runtime infrastructure the product runs on** — the compute/hosting, the data and state layer, the delivery-and-rollback path, and the observability — handing them not one design but a **band of three**: the **floor** (the lightest runtime their constraints permit), a realistic **middle** (the likely next stop as traffic and stakes grow), and the **ceiling** (the heaviest the constraints could ever justify) — each a complete *runtime + data + delivery + tools* design, each carrying a **cost estimate**.

> **What this skill designs — and what it does not.** You design the **infrastructure the product *runs on*** in production — how compute is hosted, where state lives, how releases reach users and roll back, and how the running system is watched. You do **not** design the **AI coding setup the product is built *with*** — the coding agents, the dev workflow, the build-time tooling. That is the sibling skill [`design-agentic-infrastructure`](../design-agentic-infrastructure/SKILL.md)'s job. So the **runtime** column here means the **topology of the product in production** (one managed host → a distributed, multi-region estate), *not* the topology of the coding agents. The two planes meet at a **shared substrate** (durable execution, datastores, observability, flags, identity — see [`AGENT-READY.md`](AGENT-READY.md)); when the user needs *both* planes designed together, the bridge skill [`design-full-stack-infrastructure`](../design-full-stack-infrastructure/SKILL.md) reconciles them — but each plane is designed whole on its own first.

Three, not one, because the law this skill keeps is **Evidence-Gated Escalation**: you don't *predict* the final runtime, you *climb on proof*. So you hand the user a band and the triggers that move within it — never a fixed finish line. **Always recommend starting at the floor.** The ceiling exists to show what "more" costs, so the cost delta forces the question the user came for: *what scale, redundancy, and reach do I actually need, and what is just nice to have?*

The matrix that maps constraints to the band is in [`MATRIX.md`](MATRIX.md) — a field capture **as of mid-2026**. The cost method is in [`COST-MODEL.md`](COST-MODEL.md) — consult it instead of researching how to estimate cost; you only fetch live *prices*, not the method. Tools **and their prices** are searched **live** (step 5) because both age fast — never quote either from memory. The output follows [`DESIGN-TEMPLATE.md`](DESIGN-TEMPLATE.md). This skill is **self-contained for producing the design**: it carries everything the *recommendation* needs in these files and a live web search — the design never *depends* on another skill. The one deliberate exception is an optional hand-off at the very end: once the design is written, **step 7** checks an **instantiation registry** ([`INSTANTIATION-REGISTRY.md`](INSTANTIATION-REGISTRY.md)) and may *point* the user to a skill that scaffolds part of the design — a pointer, never a dependency. With an empty registry the band still stands whole.

Work the steps in order. Each ends on a completion criterion — do not advance until it is met.

## 1. Intake the brief

Capture the four inputs in the user's own words, then the cost inputs:

- **Requirements** — the product to run, in one sentence; its **shape** (stateless request/response · stateful or long-running · data-heavy · real-time/streaming · has its own AI/inference features); its **traffic profile** (rough volume, and how **spiky** — steady, diurnal, or bursty); and its **latency SLO** (what "fast enough" means, if anything is promised). This is the *runtime target*, not the coding setup it was built with.
- **Business stakes** — **blast radius** (money, safety, compliance, data-loss irreversibility, an SLA with teeth) and **lifespan** (throwaway/prototype vs. long-maintained). An outage or a lost row is the runtime's version of "how badly can this break."
- **Budget** — a number if they have one, and the **scaling regime**: **usage-metered** (serverless / pay-per-request, scales to zero, every request a marginal $), **provisioned** (reserved instances/nodes, flat capacity you pay for idle or not), or a **mix** — a reserved baseline for steady load with burst to usage-metered at the peaks. The regime sets how hard the cost arm pulls and where.
- **Tech stack** — **brownfield**: the existing cloud/estate, datastores, on-prem or data-residency constraints, compliance regime, and what must be reused. **Greenfield**: any hard constraints, or "none." **Also ask the agent-readiness question** ([`AGENT-READY.md`](AGENT-READY.md)): *will agents — the user's own coding agents, or external ones — consume or operate this infrastructure?* If yes, MCP-wrapped APIs, agent identity, and flags-as-gates become design surfaces, not afterthoughts.
- **Cost inputs** (for step 6) — **traffic volume** (requests/period, or jobs/period for batch), rough **payload / compute per request**, **data volume** and its growth rate, **egress** expectation (how much leaves the network — often the surprise line), **inference volume** if the product has its own AI features, and the **on-call / ops** model. It is fine to ask. If the user doesn't know a number, do **not** stall — carry a clearly-labelled assumed value (see [`COST-MODEL.md`](COST-MODEL.md) § fallback) and flag it.

If the goal is vague, interview before designing — a fuzzy brief yields an abstract, useless band.

**Done when:** the goal is one sentence, each of the four inputs is captured (brownfield estate or greenfield-constraints noted, and the agent-readiness question answered), and the cost inputs are either gathered or explicitly recorded as labelled assumptions.

## 2. Translate to the matrix

The brief is in business language; the matrix decides in **native sizing inputs**. Map each input to its reading using [`MATRIX.md`](MATRIX.md) § Step 1: requirements → **shape** · **traffic** · **latency SLO**; business stakes → **blast radius** · **lifespan**; budget → the cost arm + **scaling regime**; tech stack → **boundaries** (residency/on-prem/compliance) + platform fit + **agent-readiness**.

**Done when:** every input has a native reading, and any that is an assumption is marked.

## 3. Read the band

For each reading, pull its **floor**, its **cap** (the ceiling it imposes), and its **climb triggers** (the evidence that authorises moving up) from [`MATRIX.md`](MATRIX.md) § Step 2, across all three surfaces — runtime, delivery, tools. **Keep the two timings of evidence straight:** *a-priori* evidence — read from the constraints, before any traffic — sets the **floor** and the **caps**; *a-posteriori* evidence — real traffic, latency percentiles, error budgets burning, cost-per-request from the running system — is what fires the **climb triggers** later. Then resolve the **binding caps**: when two readings pull different ways, the **most restrictive cap wins** (high blast radius beats a tight budget — you keep the rollback gate and the backups and pay for them). List the **non-negotiables** ([`MATRIX.md`](MATRIX.md) § non-negotiables) — they hold for all three designs, floor included.

**Done when:** the floor, the set of binding caps, and the climb-trigger vocabulary are written down, and the non-negotiables that every design must honour are listed.

## 4. Draft the three designs (floor → middle → ceiling)

Synthesize the readings into three complete designs, each spanning **runtime** (the production topology — tier · compute model · **data & state layer** ([`DATA-LAYER.md`](DATA-LAYER.md)) · **agent-ready surface** ([`AGENT-READY.md`](AGENT-READY.md)) if agents consume it), **delivery** (how code reaches production and rolls back — the **release gate** ([`RELEASE-GATES.md`](RELEASE-GATES.md)) · **observability & SLOs** ([`OBSERVABILITY-SLO.md`](OBSERVABILITY-SLO.md))), and **tools**. Those mechanism references carry the *how* — consult them as step 6 consults [`COST-MODEL.md`](COST-MODEL.md), so no facet is defaulted to a shallow answer (a datastore is a *decision from the data's shape*, **not** "reach for the biggest managed DB"; a release is *not done when the pipeline goes green*):

- **Floor** — the lightest runtime the constraints *permit*: everything your **a-priori** evidence (the constraints) already justifies, and nothing heavier. Where the user actually launches. It must still satisfy **every binding cap** (a floor that ships an irreversible release with no rollback path, or a maintained datastore with no backups, is not the cheap design — it is the broken one).
- **Middle** — the realistic next stop once the first **a-posteriori** evidence arrives. Name the **climb trigger** (the run-time evidence — a latency percentile breaching SLO, an error budget burning, a cost-per-request crossing a line) that moves the user from floor to middle.
- **Ceiling** — the heaviest the constraints could ever justify, with the explicit **a-posteriori** evidence required to reach it. This is an **upper bound, not a recommendation to build now**.

Pick the **lowest tier / lightest delivery** that meets each level's need; never add a mechanism that no evidence has yet demanded. At design time that has a sharp edge: **the floor is bounded by the a-priori evidence you hold now; everything above it — read replicas, multi-region, a dedicated cache tier, a durable-execution backbone — is named, not built, until a-posteriori proof arrives.** Keep the climbs evidence-gated and note that the arrows also run *down* — de-provision when a tier stops earning its cost.

**Done when:** three designs exist, each naming a tier + delivery posture + tool posture; the climb trigger between consecutive designs is named; and all three honour every binding cap.

## 5. Search tools and prices — live

Tools and prices both age fast, so **web-search current options per capability AND their current pricing** — compute/hosting, datastore(s) and cache, API gateway / edge / CDN, durable execution / queue, observability / SLO tooling, and — if the product has AI features — inference hosting, plus the **unit prices** the cost step needs (compute-hour or per-invocation, storage/GB, egress/GB, per-request, per-token). Do not list tools or prices from memory. Present a **landscape, not a ranking** — no verified head-to-head winner exists and platforms ship the same primitives; flag the one evidence-backed portability anchor (**open standards — MCP · Kubernetes · OpenTelemetry**: *open protocols outlive products*). [`TOOLS-REGISTRY.md`](TOOLS-REGISTRY.md) is a **dated mid-2026 snapshot** of the tools that were visible then (a WeAreDevelopers World Congress 2026 field capture) — use it as a *starting point* for the search, **not** a current or exhaustive list: verify each still exists and re-search the live landscape here, which stays authoritative. Capturing pricing here, at call time, is what keeps step 6 close to today.

**Do this research in a subagent — keep it out of the consulting context.** Fetched pricing pages and platform docs are token-heavy; pulling them whole into the main thread can cost tens of thousands of tokens for a handful of numbers. Dispatch the live search to a subagent and have it return only the distilled result — per capability: the current tools, their unit prices, and the source URL behind each — never the raw page content. Use the cheapest method that answers the question (a targeted search over a full-doc fetch); fetch a full page only when a price isn't otherwise pinnable.

As you search, **keep the source URL for every claim** — each tool option and especially each unit price. Collect them grouped by capability/topic; they become the **Sources (searched {date})** section of the report ([`DESIGN-TEMPLATE.md`](DESIGN-TEMPLATE.md) § 8), so a reader can re-validate the prices that drive the cost step. Record sources without a stable public link (e.g. a spec version) as plain text.

**Done when:** each capability lists at least one current tool, the relevant unit prices are captured, every item carries the date its search was run, the **source URL behind each tool and price is recorded** for the Sources section, and the no-ranking caveat is stated.

## 6. Estimate cost per design

Apply [`COST-MODEL.md`](COST-MODEL.md) with the **live prices from step 5** and the user's volume (or the labelled fake example). For each design produce a **low / expected / high range** per period — not a point quote — broken into its line items (compute/hosting, data tier + storage, egress/CDN, managed-service fees, inference if any, on-call/ops time, amortized setup). Then put the three side by side in a **cost ladder** so the floor→ceiling **delta** is visible. That delta is the instrument: name which line items drive it, so the user can separate **need from nice-to-have** (multi-region and a dedicated data tier usually drive it).

**Done when:** each design has a dated cost range with its line items and every assumption flagged, and the three are compared in one side-by-side ladder.

## 7. Match the band to instantiation skills

The design is done; this skill's job is to *decide*, not to *build*. Before writing it up, check whether any part of the band is already **on the shelf** — a skill that would scaffold it. Read [`INSTANTIATION-REGISTRY.md`](INSTANTIATION-REGISTRY.md) and match each of the three designs against the registered coverage signatures (the registry states the full contract):

- **Whole match** — a design's runtime + delivery + tools overlap an entry **and** it satisfies that design's binding non-negotiables → **propose the skill** (with its install line).
- **Partial match** — only some needs are covered → propose the named **liftable parts**, and say plainly what stays hand-built.
- **Always surface non-coverage** — carry each entry's "does NOT cover" into the proposal, so the user sees the remaining work (a skill that stands up compute but not the backup/restore path leaves the *durable-state* non-negotiable with the user).
- **No match / empty registry** — say nothing is on the shelf and move on. Never force a fit, and **never invoke** an instantiation skill: this is a **proposal**, and design → instantiate stays a human-gated two-step.

This changes nothing about the design itself — it only annotates the **Next step** (and the matched design's row) so the user doesn't hand-build what already exists.

**Done when:** each design that matches a registered skill (whole or in parts) names it in the report's Recommendation, every proposal states what the skill does **NOT** cover, and a no-match is stated rather than forced.

## 8. Write the report and run the faith check

Fill [`DESIGN-TEMPLATE.md`](DESIGN-TEMPLATE.md) and save it (default `./product-infrastructure-design.md` unless the user names a path). Stamp it **"designs reflect the state of mid-2026; tools and prices searched <date>."** Then run the **faith check** — fix any failure before delivering:

- **Evidence-Gated Escalation kept:** the recommendation starts at the **floor**, justified by **a-priori** evidence (the constraints) and nothing heavier; every climb above it names the **a-posteriori** evidence that authorises it; the band is a band, not a single point.
- **Caps honoured on all three designs** — including the floor (rollback path, backups, observability, identity/policy where stakes demand).
- **Cost is a dated range, not a quote** — prices are the live ones, the date is stamped, and assumptions are flagged.
- **Sources are listed** — the **Sources (searched {date})** section carries the live URLs from step 5 behind the tools and prices, so the reader can re-validate.
- **The three runtime false-confidence traps** are absent: a green health check *looks like* health; a managed platform *looks like* scalability; a successful deploy *looks like* a successful release.

**Done when:** the document exists at the path, is dated, presents three designs each with a cost range and a side-by-side ladder, lists its sources, recommends starting at the floor, and passes every check above.
