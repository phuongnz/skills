---
name: context-manager
description: Analyze, reduce, and monitor Claude Code session context against a healthy "smart zone" (default 150k tokens, where quality stays high before context rot sets in). Use when the user wants to see how much of the smart zone is loaded at startup and the biggest consumers, decide whether to clean up (/clear vs /compact) or trim what loads every session (MCP servers, skills, memory, CLAUDE.md), pick/configure a status line, or set their own healthy window size. Triggers include "analyze startup context", "why is my context so big", "clean up context", "reduce context usage", "status line template", "configure statusline", "set healthy window", "smart zone size".
---

# Context Manager

## The smart zone (read this first)

This skill judges context against a **healthy window** — the "smart zone" — not the model's raw context window.

The raw window can be 200k or 1M, but model quality starts degrading (**context rot**) long before it fills. By default the smart zone is **150k tokens**: the band where recall, reasoning, and instruction-following stay sharp. Past it, quality falls off no matter how much window remains. So every token under the smart zone is **gold** — that's the budget you actually do good work in, and the point of this skill is to spend as little of it as possible on startup overhead.

All percentages, verdicts, and bars here are measured against the smart zone, not the raw window.

**The healthy-window setting (used by every mode).** The smart-zone size persists in `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json` under `healthy_window_tokens`. At the start of **any** mode, read it by running the bundled helper (alongside this SKILL.md):

```bash
bash scripts/read-window.sh   # prints the token count, default 150000
```

If it's the default 150k, say so (and that Mode 4 can change it). If the user set a custom value, use it everywhere and mention it.

## Four modes

Pick the one matching the user's request; if unclear, ask which using these exact labels:

1. **Analyze startup context** — what's loaded at session start, the top consumers, and a verdict against the smart zone.
2. **Clean up context** — recommendations for reclaiming smart-zone headroom. See [CLEANUP.md](CLEANUP.md).
3. **Status line templates** — 4 ready-to-use templates or a custom one. See [STATUSLINE.md](STATUSLINE.md).
4. **Set healthy window size** — change the smart-zone threshold this skill measures against.

This skill never runs `/clear`, `/compact`, or edits user settings without confirming first — those are the user's calls.

## Mode 1 — Analyze startup context

**Goal:** report total startup context, the top 5 components, how much of the **smart zone** it spends, and whether it's worth cleaning up.

### Step 1 — Get a fresh `/context` breakdown

Read the healthy window `HW` (`scripts/read-window.sh`). Then get the breakdown from `/context` — the skill cannot run `/context` itself, so:

- If a `/context` breakdown is already visible in this conversation, parse that.
- Otherwise, **ask the user to run `/context`** (instant, free) and wait for it. Tell them to **then send "ok" or "continue"** — the output only enters the conversation with their next message, and without that hint they'll wait on a skill that appears to do nothing.

Parse the result for the total (`X / Y tokens`) and each category: System prompt, System tools, MCP tools, Memory files, Skills, Messages, Free space. Don't estimate from file sizes — `/context` is the source of truth, and one keystroke from the user beats a guess.

### Step 2 — Classify each component

- **Fixed** (cannot trim): System prompt, built-in System tools.
- **Discretionary** (the levers): MCP tools, Skills, Memory files, custom CLAUDE.md/AGENTS.md/global rules.

### Step 3 — Measure against the smart zone

Compute everything relative to `HW`, not the raw window:

- **Smart-zone spent at startup** = total startup tokens ÷ `HW`.
- **Smart-zone headroom left** = `HW` − total startup tokens (the gold left for actual work).
- Express each component's share as a % of the startup total (for ranking), and the discretionary total as a % of `HW`.

Judge **discretionary** load — the part you control; every token of it is smart-zone budget burned before any work happens (thresholds shown as a share of a 150k smart zone; scale with `HW`):

| Discretionary startup load | Verdict |
|---|---|
| < 10k tokens (~7% of smart zone) | **Lean** — no action needed. |
| 10k–25k tokens (~7–17%) | **Moderate** — review whether every MCP server / skill is actually used. |
| > 25k tokens (>17%) | **Heavy** — trim it; point to [CLEANUP.md](CLEANUP.md). |

Then sanity-check **total** context against the smart-zone occupancy rubric (the headline number — it applies to the whole session, not just startup):

| Smart-zone occupancy (total ÷ `HW`) | State |
|---|---|
| < 50% (< 75k) | **Comfortable** — full quality, plenty of gold left. |
| 50–80% (75k–120k) | **Watch** — plan to `/compact` before the next big task. |
| 80–100% (120k–150k) | **Crowded** — compact or clear before continuing heavy work. |
| > 100% (> 150k) | **Past the smart zone** — context rot likely; `/clear` or `/compact` now. |

Remind the user: startup load is one-time and cache-friendly, but it permanently narrows the smart-zone headroom for the session. The bigger mid-session lever is **conversation growth** (`/compact` or `/clear`), covered in Mode 2.

### Step 4 — Report

Output, concisely:
- **Smart zone**: `HW` tokens (note if default or user-set).
- **Total startup context**: N tokens — **P% of the smart zone**, leaving ~H tokens of gold headroom.
- **Top 5 components** as a table: Component | Tokens | % of total | Fixed/Discretionary.
- **Verdict**: discretionary rubric result + smart-zone occupancy state + 1–3 specific, actionable recommendations (e.g. "context7 MCP is loaded on demand — good"; "5 unused skills add ~Xk of your gold 150k — consider removing").

## Mode 2 — Clean up context

Read `HW` first. This mode needs a `/context` breakdown to know what's actually loaded: if one is already visible in this conversation (e.g. from Mode 1), use it; otherwise **ask the user to run `/context`** and wait — same rule as Mode 1 (including the say-"ok"-or-"continue"-after hint), never hunt for it elsewhere. Then open [CLEANUP.md](CLEANUP.md). Frame everything as **reclaiming smart-zone headroom**: each fix buys back gold tokens under `HW`. Walk the 10 targets, flag the ones that apply to this session (use Mode 1's findings if available), and recommend the highest-impact fixes first. Confirm before anything destructive — especially `/clear`, which is irreversible.

## Mode 3 — Status line templates

Open [STATUSLINE.md](STATUSLINE.md). Offer the 4 templates (Essentials / Extended / smart-zone bar / Dashboard) or a custom one. Prefer the **smart-zone bar** so the status line colors against `HW` (150k by default) instead of the raw window — otherwise a 1M window shows green at 140k, hiding context rot. The templates are bundled as ready-to-run scripts under `scripts/`; apply one only after showing the user what will change.

## Mode 4 — Set healthy window size (smart zone)

**Goal:** let the user change the smart-zone threshold every other mode measures against, and persist it.

1. **Read & report the current value** (`scripts/read-window.sh`). State whether it's the default 150k or user-set, plus one line on what it means: "below this, quality stays sharp; above it, context rot degrades output."
2. **Get the new value.** If the user already gave a number, use it. Otherwise offer choices:
   - **150k (default, recommended)** — the standard smart zone where most models hold quality.
   - **120k (conservative)** — for long, detail-sensitive work where you want to clear/compact earlier.
   - **200k** — for models/tasks where you've observed quality holds longer.
   - **Custom** — any token count.
   Accept shorthand like `150k`/`150000`; normalize to an integer of tokens. Reject non-positive or absurd values (< 10000 or > the raw window) and ask again.
3. **Confirm, then write** it by running the helper (preserves any other keys; falls back to a fresh file if `jq` is missing):
   ```bash
   bash scripts/set-window.sh <tokens>
   ```
4. **Confirm back**: the new smart zone is N tokens and now drives Modes 1–3. Offer to re-run Mode 1 against the new threshold.
