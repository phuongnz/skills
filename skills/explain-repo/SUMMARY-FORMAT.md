# Summary Format (`SUMMARY.md`)

`SUMMARY.md` is the distilled, parse-friendly file a *future agent* reads to bootstrap on the repo — the atlas compressed to roughly one screen. It is a distillation of the findings and chapters, not new investigation. It doubles as a `CLAUDE.md` seed (offered, never auto-applied).

Plain `.md`, never wrapped in HTML — the developer navigates the atlas; this file is for an agent (or a developer who wants the dense version).

## Template

```md
# {Repo} — Agent Summary

> As-of `abc1234` (2024-03-15) · remote {url} · visibility {public|private}

## What it is
{One paragraph: purpose, who it's for, maturity.}

## Run it
```
{install}
{build}
{test}
{run}
```

## Architecture
- {≤8 bullets: the layering, the boundaries, the one end-to-end flow.}

## Functional blocks
| Block | Path | Responsibility |
|-------|------|----------------|
| {name} | `dir/` | {one line} |

## Key abstractions
- {≤5 must-know types/concepts, each with where it lives.}

## Conventions & gotchas
- {The things that bite: naming rules, required setup, footguns, non-obvious wiring.}

## Where things live
- {Task} → {path}
- Add an endpoint → `...`  ·  Add a test → `...`  ·  Config → `...`

## Weak spots
- {Fragile / under-tested / risky areas, each grounded — carried over from chapter 7.}

## Open questions
- {Unverified or unknown — what a deeper pass or a maintainer should confirm.}
```

## Rules

- **Dense over complete.** This is the highest-value facts, not the whole atlas. If it runs past ~one screen plus tables, it's doing the chapters' job.
- **Copy-pasteable commands.** The run block must be runnable, drawn from verified scripts — not idealised.
- **Carry the as-of stamp.** The first line is the commit it was built against; a summary without it cannot be trusted as current.
- **Stay grounded.** Every weak-spot and gotcha traces to a chapter/finding that cited it. Don't introduce uncited claims here that the atlas doesn't back.
- **Refresh with the atlas.** When chapters go stale and are re-investigated, regenerate this from the updated findings.
