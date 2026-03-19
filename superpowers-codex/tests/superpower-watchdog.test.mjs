import test from 'node:test'
import assert from 'node:assert/strict'

import {
  buildCodexExecArgs,
  decideNextAction,
  normalizeState,
  readPrompt,
} from '../scripts/superpower-watchdog.mjs'

test('normalizeState fills defaults', () => {
  const state = normalizeState({
    workdir: '/tmp/project',
  })

  assert.equal(state.status, 'running')
  assert.equal(state.retryCount, 0)
  assert.equal(state.maxRetries, 8)
  assert.deepEqual(state.remainingTasks, [])
  assert.deepEqual(state.failedScenarios, [])
})

test('decideNextAction stops on completed runs', () => {
  const decision = decideNextAction(normalizeState({
    status: 'completed',
    workdir: '/tmp/project',
  }))

  assert.deepEqual(decision, {
    action: 'stop',
    reason: 'run completed',
  })
})

test('decideNextAction pauses when awaiting user input', () => {
  const decision = decideNextAction(normalizeState({
    status: 'blocked_awaiting_user',
    workdir: '/tmp/project',
  }))

  assert.deepEqual(decision, {
    action: 'pause',
    reason: 'waiting for user input',
  })
})

test('decideNextAction retries while under retry budget', () => {
  const decision = decideNextAction(normalizeState({
    status: 'needs_retry',
    workdir: '/tmp/project',
    retryCount: 2,
    maxRetries: 5,
  }))

  assert.deepEqual(decision, {
    action: 'continue',
    reason: 'retry allowed',
  })
})

test('decideNextAction fails terminally after exceeding retry budget', () => {
  const decision = decideNextAction(normalizeState({
    status: 'needs_retry',
    workdir: '/tmp/project',
    retryCount: 5,
    maxRetries: 5,
  }))

  assert.deepEqual(decision, {
    action: 'fail',
    reason: 'retry budget exhausted',
  })
})

test('buildCodexExecArgs uses full-auto and codex home access', () => {
  const args = buildCodexExecArgs({
    codexBin: 'codex',
    codexHome: '/Users/demo/.codex',
    state: normalizeState({
      workdir: '/repo',
      promptFile: '/repo/.codex/last-prompt.md',
    }),
    prompt: 'Continue the superpower loop.',
  })

  assert.deepEqual(args, [
    'codex',
    'exec',
    '--full-auto',
    '--cd',
    '/repo',
    '--add-dir',
    '/Users/demo/.codex',
    'Continue the superpower loop.',
  ])
})

test('readPrompt prefers inline prompt over prompt file', async () => {
  const prompt = await readPrompt({
    prompt: 'Inline prompt',
    promptFile: '/does/not/matter.md',
  })

  assert.equal(prompt, 'Inline prompt')
})
