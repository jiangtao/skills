# Refactor Plan - Complex Refactoring Workflow

## Purpose

Plan and execute complex multi-file refactoring tasks systematically, with clear checkpoints and verification stages.

## When to Use

- Cross-language migrations (Bash → Go, JS → TS)
- Architecture changes affecting multiple files
- Dependency restructuring
- Large-scale refactoring with breaking changes

## Four-Stage Process

### Stage 1: Analysis
- Analyze current codebase structure
- Identify all affected components/files
- Map dependencies and relationships
- Assess risks and breaking changes

### Stage 2: Planning
- Create detailed migration plan with ordered stages
- Define checkpoints for verification
- Identify rollback points
- Estimate effort per stage

### Stage 3: Implementation
- Implement each stage following the plan
- Run tests after each stage
- Verify functionality before proceeding
- Document any deviations from the plan

### Stage 4: Verification
- Full test suite must pass
- Manual testing of affected features
- Performance benchmarks (if applicable)
- Documentation updates

## Output Format

```markdown
# Refactor Plan: [Description]

## Scope
- Files affected: N
- Estimated stages: N
- Risk level: Low/Medium/High

## Stages
1. [Stage name]
   - Files: list
   - Changes: description
   - Tests: required

2. [Stage name]
   - Files: list
   - Changes: description
   - Tests: required

## Dependencies
- Dependency graph
- Critical path

## Rollback Points
- After Stage 1
- After Stage 2
```

## Usage in Claude Code

```
/dev:refactor-plan
```

Then describe the refactoring task.

## Examples

```
/dev:refactor-plan
Convert this React codebase from JavaScript to TypeScript.

/dev:refactor-plan
Migrate from Redux to Zustand state management.
```

## Pro Tips

1. **Use Task Agents for Large Refactors**
   - Agent 1: Map dependencies
   - Agent 2: Generate migration plan
   - Agent 3: Execute changes

2. **Verify Each Stage**
   - Never proceed to next stage without verification
   - Run `/dev:verify` after each stage

3. **Document Rollback Points**
   - Commit after each successful stage
   - Tag commits for easy rollback
