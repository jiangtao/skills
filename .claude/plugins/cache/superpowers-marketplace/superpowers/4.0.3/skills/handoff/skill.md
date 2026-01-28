# Handoff Skill

> **For Claude:** Use when user runs `/handoff:save` or `/handoff:continue` commands - manages session continuity through structured markdown documents.

---

## Overview

The handoff skill preserves context across Claude Code sessions through structured markdown documents stored in `docs/handoffs/`.

## Commands

### `/handoff:save`

Save current session context to a handoff document.

**Syntax:**
```
/handoff:save --name <project-name> [--format v1|v2|YYYY-MM-DD]
```

**Examples:**
- `/handoff:save --name blog-to-profile-sync --format v1`
- `/handoff:save --name authentication --format 2026-01-29`

**Behavior:**
1. Prompt user for handoff information using template sections
2. Generate markdown document at `docs/handoffs/<name>-<format>.md`
3. Confirm creation and suggest git commit

### `/handoff:continue`

Load context from an existing handoff document.

**Syntax:**
```
/handoff:continue <project-name>
```

**Examples:**
- `/handoff:continue blog-to-profile-sync`
- `/handoff:continue authentication`

**Behavior:**
1. Find latest handoff document for project name
2. Read and parse the handoff document
3. Present context summary to user
4. Load TODO items from Current Status section

---

## Handoff Document Structure

```markdown
# <Project Name> Handoff

**Created:** YYYY-MM-DD
**Version:** vX

## Context Overview

- **Project:** Brief description
- **Objectives:** What are we trying to achieve?
- **Architecture:** Key technical details

## Current Status

- **Completed:** What's been done
- **In Progress:** What's actively being worked on
- **TODO:** Next steps (actionable items)

## Key Decisions & Rationale

- Decision 1: Why X approach was chosen
- Decision 2: Why Y library/framework was used

## Important File Locations

- Component: `path/to/file.ts`
- Config: `path/to/config.json`

## Development Guidelines

- Code style preferences
- Testing approach
- Deployment considerations

## Blockers & Risks

- Current blockers
- Known risks or edge cases

## References

- Related documentation
- External resources
```

---

## Usage Workflow

### Saving a Handoff

1. User invokes `/handoff:save --name <project> --format <version>`
2. Claude prompts for information in each section
3. Claude generates the markdown document
4. Claude suggests: `git add docs/handoffs/<name>-<format>.md && git commit -m "docs: add <project> handoff v<version>"`

### Continuing from Handoff

1. User invokes `/handoff:continue <project>`
2. Claude locates latest handoff document
3. Claude reads and summarizes the context
4. Claude asks: "What would you like to work on?"
5. User can reference TODO items or continue from previous state

---

## Implementation Notes

- Handoff documents are stored in `docs/handoffs/`
- Version naming: `<project>-v1.md`, `<project>-v2.md`, or `<project>-YYYY-MM-DD.md`
- When continuing, Claude should find the most recent version (sorted by name)
- Template available at `docs/handoffs/template.md`

---

## Best Practices

1. **Update regularly:** Save handoff after completing significant work
2. **Be specific:** Include actual file paths, not descriptions
3. **Track decisions:** Document why, not just what
4. **Keep TODOs actionable:** Each item should be clear and independent
5. **Version strategically:** Use v1, v2 for major milestones; dates for daily snapshots
