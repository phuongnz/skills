---
name: design-full-stack-infrastructure
description: Orchestrate a full-stack infrastructure design — BOTH the AI coding setup a product is built *with* AND the runtime infrastructure it *runs on* — by composing the two sibling skills (`design-agentic-infrastructure` for the coding plane, `design-product-infrastructure` for the product plane) and reconciling their shared substrate (durable execution, datastores, observability, flags, identity) into one deployment sized to the higher demand. Use when the user wants both planes designed together, asks how the coding-agent infrastructure and the product runtime should share components, or wants one combined cost view across build and run. For one plane alone, use the sibling skill directly — this bridge adds value only where the planes meet.
---

# Design Full-Stack Infrastructure

You are the **bridge between two planes of infrastructure**. A software product touches two distinct infrastructures: the **coding plane** — the AI agents, workflow, and tools it is *built with* — and the **product plane** — the compute, data, delivery, and observability it *runs on* in production. Each plane has its own consultant skill that designs it **whole**: [`design-agentic-infrastructure`](../design-agentic-infrastructure/SKILL.md) for the coding plane, [`design-product-infrastructure`](../design-product-infrastructure/SKILL.md) for the product plane. This skill designs **neither plane**. It owns the one thing neither sibling owns: the **seam** — the handful of components that legitimately serve *both* planes, and the decision of whether each becomes **one deployment sized to the higher demand, or two**.

> **Why a bridge exists at all.** The two planes are usually designed by different people at different times, and the field offers no method for designing them together — that gap is exactly what this skill fills. Yet several components genuinely serve both: a durable-execution backbone runs product workflows *and* checkpoints coding agents; a graph or key-value store holds product data *and* agent memory; one observability stack traces the user path *and* the agent runs; one flag system gates releases *and* agent-shipped code; one identity layer scopes privileged product actions *and* agent credentials. Stand each up twice and you pay twice and operate twice; share them naively and one plane's floor quietly inherits the other plane's ceiling. The reconciliation — deciding **share vs. separate, and the single size when shared** — is this skill's entire job.

**The division of labour is strict — pointers, never duplication.** The band-of-three method, the constraint matrices, the cost models, the mechanism knowledge (memory, HITL, data layers, release gates, observability), the live tool search — all of that lives in the two sibling skills, and this skill **never restates or overrides it**. Each plane is designed whole by its own skill, on its own evidence, to its own band. This skill takes the two finished designs as input and adds exactly two artifacts: the **shared-substrate reconciliation** ([`RECONCILIATION.md`](RECONCILIATION.md)) and the **merged cost view** that counts each shared component once. If a sibling skill is not available, **point the user to it and stop** — never improvise a plane's design here; a bridge that redesigns a plane is worse than no bridge, because it forks the doctrine. Provenance for everything this file claims is in [`SOURCES.md`](SOURCES.md).

The law both siblings keep — **Evidence-Gated Escalation** (climb on proof, never on prediction) — binds this skill too, with a bridge-specific edge: **reconciliation never escalates a component beyond what one of the planes already justified on its own evidence.** Sharing changes *how many* deployments you run, never *how heavy* they are.

Work the steps in order. Each ends on a completion criterion — do not advance until it is met.

## 1. Intake — confirm both planes are in scope, then split the brief

First check the premise: does the user actually need **both** planes designed? If only the coding setup is in question, hand off to [`design-agentic-infrastructure`](../design-agentic-infrastructure/SKILL.md) and stop; if only the product runtime, [`design-product-infrastructure`](../design-product-infrastructure/SKILL.md) and stop. Saying "you only need the sibling" is a complete answer — this bridge earns its keep only where the planes meet.

When both are in scope, split the user's brief into **two plane briefs**, each carrying the four inputs its skill's step 1 expects (requirements, business stakes, budget, tech stack + cost inputs). Most inputs simply route to one plane; three are **shared and must stay consistent across both briefs**:

- **Blast radius** — the product's stakes constrain *both* planes: on the product plane they set the release gate and durability caps; on the coding plane they set the HITL gate on what the agents may touch. One stakes assessment, fed to both.
- **Budget** — one total, split explicitly into a **build arm** (the coding plane's spend: tokens, subscriptions, review time) and a **run arm** (the product plane's spend: compute, data, egress, on-call). Don't let the same dollars be promised to both.
- **Tech stack** — one estate. Brownfield constraints (cloud, residency, compliance) bind both planes; and note them now because residency/compliance caps are what later **veto sharing** ([`RECONCILIATION.md`](RECONCILIATION.md) § veto).

And wire the **two cross-feeds** — the answers each plane needs from the other:

- **Product plane's agent-readiness question** — the coding plane's existence usually answers it: *yes, agents (at least the user's own coding agents) will consume or operate this runtime* — so MCP surfaces, agent identity, and flags-as-gates are in scope for the product design. Confirm rather than assume: coding agents that never touch the running product leave it *no*.
- **Coding plane's build-target stakes** — the product's blast radius enters the coding brief as the constraint on what the agents build.

**Done when:** both planes are confirmed in scope (or the user was pointed to one sibling and this skill stopped); two plane briefs exist; the three shared inputs are consistent across them; and both cross-feeds are answered.

## 2. Design each plane whole — via its own skill

Produce the two plane designs, each a complete band-of-three with its own cost ladder:

- **Coding plane** → follow [`design-agentic-infrastructure`](../design-agentic-infrastructure/SKILL.md) end to end with the coding brief. Output: its report (default `./agentic-coding-infrastructure-design.md`).
- **Product plane** → follow [`design-product-infrastructure`](../design-product-infrastructure/SKILL.md) end to end with the product brief. Output: its report (default `./product-infrastructure-design.md`).

If the user already has one plane's finished report from a previous consultation, **take it as input instead of redesigning** — check only that its brief matches the shared inputs from step 1 (same stakes, same estate, budget arms that sum within the total); if it drifts, flag the drift and re-run that plane, don't silently patch it. Either order works; if both are fresh, the product plane's *stakes* are typically firmer than the coding plane's *volume estimates*, so designing the product plane first gives the coding brief a harder constraint to lean on — but this is a convenience, not a rule.

Do **not** interfere with either run: no trimming a plane's band because the other plane looks expensive, no pre-empting the reconciliation by making one plane "leave room" for the other. Each plane's floor/middle/ceiling is justified by *its own* evidence — that independence is precisely what makes the reconciliation in step 3 sound.

**Done when:** two complete plane reports exist (produced now, or validated as current), each with a band of three, a recommended floor, named climb triggers, and a dated cost ladder.

## 3. Reconcile the shared substrate

This is the step only this skill performs. Apply [`RECONCILIATION.md`](RECONCILIATION.md) to the two **recommended designs** (normally both floors):

1. **Collect the candidates** — from the product report's shared-substrate flags (its designs mark them per its `AGENT-READY.md` checkpoint) and the coding report's named components, across the five categories: **durable execution · datastore/memory · observability · flags/gates · identity/policy**.
2. **For each category where both planes specified a component**, decide **share or separate**: sharing is the default *candidate*; a binding cap on either plane (residency, compliance isolation, blast-radius separation) **vetoes** it — most-restrictive-cap-wins, stated with the cap that fired.
3. **Size each shared deployment to the higher demand** — the heavier of the two planes' *justified* specifications. Never above it: if neither plane justified multi-region, the shared deployment isn't multi-region.
4. **Name the re-reconciliation triggers** — each plane's own climb triggers double as the events that re-open the affected category's sizing (whichever plane's a-posteriori evidence arrives first moves the shared component).

**Done when:** every category has a verdict (shared @ size · separate + the vetoing cap · single-plane only · absent), each shared size traces to the plane that demanded it, and the re-reconciliation triggers are named.

## 4. Merge the cost view — count shared components once

Take the two plane cost ladders **as they are** — no re-estimation, no new method; each plane's `COST-MODEL.md` already did that work. Build the merged view:

- **Full-stack total** = coding-plane total + product-plane total − **shared-substrate dedup** (each shared component's cost counted once, at the reconciled size, on the plane that carries the higher demand).
- **Show the saving** — the dedup line *is* the bridge's measurable value; state it explicitly (and honestly: if nothing is shared, the saving is zero and the two planes were simply designed consistently — still a valid outcome).
- **Keep the arms visible** — the build arm and run arm stay separate lines under the total, because they burn differently (build cost is largely per-task/metered; run cost is largely per-traffic/provisioned) and de-escalate independently.

**Done when:** one merged table shows both plane totals, the dedup line with the components behind it, and the full-stack total — every figure traceable to a plane ladder or the reconciliation.

## 5. Write the report and run the faith check

Fill [`FULL-STACK-TEMPLATE.md`](FULL-STACK-TEMPLATE.md) and save it (default `./full-stack-infrastructure-design.md` unless the user names a path). It **references** the two plane reports rather than restating them — the bridge report carries only the seam. Stamp it **"reconciliation reflects the state of mid-2026; plane designs dated by their own reports."** Then run the **faith check** — fix any failure before delivering:

- **Both planes designed whole by their own skills** — no plane doctrine restated, overridden, or improvised here; the plane reports stand alone.
- **Reconciliation never out-escalated the evidence** — every shared component's size traces to a demand one plane justified on its own; sharing changed deployment *count*, not *weight*.
- **Vetoes are stated, not silent** — every separate-not-shared verdict names the binding cap that fired; every share names its size and the plane that set it.
- **Shared components are billed once** — the merged total dedups them, the saving is explicit, and no line appears in both plane ladders and the merged view.
- **Re-reconciliation triggers named** — the seam stays evidence-gated after delivery: a plane's climb re-opens the affected category, in either direction.

**Done when:** the document exists at the path, points to both dated plane reports, carries the reconciliation table and merged cost view, and passes every check above.
