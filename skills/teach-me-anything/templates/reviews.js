/* Retention queue for this workspace — the spaced-review engine reads and rewrites this.
   Back of house: the tutor maintains it; the console's "Due" panel renders it.
   One entry per idea or micro-skill worth keeping. Schema + scheduling: ../formats/reviews.md

   Each entry:
     { id, prompt, recall, kind: "fact"|"skill", box: 1..6, due: "YYYY-MM-DD",
       lesson: "lessons/....html", added: "YYYY-MM-DD" }
   New items enter at box 1, due tomorrow. Boxes widen: 1d, 3d, 7d, 16d, 35d, 90d. */
window.REVIEW = [
  // Seeded from lessons as you teach. Example (delete once real items exist):
  // {
  //   id: "example-idea",
  //   prompt: "The question or cue shown first",
  //   recall: "What the learner should produce from memory",
  //   kind: "fact",
  //   box: 1,
  //   due: "2026-01-02",
  //   lesson: "lessons/0001-first.html",
  //   added: "2026-01-01"
  // },
];
