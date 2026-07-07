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
    added: "2026-07-05"                 // ISO date it entered the queue
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

## Adding an item

When a lesson introduces something worth keeping (usually whatever the [mini challenge](../principles.md#capability-through-effort) made the learner produce):

- `box: 1`, `due:` = today **+ 1 day**, `added:` = today.
- Keep `prompt`/`recall` atomic — one idea, answerable in a breath. Split anything bigger into several items.

## Reviewing (the session ritual)

At the start of every session, compute **due** items (`due` ≤ today) and clear them *before* teaching anything new. Run each as a real retrieval attempt — pose the `prompt`, let the learner answer from memory, then reveal `recall`. Grade, then move the box and reset `due`:

| Grade | Box change | New `due` |
|-------|-----------|-----------|
| `forgot` | → box 1 | today + 1 day |
| `hard`   | stay in box | today + this box's interval |
| `good`   | box + 1 (max 6) | today + new box's interval |
| `easy`   | box + 2 (max 6) | today + new box's interval |

Always set `due` from **today**, not from the old due date, so a queue left untouched for a while doesn't avalanche. Then rewrite `reviews.js`.

## Retiring an item

When an item reaches box 6 and is graded `easy` again — or the learner clearly owns it for good — you may drop it from the queue. Note the retirement in a checkpoint if it marks real progress toward the Goal.

## Rules

- **Atomic.** One prompt, one thing to recall. Compound items lapse and don't tell you why.
- **Reschedule from today.** Never from the stored due date.
- **Seed from practice, not prose.** Prefer items the learner had to *generate*, not passively read.
- **Keep it lean.** A queue of hundreds is a signal you are keeping trivia — retain what serves the Goal, let the rest go.
