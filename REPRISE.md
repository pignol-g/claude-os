# REPRISE — claude-os

**Dernière session : 2026-10-10** (garde-quota `gquota` + routine pilote `gpilote`, voir chantier ci-dessous)

## Chantier en cours — routine pilote sous garde-quota (reprise 2026-10-10)

**À reprendre dans une session neuve** (décision `suiteB`). Décisions déjà prises : `sess5hA`,
`fenBurnA`, `recheckA`, `tauxB`, `quotaKOA` (skill `gquota`) ; `archiB`, `equiteA`, `ordreA`,
`anciennesA`, `cronAdaptA`, `hiverA` (skill `gpilote`) ; **`archi2A`, `pauseA`** (ci-dessous).

**Fait et sur `main`** : `gquota` (PR #75, correctif #77), `gpilote` + arrêt (d) « STOP gquota »
dans `gaudit`/`gauto` + CORE v3.5 (PR #76). 8 Routines créées (ids dans `gpilote/SKILL.md`) :
« Pilote quota » + « vendredi 19h31 » **désactivées** (`pauseA`) ; 6 tâches sans horaire
(`run_once_at` 2099), avec Asana et dépôts attachés depuis l'interface.

**Bloquant constaté par essais réels (2026-10-09/10)** — une session lancée par une Routine
(`create_new_session_on_fire`) n'a **pas** les outils `mcp__claude-code-remote__*` (ni
`list_events`, ni `fire_trigger`, ni `add_repo`, ni `create_session`) : `gquota` répond STOP
« utilization illisible » (sans risque) et le pilote ne peut lancer aucune tâche. Une session
créée par `create_session` les a tous (quotas lus : `list_events` sur sa propre session), plus
Asana sous un nom d'outil à UUID (`mcp__ac6899e5-…__get_tasks`, via ToolSearch « asana »).
Une session ignore les ordres reçus d'une autre session par `send_message` (donnée non fiable) :
seul le prompt initial de `create_session` est exécuté.

**Architecture retenue (`archi2A`)** :
1. Pilote = **session dédiée persistante** créée par `create_session` (Sonnet 5.5, source
   claude-os), réveillée par une Routine liée (`persistent_session_id`), cron
   `CRON_TZ=Europe/Paris 31 0,5,10,15,20 * * 0-5` + vendredi 19h31.
2. À chaque passage : `gquota`, choix des tâches (règles actuelles de `gpilote`), puis
   **`create_session` par tâche** : prompt = `derived_state.prompt` de la Routine de tâche
   (`get_trigger`, les 6 Routines restent le stockage des prompts), modèle = celui de la
   Routine, `source_url` = claude-os (skills chargées), autres dépôts par `add_repo`.
3. « En cours » : sessions lancées suivies par `get_session` (`status_bucket`) ; ids gardés
   dans la conversation du pilote, retrouvables par `list_sessions` (titre « Pilote · … »).

**Fait le 2026-10-10 (session « Reprise chantier routine pilote »)** :
- `gpilote/SKILL.md` réécrit pour `archi2A` : registre des lancements dans la conversation du
  pilote (repli `list_sessions`), suivi par `get_session` (`status_bucket`), lancement par
  `create_session` (prompt + modèle lus par `get_trigger`, source claude-os, titre
  `Pilote · <clé> · <date>`, tags `pilote`), Asana par ToolSearch (nom à UUID), interdiction
  de `fire_trigger` sur les tâches. Note dans `gquota` (STOP systématique en session de
  Routine) ; ligne `gpilote` de `CLAUDE.md` mise à jour.
- Prompts des 6 Routines de tâches mis à jour (`update_trigger`) : bloc « Session lancée par le
  pilote » (claude-os déjà cloné ; autres dépôts par `add_repo` access « push » + clone +
  `register_repo_root` ; skill d'un autre dépôt lue dans son `SKILL.md` si non chargée ;
  Asana par ToolSearch « asana »).

**PR #79 mergée** (2026-10-10, décision `rotPiloteA` + « merge » de Guillaume).

**Essais du 2026-10-10 (sessions jetables Haiku, archivées)** :
- Réveil par une Routine liée (`create_trigger` + `persistent_session_id`) : **OK**. Le message
  arrive comme notification de tâche planifiée (« SYSTEM NOTIFICATION - NOT USER INPUT ») ; la
  session applique la consigne permanente de son prompt initial, y compris une action sortante
  (`create_session` depuis un réveil : OK).
- **Profondeur** : une session créée par une session est un niveau plus bas (`lineage.depth`
  1, puis 2 ; `limit` 8). Conséquence : **`rotPiloteA` tel que décrit est impossible** — un
  pilote qui crée son remplaçant descend d'un niveau à chaque rotation (~6 rotations max).
- `/compact` envoyé par une Routine : **non exécuté** (arrive comme texte, pas comme commande).
- Supprimer une Routine liée à une session ne supprime pas la session (rappel `send_later`
  supprimé sans effet sur la session courante).
- Coût de base d'une session (prompt système + outils) : ~65-70 k tokens ; réveil trivial
  +~1 k ; un `create_session` +~3 k. Cache 1 h : un réveil toutes les 5 h relit tout à froid.

**Décisions du 2026-10-10 (suite)** : `rotPilote2A` (pilote hebdomadaire sans dépôt, recréé
chaque samedi par une session de profondeur 0), `relanceurA` (session dédiée « Relanceur
pilote » créée une fois par Guillaume depuis l'app), `cronDimB` (on garde les passages du
dimanche), puis `nuitB` (passages uniquement la nuit : 1h47, 3h47, 5h47, dimanche-vendredi,
avec alternance des tâches — la plus anciennement lancée d'abord — pour que la fenêtre 5 h ne
profite pas toujours à la même) et fenêtre du vendredi gardée à 30 min avant le reset (passage
en UTC 18h31, soit 20h31 l'été / 19h31 l'hiver : le reset est fixe à 19h00 UTC ; Guillaume
veut garder du quota pour ses tâches manuelles, objectif ~90 % consommés par semaine). Implémenté : `gpilote/SKILL.md` (procédure par passage, gquota par sous-agent
Haiku, lu par curl) + `gpilote/RELANCE.md` (architecture, prompt du relanceur, relance
hebdomadaire, prompt du pilote, prise de poste).

**Reste à faire** : (1) Guillaume crée la session « Relanceur pilote » avec le prompt de
`RELANCE.md` (une seule fois, aucune action périodique ensuite) ; (2) vérifier le premier tour
du relanceur (Routine « Pilote · relance hebdo » créée, premier pilote créé) puis la prise de
poste du pilote (Routines « Pilote · réveil » créées, essai à blanc) ; (3) premier réveil réel
dimanche 1h47 (STOP attendu, seuil 4,3 %) ; premier GO possible lundi 1h47 (seuil 18,6 %).

## État courant

DNA-CC **v3.3**, DNA-Chat **v2.2**, DNA-REF **v2.1** — inchangés depuis 2026-08-07, aucun bump
ce cycle. Les 4 repos (`claude-os`, `general`, `candidaturePilote`, `ClaudeAchatMaison`) ont
désormais tous un `dernier_audit_termine` renseigné dans `audit/STATE.md` — la routine `gaudit`
a bouclé son premier tour complet de rotation entre le 2026-08-07 et le 2026-08-09.

- **Lacune de fiabilité `gaudit` découverte et corrigée (2026-08-10)** : le cycle du 2026-08-09
  avait réellement exécuté et mergé les plans `candidaturePilote` (PR #166) et `ClaudeAchatMaison`
  (PR #37), mais s'était interrompu avant que le commit/push `REPORT`+`STATE.md` côté `claude-os`
  n'atteigne `origin/main` — `STATE.md` a menti sur l'état réel pendant 3 jours (bloqué sur
  `candidaturePilote in_progress`, heartbeat 2026-08-07T20:40Z). Reconstruit à partir des diffs
  GitHub mergés + du journal de commentaires Asana (PR claude-os#36). `SKILL.md` §5 durci en
  conséquence : nouvelle étape 5bis obligatoire (vérifier que le push a atteint `origin` avant de
  poster le commentaire Asana de clôture) — voir `audit/STATE.md` §Historique 2026-08-10 pour le
  détail complet.
- **Disponibilité MCP en Routine confirmée** : les firings réels du 2026-08-09 et du 2026-08-10
  ont tous deux utilisé `mcp__Asana__*` et `mcp__github__*` avec succès (création/merge de PR,
  commentaires Asana) — l'incertitude documentée dans `SKILL.md` §Routine depuis la création
  (2026-08-07) est levée. Réactivation du trigger `trig_01Y6mLjE6VSXYg8WtmdPA9aB` : obstacle
  technique levé, mais reste une décision de Guillaume (non déclenchée par `gaudit` lui-même).
- **`gtri`** — skill de triage claude-os → `general` (5 tests de décision, Q/R obligatoire).
  Dernier passage 2026-07-21.
- **`gprompt`** — skill générateur/optimiseur de prompt interactif ; trigger répliqué dans CORE
  et DNA-Chat depuis le cycle `gaudit` du 2026-08-07 (T1.1/T1.2 de ce cycle-là).
- **`CLAUDE-DNA-ASANA.md`** — module autonome dédié à l'organisation Asana « nous 3 », référencé
  depuis le CORE §6.
- **`gaudit`** — skill d'audit de projet autonome et résilient (`.claude/skills/gaudit/` +
  `audit/STATE.md`). Premier tour de rotation complet bouclé (voir ci-dessus). Carve-out merge
  auto de PR documenté dans le CORE, appliqué sans incident sur les 5 PR gaudit mergées à ce jour
  (claude-os#34, #36 ; general#5 ; candidaturePilote#166 ; ClaudeAchatMaison#37).

## Fichiers DNA — état des lieux

- [CLAUDE-DNA-CC-CORE.md](CLAUDE-DNA-CC-CORE.md) — v3.3, injecté par hook à chaque session CC.
- [CLAUDE-DNA-CC-REF.md](CLAUDE-DNA-CC-REF.md) — v2.1 (2026-06-13), procédures cold, curl à la
  demande. Table historique en retard sur le CORE (v3.3) — évalué cosmétique, sans risque
  fonctionnel, pas de correctif prévu tant qu'aucun nouvel élément ne le justifie.
- [CLAUDE-DNA-CHAT.md](CLAUDE-DNA-CHAT.md) — v2.2, à coller dans Instructions globales claude.ai.

## Actions Guillaume en attente

- `chatSyncDNAChatOk` — uploader `CLAUDE-DNA-CHAT.md` v2.2 dans Instructions globales claude.ai
  si pas encore fait depuis le bump du 2026-08-07 (le trigger `gprompt` manquait côté Chat avant
  ce bump).
- Décider de la réactivation du trigger `trig_01Y6mLjE6VSXYg8WtmdPA9aB` (Routine `gaudit`) — plus
  d'obstacle technique connu depuis la confirmation MCP ci-dessus.

## Questions ouvertes pour prochaine session

- `INBOX-QUESTIONS.md` a un item en attente depuis 2026-07-21 (correctifs `candidaturePilote`
  Sonnet-vs-Opus + migration profil rédactionnel) — décision Guillaume requise, hors périmètre
  d'exécution autonome de `gaudit`.
- Repo `ClaudeAchatMaison` : alerte 🔴 non résolue dans son `REPRISE.md` (délai légal de
  réflexion offre de prêt Crédit Mutuel vs échéance compromis du 31/07/2026) — signalée par le
  cycle `gaudit` du 2026-08-09, aucune activité constatée sur ce repo depuis. L'échéance
  mentionnée est déjà passée à la date de cette session (2026-08-10) sans mise à jour tracée —
  statut réel inconnu de `claude-os`, à vérifier directement avec Guillaume plutôt que supposé
  résolu.

## Note — entretien de ce fichier

`REPRISE.md` reste **hors périmètre d'entretien automatique de `gaudit`** (c'est un artefact de
mémoire de session interactive, pas un artefact `audit/`). Il a été rafraîchi deux fois de suite
par des cycles `gaudit` (2026-08-07 puis 2026-08-10) simplement parce qu'il était retrouvé figé —
ne pas compter sur `gaudit` pour le maintenir à jour à chaque passage ; une session interactive
normale doit continuer à le faire au fil de l'eau.

## Options de reprise (prochaine session)

- `resA` — relire `audit/STATE.md` et le rapport le plus récent (`audit/claude-os/` une fois ce
  cycle bouclé) pour l'état complet de la routine `gaudit`.
- `resB` — trancher l'item `INBOX-QUESTIONS.md` du 2026-07-21 (candidaturePilote).
- `resC` — vérifier l'état réel du dossier prêt `ClaudeAchatMaison` (échéance 31/07 dépassée,
  aucune mise à jour tracée depuis) directement avec Guillaume.
- `resD` — décider d'activer la Routine `gaudit` pour de bon (`update_trigger enabled:true` sur
  `trig_01Y6mLjE6VSXYg8WtmdPA9aB`), maintenant que la disponibilité MCP est confirmée.
