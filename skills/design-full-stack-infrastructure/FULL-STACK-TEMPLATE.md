# Full-Stack Infrastructure — {Project name}

*Reconciliation reflects the state of mid-2026; the two plane designs are dated by their own reports. This document carries only the **seam** between the planes — the shared-substrate reconciliation and the merged cost view. The plane designs themselves live in their own reports (referenced below) and are **not** restated here; read a plane's report for its band, its climb triggers, and its cost ladder.*

## 1. The full-stack brief

- **Goal (one sentence):** {the product — to be built with the coding plane, run on the product plane}
- **Shared inputs (held consistent across both plane briefs):** blast radius = {one assessment, fed to both} · budget = {total}, split {build arm $…} / {run arm $…} · tech stack / estate = {brownfield constraints binding both, incl. residency/compliance noted for veto checks}
- **Cross-feeds:** product plane's agent-readiness = {yes — the coding agents consume/operate the runtime / no — they never touch it} · coding plane's build-target stakes = {the product's blast radius, as fed}

## 2. The two plane designs (by reference)

| Plane | Designed by | Report | Recommended design (one line) |
|---|---|---|---|
| **Coding** (built *with*) | `design-agentic-infrastructure` | [{path}]({path}) — dated {date} | {its floor: rung + workflow + gate, one line} |
| **Product** (runs *on*) | `design-product-infrastructure` | [{path}]({path}) — dated {date} | {its floor: runtime + delivery + store, one line} |

> {If a pre-existing report was taken as input: note that its brief was checked against the shared inputs above — or the drift that forced a re-run.}

## 3. Shared-substrate reconciliation

Verdicts per [`RECONCILIATION.md`](RECONCILIATION.md) — sharing is the default candidate, a binding cap on either plane vetoes it, shared deployments are sized to the higher **justified** demand:

| Category | Product plane specified | Coding plane specified | Verdict | Size / sized-by | Owner | Re-reconcile when |
|---|---|---|---|---|---|---|
| Durable execution | {…} | {…} | {shared / separate (cap: …) / single-plane / absent} | {…} ← {plane} | {plane} | {trigger} |
| Datastore / memory | {…} | {…} | {…} | {…} | {…} | {…} |
| Observability | {…} | {…} | {…} | {…} | {…} | {…} |
| Flags / gates | {…} | {…} | {…} | {…} | {…} | {…} |
| Identity / policy | {…} | {…} | {shared **platform** — credentials never shared} | {…} | {…} | {…} |

**Vetoes, spelled out:** {each *separate* verdict with the cap that fired — e.g. "datastore: separate; blast-radius cap — coding agents hold no credential into the production store"}. *(None is a valid line — but say so.)*
**Identity note:** {the shared platform vs. per-actor scoped credentials — confirm no agent rides a human or service key}.

## 4. Merged cost view

Plane figures come from the plane reports' own ladders (their dates and assumptions apply); the only new arithmetic here is the dedup:

| Line | / period |
|---|---|
| Coding plane (build arm) — from its ladder | {$ range} |
| Product plane (run arm) — from its ladder | {$ range} |
| **Shared-substrate dedup** — {components counted once, at reconciled size, on owner's line} | −{$} |
| **Full-stack total** | **{$ range}** |

**The saving, honestly:** sharing saves {Δ / period} vs. running each plane's components unshared — driven by {which categories}. {Or: "nothing was shareable ({vetoed / single-plane}); the saving is zero — the value here is two consistently-designed planes and the vetoes on record."} The two arms stay separate lines because they burn differently — build cost moves with task volume, run cost with traffic — and de-escalate independently.

## 5. Recommendation

- **Start at both floors** — each plane's own report says why; nothing here overrides them.
- **Stand the shared substrate up once**, per the verdict table: {the shared deployments, their sizes, their owners}. The tenant plane connects with its own scoped credential.
- **Watch each plane's own climb triggers** (named in the plane reports). When one fires and touches a reconciled category, **re-open that row only** — resize to the new higher demand, or unshare if a new cap appeared. De-escalation re-opens rows too, checking the recorded dependency direction first.
- **Convenience is not evidence:** the standing trap is scope creep onto an "already running" shared deployment ({the likeliest instance here — e.g. agents acquiring production-store access}). Any new use of a shared component re-runs the four questions; it is never "just a key."

## 6. Faith check

- [ ] **Both planes designed whole by their own skills** — no plane doctrine restated or overridden here; each plane report stands alone and is referenced, not copied.
- [ ] **Reconciliation never out-escalated the evidence** — every shared size traces to a demand one plane justified in its recommended design; nothing sized "while we're at it."
- [ ] **Vetoes stated, not silent** — every *separate* names its cap; every *share* names its size, sizing plane, and owner.
- [ ] **Shared components billed once** — the dedup line lists them; no component appears in both a plane ladder and the merged view at full price; the saving (even zero) is stated.
- [ ] **The seam stays evidence-gated** — every reconciled row names the trigger that re-opens it, in both directions.
- [ ] **Credentials never shared** — identity may share a platform; every agent, human, and service carries its own scoped credential.

## 7. Sources

The plane designs carry their own **Sources (searched {date})** sections — tools and prices are theirs, re-validate there. This bridge adds {none / the following reconciliation-specific sources: …}. The five shared-substrate categories and the reconciliation doctrine are provenanced in the skill's [`SOURCES.md`](SOURCES.md) (a mid-2026 field capture; re-validate before relying on the anchors).
