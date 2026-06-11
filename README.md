# skills

A collection of agent skills.

## Install

Install a skill into your agents with the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
# List the skills available in this repo
npx skills add phuongnz/skills --list

# Install one by name
npx skills add phuongnz/skills --skill <skill-name>
```

### Scope: project vs global

Choose where a skill is installed:

```bash
# Project-level (default) — stored in ./.agents/skills/
npx skills add phuongnz/skills --skill <skill-name>

# Global / user-level — stored in ~/.agents/skills/
npx skills add phuongnz/skills --skill <skill-name> -g
```

The CLI keeps the canonical copy in `.agents/skills/` (project) or `~/.agents/skills/`
(global), then symlinks it into each selected agent's own directory so every agent can
see it. For example, a global install links into `~/.claude/skills/` for Claude Code:

```
~/.agents/skills/<skill-name>/        # canonical skill
~/.claude/skills/<skill-name>  ->  ../../.agents/skills/<skill-name>
```

Pick which agents get the symlink with `--agent` (e.g. `--agent claude-code cursor`, or
`--agent '*'` for all). If you ever drop a skill into `~/.agents/skills/` by hand,
remember to create the matching symlink in each agent's directory (`~/.claude/skills/`,
etc.) so the agents can access it.

## Structure

Each skill lives in its own folder under `skills/`, containing a `SKILL.md` that
describes what the skill does and when to use it:

```
skills/
└── <skill-name>/
    └── SKILL.md
```

## License

[MIT](./LICENSE)
