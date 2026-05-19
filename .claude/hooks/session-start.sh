#!/bin/bash
# SessionStart hook — projet claude-os (à dupliquer dans chaque projet Claude).
# Rôle (v2.0) :
#   1. Charger CLAUDE-DNA-CC-CORE.md dans le contexte CC (stdout injecté en SessionStart).
#      - Local si présent (claude-os), sinon curl depuis raw GitHub.
#      - REF (procédures rares) curlé à la demande via le sommaire CORE §5.
#   2. Signaler les uploads from-cc/ en attente vers Chat.
#   3. Terminer par une ligne marqueur visible de confirmation.

set -e
DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
DNA_URL="https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-CORE.md"

# === 1. Charger DNA-CC-CORE ===
DNA_SRC=""
DNA_CONTENT=""
if [ -f "$DIR/CLAUDE-DNA-CC-CORE.md" ]; then
    DNA_CONTENT="$(cat "$DIR/CLAUDE-DNA-CC-CORE.md")"
    DNA_SRC="local"
else
    DNA_CONTENT="$(curl -sf --max-time 5 "$DNA_URL" 2>/dev/null || true)"
    if [ -n "$DNA_CONTENT" ]; then
        DNA_SRC="curl"
    else
        DNA_SRC="missing"
    fi
fi

if [ "$DNA_SRC" = "missing" ]; then
    echo "⚠ DNA-CC-CORE introuvable (fichier local absent + curl raw GitHub échoué). Session CC sans DNA — comportement non-déterministe."
else
    echo "$DNA_CONTENT"
fi

# === 2. Extraire la version chargée ===
VERSION="$(printf '%s\n' "$DNA_CONTENT" | grep -m1 '^\*\*Version' | sed 's/\*\*//g' || true)"
[ -z "$VERSION" ] && VERSION="Version : ?"

# === 3. Vérifier from-cc/_upload-status.json ===
PENDING_MSG=""
if [ -f "$DIR/from-cc/_upload-status.json" ]; then
    PENDING_MSG="$(python3 - <<PYEOF 2>/dev/null || true
import json, sys
try:
    with open("$DIR/from-cc/_upload-status.json") as f:
        d = json.load(f)
    p = [x for x in d.get("files", []) if x.get("pending")]
    if p:
        items = ", ".join(f"{x['path']} {x.get('current_version','?')} (code: {x.get('qa_code_ok','?')})" for x in p)
        print(f"{len(p)} upload(s) Chat pending : {items}")
except Exception:
    pass
PYEOF
)"
fi

# === 4. Ligne marqueur finale (toujours affichée) ===
echo ""
echo "---"
if [ -n "$PENDING_MSG" ]; then
    echo "✓ DNA-CC-CORE chargé ($DNA_SRC, $VERSION). REF accessible via sommaire (curl à la demande). ⚠ $PENDING_MSG"
else
    echo "✓ DNA-CC-CORE chargé ($DNA_SRC, $VERSION). REF accessible via sommaire (curl à la demande). Aucun upload Chat pending."
fi
