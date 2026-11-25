#!/bin/bash
# Keeps the checker running: server + quick tunnel + register the tunnel URL with the relay.
D="$HOME/.jobsor-checker"
HERE="$(cd "$(dirname "$0")" && pwd)"
RELAY_URL="${RELAY_URL:-$(cat "$D/relay-url.txt" 2>/dev/null)}"
export REACHER_BIN="${REACHER_BIN:-$D/bin/check_if_email_exists}"
export CHECKER_SECRET="$(cat "$D/secret")"
NODE="${NODE_BIN:-$(command -v node || echo /opt/homebrew/bin/node)}"
CF="${CF_BIN:-$(command -v cloudflared || echo /opt/homebrew/bin/cloudflared)}"
mkdir -p "$D/log"

# stay awake while running
/usr/bin/caffeinate -is -w $$ &

SERVER_PID=""; CF_PID=""; REGISTERED=""
cleanup() { [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null; [ -n "$CF_PID" ] && kill "$CF_PID" 2>/dev/null; exit 0; }
trap cleanup TERM INT

while true; do
  if [ -z "$SERVER_PID" ] || ! kill -0 "$SERVER_PID" 2>/dev/null; then
    "$NODE" "$HERE/server.mjs" >> "$D/log/server.log" 2>&1 &
    SERVER_PID=$!
  fi
  if [ -z "$CF_PID" ] || ! kill -0 "$CF_PID" 2>/dev/null; then
    : > "$D/log/cloudflared.log"
    "$CF" tunnel --no-autoupdate --url http://127.0.0.1:8099 >> "$D/log/cloudflared.log" 2>&1 &
    CF_PID=$!
    REGISTERED=""
  fi
  if [ -z "$REGISTERED" ]; then
    URL=$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' "$D/log/cloudflared.log" | head -1)
    if [ -n "$URL" ] && [ -n "$RELAY_URL" ]; then
      CODE=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$RELAY_URL/register" \
        -H "x-checker-secret: $CHECKER_SECRET" -H 'content-type: application/json' \
        -d "{\"url\":\"$URL\"}")
      [ "$CODE" = "200" ] && REGISTERED=1
      echo "$(date) register: $CODE" >> "$D/log/start.log"
    fi
  fi
  sleep 5
done
