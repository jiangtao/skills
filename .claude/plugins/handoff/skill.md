---
name: handoff
description: Session handoff for context continuity across Claude Code conversations
metadata:
  author: Jiangtao
  version: "0.0.2"
---

> Handoff skill preserves context across Claude Code sessions through structured markdown documents.

## Overview

The handoff skill enables seamless continuation of work across different Claude Code sessions by:
- Saving session context to structured markdown documents
- Automatic version tracking (v0.0.1, v0.0.2, ...)
- Loading previous handoffs with confirmation
- Preserving TODOs, decisions, and file locations

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Commands | Save and continue commands | [commands](references/commands.md) |
| Document Structure | Handoff document template | [template](references/template.md) |
| Best Practices | Usage guidelines | [best-practices](references/best-practices.md) |
