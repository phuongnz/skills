# Release & rollback — how to design the delivery gate

*The design knowledge, so the skill never hand-waves "set up CI/CD" — it places the release gate from evidence here, and fetches only live **delivery / flag / rollback tools** at SKILL step 5. Field-captured as of mid-2026; re-validate before relying on it — the field moves.*

Delivery is a **step-4 runtime facet** (the "release gate" line of each design) and the mechanism behind the hard rule: the matrix cap **every irreversible release ships behind a reversible gate**. Consult this the way step 6 consults `COST-MODEL.md`. The one thing to internalize: **a successful deploy is not a successful release** — the pipeline going green means the code shipped, not that it is healthy under real traffic. Believing otherwise is the face of the faith-check trap **"a successful deploy *looks like* a successful release."**

## A release is a controlled exposure, not an event

The naive model is *deploy = done*: push, pipeline green, move on. The verified model is **progressive exposure with a watch and a way back**:

1. **Ship dark / behind a flag** — the code is in production but not yet serving users.
2. **Expose a slice** — a canary: a small % of traffic, or an internal cohort, meets the new path.
3. **Watch the slice** — error rate, latency percentiles, the business metric — *against the old path*, for a real bake period.
4. **Roll forward or roll back** — widen exposure on healthy signal; **auto-rollback** on a breach of pre-registered criteria.

The unit of safety is the **exposure control**, not the deploy. A release with no way to expose a slice and no way back is a one-way door — and a one-way door on an irreversible change is exactly what the cap forbids.

## The reversibility ladder — pick the lightest gate the blast radius demands

| Gate | What it gives | Use when |
|---|---|---|
| **Rollback / redeploy previous** | revert the whole deploy | low blast radius; the change is atomic and cheap to undo |
| **Feature flag** | flip one change on/off without a deploy; per-cohort targeting | the default runtime gate — decouples *deploy* from *release*, so exposure is a config change, not a pipeline run |
| **Canary / staged rollout** | 1% → 10% → 100% with a bake and metric watch at each step | any change that meets real traffic; a bad build reaches a slice, not everyone |
| **Blue-green** | full parallel environment, instant cutover + cutback | a change too coupled to canary; needs double capacity |
| **Shadow traffic** | new path runs on real requests, results discarded | validating a rewrite/model against production load before it serves anyone |

A single release mixes these: the risky schema change is blue-green with a tested rollback; the copy tweak is a flag flip. **Choosing one gate globally is the mistake** — match the gate to the blast radius of *that* change.

## The special case: schema & data migrations

The most irreversible release is usually a **data migration** — you can roll back code, but a dropped column is gone. The rule is **expand / contract**, never a destructive one-shot:

1. **Expand** — add the new column/table, deploy code that writes both, reads old.
2. **Migrate** — backfill; switch reads to new.
3. **Contract** — only once nothing reads the old, and a backup exists, remove it.

Each step is independently reversible. A migration that drops-and-recreates in one deploy has no way back — it violates the cap even if the code deploy is flag-gated.

## Watch after deploy — the release isn't done when the pipeline is green

The pipeline proves the build; **only production traffic proves the release.** So every gated release names:

- **The signals watched** — error rate, latency p95/p99, saturation, and at least one **business metric** (a green health check with a collapsed conversion rate is still a failed release — see [`OBSERVABILITY-SLO.md`](OBSERVABILITY-SLO.md)).
- **The bake period** — how long the slice runs before widening; long enough for the signal to be real, not noise.
- **Pre-registered rollback criteria** — the exact threshold that triggers rollback, decided *before* the release, not argued during the incident. Auto-rollback where the platform supports it.

Post-deploy watch is the delivery-side answer to *"a correct-looking deploy hides a broken release."*

## Who — or what — is allowed to ship: the governance triad

As delivery automates — CI/CD, and increasingly **agents shipping code** — the gate also answers *who is allowed to release, and can you prove it after the fact?* Three questions must stay answerable, the **governance triad**:

- **Authorization** — *is this actor allowed to ship this?* A policy-enforced scope, independent of what the actor attempts. An agent that can open a PR is not thereby allowed to deploy to production.
- **Attribution** — *who or what shipped this?* Each releasing actor — human or agent — carries its **own identity**, so every release traces to an actor. Agent identity is first-class here, not a reuse of a human's credential (see [`AGENT-READY.md`](AGENT-READY.md)).
- **Auditability** — *can you prove what shipped, by whom, and whether it was allowed?* A durable release record.

When an **agent ships code**, the feature flag *is* the runtime human-in-the-loop: the agent's change deploys dark, and a human (or a policy) flips exposure. This is the coding plane and the product plane meeting at the release gate — the flag is a shared-substrate control.

## Rubber-stamping and rollout theater — the failure modes

The mechanism works; the operators fail predictably:

- **Deploy-and-walk-away** — the release is declared done when the pipeline goes green; no one watches the slice. The dominant failure — it turns the gate into theater.
- **Canary with no real watch** — traffic is split but the signals aren't compared to the old path, so a regression widens to 100% anyway.
- **Rollback that was never rehearsed** — a "rollback plan" that has never been executed fails in the incident, when it matters most. An untested rollback is the delivery twin of an untested backup.

The sharp consequence: **a gate you don't watch is worse than no gate** — you pay the rollout cost *and* believe you have safety while having none. Designing *against* rollout theater is an architecture decision: few, well-instrumented gates; automated watch and auto-rollback; a rehearsed way back.

## Cross-check the cost & tooling

The gate's real cost is modest infra (a flag platform's seats, a second environment for blue-green) plus the **on-call time** to watch releases — cross-reference `COST-MODEL.md`'s on-call line. Durable execution / flag tooling is searched live at step 5 (present a landscape, don't quote from memory): **feature-flag platforms** (e.g. LaunchDarkly) as the runtime gate; **branch-to-production preview environments** (e.g. Upsun) for staged exposure; the CI/CD system's native canary/blue-green primitives.

## What the design must state (the checkpoint)

For the release/delivery facet of each of the three designs, name:

1. **The gate per change class** — which reversibility rung (rollback / flag / canary / blue-green / shadow) each kind of change rides, decided by blast radius, not globally.
2. **The migration discipline** — expand/contract for any schema/data change, so each step is reversible.
3. **The post-deploy watch** — the signals, the bake period, and the pre-registered (ideally automated) rollback criteria.
4. **The governance triad** — for automated/agent releases: authorization scope, releasing-actor identity, and where the audit record lands.

**Floor default:** **low blast radius ⇒ push-to-deploy + a simple rollback** is a complete design, not an omission. But **any irreversible release ⇒ a reversible gate is a cap**, present on the floor design, and it must be a *watched* gate, not a fire-and-forget deploy.
