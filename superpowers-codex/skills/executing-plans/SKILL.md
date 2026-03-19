---
name: executing-plans
description: Executes implementation plans in Codex using a persistent BDD repair loop, explicit task state, and optional sub-agent delegation.
---

# Executing Plans for Codex

This Codex variant replaces Claude's hook-based loop with two layers:

- an in-session repair loop driven by the lead agent
- an external watchdog that re-runs `codex exec --full-auto` until the state reaches a terminal condition

## Core Loop

For each task or batch:

1. Read the task and its BDD scenario.
2. Run the failing check first.
3. Delegate implementation to an `Implementer` if parallelism helps.
4. Re-run the BDD verification.
5. If the check fails, perform root-cause analysis before changing code again.
6. Escalate to `Reviewer` or `Architect` when retries stop converging.
7. Update loop state and continue until all scenarios are green.

## Completion Rules

The loop may stop only when all of the following are true:

- every required BDD scenario passes
- remaining task count is zero
- no reviewer findings remain unresolved
- loop state is marked `completed`

## Watchdog State

The watchdog reads `.codex/superpowers-loop/<run-id>/state.json`.

Suggested states:

- `running`
- `needs_retry`
- `blocked_awaiting_user`
- `completed`
- `failed_terminal`

`blocked_awaiting_user` is the only non-terminal state that intentionally pauses automatic continuation.

## Full-Auto Execution

The watchdog should invoke Codex like this:

```bash
codex exec --full-auto --cd <workdir> --add-dir "$HOME/.codex" "<prompt>"
```

`--full-auto` keeps execution low-friction while still respecting Codex's own sandbox and approval model.
