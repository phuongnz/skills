# Agentic Architecture Design — {Use case name}

*Architecture guidance research-backed as of mid-2026. Tools searched {date}. Re-validate before building; the field moves.*

## 1. Use case

- **Goal (one sentence):** {the concrete outcome}
- **Actions the agent can take:**
  | Action | Read or Write | Irreversible? | Blast radius |
  |---|---|---|---|
  | {e.g. search KB} | Read | No | None |
  | {e.g. issue refund} | Write | Yes | Customer funds |
- **Scale:** {requests/day, concurrency, conversation length}
- **Latency / cost sensitivity:** {tight / relaxed}
- **Compliance constraints:** {regulated actions, if any}

## 2. Recommended pattern (ladder rung)

- **Rung chosen:** {1–5 + name}
- **The unmet need that justifies it:** {correctness / structure / adaptivity / hard boundaries — or "rung 1 is sufficient"}
- **Single-agent optimizations to exhaust first (if not yet done):** {prompting, retrieval, caching, context, model}
- **If multi-agent:** coordinator = {who owns the plan + all writes}; sub-agents = {what intelligence they return}; parallel or single-threaded = {choice + why}.

## 3. Durable-state foundation

- **How state is persisted and resumed:** {framework checkpointer on Postgres / Temporal-style durable execution / …}
- **What relies on it here:** {long runs, HITL pauses, multi-agent coordination, replayable traces}

## 4. Memory plan

| Knowledge | Layer | Storage | Why |
|---|---|---|---|
| {conversation so far} | In-context (working) | — | perfect recall, cheap at this length |
| {help-centre facts} | External | RAG/vector | default; relationships don't matter |
| {entity relationships} | External | knowledge graph | relationships/temporal matter |
| {stable user prefs} | External | memory layer (write path) | needs store/update/forget |

- **First thing to try before adding external memory:** {keep it in-context until cost/window bites}

## 5. Human-in-the-loop plan

| Action | Gate? | Oversight mode | Risk dims that decided it |
|---|---|---|---|
| {answer question} | No | out-of-the-loop | low irreversibility/blast radius |
| {issue refund} | Yes (approve/reject) | in-the-loop | irreversible + funds + compliance |

- **Placement:** gates at chain boundaries, few, async. Not on every step.
- **Escalation signal:** trust + risk score (never raw model confidence).
- **Anti-rubber-stamping:** {how the reviewer genuinely engages — explainability, few gates, what they see}

## 6. Evaluation & observability plan

- **Tracing:** OpenTelemetry GenAI spans ({what to capture}); content capture opt-in.
- **Step-level evaluation:** {tool-call accuracy, retrieval groundedness, handoff quality}
- **End-to-end evaluation:** {task success metric}
- **Multi-agent failure attribution:** MAST {if applicable}
- **Closing the loop:** {how production traces feed regression/golden datasets}

## 7. Recommended tools (live — landscape, not a ranking)

*No verified head-to-head winner exists; frameworks ship the same primitives. Choose on operational fit; test on your stack. Searched {date}.*

| Capability | Current options | Notes |
|---|---|---|
| Orchestration / glue | {from live search} | |
| Durable execution / HITL | {from live search} | |
| Memory | {from live search} | buy the write path; discount benchmarks |
| Observability / eval | {from live search} | instrument on OpenTelemetry (evidence-backed) |

- **Build vs. buy:** {assemble best-of-breed, or adopt one connected ecosystem — recommendation + why}

## 8. Risks & the false-confidence check

- [ ] No human gate here will be **rubber-stamped** (looks like oversight, isn't).
- [ ] No huge context window is standing in for **memory** (looks like recall, hallucinates).
- [ ] Evaluation grades the **middle**, not only the final answer (looks like success, hides failure).
- **Other risks:** {workload-specific}

## 9. When to climb next

- **Current rung holds until:** {the measured failure that would justify the next rung}
- **Open questions / things to measure:** {what to instrument to make the next decision on evidence}
