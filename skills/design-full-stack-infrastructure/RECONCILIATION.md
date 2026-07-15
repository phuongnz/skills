# Shared-substrate reconciliation — one deployment or two, and the size when one

*The design knowledge this bridge owns: how to reconcile the components that serve **both** the coding plane and the product plane. The five categories and their field anchors are captured **as of mid-2026** (WeAreDevelopers World Congress 2026 — see [`SOURCES.md`](SOURCES.md)); the reconciliation doctrine is coined by this bridge on those anchors. Consult this file at SKILL step 3; re-validate the anchors before relying on them — the field moves.*

**The doctrine in one line: one deployment serves both planes, sized to the higher demand — unless a binding cap on either plane vetoes sharing.** Everything below is the working-out of that line: which components qualify, how the single size is chosen, what vetoes look like, how the cost is counted, and how the decision stays evidence-gated after it's made.

## Why reconcile at all

Each plane's skill designs its plane **whole**, blind to the other — that independence is a feature (each band is justified by its own evidence, nothing is pre-trimmed to "leave room"). The price of that independence is a seam: both designs may specify a durable-execution backbone, a fast key-value store, an observability stack, a flag system, an identity layer — **the same five categories, twice**. Unreconciled, the user stands up and operates two of each. Naively merged, one plane's floor silently inherits the other's ceiling ("we already run multi-region Temporal for the product, so the coding agents get multi-region checkpointing nobody asked for" — an un-evidenced climb wearing a thrift costume). Reconciliation is the disciplined middle: **share where nothing forbids it, at exactly the size the more demanding plane already justified.**

## The five categories

The categories where one component legitimately serves both planes — with what each plane uses it *as*, and the mid-2026 field anchor that validated the dual use:

| Category | The product plane runs it as… | The coding plane runs it as… | Field anchor (mid-2026) |
|---|---|---|---|
| **Durable execution** | the long-running product-workflow backbone | the checkpoint layer agents pause/resume on | Temporal serving both |
| **Datastore / memory** | a product datastore (graph · real-time KV) | agent memory / real-time context store | Neo4j, Redis serving both |
| **Observability** | product traces + SLOs (OTel) | agent run-traces (OTel GenAI) | OpenTelemetry, one spec both planes |
| **Flags / gates** | release exposure control | the runtime gate on agent-shipped code | LaunchDarkly serving both |
| **Identity / policy** | authorization on privileged product actions | agent identity + policy on the build plane | the governance triad, one layer |

Two boundary notes. **A category present on only one plane needs no reconciliation** — it's a plane-internal component; record it as *single-plane* and move on. And **the categories are fixed but the tools are not**: the anchors above are a dated snapshot; the tools actually specified come from each plane's own live step-5 search, and reconciliation operates on whatever they found — two different tools in the same category (say, Temporal on one plane, a cloud-native workflow service on the other) are still one reconciliation decision: converge on one, or keep both with the veto/verdict stated.

## The reconciliation, category by category

For each of the five categories, walk four questions **in order**:

### 1. Do both planes specify it?

Pull the components from the two **recommended designs** (normally both floors) — the product report flags its shared-substrate candidates explicitly (its `AGENT-READY.md` checkpoint requires it); the coding report names its durable-state, memory, observability, gate, and identity choices in its design sections. Both present → continue. One present → *single-plane*, done.

### 2. Does anything veto sharing?

Sharing is the **default candidate, not a mandate**. Re-read both planes' **binding caps** (each report's constraint-translation section); a cap on *either* plane vetoes the share — **most-restrictive-cap-wins**, the same tie-break both siblings use, applied across planes:

- **Residency / compliance isolation** — the product's data may not live in, or be traversable from, an estate the coding agents roam (or vice versa). One store cannot serve both → two deployments.
- **Blast-radius separation** — the sharpest veto, and the default posture for the **datastore** category: coding agents with a credential into the *production* datastore turn every agent mistake into a production incident. Share the *platform* only if the isolation boundary inside it is real (separate database/namespace, separate scoped credentials, no cross-grant); when in doubt, separate.
- **Availability coupling** — if the product's SLO makes the component's outage a user-facing incident, sharing means coding-plane load and coding-plane maintenance windows now sit inside the product's error budget. Share only if the product plane's operational posture (its SLO and on-call) becomes the shared deployment's posture.

A veto is a **verdict, not a failure**: record *separate*, name the cap that fired, and count both deployments in the cost. An unstated veto is the failure.

**The identity category has a special shape.** What's shared is the identity *platform and policy layer* — one place to answer *allowed? which actor? provable?* for humans, services, and agents alike. What is **never shared are the credentials**: each agent carries its own scoped, non-human credential, distinct from every human's and every service's — "no keys for the robot" means no *shared* keys most of all. A reconciliation that merges identity by handing the coding agents a product-service credential has not shared the substrate; it has broken the governance triad on both planes at once.

### 3. Shared — at what size?

**Size to the higher demand**: compare the two planes' specifications for the category — tier, redundancy, capacity, durability posture — and the shared deployment takes the **max rung** across them. The floor/ceiling conflict resolves the same way: if the product's recommended design needs the category at a rung the coding plane's doesn't (or vice versa), the shared deployment is built at the **higher** of the two — the lower-demand plane rides along on capacity the other plane already justified.

Two guardrails keep this evidence-gated:

- **Never above either plane's justification.** The max is taken over what the planes *actually specified in their recommended designs* — not over their ceilings, not over "while we're at it." If neither plane's evidence justified multi-region, the shared deployment is not multi-region. Sharing changes how many deployments exist, never how heavy one is.
- **The ride-along is free capacity, not a new baseline.** The lower-demand plane must not start *depending* on the higher rung (the coding plane discovering it "needs" the product's multi-region durability is a climb, and needs that plane's own a-posteriori evidence). Note the dependency direction in the verdict so a later de-escalation on the demanding plane isn't blocked by silent load from the other.

**Capacity is additive even when the rung isn't.** Two planes on one deployment means summed load — size the throughput/storage for both planes' volumes at the reconciled rung, and attribute each plane's share so the cost split (and a future unshare) stays computable.

### 4. Who owns it?

Every shared deployment gets **one owning plane** — the one whose demand set the size (in practice almost always the product plane, whose SLO and on-call are stricter). The owner's operational posture governs: its backup/restore discipline, its maintenance windows, its access policy. The other plane is a **tenant** with a scoped credential and an attributed slice of load. A shared component with two owners has none — that's how the untested-restore and the ungoverned credential sneak back in.

## The verdict table

Step 3's output — one row per category:

| Category | Product plane specified | Coding plane specified | Verdict | Size / sized-by | Owner | Re-reconcile when |
|---|---|---|---|---|---|---|
| {category} | {component + rung, or —} | {component + rung, or —} | **shared** · **separate (cap: {…})** · **single-plane** · **absent** | {reconciled size} ← {plane} | {plane} | {the climb trigger(s) that re-open this row} |

## Cost: counted once, saving stated

A shared component is billed **once**, at the reconciled size, on the owning plane's side of the merged view — with the tenant plane's load share noted. The merged cost view (SKILL step 4) then shows the **dedup saving**: what the same two designs would cost unshared minus the reconciled total. That number is the bridge's measurable value — state it even when it's small, and state it *especially* when it's zero (all categories vetoed or single-plane), because "nothing shareable, here's why" is a sound outcome, not a failed one. Never double-bill a shared line in both plane ladders and the merged view; never hide a veto's cost (two deployments) to make the merge look better.

## The seam stays evidence-gated

Reconciliation is an **a-priori** act — performed at design time on the two recommended designs. It does not freeze:

- **A plane climbs** → whichever plane's a-posteriori evidence fires a climb trigger touching a reconciled category **re-opens that row** (only that row): the max may move, the shared deployment resizes to the new higher demand.
- **A plane de-escalates** → the arrows run down here too. If the demanding plane steps down a rung, the shared deployment may follow — *checking first* whether the tenant plane silently grew into the higher rung (that's why the verdict records the dependency direction).
- **A veto can appear or dissolve** — a new compliance requirement can force an unshare; a retired constraint can make a share newly possible. Either way, the change is a dated re-run of the four questions for the affected category, not an ad-hoc patch.

## The trap this file exists to catch

**"Already running" looks like "already justified."** The moment one plane operates a capable deployment, every need on the other plane gravitates toward it — *we have Temporal anyway; we have a graph store anyway; just give the agent a key to prod, it's faster.* Each of those is an un-evidenced escalation (of scope, of access, of blast radius) disguised as thrift. The discipline: sharing is decided **by this file's four questions, per category, with the verdict written down** — never by convenience at integration time. If a share can't name the cap-check it passed and the plane whose evidence sized it, it isn't reconciled; it's drift.
