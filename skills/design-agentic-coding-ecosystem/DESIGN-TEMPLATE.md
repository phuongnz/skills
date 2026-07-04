# Agentic Coding Ecosystem — {Project name}

*Designs reflect the state of mid-2026. Tools and prices searched {date}. Re-validate before building; the field — and pricing — moves. Costs are calibrated estimates to expose the floor→ceiling delta, **not quotes**. This is a design for the **agentic coding ecosystem you build *with*** — the coding agents, workflow, and tools — not for the product itself; "architecture" below always means the coding-agent topology.*

## 1. The brief

- **Goal (one sentence):** {the concrete outcome}
- **Requirements:** clarity = {fuzzy / firming / clear} · testability = {machine-checkable / partial / subjective}
- **Business stakes:** blast radius = {low / high — why} · lifespan = {throwaway / maintained}
- **Budget:** {number or "open"} · pricing regime = {metered API / flat subscription / mixed — flat workhorse + selective metered slice}
- **Tech stack:** {brownfield: existing stack + constraints to reuse | greenfield: hard constraints, or "none"}
- **Cost inputs:** volume = {coding tasks or PRs / period} · context size = {tokens / agent call} · model tier = {…} · human-review = {volume + rate}

> Mark every assumed value with ⚠ — especially anything the user didn't state (volume, latency, review rate). Assumptions move the cost; flag them so they can be corrected.

## 2. Constraint translation

| The user brings… | Native reading | Cap it imposes (if any) |
|---|---|---|
| Requirements | clarity {…} · testability {…} | {…} |
| Business stakes | blast radius {…} · lifespan {…} | {the binding caps} |
| Budget | cost arm + {regime} | {…} |
| Tech stack | boundaries {…} + framework fit | {latency/on-prem cap, if any} |

**Binding caps (most-restrictive-wins):** {the ceilings every design must obey}
**Non-negotiables (hold for all three):** independent check never skipped · Verify & Review never cut · {HITL gate if high blast radius} · {eval day-one if maintained} · single-writer if split.

## 3. The band, at a glance

| | Floor | Middle | Ceiling |
|---|---|---|---|
| **Architecture** (coding agents) | rung {1} {+ posture} | rung {n} {+ what's added} | rung {n} {+ what's added} |
| **Workflow** | {workflow} | {workflow} | {workflow} |
| **Climb trigger to reach it** | — start here (what *a-priori* evidence already justifies) | {*a-posteriori* evidence: floor→middle} | {*a-posteriori* evidence: middle→ceiling} |
| **Expected cost / period** | {$ range} | {$ range} | {$ range} |

> **Start at the floor.** The middle and ceiling are priced so you can see what "more" costs — not a recommendation to build them now. You climb only when the named evidence appears.

## 4. The three designs

### 🟢 Floor — {one-line identity}

*The lightest start the constraints permit — everything your a-priori evidence justifies, no more. Build this.*

- **Architecture (coding agents):** rung {1} — {single supervised agent + tools / + a reviewer agent / a multi-agent crew}. Durable state: {checkpointing / worktrees / branch-per-task / none}. Project memory: {in-context first / a `CLAUDE.md`-style file the agent updates / …}. HITL: {gate on {the risky merge — money/auth/irreversible code}, or "none — low blast radius"}. Eval: {CI from day-one if maintained / minimal}.
- **Workflow:** spec = {low/mid} · autonomy = {…} · {named workflow}. Verify+Review: {how, never cut}.
- **Tools (live, {date}):** {capability → tool}, … — landscape, not a ranking.
- **Caps honoured:** {tick each binding cap — show the floor still obeys them}.
- **Cost / period:** {low / expected / high}. Drivers: {token cost @ {price}, {date}} · {human-review time} · {infra}. ⚠ {assumptions}.

### 🟡 Middle — {one-line identity}

*The realistic next stop once the first a-posteriori evidence arrives.*

- **Climb trigger in:** {the named evidence — e.g. "Verify shows a checkable correctness gap → add rung 2 critic"}.
- **Architecture / Workflow / Tools:** {the delta from the floor — what's added and why}.
- **Caps honoured:** {…}.
- **Cost / period:** {low / expected / high}. **Δ vs. floor:** {what the climb costs and which line item drives it}.

### 🔴 Ceiling — {one-line identity}

*The heaviest the constraints could ever justify. An upper bound, not a build-now plan.*

- **Entry condition:** {the proven boundary / single-agent limit / scale that would authorise this — and not before}.
- **Architecture / Workflow / Tools:** {e.g. rung 5 multi-agent, single-writer; multi-agent workflow; fuller tool stack}.
- **Caps honoured:** {…, incl. single-writer}.
- **Cost / period:** {low / expected / high}. **Δ vs. floor:** {often large — the `design_multiplier` (4–220× for multi-agent) + review time}.

## 5. The cost ladder

| Line item | Floor | Middle | Ceiling |
|---|---|---|---|
| Coding-agent tokens (or tool subscription) | {$} | {$} | {$} |
| Memory / code-index store (if any) | {$} | {$} | {$} |
| Durable-execution / orchestration infra | {$} | {$} | {$} |
| Observability / CI eval | {$} | {$} | {$} |
| Human-review time | {$} | {$} | {$} |
| Ecosystem setup & maintenance (amortized) | {$} | {$} | {$} |
| **Total / period** | **{$ range}** | **{$ range}** | **{$ range}** |

**What drives the delta:** {the 2–3 line items}. **Sensitivity:** {the input that most moves the total}.
**The wants-vs-needs question:** the jump from {floor} to {ceiling} costs {Δ} for {what it buys}. Is that reliability/capability a **need**, or **nice to have**? Only evidence that the floor is failing justifies paying it.

## 6. Recommendation

- **Start here:** the **Floor** — {restate it in one line}. It is what your constraints (a-priori evidence) already justify, and it satisfies every binding cap at the lowest cost.
- **First climb trigger to watch:** {the specific *a-posteriori* evidence that would move you to the middle, and where it surfaces — Verify / Review / a run trace}.
- **De-escalation:** {a mechanism to remove if a trace shows it never earns its cost — the arrow runs both ways}.
- **Instantiate with:** {a skill from the instantiation registry that scaffolds this design — whole, or named liftable parts — with its install line; or "nothing on the shelf — hand-build."} **Not covered by it:** {what the skill leaves to you — e.g. Monitor + Evaluate — so it is built separately}. *(A proposal — design → instantiate is a human-gated two-step; nothing is invoked for you.)*
- **Next step:** stand up the floor, instrument it (CI + run traces) so the climb triggers are observable, and move up only when the named evidence appears.

## 7. Faith & false-confidence check

- [ ] **Evidence-Gated Escalation kept** — the floor is justified by *a-priori* evidence (constraints) and nothing heavier; every climb above it names the *a-posteriori* evidence that authorises it; the output is a band, not a single point.
- [ ] **Caps honoured on all three designs**, floor included.
- [ ] **Cost is a dated range, not a quote** — live prices, date stamped, assumptions flagged.
- [ ] **Sources listed** — § 8 carries the live URLs behind the tools and prices, so the reader can re-validate.
- [ ] No **rubber-stamped gate** standing in for oversight (looks like oversight, isn't).
- [ ] No **huge context window** standing in for memory (looks like recall, hallucinates).
- [ ] **Evaluation grades the middle**, not only the final answer (looks like success, hides failure).

## 8. Sources (searched {date})

The live web-search sources behind the tool landscape and the prices used above — grouped by capability/topic, with each source as a markdown link. Re-validate before building; pricing and product pages move fast. Plain-text entries are sources without a stable public link (e.g. a spec version read directly).

- {capability or topic} — [{label}]({url}) · [{label}]({url})
- {capability or topic} — [{label}]({url}) · {OpenTelemetry GenAI spec (vX.YZ)}
- …
