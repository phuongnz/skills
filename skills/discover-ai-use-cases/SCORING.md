# Scoring & Prioritization

Turn the matched candidates into a ranked shortlist on **two axes — Impact × Feasibility** — then plot them. This structure is convergent across the major frameworks (OpenAI's impact/effort quadrant, Google's value-vs-feasibility, the Action Priority Matrix, and the Stanford WORKBank desire-vs-capability zones). The top-right quadrant is the **low-hanging fruit**.

Score each candidate, then run the **honesty checks** — they are what keep this from becoming a hype generator.

## Impact (score 1–5)

Impact ≈ **frequency × time-per-instance × pain**. Use the markers from Stage 3.

| | 1 (low) | 3 (medium) | 5 (high) |
|---|---|---|---|
| **Frequency** | monthly or less | weekly | daily / many times a day |
| **Time per instance** | minutes | ~30 min | hours |
| **Pain (markers)** | 0–1 markers, mildly annoying | 2–3 markers | 4+ markers / actively dreaded or stressful |

Take a holistic 1–5 (don't just average — a tiny task done constantly is high-impact; a rare task is rarely worth it). **Annualized time saved** is the sanity check: `frequency_per_year × minutes_saved_per_instance`. A 5-min task done 10×/day ≈ 200+ hours/year; a 2-hour task done quarterly ≈ 8 hours/year. Frequency usually wins.

## Feasibility (score 1–5)

Can AI actually do this *well and safely* for this person, today?

| Factor | Lowers feasibility | Raises feasibility |
|---|---|---|
| **Inputs available** | data is in someone's head / locked away | inputs are text/files the person can hand over |
| **Rules clear** | fuzzy, "I just know" judgment | a clear "good output looks like X" |
| **Blast radius if wrong** | irreversible, public, money/legal | private draft, easily reviewed |
| **AI-suitability** | needs real-world action or live human relationship | language/data transformation, drafting, synthesis |

Take a holistic 1–5. A high-impact task with feasibility 1–2 is a **flag, not a start**.

## Plot the quadrant

| | **High feasibility** | **Low feasibility** |
|---|---|---|
| **High impact** | 🟢 **Quick Win** — start here | 🟡 **Project / flag** — worth it, needs setup or better inputs |
| **Low impact** | ⚪ **Fill-in** — nice-to-have, mention only | 🔴 **Skip** |

Lead the report with the **Quick Wins** (typically 2–3). Flag the projects so they're not lost. Drop the rest.

## Honesty checks (apply before ranking)

The research is emphatic that perceived gains overstate real ones. Enforce these:

1. **No hype/refuted stats.** Do not justify a use case with marketing numbers. Specifically, these were fact-check **refuted** and must never appear: "Copilot cuts email time 25%," "sales AI agents give 25–47% gains," "you spend 50% of the time managing the AI." Avoid blanket multipliers ("10× productivity").

2. **Calibrated expected value, not headlines.** State a credible *range* tied to the task: "this ~30-min task, done daily — realistically 10–20 min saved each time once set up." The honest anchors: self-reported gen-AI time savings run ~5% of work hours (~a couple hours/week); per-task self-estimates run far higher but are unverified. Prefer "you'll review output instead of producing it from scratch" over a percentage.

3. **Watch where AI reliably hurts.** The one rigorous RCT (METR) found experienced people in a *mature, already-optimized* personal workflow can be *slower* with AI while feeling faster. If a candidate is "expert + mature workflow + fast-moving judgment," down-rank it or attach an explicit "measure your own before/after — this may not pay off" caveat. Don't put it in the Quick Wins unframed.

4. **Augmentation ≠ less value, but ≠ time saved either.** For augmentation cases (decision support, analysis), express value as *better quality / fewer misses*, not minutes. Don't inflate these with time-savings claims.

5. **Set-up cost counts.** Feasibility already captures it, but say it plainly: a Quick Win should pay back its setup within days, not months. If it won't, it's a Project.

## Output of this stage

For each candidate: **impact (1–5), feasibility (1–5), quadrant, calibrated expected value**, and automation-vs-augmentation. The Quick Wins, in order, lead the report.
