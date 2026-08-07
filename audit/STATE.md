# État gaudit — point d'entrée unique

> **Lecture obligatoire en tout premier**, avant toute autre action, à chaque démarrage
> d'un cycle `gaudit` (session interactive ou firing de Routine). Ce fichier est la
> **seule source de vérité** de l'état d'avancement — aucune mémoire de conversation ne
> doit être supposée entre deux cycles. Toujours committer/pousser après modification.

## État courant

| Champ | Valeur |
|---|---|
| `repo_cible_courant` | _(aucun — idle)_ |
| `statut` | `idle` |
| `dernier_heartbeat` | _(jamais)_ |
| `fichier_plan_actif` | _(aucun)_ |

**Statuts possibles** : `idle` (rien en cours) · `in_progress` (plan en cours d'exécution,
étapes en cours) · `terminé` (dernier plan bouclé, rapport écrit, en attente de rotation
vers le prochain repo).

**Garde anti-collision** : si `statut = in_progress` et `dernier_heartbeat` a moins de
~4h30, un cycle est probablement déjà en cours ailleurs — ne rien faire, s'arrêter
immédiatement (coût quasi nul). Sinon, considérer le cycle comme abandonné/repris et
continuer normalement (avec vérification du delta, cf. SKILL.md étape 3).

## Table de rotation (staleness)

Utilisée pour choisir le prochain repo à auditer quand aucune consigne n'est donnée dans
la tâche Asana permanente (gid `1217287685113494`, projet « Claude », section
« Section sans nom »). Choisir le repo avec `dernier_audit_termine` le plus ancien
(`jamais` = priorité maximale).

| Repo | Dernier audit terminé | Dernier rapport |
|---|---|---|
| `claude-os` | jamais | — |
| `general` | jamais | — |
| `candidaturePilote` | jamais | — |
| `ClaudeAchatMaison` | jamais | — |

## Historique des cycles

_(vide — première initialisation du système, 2026-08-07)_

<!-- Format d'entrée à l'ajout de chaque cycle terminé :
### AAAA-MM-JJ — <repo> — <statut final>
- Plan : audit/<repo>/PLAN-AAAA-MM-JJ.md
- Rapport : audit/<repo>/REPORT-AAAA-MM-JJ.md (si terminé)
- PR : <lien> (si ouverte)
-->
