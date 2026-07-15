# Product Runtime Infrastructure — {Project name}

*Designs reflect the state of mid-2026. Tools and prices searched {date}. Re-validate before building; the field — and pricing — moves. Costs are calibrated estimates to expose the floor→ceiling delta, **not quotes**. This is a design for the **infrastructure the product *runs on*** in production — compute, data, delivery, and observability — not for the AI coding setup it was built *with* (that is the sibling skill `design-agentic-infrastructure`); "runtime" below always means the production topology.*

## 1. The brief

- **Goal (one sentence):** {the product to run in production}
- **Requirements:** shape = {stateless / stateful / data-heavy / real-time / AI-featured} · traffic = {volume + spikiness} · latency SLO = {promise, or "none"}
- **Business stakes:** blast radius = {low / high — why: money / safety / compliance / data-loss} · lifespan = {throwaway / maintained}
- **Budget:** {number or "open"} · scaling regime = {usage-metered / provisioned / mixed — reserved baseline + metered burst}
- **Tech stack:** {brownfield: existing cloud/estate + residency/compliance to reuse | greenfield: hard constraints, or "none"} · agent-readiness = {agents consume/operate this: yes — surfaces apply / no — out of scope}
- **Cost inputs:** traffic = {req or jobs / period, peak vs avg} · compute/payload per request = {…} · data volume = {size + growth} · egress = {expectation} · inference = {volume if AI-featured, else "none"} · on-call = {model + rate}

> Mark every assumed value with ⚠ — especially anything the user didn't state (peak traffic, egress, data growth, on-call rate). Assumptions move the cost; flag them so they can be corrected.

## 2. Constraint translation

| The user brings… | Native reading | Cap it imposes (if any) |
|---|---|---|
| Requirements | shape {…} · traffic {…} · latency SLO {…} | {durable-state / SLO cap} |
| Business stakes | blast radius {…} · lifespan {…} | {backups + rollback gate + observability day-one} |
| Budget | cost arm + {regime} | {…} |
| Tech stack | boundaries {residency/on-prem} + platform fit + agent-readiness {…} | {residency cap, if any} |

**Binding caps (most-restrictive-wins):** {the ceilings every design must obey}
**Non-negotiables (hold for all three):** irreversible release behind a reversible gate · observability & SLOs day-one if maintained · durable state survives failure (backups + tested restore) · privileged/agent actions authorized-attributed-auditable.

## 3. The band, at a glance

| | Floor | Middle | Ceiling |
|---|---|---|---|
| **Runtime** (production topology) | {one managed tier + one store} | {+ what's added} | {+ what's added} |
| **Delivery** | {gate posture} | {gate posture} | {gate posture} |
| **Climb trigger to reach it** | — start here (what *a-priori* evidence already justifies) | {*a-posteriori*: floor→middle — e.g. p99 breaches SLO} | {*a-posteriori*: middle→ceiling — e.g. region outage hurts SLO} |
| **Expected cost / period** | {$ range} | {$ range} | {$ range} |

> **Start at the floor.** The middle and ceiling are priced so you can see what "more" costs — not a recommendation to build them now. You climb only when the named evidence appears.

## 4. The three designs

### 🟢 Floor — {one-line identity}

*The lightest runtime the constraints permit — everything your a-priori evidence justifies, no more. Launch this.*

- **Runtime (production topology):** {one managed host / serverless} + {one store matched to the data's shape; see [`DATA-LAYER.md`](DATA-LAYER.md)}. Redundancy: {none / single-AZ — climb on proof}. Durability: {backups + tested restore if maintained; checkpointing if stateful}.
- **Delivery:** {push-to-deploy + rollback / flag / canary — the gate the blast radius demands; see [`RELEASE-GATES.md`](RELEASE-GATES.md)}. Post-deploy watch: {signals + rollback criteria, or "simple rollback — low blast radius"}.
- **Observability & SLOs:** {per-request traces + core SLOs from day-one if maintained; OTel / minimal; see [`OBSERVABILITY-SLO.md`](OBSERVABILITY-SLO.md)}.
- **Agent-ready surface:** {MCP-wrapped capabilities + agent identity if agents consume it; or "no agent consumers — out of scope"; see [`AGENT-READY.md`](AGENT-READY.md)}.
- **Tools (live, {date}):** {capability → tool}, … — landscape, not a ranking.
- **Caps honoured:** {tick each binding cap — show the floor still obeys them: rollback gate · backups · observability · identity}.
- **Cost / period:** {low / expected / high}. Drivers: {compute @ {price}, {date}} · {data tier} · {egress} · {on-call}. ⚠ {assumptions}.

### 🟡 Middle — {one-line identity}

*The realistic next stop once the first a-posteriori evidence arrives.*

- **Climb trigger in:** {the named evidence — e.g. "p95 read latency breaches the SLO under load → add a cache tier"}.
- **Runtime / Delivery / Tools:** {the delta from the floor — what's added and why: a cache tier, a read replica, a tighter canary gate}.
- **Caps honoured:** {…}.
- **Cost / period:** {low / expected / high}. **Δ vs. floor:** {what the climb costs and which line item drives it}.

### 🔴 Ceiling — {one-line identity}

*The heaviest the constraints could ever justify. An upper bound, not a build-now plan.*

- **Entry condition:** {the proven scale / region-outage / write-saturation that would authorise this — and not before}.
- **Runtime / Delivery / Tools:** {e.g. multi-region active-active, dedicated data tier, durable-execution backbone; blue-green + shadow; full observability stack}.
- **Caps honoured:** {…, incl. tested cross-region failover}.
- **Cost / period:** {low / expected / high}. **Δ vs. floor:** {often large — the `redundancy_factor` (~2–3×+ for multi-region) + cross-region egress + on-call}.

## 5. The cost ladder

| Line item | Floor | Middle | Ceiling |
|---|---|---|---|
| Compute / hosting | {$} | {$} | {$} |
| Data tier (instance/ops + storage + backups) | {$} | {$} | {$} |
| Egress / CDN | {$} | {$} | {$} |
| Managed-service fees (gateway · queue · durable-exec · observability) | {$} | {$} | {$} |
| Inference (if AI-featured) | {$} | {$} | {$} |
| On-call / ops time | {$} | {$} | {$} |
| Setup & maintenance (amortized) | {$} | {$} | {$} |
| **Total / period** | **{$ range}** | **{$ range}** | **{$ range}** |

**What drives the delta:** {the 2–3 line items — usually redundancy + egress + on-call}. **Sensitivity:** {the input that most moves the total — usually peak traffic × redundancy_factor}.
**The wants-vs-needs question:** the jump from {floor} to {ceiling} costs {Δ} for {what it buys — availability, reach, headroom}. Is that a **need**, or **nice to have**? Only evidence that the floor is failing (error budget burning, SLO breached) justifies paying it.

## 6. Recommendation

- **Start here:** the **Floor** — {restate it in one line}. It is what your constraints (a-priori evidence) already justify, and it satisfies every binding cap at the lowest cost.
- **First climb trigger to watch:** {the specific *a-posteriori* evidence that would move you to the middle, and where it surfaces — an SLO breach, error-budget burn, a cost-per-request crossover}.
- **De-escalation:** {a tier to remove if the SLO shows it never earns its cost — the arrow runs both ways: a near-idle replica, an over-provisioned box}.
- **Instantiate with:** {a skill from the instantiation registry that scaffolds this design — whole, or named liftable parts — with its install line; or "nothing on the shelf — hand-build."} **Not covered by it:** {what the skill leaves to you} . *(A proposal — design → instantiate is a human-gated two-step; nothing is invoked for you.)*
- **Designing the *build* plane too?** This skill designs the product runtime only. To design the AI coding setup that builds it — and to reconcile the shared substrate (durable execution, datastores, observability, flags, identity) across both — see the sibling `design-agentic-infrastructure` and the full-stack bridge that composes the two planes.
- **Next step:** stand up the floor, instrument it (traces + SLOs) so the climb triggers are observable, and move up only when the named evidence appears.

## 7. Faith & false-confidence check

- [ ] **Evidence-Gated Escalation kept** — the floor is justified by *a-priori* evidence (constraints) and nothing heavier; every climb above it names the *a-posteriori* evidence that authorises it; the output is a band, not a single point.
- [ ] **Caps honoured on all three designs**, floor included (rollback gate · backups + tested restore · observability day-one · identity/policy where stakes demand).
- [ ] **Cost is a dated range, not a quote** — live prices, date stamped, assumptions flagged.
- [ ] **Sources listed** — § 8 carries the live URLs behind the tools and prices, so the reader can re-validate.
- [ ] No **green health check** standing in for health (looks like health, isn't — measure the user path + SLO).
- [ ] No **managed platform** standing in for scalability (looks like headroom; the bottleneck is the query / single writer, not the box).
- [ ] No **successful deploy** standing in for a successful release (looks like done; the release isn't watched or reversible).

## 8. Sources (searched {date})

The live web-search sources behind the tool landscape and the prices used above — grouped by capability/topic, with each source as a markdown link. Re-validate before building; pricing and product pages move fast. Plain-text entries are sources without a stable public link (e.g. a spec version read directly).

- {capability or topic} — [{label}]({url}) · [{label}]({url})
- {capability or topic} — [{label}]({url}) · {OpenTelemetry spec (vX.YZ)}
- …
