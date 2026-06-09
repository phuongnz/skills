---
name: context-manager
description: Analyze, reduce, and monitor Claude Code session context against a healthy "smart zone" (default 150k tokens, where quality stays high before context rot sets in). Use when the user wants to see how much of the smart zone is loaded at startup and the biggest consumers, decide whether to clean up (/clear vs /compact) or trim what loads every session (MCP servers, skills, memory, CLAUDE.md), pick/configure a status line, or set their own healthy window size. Triggers include "analyze startup context", "why is my context so big", "clean up context", "reduce context usage", "status line template", "configure statusline", "set healthy window", "smart zone size".
---

# Context Manager

## The smart zone (read this first)

This skill judges context against a **healthy window** — the "smart zone" — not the model's raw context window.

The raw window can be 200k or 1M, but model quality starts degrading (**context rot**) long before it fills. By default the smart zone is **150k tokens**: the band where recall, reasoning, and instruction-following stay sharp. Past it, quality falls off no matter how much window remains.

So every token under 150k is **gold** — that's the budget you actually do good work in. The whole point of this skill is to spend as little of it as possible on startup overhead, leaving the maximum smart-zone headroom for the real task. A 1M window does **not** mean you have 1M of *useful* room; it means you have ~150k of useful room and a long, lower-quality tail after it.

All percentages, verdicts, and bars in this skill are measured against the smart zone, not the raw window.

### The healthy window setting (used by every mode)

The smart zone size is configurable and persists across sessions in
`${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json` under the key `healthy_window_tokens`.

At the start of **any** mode, read it (default to 150000 if the file or key is absent):

```bash
cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json"
HW=$(jq -r '.healthy_window_tokens // 150000' "$cfg" 2>/dev/null || echo 150000)
echo "smart zone = ${HW} tokens"
```

If the value is the default 150k, say so (and that it's adjustable via Mode 4). If the user changed it, use their value everywhere and mention it.

## Four modes

Pick the one matching the user's request; if unclear, ask which using these exact labels:

1. **Analyze start up context** — what's loaded at session start, the top consumers, and a verdict measured against the smart zone.
2. **Clean up context** — recommendations for reclaiming smart-zone headroom. See [CLEANUP.md](CLEANUP.md).
3. **Status line templates** — 4 ready-to-use templates (Essentials / Extended / smart-zone bar / Dashboard) or a custom one. See [STATUSLINE.md](STATUSLINE.md).
4. **Set healthy window size** — change the smart-zone threshold this skill measures against.

This skill never runs `/clear`, `/compact`, or edits user settings without confirming first — those are the user's calls.

## Mode 1 — Analyze start up context

**Goal:** report total startup context, the top 5 components, how much of the **smart zone** it spends, and whether it's worth cleaning up.

### Step 1 — Get the breakdown (hybrid: prefer exact, fall back to estimate)

First read the healthy window `HW` (see above). Then try these in order; stop at the first that yields a `/context` breakdown.

1. **Exact — already in conversation.** If a `/context` breakdown is visible in this conversation, parse it directly.
2. **Exact — from the transcript (hands-off).** Find the newest session transcript and pull the last `/context` block from it, so the user needn't do anything:
   ```bash
   proj=$(echo "$PWD" | sed 's/[^a-zA-Z0-9]/-/g')
   f=$(ls -t "$HOME/.claude/projects/$proj"/*.jsonl 2>/dev/null | head -1)
   [ -z "$f" ] && f=$(ls -t "$HOME/.claude/projects"/*/*.jsonl 2>/dev/null | head -1)
   grep -al "Context Usage" "$f" 2>/dev/null
   ```
   The project dir name is the cwd with every non-alphanumeric char turned into `-` (so `_` and `/` both become `-`); the glob fallback covers cases where that derivation misses. Read the tail of that file, locate the **last** `Context Usage` block, strip ANSI escapes, and parse the total and per-category token counts. If no block exists (user never ran `/context` this session), move on.
3. **Exact — ask.** Ask the user to run `/context` (instant, free); its output then enters the conversation. Parse it for the total (`X / Y tokens`) and each category (System prompt, System tools, MCP tools, Memory files, Skills, Messages, Free space).
4. **Estimate (last resort).** Only if no `/context` data is reachable. Approximate tokens ≈ characters ÷ 4 for the discretionary loadables, and label the result an estimate:
   - `CLAUDE.md` + `AGENTS.md` and any files they import (project root).
   - Global `~/.claude/CLAUDE.md` and `~/.claude/rules/*.md`.
   - `~/.claude/projects/<this-project>/memory/MEMORY.md` + memory files.
   - Each installed skill's `SKILL.md` frontmatter `description` (only the description loads at startup, not the body).
   - MCP server tool schemas (count tools × rough size, or note "loaded on demand" if deferred).
   - Add fixed overhead you can't trim: system prompt (~2–3k) + built-in tools (~5k loaded + deferred).

### Step 2 — Classify each component

- **Fixed** (cannot trim): System prompt, built-in System tools.
- **Discretionary** (the levers): MCP tools, Skills, Memory files, custom CLAUDE.md/AGENTS.md/global rules.

### Step 3 — Measure against the smart zone

Compute everything relative to `HW`, not the raw window:

- **Smart-zone spent at startup** = total startup tokens ÷ `HW`.
- **Smart-zone headroom left** = `HW` − total startup tokens (the gold you have left for actual work).
- Express each component's share as a % of the startup total (for ranking) *and* call out the discretionary total as a % of `HW`.

Judge **discretionary** load — that's the part you control, and every token of it is smart-zone budget burned before any work happens (thresholds shown as a share of a 150k smart zone; scale with `HW`):

| Discretionary startup load | Verdict |
|---|---|
| < 10k tokens (~7% of smart zone) | **Lean** — no action needed. |
| 10k–25k tokens (~7–17%) | **Moderate** — review whether every MCP server / skill is actually used. |
| > 25k tokens (>17%) | **Heavy** — trim it; point to [CLEANUP.md](CLEANUP.md). |

Then sanity-check **total** context against the smart-zone occupancy rubric (this is the headline number — it applies to the whole session, not just startup):

| Smart-zone occupancy (total ÷ `HW`) | State |
|---|---|
| < 50% (< 75k) | **Comfortable** — full quality, plenty of gold left. |
| 50–80% (75k–120k) | **Watch** — plan to `/compact` before the next big task. |
| 80–100% (120k–150k) | **Crowded** — compact or clear before continuing heavy work. |
| > 100% (> 150k) | **Past the smart zone** — context rot likely; `/clear` or `/compact` now. |

Remind the user: startup load is one-time and cache-friendly, but it permanently narrows the smart-zone headroom for the rest of the session. The bigger mid-session lever is **conversation growth** (`/compact` or `/clear`), covered in Mode 2.

### Step 4 — Report

Output, concisely:
- **Smart zone**: `HW` tokens (note if default or user-set).
- **Total startup context**: N tokens — **P% of the smart zone**, leaving ~H tokens of gold headroom. (Optionally also show it as a tiny % of the raw window to make the point that the raw window is misleading.)
- **Top 5 components** as a table: Component | Tokens | % of total | Fixed/Discretionary.
- **Verdict**: the discretionary rubric result + the smart-zone occupancy state + 1–3 specific, actionable recommendations (e.g. "context7 MCP is loaded on demand — good"; "5 unused skills add ~Xk of your gold 150k — consider removing").

## Mode 2 — Clean up context

Read `HW` first. Open [CLEANUP.md](CLEANUP.md). Frame everything as **reclaiming smart-zone headroom**: each fix buys back gold tokens under `HW`. Walk the 10 targets, flag the ones that apply to this session (use Mode 1's findings if available), and recommend the highest-impact fixes first. Confirm before anything destructive — especially `/clear`, which is irreversible.

## Mode 3 — Status line templates

Open [STATUSLINE.md](STATUSLINE.md). Offer the 4 templates (Essentials / Extended / smart-zone bar / Dashboard) or a custom one. Every template appends reasoning effort to the model label (`[Model·effort]`); Extended and Dashboard also show the 5-hour and 7-day rate-limit usage with time-to-reset. Prefer the **smart-zone bar** (Template 3) so the status line colors against `HW` (150k by default) with the green→yellow→orange→red gradient instead of the raw window — otherwise a 1M window shows green at 140k, hiding context rot. Write the script and edit `~/.claude/settings.json` only after showing the user what will change.

## Mode 4 — Set healthy window size (smart zone)

**Goal:** let the user change the smart-zone threshold every other mode measures against, and persist it.

1. **Read & report the current value** (the snippet under "The healthy window setting"). State whether it's the default 150k or a user-set value, and one line on what it means: "below this, quality stays sharp; above it, context rot degrades output."
2. **Get the new value.** If the user already gave a number in their request, use it. Otherwise offer sensible choices and let them pick or type a custom one:
   - **150k (default, recommended)** — the standard smart zone where most models hold quality.
   - **120k (conservative)** — for long, detail-sensitive work where you want to clear/compact earlier.
   - **200k** — for models/tasks where you've observed quality holds longer.
   - **Custom** — any token count.
   Accept shorthand like `150k`/`150000`; normalize to an integer of tokens. Reject non-positive or absurd values (e.g. < 10000 or > the raw window) and ask again.
3. **Confirm, then write** it to `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json`, preserving any other keys:
   ```bash
   cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json"; N=<tokens>
   tmp=$(mktemp)
   if [ -f "$cfg" ]; then
     jq --argjson v "$N" '.healthy_window_tokens = $v' "$cfg" > "$tmp" && mv "$tmp" "$cfg"
   else
     printf '{\n  "healthy_window_tokens": %s\n}\n' "$N" > "$cfg"
   fi
   jq . "$cfg"
   ```
   (If `jq` is unavailable, write the file directly and note it.)
4. **Confirm back**: the new smart zone is N tokens and now drives Modes 1–3. Offer to re-run Mode 1 against the new threshold.
