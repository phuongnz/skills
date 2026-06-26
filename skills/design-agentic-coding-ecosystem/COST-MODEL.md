# Cost model — how to estimate the cost of a design

*The method, so the skill never has to research **how** to estimate cost — it only fetches live **prices** (SKILL step 5) and plugs them in. As of mid-2026.*

Cost is the **cost arm of the master tradeoff** made concrete — here, the **cost of building the software with this agentic setup**: the coding agents' tokens (or tool subscriptions), the dev tooling, and the user's review time, *not* the product's own runtime cost. You estimate it per design so the floor→ceiling **delta** becomes a number the user can argue with — turning "nice to have" into "and here is what it costs." The estimate is a **decision instrument, not a quote**: its job is to expose the delta, not to bill anyone. Always give a **range (low / expected / high)**, never a single point — token counts vary per run, the same way the matrix gives a band, not a point.

## Which regime are you in?

The pricing regime (from the brief) decides where the math lives:

- **Metered API** — every token is a marginal dollar. The token formula below is the whole game; optimise before climbing.
- **Flat subscription** — marginal token ≈ $0. The token math becomes a **capacity check** ("does this design's volume fit inside the plan's rate limits?"), not a bill. Cost shows up as **seat fees + any overage tier + human-review time + infra** — estimate those lines and treat tokens as a throughput constraint.

## The token formula (metered regime)

**Per model call:**

```
call_cost = input_tokens      × input_price_per_token
          + output_tokens     × output_price_per_token
          + cached_in_tokens  × cached_input_price_per_token   (if prompt caching is used)
```

**Per task** (a task = one unit of build work — one ticket, one PR, one coding task):

```
task_cost = (sum of call_cost over the calls in one task)
          × retry_factor
```

**Per period:**

```
token_cost_per_period = task_cost × tasks_per_period × design_multiplier
```

### Estimating tokens per call

Input per call ≈ system prompt + tool schemas + retrieved context + conversation/history so far. Output ≈ the response + tool-call arguments. Rough ballparks when the user has no traces yet (state them as assumptions):

| Task shape | Input tokens / call | Output tokens / call |
|---|---|---|
| Light (short prompt, few tools, little context) | 2k–10k | 0.3k–2k |
| Context-heavy (large codebase in context, long history, many tools) | 20k–100k | 1k–4k |

Anchor the estimate to the design's **context budget** (the "smart zone") — a design that keeps the window curated costs less per call than one that stuffs it. This is where architecture meets cost.

### `design_multiplier` — the structural cost of the rung/workflow

The single biggest lever. It captures how many model passes the design's structure forces. These are **estimation heuristics** (except the multi-agent figure, which is the research's confirmed range) — calibrate against real traces once you have them, and **don't double-count**: estimate the design's dominant loop structure once — don't bill the coding-agent's rung loop and the workflow's loop as if they were separate.

| Design structure | Multiplier vs. rung-1 baseline | Why |
|---|---|---|
| Rung 1 — single agent + tools | ~1× | one think→act loop, a few tool calls |
| Rung 2 — reflection (separate critic) | ~2–3× | critic re-reads the work + a revise pass |
| Rung 3 — bounded planning | ~1.2–2× | a planning call up front, then execution |
| Rung 4 — ReAct | ~2–5× | several think→act→observe iterations; **avg iterations is the driver** — estimate it |
| Rung 5 — multi-agent | **4–220×** *(confirmed)* | #sub-agents × their loop lengths; the reason the ceiling should sting |
| Workflow: TDD-with-AI | +test-gen & re-run loop | usually folds into the rung loop above — count once |
| Workflow: multi-agent (BMAD personas) | per-persona passes | same lever as rung 5 — don't add it twice |
| Workflow: spec-driven | + up-front spec-gen, − rework later | a one-time cost that often *lowers* the expected total |

`retry_factor` (~1.1–1.5×) covers verifier re-runs and failed-and-retried tasks. The independent critic's calls live inside the multiplier; its *retries* live here.

## The non-token lines (both regimes)

Token cost is rarely the whole bill. Fetch live pricing for each that applies (SKILL step 5):

- **Memory / code-index store** — usually just a project-memory file the agents read and update (≈ free). A cost appears only if the design runs a managed vector / code-search index: monthly DB + a one-time embedding pass over the codebase + per-query embed. Most coding ecosystems need little or none — include it only when the design actually uses one.
- **Durable-state infra** — Postgres/checkpointer hosting, or a durable-execution platform's pricing.
- **Observability / eval** — platform seat/usage, or self-hosted OTel (compute only).
- **Human-in-the-loop time** — the gate's *real* cost, and often the dominant line for high-blast-radius designs: `reviews_per_period × minutes_per_review × loaded_hourly_rate`. Make it explicit — it is the cost the **cap imposes**, and the user must see that a gate is not free.
- **Engineering / maintenance** — build + run effort, amortized per period. Larger for higher rungs (multi-agent is "hard debugging" — weight it up).

## Total per design

```
TCO_per_period =
      token_cost   (metered)   OR   subscription seats + overage   (flat)
    + memory / code-index store
    + durable-state infra
    + observability / eval
    + human-review time
    + amortized engineering / maintenance
```

Compute this **low / expected / high** for the **floor, middle, and ceiling**, then lay them side by side. Name the **two or three line items that drive the floor→ceiling delta** (usually the `design_multiplier` and human-review time) — that is the "need vs. nice-to-have" lever the user came for.

## Gathering inputs — and the fake-example fallback

Ask the user for: **coding tasks (or PRs) per period**, **avg context size per agent call** (or take it from the design), **model tier**, **human-review volume & rate**, and the **pricing regime**. It is fine to ask.

If the user doesn't know a number, **do not stall**. Carry a clearly-labelled assumed value, compute with it, and flag every assumption with ⚠. A serviceable default example:

> ⚠ *Assumed:* ~10 coding tasks/day (~200/month) · ~25 agent calls/task · ~15k input / 1.5k output tokens per call · rung-1 baseline, retry_factor 1.2 · prices = the live ones fetched today.

Then state the **sensitivity**: which one or two inputs most move the total (almost always volume × multiplier). A fake example computed transparently still does the real job — it makes the cost *shape* visible so the user can react with their real numbers.

## Accuracy & honesty

- **Prices are live.** Use the per-token and per-service prices fetched in SKILL step 5, and **stamp the exact price and the date** used — that is what keeps the estimate close to call time.
- **Range, not point.** Low/expected/high, because per-run token counts vary.
- **Not a quote.** Say so. The number exists to expose the floor→ceiling delta and force the wants-vs-needs question — not to promise a bill. Cost must never be over-promoted into the headline; it is one arm of the tradeoff, not the decision.
