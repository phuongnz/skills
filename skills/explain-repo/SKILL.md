---
name: explain-repo
description: Build a durable, navigable atlas of a code repository — structure, functional blocks, tech stack, history, CI/CD, strengths and weaknesses, and a "continue development" playbook — plus a distilled summary that bootstraps a future agent. Use when the user wants to understand, onboard to, document, take over, or keep building an unfamiliar codebase, asks for a repo overview / architecture map / codebase walkthrough, or wants to find good issues and PRs to contribute to a public repo.
---

# Explain Repo

This skill turns a repository into an **atlas** — a navigable set of HTML **chapters** a developer opens to understand a codebase well enough to keep building it, plus a distilled `SUMMARY.md` that bootstraps a future agent session.

Everything in the atlas is **grounded**: every claim cites the file, commit, or issue it came from, or it is cut. This is the skill's root discipline — **cite or cut**. Never describe the repo from a parametric guess of what code like this "usually" does. Read it, then cite it. The two chapters most prone to invention — History and Strengths/Weaknesses — get an adversarial **refute** pass (step 5) for exactly this reason.

The atlas lives in `.repo-atlas/` inside the target repo, gitignored so it never dirties the tree, and stamped with the **as-of** commit it was built against so it can be refreshed when the code drifts.

Work the steps in order. Each ends on a completion criterion — do not advance until it is met.

## The atlas workspace

Two layers, mirroring the territory and your map of it.

**Presentation layer — what the developer opens (HTML), under `.repo-atlas/`.**

- `index.html`: the **dashboard**. The one page the developer opens — a left menu of chapters, references, and foundations, plus a freshness line, with the current chapter in the content area. The whole sidebar is driven by a `NAV` object inside the file (see [The Dashboard](#the-dashboard)). Built from [templates/dashboard.html](./templates/dashboard.html).
- `assets/`: shared `style.css` and `md.js` (an offline Markdown renderer). Copied from this skill's `assets/` once at setup — never hand-edit per atlas.
- `brief.html`, `glossary.html`, `sources.html`: foundation docs. Built from [templates/doc.html](./templates/doc.html); content is Markdown following [BRIEF-FORMAT.md](./BRIEF-FORMAT.md), [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md), [SOURCES-FORMAT.md](./SOURCES-FORMAT.md).
- `chapters/*.html`: the atlas proper. One self-contained **chapter** per area of the repo, from the spine in [CHAPTERS.md](./CHAPTERS.md). Built from [templates/chapter.html](./templates/chapter.html). Titled `0001-<dash-case-name>.html`, the number incrementing.
- `reference/*.html`: dense, scannable cheat-sheets (directory map, command reference, key-file index). Built from [templates/reference.html](./templates/reference.html).

**State layer — your working memory, never opened by the developer (Markdown), under `.repo-atlas/`.**

- `findings/*.md`: verified facts about the repo and the open questions behind the chapters — your evidence ledger. Titled `0001-<slug>.md`. Use [FINDING-FORMAT.md](./FINDING-FORMAT.md).
- `SUMMARY.md`: the distilled agent-bootstrap file. Follows [SUMMARY-FORMAT.md](./SUMMARY-FORMAT.md).
- `.atlas-meta.json`: `{ asOf, repoRemote, chapters }` — the as-of stamp that drives refresh.
- `NOTES.md`: a scratchpad for preferences and working notes.

### Markdown is the source of truth

For the foundation docs (`brief`, `glossary`, `sources`), the Markdown lives *inside* the HTML, in a `<script type="text/markdown">` block (see [templates/doc.html](./templates/doc.html)). To edit, change only that block; to read the doc's state, read only that block. `md.js` renders it — no separate `.md` file, no double-maintenance. The state docs (`findings/`, `SUMMARY.md`, `NOTES.md`) stay plain `.md` — never opened by the developer, so never wrapped.

## Step 1 — Set up the workspace

Resolve the target repo (default: the current repo; otherwise ask for the path). Then, from the repo root:

1. Create `.repo-atlas/` and ensure it is ignored — add `.repo-atlas/` to `.gitignore` (create `.gitignore` if absent). If the target is not a git repo, say so: history and freshness will be unavailable, and ask whether to continue.
2. Copy this skill's `assets/` into `.repo-atlas/assets/`.
3. Copy [templates/dashboard.html](./templates/dashboard.html) to `.repo-atlas/index.html`, and create `brief.html`, `glossary.html`, `sources.html` from [templates/doc.html](./templates/doc.html).
4. Create `chapters/`, `reference/`, `findings/` lazily, when the first file in each is written.

**Completion criterion:** `.repo-atlas/` exists, is gitignored, holds `assets/` and a dashboard, and the three foundation docs exist (empty is fine).

## Step 2 — Recon and write the brief

Run a cheap, broad pass — do not read deeply yet:

- Layout: directory tree (depth-limited), entry points, README, CONTRIBUTING.
- Stack: manifest/lock files, Dockerfile, CI config files (their existence and names).
- Git: `git log --reverse | head`, tags, `git shortlog -sne` (skip if not a git repo).
- Origin: `git remote get-url origin` — record it, and whether the repo is **public** (the Contributing chapter depends on this; if `gh` and a public remote are available, that chapter is in scope, else it is dropped).

Use recon to do two things:

1. **Interview for the brief** — *why* is the developer studying this repo, and *what will they do* (onboard, fix a bug, add a feature, audit, take over)? Plus their stack fluency, which calibrates explanation depth. Keep it to a few questions. Write `brief.html` per [BRIEF-FORMAT.md](./BRIEF-FORMAT.md). The brief decides which chapters get depth.
2. **Enumerate the functional blocks** — the significant subsystems worth deep investigation. On a large repo, cap deep investigation at the top blocks by size and churn, and **log what was skipped** in `NOTES.md` and the brief — never silently truncate.

**Completion criterion:** `brief.html` is written, public/private is resolved, and the list of blocks-to-investigate (and any skipped) is recorded.

## Step 3 — Investigate

Read [CHAPTERS.md](./CHAPTERS.md) now — it holds the chapter spine and a per-chapter investigation recipe (what to read, what to cite). Select the chapters the brief calls for.

**Fan out**: spawn one subagent per chapter (or per functional block), each investigating only its slice and returning a structured **finding** ([FINDING-FORMAT.md](./FINDING-FORMAT.md)) plus a draft chapter Markdown. This keeps heavy reading out of the main context. The subagent's instruction is the chapter's recipe plus **cite or cut**: every claim carries a `path:line`, commit SHA, or issue/PR number, and marks itself *observed* (read directly) or *inferred* (deduced).

**Completion criterion:** every in-scope chapter has a finding whose claims are each cited and tagged observed/inferred.

## Step 4 — Assemble

Turn findings into the atlas:

- Write each `chapters/NNNN-*.html` from [templates/chapter.html](./templates/chapter.html), rendering citations as links into real source — readable text `src/foo.ts:42` that is also a relative `<a href="../../src/foo.ts">` (the atlas sits two levels deep). Link commits to `<remote>/commit/<sha>` when the remote is a web URL, else plain SHA.
- Maintain `glossary.html` (repo and domain terms, per [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)) and `sources.html` (the repo, its docs, stack docs, and — for public repos — the tracker and communities, per [SOURCES-FORMAT.md](./SOURCES-FORMAT.md)).
- Add each chapter and reference to `NAV` in `index.html` (see [The Dashboard](#the-dashboard)).

**Completion criterion:** every in-scope chapter renders in the dashboard with working source links, and the glossary and sources are populated.

## Step 5 — Refute

Run an adversarial pass over the two invention-prone chapters — **History** and **Strengths/Weaknesses**. Spawn a skeptic subagent whose job is to *refute* each claim against the actual code and git, defaulting to "unsupported" when evidence is thin. Cut or downgrade to *inferred* anything it cannot ground. A weakness with no cited evidence does not ship.

**Completion criterion:** every History and Strengths/Weaknesses claim is either grounded in a citation the refuter accepted, or removed.

## Step 6 — Distill and stamp

1. Write `SUMMARY.md` per [SUMMARY-FORMAT.md](./SUMMARY-FORMAT.md) — the dense, parse-friendly file a future agent reads to bootstrap. It is a distillation of the findings, not new investigation.
2. Write `.atlas-meta.json` with the **as-of** commit (`git rev-parse HEAD`), the remote, and the chapter list. Show the as-of in the dashboard freshness line.
3. Offer to copy `SUMMARY.md` into the repo's `CLAUDE.md` (append or seed) — offer, never do it automatically.
4. Open the dashboard (`.repo-atlas/index.html`) for the developer if a CLI open command is available.

**Completion criterion:** `SUMMARY.md` and `.atlas-meta.json` exist, the dashboard shows the as-of commit, and the developer has been pointed to the dashboard.

## Refreshing the atlas

When the atlas already exists, re-running is targeted, not a rebuild. Read `.atlas-meta.json` for the as-of commit, run `git diff <asOf>..HEAD --stat`, and map touched paths to chapters. Mark only those chapters **stale** in `NAV` (the dashboard surfaces the count), re-investigate just them (steps 3–5 for that slice), and restamp `.atlas-meta.json`. Untouched chapters stand.

## The Dashboard

The dashboard is the developer's home. Its sidebar and freshness line are driven entirely by the `NAV` object inside `index.html` — never hand-edit the sidebar markup. After creating or refreshing anything, update `NAV`:

- **New chapter** → append `{ n, href, title, stale: false }` to `NAV.chapters` and point `NAV.current` at it.
- **New reference** → append `{ href, title }` to `NAV.reference`.
- **Chapter went stale on refresh** → set its `stale: true`; clear it once re-investigated.
- **As-of changed** → update `NAV.asOf`.

## Diagrams

Default to ASCII box-diagrams in fenced code blocks — zero-dependency, print well, and consistent with the offline `file://` atlas. Architecture (module map), CI/CD (pipeline), and one end-to-end flow are the diagrams worth drawing. Only bundle a renderer like mermaid if the developer asks.
