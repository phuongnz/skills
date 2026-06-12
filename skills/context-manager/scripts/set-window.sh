#!/usr/bin/env bash
# Set the healthy-window (smart zone) size in tokens, preserving other keys.
# Usage: set-window.sh <positive-integer-tokens>
N="${1:-}"
case "$N" in
  ""|*[!0-9]*) echo "usage: set-window.sh <positive-integer-tokens>" >&2; exit 1 ;;
esac
cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json"
if command -v jq >/dev/null 2>&1 && [ -f "$cfg" ]; then
  tmp="$(mktemp)"
  jq --argjson v "$N" '.healthy_window_tokens = $v' "$cfg" > "$tmp" && mv "$tmp" "$cfg"
else
  # No jq, or no existing config: write a fresh file (clobbers any other keys).
  printf '{\n  "healthy_window_tokens": %s\n}\n' "$N" > "$cfg"
fi
cat "$cfg"
