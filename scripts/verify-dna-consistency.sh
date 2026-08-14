#!/bin/bash
# Vérifie la cohérence interne du DNA claude-os — automatise des checks que les cycles
# gaudit refaisaient manuellement à chaque passage (et qui ont laissé passer 4 cycles
# de suite un vrai décalage : CLAUDE-DNA-CC-REF.md §Historique en retard de 12 versions
# sur CLAUDE-DNA-CC-CORE.md, cf. audit/claude-os/REPORT-2026-08-14-2.md).
#
# Usage : depuis la racine de claude-os :
#   bash scripts/verify-dna-consistency.sh
#
# Sortie non-zéro si au moins un check échoue (utilisable en pre-check gaudit ou CI future).

set -u
cd "$(dirname "$0")/.." || exit 1

FAIL=0
warn() { echo "  ⚠️  $1"; FAIL=1; }
ok() { echo "  ✓ $1"; }

echo "== 1. Version CORE vs dernière entrée Historique de REF =="
CORE_VERSION=$(grep -m1 -oE '^\*\*Version : v[0-9]+\.[0-9]+' CLAUDE-DNA-CC-CORE.md | grep -oE 'v[0-9]+\.[0-9]+')
REF_LAST_VERSION=$(grep -m1 -oE '\| v[0-9]+\.[0-9]+ \(CORE\)| v[0-9]+\.[0-9]+ \| ' CLAUDE-DNA-CC-REF.md | head -1 | grep -oE 'v[0-9]+\.[0-9]+' | head -1)
if [ -z "$CORE_VERSION" ]; then
    warn "impossible d'extraire la version de CLAUDE-DNA-CC-CORE.md (format d'en-tête changé ?)"
elif [ "$CORE_VERSION" != "$REF_LAST_VERSION" ]; then
    warn "CORE est en $CORE_VERSION mais la 1ère ligne du tableau Historique de REF référence $REF_LAST_VERSION — REF est en retard, cf. §Historique"
else
    ok "REF §Historique à jour avec CORE ($CORE_VERSION)"
fi

echo "== 2. Bookkeeping to-chat/ cohérent avec CLAUDE-DNA-CHAT.md =="
CHAT_VERSION=$(grep -m1 -oE '^\*\*Version : v[0-9]+\.[0-9]+' CLAUDE-DNA-CHAT.md | grep -oE 'v[0-9]+\.[0-9]+')
STATUS_VERSION=$(grep -m1 -oE '"current_version": "v[0-9]+\.[0-9]+"' to-chat/_upload-status.json | grep -oE 'v[0-9]+\.[0-9]+')
if [ -z "$CHAT_VERSION" ] || [ -z "$STATUS_VERSION" ]; then
    warn "impossible d'extraire une des deux versions (CLAUDE-DNA-CHAT.md ou _upload-status.json)"
elif [ "$CHAT_VERSION" != "$STATUS_VERSION" ]; then
    warn "CLAUDE-DNA-CHAT.md est en $CHAT_VERSION mais to-chat/_upload-status.json déclare $STATUS_VERSION comme current_version — bookkeeping désynchronisé"
else
    ok "to-chat/_upload-status.json synchronisé avec CLAUDE-DNA-CHAT.md ($CHAT_VERSION)"
fi

echo "== 3. Liens Markdown relatifs cassés (fichiers racine) =="
BROKEN=0
for f in *.md; do
    while IFS= read -r link; do
        # ignore liens externes (http) et ancres pures (#...)
        case "$link" in
            http*|\#*) continue ;;
        esac
        target="${link%%#*}"  # retire une éventuelle ancre en suffixe
        [ -z "$target" ] && continue
        # ignore les exemples de syntaxe dans la doc (ex. `[nom](chemin/fichier:ligne)`) :
        # un vrai lien relatif du repo pointe vers un fichier/dossier existant, donc a une
        # extension connue ou finit en /
        case "$target" in
            *.md|*.md/*|*.sh|*.json|*/) ;;
            *) continue ;;
        esac
        if [ ! -e "$target" ]; then
            warn "$f → lien cassé vers '$target'"
            BROKEN=1
        fi
    done < <(grep -oE '\]\([^)]+\)' "$f" | sed -E 's/^\]\(//; s/\)$//')
done
[ "$BROKEN" -eq 0 ] && ok "aucun lien relatif cassé dans les fichiers racine"

echo "== 4. Skills .claude/skills/ toutes référencées (CLAUDE.md ou README.md) =="
for d in .claude/skills/*/; do
    name=$(basename "$d")
    if ! grep -qE "\`$name\`" CLAUDE.md README.md 2>/dev/null; then
        warn "skill '$name' présente sur disque mais non mentionnée dans CLAUDE.md/README.md"
    fi
done
ok "check skills terminé (voir avertissements ci-dessus s'il y en a)"

echo "== 5. En-tête HTML <!-- Version --> synchronisé avec la ligne visible **Version** =="
for f in CLAUDE-DNA-CC-CORE.md CLAUDE-DNA-CHAT.md CLAUDE-DNA-CC-REF.md; do
    visible=$(grep -m1 -oE '^\*\*Version : v[0-9]+\.[0-9]+' "$f" | grep -oE 'v[0-9]+\.[0-9]+')
    comment=$(grep -m1 -oE '<!-- Version : [0-9-]+ v[0-9]+\.[0-9]+' "$f" | grep -oE 'v[0-9]+\.[0-9]+')
    if [ -z "$visible" ] || [ -z "$comment" ]; then
        warn "$f : impossible d'extraire l'une des deux versions (format d'en-tête changé ?)"
    elif [ "$visible" != "$comment" ]; then
        warn "$f : ligne visible **Version** = $visible mais commentaire <!-- Version --> = $comment (convention CLAUDE-DNA-CHAT.md L134 / REF L54 : les deux doivent rester synchronisés)"
    else
        ok "$f : en-têtes synchronisés ($visible)"
    fi
done

echo
if [ "$FAIL" -eq 0 ]; then
    echo "✅ Tous les checks de cohérence DNA passent."
else
    echo "❌ Au moins un check a échoué — voir avertissements ⚠️  ci-dessus."
fi
exit $FAIL
