#!/bin/bash
# SessionStart hook — projet claude-os (à dupliquer dans chaque projet Claude).
# Rôle (v2.1) :
#   1. **Git pull origin main au démarrage** (v2.1, hookpullA — synchroniser local avec remote,
#      évite de bosser sur une ancienne version comme cela s'est produit le 27/05/2026).
#   2. Charger CLAUDE-DNA-CC-CORE.md dans le contexte CC (stdout injecté en SessionStart).
#      - Local si présent (claude-os), sinon curl depuis raw GitHub.
#      - REF (procédures rares) curlé à la demande via le sommaire CORE §5.
#   3. Signaler les uploads to-chat/ en attente vers Chat.
#   4. Terminer par une ligne marqueur visible de confirmation.

set -e
DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
DNA_URL="https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-CORE.md"

# === 0. Git pull origin main (v2.1, hookpullA) ===
# Synchronise le repo local avec le remote en début de session pour éviter de bosser sur
# une ancienne version. Échec doux : si conflits locaux non commités ou pas de réseau,
# on log un warning mais on continue la session (DNA doit charger même offline).
GITPULL_MSG=""
if [ -d "$DIR/.git" ]; then
    # Vérifier qu'on n'a pas de changements non commités qui bloqueraient le pull --rebase
    if cd "$DIR" 2>/dev/null && git diff --quiet HEAD 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
        # Working tree clean — pull rebase
        if PULL_OUT="$(cd "$DIR" && git pull --rebase --autostash origin main 2>&1)"; then
            if echo "$PULL_OUT" | grep -q "Already up to date\|Already up-to-date"; then
                GITPULL_MSG="✓ Git à jour avec origin/main (rien à puller)."
            else
                CHANGED="$(echo "$PULL_OUT" | grep -E "^\s*\d+\s+file" | head -1 || echo "fast-forward")"
                GITPULL_MSG="✓ Git pull origin main OK ($CHANGED)."
            fi
        else
            GITPULL_MSG="⚠ Git pull origin main ÉCHEC : $(echo "$PULL_OUT" | tr '\n' ' ' | cut -c1-200). À résoudre manuellement avant tout commit."
        fi
    else
        GITPULL_MSG="⚠ Changements locaux non commités — git pull skippé. Commit/stash d'abord puis 'git pull --rebase origin main' manuel."
    fi
else
    GITPULL_MSG="Pas un repo git (pas de .git) — pull skippé."
fi
echo "$GITPULL_MSG"
echo ""

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

# === 3. Vérifier to-chat/_upload-status.json (fallback legacy from-cc/) ===
PENDING_MSG=""
STATUS_FILE="$DIR/to-chat/_upload-status.json"
[ -f "$STATUS_FILE" ] || STATUS_FILE="$DIR/from-cc/_upload-status.json"
if [ -f "$STATUS_FILE" ]; then
    PENDING_MSG="$(STATUS_FILE="$STATUS_FILE" python3 - <<PYEOF 2>/dev/null || true
import json, os, sys
try:
    with open(os.environ["STATUS_FILE"]) as f:
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
echo "  Git : $GITPULL_MSG"
