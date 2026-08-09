# État gaudit — point d'entrée unique

> **Lecture obligatoire en tout premier**, avant toute autre action, à chaque démarrage
> d'un cycle `gaudit` (session interactive ou firing de Routine). Ce fichier est la
> **seule source de vérité** de l'état d'avancement — aucune mémoire de conversation ne
> doit être supposée entre deux cycles. Toujours committer/pousser après modification.

## État courant

| Champ | Valeur |
|---|---|
| `repo_cible_courant` | `ClaudeAchatMaison` |
| `statut` | `terminé` |
| `dernier_heartbeat` | 2026-08-09T06:45Z |
| `fichier_plan_actif` | `audit/ClaudeAchatMaison/PLAN-2026-08-09.md` |
| `consignes_asana` | lues (aucune nouvelle consigne) |

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
| `claude-os` | 2026-08-07 | `audit/claude-os/REPORT-2026-08-07.md` |
| `general` | 2026-08-07 | `audit/general/REPORT-2026-08-07.md` |
| `candidaturePilote` | 2026-08-09 | `audit/candidaturePilote/REPORT-2026-08-09.md` |
| `ClaudeAchatMaison` | 2026-08-09 | `audit/ClaudeAchatMaison/REPORT-2026-08-09.md` |

## Historique des cycles

### 2026-08-09 — ClaudeAchatMaison — terminé
- Plan : `audit/ClaudeAchatMaison/PLAN-2026-08-09.md`
- Rapport : `audit/ClaudeAchatMaison/REPORT-2026-08-09.md`
- PR : https://github.com/pignol-g/ClaudeAchatMaison/pull/37 (mergée automatiquement — pas de CI
  sur ce repo, merge propre)
- 🔴 **Risque signalé (hors scope gaudit, notifié séparément à Guillaume)** : alerte critique du
  27/07 non résolue dans `REPRISE.md` (délai légal réflexion offre de prêt vs échéance compromis
  31/07), aucune mise à jour du repo depuis le 07/08.
- Reporté (Tier 3, décision Guillaume requise) : bump `from-cc/knowledge-projet`/`instructions`
  (bloqué depuis 2026-06-03/05-20, contenu sensible/volumineux) ; réouverture `Q-001`/`Q-002` ;
  statut Rignieux-le-Franc 5971 potentiellement périmé.

### 2026-08-09 — candidaturePilote — terminé
- Plan : `audit/candidaturePilote/PLAN-2026-08-07.md`
- Rapport : `audit/candidaturePilote/REPORT-2026-08-09.md`
- PR : https://github.com/pignol-g/candidaturePilote/pull/166 (mergée automatiquement — CI non
  déclenchée sur ce diff (trigger `pull_request` filtré sur `scripts/veille/**`), merge propre)
- Reporté (Tier 3, décision Guillaume requise) : migration légère
  `from-cc/`/`from-chat/`/`to-claude-os/` → convention `to-chat/`/`to-cc/`/`to-os/` ;
  `from-chat/SKILL-1.md` de provenance peu claire.

### 2026-08-07 — general — terminé
- Plan : `audit/general/PLAN-2026-08-07.md`
- Rapport : `audit/general/REPORT-2026-08-07.md`
- PR : https://github.com/pignol-g/general/pull/5 (mergée automatiquement — pas de CI sur ce
  repo, merge propre)
- Reporté (Tier 3, décision Guillaume requise) : stub `perso/profil-redactionnel-guillaume.md`
  — voir `claude-os/INBOX-QUESTIONS.md` item 2026-07-21 (`R-002`).

### 2026-08-07 — claude-os — terminé
- Plan : `audit/claude-os/PLAN-2026-08-07.md`
- Rapport : `audit/claude-os/REPORT-2026-08-07.md`
- PR : https://github.com/pignol-g/claude-os/pull/34 (mergée automatiquement — pas de CI sur ce
  repo, merge propre)
- Risque signalé pour la suite : hook `session-start.sh` de `candidaturePilote` encore en v2.0
  (pas de git pull auto au démarrage) — candidat à prioriser au prochain cycle sur ce repo.

<!-- Format d'entrée à l'ajout de chaque cycle terminé :
### AAAA-MM-JJ — <repo> — <statut final>
- Plan : audit/<repo>/PLAN-AAAA-MM-JJ.md
- Rapport : audit/<repo>/REPORT-AAAA-MM-JJ.md (si terminé)
- PR : <lien> (si ouverte)
-->
