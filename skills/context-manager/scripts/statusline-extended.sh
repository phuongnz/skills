#!/usr/bin/env bash
# Status line — Extended: Essentials + 5-hour & 7-day rate-limit usage with time-to-reset.
# Renders: [Opus·xhigh] 11.5k (8%) | 5h:23% (↻2h14m) | 7d:45% (↻3d4h)
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
