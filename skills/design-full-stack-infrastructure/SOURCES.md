# Sources & provenance

This skill is a **bridge**: it composes two sibling plane skills and adds only the seam between them. It does not copy their doctrine — the band-of-three method, the matrices, the cost models, and the mechanism knowledge all stay in the siblings, single-sourced. This file records **what this bridge points to**, **what field evidence backs the seam it owns**, and **what is coined here and nowhere else** — so drift is detectable instead of silent.

> If a pointer below has moved or a claim no longer matches its source, the bridge is stale — re-validate and update this file.

## Provenance pins — the two plane skills

Validated: **2026-07-15** (both siblings read in full at that date; same repository, so the pin is the path + date rather than a cross-repo commit hash — drift shows up in this repo's own history).

| Source skill | Plane | What this bridge takes from it |
|---|---|---|
| [`../design-agentic-infrastructure`](../design-agentic-infrastructure/SKILL.md) | **Coding** — what the product is built *with* | The whole coding-plane design (band, cost ladder, climb triggers) as an input artifact; its report default `./agentic-coding-infrastructure-design.md`; its named components in the five substrate categories (durable state, memory, observability, HITL gate, identity). |
| [`../design-product-infrastructure`](../design-product-infrastructure/SKILL.md) | **Product** — what the product *runs on* | The whole product-plane design as an input artifact; its report default `./product-infrastructure-design.md`; its **shared-substrate flags** (its `AGENT-READY.md` requires each design to mark substrate candidates *for the bridge to reconcile* — that hand-off lands here); the five-category substrate table this bridge's `RECONCILIATION.md` extends. |

Both siblings live in this repository (not vendored — single source of truth stays in each skill's own directory).

```sh
# Has anything the bridge relies on changed since it was validated?
git log --oneline -- skills/design-agentic-infrastructure skills/design-product-infrastructure
```

If commits after 2026-07-15 touch either sibling's SKILL.md, MATRIX.md, or (product) AGENT-READY.md, re-read those files, fix this bridge if needed, and bump the validated date above.

**Also inherited through the siblings, not re-sourced here:** Evidence-Gated Escalation, the a-priori/a-posteriori evidence timings, band-not-point, and most-restrictive-cap-wins — coined in the upstream `agentic-coding` bridge (see its `SOURCES.md` § "Coined here") and carried by both siblings. This bridge applies them across planes; it does not re-coin them.

## Field evidence — WAD26 (mid-2026 market snapshot)

One field-evidence source — **WeAreDevelopers World Congress 2026** (Berlin, 2026-07-08/10; 492 sessions, ~98 booths; local capture `/Users/phuongnz/dev/WAD26`). Evidence grade: **market/practitioner signal** — many independent bets, stronger than single-vendor advocacy, still not a controlled benchmark. The durable part is the *dual-use pattern*, not any one product.

| Claim in this skill | WAD26 backing |
|---|---|
| The **five shared-substrate categories** exist — the same components genuinely serve both planes (`RECONCILIATION.md` § five categories) | Durable execution: Temporal as coding-plane checkpoint layer *and* product backend. Datastore/memory: Neo4j ("plug Neo4j into Claude Code & Codex") and Redis ("real-time context engine") as product stores *and* agent memory. Observability: OpenTelemetry spanning product traces and agent-run traces (GenAI conventions). Flags/gates: LaunchDarkly as release control *and* the gate on agent-shipped code. Identity/policy: the governance triad (authorization / attribution / auditability) applied to human, service, and agent actors alike. |
| **The gap this bridge fills** — no method exists for designing the two planes together (`SKILL.md` § why a bridge exists) | The congress's key negative finding: across 492 sessions and ~98 booths, no one offered a method for designing product infrastructure and coding infrastructure together — the coupling was visible everywhere (the rows above), the method nowhere. |
| Agents as runtime consumers make the seam load-bearing (the cross-feed in `SKILL.md` step 1) | "The agent is now the customer, not the product" (vendor-report conclusion); MCP-wrapped product APIs (Kong lineage). Detailed in the product sibling's `AGENT-READY.md` — pointed to, not restated. |
| Credential discipline on the shared identity platform (`RECONCILIATION.md` § identity) | "No keys for the robot" (GitOps control plane session); agent identity as first-class, distinct from human credentials (governance sessions). |

## Coined here, in neither sibling nor upstream

Flag these if you ever try to source them elsewhere — they originate in this bridge, constructed *on* the anchored material above (the same license the upstream `agentic-coding` bridge used to coin Evidence-Gated Escalation on its two anchored parents):

- **The reconciliation doctrine** — *"one deployment serves both planes, sized to the higher demand, unless a binding cap on either plane vetoes sharing."* WAD26 validates that the dual-use components exist; the decision rule for merging them is coined.
- **The four reconciliation questions** (both specify? → veto? → size to the higher *justified* demand? → who owns?) and the **verdict table** vocabulary (shared / separate+cap / single-plane / absent; sized-by; owner; re-reconcile-when).
- **The max-rung conflict rule with its two guardrails** — never above either plane's own justification; the ride-along is free capacity, not a new baseline.
- **Owner/tenant** framing for shared deployments — one owning plane whose operational posture governs; the other a tenant with a scoped credential and attributed load.
- **The full-stack decision flow** — split-brief with three shared inputs and two cross-feeds; design each plane whole and independent; reconcile; merge cost with the dedup line as the bridge's measurable value.
- **The "already running looks like already justified" trap** — convenience-driven scope creep onto a shared deployment named as the seam's standing false-confidence trap.

## What this skill deliberately does not have

No `MATRIX.md`, no `COST-MODEL.md`, no `TOOLS-REGISTRY.md`, no `INSTANTIATION-REGISTRY.md` — those exist per plane, in the siblings, and duplicating any of them here would fork doctrine the bridge exists to keep single-sourced. The bridge's only artifacts are the reconciliation and the merged cost view; everything else is a pointer.
