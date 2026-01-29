---
name: best-practices
description: Handoff usage guidelines
---

# Handoff Best Practices

## When to Use Handoff

**Use when:**
- Session is ending and you want to preserve progress
- Switching to a different task
- Before taking a break
- When you want to resume work later

**Don't use for:**
- New projects with no context
- Simple single-session tasks
- Questions answerable from git history

## Best Practices

### 1. Always Include TODOs

Every handoff should capture next steps:

```markdown
### TODO
1. [ ] Fix authentication bug
2. [ ] Add error handling
3. [ ] Write tests
```

### 2. Use Absolute File Paths

Include full paths for important files:

```markdown
## Important File Locations
- `/Users/jt/places/personal/skills/src/auth.ts` - Authentication module
```

### 3. Document Decisions

Explain why, not just what:

```markdown
## Key Decisions
- **Chose JWT over sessions:** Stateless, scales better
- **Alternatives:** Session storage, OAuth
```

### 4. Run `/compact` After Saving

Clean your session after creating handoff:

```bash
/compact
```

### 5. Commit Handoffs to Git

Handoff documents should be version controlled:

```bash
git add docs/handoffs/
git commit -m "Add handoff for feature X"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No TODO items | Always include next steps |
| Missing file paths | Use absolute paths |
| No decisions documented | Explain the why |
| Not running /compact | Clean session after saving |
| Not committing to git | Version control handoffs |

## Tips

- Save frequently: Every time you complete a meaningful task
- Use descriptive names: `/handoff:save --name user-auth` instead of `/handoff:save --name work`
- Update before breaks: Save before stepping away
- Review on continue: Read through previous handoff when resuming
