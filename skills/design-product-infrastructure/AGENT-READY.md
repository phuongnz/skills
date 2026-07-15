# Agent-ready infrastructure — designing for agents as consumers, and the shared substrate

*The design knowledge for the one dimension the coding-plane sibling has no analog for: **is this product's runtime ready to be consumed and operated by agents?** Field-captured as of mid-2026 (WeAreDevelopers World Congress 2026), where "the agent is now the customer, not the product" was a recurring vendor conclusion. Consult it the way step 6 consults `COST-MODEL.md`; fetch live gateway / identity tools at SKILL step 5. Re-validate before relying on it — the field moves.*

This file does two jobs: (1) it defines the **agent-readiness dimension** — a design surface that appears when the answer to the intake question *"will agents consume or operate this infrastructure?"* is **yes**; and (2) it marks the **shared substrate** — the handful of components that serve *both* the product runtime and the coding plane, so one deployment can serve both instead of two.

## The shift: the agent is a consumer, not just an operator

For most of software history the consumer of a product's API was a human-driven client — a browser, a mobile app, another service written by a person. The field's mid-2026 signal is that a growing share of consumers are **agents**: the user's own coding agents calling the product's APIs, or external agents integrating the product into a larger workflow. "The agent is now the customer, not the product" — the runtime that only speaks to human-driven UIs is missing a consumer class.

This is a **dimension, not a tier**: it doesn't move a design up the runtime band, it adds surfaces *across* the band. Answer the intake question first — **if no agent will consume or operate the runtime, this whole file is out of scope for that design, and saying so is a complete answer.** When it *is* in scope, three surfaces appear.

### 1. MCP-wrapped APIs — the agent-facing contract

An agent consumes an API differently from a UI: it needs machine-discoverable capabilities, typed inputs/outputs, and stable semantics. The field's convergence is on **MCP (Model Context Protocol)** as the open standard for exposing a product's capabilities to agents — an API gateway that speaks MCP (e.g. Kong's MCP gateway lineage) turns existing product APIs into agent-callable tools without a rewrite. Design note: expose the *capability*, not the raw endpoint surface — an agent tool is a bounded, typed action with clear side-effect semantics, not a thin proxy over every REST route. Favour the open standard (*open protocols outlive products*) so the agent contract survives a vendor change.

### 2. Agent identity at the edge — a first-class, non-human credential

An agent acting on the runtime is **not** a human, and must not borrow a human's credential. It carries its **own identity** — a distinct, policy-scoped credential — so the governance triad holds at the product edge:

- **Authorization** — *is this agent allowed to call this?* A scope enforced by policy, independent of what the agent attempts. "No keys for the robot": an agent gets a scoped, auditable credential, not a shared master key.
- **Attribution** — *which agent did this?* Every call traces to a specific agent identity, distinct from the human who deployed it.
- **Auditability** — *can you prove what the agent did?* A durable record of agent actions on the runtime.

This is the same triad the release gate and HITL enforce, now applied to **runtime API access by non-human actors**. As agents become consumers, this cap *rises in force* — an ungoverned agent consumer is a larger blast radius than an ungoverned human one, because it acts faster and at scale.

### 3. Flags-as-gates — the runtime hold on an agent's action

When an agent's action reaches production — an agent shipping code, or an agent-driven feature changing runtime behavior — the **feature flag is the runtime human-in-the-loop**: the action deploys dark, and a human (or a policy) flips exposure. This is the same flag mechanism the release gate uses (see [`RELEASE-GATES.md`](RELEASE-GATES.md)); here it is the seam where an *agent's* output meets the *product's* users, held behind a reversible gate until authorized.

## The shared substrate — components that serve both planes

The congress's key negative finding: across 492 sessions and ~98 booths, **no one offers a method for designing product infrastructure and coding infrastructure together** — yet several components legitimately serve *both*. When the same product also has an agentic *build* plane (the sibling skill `design-agentic-infrastructure`), these are candidates for **one deployment, sized to the higher demand**, not two:

| Substrate category | Serves the product plane as… | Serves the coding plane as… | Field anchor |
|---|---|---|---|
| **Durable execution** | long-running product workflow backbone | the checkpoint layer coding agents pause/resume on | Temporal |
| **Datastore / memory** | a product datastore (graph / real-time) | agent memory / real-time context store | Neo4j, Redis |
| **Observability** | product SLOs & traces (OTel) | agent run-trace observability (OTel GenAI) | OpenTelemetry |
| **Flags / gates** | release exposure control | the runtime gate on agent-shipped code | LaunchDarkly |
| **Identity / policy** | authorization on privileged product actions | agent identity + policy for the build plane | governance triad |

**What this file does with the overlap: flag it, don't reconcile it.** When you specify one of these components for the product plane, note that it is a shared-substrate candidate — so it isn't stood up twice if the coding plane also needs it. The *reconciliation* — deciding the single sizing that serves both, resolving a floor-on-one-plane against a ceiling-on-the-other — is **not this skill's job**. That is the job of the **full-stack bridge** — [`design-full-stack-infrastructure`](../design-full-stack-infrastructure/SKILL.md) — that composes the two plane skills: it owns the reconciliation, in its `RECONCILIATION.md` (one deployment serves both, sized to the higher demand). Each plane is designed whole on its own here; the bridge reconciles the seam when the user needs both planes together.

## Cross-check the cost line

An agent-ready surface adds modest lines: an MCP-capable gateway (managed-service fee), an identity/policy layer for non-human actors, and audit storage. A shared-substrate component counts **once** across both planes when reconciled — don't double-bill it. Cross-reference `COST-MODEL.md`'s managed-service-fees line.

## What the design must state (the checkpoint)

For the agent-readiness dimension of each design **where agents are in scope**:

1. **The agent-facing contract** — which capabilities are MCP-wrapped (typed, bounded actions), or an explicit "no agent consumers — out of scope."
2. **Agent identity** — the scoped, non-human credential and its policy scope; never a shared human key.
3. **The runtime gate** — where an agent's action is held behind a flag until authorized.
4. **Shared-substrate flags** — which specified components are candidates to serve the coding plane too (for the bridge to reconcile), so nothing is duplicated.

**Floor default:** **no agent consumers ⇒ this dimension is out of scope**, and stating that is a complete design. When agents *are* consumers, the identity + governance triad on their access is a **cap**, present on the floor — an ungoverned agent consumer is not the cheap design, it is the broken one.
