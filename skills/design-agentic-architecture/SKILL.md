---
name: design-agentic-architecture
description: Design an agentic AI architecture from a use case and produce a dated design document. Use when the user wants to design or architect an agent or multi-agent system, decide single vs multi-agent, choose where to place memory, human-in-the-loop, or evaluation, or asks how to build an agent for a specific use case.
---

# Design Agentic Architecture

Agentic complexity is a cost you pay down, not a default you start with. This skill turns a use case into a **design document** by **climbing the ladder on evidence** — adding structure only when a need forces it — on a foundation of **durable state**, wiring in memory, **human-in-the-loop**, and observability only where each earns its place.

The architecture rules are research-backed **as of mid-2026** and live in [`PRINCIPLES.md`](PRINCIPLES.md) — consult it as you design. Tools are checked **live** (step 7) because they age fast; never recommend them from memory. The output follows [`DESIGN-DOC-TEMPLATE.md`](DESIGN-DOC-TEMPLATE.md).

Work the steps in order. Each ends on a completion criterion — do not advance until it is met.

## 1. Pin the use case

Capture the **goal** (one sentence), every **action** the agent can take (read vs. write/irreversible), the **risk profile** (irreversibility, blast radius, compliance), expected **scale**, **latency/cost** sensitivity, and the **pricing regime** (metered API vs. flat subscription — it sets how hard the cost arm pulls, and so how aggressively to optimize before climbing). If the goal is vague, interview the user before designing — a fuzzy use case yields an abstract, useless design.

**Done when:** you can state the goal in one sentence, have listed every action tagged read or write, and have captured the risk profile, expected scale, latency/cost sensitivity, and pricing regime.

## 2. Climb the ladder on evidence

Start at **rung 1** (single agent + typed, validated tools). Add a rung only for an *unmet need*: correctness → reflection (a **separate** critic), structure → bounded planning, adaptivity → ReAct, hard org boundaries → multi-agent. Pick the **lowest** rung that meets the need. Before climbing, exhaust single-agent optimization — prompting, retrieval, caching, **context engineering** (curate/compact/offload), model upgrade; a window that is overflowing or rotting is a signal to **fix the context first**, not to add a rung. Multi-agent is the last resort (4–220× tokens, handoff latency, hard debugging) and only for boundaries — never for parallelism alone. If multi-agent, enforce the **single-writer** rule: one coordinator owns the plan and all writes; sub-agents return intelligence and full traces, not actions.

**Done when:** the chosen rung is named with the specific need that justifies it (or rung 1 is justified as sufficient), and single-agent optimization — including context engineering — has been exhausted before any climb.

## 3. Lay the durable-state foundation

Decide the checkpointing / durable-execution approach **first** — it is the shared substrate that memory, HITL, long runs, and replayable traces all stand on. Retrofitting it is painful. What travels through a checkpoint or handoff is usually a **compacted** form of the context (a summary, notes file, or handoff brief), not the raw transcript — persisting context and keeping it inside its budget (step 4) are one problem seen from two ends.

**Done when:** the design states how run state is persisted and resumed.

## 4. Place memory

Start **in-context**, but treat the window as a **budget** with a sweet spot — **curate, compact** (trim/summarise), and **offload** durable facts to memory *before* reaching for a bigger window or external memory. Add external memory only when token cost or window limits actually bite. Default to RAG/vector; reach for a knowledge graph only when relationships or change-over-time matter. Bigger context is not a memory strategy (long-context models rot and hallucinate on adversarial recall). Buy the write path if needed — but discount vendor benchmarks.

**Done when:** each kind of knowledge the agent needs is assigned to a layer (in-context or external) with a reason, and the context-budget plan (curate/compact/offload) is stated.

## 5. Place human-in-the-loop

Gate an action only where **expected error cost > review-latency cost**. Score each action on irreversibility, blast radius, compliance, and confidence — but never escalate on the model's raw confidence (LLMs are overconfident); combine trust + risk. Put gates at **chain boundaries**, few and async — never on every step, which manufactures **rubber-stamping**. Oversight is a per-action dial (in / on / out of the loop), not a global mode.

**Done when:** every write/high-risk action has an explicit gate decision, and routine actions are left out-of-the-loop.

## 6. Measure the middle

Agentic systems fail in the *middle*. Instrument on the **OpenTelemetry GenAI** conventions; evaluate the **trajectory** (tool-call accuracy, retrieval groundedness, handoff quality) at step level, not just the final answer; close the loop (production traces → eval datasets → CI). For multi-agent, attribute failures with **MAST**.

**Done when:** the design names what to trace and what to evaluate at step level, plus the end-to-end check.

## 7. Recommend tools — live

Tools age fast, so **web-search current options** per capability (orchestration, durable execution / HITL, memory, observability / evaluation) — do not list tools from memory. Present a **landscape, not a ranking**: the research found no verified head-to-head winner, and frameworks ship the same primitives. Flag the two evidence-backed anchors (OpenTelemetry, MAST). Always offer a **build vs. buy** option (assemble best-of-breed, or adopt one connected ecosystem). See [`PRINCIPLES.md`](PRINCIPLES.md) for the build-vs-buy heuristics.

**Done when:** each capability lists at least one current tool, each carries the date its search was run, and the no-ranking caveat is stated.

## 8. Write the document and run the false-confidence check

Fill [`DESIGN-DOC-TEMPLATE.md`](DESIGN-DOC-TEMPLATE.md) and save it (default `./agentic-architecture-design.md` unless the user names a path). Stamp it **"architecture guidance as of mid-2026; tools searched <date>."** Then run the **false-confidence check**: audit the design against the three traps in [`PRINCIPLES.md`](PRINCIPLES.md) — the thing that *looks* fine while hiding a failure — and fix any you find before delivering.

**Done when:** the document exists at the path, is dated, and you have confirmed it contains none of the three false-confidence traps.
