#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
WATCHDOG="$SCRIPT_DIR/superpower-watchdog.mjs"

if [ $# -lt 1 ]; then
  echo "Usage: start-superpower-loop.sh <state-file> [prompt-file]" >&2
  exit 1
fi

STATE_FILE=$1
PROMPT_FILE=${2:-}

if [ -n "$PROMPT_FILE" ]; then
  exec node "$WATCHDOG" --state-file "$STATE_FILE" --prompt-file "$PROMPT_FILE"
fi

exec node "$WATCHDOG" --state-file "$STATE_FILE"
