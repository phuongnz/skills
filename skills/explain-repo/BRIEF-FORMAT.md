# Brief Format (`brief.html`)

The brief lives at the atlas root as `brief.html`. It captures *why* this person is studying the repo and *what they will do* with the understanding. Every chapter-selection and depth decision traces back to it.

`brief.html` is built from [templates/doc.html](./templates/doc.html): the source of truth is the Markdown inside its `<script type="text/markdown">` block, which `assets/md.js` renders. Edit and read only that block — the template below is exactly what goes in it.

## Template

```md
# Brief: {Repo name}

## Why
{1-3 sentences. The concrete reason this person is studying this repo right now. Push past "to understand it" to the underlying goal.}

## Intent
{What they will do with the understanding — onboard, fix a specific bug, add a feature, audit/security, take over development. This decides which chapters get depth.}

## Reader background
{Stacks and languages they're already fluent in — this calibrates explanation depth. Note what is genuinely new to them here.}

## Scope
- In depth: {chapters / functional blocks to cover thoroughly}
- Skipped: {blocks deprioritised or skipped on a large repo — never silently truncated}

## Repo facts
- Remote: {url}  ·  Visibility: {public | private}  ·  As-of: {commit short SHA at brief time}
```

## Rules

- **One repo per atlas.** Studying two repos is two atlases.
- **Intent over completeness.** A brief that says "take over the billing service" steers depth better than "understand everything." Let it.
- **Push back on vagueness.** If the reader cannot say why, interview before writing. A bad brief produces an unfocused atlas.
- **Record what you skipped.** On a large repo, the skipped list is not optional — it is how the atlas stays honest about its coverage.
- **Revise when intent shifts.** If the reader's goal moves mid-study, update the Markdown block here — and `NAV.tagline` in `index.html` if the one-line description changed too.
