#!/usr/bin/env bash
# Status line — Smart-zone bar (recommended): model + effort, then a bar colored
# against the smart zone (healthy_window_tokens, default 150k) instead of the raw window.
# Renders: [Opus·xhigh] ██████░░░░ 95k/150k smart zone (63%)
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
