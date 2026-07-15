# Instantiation registry

**What this is.** A catalog of **instantiation skills** — skills that *scaffold and run* a
design this skill produces (the compute + IaC, the datastore, the delivery gate, the
observability), as opposed to *deciding* the design, which is this skill's job. **Step 7** reads
this file to see whether a finished band design — whole, or in part — matches a skill that could
build it, and if so **proposes** it.

**The boundary this keeps.** This skill *designs*; it does not *build*. When a design lands on a
shape a registered skill already instantiates, the user shouldn't hand-build what's on the shelf
— but it stays a **proposal, human-gated**: this skill **never invokes** an instantiation skill.
Design → instantiate is a deliberate two-step.

**The matching contract.** Each entry describes its skill in *this skill's own vocabulary* —
runtime posture (tier / topology), delivery shape, data layer, tools, and which
**non-negotiables** it satisfies vs. leaves to you. To match, compare a band design (§4 of the
report) against an entry:

- **Whole-skill match** — the design's runtime + delivery + tools overlap the entry's signature
  **and** the entry satisfies that design's binding non-negotiables → propose the skill (with its
  install line).
- **Partial match** — only some of the design's needs are covered → propose the named **liftable
  parts** the entry lists, and say plainly what stays hand-built.
- **Non-coverage is mandatory to surface** — every entry lists what it does **NOT** cover; carry
  that into the proposal so the user sees the remaining work (a skill that stands up compute but
  not the backup/restore path leaves the *durable-state* non-negotiable with the user).
- **No match / empty registry** — say nothing is on the shelf; the design stands whole and is
  hand-built. **Never force a fit.**
- **Wanted (not yet built)** — entries under *§ Wanted* name a known gap that **no skill
  instantiates yet**. They carry **no `PROVIDES.md` and no install line**, so **never propose one
  as installable**. Their only use: when a design's *non-coverage* matches a wanted entry, say so
  in the report's *hand-build this separately* note — "a skill to close this is planned, not yet
  built" — so the gap is **tracked once**, not silently re-discovered every design.

Each skill's linked `PROVIDES.md` is the **authoritative** signature; the row here is a curated
summary — re-sync it from the source when the skill changes.

---

## Entries

*None registered yet.* No skill on the shelf instantiates a product-runtime design produced here.
Until one is added, step 7 says plainly that nothing is on the shelf and the design is hand-built
— it never forces a fit.

---

## Wanted (not yet built)

Known gaps a design keeps landing on that **no skill instantiates yet**. These are *signposts*,
not shelf items: **no install line, no `PROVIDES.md`** — step 7 must never propose them as
installable. Their job is to make a recurring non-coverage **visible**, so the report's
*hand-build this separately* note can say "planned, not yet built" instead of rediscovering the
same gap every time.

*(No wanted entries yet. Add one here the first time a product-runtime design lands on a recurring
non-coverage — e.g. an IaC-plus-delivery-gate scaffold — so the gap is tracked once.)*

---

## Adding a new instantiation skill
1. In the new skill, author a `PROVIDES.md` — its coverage signature in the shape above: what it
   instantiates, its facet table, non-negotiables satisfied, liftable parts, what it does **NOT**
   cover.
2. Add one entry here summarizing that `PROVIDES.md` and linking to it, with its source repo +
   install line.
3. **Nothing in `SKILL.md` changes** — step 7 reads this file. The skill is *closed for
   modification, open for extension*: growth is new rows here, never new logic there.

**Promoting a wanted entry.** When a skill under *§ Wanted* actually gets built, run the three
steps above and **remove its wanted stub** — a gap is tracked once, either as a want or as a
shelf item, never both.
