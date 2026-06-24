---
name: discover-ai-use-cases
description: Discover high-impact, personally-relevant AI use cases for a knowledge worker through a guided interview, then produce a dated report with a prioritized shortlist and ready-to-start plans. Use when someone wants help finding a worthwhile way to use AI in their job, asks "what could I actually use AI for", feels their AI use is stuck on Q&A/summaries/images and wants real impact, or wants to audit their workday for automation and augmentation opportunities.
---

# Discover AI Use Cases

Most people's AI use stalls at asking questions, summarizing, and generating images — pleasant, low-impact. The impact lives somewhere else: in the **repetitive, tedious, time-draining, error-prone, mentally-stressful** work a specific person does every week. You cannot guess it. You have to **interview for it**, then match what you hear to a pattern, then **score it honestly** so the person starts with a real win instead of a gimmick.

This skill runs that interview in **structured stages**, matches findings against a [use-case catalog](USE-CASE-CATALOG.md), scores candidates on **impact × feasibility** ([SCORING.md](SCORING.md)), and writes a dated [report](REPORT-TEMPLATE.md). The interviewing discipline — open, non-leading, concrete-past-behavior questions — lives in [QUESTION-BANK.md](QUESTION-BANK.md) and is **not optional**: leading questions manufacture fake use cases.

The evidence base (what people actually want automated, what really saves time, where AI reliably *hurts*) is current **as of mid-2026** and is baked into the catalog and scoring. Set calibrated expectations throughout — the honest numbers are smaller than the headlines, and for some tasks AI is a net loss.

Work the stages in order. Each ends on a completion criterion — do not advance until it is met. **Audience: knowledge/office workers.** Pace: a small **batch** of questions per stage, then react to the answers before moving on. Never dump all questions at once, and never fill in answers yourself.

## 1. Frame and calibrate

Tell the user what's about to happen and why, in two or three sentences: you'll ask about their actual workweek to find a *few* genuinely worthwhile AI use cases, not generic tips. Set the honesty frame now — AI helps most with drudgery and repetition, the real time-savings are meaningful but smaller than the hype, and for some tasks (especially expert work in a mature personal workflow) it can even slow you down. You are hunting for fit, not selling AI.

Capture lightweight context to steer later stages: their **role/field**, roughly how their week is split, and whether they want the **fast pass** (one batch per stage) or a **thorough pass** (follow threads deeper). Do not ask "what do you want to use AI for" — people answer that with stated wants ("faster horses"), not real needs. See [QUESTION-BANK.md § Stage 1](QUESTION-BANK.md).

**Done when:** you've stated the honest frame, and you know the user's role and chosen depth.

## 2. Map the workweek

Walk a typical week **chronologically and concretely** — a day-in-the-life pass. The goal is a plain list of the recurring tasks they actually do, in their words, before any judgment about AI. Ask about the last real instance, not the abstract routine ("Walk me through what you did yesterday morning" beats "What do you usually do"). Capture each task with rough **frequency** and **time per instance** — you need these for scoring later.

Keep the batch small (3–5 questions), then reflect the task list back and let them correct it. Probe the gaps: handoffs, waiting, the "boring admin" people forget to mention, work done outside normal hours.

**Done when:** you have a written list of the user's recurring tasks, each with rough frequency and time-per-instance, confirmed by the user.

## 3. Hunt the signals

For the tasks surfaced, find the ones carrying the **high-impact markers** — the things people most want off their plate: *repetitive, low-value/tedious, time-consuming, error-prone, mentally draining/stressful,* and *information-transforming* (moving info from one form to another: notes→summary, data→report, format→format). These markers are the signal that a task is worth automating or augmenting; a task without them is usually a "nice to have."

Use the elicitation techniques in [QUESTION-BANK.md § Stage 3](QUESTION-BANK.md): the **Mom Test** (ask about concrete past pain, never hypothetical futures), **5 Whys** (drill a complaint to its root), and probing for **latent** frustration the person has normalized. Stay strictly non-leading — do not suggest AI solutions yet, and do not imply the answer you want. Ask which tasks they'd most want to stop doing, and *why*.

**Done when:** each candidate task is tagged with the markers it carries, and you've identified the 3–6 that carry the most.

## 4. Match to patterns

Map each high-signal task to one or more patterns in [USE-CASE-CATALOG.md](USE-CASE-CATALOG.md) (organized by knowledge-work domain: comms, meetings, research & analysis, data wrangling, content, personal admin/scheduling, coding/automation, decision support, learning). For each, classify where it sits on the **automation ↔ augmentation** spectrum — fully hand it off, or AI drafts/assists and the human decides. Clerical and information-transforming tasks lean automatable; analytical, judgment, and relationship tasks lean augmentation. Reject matches that don't fit the person's *actual* workflow — generic adoption is where impact goes to die.

**Done when:** every high-signal task maps to a catalog pattern (or is explicitly marked "no good AI fit"), each tagged automation or augmentation.

## 5. Score and prioritize

Score each candidate on the two axes in [SCORING.md](SCORING.md): **Impact** (frequency × time-per-instance × pain) and **Feasibility** (data/inputs available, rules clear enough, low blast radius if wrong, genuinely AI-suitable). Plot them: high-impact/high-feasibility are the **Quick Wins** — the low-hanging fruit to start with; high-impact/low-feasibility are projects to flag, not start; low-impact items are skipped.

Apply the **honesty checks** from SCORING.md before ranking: strip any candidate that relies on a refuted/hype claim, down-rank tasks where the user is an expert in a mature workflow (AI may slow them down), and attach a *calibrated* expected value — a credible time range, not a headline multiplier.

**Done when:** every candidate has an impact score, a feasibility score, a quadrant, and a calibrated expected value; the Quick Wins are identified.

## 6. Write the report

Fill [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) and save it (default `./ai-use-cases-<name-or-role>.md` unless the user names a path). Stamp it with today's date and "use-case evidence as of mid-2026; re-validate, the field moves fast." Lead with the **2–3 Quick Wins**, and for each give: the task and its markers, automation-vs-augmentation framing, the calibrated expected value, and a concrete **"start this today"** plan (the first prompt to try, the tool, or the 3 setup steps). Include the full scored table and the flagged-but-deferred items so nothing is lost.

Then run the **honest-impact check**: re-read the report and confirm none of the three traps below survived. Fix any before delivering.

- [ ] No use case is justified by a hype/refuted stat or a generic "AI makes you faster" claim — every expected value is calibrated and task-specific.
- [ ] No top recommendation puts AI where the evidence says it reliably *hurts* (expert in a mature, fast personal workflow) without flagging it.
- [ ] Every Quick Win fits the user's *actual* described workflow, not a generic best-practice list.

**Done when:** the report exists at the path, is dated, leads with calibrated Quick Wins that each have a "start today" plan, and contains none of the three traps.
