# Superpowers Repo Migration Design

Date: 2026-03-20

## Summary

Migrate the current `superpowers` ownership out of the `skills` repository and establish clear source-of-truth repositories:

- `dotclaude` becomes the Claude-side source of truth for `superpowers`
- `dotcodex` becomes the Codex-side source of truth for the Codex adaptation
- `skills` exits ongoing `superpowers` maintenance and becomes a short-lived transition layer

This plan keeps the migration safe by preserving reviewability, minimizing accidental content loss, and avoiding another mixed-runtime repository.

## Current State

### `skills` repository

The `skills` repository currently contains:

- original hand-maintained skills unrelated to `superpowers`
- `superpowers/` copied and adapted for Claude
- `superpowers-codex/` created as a Codex adaptation
- updated README text describing source-vs-distribution concerns

This repository now mixes three concerns:

- generic personal skills
- Claude plugin maintenance
- Codex-native workflow maintenance

That makes ownership and installation guidance unclear.

### `dotclaude` repository

`/Users/jt/places/personal/dotclaude` already has a `superpowers/` plugin directory with the expected Claude plugin shape:

- `.claude-plugin/plugin.json`
- `hooks/`
- `scripts/`
- `skills/`
- `tests/`

This makes `dotclaude` the natural home for Claude-side maintenance.

### `dotcodex` repository

`/Users/jt/places/personal/dotcodex` is now initialized as a Codex-native repository with:

- `.agents/skills/` for Codex skill discovery
- `vendor/superpowers/` as a synced Claude-side reference snapshot
- a sync script from `dotclaude/superpowers`
- initial Codex skill scaffolding

This makes `dotcodex` the natural home for Codex-side adaptation.

## Target Repository Roles

### `dotclaude`

`dotclaude` is the only Claude-side source of truth for `superpowers`.

It should own:

- Claude plugin manifest and runtime structure
- Claude installation and usage docs
- upstream fork maintenance and attribution
- any Claude-specific workflow adjustments
- approved plans/design assets that belong to the Claude fork

It should not own:

- Codex runtime adapters
- `.agents/skills` Codex-native packaging
- Codex watchdog logic

### `dotcodex`

`dotcodex` is the only Codex-side source of truth for `superpowers` adaptation.

It should own:

- `.agents/skills/*`
- Codex execution workflows
- Codex BDD repair loop guidance
- sub-agent orchestration guidance
- optional watchdog or re-entry tooling
- vendor snapshots synced from `dotclaude/superpowers`

It should not own:

- Claude plugin manifests
- Claude hook runtime logic as a primary implementation

### `skills`

`skills` should stop being the maintenance home for `superpowers`.

It may temporarily keep:

- migration notes
- short-term references or redirect docs

It should eventually remove:

- `superpowers/`
- `superpowers-codex/`

once both target repos are stable.

## Migration Scope

### What must move from `skills/superpowers` to `dotclaude/superpowers`

The migration is not a blind directory overwrite. It is a selective merge of valid Claude-side enhancements.

Expected migration candidates:

- `plugin.json` compatibility fixes for the current Claude Code version
- `README.md` improvements:
  - attribution
  - fork ownership
  - updated local installation guidance
  - future direction pointing to `jiangtao/dotclaude`
- approved `plans/` and `designs/` content, if these are intended as assets in the forked plugin repository

### What must move from `skills/superpowers-codex` to `dotcodex`

- Codex README and repository-level installation guidance
- Codex-native skill definitions
- watchdog or re-entry tooling
- examples and tests
- any Codex-specific execution rules that diverge from Claude

### What must not move into `dotclaude`

- `superpowers-codex/`
- Codex watchdog scripts
- Codex-only execution semantics
- `.agents/skills` packaging

## Installation Direction After Migration

### Claude

The final Claude documentation should point to `jiangtao/dotclaude` as the maintained fork.

Short-term recommended install pattern:

```bash
git clone https://github.com/jiangtao/dotclaude.git
cd dotclaude
claude plugin validate superpowers
claude --plugin-dir "$PWD/superpowers"
```

If a dedicated marketplace is created later, a one-command install path can be added then. It should not be documented as available before it exists.

### Codex

The final Codex documentation should point to `dotcodex` as the Codex-native home.

Repository-local use should prefer running Codex from the `dotcodex` root so `.agents/skills/` is auto-discovered.

## Recommended Migration Strategy

Use a staged migration rather than a hard cut.

### Phase 1: Diff and classify

Compare:

- `skills/superpowers`
- `dotclaude/superpowers`

Classify differences into:

- must migrate
- optional migrate
- do not migrate

### Phase 2: Migrate Claude source of truth

Apply the approved Claude-side deltas into `dotclaude/superpowers`:

- merge README improvements
- keep original attribution and add Jerret fork attribution
- update install docs to point to `jiangtao/dotclaude`
- carry over plugin compatibility fixes
- decide whether `plans/` and `designs/` belong in the repository

### Phase 3: Migrate Codex source of truth

Move Codex adaptation ownership into `dotcodex`:

- keep `vendor/superpowers/` synced from `dotclaude/superpowers`
- keep `.agents/skills/` as the runtime-facing Codex layer
- move or recreate `superpowers-codex` logic in Codex-native form
- verify with lightweight structure tests

### Phase 4: Retire `skills` as a superpowers home

After both repos are stable:

- replace `skills` superpowers content with migration notes or redirects
- or remove `superpowers/` and `superpowers-codex/` entirely

## Risks

### Risk: mixed ownership persists

If `skills`, `dotclaude`, and `dotcodex` all continue changing `superpowers`, drift will return quickly.

Mitigation:

- define one source of truth per runtime
- document it clearly in each repo

### Risk: Codex and Claude docs promise unsupported install flows

Mitigation:

- only document current working install methods
- defer marketplace-style instructions until they actually exist

### Risk: useful fork-specific changes are lost during migration

Mitigation:

- run an explicit diff review before copying
- move content by category, not just by directory

## Success Criteria

Migration is successful when:

- Claude-side `superpowers` is clearly maintained in `dotclaude`
- Codex-side adaptation is clearly maintained in `dotcodex`
- `skills` no longer acts as the active maintenance home for either
- installation docs in each repo point to the correct runtime-specific source
- attribution to the original author remains intact

## Next Execution Plan

1. Diff `skills/superpowers` against `dotclaude/superpowers`
2. Apply approved Claude-side deltas into `dotclaude/superpowers`
3. Commit the initial Codex-native baseline in `dotcodex`
4. Rewrite `skills` docs to mark `superpowers` as migrated
