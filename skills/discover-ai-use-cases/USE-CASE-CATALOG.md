# Use-Case Catalog — knowledge-work patterns

Match the tasks you elicited (Stage 3) to the patterns here, then carry the match into scoring. This is a **lookup, not a menu** — never read it to the user as a list of suggestions. A pattern only counts if it maps to a task the person *actually does* and *carries real signal markers*. Generic adoption ("you could use AI for emails!") is exactly the low-impact noise this skill exists to avoid.

Each pattern notes its dominant **signal markers**, where it sits on **automation ↔ augmentation**, typical **feasibility**, and a **starter** (the concrete first thing to try). The strongest, most reliable wins are **information-transforming** and **repetitive clerical** tasks. The riskiest are high-judgment, high-stakes, or expert-in-a-mature-workflow tasks — flag these rather than lead with them.

> The **signal markers** abbreviated in each pattern below (REP, TED, TIME, ERR, DRAIN, XFORM) are defined in `SKILL.md` Stage 3, which stays in context while this file is read.

---

## Comms & email
- **Signal markers:** REP, TED, TIME, sometimes DRAIN
- **Patterns:** triage/summarize long threads; draft replies from bullet points; turn a decision into an announcement; tone/length rewrites; recurring status updates from notes.
- **Spectrum:** augmentation (draft → human sends). Sending autonomously is rarely worth the blast radius.
- **Feasibility:** high. Inputs are text the person already has.
- **Starter:** paste the 3 longest unanswered threads and ask for a one-line summary + a draft reply each; edit and send.

## Meetings & calls
- **Signal markers:** REP, TED, XFORM, TIME
- **Patterns:** transcript → summary + decisions + action items with owners; pre-read briefs from prior notes; "what did we decide about X" search across past meetings.
- **Spectrum:** automation for capture/summary; augmentation for what-to-do-next.
- **Feasibility:** high if recordings/transcripts exist; medium if notes are sparse.
- **Starter:** run the next meeting's transcript through a fixed prompt that returns Decisions / Actions (owner + date) / Open questions.

## Research & analysis
- **Signal markers:** TIME, XFORM, DRAIN
- **Patterns:** synthesize many sources into a briefing; compare options into a table; literature/market/competitor scans; "explain this dense document"; first-pass analysis of findings.
- **Spectrum:** augmentation — AI gathers and drafts, human verifies. **Always** demand citations and spot-check; this is where confident wrong answers hurt.
- **Feasibility:** medium-high. Quality depends on source access and verification discipline.
- **Starter:** give it the 5 sources you'd have read anyway; ask for a cited synthesis with a "what's uncertain" section.

## Data wrangling
- **Signal markers:** REP, TED, ERR, XFORM
- **Patterns:** reformatting/cleaning; extracting structured fields from messy text; categorizing/tagging records; spreadsheet formulas and one-off scripts; reconciling two lists.
- **Spectrum:** automation, with a human check on a sample.
- **Feasibility:** high for well-defined transforms; **the classic Quick Win**. Watch ERR — always validate a sample before trusting the batch.
- **Starter:** take one recurring cleanup, describe the input and exact desired output, have AI produce the transform (or a reusable script); verify 10 rows.

## Content & writing
- **Signal markers:** REP, TIME, XFORM
- **Patterns:** first drafts from an outline; repurpose one asset into many formats (doc→slides→post→email); templated recurring docs; editing for clarity/length.
- **Spectrum:** augmentation (draft → human shapes). Voice and stakes decide how much editing.
- **Feasibility:** high for drafts/repurposing; lower where the writing *is* the expertise.
- **Starter:** take a doc you already wrote and have it produce the three downstream formats you'd otherwise make by hand.

## Personal admin & scheduling
- **Signal markers:** REP, TED, TIME
- **Patterns:** draft scheduling messages; turn a goal into a checklist/plan; fill recurring forms/templates; summarize-then-route incoming requests; expense/report prep.
- **Spectrum:** augmentation for anything that leaves your outbox; automation for private prep.
- **Feasibility:** high but individually small — these stack into a Quick Win when frequent.
- **Starter:** pick the most-repeated admin message/form and build a reusable fill-in-the-blanks prompt.

## Coding & automation
- **Signal markers:** REP, TIME, XFORM, ERR
- **Patterns:** scripts for repetitive manual steps; boilerplate; explain/refactor unfamiliar code; tests; glue between tools.
- **Spectrum:** augmentation. ⚠️ **Calibration flag:** the one rigorous RCT (METR) found *experienced* devs in their *own mature* codebases were ~19% slower with AI while feeling faster. Lead with this only for unfamiliar code, boilerplate, or non-developers automating manual steps — not for an expert in a workflow they've already optimized.
- **Feasibility:** high for self-contained scripts; lower in large unfamiliar systems.
- **Starter:** name one manual multi-step computer chore done weekly; have AI write a script for it; time the before/after honestly.

## Decision support
- **Signal markers:** DRAIN, TIME
- **Patterns:** structure a messy decision (options/criteria/tradeoffs); pressure-test a plan ("what am I missing"); pros-cons; risk lists.
- **Spectrum:** augmentation only — AI frames, human decides. Never automate the decision.
- **Feasibility:** medium. Value is in better thinking, not time saved; expected value is "fewer misses," not "minutes."
- **Starter:** bring a real upcoming decision; ask for the options/criteria table and the strongest case against your leaning.

## Learning & skill-building
- **Signal markers:** TIME, XFORM
- **Patterns:** explain a hard concept at your level; turn material into practice questions/flashcards; personalized study plan; on-demand tutor for a new tool.
- **Spectrum:** augmentation.
- **Feasibility:** high. Verify facts for anything that matters.
- **Starter:** take the thing you're currently trying to learn; ask for a 20-minute plan + 5 practice questions.

---

## Cross-cutting notes for matching

- **Frequency turns small into big.** A 5-minute task done 10×/day outranks a 2-hour task done once a quarter. Always weight by frequency (scoring does this).
- **Information-transforming is the most reliable win** and the most under-recognized — actively look for "I take X and make Y."
- **Augmentation is not a consolation prize.** For analytical/judgment/relationship work it's the *correct* design; forcing automation there is how projects fail.
- **No-fit is a valid result.** If a high-signal task needs inaccessible data, real-world action, or pure human judgment, mark it "no good AI fit" and move on. Honesty here is the whole value.
