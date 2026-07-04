# Instantiation registry

**What this is.** A catalog of **instantiation skills** — skills that *scaffold and run* a
design this skill produces (the CI, the agent playbooks, the state machine, the tools), as
opposed to *deciding* the design, which is this skill's job. **Step 7** reads this file to see
whether a finished band design — whole, or in part — matches a skill that could build it, and
if so **proposes** it.

**The boundary this keeps.** This skill *designs*; it does not *build*. When a design lands on
a shape a registered skill already instantiates, the user shouldn't hand-build what's on the
shelf — but it stays a **proposal, human-gated**: this skill **never invokes** an instantiation
skill. Design → instantiate is a deliberate two-step.

**The matching contract.** Each entry describes its skill in *this skill's own vocabulary* —
architecture posture (rung / topology), workflow shape, autonomy, tools, and which
**non-negotiables** it satisfies vs. leaves to you. To match, compare a band design (§4 of the
report) against an entry:

- **Whole-skill match** — the design's architecture + workflow + tools overlap the entry's
  signature **and** the entry satisfies that design's binding non-negotiables → propose the
  skill (with its install line).
- **Partial match** — only some of the design's needs are covered → propose the named
  **liftable parts** the entry lists, and say plainly what stays hand-built.
- **Non-coverage is mandatory to surface** — every entry lists what it does **NOT** cover;
  carry that into the proposal so the user sees the remaining work (a skill that builds the
  lifecycle but not eval/observability leaves the *eval-day-one* non-negotiable with the user).
- **No match / empty registry** — say nothing is on the shelf; the design stands whole and is
  hand-built. **Never force a fit.**

Each skill's linked `PROVIDES.md` is the **authoritative** signature; the row here is a curated
summary — re-sync it from the source when the skill changes.

---

## Entries

### `run-devops-with-orch-impl-rev`  ·  source: `phuongnz/skills`

> **Authoritative signature:** [`../run-devops-with-orch-impl-rev/PROVIDES.md`](../run-devops-with-orch-impl-rev/PROVIDES.md)
> **Install (if absent):** `npx skills add phuongnz/skills --skill run-devops-with-orch-impl-rev`

**Instantiates:** the build-plane lifecycle — Plan → Build → Verify → Review → Ship — as a
running, restartable **GitHub-native** loop.

| Facet | Signature |
|---|---|
| Architecture | Human orchestrator + **impl-bot** (builder) + **review-bot** (independent reviewer), each a *distinct GitHub App identity*; **single-writer** orchestrator. The **independent check** as real separate identities (rung-2 reflection concrete). Not a rung-5 autonomous crew. |
| Workflow | Six-phase lifecycle on GitHub; spec + autonomy dials applied **per issue** by triage (`big`=approve-before-build · `critical`=approve-at-merge · `auto`=none). Verify (CI) + Review (bot) never cut. |
| Tools | GitHub-native: Actions (CI = merge truth, Ship/CD stubbed), `gh`, two GitHub Apps, repo test command; **state bus = GitHub labels** (durable, restartable). No external DB / MCP. |
| Satisfies | ✅ independent-check · ✅ Verify+Review-never-cut · ✅ single-writer · ✅ HITL-by-blast-radius |
| Does **NOT** cover | ❌ **Monitor / observability** · ❌ **Evaluate / eval harness** (→ a *maintained* product's eval-day-one non-negotiable stays with the user) · the design decision itself · durable execution beyond labels · untrusted-input hardening · continuous daemon · multi-issue parallelism |
| Liftable parts | **independent-review pattern** (two-GitHub-App impl + review) · **triage rubric** (dials → gate). Less separable: state machine (pattern only), orchestrator loop (take whole). See `PROVIDES.md`. |

**Matches a design when:** architecture ≈ a single / low-rung build with an **independent
reviewer** + single-writer orchestrator; workflow = the GitHub lifecycle with per-issue HITL
gates; tools = GitHub-native. Typically a **floor / low-middle** design for a maintained-but-
modest, GitHub-hosted codebase. **Always add to the proposal:** "does not cover Monitor +
Evaluate — instrument those separately if the design's lifespan is *maintained*."

---

## Adding a new instantiation skill
1. In the new skill, author a `PROVIDES.md` — its coverage signature in the shape above: what
   it instantiates, its facet table, non-negotiables satisfied, liftable parts, what it does
   **NOT** cover.
2. Add one entry here summarizing that `PROVIDES.md` and linking to it, with its source repo +
   install line.
3. **Nothing in `SKILL.md` changes** — step 7 reads this file. The skill is *closed for
   modification, open for extension*: growth is new rows here, never new logic there.
