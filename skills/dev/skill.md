---
name: dev
description: Development workflow skills for verification, refactoring, commit process, and error handling
metadata:
  author: Jiangtao
  version: "0.2.0"
---

> Development workflow skills to improve code quality and reduce debugging iterations.

## Overview

The dev skill suite provides structured workflows for common development tasks:
- **Verify** - Automatic code change verification
- **Refactor Plan** - Complex multi-file refactoring
- **Commit** - Structured Git commit and PR workflow
- **Error Check** - Safe error handling modifications

These skills are based on insights from analyzing Claude Code usage patterns, addressing common friction points like:
- Buggy code requiring iterative fixes (37 occurrences)
- Missing verification steps before task completion
- Premature removal of error handling configurations
- Unstructured commit and review processes

## Core References

| Skill | Description | Reference |
|-------|-------------|-----------|
| verify | Verify code changes after implementation | [verify](references/verify.md) |
| refactor-plan | Plan complex refactoring tasks | [refactor-plan](references/refactor-plan.md) |
| commit | Structured Git commit and PR workflow | [commit](references/commit.md) |
| error-check | Check before modifying error handling | [error-check](references/error-check.md) |

## Usage

```bash
# Verify changes after implementation
/dev:verify

# Plan a complex refactoring
/dev:refactor-plan

# Create structured commit and PR
/dev:commit

# Check error handling before changes
/dev:error-check
```

## Integration with CLAUDE.md

These skills complement the Development Workflow section in CLAUDE.md:
- `/dev:verify` implements the mandatory verification steps
- `/dev:refactor-plan` follows the structured development approach
- `/dev:commit` follows the Git Commit Workflow (MANDATORY)
- `/dev:error-check` enforces safe error handling practices
