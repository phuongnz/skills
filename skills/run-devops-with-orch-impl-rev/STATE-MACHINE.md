# The state machine & orchestrator rules

The bus is **real GitHub issue/PR labels**. Agents never call each other — the
**orchestrator** (a local Claude Code session) reads labels, decides the next action,
spawns a fresh subagent to do it, and transitions the label. State lives in GitHub, so
the whole thing is restartable: stop the orchestrator and the labels remember where every
issue is.

## Labels

**Flow state** (exactly one per issue at a time):

| Label | Meaning | Who acts next |
|---|---|---|
| `ready-for-impl` | Triaged, spec attached, waiting to be built | Implement subagent |
| `in-progress` | Implement subagent is working | (in flight) |
| `needs-ci` | PR opened, CI running | CI (GitHub Actions) |
| `needs-review` | CI finished (green *or* red), awaiting review | Review subagent |
| `changes-requested` | Review said no → back to implement | Implement subagent |
| `approved` | CI green **and** review OK → merge | Orchestrator: merge → `deploying` |
| `deploying` | Merge landed, Ship (CD) in flight — outcome not yet known | Orchestrator: watch the Ship run → `shipped` / `deploy-failed` |
| `shipped` | Merged and Ship (stub-)deploy succeeded | — done |
| `deploy-failed` | Ship failed | Deploy step: rollback → file issue |
| `blocked-human` | Escalation sink — needs a human decision | **The human** |

> **On `deploying`:** it's a *transient* state — set the instant the merge lands, cleared
> as soon as the Ship run concludes. With a **synchronous stub** deploy the dwell time is
> ~one API call, so it looks like ceremony. Model it anyway: (1) it makes a crash legible —
> an orchestrator that dies mid-deploy leaves the issue at `deploying`, not ambiguously at
> `approved`; (2) it's the state that earns real dwell time the moment Ship becomes
> **asynchronous** (a slow/remote deploy).

**Triage** (set by the human at Plan time — see [`TRIAGE-RUBRIC.md`](TRIAGE-RUBRIC.md)):

| Label | Meaning | Gate it triggers |
|---|---|---|
| `triage:auto` | Clear + low blast radius + testable | None — fully autonomous |
| `triage:critical` | High blast radius (control-plane / hard to undo) | Human approves the **merge** |
| `triage:big` | Big / unclear (design decision, untestable, no real spec) | Human approves the **approach before build** |

**Attempt counter:** `attempt-1` → `attempt-2` → `attempt-3`. Bumped on each
`changes-requested`. At the cap (3), flip to `blocked-human` instead of looping.

## Orchestrator loop (what the local session does each turn)

```
1. Poll:   gh issue list --state open --json number,title,labels
2. Pick ONE actionable issue, in this priority order:
     approved            → squash-merge (one commit per issue) → set `deploying` (Ship fires on push)
     deploying           → watch the Ship run: success → `shipped`; failure → `deploy-failed` (rollback first)
     needs-review        → spawn REVIEW subagent
     needs-ci            → check `gh pr checks`; when complete → needs-review
     changes-requested   → (bump attempt; if >3 → blocked-human) else spawn IMPLEMENT
     ready-for-impl      → spawn IMPLEMENT subagent  (subject to the gates below)
3. Apply the triage gate for that issue (below). If a gate says "consult", STOP
   and ask the human; do not proceed on that issue.
4. Do the action, transition the label, comment the reason on the issue.
5. Repeat until nothing is actionable or a human gate is hit, then report.
```

### Guardrails (baked into the loop)

1. **One implement agent at a time.** Only ever one issue in `in-progress`. Issues are built
   sequentially — no parallel branches colliding.
2. **Triage gates** (the human stays in the loop only where it matters):
   - `triage:big` → **before** spawning the implement subagent, the orchestrator asks the human
     to approve the approach. (Prevents building the wrong thing.)
   - `triage:critical` → the implement subagent may build and open the PR, but the orchestrator
     **will not merge** until a human approves. (Guards blast radius.)
   - both labels → human at **both** gates.
   - `triage:auto` → no human gate; runs to merge on its own.
3. **Attempt cap = 3.** implement ⇄ review can't loop forever. At the cap → `blocked-human`.
   Append to the *same* issue; never spawn duplicate issues.
4. **CI is the source of truth for merge.** Merge only when `gh pr checks` is green **and** the
   review subagent approved. A red build may be *reviewed* but **never merged**. The implement
   subagent's own "I tested it" is not a gate. **Squash-merge**, so the default branch gets
   exactly **one commit per issue** — impl-bot's intermediate commits collapse into a single,
   issue-titled commit. The merge *is* the per-issue commit; the orchestrator never
   freehand-commits app code (impl-bot authors, the merge lands it — see guardrail 6).
5. **Three identities; reviewer ≠ author at the *identity* level.** Every actor authors as its
   own GitHub identity, so "who did what" is unambiguous:
   - **impl-bot** — authors the PR, commits, and its restatement comment. Separate App,
     separate context from review.
   - **review-bot** — posts the review/approval. A *different App*, which is what makes the
     approval valid two-party review.
   - **human / orchestrator** — owns the **state machine and the merge**, and posts management
     comments. Does *not* ghost-write for the bots.
   *(The two bot logins are recorded in the project config; see `SETUP.md`.)*
6. **Split writes: authority vs authored.** The orchestrator owns only *authority* writes —
   **label/state transitions and the merge**. Everything an actor *authors* (its PR, its commits,
   its comments, its review) is written by that actor **as its own identity**, not funneled
   through the orchestrator. *(Earlier designs routed all writes through the orchestrator because
   background subagents couldn't clear permission prompts; pre-authorizing the toolkit removes
   that limitation — see `FIELD-NOTES.md`, Trap 5.)*
7. **Ship failure → rollback first.** If Ship fails, the rule is roll back, *then* file a
   follow-up issue as `ready-for-impl`.

## Not yet handled (deliberately deferred)

- **Untrusted input / prompt injection.** Issue and PR text is treated as trusted for a
  **private repo you control**. Revisit before any public/multi-user use.
- **Continuous watching.** The orchestrator is turn-driven (drains the actionable queue, then
  stops), not a 24/7 daemon. Fine for testing; add a loop later.
