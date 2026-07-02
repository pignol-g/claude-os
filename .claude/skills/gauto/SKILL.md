---
name: gauto
description: >
  Mode autonome longue durée de Guillaume : Claude pilote seul jusqu'à arrêt explicite.
  À invoquer dès que Guillaume écrit `gauto` n'importe où dans un message (déclenchement
  inline), ou dit « pilote seul », « mode autonome », « continue sans moi ». Boucle pilotée
  (analyse état → plan priorisé → découpage atomique → exécution 1 commit+push/étape → MAJ
  REPRISE.md → reboucle), avec persistance/git, économie API et conditions d'arrêt. `gstop`
  (ou bouton stop, ou fin de crédits) désactive le mode et rebascule en interactif. Les
  SAFETY INTERDITS (pas de merge/force-push/delete-branch/--no-verify/modif hooks) restent
  des garde-fous non négociables rappelés dans le DNA-CORE.
---

# gauto / gstop — mode autonome longue durée

Quand Guillaume écrit `gauto` (n'importe où dans un message), Claude **pilote seul** jusqu'à
arrêt explicite. `gstop` désactive le mode et rebascule en mode interactif normal.

> **Source de vérité** : cette skill contient le corps de la boucle. Le `CLAUDE-DNA-CC-CORE.md`
> garde (a) une ligne-trigger qui pointe ici et (b) le rappel des **safety interdits**
> (garde-fous non déportables). Patron « CORE pointe, skill contient » validé 2026-07-01
> (PLAN-ARCHITECTURE-SKILLS.md chantier B, Q2 = skill invocable).

## Quand m'activer

- Guillaume écrit `gauto` (n'importe où dans le message).
- Formulations équivalentes : « pilote seul », « mode autonome », « continue sans moi
  jusqu'à ce que je dise stop ».

## Boucle pilotée (ne JAMAIS s'arrêter spontanément)

1. **Analyse** de l'état projet (`REPRISE.md`, INDEX, bien actif, TODO ouverts).
2. **Plan d'action** priorisé (Tier 1 / 2 / 3 par valeur opérationnelle).
3. **Découpage** en étapes atomiques.
4. **Exécution** étape par étape, **1 commit + push par étape significative**.
5. **MAJ `REPRISE.md`** à chaque cycle (état ultra-récupérable, comme si la session pouvait
   finir à l'improviste).
6. **Reboucler en (1)** dès le plan épuisé — ré-analyser, identifier les nouvelles priorités.

## Persistance & git

- Commit/push après chaque étape (pas de batch tardif).
- Avant chaque push : `git fetch origin && git rebase origin/main` (résolution de conflits
  autonome — historique `main` linéaire préservé).
- `RECAP-AUTO-YYYY-MM-DD.md` à la racine du projet, alimenté à chaque cycle + lien dans
  `REPRISE.md`.
- Documenter chaque décision autonome significative (pour revue de Guillaume au réveil).

## Économie API (jamais crasher)

- Batchs séquentiels, pas de pic multimodal parallèle (max 5 Read images/message).
- Retry doucement sur 529 (attente 30s puis abandon clean du cycle courant).
- Modèles légers (Sonnet/Haiku) pour Read volumineux ou tâches structurées.

## File d'attente inbox (`q:`) en session autonome

À la fin du plan principal, s'il reste des tokens, piocher dans `## ⏳ En attente` de l'inbox
(priorité 🔴 puis FIFO), traiter, déplacer en `## ✅ Traitées` avec réponse résumée
(3-5 lignes + lien analyse détaillée si applicable). Compte rendu en fin de session.

## Arrêt (3 conditions)

- (a) Extinction des crédits / session limit atteint.
- (b) Guillaume écrit `gstop`.
- (c) Bouton stop CC pressé.

Dans tous les cas, **dernier turn obligatoire** : MAJ `REPRISE.md` + `RECAP-AUTO` finalisé +
commit/push.

## Safety interdits (toute violation = arrêt + alerte Guillaume)

Rappelés aussi dans le DNA-CORE (garde-fous non déportables) :

- Pas de merge PR sans validation explicite de Guillaume.
- Pas de force-push (jamais).
- Pas de `git branch -D` ni delete de branche remote.
- Pas de `--no-verify` ni skip de hooks.
- Pas de modif `.claude/settings.json` ni des hooks `.claude/hooks/`.
