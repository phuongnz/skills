# What this skill provides — coverage signature

**Authoritative** source for how `design-agentic-coding-ecosystem` matches a design to this
skill. It is described in *that skill's* vocabulary — rung / topology, workflow, autonomy,
tools, and the **non-negotiables** it satisfies vs. leaves to you — so a finished band design
can be matched against it. The design skill's `INSTANTIATION-REGISTRY.md` carries a curated
summary of this file; **this file wins** if the two drift. Keep it current when the skill's
shape changes.

> **What this skill is.** It *instantiates and runs* a design — it does **not** decide one.
> Which rung / workflow / tools to run is chosen upstream by `design-agentic-coding-ecosystem`.
> This skill builds a setup that already looks like the signature below.

**Instantiates:** the build-plane lifecycle — **Plan → Build → Verify → Review → Ship** — as a
running, restartable **GitHub-native** loop.

## Coverage signature

| Facet | What this skill stands up |
|---|---|
| **Architecture / topology** | A human-owned **orchestrator** + two subagents: **impl-bot** (builder) and **review-bot** (independent reviewer), each a *distinct GitHub App identity*. Realizes the **independent check / "separate critic"** as genuinely separate identities (rung-2 reflection made concrete), coordinated **single-writer** by the orchestrator. Not an autonomous multi-agent crew (not rung 5). |
| **Workflow** | The six-phase lifecycle on GitHub. Spec dial + autonomy dial applied **per issue** via triage: `big` = approve the approach *before build*; `critical` = approve *at merge*; `auto` = no gate. **Verify (CI) + Review (bot) never cut.** |
| **Autonomy** | Per-issue, human-in-the-loop **by blast radius** — gate before-build / at-merge / none. |
| **Tools** | GitHub-native: Actions (CI = merge truth; Ship/CD stubbed), `gh`, two GitHub Apps, the repo's own test command. **State bus = GitHub issue/PR labels** — durable and restartable (kill the session; the labels remember). No external DB, no MCP. |

## Non-negotiables satisfied
- ✅ **independent check never skipped** — reviewer is a *different identity*, fresh context, judges the spec
- ✅ **Verify + Review never cut** — CI green **and** bot approval both required to merge
- ✅ **single-writer** — orchestrator alone writes labels / merge / rollback; subagents author only
- ✅ **HITL gate by blast radius** — triage `critical` / `big` stop for a human
- ❌ **eval & observability day-one** — **NOT provided** (see *Does NOT cover*)

## Parts — separable units, for partial reuse
Honest seams: not all parts lift cleanly. The reviewer-identity pattern and the triage rubric
are the cleanly liftable pieces; the orchestrator loop is the **least** separable (it assumes
the rest), so "just take the orchestrator" is not a clean cut — take the whole skill instead.

| Part | File(s) | Liftable alone? |
|---|---|---|
| **Independent-review pattern** (impl-bot + review-bot as two GitHub Apps) | `agents/IMPLEMENT-AGENT.md`, `agents/REVIEW-AGENT.md`, `scripts/app-token.js`, `scripts/bot-env.example` | **Yes** — the "separate critic made real" works on any PR flow |
| **Triage rubric** (two dials → gate placement) | `TRIAGE-RUBRIC.md` | **Yes** — standalone way to place HITL gates by clarity × blast radius |
| Label state machine + guardrails (the bus) | `STATE-MACHINE.md` | Partly — reusable as a *pattern*; the orchestrator assumes it |
| Orchestrator loop (authority writes, merge, rollback, crash recovery) | `SKILL.md` | **Least** — assumes the state machine + both bot identities; take the whole skill |
| Setup / scaffolding (labels, seed backlog, token minting) | `SETUP.md`, `scripts/*.sh` | Yes — one-time installer |
| Field notes (why each rule exists — 6 traps found in practice) | `FIELD-NOTES.md` | Reference only |

## Does NOT cover — hand-build these separately
- **Monitor / observability** of the loop — no tracing, metrics, or dashboards; crash recovery is *manual* label reconstruction.
- **Evaluate / eval harness** — no agent-behavior eval, no production feedback. (The target repo's tests are *app* tests, not eval of the agents.) → For a **maintained** product, the design's *eval-day-one* non-negotiable stays with you.
- **The design decision itself** — which rung / workflow / tools to run. That's `design-agentic-coding-ecosystem`, upstream.
- Durable execution beyond GitHub labels · untrusted-input / prompt-injection hardening (private-repo trust assumed) · a continuous daemon (turn-driven only) · multi-issue parallelism (one build at a time).
