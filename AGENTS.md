# Skills Generator

Generate [Agent Skills](https://agentskills.io/home) from project documentation.

## Skill Source Types

### Type 1: Generated Skills (`sources/`)

For OSS projects **without existing skills**. We clone the repo as a submodule and generate skills from their documentation.

**Workflow:** Read docs → Understand → Generate skills

**Source:** `sources/{project}/docs/`

### Type 2: Synced Skills (`vendor/`)

For projects that **already maintain their own skills**. We clone their repo as a submodule and sync specified skills.

**Workflow:** Pull updates → Copy specified skills (with optional renaming)

**Source:** `vendor/{project}/skills/{skill-name}/`

**Config:** Each vendor specifies which skills to sync in `meta.ts`

### Type 3: Hand-written Skills

Skills written manually with personal preferences and best practices.

## Repository Structure

```
.
├── meta.ts              # Project metadata (repos & URLs)
├── scripts/             # CLI management scripts
│   └── cli.ts          # Main CLI entry point
│
├── sources/             # Type 1: OSS repos (generate from docs)
│   └── {project}/
│       └── docs/       # Read documentation from here
│
├── vendor/              # Type 2: Projects with existing skills (sync only)
│   └── {project}/
│       └── skills/
│           └── {skill-name}/  # Individual skills to sync
│
└── skills/              # Output directory (generated or synced)
    └── {output-name}/
        ├── skill.md    # Index of all skills
        ├── GENERATION.md  # Tracking metadata (for generated skills)
        ├── SYNC.md     # Tracking metadata (for synced skills)
        └── references/
            └── *.md    # Individual skill files
```

## Workflows

### For Generated Skills (Type 1)

#### Adding a New Project

1. Add entry to `meta.ts` in the `submodules` object
2. Run `pnpm start init -y` to clone the submodule
3. Follow generation guide to create the skills

#### Creating New Skills

1. Read source docs from `sources/{project}/docs/`
2. Understand the documentation thoroughly
3. Create skill files in `skills/{project}/references/`
4. Create `skill.md` index listing all skills
5. Create `GENERATION.md` with the source git SHA

#### Updating Generated Skills

1. Check git diff since the SHA in `GENERATION.md`
2. Update affected skill files based on changes
3. Update `skill.md` with the new version
4. Update `GENERATION.md` with new SHA

### For Synced Skills (Type 2)

#### Initial Sync

1. Copy specified skills from `vendor/{project}/skills/{skill-name}/` to `skills/{output-name}/`
2. Create `SYNC.md` with the vendor git SHA

#### Updating Synced Skills

1. Check git diff since the SHA in `SYNC.md`
2. Copy changed files from vendor to output
3. Update `SYNC.md` with new SHA

**Note:** Do NOT modify synced skills manually. Contribute changes upstream.

## File Formats

### `skill.md`

Index file listing all skills with brief descriptions.

```markdown
---
name: {name}
description: {description}
metadata:
  author: Jerret
  version: "2026.1.28"
---

> Brief summary/context

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Topic Name | Description | [reference-name](references/file.md) |
```

### `GENERATION.md`

Tracking metadata for generated skills (Type 1).

```markdown
# Generation Info

- **Source:** `sources/{project}`
- **Git SHA:** `abc123def456...`
- **Generated:** 2024-01-15
```

### `SYNC.md`

Tracking metadata for synced skills (Type 2).

```markdown
# Sync Info

- **Source:** `vendor/{project}/skills/{skill-name}`
- **Git SHA:** `abc123def456...`
- **Synced:** 2024-01-15
```

### `references/*.md`

Individual skill files. One concept per file.

```markdown
---
name: {name}
description: {description}
---

# {Concept Name}

Brief description.

## Usage

Code examples and patterns.

## Key Points

- Important detail 1
- Important detail 2
```
