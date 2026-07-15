# Observability & SLOs — how to design the feedback loop

*The design knowledge, so the skill never treats "add monitoring" as a green dashboard — it designs the feedback loop from evidence here, and fetches only live **observability / SLO tools** at SKILL step 5. Field-captured as of mid-2026; re-validate before relying on it — the field moves.*

This is a **step-4 runtime facet** (the "observability & SLOs" line of each design) and the mechanism behind the matrix cap **a maintained product ⇒ observability & SLOs from day one**. Consult it the way step 6 consults `COST-MODEL.md`. It is also what makes the whole skill's law *operable*: **a-posteriori evidence** — the climb/descend triggers — is only visible if the running product is instrumented. No observability, no evidence, no evidence-gated escalation.

## Stop trusting the health check

A `/healthz` that returns 200 proves the process is *up*. It does **not** prove the product *works* — the checkout can be broken while every liveness probe is green, because the probe doesn't exercise the real user path. That is the faith-check trap **"a green health check *looks like* health"** stated exactly. The design must measure **what the user experiences**, not just what the process reports about itself.

## Two altitudes — always measure at both

| Altitude | Answers | Catches |
|---|---|---|
| **Per-request (traces/metrics)** | did *this* request succeed, and how slow was it? | *where and why* a request failed — which service, query, or dependency |
| **Fleet / SLO (aggregate)** | is the service meeting its promise over the window? | *that* the product is degrading — before users file it as an outage |

Per-request tracing maps onto the runtime topology, so the instrumentation follows the design:

- **API / service** → request success, latency p95/p99, dependency errors
- **Data tier** → query latency, connection saturation, replication lag
- **Async / durable-execution** → job success, queue depth, retry/failure rate
- **Real-time / streaming** → back-pressure, consumer lag, drop rate

Per-request tells you *why one request* broke; the SLO view tells you the *fleet* is breaching its promise. You need both — a dashboard of green averages hides the p99 tail where real users live.

## SLIs, SLOs, and the error budget

The discipline that turns "add monitoring" into an operable feedback loop:

- **SLI** (indicator) — the measured thing: request success rate, p95 latency, freshness. Measure the **percentile the user feels (p95/p99), never the mean** — the mean hides the tail that generates complaints.
- **SLO** (objective) — the promise on the SLI over a window (e.g. "99.9% of requests succeed, p95 < 300 ms, over 30 days").
- **Error budget** — `1 − SLO`. The budget *is* the a-posteriori evidence: **budget burning fast** is the climb trigger to a heavier tier (a cache, a replica, multi-region); **budget untouched for weeks** is the de-escalation signal that a tier is over-built. This is how the matrix's climb triggers become observable numbers instead of opinions.

An SLO with no error budget is a wish; an error budget is what makes escalation *evidence-gated* rather than fear-driven.

## The evidence-backed portability anchor (flag it, don't rank tools)

- **OpenTelemetry** — vendor-neutral traces, metrics, and logs; the portability anchor. Instrument to OTel so the observability backend stays swappable and the runtime survives a vendor change (*open protocols outlive products*). Present tracing/metrics platforms (Datadog, Dynatrace, Coralogix, Sentry, Grafana-lineage, VictoriaMetrics, Better Stack, Dash0, …) as a **landscape, not a ranking** — no verified head-to-head winner exists, and the SLO discipline matters more than the vendor. Adopt OTel for portability; **budget for ingest/retention cost**, which scales with traffic and cardinality.

## Fleet health for AI-featured products — the SRE view

If the product runs **its own AI/model features**, the SLO set extends with AI-specific health signals — the field's AI-SRE view: **tokens-per-minute** (throughput/load on the model tier), **time-to-first-token** (the latency a user actually feels on a streamed response), and **turn / task success rate** (is the AI feature actually completing work, not just returning *a* response?). These sit alongside the ordinary request SLIs, and at scale they drive **model-endpoint routing / failover** and GPU-capacity tuning — the ceiling of a maintained AI product, where keeping the model fleet inside its SLOs is its own operational concern. For a product with no AI features, this section doesn't apply; the ordinary SLIs are the whole story.

## Close the loop: incidents become SLOs become gates

The mature pattern turns production pain into prevention:

1. Real incidents captured in traces → become **new SLIs / alerts** so the next occurrence is caught earlier.
2. The **release gate watches the SLIs** (see [`RELEASE-GATES.md`](RELEASE-GATES.md)) — a release that burns error budget auto-rolls-back.
3. Error-budget policy governs the pace — budget spent ⇒ freeze risky releases and stabilize; budget healthy ⇒ ship faster.

This is how a-posteriori evidence gets *manufactured* instead of hoped for — the running product tells you when to climb, when to hold, and when to de-provision.

## Anti-patterns

- **Health-check-as-health** — a liveness 200 standing in for real user-path success; the default mistake.
- **Averages hide the tail** — reporting mean latency; the p99 is where the SLO breaks and users churn.
- **Dashboards no one reads / alerts that always fire** — alert fatigue turns the feedback loop off; alert on **SLO burn**, not on every metric wiggle.
- **Trusting vendor benchmarks** — no verified head-to-head observability-tool comparison exists; present a landscape, instrument to OTel for portability, verify prices live at step 5.
- **Unbounded cardinality** — high-cardinality labels make the observability bill rival compute; budget retention and cardinality deliberately.

## Cross-check the cost line

Observability is a real standing line: platform seats + **ingest/retention that scales with traffic**, or self-hosted OTel collectors (compute + storage only). Cross-reference the **managed-service fees** line in `COST-MODEL.md`; a high-cardinality trace bill can surprise a budget as much as egress.

## What the design must state (the checkpoint)

For the observability/SLO facet of each of the three designs, name:

1. **Both altitudes** — per-request tracing *and* fleet SLOs, from day one *if maintained*, so a-posteriori climb triggers are observable.
2. **The SLIs + SLOs + error budget** — the user-felt percentile (p95/p99), the promise, and the budget whose burn *is* the climb trigger.
3. **AI-SRE signals** — TPM / TTFT / turn-success, *only if* the product runs its own model features.
4. **The cost line** — ingest/retention carried into the cost ladder.

**Floor default:** **maintained ⇒ per-request traces + core SLOs (success, p95 latency) from day one** is part of the floor, not an upgrade — it is the cap. **Throwaway/prototype ⇒ minimal**, and that is a complete design, not an omission.
