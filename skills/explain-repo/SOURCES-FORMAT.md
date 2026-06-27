# Sources Format (`sources.html`)

`sources.html` is the set of grounding sources for the atlas. The first source is always the repo itself; the rest are the docs and communities that let a developer go deeper or get help. Knowledge in chapters is drawn from here, not from parametric guesses.

It is built from [templates/doc.html](./templates/doc.html): the source of truth is the Markdown inside its `<script type="text/markdown">` block, which `assets/md.js` renders. Edit and read only that block — the structure below is exactly what goes in it.

## Structure

```md
# {Repo} Sources

## The repo
- [README](../README.md) — the project's own entry point. Use for: stated purpose, quick start.
- [CONTRIBUTING](../CONTRIBUTING.md) — Use for: PR conventions, dev setup.
- [docs/](../docs/) — in-repo documentation. Use for: {what it actually covers}.

## Stack docs
- [Framework X docs](https://example.com) — official reference for the main framework. Use for: routing, lifecycle.
- [Library Y guide](https://example.com) — Use for: the {feature} the repo leans on heavily.

## Tracker & community (public repos)
- [Issues](https://github.com/org/repo/issues) — Use for: known bugs, good-first-issues, roadmap signals.
- [Discussions / Discord / mailing list](https://example.com) — Use for: design questions, maintainer contact.
```

## Rules

- **The repo is source zero.** Always link the repo's own README, CONTRIBUTING, and docs first, with relative paths into the tree. These outrank any external write-up. `sources.html` sits at `.repo-atlas/` root, so links into the repo are one level up (`../README.md`) — unlike chapters and reference docs, which sit a level deeper and use `../../`.
- **High-trust only.** Prefer official docs and primary sources over blog posts. If a source is marketing dressed as docs, leave it out.
- **Annotate every entry.** A bare link rots. Add one line: what it covers and when to reach for it.
- **Tracker & community is for public repos.** Drop the section for private repos or when `gh` is unavailable; note why if a reader might expect it.
- **Surface gaps.** If an area the brief needs has no good source (e.g. an undocumented subsystem), add a `## Gaps` section — it tells the reader where they're on their own.
- **Prune ruthlessly.** Five sharp sources beat thirty mediocre ones.
