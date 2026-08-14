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
| `dernier_heartbeat` | 2026-08-14T10:38Z |
| `fichier_plan_actif` | `audit/general/PLAN-2026-08-14-3.md` |
| `consignes_asana` | lues (aucune consigne, cf. accusé de réception 2026-08-14T10:35Z) |

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
| `claude-os` | 2026-08-14 | `audit/claude-os/REPORT-2026-08-14-3.md` |
| `general` | 2026-08-14 | `audit/general/REPORT-2026-08-14-3.md` |
| `candidaturePilote` | 2026-08-14 | `audit/candidaturePilote/REPORT-2026-08-14-2.md` |
| `ClaudeAchatMaison` | 2026-08-14 | `audit/ClaudeAchatMaison/REPORT-2026-08-14-2.md` |

## Historique des cycles

### 2026-08-14 — general — terminé (3e cycle du jour, 5e tour de rotation)
- Plan : `audit/general/PLAN-2026-08-14-3.md`
- Rapport : `audit/general/REPORT-2026-08-14-3.md`
- PR : https://github.com/pignol-g/general/pull/6 (convention « ⚠️ Photo à date » pour les
  recherches à contenu volatil — documentée dans README.md/CLAUDE.md + rétrofit de 2
  fichiers) — mergée automatiquement (pas de CI, `mergeable_state: clean`).
- R&D menée en étape dédiée (cf. correctif de doctrine du cycle précédent) : 1 item Tier 2
  exécuté (badge photo à date) + 2 pistes Tier 3 documentées (migration réelle du profil
  rédactionnel — décision Guillaume déjà en attente ; pipeline `gtri` inactif depuis 3
  semaines — observation, non actionnable depuis `general`).
- Rotation : enchaîne sans pause sur `candidaturePilote` (prochain de la table).

### 2026-08-14 — claude-os — terminé (3e cycle du jour, 5e tour de rotation — 1er cycle post-correctif de doctrine)
- Plan : `audit/claude-os/PLAN-2026-08-14-3.md`
- Rapport : `audit/claude-os/REPORT-2026-08-14-3.md`
- PR : https://github.com/pignol-g/claude-os/pull/57 (script `scripts/verify-dna-
  consistency.sh` + resync 3 en-têtes de version + bump REF v2.2) — mergée automatiquement.
- **Retour direct de Guillaume ce jour** : gaudit s'arrêtait après chaque tour complet
  malgré §7 (3 conditions seulement), et la R&D avait disparu des diagnostics (0 item
  Tier 2/3 depuis 08-13 sur claude-os/general). `SKILL.md` corrigé (§6/§7 : tour complet
  ≠ condition d'arrêt ; §3 : R&D = étape dédiée). Ce cycle applique le correctif : enchaîne
  sans pause après la fin du 4e tour, et documente 3 vraies pistes R&D (Tier 3) au lieu de
  conclure "rien trouvé" par défaut.
- Rotation : enchaîne sans pause sur `general` (correctif de doctrine appliqué).

### 2026-08-14 — ClaudeAchatMaison — terminé (2ᵉ cycle du jour, fin du 4ᵉ tour complet de rotation)
- Plan : `audit/ClaudeAchatMaison/PLAN-2026-08-14-2.md`
- Rapport : `audit/ClaudeAchatMaison/REPORT-2026-08-14-2.md`
- PR : aucune — repo inchangé depuis le 2026-08-09, 3 PR ouvertes revérifiées (mergeabilité
  inchangée), mêmes raisons de non-intervention que les cycles précédents.
- 🔴 Alerte délai légal de réflexion vs échéance compromis 31/07 inchangée depuis ce matin
  même (déjà notifiée séparément), pas de nouvelle notification (situation non aggravée).
- Les 4 repos ont de nouveau `dernier_audit_termine = 2026-08-14` — fin du 4ᵉ tour complet.

### 2026-08-14 — candidaturePilote — terminé (2ᵉ cycle du jour)
- Plan : `audit/candidaturePilote/PLAN-2026-08-14-2.md`
- Rapport : `audit/candidaturePilote/REPORT-2026-08-14-2.md`
- PR : aucune côté `candidaturePilote` — travail direct via l'API GitHub (fermeture PR).
- 1 item traité (Tier 1) : trié les 4 PR jamais catégorisées par la revue #133 (#25/27/29/134,
  créées avant cette revue). #25 et #27 fermées comme superseded (vérification fraîche,
  dont un mail Gmail revérifié pour #27) ; #29 et #134 laissées ouvertes (décision Guillaume
  requise, gated explicitement ou draft incomplet).
- Rotation : `ClaudeAchatMaison` reste seul non repris ce 4e tour — j'enchaîne.

### 2026-08-14 — general — terminé (2ᵉ cycle du jour)
- Plan : `audit/general/PLAN-2026-08-14-2.md`
- Rapport : `audit/general/REPORT-2026-08-14-2.md`
- PR : aucune côté `general` — repo inchangé depuis le 2026-08-07 (5e cycle consécutif),
  relecture indépendante fichier par fichier, aucun bug ni incohérence trouvé.
- Rotation : `candidaturePilote`/`ClaudeAchatMaison` ex æquo à 2026-08-14 (granularité jour,
  pas encore repris ce 4e tour) — j'enchaîne sur `candidaturePilote` (premier de la table).

### 2026-08-14 — claude-os — terminé (2ᵉ cycle du jour, ouverture du 4ᵉ tour de rotation)
- Plan : `audit/claude-os/PLAN-2026-08-14-2.md`
- Rapport : `audit/claude-os/REPORT-2026-08-14-2.md`
- PR : https://github.com/pignol-g/claude-os/pull/50 (rattrape 12 entrées manquantes au
  tableau `## Historique` de `CLAUDE-DNA-CC-REF.md`, re-signalées « cosmétiques » 4 cycles
  de suite sans être corrigées ; vérification approfondie a montré un vrai déficit de
  traçabilité, corrigé plutôt que re-reporté) — mergée automatiquement (pas de CI, merge
  propre).
- Rotation : `general`/`candidaturePilote`/`ClaudeAchatMaison` ex æquo à 2026-08-14 —
  j'enchaîne sur `general` (premier de la table).

### 2026-08-14 — ClaudeAchatMaison — terminé (fin du 3ᵉ tour complet de rotation)
- Plan : `audit/ClaudeAchatMaison/PLAN-2026-08-14.md`
- Rapport : `audit/ClaudeAchatMaison/REPORT-2026-08-14.md`
- PR : aucune — 3 PR ouvertes revérifiées (mergeabilité inchangée), non touchées : mêmes
  raisons que le cycle 08-13 (#30/#36 propres mais contenu financier substantif, #31 en
  conflit). 2 biens `INDEX.md` périmés non requalifiés (décision, pas correctif mécanique).
- 🔴 Re-signalé (5ᵉ fois, encore aggravé) : alerte délai légal de réflexion vs échéance
  compromis du 31/07/2026, maintenant dépassée de 14 jours, aucune mise à jour tracée depuis
  le 27/07 (18 jours). Notification envoyée à Guillaume ce cycle (hors mécanisme gaudit
  standard, jugé suffisamment important/urgent pour sortir du canal Asana habituel).
- Les 4 repos ont de nouveau `dernier_audit_termine = 2026-08-14` — fin du 3ᵉ tour complet.

### 2026-08-14 — candidaturePilote — terminé
- Plan : `audit/candidaturePilote/PLAN-2026-08-14.md`
- Rapport : `audit/candidaturePilote/REPORT-2026-08-14.md`
- PR : https://github.com/pignol-g/candidaturePilote/pull/176 (chaîne MERGER #40/#46/#125
  revérifiée et réappliquée, PR fermées comme superseded ; #67 laissée ouverte, info
  contradictoire) — mergée automatiquement (CI verte, merge propre).
- Rotation : `ClaudeAchatMaison` reste seul à 2026-08-13, désormais le plus ancien —
  j'enchaîne.

### 2026-08-14 — general — terminé
- Plan : `audit/general/PLAN-2026-08-14.md`
- Rapport : `audit/general/REPORT-2026-08-14.md`
- PR : aucune côté `general` — repo inchangé depuis le 2026-08-07 (4e cycle consécutif sans
  changement), aucun bug ni incohérence trouvé à l'inventaire complet.
- Rotation : `candidaturePilote`/`ClaudeAchatMaison` ex æquo à 2026-08-13 — j'enchaîne sur
  `candidaturePilote` (premier de la table).

### 2026-08-14 — claude-os — terminé
- Plan : `audit/claude-os/PLAN-2026-08-14.md`
- Rapport : `audit/claude-os/REPORT-2026-08-14.md`
- PR : aucune côté contenu audité (rien à corriger, repo inchangé depuis le 2026-08-13) —
  comptabilité `audit/` de ce cycle committée sur `claude/bold-cerf-6m3tc6`.
- Rotation : `general`/`candidaturePilote`/`ClaudeAchatMaison` ex æquo à 2026-08-13 —
  j'enchaîne sur `general` (premier de la table).

### 2026-08-13 — ClaudeAchatMaison — terminé (fin du 2ᵉ tour complet de rotation)
- Plan : `audit/ClaudeAchatMaison/PLAN-2026-08-13.md`
- Rapport : `audit/ClaudeAchatMaison/REPORT-2026-08-13.md`
- PR : aucune — 3 PR ouvertes analysées (mergeabilité vérifiée localement), non touchées :
  #30/#36 propres mais contenu financier substantif (décision Guillaume), #31 en conflit et
  potentiellement pertinente pour la situation de prêt actuelle. Portée stratégique jugée
  hors correctif sûr, cohérent avec la décision du cycle du 2026-08-10 sur ce repo.
- 🔴 Re-signalé (4ᵉ fois, aggravé) : alerte délai légal de réflexion vs échéance compromis du
  31/07/2026 maintenant dépassée de 17 jours, aucune mise à jour tracée depuis le 27/07.
- Les 4 repos ont maintenant tous `dernier_audit_termine = 2026-08-13`.

### 2026-08-13 — candidaturePilote — terminé
- Plan : `audit/candidaturePilote/PLAN-2026-08-13.md`
- Rapport : `audit/candidaturePilote/REPORT-2026-08-13.md`
- PR : aucune côté `candidaturePilote` — travail effectué directement sur GitHub (PR/issues).
- **Constat majeur** : 35 PR ouvertes, aucune créée depuis le 2026-07-24 (activité de dev à
  l'arrêt net depuis 3 semaines, seule l'automatisation veille tourne). PR #133 (2026-07-24)
  avait déjà triage + recommandé 22 fermetures (17 candidaturePilote), jamais exécutées en
  3 semaines malgré 4 signalements successifs. Vérifié la fraîcheur puis exécuté la partie
  sûre : 17 PR fermées (#30, #35, #43, #60, #62, #64, #68, #71, #72, #77, #80, #83, #90, #93,
  #95, #128, #130), chacune commentée + suivi sur #133. Reste (mergeabilité à revérifier,
  arbitrage Guillaume, volet claude-os/ClaudeAchatMaison de la même revue, 116 issues veille
  sans mécanisme de clôture) documenté dans le rapport, non exécuté.
- Rotation : `ClaudeAchatMaison` reste seul à 2026-08-10, désormais le plus ancien — prochain
  repo par ordre de staleness.

### 2026-08-13 — general — terminé
- Plan : `audit/general/PLAN-2026-08-13.md`
- Rapport : `audit/general/REPORT-2026-08-13.md`
- PR : aucune côté `general` — repo inchangé depuis le 2026-08-10, aucun bug ni incohérence
  trouvé à l'inventaire complet.
- Rotation : `candidaturePilote`/`ClaudeAchatMaison` ex æquo à 2026-08-10 — j'enchaîne sur
  `candidaturePilote` (premier de la table).

### 2026-08-13 — claude-os — terminé
- Plan : `audit/claude-os/PLAN-2026-08-13.md`
- Rapport : `audit/claude-os/REPORT-2026-08-13.md`
- PR : https://github.com/pignol-g/claude-os/pull/41 (resynchronise `to-chat/_upload-status.json`
  / `_TODO.md` / `_track-log.md`, restés sur v2.1 depuis le bump v2.2 du 2026-08-07 — mergée
  automatiquement, pas de CI, merge propre)
- Rotation : `general`/`candidaturePilote`/`ClaudeAchatMaison` ex æquo à 2026-08-10, plus anciens
  désormais — j'enchaîne sur `general` (premier de la table).

### 2026-08-10 — ClaudeAchatMaison — terminé
- Plan : `audit/ClaudeAchatMaison/PLAN-2026-08-10.md`
- Rapport : `audit/ClaudeAchatMaison/REPORT-2026-08-10.md`
- PR : aucune — deux pistes mécaniques identifiées (statuts `biens/INDEX.md` périmés, sync
  knowledge claude.ai) volontairement non appliquées, portée stratégique jugée hors correctif
  sûr. Alerte 🔴 délai légal de réflexion vs échéance compromis 31/07 re-signalée (échéance
  désormais dépassée, aucune mise à jour tracée depuis le 27/07).
- **Fin du premier tour complet de rotation** : les 4 repos ont un `dernier_audit_termine =
  2026-08-10`.

### 2026-08-10 — candidaturePilote — terminé
- Plan : `audit/candidaturePilote/PLAN-2026-08-10.md`
- Rapport : `audit/candidaturePilote/REPORT-2026-08-10.md`
- PR : aucune — rien de nouveau depuis le cycle du 2026-08-09, fix du hook vérifié toujours en
  place.

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
