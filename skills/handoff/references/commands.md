---
name: commands
description: Handoff command reference
---

# Handoff Commands

## `/handoff:save`

Save current session context to a handoff document.

**Usage:**
```bash
/handoff:save --name <feature-name>
```

**What happens:**
1. Collects session context (project, status, decisions, files, TODOs)
2. Auto-generates version number (v0.0.1, v0.0.2, v0.0.3...)
3. Creates document at `docs/handoffs/<name>-v<version>.md`
4. Displays success message
5. Reminds you to run `/compact`

**Example:**
```bash
/handoff:save --name blog-sync
# Creates: docs/handoffs/blog-sync-v0.0.1.md
```

## `/handoff:continue`

Load and display a previous handoff document.

**Usage:**
```bash
/handoff:continue <feature-name>
```

**What happens:**
1. Finds all handoff files for the feature
2. Sorts by version (v0.0.3 > v0.0.2 > v0.0.1)
3. Shows confirmation dialog
4. Loads and presents handoff content

**Example:**
```bash
/handoff:continue blog-sync

Found handoff(s) for "blog-sync":
📄 blog-sync-v0.0.3.md (26-01-29 14:30:15)
📄 blog-sync-v0.0.2.md (26-01-28 09:15:20)

Load latest: blog-sync-v0.0.3.md? [Y/n]
```

## `/compact`

Clean and organize the current session.

**Usage:**
```bash
/compact
```

**When to use:**
- After saving a handoff
- When session becomes too long
- Before closing a session
