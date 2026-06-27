---
name: audit-auto-amelioration
description: >-
  ÉBAUCHE (à itérer avec Guillaume). Skill « mère » d'audit large + auto-amélioration autonome
  de TOUS les projets. Inspecte en profondeur (audit), propose des améliorations, les persiste
  en fichier, puis lance automatiquement les actions — d'abord correctrices (bugs/erreurs) puis
  amélioratrices — en consignant tout dans un rapport lisible. À invoquer quand Guillaume veut
  faire avancer ses projets sans y passer de temps lui-même, ou via routine planifiée.
---

# audit-auto-amelioration — audit large + auto-amélioration autonome

> **Statut : ÉBAUCHE v0.1** — brouillon demandé par Guillaume (tâche Asana 1208173596025174,
> réponse (b) : audit large multi-projets + auto-amélioration autonome). À travailler par
> itérations.

## Intention (mots de Guillaume)

> « Même si je n'ai pas le temps de faire avancer les projets, Claude le fait pour moi. Il
> inspecte d'abord en profondeur avec un audit. Propose des améliorations, persiste en fichier
> puis lance automatiquement les actions. En priorité les actions correctrices si des bugs /
> erreurs sont détectés, puis les améliorations. Tout doit être consigné dans un rapport. »

## Architecture : mère qui orchestre des skills filles

Cette skill **n'exécute pas tout elle-même** : elle orchestre.

- **Fille `audit`** — l'inspection profonde d'un projet (réutilise/étend l'existant :
  `audit-veille` côté pilote ; à généraliser aux autres projets).
- **Fille `auto-amelioration`** (≈ `gauto` / « avance autonome », tâche 1208173596025173,
  désormais sous-tâche de celle-ci) — l'exécution autonome des actions issues de l'audit.

## Logique d'orchestration (machine à états — reprise sur interruption)

À chaque lancement, **lire l'état du dernier run** (fichier d'état persistant, cf. ci-dessous)
et décider :

```
état du dernier run ?
├─ AUDIT non terminé      → REPRENDRE l'audit là où il s'est arrêté
├─ AUDIT terminé,
│  AUTO-AMÉLIO non finie   → REPRENDRE l'auto-amélioration (actions restantes)
└─ tout terminé           → LANCER un NOUVEL audit (nouveau cycle)
```

Priorité d'exécution des actions issues de l'audit :
1. **Correctives d'abord** — bugs / erreurs / incohérences détectés (ex : lien mort, donnée
   divergente, test cassé).
2. **Amélioratrices ensuite** — enrichissements, cohérence, dette.

## Persistance

- **Fichier d'état** par cycle (permet la reprise) : `AUTO-AMELIO-STATE.json` à la racine
  claude-os — `{ cycle, projet_courant, phase: audit|amelioration|done, actions_faites[],
  actions_restantes[] }`.
- **Rapport lisible** (demande explicite) : `RAPPORT-AUTO-AMELIO-YYYY-MM-DD.md` — ce qui a été
  audité, ce qui a été détecté (bugs vs améliorations), ce qui a été appliqué, les diffs/PR,
  et ce qui reste. Guillaume y lit l'évolution et ce qu'a fait la skill.
- **1 passe = 1 commit poussé** (granularité anti-interruption, conforme `gauto`).

## Safety (héritée de `gauto`)

Pas de merge PR ni d'envoi externe sans validation Guillaume ; pas de force-push / delete
branche / skip hooks. Toute action destructive ou ambiguë → s'arrêter et demander.

## Périmètre des projets audités

claude-os · candidaturePilote · ClaudeAchatMaison (à confirmer : ordre de priorité + un
projet par passe ou round-robin ?).

## Points ouverts à trancher (itération)

- **Niveau d'autonomie** : appliquer les correctives directement (sur branche + PR draft) ou
  seulement proposer ? Proposition d'ébauche : **appliquer sur branche dédiée + PR draft**
  (jamais merge auto) → Guillaume valide en relisant la PR.
- **Déclenchement** : manuel (`/audit-auto-amelioration`) et/ou planifié (routine), et/ou
  branché sur `routine-credit` (surplus de crédit → un cycle).
- **Définition du « fini »** d'un audit / d'une auto-amélioration (critère d'arrêt par phase).
