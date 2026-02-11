# Commit - Structured Git Commit and PR Workflow

## Purpose

Enforce a structured 5-step Git commit and Pull Request workflow to ensure code quality and proper review.

## When to Use

- Before committing any code changes
- When creating a Pull Request
- Before merging to main branch

## Five-Step Workflow (MANDATORY)

### Step 1: Create Branch & Summarize Changes

Create a new branch with a descriptive name and summarize the change in one sentence.

```bash
# Branch naming convention
git checkout -b feat/add-dev-skill
git checkout -b fix/error-handling
git checkout -b refactor/cleanup-code
git checkout -b docs/update-readme
git checkout -b test/add-unit-tests
```

**One-line summary template:**
```
<type>: <what changed> → <outcome/benefit>

Examples:
- feat: Add dev skill for workflow verification → Reduce debugging iterations
- fix: Remove ignoreError from API client → Proper error handling
- refactor: Migrate Bash scripts to Go → Better maintainability
- docs: Update README with new skills → Better discoverability
```

### Step 2: Create PR with Change Summary

Create a Pull Request with structured summary.

```markdown
## Summary
<!-- One sentence describing the change -->

## Changes
- [ ] File path - Description of change
- [ ] File path - Description of change
- [ ] File path - Description of change

## Type
- [ ] feat - New feature
- [ ] fix - Bug fix
- [ ] refactor - Code restructuring (no behavior change)
- [ ] docs - Documentation only
- [ ] test - Tests only
- [ ] chore - Build/config changes

## Related Issue
Closes #(issue number) or Relates to #(issue number)
```

### Step 3: Define Test Cases (Test First)

Before running tests, explicitly define what will be tested.

```markdown
## Test Plan

### Unit Tests
- [ ] Test case 1: Description
- [ ] Test case 2: Description
- [ ] Test case 3: Description

### Integration Tests
- [ ] Test case 1: Description
- [ ] Test case 2: Description

### Manual Tests
- [ ] Test case 1: Description
- [ ] Test case 2: Description

### Edge Cases
- [ ] Test case 1: Description
- [ ] Test case 2: Description
```

### Step 4: Run Tests & Generate Report

Execute all tests and generate a feedback report.

```bash
# Run test suite
npm test
# or
go test ./...
# or
pytest

# Run build (if applicable)
npm run build

# Run linter
npm run lint
```

**Test Report Template:**
```markdown
## Test Results

### Summary
| Category | Total | Passed | Failed |
|----------|-------|--------|--------|
| Unit Tests | N | N | N |
| Integration Tests | N | N | N |
| Manual Tests | N | N | N |

### Passed Tests
<!-- List key tests that passed -->

### Failed Tests
<!-- List any failures with details -->

### Issues Found
<!-- Document any issues discovered during testing -->

### Build Status
- [ ] Build successful
- [ ] Linting passed
- [ ] No console errors
- [ ] No type errors
```

### Step 5: User Review

User reviews the following before approving merge:

```markdown
## Review Checklist
- [ ] Code changes align with the one-line summary
- [ ] All tests pass (no failures)
- [ ] Documentation is updated (if applicable)
- [ ] No unintended side effects
- [ ] Edge cases are covered
- [ ] Code follows project style guidelines
```

**Only after all 5 steps are completed and approved, merge to main.**

## Usage in Claude Code

```
/dev:commit
```

Then describe the changes you want to commit.

## Examples

```
/dev:commit
I've added the dev skill with verify, refactor-plan, and error-check.
The changes include:
- skills/dev/skill.md
- skills/dev/references/verify.md
- skills/dev/references/refactor-plan.md
- skills/dev/references/error-check.md
```

## Quick Reference

| Step | Action | Command |
|------|--------|---------|
| 1 | Create branch | `git checkout -b type/description` |
| 2 | Create PR | `gh pr create --title "Summary" --body-file pr.md` |
| 3 | Define tests | Add test plan to PR description |
| 4 | Run tests | `npm test && npm run build && npm run lint` |
| 5 | User review | Review checklist in PR comments |

## Commit Message Convention

When committing to the branch, use conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, refactor, docs, test, chore

**Example:**
```
feat(dev): add commit workflow skill

- Add /dev:commit for structured Git workflow
- Update skill.md version to 0.2.0
- Create commit.md reference documentation

Closes #42
```

## Related CLAUDE.md Section

See `## Development Workflow > Git Commit Workflow (MANDATORY)`
