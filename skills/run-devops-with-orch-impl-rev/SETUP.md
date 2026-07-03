# Setup — installing the machinery into a repo

One-time, per repo. After this, a Claude Code session opened in the repo boots as the
orchestrator and you tell it *"boot and drain the queue."* What the workflow *is* →
[`SKILL.md`](SKILL.md); *why* each rule exists → [`FIELD-NOTES.md`](FIELD-NOTES.md).

## Prerequisites

- A GitHub repo you control (**private** — untrusted-input handling is deferred; see
  `STATE-MACHINE.md` "Not yet handled").
- `gh` authenticated as **you** (`gh auth status`), `node` available, a test command that
  exits non-zero on failure.
- Ability to create **two GitHub Apps** (the two bot identities). They must be *different*
  Apps — `reviewer ≠ author` at the identity level is what buys unattended merge.

## 1. Drop the machinery into the repo

Copy this skill's `scripts/*` into a namespaced dir at the repo root:

```bash
mkdir -p .orchestrator
cp <this-skill>/scripts/app-token.js <this-skill>/scripts/setup-labels.sh \
   <this-skill>/scripts/seed-backlog.sh <this-skill>/scripts/bot-env.example .orchestrator/
```

Add to the repo's `.gitignore` (secrets + machine-local files never get committed):

```gitignore
.orchestrator/.bot-env.*
*.pem
.claude/settings.local.json
```

## 2. Deposit the config + bootstrap stanza into CLAUDE.md

Append this block to the repo's `CLAUDE.md` (create it if absent). It is both the
**bootstrap** — how a fresh session picks up the orchestrator role — and the **project
config** every playbook reads. Fill in the five values:

```markdown
## Orchestrator config

A Claude Code session opened in this repo is the **orchestrator** for the
orchestrator · impl · review delivery loop. Follow the skill
`run-devops-with-orch-impl-rev` (invoke it, or read its `SKILL.md`), run its boot/recovery
sequence, then: **"boot and drain the queue."**

- Default branch: `main`
- Test command: `npm test`
- Write-scope (a build may write ONLY these): `src/**`, `test/**`
- impl-bot login: `<your-impl-bot>[bot]`
- review-bot login: `<your-review-bot>[bot]`
- Repo: `owner/repo`
```

## 3. Create the labels (the bus)

```bash
bash .orchestrator/setup-labels.sh
```

## 4. Wire CI — the merge gate

CI is the **source of truth for merge**; without it there is no gate. Ensure a required
check runs your test command on every PR. Minimal example (`.github/workflows/ci.yml`):

```yaml
name: CI
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: <your test command>   # must exit non-zero on failure
```

Ship (CD) is optional and may start as a **stub** that fires on merge to the default branch —
the state machine models `deploying → shipped/deploy-failed` regardless. Verify CI is live by
opening any PR and confirming the check runs. *(Beware unquoted `:` in a `run:` value — it
breaks the YAML and the run never starts; see `FIELD-NOTES.md`, Trap 4.)*

## 5. Create the two bot identities

Create two GitHub Apps (Contents/PR/Issues permissions — least privilege: impl-bot gets
Contents+Issues **write**, review-bot gets Issues **read-only**, since its verdict lives on the
PR — see `FIELD-NOTES.md`). **Install each App on the repo.** Then, for each role, copy
`.orchestrator/bot-env.example` to the real gitignored file and fill it in:

```bash
cp .orchestrator/bot-env.example .orchestrator/.bot-env.impl     # fill with impl-bot's App
cp .orchestrator/bot-env.example .orchestrator/.bot-env.review   # fill with review-bot's App
```

Confirm each mints a token: `set -a; source .orchestrator/.bot-env.impl; set +a; node .orchestrator/app-token.js`
should print a token. **Never commit** `.bot-env.*` or the `.pem` keys.

## 6. Pre-authorize the toolkit (permissions ≠ gates)

An "unattended" run isn't autonomous by default: every subagent bash call hits an interactive
permission prompt, and a **background subagent can't answer one**. Pre-allow the whole routine
toolkit in machine-local `.claude/settings.local.json` (gitignored). Two structural wins fall
out of scoping it precisely: **scope writes to the write-scope globs only**, and **deny the Read
tool on secrets**. Adapt the globs to your project config:

```json
{
  "permissions": {
    "allow": [
      "Bash(gh issue:*)", "Bash(gh pr:*)", "Bash(gh run:*)", "Bash(gh label:*)",
      "Bash(git checkout:*)", "Bash(git fetch:*)", "Bash(git push:*)",
      "Bash(git add:*)", "Bash(git commit:*)", "Bash(git revert:*)",
      "Bash(npm test:*)", "Bash(node .orchestrator/app-token.js:*)",
      "Edit(./src/**)", "Write(./src/**)", "Edit(./test/**)", "Write(./test/**)",
      "Read(./**)"
    ],
    "deny": [
      "Read(./.orchestrator/.bot-env.*)",
      "Read(./**/*.pem)"
    ]
  }
}
```

**But permissions are NOT your human gates.** The critical-merge and big-approach gates are
enforced by the orchestrator *stopping to ask you*, never by a withheld permission. Pre-allow
generously (even `gh pr merge`) and keep the judgment gates in the loop. *(Full reasoning +
the per-step responsibility × tools × permission matrix: `FIELD-NOTES.md`, Trap 5.)*

## 7. Get work into the queue

For a **real project**: file issues, then triage each with `TRIAGE-RUBRIC.md` and label it
`ready-for-impl` + `triage:*` + `attempt-1`. The issue **body is the spec**; comments are the
hub. Nothing reads a `backlog/` file at runtime — the issue is the single source of truth.

For a **smoke test** (prove all three gates fire): `bash .orchestrator/seed-backlog.sh` files
one demo issue per triage branch — but replace each body with a real spec before building.

## Run

Open a Claude Code session **in the repo** — `CLAUDE.md` bootstraps it as the orchestrator —
then: **"Boot and drain the queue."** It boots, drives the loop, and stops at each human gate
or when the queue is empty.

## Recovery (session died / new machine)

State lives in GitHub labels, so just open a fresh session — the boot/recovery sequence in
`SKILL.md` reconstructs and reconciles state. Two things must exist **on the machine** first
(gitignored, never in the repo): the bot creds (`.orchestrator/.bot-env.{impl,review}` + the
two `.pem` keys) and the permission allow-list (`.claude/settings.local.json`).

## What a good run proves

- **`triage:auto`** rides all the way to `shipped` with no human gate.
- **`triage:critical`** pauses for your approval **at merge**.
- **`triage:big`** pauses for your approval **before build** — and a thin spec should trip the
  implement agent's "restate first" step even if it somehow isn't gated.
- A deliberately broken PR gets **REQUEST_CHANGES** and/or a red CI, and never merges.
- Every artifact is attributable: impl-bot authored, review-bot approved, you merged.
