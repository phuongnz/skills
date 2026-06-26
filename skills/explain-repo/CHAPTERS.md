# Chapter Spine

The recommended set of **chapters** for a repo atlas, each with an investigation recipe — what to read, and what to cite. Select chapters by the brief: a "fix one bug" brief leans on 0–2 and 9; an "audit" brief leans on 5–7; a "take over development" brief wants the whole spine. Adapt depth to the reader's stack fluency.

Every chapter obeys **cite or cut**: each claim carries a `path:line`, commit SHA, or issue/PR number, tagged *observed* (read directly) or *inferred* (deduced). A chapter is built from [templates/chapter.html](./templates/chapter.html); its evidence is recorded as a [finding](./FINDING-FORMAT.md).

## Granularity

Keep functional blocks as **sections of one chapter** when there are few; split into **one chapter per block** once there are many (roughly more than five significant blocks). Let the count decide, not a fixed rule.

## The spine

### 0 · Start here
What the repo is (2–3 sentences), who it's for, its maturity, and the 60-second get-it-running.
- **Investigate:** README, manifest scripts (`scripts`, `Makefile` targets), CONTRIBUTING, top-level layout.
- **Cite:** the actual install/build/test/run commands — verify each script exists before listing it.
- **Hands-on:** include a verification block (clone → run these commands → you should see X) per [templates/chapter.html](./templates/chapter.html).

### 1 · Architecture & structure
The map: top-level directories and what each holds, the layering/boundaries, entry points, and one end-to-end flow (e.g. a request from edge to response).
- **Investigate:** directory tree, entry points (`main`/`index`/`cmd`), a sampled import graph, framework conventions.
- **Cite:** directories and entry-point files. Draw an ASCII module-map diagram.

### 2 · Functional blocks
Per major subsystem: its responsibility, key files, public interface, and dependencies on other blocks.
- **Investigate:** one subagent per block; read its directory and the files its interface lives in.
- **Cite:** the block's directory and key files.

### 3 · Tech stack & dependencies
Languages, frameworks, runtime, datastores, and notable libraries — with *why* each is present. Flag dependency health (clearly outdated or deprecated) when cheap to detect.
- **Investigate:** manifests (`package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`/`requirements`, etc.), lockfiles, Dockerfile base images.
- **Cite:** manifest lines.

### 4 · Data model & key abstractions
The core domain types/schemas and the 3–5 abstractions you must hold to be productive here.
- **Investigate:** models/migrations/schema directories, central type definitions.
- **Cite:** the type and schema definitions.

### 5 · Build, test & CI/CD
How it builds, the shape of its tests, and the full pipeline: triggers → jobs → deploy targets, environments, and where secrets enter.
- **Investigate:** `Makefile`/build scripts, test config, `.github/workflows/*` (or `.gitlab-ci.yml`, `Jenkinsfile`, etc.), Dockerfile, deploy manifests; branch protection via `gh api` if public.
- **Cite:** the workflow and config files. Draw an ASCII pipeline diagram.

### 6 · History & evolution
Origin (first commit), eras and major refactors/rewrites/pivots, release milestones, the people who built it, and the trajectory it's on. **Refute-pass chapter.**
- **Investigate:** `git log --reverse | head`, tags, `git shortlog -sne`, churn by directory over time (`git log --stat`), README at successive tags.
- **Cite:** commit SHAs, dates, and tags. Mark anything not directly evidenced as *inferred*.

### 7 · Strengths, weaknesses & risks
Evidenced and opinionated: what's well-built, what's fragile or debt-laden or under-tested, security and operational risks, and bus-factor. **Refute-pass chapter — the hardest.**
- **Investigate:** synthesize from chapters 1–6 plus targeted reads (test coverage shape, error handling, TODO/FIXME density, hot churn files, single-author criticality).
- **Cite:** every claim needs evidence — a file, a pattern, a metric, an issue. A weakness with no citation does not ship.

### 8 · Contributing — *public repos only*
How to contribute, what to pick up, and how responsive the project is. Drop this chapter for private repos or when `gh` is unavailable.
- **Investigate:** CONTRIBUTING and PR conventions, `gh issue list --label "good first issue"`, `gh pr list` (open and recently merged), CODEOWNERS, maintainer activity.
- **Cite:** issue and PR numbers; the contributing guide.

### 9 · "Continue development" playbook
The payoff. Where to start for common tasks (add a feature, fix a bug, add an endpoint/component), the conventions to follow, the footguns to avoid, and the local dev loop. This is what makes the atlas actionable.
- **Investigate:** synthesize from all prior chapters; confirm the dev loop by reading the actual scripts and test setup.
- **Cite:** back-reference the chapters and the files each instruction touches.

## Reference docs

Alongside chapters, build dense cheat-sheets from [templates/reference.html](./templates/reference.html) — revisited far more than chapters are:

- **Directory map** — every significant directory → one-line purpose.
- **Command reference** — install / build / test / run / lint / deploy, copy-pasteable.
- **Key-file index** — the files a newcomer opens first, and why.
- **Module glossary** — block/abbreviation names → meaning (cross-links `glossary.html`).
