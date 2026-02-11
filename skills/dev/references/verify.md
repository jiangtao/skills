# Verify - Code Change Verification

## Purpose

Automatically verify code changes before considering a task complete, reducing the need for iterative debugging.

## When to Use

- After implementing any feature
- After fixing bugs
- After refactoring
- Before committing changes

## Verification Steps

### 1. Run Tests
```bash
# JavaScript/TypeScript
npm test
pnpm test

# Go
go test ./...

# Python
pytest
```

### 2. Start Development Server
```bash
# Next.js
npm run dev

# Go
go run main.go

# Vite
npm run dev
```

### 3. End-to-End Verification
- Test the user flow
- Check edge cases
- Verify error handling

### 4. Check Console
- Browser console for web apps
- Terminal output for CLI tools
- Server logs for APIs

### 5. Proceed Only After All Pass

## Usage in Claude Code

```
/dev:verify
```

## Expected Outcome

- All tests passing
- No console errors
- Feature working as expected
- Ready to commit

## Related CLAUDE.md Section

See `## Development Workflow > MANDATORY: Testing After Every Feature`
