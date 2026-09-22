# Scaffolding a learning workspace

One-time setup. Run this the first time you land in an empty workspace (no `index.html`); after that the workspace is built and you can ignore this file. The anatomy of what you are creating — every file and what it is for — is in [SKILL.md → The Learning Workspace](./SKILL.md#the-learning-workspace).

## Stand up the workspace

1. Copy this skill's `assets/` into the workspace (the shared `style.css` and `md.js`; leave them untouched per workspace).
2. Copy `templates/dashboard.html` to `index.html`, and `templates/reviews.js` to `reviews.js` (the retention queue, starts empty).
3. Create `goal.html`, `glossary.html`, and `sources.html` from `templates/doc.html` — and `curriculum.html` too, if the diagnostic below turns up a syllabus.
4. Fill in the `MENU` object in `index.html` — the topic and a one-line Goal. Lessons and cards start empty and grow; `milestones` stays empty unless the workspace is in curriculum mode.
5. Copy `templates/bin/` to `bin/` and keep the three scripts executable (`chmod +x bin/*`) — this is the [tutor terminal](./SKILL.md#the-tutor-terminal). Check `command -v ttyd`; if it is missing, tell the learner how to get it (`brew install ttyd`) rather than installing it for them. Without it the console still works, minus the drawer.
6. Create `lessons/`, `reference/`, `checkpoints/` — and, in curriculum mode, `assessments/` — only when you write the first of each.

## Then open with the diagnostic

Before designing a single lesson, run the opening conversation — it sets everything that follows:

- **Settle the teaching language.** Ask what language to teach *in* — **never assume English**. Record it in `NOTES.md`, then write every page (foundations, lessons, cards) *and the templates' visible labels* (the eyebrows, "Quick check", buttons, the console's "Due for review" / "Review" / "Show · Hide N questions" / "Tutor terminal" / "Open" · "Hide", the Review overlay's note, the drawer's offline hint, an assessment's "Show the answer" / "Did you have it?" / result lines, etc.) in it, and set each page's `<html lang>` to match. If the Goal is to learn a language, this is the language of *instruction*, distinct from the target. The pedagogy: [principles.md → Read the learner](./principles.md#read-the-learner).
- **Settle the Goal.** Why is this learner here, and what do they want to be able to do? Record it in `goal.html` ([formats/goal.md](./formats/goal.md)), and keep its one line in step with `MENU.goalLine`. The pedagogy: [principles.md → Ground everything in the Goal](./principles.md#ground-everything-in-the-goal).
- **Settle the mode.** Ask: *is there a syllabus or exam this has to cover?* If not, record `Mode: open` in `NOTES.md` and carry on. If there is, the workspace runs in [curriculum mode](./SKILL.md#two-modes-open-and-curriculum):
  - Get the syllabus. Public (a certification's exam topics, a course page) → fetch it and cite it in `sources.html`. A file from the learner → keep it as given in `curriculum/`.
  - Get the date, if any, into the Goal's constraints.
  - Build `curriculum.html` from it ([formats/curriculum.md](./formats/curriculum.md)): one milestone per part of the syllabus, in the order *you* would teach them, every topic listed in the syllabus's words, all `open`.
  - Fill `MENU.milestones` (one entry per milestone, all `status: "todo"`), add `{ href: "curriculum.html", title: "Curriculum" }` to `MENU.foundations`, and record `Mode: curriculum` plus the pace (milestones against weeks to the date) in `NOTES.md`.
- **Read the learner.** Prior contact, self-rated level, neighbouring strengths. Write it as the first checkpoint (type `background`, [formats/checkpoint.md](./formats/checkpoint.md)) so every later session inherits it. In curriculum mode keep this light — the pre-assessment before each milestone does the fine-grained reading, topic by topic, that no opening conversation can. The pedagogy: [principles.md → Read the learner](./principles.md#read-the-learner).

Then hand over the front door. First run `bin/study status`. If it prints an address, the console is already open in the learner's browser (a re-scaffold, or you are speaking through its drawer): tell them the console has their workspace and a **new content** badge on the page reloads it — do not tell them to run `bin/study`. Otherwise tell the learner to run `bin/study` **in their own terminal** — never launch it yourself ([why](./SKILL.md#the-tutor-terminal)). It opens the console with the tutor terminal in the drawer, and the drawer's `claude --continue` resumes this very conversation, so nothing from the diagnostic is lost. If they have no `ttyd`, open `index.html` for them with a shell command instead. From then on, the console is their front door, and you are into the normal teaching loop in [SKILL.md](./SKILL.md#how-a-session-goes).
