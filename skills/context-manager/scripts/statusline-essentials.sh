#!/usr/bin/env bash
# Status line — Essentials: model + reasoning effort, context tokens, context %.
# Renders: [Opus·xhigh] 11.5k (8%)
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
EFFORT=$(echo "$input" | jq -r '.effort.level // empty')
TOK=$(echo "$input" | jq -r '.context_window.total_input_tokens // empty')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
LABEL="[${MODEL}]"; [ -n "$EFFORT" ] && LABEL="[${MODEL}·${EFFORT}]"
TOKD=$(awk -v n="$TOK" 'BEGIN{ if(n=="") print "?"; else if(n>=1000) printf "%.1fk", n/1000; else printf "%d", n }')
echo "$LABEL ${TOKD} (${PCT}%)"
