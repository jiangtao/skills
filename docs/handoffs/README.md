# Handoff Documentation

This directory contains session handoff documents that preserve context across Claude Code conversations.

## Quick Start

### Save Current Session

```bash
/handoff:save --name <project-name> --format v1
```

Example:
```bash
/handoff:save --name authentication --format v1
```

### Continue Previous Session

```bash
/handoff:continue <project-name>
```

Example:
```bash
/handoff:continue authentication
```

## Command Reference

### `/handoff:save`

Save current session context to a handoff document.

| Parameter | Description | Examples |
|-----------|-------------|----------|
| `--name` | Project/feature name | `--name blog-sync` |
| `--format` | Version identifier | `--format v1`, `--format 2026-01-29` |

**Output:** Creates `docs/handoffs/<name>-<format>.md`

### `/handoff:continue`

Load context from an existing handoff document.

| Parameter | Description | Examples |
|-----------|-------------|----------|
| `<project-name>` | Project to continue | `authentication`, `blog-sync` |

**Behavior:** Finds latest handoff document for the project and loads context.

## File Naming

Two naming conventions are supported:

### Version-Based (Milestones)
- `project-v1.md`
- `project-v2.md`
- Use for major milestones or completed features

### Date-Based (Snapshots)
- `project-2026-01-29.md`
- `project-2026-01-30.md`
- Use for daily progress snapshots

## Document Structure

Each handoff document contains:

1. **Context Overview** - Project background, objectives, architecture
2. **Current Status** - Completed, in progress, TODO items
3. **Key Decisions & Rationale** - Why certain approaches were chosen
4. **Important File Locations** - Paths to key files
5. **Development Guidelines** - Code style, testing approach
6. **Blockers & Risks** - Known issues or concerns
7. **References** - Related docs and resources

## Best Practices

### 1. Update Regularly
Save a handoff after completing significant work or reaching a milestone.

### 2. Be Specific
Include actual file paths, not descriptions:
```
✅ Good: `src/components/auth/login.tsx`
❌ Bad: `the login component file`
```

### 3. Track Decisions
Document **why**, not just **what**:
```
✅ Good: "Chose Zustand over Redux for simpler state management in small app"
❌ Bad: "Used Zustand"
```

### 4. Keep TODOs Actionable
Each TODO should be clear and independent:
```
✅ Good: "Add unit tests for `validateEmail()` function"
❌ Bad: "Work on tests"
```

### 5. Version Strategically
- Use **v1, v2** for completed features or major milestones
- Use **dates** for daily snapshots or work-in-progress

## Examples

See `blog-to-profile-sync-v1.md` and `handoff-skill-v1.md` for examples of completed handoff documents.

## Template

A blank template is available at `template.md` for creating new handoff documents manually.
