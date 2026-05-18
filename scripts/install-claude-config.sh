#!/bin/bash
# Installe la config CC d'un projet : .claude/settings.json + .claude/hooks/session-start.sh
# Usage : depuis la racine du projet cible :
#   bash <path-vers-claude-os>/scripts/install-claude-config.sh
# Ou via curl si claude-os Drive inaccessible (ex : CC cloud) :
#   bash <(curl -s https://raw.githubusercontent.com/pignol-g/claude-os/main/scripts/install-claude-config.sh)

set -e

TARGET="${1:-$PWD}"
CLAUDE_OS_DRIVE="/Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os"
RAW_BASE="https://raw.githubusercontent.com/pignol-g/claude-os/main"

echo "Installation .claude/ vers : $TARGET"

mkdir -p "$TARGET/.claude/hooks"

# settings.json
if [ -f "$CLAUDE_OS_DRIVE/.claude/settings.json" ]; then
    cp "$CLAUDE_OS_DRIVE/.claude/settings.json" "$TARGET/.claude/settings.json"
    echo "  ✓ .claude/settings.json (depuis Drive)"
else
    curl -sf "$RAW_BASE/.claude/settings.json" -o "$TARGET/.claude/settings.json"
    echo "  ✓ .claude/settings.json (depuis curl)"
fi

# hooks/session-start.sh
if [ -f "$CLAUDE_OS_DRIVE/.claude/hooks/session-start.sh" ]; then
    cp "$CLAUDE_OS_DRIVE/.claude/hooks/session-start.sh" "$TARGET/.claude/hooks/session-start.sh"
    echo "  ✓ .claude/hooks/session-start.sh (depuis Drive)"
else
    curl -sf "$RAW_BASE/.claude/hooks/session-start.sh" -o "$TARGET/.claude/hooks/session-start.sh"
    echo "  ✓ .claude/hooks/session-start.sh (depuis curl)"
fi

chmod +x "$TARGET/.claude/hooks/session-start.sh"
echo "  ✓ hook exécutable"

echo "Installation terminée."
