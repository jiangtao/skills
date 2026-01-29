---
name: template
description: Handoff document template
---

# Handoff Document Template

## Structure

Every handoff document follows this structure:

```markdown
# <Project Name> Handoff

**Created:** yy-MM-DD hh:mm:ss
**Version:** v0.0.X

## Context Overview

- **Project:** Brief project description
- **Objectives:** Main goals
- **Architecture:** Key architectural decisions

## Current Status

### Completed
- [x] Item 1
- [x] Item 2

### In Progress
- [ ] Current task

### TODO
1. [ ] Next task 1
2. [ ] Next task 2

## Key Decisions & Rationale

- **Decision 1:** What was decided
  - **Why:** Rationale
  - **Alternatives considered:** Other options

## Important File Locations

| File | Purpose | Notes |
|------|---------|-------|
| `path/to/file` | Description | Notes |

## Development Guidelines

- Style notes
- Conventions
- Tools used

## Blockers & Risks

| Issue | Status | Resolution |
|-------|--------|------------|
| Issue | open/closed | Notes |

## References

- Related docs
- Links to resources
```

## Timestamp Format

- Format: `yy-MM-DD hh:mm:ss`
- Example: `26-01-29 14:30:15` (January 29, 2026, 2:30:15 PM)

## Version Format

- Automatic patch versioning: v0.0.1, v0.0.2, v0.0.3...
- Each save increments the patch number
