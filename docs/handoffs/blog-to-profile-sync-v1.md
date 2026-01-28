# Blog to Profile Sync Handoff

**Created:** 2026-01-28
**Version:** v1

## Context Overview

- **Project:** Blog to Profile Sync feature
- **Objectives:** Synchronize profile data between personal blog (Hexo-based) and portfolio website
- **Architecture:** Node.js scripts that read/write markdown frontmatter across both codebases

## Current Status

### Completed

- Created initial sync script structure
- Implemented markdown frontmatter parser
- Set up git submodules for monorepo management

### In Progress

- Developing sync logic for bio field

### TODO

- Complete bio field sync implementation
- Add avatar/image sync capability
- Write unit tests for sync functions
- Create documentation for usage

## Key Decisions & Rationale

- **Hexo choice:** Already using for blog, minimal migration needed
- **Frontmatter approach:** Standard format, human-readable, version-controllable
- **Submodules:** Keeps repos separate while enabling shared tooling

## Important File Locations

- Sync script: `scripts/sync-profile.js`
- Blog profile: `source/about/index.md`
- Portfolio profile: `src/data/profile.json`

## Development Guidelines

- Use ES6+ syntax
- Preserve frontmatter formatting when reading/writing
- Always backup before syncing

## Blockers & Risks

- None currently identified

## References

- Hexo docs: https://hexo.io/docs/front-matter
- Project issue: #42
