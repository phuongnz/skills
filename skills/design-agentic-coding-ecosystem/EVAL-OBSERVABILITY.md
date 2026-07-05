# Evaluation & observability — how to design the feedback loop

*The design knowledge, so the skill never treats "add eval" as a green bar — it designs the feedback loop from evidence here, and fetches only live **eval / observability tools** at SKILL step 5. Research-backed as of mid-2026; re-validate before relying on it — the field moves.*

This is a **step-4 architecture facet** (the "CI / eval" line of each design) and the mechanism behind the matrix cap **a maintained product ⇒ evaluation & observability from day one**. Consult it the way step 6 consults `COST-MODEL.md`. It is also what makes the whole skill's law *operable*: **a-posteriori evidence** — the climb/descend triggers — is only visible if the running build is instrumented. No observability, no evidence, no evidence-gated escalation.

## Stop measuring only final answers

Agentic systems **fail in the middle** — wrong tool, wrong parameters, bad retrieval, botched handoff — and a **correct-looking final output routinely hides those failures.** That is the faith-check trap **"a correct final answer *looks like* success"** stated exactly. The design must grade the *trajectory*, not just the last token.

## Two altitudes — always evaluate at both

| Altitude | Answers | Catches |
|---|---|---|
| **End-to-end** | did the task succeed? | *that* it failed — overall outcome |
| **Step-level / trajectory** | was each decision, tool call, handoff correct? | *where and why* it failed |

Step-level maps onto the architecture rungs, so the eval you need follows the design:

- **Tool use** → tool-selection / parameter accuracy
- **Memory** → retrieval groundedness
- **ReAct / planning** → step correctness
- **Multi-agent** → handoff quality, per-agent attribution

End-to-end alone tells you it broke; only the step level tells you *why* — and that "why" is what feeds the next climb decision.

## Observability is a view into the same durable state; evaluation grades it

Observability makes the trajectory **visible** (spans over agent/tool calls); evaluation **judges** it. Both rest on the same **durable, checkpointed state** as memory and HITL — one loop, one substrate. Observability provides the data; evaluation scores it.

### The two evidence-backed anchors (flag these, don't rank tools)

- **OpenTelemetry GenAI** — vendor-neutral span conventions; the portability anchor. The span tree:
  - `invoke_agent` — top-level run (agent id/name).
  - `chat` — per LLM call (input/output/reasoning tokens, cache, finish reason, time-to-first-chunk).
  - `execute_tool` — per tool call (tool name + *opt-in* args/result) — **your tool-accuracy signal.**
  - Content capture (prompts/results) is **opt-in, off by default** (PII). Status is still **experimental** — adopt for portability, but **budget for churn**.
- **MAST** (Multi-Agent System Taxonomy) — **14 failure modes** in 3 categories, the eval taxonomy anchor (built with strong human agreement, κ = 0.88):
  - **system design / specification**
  - **inter-agent misalignment** (coordination / handoffs)
  - **task verification / termination** (stopping too early, or failing to verify)

  It maps back onto this skill's own concerns: loss-of-history ↔ memory/context rot; coordination modes ↔ multi-agent; verify-the-middle ↔ the never-cut Verify.

## The mature pattern: close the loop

Production traces → **evaluation datasets** → CI gate:

1. Real failures captured in OTel traces become **regression / golden test cases.**
2. Debiased, **human-calibrated** LLM-judges score them.
3. **CI gates** catch regressions before deploy.

It's keeping a log of every mistake and turning it into next term's practice exam — and it is exactly how a-posteriori evidence gets *manufactured* instead of hoped for.

## LLM-as-judge is a biased instrument — reduce, never trust raw

If the design uses an LLM judge (e.g. for subjective "feel" testability), treat it as biased by construction: **position bias**, **length / concreteness bias** (longer, more-confident-sounding scores higher regardless of correctness), and **scoring-prompt biases**. These are reducible, not removable. Mitigation, in order:

1. **Calibrate against human labels first** — the non-negotiable baseline; your answer key.
2. **Position-swap** the scoring (present options in different orders).
3. **Label-free debiasing** (e.g. CalibraEval) to *complement*, not replace, human calibration.
4. A **stronger / bigger judge model** is measurably more stable.

A green bar from an uncalibrated judge is not evidence — it is the *appearance* of evidence.

## When it's day-one vs. when to skip

- **Maintained product ⇒ day-one.** Instrument (traces) and evaluate (trajectory) from the first commit — it's a **cap**, on the floor design, because you can't otherwise see *why* a run broke, and the climb triggers are invisible without it. This is the exact non-negotiable a build-loop instantiation skill leaves to you (see the `instrument-eval-observability` wanted entry in `INSTANTIATION-REGISTRY.md`).
- **Throwaway ⇒ skip the scaffolding.** No maintenance means no need to see *why* over time; minimal ceremony.

Cross-check the **observability / eval** line in `COST-MODEL.md` (platform seat/usage, or self-hosted OTel = compute only).

## Anti-patterns

- **End-to-end only** — hides middle failures; the default mistake.
- **Assuming pairwise comparison is inherently more reliable than scoring** — refuted; debias *whichever* you pick.
- **Trusting vendor benchmarks** — no verified head-to-head tool comparison exists; present a landscape, evaluate against *your* stack, verify live at step 5. (Tracing/eval tools to search, not endorse: LangSmith, Langfuse, Phoenix, Braintrust, Weave, RAGAS, DeepEval, …)
- **Raw LLM confidence as a score** — debias first or don't use it.

## What the design must state (the checkpoint)

For the eval/observability facet of each of the three designs, name:

1. **Both altitudes** — end-to-end success *and* the step-level trajectory checks the rung demands (tool accuracy, retrieval groundedness, handoff quality).
2. **Instrumentation** — tracing (OTel GenAI spans) present from day one *if maintained*, so a-posteriori climb triggers are observable.
3. **The judge's honesty** — if an LLM judge is used, it is calibrated against human labels, not a raw green bar.
4. **The cost line** — the observability/eval line carried into the cost ladder.

**Floor default:** **maintained ⇒ traces + trajectory eval from day one is part of the floor**, not an upgrade. **Throwaway ⇒ minimal**, and that is a complete design, not an omission.
