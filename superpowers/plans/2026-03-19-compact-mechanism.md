# Compact Mechanism Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add compact mechanism to preserve BDD Loop and Agent-Team state across Claude Code /compact operations

**Architecture:** Dual-layer storage (lightweight state.json + complete markdown), trigger points at phase completion/agent tasks/BDD retries, support both Claude Code (.claude/) and Codex (.codex/)

**Tech Stack:** Markdown templates, JSON state files, skill integration

---

## Task 1: Create Compact State Extractor Reference

**Files:**
- Create: `superpowers/skills/references/compact-state-extractor.md`

**Step 1: Create the state extractor reference document**

```markdown
# Compact State Extractor

## Purpose

Extract BDD Loop and Agent-Team state for compact operations.

## State Extraction Functions

### Extract BDD Loop State

```
