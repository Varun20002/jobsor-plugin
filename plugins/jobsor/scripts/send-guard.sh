#!/bin/bash
# JOBSOR send guard (Cowork and Claude Code only; Chat ignores hooks). Runs before any Gmail send tool call and refuses it outside
# 9 AM to 12 midnight India time or above 50 sends in an India day, the hard ceiling (the user's own lower cap is kept by the send skill).
# It then runs the content check (skills/send/scripts/check_message.py --hook: no JOBSOR ids, placeholders, banned phrases) and refuses a
# message that fails it. A missing python3 or a broken check lets the send through, so a broken check never blocks all mail.
# Counts are kept in the plugin's data directory, one file per day; nothing else is stored. The day count file does not survive between
# cloud runs, so in the cloud the send skill's own count of today's Sent rows is the cap.
set -u
CAP=50
dir="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/jobsor}"
mkdir -p "$dir" 2>/dev/null || true
day=$(TZ=Asia/Kolkata date +%F)
hour="${JOBSOR_TEST_HOUR:-$(TZ=Asia/Kolkata date +%H)}" # JOBSOR_TEST_HOUR only for the guard's own test
log="$dir/sends-$day.log"
input=$(cat)
# Claude's own Gmail connector has no "gmail" in its tool names (e.g. mcp__<id>__send_message), so the hook matches any send, reply or
# forward tool, and this check lets through anything that is clearly not Gmail (Slack and others: no email fields in the call).
case "$input" in
  *[Gg]mail*|*'"to"'*|*'"draftId"'*|*'"replyThreadId"'*|*'"messageId"'*) ;;
  *) exit 0 ;;
esac
if [ "$((10#$hour))" -lt 9 ]; then
  echo "JOBSOR: no sending between 12 midnight and 9 AM India time. Leave it as a draft; the round sends after 9 AM." >&2
  exit 2
fi
count=$( [ -f "$log" ] && wc -l <"$log" | tr -d ' ' || echo 0 )
if [ "$count" -ge "$CAP" ]; then
  echo "JOBSOR: $CAP emails already sent today (India time), the most JOBSOR allows. Leave the rest as drafts for tomorrow." >&2
  exit 2
fi
if command -v python3 >/dev/null 2>&1; then
  result=$(printf '%s' "$input" | python3 -I "${CLAUDE_PLUGIN_ROOT:-.}/skills/send/scripts/check_message.py" --hook 2>/dev/null)
  if [ "$?" -eq 3 ]; then
    problems=$(printf '%s' "$result" | python3 -I -c 'import json,sys; print("; ".join(json.load(sys.stdin)["problems"]))' 2>/dev/null)
    echo "JOBSOR check refused this email: ${problems:-see the JOBSOR check}" >&2
    exit 2
  fi
fi
date +%T >>"$log"
# Old day files are removed after 7 days.
find "$dir" -name 'sends-*.log' -mtime +7 -delete 2>/dev/null || true
exit 0
