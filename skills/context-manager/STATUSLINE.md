# Status line templates

Claude Code runs a shell command after each message and pipes session JSON to it on stdin; whatever it prints becomes the status bar. The four templates are bundled as ready-to-run scripts under `scripts/` (alongside this file) — you apply one by **copying** it to `~/.claude/statusline.sh`, not by re-typing it.

The built-in `/statusline <description>` command also generates a script and wires up settings automatically — mention it as the fastest path if the user wants something bespoke.

All four scripts use `jq`. Check `command -v jq` first; if missing, suggest `brew install jq` (macOS). Every template shows the model with its reasoning effort appended as `[Model·effort]` (e.g. `[Opus·xhigh]`), falling back to `[Model]` when `effort.level` is absent.

| Template | Script | Shows |
|---|---|---|
| **1 Essentials** | `scripts/statusline-essentials.sh` | model · effort, context tokens (context %) |
| **2 Extended** | `scripts/statusline-extended.sh` | Essentials + 5-hour & 7-day rate-limit usage, each with time-to-reset |
| **3 Smart-zone bar** (recommended) | `scripts/statusline-smartzone.sh` | model · effort, smart-zone bar |
| **4 Dashboard** | `scripts/statusline-dashboard.sh` | line 1: model · effort, folder, branch · line 2: smart-zone bar, cost, net lines, 5h & 7d limits |

Renders:

```
1  [Opus·xhigh] 11.5k (8%)
2  [Opus·xhigh] 11.5k (8%) | 5h:23% (↻2h14m) | 7d:45% (↻3d4h)
3  [Opus·xhigh] ██████░░░░ 95k/150k smart zone (63%)
4  [Opus·xhigh] 📁 my-project | 🌿 main
   ██████░░░░ 95k/150k smart zone (63%) | $0.12 | 📝 +142 | 5h:23% (↻2h14m) | 7d:45% (↻3d4h)
```

## Why the smart-zone bar (3 & 4)

`context_window.used_percentage` is a share of the **raw** window (200k or 1M). On a 1M window that bar stays green at 140k tokens — right where context rot is already biting. The smart-zone scripts color against the healthy window (`healthy_window_tokens`, default 150k, read from the same config the skill uses) so the bar shifts through a gradient as quality actually starts to suffer. Four bands, keyed to smart-zone occupancy `SZPCT` (used tokens ÷ `HW`):

| Smart-zone occupancy (`SZPCT`) | Band | Color |
|---|---|---|
| ≤ 100% (within the smart zone) | comfortable | 🟢 green |
| 100–133% (up to smart zone + ⅓) | watch | 🟡 yellow |
| 133–166% (up to smart zone + ⅔) | crowded | 🟠 orange |
| > 166% (beyond smart zone + ⅔) | past it | 🔴 red |

The bar is mostly empty at low occupancy — that's the point: most of the smart zone should be headroom. `SZPCT` keeps climbing past 100% once you're past the healthy window — green→yellow→orange→red is your cue to compact or clear.

## Customizing — the most useful stdin fields

| Field | Meaning |
|---|---|
| `model.display_name` / `model.id` | Current model |
| `effort.level` | Reasoning effort (low…max, e.g. `xhigh`); absent if unsupported |
| `workspace.current_dir` / `workspace.project_dir` | Cwd / launch dir |
| `context_window.total_input_tokens` | Exact tokens in context (input + cache); best for a token count |
| `context_window.used_percentage` / `remaining_percentage` | Context used / left, as a share of the raw window (null early → `// 0`) |
| `context_window.context_window_size` | Window size (200000 or 1000000) |
| `cost.total_cost_usd` / `cost.total_duration_ms` | Session cost / wall-clock ms |
| `cost.total_lines_added` / `cost.total_lines_removed` | Lines changed |
| `rate_limits.five_hour.used_percentage` / `.resets_at` | 5-hour limit usage % and reset time (`resets_at` is epoch-seconds or ISO-8601); use `// empty` |
| `rate_limits.seven_day.used_percentage` / `.resets_at` | 7-day limit usage % and reset time; `seven_day_opus` / `seven_day_sonnet` variants also exist |
| `session_name` / `version` / `output_style.name` | Misc; `session_name` absent unless set |

Many fields are absent or `null` early on — always provide fallbacks (`// 0`, `// empty`). Keep output short; the bar has limited width. To tweak a template, copy its script and edit the copy.

## Applying a choice

1. **Confirm** which template, and that you'll write `~/.claude/statusline.sh` and add a `statusLine` entry to `~/.claude/settings.json`. If either exists, note it'll change and preserve the rest of settings.json (merge, don't overwrite).
2. **Copy** the chosen script and make it executable:
   ```bash
   cp scripts/statusline-<name>.sh ~/.claude/statusline.sh && chmod +x ~/.claude/statusline.sh
   ```
3. **Merge** into `~/.claude/settings.json`: `"statusLine": { "type": "command", "command": "~/.claude/statusline.sh" }`. Optional: `"padding": 2`, or `"refreshInterval": <seconds>` to keep the time-to-reset and wall-clock segments fresh.
4. **Test** before relying on it (this payload exercises tokens, effort, and both rate limits):
   ```bash
   N=$(date +%s); echo '{"model":{"display_name":"Opus"},"effort":{"level":"xhigh"},"workspace":{"current_dir":"'$PWD'"},"context_window":{"used_percentage":8,"total_input_tokens":11500,"context_window_size":1000000},"rate_limits":{"five_hour":{"used_percentage":23,"resets_at":'$((N+8040))'},"seven_day":{"used_percentage":45,"resets_at":'$((N+273600))'}},"cost":{"total_cost_usd":0.12,"total_lines_added":142,"total_lines_removed":0}}' | ~/.claude/statusline.sh
   ```
5. It appears on the next interaction. If blank: ensure the script is executable, prints to stdout, and that `disableAllHooks` isn't set.
