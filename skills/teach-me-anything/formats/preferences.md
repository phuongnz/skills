# Preferences format

`preferences.js` holds the choices the learner makes on `preferences.html`: how review runs, how lessons are shaped, how a session opens. It is the one place these settings live. The console reads it to draw the review panel, you read it at the start of every session, and the page rewrites it when the learner presses **Save**.

Every default is the skill's own behaviour, so a page nobody has touched changes nothing. Nuance that no setting captures — tone, formats they love or hate, a bad day — still goes to `NOTES.md` under **Learner preferences**.

## Shape

```js
window.PREFS = {
  "review": "daily",
  "reviewCap": 6,
  "practice": "checks-and-summary",
  "lessonLength": "standard",
  "opener": "recap",
  "feedback": "few-lessons",
  "language": "English"
};
```

After `window.PREFS =` the object is **strict JSON** — quoted keys, no comments, no trailing commas. The server reads it back to tell you what changed, and rewrites the whole file on save.

In curriculum mode, add `"hoursPerWeek"` (a number) and `"targetDate"` (`YYYY-MM-DD`, or `""` for none) at setup. The page shows its pace section only when these keys exist.

## What each setting does

| Setting | Values, default first | The console | You |
|---|---|---|---|
| `review` | `daily`, `optional`, `off` | `daily`: the **Due for review** panel with its count and list. `optional`: a quiet **Review** button, no count, no list. `off`: no panel. | `daily`: the [retention ritual](../SKILL.md#the-retention-engine) opens every session, before new material. `optional`: never open with it. Run it when they ask, the day's share, shakiest first. `off`: no ritual, and no review items proposed after lessons. |
| `reviewCap` | `6`, `3`, `10` | The most items the panel shows and its **Review** button runs. | The most items one pass runs, and the daily load [backlog triage](./reviews.md#backlog-triage) spreads to. |
| `practice` | `checks-and-summary`, `checks-only` | — | `checks-only`: a lesson ends after its quick checks; leave out the mini-challenge block. Review candidates are then only the ideas a check caught them out on. A doing topic still gets its drill. |
| `lessonLength` | `standard`, `short` | — | `standard` is about 10 minutes, `short` about 5. Short means split sooner: one idea per lesson, never two. |
| `opener` | `recap`, `straight` | — | `recap`: open each session with two lines, where they are and what today holds. `straight`: the first thing you say is the first thing to do. |
| `feedback` | `few-lessons`, `every-lesson`, `when-asked` | — | `few-lessons`: the [feedback conversation](../SKILL.md#the-feedback-conversation) on its usual rhythm. `every-lesson`: one line at the end of each lesson. `when-asked`: no scheduled check-ins at all. |
| `language` | from the diagnostic | — | Every new page in it, labels included. Pages already written stay as they are unless the learner asks for them translated. Keep `NOTES.md`'s **Teaching language** in step. |
| `hoursPerWeek`, `targetDate` | curriculum mode only | — | Recompute the `Budget:` and `Lessons left:` lines in `NOTES.md` in the same session ([pace](../SKILL.md#two-modes-open-and-curriculum)). |

## Review dates are kept in every mode

A preference changes how review is **offered**, never what the queue records.

- `optional`: an item nobody reviewed keeps its `due` date. Do not reschedule it as `good` — nothing was retrieved. When the backlog passes about three days' worth, triage it as usual.
- `off`: leave `reviews.js` as it is, dates and all, and add nothing to it — not even a post-assessment miss; the re-take covers that. When review comes back on, triage the backlog first.

## When the learner saves

Served, the page types one line into your drawer:

`[console] I saved my preferences: review daily → optional, reviewCap 6 → 3. Now in preferences.js.`

The console's review panel has already changed by then. Answer in one or two lines: what changes and from when — a lesson-shape change starts with the next lesson. Record it in `NOTES.md` under **Learner preferences** with the date, and write a `preference` [checkpoint](./checkpoint.md) when it is not obvious (review turned off, say). The page itself states the cost of turning review off, so do not argue it again.

Off disk there is no server: the page shows the learner a line to pass on, and you write `preferences.js` from it.

## Rules

- **The page and the file agree.** When the learner states in conversation something one of these settings captures — "stop opening with reviews" — change `preferences.js` too, and say so. Otherwise the page contradicts what you do.
- **Never change a setting on your own judgment.** Suggest it, and let the learner tick it or tell you.
- **Read it every session.** A setting saved between sessions is still a setting.
