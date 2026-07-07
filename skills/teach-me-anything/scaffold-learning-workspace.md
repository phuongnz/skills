# Scaffolding a learning workspace

One-time setup. Run this the first time you land in an empty workspace (no `index.html`); after that the workspace is built and you can ignore this file. The anatomy of what you are creating — every file and what it is for — is in [SKILL.md → The Learning Workspace](./SKILL.md#the-learning-workspace).

## Stand up the workspace

1. Copy this skill's `assets/` into the workspace (the shared `style.css` and `md.js`; leave them untouched per workspace).
2. Copy `templates/dashboard.html` to `index.html`, and `templates/reviews.js` to `reviews.js` (the retention queue, starts empty).
3. Create `goal.html`, `glossary.html`, and `sources.html` from `templates/doc.html`.
4. Fill in the `MENU` object in `index.html` — the topic and a one-line Goal. Lessons and cards start empty and grow.
5. Create `lessons/`, `reference/`, and `checkpoints/` only when you write the first of each.

## Then open with the diagnostic

Before designing a single lesson, run the opening conversation — it sets everything that follows:

- **Settle the teaching language.** Ask what language to teach *in* — **never assume English**. Record it in `NOTES.md`, then write every page (foundations, lessons, cards) *and the templates' visible labels* (the eyebrows, "Quick check", buttons, the console's "Due for review" / "Start self-test", etc.) in it, and set each page's `<html lang>` to match. If the Goal is to learn a language, this is the language of *instruction*, distinct from the target. The pedagogy: [principles.md → Read the learner](./principles.md#read-the-learner).
- **Settle the Goal.** Why is this learner here, and what do they want to be able to do? Record it in `goal.html` ([formats/goal.md](./formats/goal.md)), and keep its one line in step with `MENU.goalLine`. The pedagogy: [principles.md → Ground everything in the Goal](./principles.md#ground-everything-in-the-goal).
- **Read the learner.** Prior contact, self-rated level, neighbouring strengths. Write it as the first checkpoint (type `background`, [formats/checkpoint.md](./formats/checkpoint.md)) so every later session inherits it. The pedagogy: [principles.md → Read the learner](./principles.md#read-the-learner).

If you can, open `index.html` for the learner with a shell command. From then on, the console is their front door, and you are into the normal teaching loop in [SKILL.md](./SKILL.md#how-a-session-goes).
