# État gaudit — point d'entrée unique

> **Lecture obligatoire en tout premier**, avant toute autre action, à chaque démarrage
> d'un cycle `gaudit` (session interactive ou firing de Routine). Ce fichier est la
> **seule source de vérité** de l'état d'avancement — aucune mémoire de conversation ne
> doit être supposée entre deux cycles. Toujours committer/pousser après modification.

## État courant

| Champ | Valeur |
|---|---|
| `repo_cible_courant` | `general` |
| `statut` | `terminé` |
| `dernier_heartbeat` | 2026-08-10T00:20Z |
| `fichier_plan_actif` | `audit/general/PLAN-2026-08-10.md` |
| `consignes_asana` | lues (aucune consigne, cf. commentaire d'accusé de réception 2026-08-10) |

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
| `claude-os` | 2026-08-10 | `audit/claude-os/REPORT-2026-08-10.md` |
| `general` | 2026-08-10 | `audit/general/REPORT-2026-08-10.md` |
| `candidaturePilote` | 2026-08-09 | `audit/candidaturePilote/REPORT-2026-08-09.md` |
| `ClaudeAchatMaison` | 2026-08-09 | `audit/ClaudeAchatMaison/REPORT-2026-08-09.md` |

## Historique des cycles

### 2026-08-10 — general — terminé
- Plan : `audit/general/PLAN-2026-08-10.md`
- Rapport : `audit/general/REPORT-2026-08-10.md`
- PR : aucune — repo inchangé depuis le cycle du 2026-08-07, aucun correctif identifié.

### 2026-08-10 — claude-os — terminé
- Plan : `audit/claude-os/PLAN-2026-08-10.md`
- Rapport : `audit/claude-os/REPORT-2026-08-10.md`
- PR : https://github.com/pignol-g/claude-os/pull/37 (durcit `SKILL.md` §5 — vérifier le push
  avant le commentaire Asana de clôture ; confirme la disponibilité MCP GitHub/Asana en Routine ;
  rafraîchit `REPRISE.md`)
- Enchaîné dans la foulée de la reconciliation ci-dessous (même cycle, même jour).

### 2026-08-10 — reconciliation (pas un cycle d'audit) — lacune de fiabilité découverte et corrigée

Au démarrage du cycle du 2026-08-10 (routine, repo attendu par rotation : `candidaturePilote`,
statut lu `in_progress` / heartbeat `2026-08-07T20:40Z`), la garde anti-collision ne s'appliquait
pas (heartbeat > 4h30) → reprise normale avec vérification du delta (SKILL §3). Le delta a
révélé que le plan `candidaturePilote` avait en réalité déjà été **entièrement exécuté et mergé**
le 2026-08-09 (PR #166), **et** qu'un cycle supplémentaire complet sur `ClaudeAchatMaison` avait
suivi le même jour (PR #37, ClaudeAchatMaison) — les deux confirmés par commit git mergé +
`pull_request_read` + le journal de commentaires de la tâche Asana consignes (accusés de
réception et « cycle terminé » postés aux deux repos le 2026-08-09 06:29–06:38Z). Aucune de ces
deux clôtures n'avait cependant atteint `claude-os/audit/` : ni `REPORT-*.md`, ni cases cochées
sur les plans, ni mise à jour de `STATE.md` (resté bloqué sur l'ancien pointeur `candidaturePilote
/ in_progress / 2026-08-07T20:40Z` pendant 3 jours).

**Cause probable** : le cycle du 2026-08-09 a exécuté le travail cible (git push sur le repo
audité + merge PR via l'outil GitHub) et le commentaire Asana « cycle terminé » (étape 6 du
SKILL) sans que le commit/push de `REPORT` + `STATE.md` côté `claude-os` (étapes 4-5) n'ait
réellement abouti sur `origin/main` — deux chemins d'écriture différents (git push vs appels
MCP GitHub/Asana) avec des modes de défaillance indépendants ; un échec silencieux du premier
(réseau, ou session interrompue entre les deux) n'a pas empêché les seconds de s'exécuter.
Conséquence concrète : `STATE.md` a menti sur l'état réel pendant 3 jours, et le cycle suivant a
dû reconstruire deux `REPORT` + cocher deux `PLAN` a posteriori à partir du diff GitHub et du
journal Asana plutôt que d'une clôture normale.

**Correctif appliqué à ce cycle** : `audit/candidaturePilote/PLAN-2026-08-07.md` (cases cochées
+ note de reconstruction), `audit/candidaturePilote/REPORT-2026-08-09.md`,
`audit/ClaudeAchatMaison/PLAN-2026-08-09.md`, `audit/ClaudeAchatMaison/REPORT-2026-08-09.md`
(les deux derniers recréés intégralement) et table de rotation ci-dessus mise à jour
(`candidaturePilote`/`ClaudeAchatMaison` → `2026-08-09`).

**Recommandation retenue pour un futur cycle `claude-os`** (Tier 1, pas encore exécutée à ce
stade du cycle 2026-08-10 — voir plan à venir si `claude-os` est la cible choisie ensuite) :
durcir `SKILL.md` §5 pour rendre l'ordre non ambigu et vérifiable — committer/pousser
`REPORT`+`STATE.md` côté `claude-os` **et vérifier que le push a atteint `origin` (comparer
`git rev-parse HEAD` local à `git ls-remote origin <branche>` après push, ou équivalent)** avant
de poster le commentaire Asana « cycle terminé ». Le commentaire Asana ne doit jamais pouvoir
être posté sans confirmation que la persistance disque a réellement abouti côté remote — c'est
justement le seul canal qui a donné une fausse impression de clôture ici.

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
