# Field notes — why each rule exists

The design tables live in [`STATE-MACHINE.md`](STATE-MACHINE.md) and
[`TRIAGE-RUBRIC.md`](TRIAGE-RUBRIC.md). This file is the **rationale**: the traps that only
showed up when the workflow was actually built and run, and how each one hardened a rule.
Consult it when a rule seems arbitrary or you hit an edge case.

**Reference implementation.** A real private repo with a toy todo API as substrate, real
GitHub Actions as the CI gate, a stubbed Ship, and the flow encoded as label state-machine +
triage rubric + implement/review playbooks + a seed backlog (one issue per triage branch).
Three issues were driven end-to-end: `triage:auto` (#1), `triage:critical` (#2), `triage:big` (#3).

**The two non-negotiables** everything below serves:
1. **A verification loop you don't judge by feel** — CI on every PR is the machine-runnable
   gate; a red build can be *reviewed* but never *merged*.
2. **Reviewer ≠ author** — the review agent is a *fresh context*, never the implement agent
   that wrote the PR. *(Field-tested: this must also hold at the **identity** level — Trap 1.)*

**Verify appears twice on purpose:** the implement agent's *self-verify* is fast and local; CI
is the source of truth for merge. **At least one review, always:** every PR gets a review pass
even when CI is red — a failing build and a design flaw are often the *same* root cause, and one
review that sees both catches it in a single round.

## Trap 1 — `reviewer ≠ author` must hold at the *identity* level, not just context

The non-negotiable says the reviewer is a fresh context. True, but insufficient: if both
subagents drive the **same GitHub account**, GitHub itself refuses the approval (*"Can not
approve your own pull request"*) and a security classifier flags the fallback comment as
`[Self-Approval]`. **The workflow was right to block it** — one identity authoring, reviewing,
and merging is self-approval no matter how many contexts.
**Fix:** give each agent a **distinct identity** via a **GitHub App**. impl-bot authors;
review-bot mints a short-lived App *installation token* (`app-token.js`, zero-dep RS256 JWT via
`node:crypto`) and approves as `app[bot]`. Only then is it real two-party review.
**Residual caveat:** two agents on the **same model** are identity-independent, not
*judgment*-independent — they can share blind spots. A human reviewer is the only option here
that's independent in judgment. Separate identity buys unattended merge; it does not buy a
second brain.

## Trap 2 — write actions: authored vs authority (superseded by Iteration 2)

*As first drawn:* a background review subagent couldn't get interactive approval for `gh`
**write** commands, stalled, and derailed into proposing `settings.json` edits instead of
finishing — so "subagents read/judge/report; the orchestrator performs the writes."
**Refined:** that was a **workaround for a harness limitation**, not a principle. The real
blocker was that a *background* subagent can't clear an interactive permission prompt. Once the
toolkit is pre-authorized (Trap 5), writes move to where they belong: the orchestrator owns only
**authority** writes (labels, merge, rollback); each actor **authors its own artifacts as its
own identity**.

## Trap 3 — branch discipline (how we "deleted" our own files)

The implement subagent left the on-disk repo checked out on its feature branch. The orchestrator
then committed new tooling **while unknowingly on that branch**; a later `gh pr merge
--delete-branch` deleted the branch and took the un-pushed tooling with it. **Lesson:** after any
subagent runs, the working tree is **not** where you left it — the orchestrator must assert its
branch (`git checkout <default-branch>`) before committing, and push tooling promptly. A real
hazard whenever one workspace is shared by author-agent + orchestrator.

## Trap 4 — a stubbed Ship that "failed" for the wrong reason

The Ship workflow came back `startup_failure` — an unquoted `:` in a `run:` value broke the YAML,
so it never ran. **Instructive twist:** in the *real* flow this is exactly what should trip
`deploy-failed` → rollback → file issue; the pipeline correctly flagged a bad ship. Here it was
a stub bug (fixed with block-scalar quoting) — a clean reminder that "Ship failed" and "the app
is broken" are different events, and the flow handles them the same safe way.

## Trap 5 — "unattended" isn't free: pre-allow the toolkit, but permissions ≠ gates

An "autonomous" run isn't autonomous by default. Every subagent bash call — the test command,
`git`, `gh`, minting the bot token — hits an interactive permission prompt, and a **background
subagent can't answer it**; the prompt bubbles up to the human, who becomes a click-through
bottleneck. The run only *looked* hands-off.

Two lessons that pull in opposite directions:
1. **Pre-authorize the whole routine toolkit** (in `.claude/settings.local.json` →
   `permissions.allow`). Without it, unattended runs stall on the first tool call.
2. **But permissions are NOT your human gates.** The critical-merge gate and the big-approach
   gate are enforced by the *orchestrator stopping to ask you* (its own logic / an interactive
   question), never by "leave the permission un-granted." Pre-allow generously — even `gh pr
   merge` — and keep the judgment gates in the loop. A withheld permission used as a gate just
   moves the stall to the worst moment and hands it to a subagent that can't clear it.

Two structural wins fell out of scoping the allow-list precisely:
- **Scope file writes to the write-scope globs only.** This makes "never touch CI/workflow files"
  a *structural* fact, not a hope — an edit outside scope still prompts.
- **Deny the Read tool on the secrets** (`*.pem`, `.bot-env.*`). The agents still work: each
  `source`s its `.bot-env.<role>` (a shell builtin) and `app-token.js` reads the key via `fs` —
  neither goes through the Read tool, so the private key can't be slurped into an agent's context.

**Read the "Permission" column as three kinds:** **pre-allowed** (unattended, in the allow-list),
**workflow gate** (a human decision the orchestrator's own logic stops for — deliberately
*outside* the permission layer), and **GitHub-side** (runs on GitHub; the orchestrator only reads
status). The design's judgment gates all live in the middle kind, never the first.

| Step | Responsible | Permission kind |
|---|---|---|
| Triage / classify at Plan time | **Human** | applies `triage:*` in the UI |
| Pick up `ready-for-impl`, decide the gate | Orchestrator | pre-allowed (`gh issue`) |
| **[big] Approve the approach before build** | **Human** | **workflow gate** — orchestrator STOPS and asks |
| Label transitions | Orchestrator | pre-allowed (`gh issue`) |
| Spawn subagent | Orchestrator | internal (Agent/Task tool) |
| Authenticate as bot, read spec, restate | impl-bot / review-bot | `source` (builtin) + `node app-token.js` pre-allowed; **`.bot-env.*`/`.pem` denied to Read** |
| Branch, edit source, add tests | impl-bot | pre-allowed, **scoped** Edit/Write to write-scope globs |
| Self-verify | impl-bot | pre-allowed (test command) |
| Commit, push, open PR | impl-bot | pre-allowed (`git`, `gh pr`) — the write *is* the bot's job |
| Run CI / Ship | **GitHub Actions** | GitHub-side — no local permission |
| Read CI result | Orchestrator | pre-allowed (`gh pr checks` / `gh run`) |
| Post review (approve / request-changes) | review-bot | pre-allowed (`gh pr review`) — the write *is* the job, not a gate |
| **[critical] Approve the merge** | **Human** | **workflow gate** — orchestrator STOPS and asks |
| Merge (squash, delete branch) | Orchestrator | pre-allowed — the gate already passed |
| Label `shipped` / `deploy-failed` | Orchestrator | pre-allowed (`gh issue`) |
| [ship failed] roll back first, then file issue | Orchestrator | pre-allowed (`git revert`, `gh issue create`) |

## Trap 6 — the orchestrator's own git state can contaminate a build; the review gate caught it

The headline finding, and the first time the review gate blocked a *real* defect. Before spawning
impl-bot, the orchestrator had committed machinery docs to **local default branch and not pushed
them**. impl-bot correctly branched "off the latest default branch" — but *local* carried those
unpushed commits, so its PR diff spilled **10 unrelated files** on top of the 2-file feature. **CI
went green anyway** — docs don't break tests. The *review agent* — fresh, adversarial, distinct
identity — flagged the scope violation and returned `REQUEST_CHANGES`, refusing to let 10
unreviewed files ride behind a feature PR.

Why it matters: this is **two-party review catching a defect that CI structurally cannot**, and
the defect was the *orchestrator's*, not the implementer's. Green CI plus a plausible-looking diff
is exactly the state a rubber-stamp reviewer waves through. `reviewer ≠ author` stopped being
theoretical here.
**Fix + guardrail.** Root cause: branching off a dirty local tree — a cousin of Trap 3, from the
*base* side. Two guardrails baked in so it can't recur: (a) **impl-bot branches off
`origin/<default-branch>` after a `git fetch`**, immune to whatever the orchestrator left in the
local tree; (b) the orchestrator playbook says **don't leave local default branch ahead of
`origin` when spawning a build** — push or stash first.

**One-commit-per-issue = squash-merge.** A smaller rule this pinned down: the "one clean commit
per issue" isn't a separate orchestrator commit step — it *is* the PR merge, done as a **squash**.
impl-bot authors several intermediate commits; the squash collapses them into one issue-titled
commit. The orchestrator never freehand-commits app code (that would break "authored by the
actor"); it *merges*. "Commit per issue" and "the orchestrator owns only authority writes" are the
same rule from two angles.

## Iteration 2 — three identities, one source of truth

Between issue #2 and #3 the model hardened in four connected ways — none from a crash; all from
sharper questions about *who owns what*.

**The rule: what earns a distinct identity.** A separate GitHub identity is earned by exactly one
of two things — (1) **an integrity constraint that two parties must differ** (`reviewer ≠ author`:
GitHub *structurally* blocks self-approval, so the reviewer **must** be a different identity — that
buys unattended merge); or (2) **attribution of a non-human actor's writes** (so "who did what" is
unambiguous). If neither applies, a new identity is pure ceremony. This rule tells you where to
*stop* adding bots.

**Three identities (+ one free) — and why there's no deployer bot.**
- **impl-bot** (GitHub App) — authors PR, commits, restatement comment → *attribution*.
- **review-bot** (GitHub App) — posts the review/approval → *integrity* (must differ from impl-bot).
- **human / orchestrator** — owns the state machine, the merge, rollback → authority decisions
  belong to the accountable human.
- **`github-actions[bot]`** (provided by GitHub) — executes CD, can file deploy-failure issues →
  *free* (every Actions run already has an ephemeral identity).

**No deployer bot:** deploy *execution* is done by CD (which already has an identity); deploy
*decisions* (rollback, gating) are **authority** → the orchestrator's. No pairing demands "the
deployer must differ from some party," so integrity doesn't require one and attribution is already
covered. Two caveats: a *real* deploy needs a **cloud/CD credential** (an OIDC role, a registry
token) — a different species, scoped in the pipeline's secrets, not a GitHub App; and a complex
deploy might warrant a deploy **agent** (a fresh context to judge canary health) — but that's a
**second brain, not a second identity**.

**The GitHub issue is the single source of truth; a `backlog/` file is only seed.** Holding a spec
in two places (a backlog file *and* the issue body) silently drifts. Fixed: **issue body = the
spec**, **issue comments = the hub** (human clarifications, orchestrator state notes, impl-bot's
restatement, and for `big` the human's approved approach). Nothing reads `backlog/` at runtime.
The issue becomes the hub precisely *because* every actor has an identity — a comment from
impl-bot vs review-bot vs you is legible at a glance.

**Split writes: authority vs authored** (supersedes Trap 2's blanket rule). Authority/state
(labels, merge, rollback) → orchestrator only. Authored artifacts (PR, commits, restatement, the
review) → each actor, as its own identity. And a matching split on *reads*: **read scope ≠ write
scope** — agents may **read repo-wide** (the issue, `CLAUDE.md`, ADRs) to avoid drifting from house
style, but **write only the write-scope globs**. Wide read, narrow write.

**Least-privilege per identity.** impl-bot: Contents read+write, Issues read+write (its
restatement happens *before any PR exists*, so the issue is its only home). review-bot: Contents
read, Issues **read-only** (its verdict lives on the **PR**, so it never needs to write issues).
The asymmetry is principled, not accidental — grant each identity the minimum and verify by probe.

## Running tally — what the test changed in the design

| Original claim | Refined by the test |
|---|---|
| `reviewer ≠ author` = fresh context | …and a **distinct GitHub identity** (App bot), or GitHub blocks it as self-approval |
| Agents react to labels and act | Orchestrator owns **authority** writes (labels, merge, rollback); each actor **authors its own artifacts as its own identity** |
| "Isolate agents in worktrees" | Even *orchestrator vs. author-agent* sharing one checkout needs branch discipline |
| Spawn a subagent and it runs unattended | …only if you **pre-authorize its whole toolkit** — a background subagent can't answer a permission prompt |
| Withhold a permission to create a human gate | Gates live in **orchestrator logic (an interactive question)**, not the permission layer |
| The spec is the issue *and* a `backlog/` file | The **GitHub issue is the single source of truth** (body = spec, comments = hub); `backlog/` is one-time seed |
| Two identities (human author, bot reviewer) | **Three** (impl-bot, review-bot, human/orchestrator) + `github-actions[bot]` free — a new identity earned only by **integrity or attribution**, so **no deployer bot** |
| Agents read the files they change | **Read scope ≠ write scope**: read repo-wide, write only the write-scope globs; grant each identity **least privilege** |
| `reviewer ≠ author` is a nice-to-have | It **caught a real defect** — 10 stray files green CI passed — proving two-party review earns its keep (Trap 6) |
| The implement agent branches "off the default branch" | Off **`origin/<default-branch>` after a fetch** — local may carry the orchestrator's unpushed state (Trap 6) |
| The orchestrator merges the approved PR | **Squash-merge = one commit per issue**; the merge *is* the per-issue commit |
| `triage:big` / `triage:critical` gates untested | **All three gates proven end-to-end**: `auto` autonomous, `critical` human-approves-merge, `big` human-approves-approach-before-build |
