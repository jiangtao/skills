# Superpowers for Codex

Codex-oriented adaptation of the `superpowers/` workflow.

> Migration notice: the maintained Codex-side source of truth now lives in `/Users/jt/places/personal/dotcodex`. This directory remains only as a transition artifact inside the `skills` repository.

## Installation

This repository is the source-of-truth workflow repository. The Codex adapter currently ships as local skills plus a local watchdog script.

From the repository root:

```bash
mkdir -p "$HOME/.codex/skills"
ln -sfn "$PWD/superpowers-codex/skills/agent-team-driven-development" \
  "$HOME/.codex/skills/agent-team-driven-development"
ln -sfn "$PWD/superpowers-codex/skills/executing-plans" \
  "$HOME/.codex/skills/executing-plans"
```

Then restart Codex so it reloads the installed skills.

Notes:

- Keep this repository checked out locally. The watchdog and examples run from the repo path.
- This first pass installs the Codex-adapted `agent-team-driven-development` and `executing-plans` skills.
- `behavior-driven-development` and `systematic-debugging` can still be referenced from the existing skill ecosystem until dedicated Codex variants are added here.
- If you later want a cleaner public install flow, publish a separate distribution repository that syncs from `superpowers-codex/`.

## Goals

- preserve the Claude workflow concepts without modifying the Claude plugin
- support Codex sub-agent orchestration for team-style execution
- keep BDD checks in a self-repair loop until all required scenarios pass
- re-launch Codex automatically with `--full-auto` until the loop reaches a terminal state

## Layout

```text
superpowers-codex/
├── README.md
├── scripts/
│   ├── start-superpower-loop.sh
│   └── superpower-watchdog.mjs
├── skills/
│   ├── agent-team-driven-development/
│   │   └── SKILL.md
│   └── executing-plans/
│       └── SKILL.md
└── tests/
    └── superpower-watchdog.test.mjs
```

## Watchdog

`scripts/superpower-watchdog.mjs` is the first Codex runtime primitive. It:

- reads a loop state file
- decides whether the run should continue, pause, stop, or fail terminally
- launches `codex exec --full-auto` when continuation is allowed

## Current Scope

This first pass focuses on Codex runtime behavior rather than full content parity with the Claude plugin.

## Quick Start

From this repository root:

```bash
sh superpowers-codex/scripts/start-superpower-loop.sh \
  superpowers-codex/examples/state.json \
  superpowers-codex/examples/prompt.md
```

The watchdog will launch:

```bash
codex exec --full-auto --cd <workdir> --add-dir "$HOME/.codex" "<prompt>"
```

## Attribution

**Original author**

Frad LEE (fradser@gmail.com)

The Codex adaptation in this repository is built on top of Frad LEE's original `superpowers` workflow. Thanks to Frad for the original structure, ideas, and implementation direction.

**Codex adaptation and customization**

Jerret (321jiangtao@gmail.com)
