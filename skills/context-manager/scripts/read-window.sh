#!/usr/bin/env bash
# Print the configured healthy-window (smart zone) size in tokens.
# Defaults to 150000 if the config file or key is absent.
cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/context-manager.json"
jq -r '.healthy_window_tokens // 150000' "$cfg" 2>/dev/null || echo 150000
