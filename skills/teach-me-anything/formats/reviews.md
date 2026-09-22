# Retention queue format

The **retention queue** (`reviews.js`) is the workspace's spaced-review engine: one entry per idea or micro-skill worth keeping, each carrying the date it next comes due. You maintain it; the console reads it to show what is due today. This is what makes *durable beats fluent* a mechanism rather than a wish. See [The Retention Engine](../SKILL.md#the-retention-engine).

It is **back of house** — the learner never opens the file, only the console's derived **Due** panel. It is plain JS data (JSON in a one-line wrapper) so the console can read it offline without a fetch.

## The file

```js
/* Retention queue — the spaced-review engine reads and rewrites this. */
window.REVIEW = [
  {
    id: "squat-depth",                 // stable, unique, dash-case
    prompt: "What depth makes a squat count?",   // the retrieval cue, shown first
    recall: "Hip crease drops below the top of the knee — 'below parallel'.", // what to produce from memory
    kind: "fact",                       // "fact" (knowledge) | "skill" (a doable rep)
    box: 2,                             // interval stage, 1..6
    due: "2026-07-10",                  // ISO date this next comes due
    lesson: "lessons/0003-depth.html",  // where it was taught (optional)
    added: "2026-07-05",                // ISO date it entered the queue
    source: "lesson"                    // "lesson" (you proposed it) | "learner" (they added it) | "assessment" (a post-assessment miss); optional
  }
];
```

## Boxes → intervals

Each item sits in a **box**. The box sets how long until it comes due again — the intervals widen so well-known items are seen rarely and shaky ones often (a Leitner schedule with expanding steps):

| Box | Interval until next due |
|----:|------------------------|
| 1   | 1 day   |
| 2   | 3 days  |
| 3   | 7 days  |
| 4   | 16 days |
| 5   | 35 days |
| 6   | 90 days |

## Adding items — propose, then let the learner decide

Items are never added silently. At the end of a lesson you **propose** the candidates and the learner **confirms, edits, drops, or adds** — a queue the learner agreed to is one they will clear; one that fills itself is one they stop opening.

- **Propose 1–3 items per lesson, no more.** The first is always the learner's own summary from the [mini challenge](../principles.md#capability-through-effort); the others are only the ideas a quick check actually caught them out on. An idea they got right first time is not a candidate.
- **Argue, then yield.** If they drop an item you think will fade — "this feels easy now; it is exactly the kind that slips" — say so once. Then respect the answer.
- **Take what they add.** Anything the learner wants to keep goes in as `source: "learner"`, in their words. Help them make it atomic.
- New items: `box: 1`, `due:` = today **+ 1 day**, `added:` = today.
- Keep `prompt`/`recall` atomic — one idea, answerable in a breath. Split anything bigger into several items.
- Write `prompt`/`recall` as **plain text**, not HTML. The console escapes them, so a prompt may safely contain quotes, `<placeholders>` or code — and any markup would show up literally.

**Assessment misses are the one exception.** A topic a post-assessment shows did not hold is a proven gap, and goes in without asking, as `source: "assessment"` (see [Milestones and assessments](../SKILL.md#milestones-and-assessments)).

## The daily cap

The console shows at most **six** due items a day, shakiest first (lowest box, then most overdue). Whatever else is due waits, unseen. Twenty prompts on screen reads as a verdict on the learner; six reads as today's work. Mirror this in the terminal: run the six the console shows, not the whole backlog.

## Reviewing (the session ritual)

At the start of every session, compute **due** items (`due` ≤ today) and clear the day's share *before* teaching anything new. Run each as a real retrieval attempt — pose the `prompt`, let the learner answer from memory, then reveal `recall`. Grade in three steps, then move the box and reset `due`:

| Grade | Meaning | Box change | New `due` |
|-------|---------|-----------|-----------|
| `weak`   | forgot, or got there with real effort | ask *when* they want it back — tomorrow, in a few days, or in a week → box 1, 2 or 3 | today + that box's interval |
| `good`   | produced it, with a pause | box + 1 (max 6), silently | today + new box's interval |
| `strong` | produced it at once, cleanly | box + 2 (max 6), silently — and if it was already in box 5 or 6, **retire it** and say so | today + new box's interval |

Ask *when*, never *whether*: a weak answer is precisely the one that must come back, and offering "or not at all" invites the learner to choose to forget. A strong answer needs no question at all — it moves out of sight on its own, and after enough of them it leaves for good.

Always set `due` from **today**, not from the old due date, so a queue left untouched for a while doesn't avalanche. Then rewrite `reviews.js`.

## Backlog triage

After a gap — a week away, a run of sessions that skipped the ritual — do not march the learner through everything that piled up. Triage it in the terminal, out loud: **merge** items that have grown into one idea, **retire** what they plainly own, and **spread** the rest over the coming weeks by setting staggered `due` dates so no single day carries more than the cap. "Twenty-three came due while you were away; we'll do six today and I've spread the rest over the next two weeks" is the whole conversation. The learner sees six.

## Retiring an item

Retire an item when it is graded `strong` from box 5 or 6, or when the learner clearly owns it for good. Tell them it is gone — that is a visible win. Note the retirement in a checkpoint if it marks real progress toward the Goal.

## Rules

- **Atomic.** One prompt, one thing to recall. Compound items lapse and don't tell you why.
- **Proposed, not imposed.** The learner has the last word on what enters the queue, except assessment misses.
- **Reschedule from today.** Never from the stored due date.
- **Seed from practice, not prose.** Prefer items the learner had to *generate*, not passively read.
- **Keep it lean.** 1–3 items a lesson; six a day on screen. A queue of hundreds is a signal you are keeping trivia — retain what serves the Goal, let the rest go.
