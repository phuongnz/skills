# Data & state layer — how to design where the product's state lives

*The design knowledge, so the skill never defaults to a shallow datastore recommendation — it decides the data layer from evidence here, and fetches only live datastore **tools/prices** at SKILL step 5. Field-captured as of mid-2026; re-validate before relying on it — the field moves.*

The data layer is a **step-4 runtime facet** (the "data & state" line of each design). Consult this the way step 6 consults `COST-MODEL.md`: it carries the *how*, so the store is reasoned from the data's shape — **not** hand-waved to "use the biggest managed database." That default is the trap this file exists to prevent (see *The scalability illusion* below); it is also the exact face of the faith-check trap **"a managed platform *looks like* scalability."**

## The store is a decision from the data's shape, not a default

The single most common bad recommendation is *"reach for the managed relational DB you always use"* regardless of what the data actually is. Pick the store from the **access pattern and shape**, not habit:

| Data shape | Store flavour | Reach for it when |
|---|---|---|
| Transactional, relational, needs consistency | **Relational** (Postgres/MySQL lineage; TiDB for scale-out) | the default for state with invariants — start here unless the shape says otherwise |
| Document / flexible schema, high write throughput | **Document / wide-column** | schema churns, or writes dominate and joins don't |
| Relationships / graph traversal, change-over-time | **Graph** (Neo4j) | the *relationships* are the query, not a side-effect — not merely "it has connections" |
| Key/value, sub-ms, ephemeral or cache | **In-memory** (Redis) | a cache, a session store, a rate-limit counter, a real-time context store |
| Append-heavy events / metrics over time | **Timeseries / columnar** (ClickHouse, MotherDuck lineage) | analytics, telemetry, event history — not an OLTP path |
| Semantic similarity / embeddings | **Vector** | retrieval for an AI feature — often *alongside* the primary store, not instead of it |
| Search over text | **Search index** (OpenSearch) | full-text / faceted queries the primary store serves badly |

Do **not** collapse "my data is important" into "the biggest managed instance." A product usually needs **one primary store matched to its shape**, plus — only when evidence demands — a cache and/or a secondary store for a genuinely different access pattern. Polyglot persistence is a climb on proof, not a floor default.

## The two properties every stateful design must state

- **Durability** — does this state survive a crash / restart / zone failure? Anything whose loss costs money, safety, or user trust is a **cap**: it needs **backups + a *tested* restore path** (an untested backup is a hope, not a backup) and, for stateful/long-running work, **checkpointing** so a job resumes rather than restarts. This is the non-negotiable "durable state survives failure."
- **Consistency & the single writer of record** — for each piece of state, one authoritative owner. Distributing writes across replicas without a clear writer of record is how you get split-brain and lost updates. Read replicas fan out *reads*; the write path stays single-owner unless you have deliberately designed (and can operate) multi-writer consistency.

## Start with the fewest stores. A datastore is a standing cost, not free capacity

The floor is the **smallest set of stores the shape requires** — usually **one primary store** (plus a cache only if the read path already demands it a-priori). Every store you add is a standing bill *and* a standing operational burden (backups, migrations, failover, its own on-call). Add a second store only on **a-posteriori** evidence:

- **Cache tier** — climb when p95/p99 read latency breaches the SLO or the origin DB is the proven bottleneck. Order of operations: **cache the hot read path first**, then a read replica, *then* a bigger primary — the cheap origin-offload move before the expensive one. (A cache *looks like* scale but trades correctness for latency — govern staleness; see the caching caveat in `COST-MODEL.md`.)
- **Read replica** — climb when reads saturate the primary after caching. Adds standing DB cost + replication egress.
- **Sharding / partitioning** — climb only when a single primary can't hold the write volume or data size, and you can operate the added complexity. The last resort, not a starting posture.
- **De-escalation runs too:** a replica or secondary store that sits near-idle isn't earning its standing cost — remove it.

## The scalability illusion — why a managed platform is not "free scale"

**Provisioning a large managed database, or an autoscaling compute tier, is not the same as having headroom.** The bottleneck of a product under load is almost never raw compute — it is the **query pattern** (an N+1, a missing index, a full-table scan), the **single-writer contention**, or the **connection pool**. Scaling the box up hides the symptom and multiplies the bill while the real limit is untouched.

So the design rule: **the data layer's scale story is the *access pattern*, not the instance size.** Before pricing a bigger tier, name:

- the **hot queries** and whether they're indexed / cached,
- where the **single writer** contends,
- what the **connection / pool** ceiling is.

A design that answers "how does it scale?" with "we'll use a big managed instance" has fallen for the illusion. The honest answer names the access pattern that would break first and the cache/replica/shard move — gated on evidence — that relieves it.

## The shared-substrate overlap (with the coding plane)

Some stores serve **both** planes: **Neo4j** and **Redis** appear at the congress as agent-memory / real-time-context stores *and* as ordinary product datastores; a **durable-execution backbone** (Temporal) is a product state substrate *and* the checkpoint layer coding agents pause on. When the same product also has an agentic *build* plane (the sibling skill), one deployment can serve both — sized to the higher demand. That reconciliation is the full-stack bridge's job; here, just **flag** when a store you're specifying is a shared-substrate candidate, so it isn't stood up twice. See [`AGENT-READY.md`](AGENT-READY.md).

## Cross-check the cost line

A single primary store is a real but modest standing line; each added tier (cache node, read replica, second store) adds its own instance/ops + storage + backup + replication-egress cost. Only price a tier the design actually runs — cross-reference the **data tier** line in `COST-MODEL.md`.

## What the design must state (the checkpoint)

For the data/state facet of each of the three designs, name:

1. **The primary store and why** — matched to the data's shape, not habit; the fewest stores the shape requires.
2. **Durability** — backups + a tested restore path for anything whose loss has a cost; checkpointing for stateful/long-running work.
3. **The single writer of record** — who owns writes; where reads fan out to replicas (if any).
4. **The climb trigger to the next store/tier** — the specific a-posteriori evidence (read latency breaching SLO, write saturation) that would add a cache/replica/shard, and the cheaper origin-offload move tried first.
5. **Shared-substrate flag** — whether any store is a candidate to serve the coding plane too (so it isn't duplicated).

**Floor default:** one primary store matched to the shape, backups if maintained, no cache/replica until read evidence demands it — and that is a *complete* data design for most low-traffic and prototype products, not an omission.
