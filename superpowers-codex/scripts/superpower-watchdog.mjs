#!/usr/bin/env node

import { readFile, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import process from 'node:process'
import { spawn } from 'node:child_process'

const DEFAULT_MAX_RETRIES = 8

export function normalizeState(state) {
  return {
    status: 'running',
    retryCount: 0,
    maxRetries: DEFAULT_MAX_RETRIES,
    remainingTasks: [],
    failedScenarios: [],
    ...state,
  }
}

export function decideNextAction(state) {
  if (state.status === 'completed') {
    return { action: 'stop', reason: 'run completed' }
  }

  if (state.status === 'blocked_awaiting_user') {
    return { action: 'pause', reason: 'waiting for user input' }
  }

  if (state.status === 'failed_terminal') {
    return { action: 'fail', reason: 'run failed terminally' }
  }

  if (state.status === 'needs_retry' && state.retryCount >= state.maxRetries) {
    return { action: 'fail', reason: 'retry budget exhausted' }
  }

  if (state.status === 'needs_retry') {
    return { action: 'continue', reason: 'retry allowed' }
  }

  return { action: 'continue', reason: 'run still active' }
}

export function buildCodexExecArgs({ codexBin, codexHome, state, prompt }) {
  return [
    codexBin,
    'exec',
    '--full-auto',
    '--cd',
    state.workdir,
    '--add-dir',
    codexHome,
    prompt,
  ]
}

export async function readPrompt({ prompt, promptFile }) {
  if (prompt && prompt.trim()) {
    return prompt.trim()
  }

  if (!promptFile) {
    throw new Error('Missing prompt and promptFile')
  }

  return (await readFile(promptFile, 'utf8')).trim()
}

async function readState(stateFile) {
  if (!existsSync(stateFile)) {
    throw new Error(`State file not found: ${stateFile}`)
  }

  const raw = await readFile(stateFile, 'utf8')
  return normalizeState(JSON.parse(raw))
}

async function appendEvent(eventsFile, event) {
  const line = `${JSON.stringify({
    ts: new Date().toISOString(),
    ...event,
  })}\n`
  await writeFile(eventsFile, line, { flag: 'a' })
}

async function persistState(stateFile, state) {
  await writeFile(stateFile, `${JSON.stringify(state, null, 2)}\n`)
}

function parseArgs(argv) {
  const options = {
    codexBin: process.env.CODEX_BIN || 'codex',
    codexHome: process.env.CODEX_HOME || resolve(process.env.HOME || '~', '.codex'),
  }

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === '--state-file') {
      options.stateFile = argv[i + 1]
      i += 1
    }
    else if (arg === '--prompt') {
      options.prompt = argv[i + 1]
      i += 1
    }
    else if (arg === '--prompt-file') {
      options.promptFile = argv[i + 1]
      i += 1
    }
  }

  if (!options.stateFile) {
    throw new Error('Usage: superpower-watchdog.mjs --state-file <path> [--prompt <text>] [--prompt-file <path>]')
  }

  return options
}

async function runCodex(args, cwd) {
  await new Promise((resolvePromise, rejectPromise) => {
    const child = spawn(args[0], args.slice(1), {
      cwd,
      stdio: 'inherit',
      env: process.env,
    })

    child.on('error', rejectPromise)
    child.on('exit', (code) => {
      if (code === 0) {
        resolvePromise()
        return
      }
      rejectPromise(new Error(`Codex exited with code ${code}`))
    })
  })
}

async function main() {
  const options = parseArgs(process.argv.slice(2))
  const stateFile = resolve(options.stateFile)
  const eventsFile = resolve(dirname(stateFile), 'events.log')
  const state = await readState(stateFile)
  const decision = decideNextAction(state)

  await appendEvent(eventsFile, {
    type: 'watchdog.check',
    status: state.status,
    decision,
  })

  if (decision.action === 'stop' || decision.action === 'pause') {
    return
  }

  if (decision.action === 'fail') {
    state.status = 'failed_terminal'
    state.resumeReason = decision.reason
    await persistState(stateFile, state)
    return
  }

  const prompt = await readPrompt({
    prompt: options.prompt,
    promptFile: options.promptFile || state.promptFile,
  })
  const args = buildCodexExecArgs({
    codexBin: options.codexBin,
    codexHome: options.codexHome,
    state,
    prompt,
  })

  state.retryCount += 1
  state.lastRunCommand = args.join(' ')
  state.resumeReason = decision.reason
  await persistState(stateFile, state)
  await appendEvent(eventsFile, {
    type: 'watchdog.spawn',
    command: args,
  })

  await runCodex(args, state.workdir)
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(async (error) => {
    process.stderr.write(`${error.message}\n`)
    process.exitCode = 1
  })
}
