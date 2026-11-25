#!/bin/bash
# Stops the checker and removes the LaunchAgent. Keeps ~/.jobsor-checker (cache, secret).
PLIST="$HOME/Library/LaunchAgents/com.jobsor.emailchecker.plist"
launchctl bootout "gui/$UID" "$PLIST" 2>/dev/null || true
rm -f "$PLIST"
echo "Removed."
