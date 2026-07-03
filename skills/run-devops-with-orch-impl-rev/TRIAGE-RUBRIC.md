# Issue triage rubric

Applied **by a human at Plan time**, before an issue gets `ready-for-impl`. It assigns each
issue one of the `triage:*` labels, which decides *where (if anywhere) a human gate sits*.
It falls out of four dials — **blast radius, lifespan, clarity, testability** — applied
per-issue instead of per-project.

## "Big" and "critical" are different axes

- **Critical = high blast radius** (how bad if it ships wrong). Human gate at **merge/ship**.
- **Big / confusing = low clarity or low testability** (how likely the agent builds the
  *wrong* thing, or can't prove it's right). Human gate **before the build**.

They are independent. A one-line fix on the payments path is *critical but clear*. A sprawling
refactor of a toy feature is *big but harmless*.

|                       | Clear + testable | Unclear / untestable |
|-----------------------|------------------|----------------------|
| **Low blast radius**  | `triage:auto` — fully autonomous | `triage:big` — human approves approach first |
| **High blast radius** | `triage:critical` — human reviews before merge | `triage:critical` + `triage:big` — human at both ends |

## Trigger checklists (any box ticked → that label)

**`triage:critical`** (→ human approves the merge). Roughly: *touches the control plane, or is
hard to undo.*
- [ ] auth / sessions / secrets / permissions
- [ ] money / billing
- [ ] schema migration or data-destructive op (DROP, DELETE, backfill)
- [ ] public API contract change (breaks clients)
- [ ] the pipeline / deploy / CI config itself
- [ ] hard to roll back (if `git revert` + redeploy doesn't cleanly undo it)

**`triage:big`** (→ human approves the approach before the implement agent builds).
- [ ] can't describe the intended diff in ~one sentence
- [ ] crosses multiple modules/layers, or touches many files
- [ ] needs a design decision with more than one reasonable answer
- [ ] "done" can't be machine-checked (UX feel, product judgment)
- [ ] the issue is a title with no real spec

**`triage:auto`** — none of the above ticked. Clear, low-stakes, testable.

## Two honest guards against mis-tagging

Humans skimming systematically *under-rate* ambiguity (the perception gap).

1. **Default to escalate when unsure** — a needless human glance is far cheaper than an agent
   confidently shipping the wrong thing.
2. **The implement agent restates the plan first.** Its first act is to restate the intended
   diff and check it against the spec. If they diverge, the issue was mis-tagged as "clear" —
   caught for pennies, before any code. (Grill the ticket.)
