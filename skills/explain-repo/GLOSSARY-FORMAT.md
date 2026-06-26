# Glossary Format (`glossary.html`)

`glossary.html` is the canonical language for the atlas — the repo's own module names, abbreviations, and domain terms, defined once so every chapter uses them consistently. A newcomer's biggest tax is undefined vocabulary; this is where it's paid down.

It is built from [templates/doc.html](./templates/doc.html): the source of truth is the Markdown inside its `<script type="text/markdown">` block, which `assets/md.js` renders. Edit and read only that block — the structure below is exactly what goes in it.

## Structure

```md
# {Repo} Glossary

{One or two sentences naming the domain this glossary covers.}

## Terms

**Ingestor**:
The service under `cmd/ingest/` that pulls raw events off the queue and normalises them before persistence.
_Aka_: the consumer, the intake worker

**Tenant**:
A single customer account; the top-level isolation boundary for data and config. Every table carries a `tenant_id`.
_Aka_: org, workspace, account

**ULID**:
The 26-char sortable identifier used for all primary keys (see `pkg/id/`), preferred over UUID for index locality.
```

## Rules

- **Define what the repo actually says.** Glossary entries are terms that appear in the code, docs, or tracker — not generic CS vocabulary the reader already knows. Cite where the term lives when it helps (`cmd/ingest/`).
- **Be opinionated about aliases.** When the codebase uses several names for one thing, pick the dominant one and list the rest as `_Aka_`. This is how the atlas compresses language.
- **Keep definitions tight.** One or two sentences. Define what the term *is* in this repo, not the abstract concept.
- **Use the glossary's own terms inside definitions.** Once a term is defined, prefer it everywhere — including inside other definitions.
- **Group under subheadings** when natural clusters emerge (`## Services`, `## Data`, `## Build`). A flat list is fine when terms cohere.
- **Flag repo-local meanings.** If the repo uses a common word in an unusual way, note the resolution: "In this repo, 'job' always means a queue task, never a CI job."
- **Revise as understanding deepens.** Update entries in place; do not leave a stale definition behind once you've read the code that contradicts it.
