# Error Check - Safe Error Handling Modifications

## Purpose

Verify error handling before removing error-suppression configurations, preventing unhandled errors from reaching users.

## When to Use

- Before removing `ignoreError` configurations
- Before deleting error boundaries
- Before removing try-catch blocks
- When cleaning up technical debt related to error handling

## Four-Step Process

### 1. Audit Existing Error Handling
Search for all places this error type is caught/handled:
- Error boundaries (React)
- Try-catch blocks
- API interceptors
- Event handlers
- Middleware

### 2. Verify Downstream Handling
- Check if errors are properly propagated
- Verify user-facing error messages exist
- Ensure logging captures errors
- Confirm no silent failures

### 3. Remove Suppression
- Remove `ignoreError` config
- Delete error suppression middleware
- Remove silent catch blocks

### 4. Test Error Scenarios
- Trigger the error intentionally
- Verify graceful user experience
- Check error logging
- Confirm no unhandled rejections

## Usage in Claude Code

```
/dev:error-check
```

Then describe the error handling change.

## Examples

```
/dev:error-check
I want to remove the ignoreError config from the API client.

/dev:error-check
This try-catch is swallowing errors. Can I safely remove it?
```

## Common Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Removing ignoreError before adding proper handling | Errors reach UI as toast alerts | Verify downstream handling first |
| Deleting error boundaries | Entire app crashes on errors | Ensure parent boundaries exist |
| Silent catch removal | Unhandled promise rejections | Add explicit error propagation |

## Related CLAUDE.md Section

See `## Development Workflow > Language-Specific Guidelines > Error Handling`
