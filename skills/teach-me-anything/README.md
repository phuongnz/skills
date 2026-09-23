# teach-me-anything

A tutor that teaches you one topic across many sessions, in a small local **learning workspace** that remembers what you have learned and brings it back before it fades. Languages, programming, a certification, a craft — anything with a Goal behind it.

This file is for you, the learner. `SKILL.md` and the files beside it are the tutor's manual; you never need to read them.

## What you get

A folder that grows as you learn. You open one page in it — the **console** — and work from there:

- a menu of lessons, reference cards and foundation pages down the side, with a progress meter
- a **Due for review** panel: at most six things a day, the shakiest first, drawn from a spaced-review queue the tutor keeps
- the current lesson in the middle — short, one idea, a few quick checks, and a mini challenge where you summarise it in your own words
- the tutor in a **terminal drawer** along the bottom, the same conversation every day

Lessons are written from trusted sources, cite them, and tie back to your Goal. If there is a syllabus or exam behind the Goal, the workspace runs in **curriculum mode**: the syllabus becomes milestones with **Start** buttons, each opened by a short pre-assessment (what you already hold is skipped) and closed by a post-assessment (what actually stuck). It deliberately holds no exam simulation — practice exams are your own preparation, and the tutor books time for them.

## Prerequisites

- An agent CLI on your `PATH`: [Claude Code](https://claude.com/claude-code) (`claude`) or [Codex](https://github.com/openai/codex) (`codex`)
- [`ttyd`](https://github.com/tsl0922/ttyd) for the terminal drawer — `brew install ttyd`. Without it the console still works, minus the drawer.
- Python 3 (ships with macOS) for the local server
- macOS is where this has been tested. On Linux or Windows (WSL) the console and server should run as they are, but expect small adjustments — `bin/tutor-shell` in particular is written in `zsh`, and the tutor can adapt it to the shell it finds.

## Getting started

1. Install the skill, project-scoped, in an **empty folder** — one folder per topic:

   ```bash
   mkdir ~/learn-spanish && cd ~/learn-spanish
   npx skills add phuongnz/skills --skill teach-me-anything
   ```

2. Start your agent in that folder and say what you want to learn:

   ```
   claude
   > /teach-me-anything Spanish, enough to hold a conversation on a trip next spring
   ```

   The tutor asks a few questions — teaching language, your Goal, whether there is a syllabus, what you already know — and builds the workspace.

3. When it tells you to, run **in your own terminal** (not the agent's):

   ```bash
   bin/study
   ```

   It prints an address, opens the console in your browser, and puts the tutor in the drawer — resuming the conversation you just had. Ctrl-C ends the session; nothing is left running.

From the next day on, `bin/study` is the whole routine.

## Day to day

- **Clear what's due first.** The panel shows today's items; the tutor runs them with you in the drawer and reschedules each one by how it went. (The **Review** button on the page is an ungraded flip-through — handy, but only the tutor moves the dates.)
- **Then one lesson.** The tutor writes it, the page shows a blinking **new content** badge, you click it and the lesson appears — the drawer stays as it was.
- **Send to tutor.** Quick checks, short answers, your summary and assessments end in a button that hands your answers to the drawer. The tutor reads them and reacts.
- **Start buttons.** In curriculum mode you choose which milestone to open next; the tutor's suggested order is advice.
- Ask anything in the drawer, any time. Quit the tutor and you have a plain shell in the workspace for hands-on practice.

## Knobs

```bash
STUDY_PORT=9000 bin/study     # pick the port (default: one derived from the folder's path)
STUDY_AGENT=codex bin/study   # which agent tutors in the drawer (default: claude, then codex)
STUDY_AGENT="gemini -r" bin/study   # any command line
bin/study status              # prints the address if this workspace is already being served
bin/check-quiz lessons/0001-*.html  # what the tutor runs to keep quiz options from giving the answer away
```

## What is in the folder

Yours: `index.html` (the console), `lessons/`, `reference/`, `goal.html`, `glossary.html`, `sources.html`, `curriculum.html` and `assessments/` in curriculum mode.

The tutor's — plain text, read them if you are curious, but they are its working memory: `NOTES.md` (course outline, pace, decisions), `checkpoints/` (what it believes you hold), `reviews.js` (the review queue), `submissions/` (what you sent). `AGENTS.md` / `CLAUDE.md` tell any agent that starts cold here that it is the tutor.

The workspace is plain files. Back it up, put it in git, move it — nothing lives anywhere else.
