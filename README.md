# Jiangtao's Skills

A curated collection of [Agent Skills](https://agentskills.io/home) reflecting Jiangtao's preferences, experience, and best practices.

## Installation

```bash
pnpx skills add jiangtao/skills
```

or to install it globally:

```bash
pnpx skills add jiangtao/skills -g
```

Learn more about the CLI usage at [skills](https://github.com/agentskills/skills).

## Skills

### Hand-maintained Skills

> Opinionated

Manually maintained with preferred tools, setup conventions, and best practices.

| Skill | Description |
|-------|-------------|
| [handoff](skills/handoff) | Session handoff for context continuity across conversations |
| [dev](skills/dev) | Development workflow skills for verification, refactoring, and error handling |
| [exam](skills/exam) | Generate exam questions from documents or topics |

---

#### Handoff Skill

Session handoff for context continuity across Claude Code conversations.

**Usage:**
```bash
# Save current session before closing
/handoff:save --name my-feature

# Resume previous work
/handoff:continue my-feature

# Clean up session (recommended after saving)
/compact
```

**Features:**
- ✅ Automatic versioning (v0.0.1, v0.0.2, ...)
- ✅ Finds and loads latest handoff automatically
- ✅ Timestamp format: `yy-MM-DD hh:mm:ss`
- ✅ Documents stored in `docs/handoffs/`

---

#### Dev Skill

Development workflow skills to improve code quality and reduce debugging iterations.

**Usage:**
```bash
# Verify code changes after implementation
/dev:verify

# Plan complex refactoring tasks
/dev:refactor-plan

# Check error handling before modifications
/dev:error-check
```

**Features:**
- ✅ Automatic verification workflow (tests + dev server + e2e)
- ✅ Structured refactoring with checkpoints
- ✅ Safe error handling modifications

---

#### Exam Skill

Generate exam questions from documents or topics with multiple question types.

**Usage:**
```bash
/exam:generate --from <file|topic> --type <choice|essay|mixed> --count <number>
```

**Features:**
- ✅ Multiple question types (single choice, multiple choice, true/false, essay)
- ✅ Support for PDF and markdown input
- ✅ Configurable difficulty and scoring

---

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
