# Status line templates

Claude Code runs a shell command after each message and pipes session JSON to it on stdin; whatever the command prints becomes the status bar. Configure it in `~/.claude/settings.json`:

```json
{ "statusLine": { "type": "command", "command": "~/.claude/statusline.sh" } }
```

Offer the 4 templates below or a custom one. The fastest path is the built-in `/statusline <description>` command, which generates a script and wires up settings automatically — mention it. To build it deliberately, use a template here.

All four use `jq`. Check `command -v jq` first; if missing, suggest `brew install jq` (macOS) or offer the Python equivalent (the official docs provide Python and Node versions of each). Every template shows the model with its reasoning effort appended as `[Model·effort]` (e.g. `[Opus·xhigh]`), falling back to `[Model]` when `effort.level` is absent.

| Template | Shows |
|---|---|
| **1 Essentials** | model · effort, context tokens (context %) |
| **2 Extended** | Essentials + 5-hour & 7-day rate-limit usage, each with time-to-reset |
| **3 Smart-zone bar** (recommended) | model · effort, smart-zone bar |
| **4 Dashboard** | line 1: model · effort, folder, branch · line 2: smart-zone bar, cost, net lines, 5h & 7d limits |

## Template 1 — Essentials (single line)

Model + reasoning effort, context tokens, context %.

```bash
#!/usr/bin/env bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
EFFORT=$(echo "$input" | jq -r '.effort.level // empty')
TOK=$(echo "$input" | jq -r '.context_window.total_input_tokens // empty')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
LABEL="[${MODEL}]"; [ -n "$EFFORT" ] && LABEL="[${MODEL}·${EFFORT}]"
TOKD=$(awk -v n="$TOK" 'BEGIN{ if(n=="") print "?"; else if(n>=1000) printf "%.1fk", n/1000; else printf "%d", n }')
echo "$LABEL ${TOKD} (${PCT}%)"
```

Renders: `[Opus·xhigh] 11.5k (8%)` — `total_input_tokens` is the exact token count in context; the `%` is share of the raw window.

## Template 2 — Extended (single line)

Essentials plus the **5-hour** and **7-day** rate-limit usage, each with the time until it resets. The `resets_at` value can be epoch-seconds or an ISO-8601 timestamp; the `reltime` helper handles both and prints nothing if the field is missing (common early in a session, or outside Pro/Max).

```bash
#!/usr/bin/env bash
input=$(cat)
# human time-to-reset from an epoch-seconds or ISO-8601 timestamp; prints "" if unknown
reltime(){ ts="$1"; case "$ts" in ""|null) return;; esac
  now=$(date +%s)
  case "$ts" in *[!0-9]*) c=${ts%Z}; c=${c%.*}
      t=$(date -u -d "$c" +%s 2>/dev/null) || t=$(TZ=UTC date -j -f "%Y-%m-%dT%H:%M:%S" "$c" +%s 2>/dev/null);;
    *) t="$ts";; esac
  case "$t" in ""|*[!0-9]*) return;; esac
  d=$((t-now)); [ "$d" -lt 0 ] && d=0
  if   [ "$d" -ge 86400 ]; then printf '%dd%dh' $((d/86400)) $(((d%86400)/3600))
  elif [ "$d" -ge 3600 ];  then printf '%dh%dm' $((d/3600)) $(((d%3600)/60))
  else printf '%dm' $((d/60)); fi; }
MODEL=$(echo "$input" | jq -r '.model.display_name')
EFFORT=$(echo "$input" | jq -r '.effort.level // empty')
TOK=$(echo "$input" | jq -r '.context_window.total_input_tokens // empty')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
F_PCT=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
F_RST=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
W_PCT=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
W_RST=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')
LABEL="[${MODEL}]"; [ -n "$EFFORT" ] && LABEL="[${MODEL}·${EFFORT}]"
TOKD=$(awk -v n="$TOK" 'BEGIN{ if(n=="") print "?"; else if(n>=1000) printf "%.1fk", n/1000; else printf "%d", n }')
OUT="$LABEL ${TOKD} (${PCT}%)"
if [ -n "$F_PCT" ]; then r=$(reltime "$F_RST"); OUT="$OUT | 5h:$(printf '%.0f' "$F_PCT")%"; [ -n "$r" ] && OUT="$OUT (↻$r)"; fi
if [ -n "$W_PCT" ]; then r=$(reltime "$W_RST"); OUT="$OUT | 7d:$(printf '%.0f' "$W_PCT")%"; [ -n "$r" ] && OUT="$OUT (↻$r)"; fi
echo "$OUT"
```

Renders: `[Opus·xhigh] 11.5k (8%) | 5h:23% (↻2h14m) | 7d:45% (↻3d4h)` — `↻` marks time-to-reset.

## Template 3 — Smart-zone bar (recommended)

Model + reasoning effort, then a bar colored against the **smart zone** instead of the raw window.

`context_window.used_percentage` is a share of the **raw** window (200k or 1M). On a 1M window that bar stays green at 140k tokens — right where context rot is already biting. Coloring against the smart zone (healthy window, default 150k) makes the bar shift through a gradient as quality actually starts to suffer. The gradient has four bands, keyed to smart-zone occupancy `SZPCT` (used tokens ÷ `HW`, so it passes 100% once you're past the healthy window):

| Smart-zone occupancy (`SZPCT`) | Band | Color |
|---|---|---|
| ≤ 100% (within the smart zone) | comfortable | 🟢 green |
| 100–133% (up to smart zone + ⅓) | watch | 🟡 yellow |
| 133–166% (up to smart zone + ⅔) | crowded | 🟠 orange |
| > 166% (beyond smart zone + ⅔) | past it | 🔴 red |

It reads the same healthy-window setting the skill uses (`healthy_window_tokens`, default 150000) and prefers the exact `total_input_tokens`, falling back to `used_percentage × window`. Orange uses a 256-color code (`\033[38;5;208m`); virtually all modern terminals render it, falling back to a near color otherwise.

```bash
#!/usr/bin/env bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
EFFORT=$(echo "$input" | jq -r '.effort.level // empty')
HW=$(jq -r '.healthy_window_tokens // 150000' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json" 2>/dev/null || echo 150000)
LABEL="[${MODEL}]"; [ -n "$EFFORT" ] && LABEL="[${MODEL}·${EFFORT}]"
# prefer the exact token count; fall back to used_percentage × window
USEDTOK=$(echo "$input" | jq -r '.context_window.total_input_tokens // empty')
if [ -z "$USEDTOK" ]; then
  WIN=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
  USEDPCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
  USEDTOK=$(awk -v p="$USEDPCT" -v w="$WIN" 'BEGIN{printf "%d", p*w/100}')
fi
SZPCT=$(awk -v u="$USEDTOK" -v h="$HW" 'BEGIN{printf "%d", u*100/h}')
GREEN='\033[32m'; YELLOW='\033[33m'; ORANGE='\033[38;5;208m'; RED='\033[31m'; RESET='\033[0m'
if   [ "$SZPCT" -ge 166 ]; then BAR_COLOR="$RED"      # beyond smart zone + 2/3
elif [ "$SZPCT" -ge 133 ]; then BAR_COLOR="$ORANGE"   # past smart zone + 1/3
elif [ "$SZPCT" -ge 100 ]; then BAR_COLOR="$YELLOW"   # past the smart zone
else BAR_COLOR="$GREEN"; fi                            # within the smart zone
CAP=$((SZPCT > 100 ? 100 : SZPCT)); FILLED=$((CAP / 10)); EMPTY=$((10 - FILLED))
printf -v FILL "%${FILLED}s"; printf -v PAD "%${EMPTY}s"
BAR="${FILL// /█}${PAD// /░}"
echo -e "$LABEL ${BAR_COLOR}${BAR} $((USEDTOK/1000))k/$((HW/1000))k smart zone (${SZPCT}%)${RESET}"
```

Renders: `[Opus·xhigh] ██████░░░░ 95k/150k smart zone (63%)`. The bar is mostly empty at low occupancy — that's the point: most of the smart zone should be headroom. `SZPCT` keeps climbing past 100% once you're past the healthy window — green→yellow→orange→red is your cue to compact or clear.

## Template 4 — Dashboard (multi-line)

Line 1: model + reasoning effort, project folder, git branch.
Line 2: smart-zone bar (same gradient as Template 3), running cost, net lines changed (added − removed), and the 5-hour & 7-day rate-limit usage with time-to-reset.

```bash
#!/usr/bin/env bash
input=$(cat)
reltime(){ ts="$1"; case "$ts" in ""|null) return;; esac
  now=$(date +%s)
  case "$ts" in *[!0-9]*) c=${ts%Z}; c=${c%.*}
      t=$(date -u -d "$c" +%s 2>/dev/null) || t=$(TZ=UTC date -j -f "%Y-%m-%dT%H:%M:%S" "$c" +%s 2>/dev/null);;
    *) t="$ts";; esac
  case "$t" in ""|*[!0-9]*) return;; esac
  d=$((t-now)); [ "$d" -lt 0 ] && d=0
  if   [ "$d" -ge 86400 ]; then printf '%dd%dh' $((d/86400)) $(((d%86400)/3600))
  elif [ "$d" -ge 3600 ];  then printf '%dh%dm' $((d/3600)) $(((d%3600)/60))
  else printf '%dm' $((d/60)); fi; }
MODEL=$(echo "$input" | jq -r '.model.display_name')
EFFORT=$(echo "$input" | jq -r '.effort.level // empty')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
LINES_ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
LINES_REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')
HW=$(jq -r '.healthy_window_tokens // 150000' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json" 2>/dev/null || echo 150000)
F_PCT=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
F_RST=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
W_PCT=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
W_RST=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')
LABEL="[${MODEL}]"; [ -n "$EFFORT" ] && LABEL="[${MODEL}·${EFFORT}]"
USEDTOK=$(echo "$input" | jq -r '.context_window.total_input_tokens // empty')
if [ -z "$USEDTOK" ]; then
  WIN=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
  USEDPCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
  USEDTOK=$(awk -v p="$USEDPCT" -v w="$WIN" 'BEGIN{printf "%d", p*w/100}')
fi
SZPCT=$(awk -v u="$USEDTOK" -v h="$HW" 'BEGIN{printf "%d", u*100/h}')
CYAN='\033[36m'; GREEN='\033[32m'; YELLOW='\033[33m'; ORANGE='\033[38;5;208m'; RED='\033[31m'; RESET='\033[0m'
if   [ "$SZPCT" -ge 166 ]; then BAR_COLOR="$RED"
elif [ "$SZPCT" -ge 133 ]; then BAR_COLOR="$ORANGE"
elif [ "$SZPCT" -ge 100 ]; then BAR_COLOR="$YELLOW"
else BAR_COLOR="$GREEN"; fi
CAP=$((SZPCT > 100 ? 100 : SZPCT)); FILLED=$((CAP / 10)); EMPTY=$((10 - FILLED))
printf -v FILL "%${FILLED}s"; printf -v PAD "%${EMPTY}s"
BAR="${FILL// /█}${PAD// /░}"
NET=$((LINES_ADDED - LINES_REMOVED)); [ "$NET" -ge 0 ] && NET="+$NET"
BRANCH=""
git rev-parse --git-dir >/dev/null 2>&1 && BRANCH=" | 🌿 $(git branch --show-current 2>/dev/null)"
COST_FMT=$(printf '$%.2f' "$COST")
LINE2="${BAR_COLOR}${BAR} $((USEDTOK/1000))k/$((HW/1000))k smart zone (${SZPCT}%)${RESET} | ${YELLOW}${COST_FMT}${RESET} | 📝 ${NET}"
if [ -n "$F_PCT" ]; then r=$(reltime "$F_RST"); LINE2="$LINE2 | 5h:$(printf '%.0f' "$F_PCT")%"; [ -n "$r" ] && LINE2="$LINE2 (↻$r)"; fi
if [ -n "$W_PCT" ]; then r=$(reltime "$W_RST"); LINE2="$LINE2 | 7d:$(printf '%.0f' "$W_PCT")%"; [ -n "$r" ] && LINE2="$LINE2 (↻$r)"; fi
echo -e "${CYAN}${LABEL}${RESET} 📁 ${DIR##*/}$BRANCH"
echo -e "$LINE2"
```

Renders:

```
[Opus·xhigh] 📁 trade_with_ai_run_1 | 🌿 main
██████░░░░ 95k/150k smart zone (63%) | $0.12 | 📝 +142 | 5h:23% (↻2h14m) | 7d:45% (↻3d4h)
```

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

Many fields are absent or `null` early on — always provide fallbacks (`// 0`, `// empty`). Keep output short; the bar has limited width.

## Applying a choice

1. **Confirm** which template and that you'll write `~/.claude/statusline.sh` and add a `statusLine` entry to `~/.claude/settings.json`. If either exists, note it'll be changed and preserve the rest of settings.json (merge, don't overwrite).
2. Write the script; `chmod +x ~/.claude/statusline.sh`.
3. Merge into `~/.claude/settings.json`: `"statusLine": { "type": "command", "command": "~/.claude/statusline.sh" }`. Optional: `"padding": 2`, or `"refreshInterval": <seconds>` to keep the time-to-reset and wall-clock segments fresh.
4. **Test** before relying on it (this payload exercises tokens, effort, and both rate limits):
   ```bash
   N=$(date +%s); echo '{"model":{"display_name":"Opus"},"effort":{"level":"xhigh"},"workspace":{"current_dir":"'$PWD'"},"context_window":{"used_percentage":8,"total_input_tokens":11500,"context_window_size":1000000},"rate_limits":{"five_hour":{"used_percentage":23,"resets_at":'$((N+8040))'},"seven_day":{"used_percentage":45,"resets_at":'$((N+273600))'}},"cost":{"total_cost_usd":0.12,"total_duration_ms":200000}}' | ~/.claude/statusline.sh
   ```
5. It appears on the next interaction. If blank: ensure the script is executable, prints to stdout, and that `disableAllHooks` isn't set.
