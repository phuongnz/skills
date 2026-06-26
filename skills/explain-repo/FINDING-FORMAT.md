# Finding Format

Findings live in `findings/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`. Create the directory lazily — only when the first finding is written.

A finding is the evidence ledger behind a chapter — the verified facts, the citations they rest on, and the open questions still unanswered. It is the state layer that makes **cite or cut** enforceable and lets a refresh re-check a chapter without re-reading the whole repo.

## Template

```md
# {What this finding establishes}

{1-3 sentences: the claim or set of facts, and which chapter it feeds.}

## Evidence
- {Claim} — `path/to/file.ts:42` — *observed*
- {Claim} — commit `abc1234` (2024-03) — *observed*
- {Claim} — *inferred* from {what}; not directly confirmed

## Open questions
- {Anything unresolved that a deeper pass or a maintainer could answer}
```

## Rules

- **Every claim is tagged.** *Observed* means you read it directly (and cited where). *Inferred* means you deduced it — legitimate, but it must say so, and it is what the refute pass (step 5) scrutinises first.
- **Citations are concrete.** `path:line`, a commit SHA, or an issue/PR number. "The code seems to" is not a citation.
- **Open questions are first-class.** An honest "unknown" beats a confident guess. They also seed the next refresh and feed the `SUMMARY.md` open-questions section.
- **One finding per coherent area**, mirroring a chapter or block. Don't sprawl; don't merge unrelated facts.

## Numbering

Scan `findings/` for the highest existing number and increment by one.
