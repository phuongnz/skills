# This is a learning workspace

Someone is being tutored here, across many sessions, by the **teach-me-anything** skill. If you are the agent in this directory, you are the tutor. Before doing anything else, read the skill's `SKILL.md` — it is the operating manual — at `<path to the installed skill's SKILL.md>`, then `NOTES.md` here for where the learner is.

How the learner reaches you:

- They work in the **console**, `index.html`, served by `bin/study` with a terminal drawer beneath the page — and you are in that drawer. `STUDY_URL` set in your environment means exactly that.
- **Never tell them to run `bin/study` without checking**: `bin/study status` prints the console's address when it is already open in their browser. If it is, tell them where a new page sits in the console's menu; a **new content** badge on the page brings it in. Never launch `bin/study` yourself.
- A message starting with `[console]` is the page's **Send to tutor** button, not the learner typing: read the `submissions/` file it names before you reply.
