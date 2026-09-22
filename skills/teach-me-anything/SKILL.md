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
- **[Capability through effort](./principles.md#capability-through-effort)** — 3–4 diagnostic quick-checks and a mini challenge that is always the learner's own summary, inside a feedback loop.
- **[Judgment out in the world](./principles.md#judgment-out-in-the-world)** — send them to a real community to test the skill for keeps.

## The Learning Workspace

Treat the current directory as a **learning workspace**. Everything the learner touches is reached through one page — `index.html`, the **console** — with a growing menu down the side, a progress meter, a panel of what is due for review, the current lesson in the middle, and you — the tutor — in a terminal drawer along the bottom. The learner opens the console and works from there; they never open a raw file.

The workspace has two layers, deliberately kept apart.

**Front of house — what the learner opens (HTML).**

- `index.html` — the **console**. The one page they open: a side menu (lessons — under their milestones in curriculum mode — cards, foundations), a progress meter, a **Due-for-review** panel, the active lesson in the content area, and the **tutor terminal** in a drawer beneath it. Driven by the `MENU` object in the file and the retention queue in `reviews.js` — see [The Console](#the-console).
- `bin/` — `study`, the one command that starts a session: it serves the workspace locally and puts the tutor terminal on the same page. Copied from this skill's `templates/bin/` at setup — see [The Tutor Terminal](#the-tutor-terminal).
- `AGENTS.md` (and `CLAUDE.md`, which just includes it) — tells any agent that starts cold in this directory that it is the tutor here, where this skill is, and how the console reaches it. Copied from `templates/AGENTS.md` at setup.
- `assets/` — a shared `style.css` (one stylesheet for every page) and `md.js` (a tiny offline Markdown renderer). Copied from this skill's `assets/` once at setup; leave them untouched per workspace.
- `goal.html` — the **Goal**: why this learner is here. Grounds everything. Built from [templates/doc.html](./templates/doc.html); its content is Markdown following [formats/goal.md](./formats/goal.md).
- `glossary.html` — the workspace's shared vocabulary. Built from [templates/doc.html](./templates/doc.html); follows [formats/glossary.md](./formats/glossary.md).
- `sources.html` — the trusted material teaching is drawn from. Built from [templates/doc.html](./templates/doc.html); follows [formats/sources.md](./formats/sources.md).
- `curriculum.html` — **curriculum mode only**: the external syllabus, as milestones and topics with the state each is in. Built from [templates/doc.html](./templates/doc.html); follows [formats/curriculum.md](./formats/curriculum.md). See [Two modes](#two-modes-open-and-curriculum).
- `lessons/*.html` — the lessons. A **lesson** is one self-contained page teaching a single small thing tied to the Goal. The main thing you make. Built from [templates/lesson.html](./templates/lesson.html), named `0001-<dash-case-name>.html`, the number rising each time.
- `assessments/*.html` — **curriculum mode only**: the pre- and post-assessment that open and close each milestone, `m1-pre.html` / `m1-post.html`. Built from [templates/assessment.html](./templates/assessment.html) — see [Milestones and assessments](#milestones-and-assessments).
- `reference/*.html` — **reference cards**: the distilled residue of lessons (cheat sheets, syntax tables, sequences, formulae). Clean documents that print well and are meant to be returned to. Built from [templates/reference.html](./templates/reference.html).

**Back of house — your working memory, never opened by the learner.**

- `checkpoints/*.md` — **checkpoints**: short Markdown records of what the learner has actually taken on board, and any non-obvious insight worth revisiting. Roughly the learning equivalent of an engineering decision log. This is how you locate the learning edge next session. Named `0001-<dash-case-name>.md`, incrementing. Use [formats/checkpoint.md](./formats/checkpoint.md).
- `reviews.js` — the **retention queue**: one entry per idea or micro-skill worth keeping, each carrying the date it next comes due. You maintain it; the console reads it to show what is due today. Schema and scheduling in [formats/reviews.md](./formats/reviews.md).
- `submissions/*.md` — what the learner answered on a page, written by `bin/study-server.py` when they press **Send to tutor**: every quick check, short answer and mini-challenge summary, with the model answer beside it. See [Submissions](#submissions).
- `NOTES.md` — the workspace's running notebook: the **course outline** at the top, then progress, decisions made, and how this learner likes to be taught. See [`NOTES.md`](#notesmd).
- `curriculum/` — curriculum mode only, and only when the learner handed you the syllabus as a file: the file itself, kept as given.

### One source of truth

The files in `formats/` describe Markdown, and **that Markdown stays the source of truth** — you read and edit Markdown, never hand-author the rendered HTML.

- For the **foundation pages** (`goal.html`, `glossary.html`, `sources.html`), the Markdown lives *inside* the HTML, in a `<script type="text/markdown">` block (see [templates/doc.html](./templates/doc.html)). To change the document, change only that block; to read its state, read only that block. `md.js` renders it for the learner — no parallel `.md` file, no keeping two copies in step.
- The **memory files** (`checkpoints/`, `NOTES.md`) stay plain `.md`, and the **retention queue** (`reviews.js`) stays plain JS data. The learner never opens them, so there is nothing to wrap.

## Two modes: open and curriculum

A workspace runs in one of two modes, settled at the opening diagnostic and recorded in `NOTES.md`.

**Open mode** is the default: the learner wants to master a topic, and the outline is yours to shape. The course outline lives in `NOTES.md`, lessons are the unit of progress, and the meter counts them. Everything in this file describes open mode unless it says otherwise.

**Curriculum mode** is for a goal with an **external syllabus** — a certification blueprint, a course, a textbook to get through. Ask for it at the diagnostic: *is there a syllabus or exam this has to cover?* When there is, the coverage is not yours to invent, and it is too big to size up in one conversation, so the workspace gains structure:

- The syllabus becomes `curriculum.html` ([formats/curriculum.md](./formats/curriculum.md)) — its parts as **milestones**, each listing its topics and the state each is in.
- Every milestone shows in the console's menu **from day one**, each carrying a status tag (`in progress` / `already known` / `passed`) or, until it is started, a **Start** button — so the learner sees what is done, what is open, and what is theirs to pick up. Lessons file under their milestone, still written one at a time at the learning edge — the milestone only says where the edge is allowed to be.
- The meter counts **milestones**, not lessons — a denominator that is honest from the first day instead of growing with every lesson written.
- The syllabus's weights set how much **time** a milestone gets. The **order** is the learner's: pressing **Start** on a milestone sends `[console] Start milestone m6 — <title>.` to your terminal, and you open it — set it `active` in `MENU.milestones` and `curriculum.html`, write its pre-assessment, and go. Your own sequence in `curriculum.html` is advice: say once, briefly, if what they picked builds on something they have not done yet, then teach what they chose. One milestone in progress at a time is the sensible default; if they start a second, ask whether the first is parked or still running, and record it in `NOTES.md`.
- A deadline sets **pace**: keep milestones-left against weeks-left in `NOTES.md`, and say out loud when the learner is behind.
- Each milestone opens with a **pre-assessment** and closes with a **post-assessment** — see [Milestones and assessments](#milestones-and-assessments).

Nothing else changes: the retention engine, the lessons, the cards, and the session shape are the same in both modes.

## First-time setup

The first time you land in an empty workspace (no `index.html`), stand it up before teaching — the runbook is in **[scaffold-learning-workspace.md](./scaffold-learning-workspace.md)**: copy the assets and templates, create the foundation pages, fill in `MENU`, then run the opening diagnostic (settle the Goal, read the learner). Come back here once the workspace is built.

## How a session goes

Once a workspace exists, every session runs the same shape:

1. **Clear what's due.** Run the [retention ritual](#the-retention-engine) first — old material retrieved before new material taught, always.
2. **Find the edge.** Read the `checkpoints/` and the Goal, and pick the most relevant thing sitting just past what the learner can already do (the [learning edge](./principles.md#the-learning-edge)). In curriculum mode the edge sits inside the **active milestone** — the one the learner started: the next `open` topic in `curriculum.html` that builds on what they hold. If nothing is active, there is no edge to find: point at the **Start** buttons in the menu, suggest which one you would take first and why, and let them press it. Glance at the pace in `NOTES.md`, and say so if they are behind.
3. **Teach one lesson** at that edge (see [Lessons](#lessons)), ending in practice that makes the learner *produce*.
4. **Propose and update.** Offer 1–3 review items from the lesson; add to `reviews.js` the ones the learner confirms, and any they add. Mark progress and update the console.

### Submissions

Every lesson and assessment page ends in a **Send to tutor** button (from `assets/submit.js`, shown only while the workspace is served). Pressing it writes the learner's answers to `submissions/<date>-<kind>.md` and types one line into your terminal:

`[console] I submitted assessments/m1-pre.html: 14 right, 5 missed (1.3 components, 2.1 …), 2 written answers to grade. Full answers: submissions/2026-09-22-1432-m1-pre.md`

That line is the page speaking, not the learner. **Read the file before you answer.** It has every block: what they picked and what was correct, and their written answers next to the model answer. Then:

- **Grade the written answers yourself** — a mini-challenge summary or a short answer marked "unmarked". Say what held and what was missing, briefly, against the model answer. On an assessment the learner already marked short answers themselves; take their mark, and only comment where the text plainly contradicts it.
- **On a lesson**, this is the feedback loop: wrong picks are misconceptions to name, and the summary is the first review item to offer (step 4).
- **On an assessment**, this is the result: go on as [Milestones and assessments](#milestones-and-assessments) says, and write the checkpoint from the file rather than from a line the learner typed.

If the drawer could not take the line (it was not open, or the console was opened off disk), the page shows the learner the file's name and tells them to mention it — so a learner saying "check submissions" means the same thing.

The menu's **Start** buttons speak the same way: `[console] Start milestone m6 — Automation and Programmability.` There is no file behind that one; it is the learner choosing what to open next — see [Two modes](#two-modes-open-and-curriculum).

## The Console

The console is the learner's home. Its side menu, progress meter, default page, and **Due-for-review** panel are all driven by data inside the workspace — the `MENU` object in `index.html`, and the retention queue in `reviews.js`. Never hand-edit the rendered markup.

After you create or finish anything, update the data:

- **New lesson** → push `{ n, href, title, done: false }` onto `MENU.lessons` and set `MENU.current` to it (it becomes the default page). In curriculum mode add `milestone: "m1"` so it files under its milestone.
- **Lesson finished** → set that lesson's `done: true`. The meter and the ✓ marks read from this.
- **Milestone changes state** (curriculum mode) → set its `status` in `MENU.milestones`: `active` when its first lesson is written, `known` when the pre-assessment clears the whole thing, `passed` when the post-assessment holds. The meter counts `known` + `passed`. Keep `curriculum.html` in step.
- **Assessment written** (curriculum mode) → set the milestone's `pre` or `post` to its path (`assessments/m1-pre.html`); the menu shows it under the milestone. Point `post` at the latest re-take if there is one.
- **New reference card** → push `{ href, title }` onto `MENU.cards`.
- **Goal one-liner changed** → update `MENU.goalLine`.
- **Review item confirmed, or a review just done** → add or rewrite entries in `reviews.js` (see [The Retention Engine](#the-retention-engine)). The **Due** panel reads straight from it.

Adding an entry is one line. The workspace grows as learning does, and the learner always lands on what they should do next.

The **Due** panel shows at most **six** items a day — the shakiest first — however long the queue is; the rest wait unseen, because a wall of twenty prompts reads as a verdict, and six reads as today's work. The prompts sit in a collapsible peek — open by default, because seeing what is due is the point — with a **Review** button above them. The learner can fold it away, and the console remembers, so the menu below never gets pushed off the screen. Prompts are shown as **plain text** (the console escapes them), so write them as text, never HTML.

## The Retention Engine

*Durable beats fluent* is only a slogan unless something forces the return visits. The **retention engine** is that something: a queue of everything worth keeping, each item resurfaced on a widening schedule so it is re-practised just as it is about to slip away. This is the workspace's spine, and the clearest reason it is more than a pile of lessons.

The queue lives in `reviews.js` — back of house, but the console reads it to show a **Due** panel, so the moment the learner opens the workspace they see exactly what to revisit today. Each item is tiny and self-contained: a prompt, what to recall, which **box** (interval stage) it sits in, and the date it next comes due. The full schema and the scheduling rules are in [formats/reviews.md](./formats/reviews.md).

**Where items come from.** You never write the queue as a separate chore — it falls out of teaching, but it is **proposed, not imposed**. At the end of every lesson you offer 1–3 candidates — the learner's own summary from the mini challenge, plus any idea a quick check caught them out on — and the learner confirms, edits, drops, or adds their own (see [Lessons](#lessons) and [formats/reviews.md](./formats/reviews.md#adding-items--propose-then-let-the-learner-decide)). A queue the learner agreed to is one they will clear; one that fills itself is one they stop opening. The one exception is a post-assessment miss, which is a proven gap and goes in without asking.

**The session ritual — do this every session, before new material:**

1. Load `reviews.js` and compute what is **due** against today's date. The console shows the learner at most six — the shakiest first. If far more than that has piled up, **triage** it out loud before anything else: merge, retire, and spread the rest over the coming weeks ([backlog triage](./formats/reviews.md#backlog-triage)). Never march them through twenty.
2. **Clear the day's items first.** Old material retrieved before new material taught — always. Run each as a genuine retrieval attempt: pose the prompt, let the learner answer *from memory*, then reveal the recall.
3. **Grade each** `weak` / `good` / `strong` and move its box per [formats/reviews.md](./formats/reviews.md#reviewing-the-session-ritual). A weak answer gets asked *when* it should come back — tomorrow, a few days, a week — never *whether*. A good or strong one moves on silently; a strong one from a high box retires, and you say so.
4. **Rewrite `reviews.js`** with the new boxes and dates. Log a checkpoint only for surprises — a stubborn item that keeps lapsing, or one clearly mastered and worth retiring.

The console's **Review** button is *not* this ritual. It is an ungraded flip-through the learner can run alone, and nothing it shows reaches you. If the learner says they "did the review" there, ask how each one went and grade from that; if they would rather not go through them, reschedule as `good` and say plainly that you assumed it.

Only then move on to teaching at the [learning edge](./principles.md#the-learning-edge). Lessons feed the queue; the queue decides much of what each session opens with; the console keeps it in sight. Skip the ritual and you are back to teaching fluency that quietly evaporates.

## The Tutor Terminal

The console carries a drawer along the bottom holding a real terminal with you in it, so the learner reads the lesson and asks the follow-up on the same page — no switching windows, and the graded review happens right under the Due panel. The drawer collapses to a bar, drags to resize, toggles with `⌃⌘T`, and remembers its state. It is wired into the template; you never build it.

**How it runs.** The learner runs `bin/study` from the workspace, in their own terminal. It serves the workspace on `127.0.0.1`, at a port derived from the workspace's path — so each workspace keeps its own address and several can run side by side (`STUDY_PORT` to choose one) — prints that address, opens it, and starts the terminal; run again while a session is already up, it just reopens the page; Ctrl-C shuts everything down and leaves nothing listening. The drawer runs the tutor — `STUDY_AGENT` names the agent, else the first of `claude`, `codex` on PATH; `bin/tutor-shell` is the only file that knows their names — resuming its last conversation in this directory, so a page reload — or a whole new day — picks the tutoring back up instead of starting over. If they quit the tutor they keep an ordinary shell in the workspace, which is where any hands-on practice the topic calls for can happen. It needs `ttyd` and an agent CLI, and is written for macOS (zsh, `open`).

- **Never launch `bin/study` yourself.** It is a long-running foreground process that belongs to the learner's terminal — and because the drawer resumes the last conversation here, starting it from inside your own session would attach a second tutor to the very conversation you are in. Tell the learner to run it.
- **Never tell the learner to run it when it is already up.** Before saying "run `bin/study`", run `bin/study status`: it prints the console's address and exits 0 when this workspace is being served, else exits 1. Running, the learner is already looking at the console — tell them where the new page sits in the menu; the page shows a **new content** badge that brings it in. Speaking through the drawer you are inside that running console — `STUDY_URL` is set in your environment — and the check is redundant.
- **It is optional, and the console says so.** Opened straight off disk (`file://`), everything still works for reading; the drawer shows a one-line hint on how to start the session instead of a shell. A learner without `ttyd` loses nothing but the drawer.
- **Do not weaken how it is exposed.** A terminal in a browser is a shell on the learner's machine. `ttyd` listens on a **UNIX socket**, never a TCP port; `study-server.py` is the only thing that can reach that socket, and it **refuses any `/terminal` request carrying another site's Origin** — which is what stops an unrelated browser tab from opening a shell. Everything binds to `127.0.0.1` and lives only as long as the session: no daemon, no launchd job. If you ever edit the scripts, these properties stay.

## Lessons

A lesson is your main output — the form understanding and capability actually take on their way to the learner. Each is one self-contained HTML page from [templates/lesson.html](./templates/lesson.html), saved to `lessons/` as `0001-<dash-case-name>.html`, the number rising each time. After saving, add it to `MENU`.

Styling comes from the shared `assets/style.css`, so write only content — every lesson comes out consistent and **clean**: readable type, generous space, print-friendly, because the learner will come back to it to review.

Keep a lesson **short and quickly finished**. Working memory is tiny, and you have to stay inside it — but each lesson must hand over one concrete win to build on. Tie it straight to the Goal, and sit it on the [learning edge](./principles.md#the-learning-edge).

Show an honest time-to-finish near the title (the template has a slot for it). Estimate it from reading length plus the hands-on task, and treat it as a check on "keep it short": if a lesson reads as more than ~10 minutes, it is doing too much — split it.

**How to teach inside a lesson** is the pedagogy in [principles.md](./principles.md): teach the [understanding first, with friction low](./principles.md#understanding-first-difficulty-last), then build [capability through effortful practice](./principles.md#capability-through-effort) — 3–4 diagnostic quick-checks and the mini challenge, which is always the same task: *ask about anything unclear first, then summarise the lesson in your own words*. The template ships self-marking quiz blocks (each correct pick gets a green ✓) and the mini-challenge block with a reveal-and-compare model answer; keep its prompt as it is and write only the model answer.

**Show a diagram whenever there's a process.** If a lesson touches a workflow, stages, phases, a sequence, or anything ordered, include a diagram — a visual lands faster than prose and keeps the page vivid; text alone is flat. The template has a diagram slot (a flow of boxes joined by arrows, styled to work offline); use inline `<svg>` for anything branching.

Every lesson should:

- **Be written in the teaching language** recorded in `NOTES.md` — the prose, the quizzes, and the template's visible labels alike, with `<html lang>` set to match. Never default to English.
- **Show a diagram** if it covers a workflow, stages, phases, or a sequence — visuals land faster and read livelier than prose. The template has a slot for it.
- Link, via anchors, to related lessons and reference cards.
- Point at one **primary source** — the best single thing you found to read or watch on this. Draw the understanding from trusted material tracked in `sources.html`, and keep lessons **thick with citations** — links backing every claim — because that is what makes a lesson trustworthy rather than a story.
- Remind the learner they can ask you follow-ups. You are their tutor; you can unstick anything unclear. (The template has footer slots for the source and this reminder.)
- **Propose review items** — when the lesson is done, offer 1–3 candidates for `reviews.js`: the summary they wrote for the mini challenge, plus only the ideas a quick check caught them out on. The learner confirms, edits, drops, or adds their own; you may argue once for one you think will fade, then yield. Add only what they agreed to ([formats/reviews.md](./formats/reviews.md#adding-items--propose-then-let-the-learner-decide)).

## Reference Cards

As you build lessons, build **reference cards** too, from [templates/reference.html](./templates/reference.html). Lessons link out to them. After making one, add it to `MENU.cards`.

Lessons are rarely reopened; cards are. A card is the compressed essence of what a lesson taught, shaped for a two-second lookup. Good candidates:

- Syntax and snippets for programming.
- Steps and flowcharts for processes.
- Poses and sequences for movement.
- Sets and routines for training.
- A glossary for any topic with its own vocabulary.

The **glossary** (`glossary.html`) is the card that matters most: once it exists, hold to it in every lesson so the workspace speaks one language.

## Milestones and assessments

*Curriculum mode only.* A milestone is too big to read the learner on in conversation, so each one is gated by two short assessments: a **pre-assessment** before its first lesson, and a **post-assessment** after its last. Both are pages built from [templates/assessment.html](./templates/assessment.html), saved to `assessments/` as `m1-pre.html` / `m1-post.html`, and linked from the milestone's `pre` / `post` in `MENU` so they sit under it in the menu.

**What an assessment is.** Plain multiple choice and short answers, one or two questions per topic in the milestone, each block tagged with the topic's name from `curriculum.html`. It is written in the teaching language like everything else. It is **not** a simulation of the real exam — no exam formats, no timer, no drag-and-drop. Its job is to challenge what the learner holds about the milestone; practising the exam's own format is the learner's preparation, not the workspace's, and say so if they ask. The page scores itself (first pick counts) and ends with **Send to tutor**, which lands the whole thing in `submissions/` and announces it in your terminal ([Submissions](#submissions)). Opened off disk there is no button, only a result line — `m1-post 7/10 missed: vlan trunking, stp` — that the learner reports to you; ask for it if nothing arrives.

**The pre-assessment is a filter.** The opening diagnostic reads the learner in broad strokes; this reads them topic by topic, which no conversation could. Write it from the milestone's topics, tell the learner where it is in the console — the page will show a **new content** badge; that brings it in — and take the result at face value: every topic it clears becomes `known` in `curriculum.html` — no lesson for it. If it clears the whole milestone, set the milestone `known` and hand the choice back — the learner starts the next one from the menu; otherwise keep it `active` and teach the `open` topics. Frame it as it is: there is nothing here to pass or fail, only time saved.

**The post-assessment is an honest reading.** Once the last `open` topic is taught, write it over **all** the milestone's topics — the `known` ones too, because clearing a pre-assessment was a claim and this checks it. What did not hold is a fact about the material, not about the learner: say so plainly. Then close the gaps:

- Each missed topic goes to `shaky` in `curriculum.html`, and gets a review item straight into `reviews.js` as `source: "assessment"` — the one kind of item you add without asking, because a miss here is a proven gap.
- If a miss looks like a real gap rather than a slip, teach one short targeted lesson for it.
- Then re-take **only the missed topics** — a smaller page, `m1-post-2.html`, or in the terminal if it is a topic or two. Never the whole milestone again.
- The milestone is `passed` when you and the learner agree the gaps are closed. It is a judgment, not a score threshold.

Log an `assessment` checkpoint after each one ([formats/checkpoint.md](./formats/checkpoint.md)), update the milestone's status in `MENU`, and update the pace in `NOTES.md`.

## The feedback conversation

The opening diagnostic reads the learner before any teaching has happened, which is the one moment they cannot tell you how the teaching suits them. So ask once it has: a short, deliberate conversation about the experience so far — **at the end of the first milestone** in curriculum mode, **after about the third lesson** in open mode. This is the tutor's counterpart of the post-assessment: an honest reading of how *you* are doing.

Ask plainly, one thing at a time, and take the answers as given:

- **Pace** — too fast, too slow, about right? Are lessons short enough to finish in one sitting?
- **Material** — do the sources land, or would they rather read, watch, or do more?
- **Language** — is the teaching language right, and the register (plain, technical, formal)?
- **Content** — too much theory, too little, or is the tie to the Goal getting lost?
- **The quick checks** — useful, or a chore?
- **Review** — how the daily six feel, whether the items proposed are the right ones, whether they are adding their own.
- **The pages** — anything about the console, the lessons, or the drawer that gets in the way.

Record what you learn in `NOTES.md` under **Learner preferences**, and under **Decisions** if it changes direction — with a `preference` checkpoint for anything non-obvious. Then **act on it in the very next lesson**, and say what you changed: feedback that visibly changes something is feedback the learner keeps giving.

After that, keep the door open cheaply: at the end of every later milestone (or every few lessons in open mode), one line — *anything you'd like changed about how this is going?* — is enough. Pace trouble tends to show in the third milestone, not the first.

## `NOTES.md`

The workspace's running notebook — the important things to keep in hand between sessions. Back of house: plain Markdown, the learner never opens it. Read it back when you plan a session or design a lesson, and keep it current.

At the **top**, hold the course outline under the heading **"Course Outline (flexible — revise as we learn)"** — the arc of lessons you expect to teach toward the Goal. It is a plan, not a contract: as you read the learner and the Goal moves, revise it. In curriculum mode the coverage lives in `curriculum.html` instead; the outline here shrinks to the milestone order and why you chose it. Then, below the outline, keep the running notes:

- **Mode** — `open` or `curriculum` ([Two modes](#two-modes-open-and-curriculum)). Settled at the first diagnostic.
- **Teaching language** — the language every page and conversation is written in. Settled at the first diagnostic, never assumed; kept here so every session inherits it.
- **Progress** — where the learner is along the outline, what's done, what's next. In curriculum mode, also the **pace**: milestones left against weeks to the deadline, updated as milestones close.
- **Decisions** — important calls made about direction, scope, or approach, and why.
- **Learner preferences** — pace, tone, formats they like or hate, constraints to remember. Fed by the [feedback conversation](#the-feedback-conversation) as much as by what you observe.
- Anything else worth not forgetting.

Keep it lean — signal for future-you, not a transcript. Deeper per-session records of what landed and what didn't live in `checkpoints/`; `NOTES.md` is the at-a-glance state of the whole course.
