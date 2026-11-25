#!/bin/bash
# Usage: bash install.sh /path/to/check_if_email_exists   (the Reacher binary)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
D="$HOME/.jobsor-checker"
BIN_SRC="$1"
[ -f "$BIN_SRC" ] || { echo "Give the path to the Reacher binary as the first argument."; exit 1; }
command -v cloudflared >/dev/null || brew install cloudflared
mkdir -p "$D/bin" "$D/log" "$HOME/Library/LaunchAgents"
cp "$BIN_SRC" "$D/bin/check_if_email_exists"; chmod +x "$D/bin/check_if_email_exists"
if [ ! -f "$D/secret" ]; then (umask 077; openssl rand -hex 24 > "$D/secret"); fi
chmod 600 "$D/secret"
RELAY="${RELAY_URL:-$(cat "$D/relay-url.txt" 2>/dev/null)}"
[ -n "$RELAY" ] || { echo "Set RELAY_URL (the relay's workers.dev address) or put it in $D/relay-url.txt"; exit 1; }
echo "$RELAY" > "$D/relay-url.txt"
# the address to paste into claude.ai (contains the secret, kept in a file only)
(umask 077; printf '%s/mcp/%s\n' "$RELAY" "$(cat "$D/secret")" > "$D/connector-url.txt")
chmod 600 "$D/connector-url.txt"
PLIST="$HOME/Library/LaunchAgents/com.jobsor.emailchecker.plist"
sed -e "s#__START__#$HERE/start.sh#g" -e "s#__LOG__#$D/log#g" -e "s#__PATH__#/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin#g" \
  "$HERE/com.jobsor.emailchecker.plist" > "$PLIST"
launchctl bootout "gui/$UID" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$UID" "$PLIST"
echo "Installed and started."
echo "Your connector address is in ~/.jobsor-checker/connector-url.txt"
