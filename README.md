# Jerret's Skills

A curated collection of [Agent Skills](https://agentskills.io/home) reflecting Jerret's preferences, experience, and best practices.

## Installation

```bash
pnpx skills add jerret/skills
```

or to install it globally:

```bash
pnpx skills add jerret/skills -g
```

Learn more about the CLI usage at [skills](https://github.com/agentskills/skills).

## Skills

### Hand-maintained Skills

> Opinionated

Manually maintained with preferred tools, setup conventions, and best practices.

| Skill | Description |
|-------|-------------|
| [handoff](skills/handoff) | Session handoff for context continuity across conversations |
| [jerret](skills/jerret) | Jerret's preferences and best practices |

#### Handoff Skill Usage

Preserve context across Claude Code sessions:

```bash
# Save current session
/handoff:save --name my-feature

# Resume previous work
/handoff:continue my-feature

# Clean session (manual)
/compact
```

**Features:**
- Automatic versioning (v0.0.1, v0.0.2, ...)
- Finds and loads latest handoff
- Timestamp format: `yy-MM-DD hh:mm:ss`
- Documents stored in `docs/handoffs/`

See [CLAUDE.md](CLAUDE.md) for detailed documentation.

### Skills Generated from Official Documentation

> Unopinionated but with tilted focus

Generated from official documentation.

| Skill | Description | Source |
|-------|-------------|--------|
| *(Coming soon)* | | |

### Vendored Skills

Synced from external repositories that maintain their own skills.

| Skill | Description | Source |
|-------|-------------|--------|
| *(Coming soon)* | | |

## What Makes This Collection Different?

This collection uses git submodules to directly reference source documentation, providing more reliable context and allowing skills to stay up-to-date with upstream changes.

## Generate Your Own Skills

Fork this project to create your own customized skill collection.

1. Fork or clone this repository
2. Install dependencies: `pnpm install`
3. Update `meta.ts` with your own projects and skill sources
4. Run `pnpm start cleanup` to remove existing submodules and skills
5. Run `pnpm start init` to clone the submodules
6. Run `pnpm start sync` to sync vendored skills
7. Ask your agent to "generate skills for <project>"

See [AGENTS.md](AGENTS.md) for detailed generation guidelines.

## License

Skills and the scripts in this repository are [MIT](LICENSE.md) licensed.

Vendored skills from external repositories retain their original licenses - see each skill directory for details.
