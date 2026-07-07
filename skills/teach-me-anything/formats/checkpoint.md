# Checkpoint format

A **checkpoint** is a short, private record of what the learner has actually taken on board — and any non-obvious insight worth revisiting. It is the learning equivalent of an engineering decision log: it captures the things that were true at a moment and may need revising later. Checkpoints are how you find the [learning edge](../principles.md#the-learning-edge) next session.

Checkpoints are **back of house** — plain Markdown in `checkpoints/`, never shown to the learner. Name them `0001-<dash-case-name>.md`, the number rising each time.

## Shape

```markdown
# <NNNN> — <short title>

- **Date:** <YYYY-MM-DD>
- **Lesson:** <link to the lesson this came from, if any>
- **Type:** learned | insight | struggle | preference | goal-change | background

## What happened
<One or two sentences. What was taught, or what you learned about the learner.>

## What they now hold
<What you believe the learner can now do or explain, honestly. Distinguish quick
recall ("got it today") from durable retention ("still had it after a gap").>

## Open / to revisit
<What's shaky, what to circle back to, what to space out for review, and roughly
when. This drives future sessions.>
```

## Rules

- Write one whenever something non-obvious happens: a concept lands, a concept won't land, the learner reveals a preference or a strength, or the Goal moves.
- Always write the **first** checkpoint after the opening diagnostic (type `background`): the learner's prior knowledge, level, and neighbouring strengths. Later sessions inherit it.
- Be honest about **durable vs quick** — don't record a fluent-in-the-moment answer as mastery. Note when something is due for spaced review.
- Keep them short. A checkpoint is a signal for future-you, not a transcript.
