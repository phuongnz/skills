# Cleaning up context

Every fix here buys back **smart-zone headroom** — gold tokens under the healthy window (default 150k, see SKILL.md) where the model still works at full quality. The goal isn't to fit inside the raw 200k/1M window; it's to stay well under the smart zone so context rot never sets in.

Two kinds of cleanup. **Transient** shrinks the current conversation; **persistent** shrinks what loads every session. Always confirm before `/clear` (irreversible) or editing the user's files.

Quick decision — approaching or past the smart zone:
- Task done / switching topics → **`/clear`** (full reset — fastest way back to a fresh smart zone).
- Mid-task but bloated with stale tool output → **`/compact`** (summarize, keep going). Optionally `/compact <focus>` to steer the summary.
- Already over the smart zone (total > healthy window) → don't push on; quality is degrading. Compact or clear before the next substantive step.

## The 10 places where cleaning makes sense

Ordered roughly by typical impact. For each: what it costs → how to spot it → fix.

1. **Conversation history (transient, biggest lever).** Long sessions accumulate old tool results and reasoning. Spot: `Messages` is the largest `/context` row, or you're deep into a finished task. Fix: `/compact` to summarize, or `/clear` when starting fresh.

2. **Unused MCP servers (persistent).** Every connected server injects its tool schemas at startup. Spot: `MCP tools` row is large, or servers listed in `/mcp` you don't use. Fix: remove/disable them in `.mcp.json` / settings; prefer servers that load **on demand** (e.g. context7 here is deferred — good).

3. **Oversized CLAUDE.md / AGENTS.md and imported files (persistent).** These load in full every session. Spot: large `Memory files`/project-instructions footprint; long files with rarely-needed detail. Fix: trim to essentials; move deep detail into linked docs the agent reads on demand instead of inlining.

4. **Global `~/.claude/` instructions (persistent).** `~/.claude/CLAUDE.md` and `~/.claude/rules/*.md` load into **every** project. Spot: rules that only matter for one repo. Fix: keep global lean; push project-specifics into that project's files.

5. **Too many always-on skills (persistent).** Each installed skill's description sits in the system prompt; the list grows with every one. Spot: large `Skills` row, or skills in `/skills` you never invoke. Fix: uninstall/disable unused skills.

6. **Bloated memory (persistent).** `MEMORY.md` and auto-memory files load each session. Spot: stale, duplicate, or wrong entries. Fix: prune them; delete memories that proved wrong; keep MEMORY.md to one line per memory.

7. **Large tool outputs (transient).** Whole-file reads, `cat` of big files, build/test log dumps stay in the transcript. Spot: a single huge tool result. Fix: read narrow line ranges, prefer targeted Grep/Read offsets, pipe noisy commands through `head`/filters.

8. **Pasted blobs, screenshots, logs (transient).** Big inline pastes persist for the rest of the session. Fix: save to a file and reference its path, or paste only the relevant excerpt.

9. **Redundant re-reads (transient).** Re-reading the same file repeatedly duplicates it in context; the harness already tracks file state, so re-reading just to "verify" an edit is wasted. Fix: read once; trust Edit/Write to error if they fail.

10. **Fan-out searches done inline (transient).** Sweeping many files directly dumps all those excerpts into the main context. Fix: delegate broad searches to a subagent (e.g. Explore) so only the conclusion returns.

Also worth a glance: stale `--add-dir` directories widening the workspace, and verbose mode's token counter. Minor, but free wins.
