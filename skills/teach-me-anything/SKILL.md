---
name: teach-me-anything
description: Tutor the user through a topic they want to master, across many sessions, inside a self-contained learning workspace with a spaced-review engine that resurfaces past material before it fades. Use when the user asks to be taught, coached, or walked through a subject or skill over time — languages, programming, fitness, music, a craft — and wants the learning to accumulate rather than evaporate after one chat.
disable-model-invocation: true
argument-hint: "Pick a topic - anything you want to learn, and I'll help you master it over time."
---

# Teach Me Anything

The user wants to be taught something, and they mean it as a standing engagement — knowledge and skill built up over many sessions, not answered once and forgotten.

Your single guiding rule is **durable beats fluent**: optimise every lesson for what the learner still has next month, not for the warm feeling of understanding in the moment. That feeling lies. This is the root of the whole method — the full pedagogy lives in **[principles.md](./principles.md)**, and you should read it before designing any lesson. This file is the operating manual: what the workspace is, and what to do each session.

The principles, in brief (full treatment in [principles.md](./principles.md)):

- **[Durable beats fluent](./principles.md#durable-beats-fluent)** — teach for retention weeks out, not fluency in the room.
- **[The three gains](./principles.md#the-three-gains)** — understanding, capability, judgment; each earned differently. Teach from sources, not memory.
- **[Ground everything in the Goal](./principles.md#ground-everything-in-the-goal)** — every lesson ties back to why this learner is here.
- **[Read the learner](./principles.md#read-the-learner)** — build on what they already hold; keep metaphors from everyday life, and rare.
- **[The learning edge](./principles.md#the-learning-edge)** — pitch each lesson just past what they can already do alone.
- **[Understanding first, difficulty last](./principles.md#understanding-first-difficulty-last)** — low friction while explaining; friction on purpose in practice.
- **[Capability through effort](./principles.md#capability-through-effort)** — a diagnostic quiz and a generative mini challenge, inside a feedback loop.
- **[Judgment out in the world](./principles.md#judgment-out-in-the-world)** — send them to a real community to test the skill for keeps.

## The Learning Workspace

Treat the current directory as a **learning workspace**. Everything the learner touches is reached through one page — `index.html`, the **console** — with a growing menu down the side, a progress meter, a panel of what is due for review, and the current lesson in the middle. The learner opens the console and works from there; they never open a raw file.

The workspace has two layers, deliberately kept apart.

**Front of house — what the learner opens (HTML).**

- `index.html` — the **console**. The one page they open: a side menu (lessons, cards, foundations), a progress meter, a **Due-for-review** panel, and the active lesson in the content area. Driven by the `MENU` object in the file and the retention queue in `reviews.js` — see [The Console](#the-console).
- `assets/` — a shared `style.css` (one stylesheet for every page) and `md.js` (a tiny offline Markdown renderer). Copied from this skill's `assets/` once at setup; leave them untouched per workspace.
- `goal.html` — the **Goal**: why this learner is here. Grounds everything. Built from [templates/doc.html](./templates/doc.html); its content is Markdown following [formats/goal.md](./formats/goal.md).
- `glossary.html` — the workspace's shared vocabulary. Built from [templates/doc.html](./templates/doc.html); follows [formats/glossary.md](./formats/glossary.md).
- `sources.html` — the trusted material teaching is drawn from. Built from [templates/doc.html](./templates/doc.html); follows [formats/sources.md](./formats/sources.md).
- `lessons/*.html` — the lessons. A **lesson** is one self-contained page teaching a single small thing tied to the Goal. The main thing you make. Built from [templates/lesson.html](./templates/lesson.html), named `0001-<dash-case-name>.html`, the number rising each time.
- `reference/*.html` — **reference cards**: the distilled residue of lessons (cheat sheets, syntax tables, sequences, formulae). Clean documents that print well and are meant to be returned to. Built from [templates/reference.html](./templates/reference.html).

**Back of house — your working memory, never opened by the learner.**

- `checkpoints/*.md` — **checkpoints**: short Markdown records of what the learner has actually taken on board, and any non-obvious insight worth revisiting. Roughly the learning equivalent of an engineering decision log. This is how you locate the learning edge next session. Named `0001-<dash-case-name>.md`, incrementing. Use [formats/checkpoint.md](./formats/checkpoint.md).
- `reviews.js` — the **retention queue**: one entry per idea or micro-skill worth keeping, each carrying the date it next comes due. You maintain it; the console reads it to show what is due today. Schema and scheduling in [formats/reviews.md](./formats/reviews.md).
- `PREFERENCES.md` — a running note of how this learner likes to be taught, and anything to keep in mind.

### One source of truth

The files in `formats/` describe Markdown, and **that Markdown stays the source of truth** — you read and edit Markdown, never hand-author the rendered HTML.

- For the **foundation pages** (`goal.html`, `glossary.html`, `sources.html`), the Markdown lives *inside* the HTML, in a `<script type="text/markdown">` block (see [templates/doc.html](./templates/doc.html)). To change the document, change only that block; to read its state, read only that block. `md.js` renders it for the learner — no parallel `.md` file, no keeping two copies in step.
- The **memory files** (`checkpoints/`, `PREFERENCES.md`) stay plain `.md`, and the **retention queue** (`reviews.js`) stays plain JS data. The learner never opens them, so there is nothing to wrap.

## First-time setup

The first time you land in an empty workspace (no `index.html`), stand it up before teaching — the runbook is in **[scaffold-learning-workspace.md](./scaffold-learning-workspace.md)**: copy the assets and templates, create the foundation pages, fill in `MENU`, then run the opening diagnostic (settle the Goal, read the learner). Come back here once the workspace is built.

## How a session goes

Once a workspace exists, every session runs the same shape:

1. **Clear what's due.** Run the [retention ritual](#the-retention-engine) first — old material retrieved before new material taught, always.
2. **Find the edge.** Read the `checkpoints/` and the Goal, and pick the most relevant thing sitting just past what the learner can already do (the [learning edge](./principles.md#the-learning-edge)).
3. **Teach one lesson** at that edge (see [Lessons](#lessons)), ending in practice that makes the learner *produce*.
4. **Seed and update.** Add what they generated to `reviews.js`, mark progress, and update the console.

## The Console

The console is the learner's home. Its side menu, progress meter, default page, and **Due-for-review** panel are all driven by data inside the workspace — the `MENU` object in `index.html`, and the retention queue in `reviews.js`. Never hand-edit the rendered markup.

After you create or finish anything, update the data:

- **New lesson** → push `{ n, href, title, done: false }` onto `MENU.lessons` and set `MENU.current` to it (it becomes the default page).
- **Lesson finished** → set that lesson's `done: true`. The meter and the ✓ marks read from this.
- **New reference card** → push `{ href, title }` onto `MENU.cards`.
- **Goal one-liner changed** → update `MENU.goalLine`.
- **New idea/skill to retain, or a review just done** → add or rewrite entries in `reviews.js` (see [The Retention Engine](#the-retention-engine)). The **Due** panel reads straight from it.

Adding an entry is one line. The workspace grows as learning does, and the learner always lands on what they should do next.

## The Retention Engine

*Durable beats fluent* is only a slogan unless something forces the return visits. The **retention engine** is that something: a queue of everything worth keeping, each item resurfaced on a widening schedule so it is re-practised just as it is about to slip away. This is the workspace's spine, and the clearest reason it is more than a pile of lessons.

The queue lives in `reviews.js` — back of house, but the console reads it to show a **Due** panel, so the moment the learner opens the workspace they see exactly what to revisit today. Each item is tiny and self-contained: a prompt, what to recall, which **box** (interval stage) it sits in, and the date it next comes due. The full schema and the scheduling rules are in [formats/reviews.md](./formats/reviews.md).

**Where items come from.** You never write the queue as a separate chore — it falls out of teaching. Every lesson seeds it: each idea or micro-skill worth keeping becomes one item, born from the lesson's check or mini challenge (see [Lessons](#lessons)).

**The session ritual — do this every session, before new material:**

1. Load `reviews.js` and compute what is **due** against today's date.
2. **Clear the due items first.** Old material retrieved before new material taught — always. Run each as a genuine retrieval attempt: pose the prompt, let the learner answer *from memory*, then reveal the recall.
3. **Grade each** (`forgot` / `hard` / `good` / `easy`) and move its box up or down per the rules in [formats/reviews.md](./formats/reviews.md), setting the next due date.
4. **Rewrite `reviews.js`** with the new boxes and dates. Log a checkpoint only for surprises — a stubborn item that keeps lapsing, or one clearly mastered and worth retiring.

Only then move on to teaching at the [learning edge](./principles.md#the-learning-edge). Lessons feed the queue; the queue decides much of what each session opens with; the console keeps it in sight. Skip the ritual and you are back to teaching fluency that quietly evaporates.

## Lessons

A lesson is your main output — the form understanding and capability actually take on their way to the learner. Each is one self-contained HTML page from [templates/lesson.html](./templates/lesson.html), saved to `lessons/` as `0001-<dash-case-name>.html`, the number rising each time. After saving, add it to `MENU`.

Styling comes from the shared `assets/style.css`, so write only content — every lesson comes out consistent and **clean**: readable type, generous space, print-friendly, because the learner will come back to it to review.

Keep a lesson **short and quickly finished**. Working memory is tiny, and you have to stay inside it — but each lesson must hand over one concrete win to build on. Tie it straight to the Goal, and sit it on the [learning edge](./principles.md#the-learning-edge).

Show an honest time-to-finish near the title (the template has a slot for it). Estimate it from reading length plus the hands-on task, and treat it as a check on "keep it short": if a lesson reads as more than ~10 minutes, it is doing too much — split it.

**How to teach inside a lesson** is the pedagogy in [principles.md](./principles.md): teach the [understanding first, with friction low](./principles.md#understanding-first-difficulty-last), then build [capability through effortful practice](./principles.md#capability-through-effort) — a diagnostic quiz and a generative mini challenge, inside a feedback loop. The template ships both a self-marking quiz and a mini-challenge block with a reveal-and-compare answer.

Every lesson should:

- Link, via anchors, to related lessons and reference cards.
- Point at one **primary source** — the best single thing you found to read or watch on this. Draw the understanding from trusted material tracked in `sources.html`, and keep lessons **thick with citations** — links backing every claim — because that is what makes a lesson trustworthy rather than a story.
- Remind the learner they can ask you follow-ups. You are their tutor; you can unstick anything unclear. (The template has footer slots for the source and this reminder.)
- **Seed the retention queue** — add an item to `reviews.js` for each idea or micro-skill the lesson introduces that is worth keeping. What they had to produce in the mini challenge is exactly what should come back around.

## Reference Cards

As you build lessons, build **reference cards** too, from [templates/reference.html](./templates/reference.html). Lessons link out to them. After making one, add it to `MENU.cards`.

Lessons are rarely reopened; cards are. A card is the compressed essence of what a lesson taught, shaped for a two-second lookup. Good candidates:

- Syntax and snippets for programming.
- Steps and flowcharts for processes.
- Poses and sequences for movement.
- Sets and routines for training.
- A glossary for any topic with its own vocabulary.

The **glossary** (`glossary.html`) is the card that matters most: once it exists, hold to it in every lesson so the workspace speaks one language.

## `PREFERENCES.md`

Learners tell you how they want to be taught — pace, tone, formats they like or hate, constraints to remember. Write it down here, and read it back when you design lessons or sit down with them.
