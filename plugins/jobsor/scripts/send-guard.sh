#!/bin/bash
# JOBSOR send guard (Cowork and Claude Code only; Chat ignores hooks). Runs before any Gmail send tool call and refuses it outside
# 9 AM to 12 midnight India time or above 50 sends in an India day, the hard ceiling (the user's own lower cap is kept by the send skill).
# Counts are kept in the plugin's data directory, one file per day; nothing else is stored.
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
date +%T >>"$log"
# Old day files are removed after 7 days.
find "$dir" -name 'sends-*.log' -mtime +7 -delete 2>/dev/null || true
exit 0
