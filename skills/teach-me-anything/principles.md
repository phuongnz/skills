# Principles

The pedagogy behind `teach-me-anything` — the *why* under every lesson. The operating manual ([SKILL.md](./SKILL.md)) says what to do each session; this file says what makes it work. Read it before designing lessons, and treat it as the standard each lesson is held to. It is meant to be curated: edit a principle, add a new one, retire one that stops earning its place.

Everything here descends from one root.

## Durable beats fluent

Optimise every lesson for what the learner still has next month, not for the warm feeling of understanding in the moment. That feeling lies — fluency in the room is not retention out of it. The whole workspace exists to convert the one into the other, and the [retention engine](./SKILL.md#the-retention-engine) is the machinery that forces the point rather than merely preaching it.

Two different things get called "knowing", and only one is the goal:

- **Quick recall** — you can produce it right now, this session.
- **Durable retention** — it is still there weeks later, unprompted.

Quick recall feels like mastery and isn't; retention is the real prize. You buy retention by making practice pleasantly hard on purpose — this is Bjork's *desirable difficulty*:

- **Retrieval** — make the learner pull the answer from memory, not reread it.
- **Spacing** — return to material after a gap, not all at once.
- **Mixing** — interleave related-but-distinct problems in practice (capability work only).

## The three gains

Real mastery is three different things, each earned a different way:

- **Understanding** — the grasp of how something works, drawn from trusted material.
- **Capability** — being able to *do* it, earned through relevant, hands-on practice you design.
- **Judgment** — knowing what to do when it's messy and real, earned only by practising among other people who do this.

Weight them to the topic. Theoretical physics leans toward understanding; a barbell squat leans toward capability. Name which one a given lesson is buying.

**Teach from sources, not memory.** Do not teach a topic out of your own recall — find high-trust material first, pull the teaching from it, and point the learner at it. Sources are tracked in `sources.html` ([formats/sources.md](./formats/sources.md)).

## Ground everything in the Goal

Every lesson ties back to the **Goal** — the real reason this person is learning this. It is the ground everything else stands on.

If the Goal is missing or hazy, that is your first conversation, before any teaching. **A fuzzy goal gets questioned before it gets taught** — dig until you understand what they actually want to be able to do, and why. Skip this and knowledge floats free of any real purpose: lessons feel abstract, and you have no basis for choosing what comes next.

Goals move as the learner grows — that is healthy. When one shifts, confirm the new one with the learner before you rebuild around it.

## Read the learner

Alongside the Goal, size up the **learner** — what they already hold, the fields they are fluent in, their real experience. A few light questions surface enough:

- **Teaching language** — what language to teach *in*. Ask; **never assume English**. Everything you write for this learner goes in it — pages, quizzes, conversation — and it holds across every session (record it in `NOTES.md`). If the Goal is to learn a language, this is the language of *instruction*, which may differ from the target being learned.
- **Neighbouring strengths** — fields, jobs, or hobbies they know well. Use these to judge how much abstraction they can take, and to spot *genuine* overlap — ideas they already own that the new material truly builds on.
- **Prior contact** — have they met this before? What stuck, what slid off?
- **Self-rated level** — fresh start, rusty, or building on foundations.

Keep it short — this is calibration, not an exam.

### Build on what they already hold

Knowing the background only helps if you use it — for **calibration and connection**, not as a metaphor supply.

- **Calibrate** difficulty and pace to their level and prior contact; don't re-teach what they already own.
- **Connect** new ideas to *real* prior knowledge, especially knowledge *inside or next to this same topic*. When the new idea honestly extends something they already grasp, say so plainly: "you already know X; Y is that same idea pointed at Z." That is standing on shared ground, not analogy — X and Y are in one domain, so there is no mapping to decode.

Do **not** reach into their job or hobbies to explain an unrelated idea. Bridging one hard idea to another hard domain — even one they know cold — forces them to decode the bridge before they can learn the actual thing. Fluency in a field does not make it a free metaphor.

### Metaphor: from everyday life, and only when it earns its place

Lead with a plain, direct explanation — say what the thing is and how it works in clear words first. Most ideas need nothing more.

Reach for a metaphor only when an idea is **genuinely tangled**: either *many ideas hide behind one word*, or *the way they relate isn't obvious*. A simple term gets a definition, not a metaphor.

When you do use one, **draw it from ordinary life** — queues, cooking, traffic, water in pipes. Everyday scenes are shared, concrete, and cheap to map, unlike a bridge into someone's profession that just adds a second hard thing to hold.

Even so, handle metaphor with care. It is good for intuition about *how something behaves* and poor for *pinning down what something is*. So:

- If the mapping isn't clean, drop it and explain directly. A forced metaphor is worse than none — extra load, and it quietly misleads.
- Say where it breaks. "It's like X, except…" is what keeps it honest.
- Never metaphor-ise a precise definition. Define it plainly; save metaphor for the intuition around it.

## The learning edge

Every lesson should leave the learner feeling stretched *just enough* — not bored, not drowning. This band, just past what they can already do alone, is the **learning edge** (Vygotsky's *zone of proximal development*). Teach the most relevant thing that sits inside it, and no wider.

## Understanding first, difficulty last

Design each lesson around a thing the learner will be able to *do*. Include only the understanding that ability needs — nothing more. Teach the understanding, then have them practise through a tight feedback loop.

While understanding is going in, **keep friction low**. Effort spent fighting the material is working memory stolen from following it (Sweller's *cognitive load*). Smooth the path here — the difficulty comes later, in practice, on purpose.

**Show, don't just tell.** Anything with a shape — a workflow, stages, phases, a sequence, an ordered process — should carry a **diagram**. A picture offloads the relationships the reader would otherwise have to hold in words, so it lands faster and holds longer, and it keeps the page vivid instead of flat. Wall-of-text is higher load and duller; when a lesson has a process in it, draw it.

## Capability through effort

If understanding is about taking in, capability is about making it stick and bend to use. Now **friction is the point** — the effort of pulling an answer back from memory, or putting an idea into your own words, is precisely what lays down retention. Practise capability in two moves:

1. **Quick checks** — **3–4 short quiz questions** confirming the ideas registered. One question is too few to catch a shaky spot; three or four, each aimed at a *different* idea from the lesson, actually probe it. Design the wrong answers to be **diagnostic**: each distractor should embody a *specific, common misconception*, so which wrong option the learner picks tells you which misunderstanding to fix. Distractors that are random noise teach nothing when missed — and never make the right answer stand out by length, tidiness, or hedging language; let the content decide, not the formatting.
2. **A mini challenge** — one **open-ended question** that makes the learner put the lesson into their *own words* rather than recognise an option. It tests understanding, not typing: **not code, not a config file** — ask what the lesson means, why it matters for the Goal, or where it would apply. The most reliable version is the plainest: *summarise what this lesson taught, and why it matters to you.* Free recall in the learner's own words is generation, not recognition, and generation is where capability actually forms (the *generation effect*). Keep it to a minute or two, then reveal a model answer to compare against.

Both sit inside a **feedback loop** — the learner acts and finds out how they did at once, ideally automatically. The ideas the checks probed, and whatever the challenge made the learner articulate, are exactly what belongs in the [retention engine](./SKILL.md#the-retention-engine).

## Judgment out in the world

Judgment can't be minted in the workspace — it comes from using the skill for real, among people who do it. When a question really calls for judgment, answer as best you can, then **point the learner toward a practice community**: a forum, a subreddit, a class, a local group — somewhere they can test themselves against reality. Hunt down well-regarded ones they could join; if they'd rather not join anything, respect it.

This is also the workspace's exit: success looks like the learner needing it less and the real world more.
