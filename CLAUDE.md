# Jerret's Skills - Project Context

> **Last Updated:** 2026-01-29
> **Version:** 0.0.2

## Project Overview

A curated collection of [Agent Skills](https://agentskills.io/home) reflecting personal preferences, experience, and best practices. This project uses git submodules to reference source documentation directly.

### Repository Structure

```
.
├── skills/              # Hand-written and synced skills
│   ├── handoff/        # Session handoff skill
│   └── jerret/         # Personal preferences
├── docs/               # Documentation
│   ├── handoffs/       # Session handoff documents
│   └── plans/          # Implementation plans
├── scripts/            # CLI management scripts
│   └── cli.ts         # Main CLI entry point
└── meta.ts            # Project metadata
```

## Handoff Commands

### Overview

Session handoff commands preserve context across Claude Code conversations through structured markdown documents.

### Available Commands

#### `/handoff:save [options]`

Save current session context to a handoff document.

**Usage:**
```bash
/handoff:save --name <功能名> [--continue <版本>]
```

**Options:**
- `--name <功能名>` - Feature/project name (required)
- `--continue <版本>` - Chain from previous handoff version

**Trigger phrases:**
- `/handoff:save --name blog-sync`
- `save handoff <功能名>`
- "保存 handoff <功能名>"
- "保存当前进度"
- "checkpoint"

**What happens:**
1. Collect session context (project, status, decisions, files, TODOs)
2. Auto-generate version number (v0.0.1, v0.0.2, v0.0.3...)
3. Generate handoff document at `docs/handoffs/<name>-v<version>.md`
4. Display success message with file path
5. **Remind user to run `/compact`** to clean and organize session

**Example:**
```bash
# First save
/handoff:save --name blog-sync
# Creates: docs/handoffs/blog-sync-v0.0.1.md
# Output:
# ✅ Handoff saved: docs/handoffs/blog-sync-v0.0.1.md
# 💡 Tip: Run `/compact` to clean up the current session before closing.

# Second save (auto-increments)
/handoff:save --name blog-sync
# Creates: docs/handoffs/blog-sync-v0.0.2.md
```

**Version format:**
- Automatic patch versioning: v0.0.1, v0.0.2, v0.0.3...
- Each save increments the patch number
- No manual version management needed

#### `/handoff:continue <功能名|路径>`

Load and display a previous handoff document.

**Usage:**
```bash
/handoff:continue <功能名>
/handoff:continue docs/handoffs/<功能名>-v0.0.1.md
```

**Trigger phrases:**
- `/handoff:continue blog-sync`
- `continue handoff <功能名>`
- "继续 handoff <功能名>"
- "继续之前的工作"
- "what were we working on?"

**What happens:**
1. Search `docs/handoffs/` for matching files
2. Sort by version (v0.0.3 > v0.0.2 > v0.0.1)
3. Show found handoffs with timestamps
4. Ask for confirmation
5. Load and display handoff content
6. Ask: "What would you like to work on?"

**Example interaction:**
```
Found handoff(s) for "blog-sync":
📄 blog-sync-v0.0.3.md (26-01-29 14:30:15)
📄 blog-sync-v0.0.2.md (26-01-28 09:15:20)

Load latest: blog-sync-v0.0.3.md? [Y/n]

→ User confirms, handoff content is displayed
```

#### `/compact`

Clean and organize the current session to reduce token usage and improve focus.

**Usage:**
```bash
/compact
```

**When to use:**
- After saving a handoff document
- When session becomes too long
- Before closing a session

**What happens:**
- Compresses conversation history
- Removes redundant messages
- Preserves essential context
- Updates CLAUDE.md if needed

### Handoff Document Structure

```markdown
# <Feature Name> Handoff

**Created:** yy-MM-DD hh:mm:ss
**Version:** v0.0.X

## Context Overview
- Project: ...
- Objectives: ...
- Architecture: ...

## Current Status
### Completed
- [x] Item 1

### In Progress
- [ ] Item 2

### TODO
- [ ] Next task 1
- [ ] Next task 2

## Key Decisions & Rationale
- Decision 1: ...

## Important File Locations
- `path/to/file` - Description

## Development Guidelines
- Style notes

## Blockers & Risks
- Issue - Status

## References
- Related docs
```

**Timestamp format:** `yy-MM-DD hh:mm:ss`
- Example: `26-01-29 14:30:15` (January 29, 2026, 2:30:15 PM)

### Best Practices

1. **Always include TODO items** - Handoffs should capture next steps
2. **Auto versioning** - No need to manually specify versions
3. **Include file paths** - Use absolute paths for important files
4. **Document decisions** - Explain why, not just what
5. **Commit to git** - Handoffs should be version controlled
6. **Run /compact** - Clean session after saving handoff

### Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.0.2 | 26-01-29 | Simplified handoff: removed day format, auto versioning, /compact reminder |
| v0.0.1 | 2026-01-29 | Initial CLAUDE.md with handoff commands and testing requirements |

## Development Workflow

### MANDATORY: Testing After Every Feature

**CRITICAL REQUIREMENT:** Every feature completion or version update MUST be followed by comprehensive testing and verification.

**Testing Checklist:**
- [ ] Feature functionality tested
- [ ] Edge cases covered
- [ ] Integration tested (if applicable)
- [ ] Documentation updated
- [ ] Test results documented

**No exceptions:** Even "simple" changes require testing verification.

### Typical Workflow

1. **Plan** - Use brainstorming skill to design approach
2. **Implement** - Write the code/feature
3. **TEST** - Verify functionality works as expected
4. **Document** - Update CLAUDE.md and other docs
5. **Handoff** - Create session handoff if pausing

### Skills Management

```bash
# Initialize submodules
pnpm start init

# Sync skills from vendors
pnpm start sync

# Check for updates
pnpm start check

# Cleanup unused skills
pnpm start cleanup
```

## Key Files

| File | Purpose |
|------|---------|
| `skills/handoff/skill.md` | Handoff skill definition |
| `docs/handoffs/` | Session handoff documents |
| `docs/handoffs/template.md` | Handoff document template |
| `scripts/cli.ts` | Skills management CLI |
| `meta.ts` | Project metadata and submodule config |
| `CLAUDE.md` | This file - project context and guidelines |

## Recent Changes

### v0.0.2 (26-01-29)

**Handoff Simplification:**
- ✅ Removed day format (only version mode now)
- ✅ Removed `--format` parameter (auto versioning)
- ✅ Changed `/compact` from auto-call to user reminder
- ✅ Updated timestamp format to `yy-MM-DD hh:mm:ss`

**Benefits:**
- Simpler command interface
- No manual version management
- Clearer user control over session cleanup
- Consistent timestamp format

**Migration Guide:**
```bash
# Old (no longer works)
/handoff:save --name my-feature --format day

# New (automatic versioning)
/handoff:save --name my-feature
# Creates: my-feature-v0.0.1.md

# Session cleanup (manual)
/compact  # User runs this after saving
```
