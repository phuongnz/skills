# Curriculum format

The **curriculum** is the external syllabus a workspace in [curriculum mode](../SKILL.md#two-modes-open-and-curriculum) has to cover — an exam blueprint, a course outline, a textbook's contents. It is not yours to invent, so it gets its own foundation page, `curriculum.html`, and that page is where the coverage lives: every milestone, every topic, and the state each topic is in. Open workspaces have no curriculum page; their outline stays in `NOTES.md`.

This is the Markdown that goes inside the `<script type="text/markdown">` block of `curriculum.html`. The learner reads it; you keep it current.

## Shape

```markdown
# Curriculum: <name of the exam, course, or syllabus>

**Source:** <link to the public blueprint, or the name of the file the learner gave you (kept in `curriculum/`)>
**Deadline:** <exam or course date, or "none">

## Milestones

### M1 — <title> (<weight>%)

| Topic | State | Lesson |
|-------|-------|--------|
| <topic as the syllabus names it> | open | — |
| <topic> | known | — |
| <topic> | taught | [0004](lessons/0004-vlans.html) |
| <topic> | shaky | [0004](lessons/0004-vlans.html) |

### M2 — <title> (<weight>%)
…
```

## Milestones

A milestone is one part, section, domain, or module of the syllabus — the unit the learner sees in the console's menu from day one, each with its status, so they always know what is done and what is coming. Its `id` is `m1`, `m2`, … in the order you will teach them; that id is what `MENU.milestones` and each lesson's `milestone` key point at.

- **Weight** is the share the syllabus gives it (an exam blueprint's percentage; for a course, a fair estimate). Weight drives *time*: a 25% domain gets roughly a quarter of the sessions. It does not drive order.
- **Order is your advice; the choice is the learner's.** A blueprint is a coverage list, not a teaching sequence. List milestones in the order that builds best for this learner, and say in `NOTES.md` why if it differs from the source — but the learner starts whichever they like from the console's menu, and you teach what they chose.
- **Status** lives in `MENU.milestones` (like the Goal's one line lives in `MENU.goalLine`), not here: `todo` → `active` when its first lesson is written → `passed` when its post-assessment holds, or `known` when the pre-assessment clears the whole thing. Keep the two in step.

## Topics and their state

Each milestone lists its topics as the syllabus names them — that is what the learner will be tested on. The **State** column is the fine-grained record of coverage:

| State | Meaning | Set when |
|-------|---------|----------|
| `open`   | not yet taught, not yet shown to be known | the page is created |
| `known`  | the learner already had it | the milestone's pre-assessment clears it — no lesson needed |
| `taught` | a lesson covered it | that lesson is done; link it in the Lesson column |
| `shaky`  | a post-assessment showed it did not hold | after the post-assessment; back to `taught` once a targeted lesson or review closes the gap |

`known` topics get no lesson, but they still appear in the post-assessment — clearing a pre-assessment is a claim, and the post-assessment checks it.

## Rules

- **Coverage, not a plan.** Every topic the syllabus names is listed, in the syllabus's words, so nothing is quietly skipped. The lesson-by-lesson plan stays where it was: written one lesson at a time, at the learning edge, inside the active milestone.
- **The syllabus is a source.** Cite it in `sources.html`. If the learner handed you a file, keep it in `curriculum/` (back of house) and name it under **Source**.
- **Deadline sets pace.** With a date, `NOTES.md` keeps the pace — milestones left against weeks left — and you say out loud when the learner is behind.
- **Edit the state, not the list.** Topics change state; they are not removed. If the syllabus itself changes (a new exam version), rewrite the page and log a checkpoint.
