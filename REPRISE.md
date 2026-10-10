# REPRISE — claude-os

**Dernière session : 2026-10-10** (routine pilote mise en service : `gpilote` + `gquota`, voir ci-dessous)

## Routine pilote — en service depuis le 2026-10-10

Architecture et prompts : `.claude/skills/gpilote/RELANCE.md` ; procédure par passage :
`gpilote/SKILL.md` ; garde-quota : `gquota/` (PR #75-#82). Décisions : `sess5hA`, `fenBurnA`,
`recheckA`, `tauxB`, `quotaKOA`, `fin90A` (gquota) ; `archi2A`, `rotPilote2A`, `relanceurA`,
`cronDimB`, `nuitB`, `anciennesA` (gpilote). `rotPiloteA` abandonnée (profondeur des sessions
limitée à 8, essai du 2026-10-10).

- **Relanceur** (profondeur 0, créé par Guillaume) : `session_019Gz7iuojn5xBhHTnMbT3Jx`,
  Routine « Pilote · relance hebdo » `trig_01UiLheDTB2Rg67VJjYN9abj` (samedi 09h56 Paris) :
  crée chaque samedi le pilote de la semaine.
- **Pilote de la semaine** : `session_013PpYzKzTmZwFst3mH8zzuy` (« Pilote quota · semaine du
  2026-10-10 »), prise de poste faite (essai à blanc partiel : STOP samedi, choix non exercé).
  Routines : « Pilote · réveil nuit » `trig_01YTkY5SX4ZNtAvxiPVwzCCg` (1h47, 3h47, 5h47 Paris,
  dim-ven), « Pilote · réveil vendredi » `trig_01D178ZKxaU5XKLi2kcjoe3n` (18h31 UTC, 30 min
  avant le reset), « Pilote · réveil mesure vendredi » `trig_01H9SdxLRAFj75HxT2VuUPjE`
  (18h58 UTC, relevé sans lancement). Ces ids changent chaque samedi (nouveau pilote).
- **Tâches** : 6 Routines sans horaire = stockage du prompt et du modèle (ids dans
  `gpilote/SKILL.md`), prompts adaptés au lancement par `create_session` le 2026-10-10.
- **Règles** : gquota (seuil = jours révolus × 14,3 − 10 ; vendredi dès 00h00 : 90 % ;
  fenêtre de solde 30 min avant le reset, coupure 1 min avant) ; alternance des tâches (la
  plus anciennement lancée d'abord) ; une tâche du groupe candidaturePilote/claude-os à la
  fois ; une lourde par passage.
- **Indicateurs** pour décider (`RELANCE.md` §Analyse) : journal par passage, mesure du
  vendredi 20h58, bilan de la semaine à chaque prise de poste. Guillaume écrit « bilan
  pilote » pour une analyse.

**À surveiller** : premier passage GO lundi 12/10 1h47 (seuil 18,6 %, hebdo à 15 % samedi
matin → marge probablement < 5 points, une seule tâche) — outils Asana trouvés,
`create_session` des tâches, gquota par sous-agent Haiku (le pilote l'a fait à la main lors
de l'essai) ; première relance réelle samedi 17/10 09h56 (registre et journal repris,
Routines du précédent supprimées, bilan). Point d'analyse avec Guillaume après 1-2 semaines.

## État courant

DNA-CC **v3.5** (2026-10-09), DNA-Chat **v2.2**, DNA-REF **v2.2** (vérifié par
`scripts/verify-dna-consistency.sh` le 2026-10-10). Les 4 repos (`claude-os`, `general`, `candidaturePilote`, `ClaudeAchatMaison`) ont
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

- [CLAUDE-DNA-CC-CORE.md](CLAUDE-DNA-CC-CORE.md) — v3.5, injecté par hook à chaque session CC.
- [CLAUDE-DNA-CC-REF.md](CLAUDE-DNA-CC-REF.md) — v2.2, procédures cold, curl à la demande ;
  table historique à jour avec le CORE v3.5.
- [CLAUDE-DNA-CHAT.md](CLAUDE-DNA-CHAT.md) — v2.2, à coller dans Instructions globales claude.ai.

## Actions Guillaume en attente

- `chatSyncDNAChatOk` — uploader `CLAUDE-DNA-CHAT.md` v2.2 dans Instructions globales claude.ai
  si pas encore fait depuis le bump du 2026-08-07 (le trigger `gprompt` manquait côté Chat avant
  ce bump).
- Aucune autre : la Routine `gaudit` d'origine (`trig_01Y6mLjE6VSXYg8WtmdPA9aB`) reste désactivée
  pour archive (`anciennesA`) ; `gaudit` est désormais lancé par le pilote.

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
- `resD` — « bilan pilote » : lire les journaux des pilotes (`RELANCE.md` §Analyse) et proposer
  les réglages (alternance, passages de nuit, effet de `fin90A`).
