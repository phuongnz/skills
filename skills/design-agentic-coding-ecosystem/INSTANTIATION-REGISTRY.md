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
- **Wanted (not yet built)** — entries under *§ Wanted* name a known gap that **no skill
  instantiates yet**. They carry **no `PROVIDES.md` and no install line**, so **never propose one
  as installable**. Their only use: when a design's *non-coverage* (e.g. Monitor + Evaluate on a
  *maintained* product) matches a wanted entry, say so in the report's *hand-build this
  separately* note — "a skill to close this is planned, not yet built" — so the gap is **tracked
  once**, not silently re-discovered every design.

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

## Wanted (not yet built)

Known gaps a design keeps landing on that **no skill instantiates yet**. These are *signposts*,
not shelf items: **no install line, no `PROVIDES.md`** — step 7 must never propose them as
installable. Their job is to make a recurring non-coverage **visible**, so the report's
*hand-build this separately* note can say "planned, not yet built" instead of rediscovering the
same gap every time.

### `instrument-eval-observability`  ·  status: **WANTED — not built**

> **Would close the gap left by `run-devops-with-orch-impl-rev`: Monitor + Evaluate.** For a
> *maintained* product the design's **eval-day-one** non-negotiable currently stays with the
> user (hand-built) — this skill would instantiate it.

**Would instantiate:** the **product-plane foundation** for a maintained build — **Monitor**
(run-trace observability) + **Evaluate** (an eval harness that grades the *trajectory*, not only
the final answer) — stood up **day one**, wrapping whatever build loop is already running.

| Facet | Intended signature *(hypothetical — not yet built)* |
|---|---|
| Architecture | **Not** an agent topology — **instrumentation around** the build loop: tracing spans on every agent/tool call, an **eval harness** as a separate grader, metrics/dashboards. Composes *alongside* a loop skill like `run-devops`; it does not replace it. |
| Workflow | **Eval-in-CI** — trajectory grading as a gate, not just app tests; continuous run-trace collection so *a-posteriori* climb triggers become **observable**. |
| Tools | Anchored on the two evidence-backed standards the matrix already names — **OpenTelemetry GenAI** (tracing) and **MAST** (failure taxonomy for eval) — plus a trace/eval store (searched live when built). |
| Would satisfy | ✅ **eval & observability day-one** — the exact non-negotiable `run-devops` leaves open for maintained products. |
| Does **NOT** cover | the build loop itself (that's `run-devops` or another instantiation skill) · the design decision (upstream — this skill). |

**Why it belongs here now (empty though it is):** the dry-run against a *maintained* GitHub repo
lands on `run-devops` for the loop **plus** a hand-built eval/observe layer. That second half is
a real, recurring gap — logging it as a want means the next maintained design *names* it instead
of re-deriving it. When it gets built, a maintained design would propose **both** skills together
and close the band with no hand-built remainder.

---

## Adding a new instantiation skill
1. In the new skill, author a `PROVIDES.md` — its coverage signature in the shape above: what
   it instantiates, its facet table, non-negotiables satisfied, liftable parts, what it does
   **NOT** cover.
2. Add one entry here summarizing that `PROVIDES.md` and linking to it, with its source repo +
   install line.
3. **Nothing in `SKILL.md` changes** — step 7 reads this file. The skill is *closed for
   modification, open for extension*: growth is new rows here, never new logic there.

**Promoting a wanted entry.** When a skill under *§ Wanted* actually gets built, run the three
steps above and **remove its wanted stub** — a gap is tracked once, either as a want or as a
shelf item, never both.
