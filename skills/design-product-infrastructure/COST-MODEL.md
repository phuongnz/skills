# Cost model — how to estimate the cost of a design

*The method, so the skill never has to research **how** to estimate cost — it only fetches live **prices** (SKILL step 5) and plugs them in. As of mid-2026.*

Cost is the **cost arm of the master tradeoff** made concrete — here, the **cost of *running the product* in production**: compute/hosting, the data tier, egress, managed-service fees, the product's own inference (if it has AI features), and the on-call/ops time to keep it up. This is the **runtime bill**, *not* the cost of building the product with coding agents — that is the sibling skill `design-agentic-infrastructure`'s cost model. You estimate it per design so the floor→ceiling **delta** becomes a number the user can argue with — turning "nice to have" into "and here is what it costs." The estimate is a **decision instrument, not a quote**: its job is to expose the delta, not to bill anyone. Always give a **range (low / expected / high)**, never a single point — traffic varies, the same way the matrix gives a band, not a point.

## Which regime are you in?

The scaling regime (from the brief) decides where the math lives:

- **Usage-metered** (serverless / per-request; scales to zero) — every request is a marginal dollar. The per-request formula below is the whole game at low/spiky traffic; watch the crossover where it overtakes a reserved box.
- **Provisioned** (reserved instances/nodes) — you pay for **capacity**, used or idle. Cost is **committed instance/node hours + storage + egress + ops**, and the per-request math becomes a **capacity check** ("does this design's peak fit inside the provisioned fleet, with headroom?"), not a per-request bill. Right-size against real utilization.
- **Mixed** (reserved baseline + burst to usage-metered) — estimate it as **both lines summed**: the reserved fleet as a capacity check on the steady floor, **plus** the per-request formula applied *only to the burst slice* above the baseline. Size that slice first — the fraction of traffic that spills to the metered burst tier — because that fraction is the only place the metered cost arm pulls.

## The per-request / per-unit formula (metered regime)

**Per request** (a request = one unit of served work — an API call, a page render, a job):

```
request_cost = compute_time × compute_price_per_unit_time      (or per-invocation price)
             + data_ops      × data_op_price                    (reads/writes/queries)
             + bytes_out      × egress_price_per_gb              (the response leaving the network)
             + inference_tokens × token_price                    (only if the product runs its own model)
```

**Per period:**

```
runtime_cost_per_period = request_cost × requests_per_period × redundancy_factor
```

### Estimating compute per request

Compute per request ≈ the CPU/GPU time the request holds × the instance/function price for that time (metered platforms bill per-invocation + per-GB-second; provisioned bills the reserved hour regardless). Rough ballparks when the user has no traces yet (state them as assumptions):

| Request shape | Compute / request | Notes |
|---|---|---|
| Light (static/cached, thin API) | sub-ms–50 ms CPU | often served from cache/edge — near-free at the origin |
| Standard (DB-backed API, a render) | 50–500 ms CPU | the data-ops line usually dominates, not the compute |
| Heavy (aggregation, media, model inference) | 500 ms–seconds; GPU for inference | inference tokens or GPU-seconds become the dominant line |

Anchor the estimate to the design's **read path** — a request served from a cache/edge costs a fraction of one that hits the origin and the database. This is where architecture meets cost: the cache tier the matrix adds on an SLO cap *lowers* the per-request bill, not just the latency.

### `redundancy_factor` — the structural cost of the tier

The single biggest lever above baseline. It captures how much duplicate capacity the design's topology carries for availability/scale. These are **estimation heuristics** — calibrate against real utilization once you have it, and **don't double-count** (a multi-region deployment already includes its replicas; don't bill the replica *and* the region separately):

| Design structure | Multiplier vs. single-tier baseline | Why |
|---|---|---|
| Single tier — one host + one store | ~1× | no duplicate capacity |
| Horizontal replicas behind a balancer | ~Nx (N = instance count) | pay per running instance; autoscale makes N track load |
| Read replica(s) on the data tier | + replica hours + replication egress | offloads reads; adds standing DB cost |
| Dedicated cache tier | + cache node hours, − origin/DB ops | usually **lowers** total by removing origin work — count the offset |
| Multi-region / active-active | **~2–3×+** | duplicate estate per region **plus cross-region egress** — the reason the ceiling should sting |
| Durable-execution backbone | + platform fee + its state store | a standing cost that buys resume-not-restart for stateful work |

`redundancy_factor` covers standing duplicate capacity; **retries / failover re-runs** (~1.05–1.2×) sit on top for the extra work a degraded system does.

## The non-compute lines (both regimes)

Runtime cost is rarely just compute. Fetch live pricing for each that applies (SKILL step 5):

- **Data tier** — managed DB instance/hours or serverless-DB per-op, **storage per GB/month**, provisioned IOPS, and **backup storage**. For a maintained product the backup line is a cap, not optional. A cache tier is a separate node cost (that pays for itself in offloaded origin ops — net it out).
- **Egress / CDN** — bytes leaving the network, billed per GB and **often the surprise line**: a chatty API, media, or cross-region replication can make egress the largest single item. Size it explicitly (`bytes_out_per_request × requests`), and separately for cross-region traffic in a multi-region design. CDN offload lowers origin egress but adds its own per-GB + request price.
- **Managed-service fees** — API gateway, auth/identity, queue/event bus, durable-execution platform, observability platform (seats + ingest/retention). Observability ingest scales with traffic — a high-cardinality trace/metric bill can rival compute; budget retention deliberately.
- **Inference (only if the product has its own AI features)** — per-token (hosted model API) or GPU-hour (self-hosted). This is the **product's own runtime inference**, distinct from the coding agents' tokens in the sibling skill. Apply the token line of the formula, and cross-check the caching lever below.
- **On-call / operations time** — the *real* cost of a maintained runtime, and often dominant for a high-blast-radius design: `on_call_hours_per_period × loaded_hourly_rate` + incident time. Make it explicit — a runtime with an SLA carries human cost the cap imposes.
- **Setup / maintenance** — provisioning + IaC + migration effort, amortized per period. Larger for higher tiers (multi-region is "hard operations" — weight it up).

## Cost levers — pull these before you climb

Two levers **soften the cost arm without adding a tier** — reach for them before you price a heavier design:

- **Caching & the read path** — a cache/CDN in front of the origin removes compute *and* data-ops *and* origin egress from the hot path. It is usually the highest-leverage single move on a read-heavy product's bill.
- **Right-sizing & scale-to-zero** — provisioned capacity sitting near-idle is pure waste; metered scale-to-zero pays nothing between requests. Match the regime to the traffic shape (steady → provisioned, spiky → metered/mixed) before adding redundancy.

⚠ **Caching trades correctness for cost — govern it, don't just switch it on.** A cache needs a TTL + invalidation and observability on **staleness against correctness**: a stale hit is a *wrong answer* served fast, not a saving. Treat it as deliberate architecture with a measurable SLA. (Same discipline the sibling skill applies to agent-response caching — [`AGENT-READY.md`](AGENT-READY.md) notes where the two planes share it.)

## Total per design

```
TCO_per_period =
      compute / hosting   (metered per-request  OR  provisioned instance-hours  OR  reserved baseline + metered burst)
    + data tier (instance/ops + storage + backups)
    + egress / CDN
    + managed-service fees (gateway · queue · durable-exec · observability)
    + inference            (only if the product has AI features)
    + on-call / ops time
    + amortized setup / maintenance
```

Compute this **low / expected / high** for the **floor, middle, and ceiling**, then lay them side by side. Name the **two or three line items that drive the floor→ceiling delta** (usually the `redundancy_factor` — multi-region and a dedicated data tier — plus egress and on-call time) — that is the "need vs. nice-to-have" lever the user came for.

## Gathering inputs — and the fake-example fallback

Ask the user for: **requests (or jobs) per period**, **peak vs. average** traffic (the spikiness), **payload / compute per request**, **data volume + growth**, **egress expectation**, **inference volume** if AI-featured, the **on-call model**, and the **scaling regime**. It is fine to ask.

If the user doesn't know a number, **do not stall**. Carry a clearly-labelled assumed value, compute with it, and flag every assumption with ⚠. A serviceable default example:

> ⚠ *Assumed:* ~50 req/s average, ~200 req/s peak (~130M req/month) · ~150 ms compute + 2 DB ops per request · ~30 KB response · ~500 GB/month storage growing 10%/mo · no product inference · single on-call engineer · prices = the live ones fetched today.

Then state the **sensitivity**: which one or two inputs most move the total (almost always peak traffic × redundancy_factor, and egress on a chatty/media product). A fake example computed transparently still does the real job — it makes the cost *shape* visible so the user can react with their real numbers.

## Accuracy & honesty

- **Prices are live.** Use the per-unit prices fetched in SKILL step 5, and **stamp the exact price and the date** used — that is what keeps the estimate close to serving time.
- **Range, not point.** Low/expected/high, because traffic and per-request cost vary.
- **Not a quote.** Say so. The number exists to expose the floor→ceiling delta and force the wants-vs-needs question — not to promise a bill. Cost must never be over-promoted into the headline; it is one arm of the tradeoff, not the decision.
