---
name: handoff
description: Session handoff for context continuity across conversations
metadata:
  author: Claude
  version: "1.0.0"
---

> Handoff skill for preserving context across Claude Code sessions through structured markdown documents.

## Commands

This skill supports two commands:

### `/handoff:save`

Save current session context to a handoff document.

**Usage:**
```
/handoff:save --name <project-name> [--format v1|v2|YYYY-MM-DD]
```

**Process:**
1. Ask user for project name and version format
2. Prompt for handoff information:
   - Context Overview (project, objectives, architecture)
   - Current Status (completed, in progress, TODO)
   - Key Decisions & Rationale
   - Important File Locations
   - Development Guidelines
   - Blockers & Risks
3. Generate `docs/handoffs/<name>-<version>.md`
4. Suggest git commit

### `/handoff:continue`

Load context from an existing handoff document.

**Usage:**
```
/handoff:continue <project-name>
```

**Process:**
1. Find latest handoff document for project in `docs/handoffs/`
2. Read and present context summary
3. Show TODO items from Current Status
4. Ask "What would you like to work on?"

## Handoff Document Template

```markdown
# <Project Name> Handoff

**Created:** YYYY-MM-DD
**Version:** vX

## Context Overview

- **Project:**
- **Objectives:**
- **Architecture:**

## Current Status

### Completed
-
-

### In Progress
-

### TODO
-
-

## Key Decisions & Rationale

-

## Important File Locations

-

## Development Guidelines

-

## Blockers & Risks

-

## References

-
```

## File Locations

- Handoff documents: `docs/handoffs/`
- Template: `docs/handoffs/template.md`
- README: `docs/handoffs/README.md`
