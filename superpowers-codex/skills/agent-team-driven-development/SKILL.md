---
name: agent-team-driven-development
description: Coordinates Codex sub-agents as an implementation team. Use when a plan has independent workstreams that benefit from explicit role ownership, parallel execution, and review gates.
---

# Agent Team Driven Development for Codex

Codex does not expose Claude's native teammate runtime, so this skill translates the same workflow into explicit sub-agent orchestration.

## Runtime Model

- The main Codex session is the team lead.
- `spawn_agent` creates role-based sub-agents.
- `send_input` assigns work and follow-up instructions.
- `wait_agent` is used only when the next critical-path step is blocked.
- `close_agent` shuts down finished workers.

## Roles

- `Architect`: breaks down cross-cutting work, resolves design conflicts, and unblocks retries after repeated failures.
- `Implementer`: owns one bounded task slice, follows BDD, and returns verification evidence.
- `Reviewer`: checks plan compliance, regressions, and missing tests before the task is accepted.

## Team Rules

1. The lead owns the plan and the shared state file.
2. Every sub-agent gets clear file ownership and must not revert others' work.
3. `Implementer` tasks must include the BDD scenario and the expected verification command.
4. `Reviewer` runs after implementation green, not before the first failing check.
5. After 2-3 failed repair loops on the same scenario, escalate to `Architect`.

## When to Use a Team

Use sub-agents when:
- at least two tasks are independent
- the files can be split cleanly
- review can happen in parallel with ongoing implementation

Stay in the lead session when:
- the task is highly coupled
- the next step depends on immediate local inspection
- only one small change remains
