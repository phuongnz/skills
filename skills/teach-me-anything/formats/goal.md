# Goal format

The **Goal** is the reason this learner is here. It grounds every lesson, and it is the first thing you settle. Keep it honest and specific — a vague Goal produces abstract lessons.

This is the Markdown that goes inside the `<script type="text/markdown">` block of `goal.html`.

## Shape

```markdown
# Goal: <topic>

**One line:** <a single sentence naming what the learner wants to be able to do, and why>

## What success looks like
<A concrete picture of the learner having arrived. Not "understand React" but
"ship a small app my team actually uses." Prefer things you could watch them do.>

## Why it matters to them
<The real driver behind the topic — the job, the project, the itch, the deadline.
This is what lets you judge what to teach next and keep lessons from floating.>

## Constraints & context
<Timeframe, budget, tools they must use, how much time per week, anything that
bounds the teaching.>

## Out of scope (for now)
<What this Goal deliberately does not cover, so lessons stay focused.>
```

## Rules

- The **one line** also lives in `index.html` as `MENU.goalLine`. Keep the two in step.
- Write success as something observable, not a feeling. "Can hold a five-minute conversation," not "feel confident in French."
- Goals shift as the learner grows. When one does, rewrite this document, update `MENU.goalLine`, and log a checkpoint noting the change — after confirming it with the learner.
