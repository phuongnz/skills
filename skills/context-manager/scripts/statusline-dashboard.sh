#!/usr/bin/env bash
# Status line — Dashboard (multi-line).
# Line 1: model + effort, project folder, git branch.
# Line 2: smart-zone bar (same gradient as smartzone), cost, net lines, 5h & 7d limits.
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
