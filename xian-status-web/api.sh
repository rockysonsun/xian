#!/bin/bash
# API endpoint for Xian Status

export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
export HOME="/Users/rocky"

# Get real-time data
VERSION=$(openclaw --version 2>/dev/null | head -1 | grep -o "2026\.[0-9]*\.[0-9]*" || echo "unknown")
if ps aux | grep -v grep | grep "openclaw-gateway" > /dev/null 2>&1; then
    GATEWAY_STATUS="running"
else
    GATEWAY_STATUS="stopped"
fi
SESSION_COUNT=$(openclaw status 2>/dev/null | grep -o "Sessions.*[0-9]* active" | grep -o "[0-9]*" || echo "0")
MODEL=$(openclaw status 2>/dev/null | grep "default" | grep -o "kimi[^)]*" || echo "unknown")
XIAN_STATUS=$(cat ~/.xian/status 2>/dev/null || echo "meditating")

# Output JSON
echo "Content-Type: application/json"
echo ""
echo "{"
echo "  \"version\": \"$VERSION\","
echo "  \"gateway\": \"$GATEWAY_STATUS\","
echo "  \"sessions\": $SESSION_COUNT,"
echo "  \"model\": \"$MODEL\","
echo "  \"xianStatus\": \"$XIAN_STATUS\","
echo "  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\""
echo "}"
