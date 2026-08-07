---
name: gaudit
description: >
  Audit de projet autonome de Guillaume, façon R&D : diagnostic + implémentation des
  correctifs/améliorations sur UN projet à la fois (claude-os / general /
  candidaturePilote / ClaudeAchatMaison), pensé pour tourner comme **Routine Claude
  Code Remote** (session neuve à chaque firing, aucune mémoire de conversation entre
  deux cycles) plutôt qu'en session interactive classique. À invoquer quand Guillaume
  écrit `gaudit` n'importe où dans un message, ou dit « audite le projet », « lance
  l'audit », « passe d'audit », ou en exécution planifiée (firing de Routine). Résilient
  à l'interruption (coupure crédits) : tout l'état vit dans `claude-os/audit/`, jamais
  en mémoire. Boucle façon `gauto` (ne s'arrête que sur extinction de crédits ou arrêt
  explicite de Guillaume), avec rotation automatique du repo cible par staleness quand
  aucune consigne n'est donnée. Merge automatique des PR autorisé UNIQUEMENT pour cette
  routine et seulement si CI verte + merge propre sans conflit (carve-out documenté dans
  `CLAUDE-DNA-CC-CORE.md` §Safety interdits) — en cas de conflit, jamais de résolution
  automatique, la PR repart en attente de validation manuelle.
---

# gaudit — audit de projet autonome, résilient, multi-session

Boucle pilotée qui audite **un projet à la fois** parmi les 4 repos de Guillaume :
diagnostic (bugs, dette, points d'amélioration) **et** pistes R&D (nouvelles
fonctionnalités pour « mieux performer »), puis **implémente** les correctifs/
améliorations retenus — pas seulement un rapport, du vrai travail commité.

> **Différence structurante avec les autres skills `g*`** : celles-ci tournent en
> session interactive, avec Guillaume qui tape le trigger. `gaudit` est conçue pour
> tourner **aussi** (surtout) comme **Routine Claude Code Remote** — un firing = une
> session entièrement neuve, sans aucun souvenir du firing précédent. Toute la
> mémoire du système doit donc être **écrite sur disque et commitée**, jamais
> supposée en contexte de conversation. C'est le rôle de `claude-os/audit/`.

## Quand m'activer

- Guillaume écrit `gaudit` (n'importe où dans le message), ou `/gaudit`.
- Formulations équivalentes : « audite le projet », « lance l'audit », « passe d'audit »,
  « fais une passe d'amélioration sur [repo] ».
- Firing de la Routine Claude Code Remote dédiée (prompt minimal, voir §Routine).

## Outils à charger (ToolSearch)

`mcp__Asana__get_task`, `get_task_stories`, `add_comment` (tâche consignes) ;
`mcp__github__create_branch`, `create_pull_request`, `merge_pull_request`,
`get_check_run`/`actions_get` (statut CI), `pull_request_read` (détection conflit) ;
`Read`/`Write`/`Edit`/`Bash`/`Grep`/`Glob` pour le travail de fond sur chaque repo.

## Boucle pilotée (ne JAMAIS s'arrêter spontanément)

### 0. Lire l'état — `claude-os/audit/STATE.md`

**Premier geste, sans exception**, avant toute autre décision. Ce fichier dit tout :
repo cible courant, statut, dernier heartbeat, fichier de plan actif, table de rotation.

### 1. Garde anti-collision

Si `statut = in_progress` **et** `dernier_heartbeat` a moins de ~4h30 : un autre cycle
est probablement encore en cours (session précédente pas encore terminée, ou firing qui
se chevauche). **S'arrêter immédiatement**, ne rien lire/écrire d'autre. Coût quasi nul —
c'est précisément ce qui rend un cron horaire sûr sans avoir besoin de connaître le quota
de crédits restant.

Sinon (statut `idle`/`terminé`, ou `in_progress` mais heartbeat ancien = cycle abandonné) :
continuer.

### 2. Lire la tâche Asana consignes

Tâche permanente, gid `1217287685113494`, projet « Claude » (`1208173596025068`),
section **« Section sans nom »** (`1208173596025069` — choisie délibérément en dehors
du flux ping-pong de `asana-pass`, qui ne scanne que « pour claude » : cette tâche ne
doit **jamais** être traitée comme une consigne `asana-pass`, ni déplacée, ni complétée).

Lire la description + le dernier commentaire. Si Guillaume y a indiqué un repo cible ou
des points d'attention, en tenir compte pour l'étape suivante. Poster un commentaire
signé `[Claude] ` accusant réception (texte brut, pas de `html_text`, cf. convention
`asana-pass`), **sans déplacer la tâche**.

### 3. Reprendre ou démarrer

- **Si un plan est `in_progress`** (fichier `audit/<repo>/PLAN-<date>.md` avec des cases
  non cochées) : **reprendre ce plan**, ne pas repartir de zéro. D'abord vérifier le
  **delta** depuis le dernier heartbeat sur ce repo (`git log` depuis la date du dernier
  heartbeat côté repo cible) :
  - Des commits humains ou d'une autre session sont apparus entretemps → relire ce qui a
    changé, **retirer du plan les items déjà couverts**, signaler dans le plan les items
    devenus obsolètes ou en conflit avec ce nouveau travail. Ne jamais exécuter une étape
    du plan sans avoir vérifié qu'elle est toujours pertinente.
  - Rien n'a changé → reprendre la prochaine case non cochée normalement.
- **Si `idle`/`terminé`** : choisir le repo cible —
  1. Consigne Asana explicite (étape 2) si présente.
  2. Sinon, rotation par staleness : le repo avec `dernier_audit_termine` le plus ancien
     dans la table de `STATE.md` (`jamais` = priorité maximale).
  Puis **diagnostiquer** ce repo : lire son `CLAUDE.md`, son historique récent, sa
  structure, chercher bugs/dette/incohérences ET pistes d'amélioration/R&D pour mieux
  servir son objectif propre (pas un audit générique — se caler sur ce que CE projet
  cherche à accomplir). Écrire `audit/<repo>/PLAN-<date>.md` : items découpés Tier 1
  (correctifs sûrs et à fort impact) / Tier 2 (améliorations) / Tier 3 (R&D, plus
  spéculatif), en étapes atomiques cochables.
  Mettre à jour `STATE.md` : `repo_cible_courant`, `statut = in_progress`,
  `fichier_plan_actif`, `dernier_heartbeat = maintenant`.

### 4. Exécuter

Étape par étape, dans l'ordre du plan :
- Travail sur une **branche dédiée** du repo cible (jamais direct sur la branche par
  défaut) — nommer la branche `gaudit/<date>-<slug-item>`.
- **1 commit + push par étape significative** (pas de batch tardif — résilience = comme
  si la session pouvait s'arrêter à tout instant sans prévenir).
- Après chaque commit : mettre à jour `audit/<repo>/PLAN-<date>.md` (cocher l'item) et
  `claude-os/audit/STATE.md` (`dernier_heartbeat = maintenant`), committer/pousser côté
  `claude-os` aussi. Ces deux commits (repo cible + `claude-os`) sont **indépendants**,
  pas besoin d'atomicité entre les deux repos.
- Respecter integralement les **safety interdits** du DNA-CORE (force-push interdit,
  pas de `--no-verify`, pas de modif hooks/settings, pas de `branch -D`/delete remote)
  — le seul carve-out existant concerne le merge de PR (étape 5), rien d'autre.

### 5. Fin de plan — PR et merge conditionnel

Quand toutes les étapes du plan sont cochées :
1. Ouvrir une **pull request** (pas draft cette fois — elle doit pouvoir être mergée
   automatiquement si les conditions sont réunies) depuis la branche `gaudit/...` vers
   la branche par défaut du repo cible. Description = résumé des items traités.
2. Attendre/consulter le statut CI (`get_check_run` / `actions_get`). Si le repo n'a pas
   de CI configurée, considérer la condition CI comme satisfaite par défaut (rien à
   attendre).
3. Vérifier la mergeabilité (`pull_request_read` — `mergeable_state`/`mergeable`).
   - **CI verte ET merge propre (pas de conflit)** → `merge_pull_request` directement.
     C'est le **seul** cas où `gaudit` merge sans validation de Guillaume (carve-out
     `CLAUDE-DNA-CC-CORE.md` §Safety interdits, décision 2026-08-07).
   - **CI rouge, ou conflit, ou CI en attente trop longtemps** → **ne pas merger**. La
     PR reste ouverte en attente de validation manuelle, comme pour toute autre skill.
     Ne jamais tenter de résoudre un conflit automatiquement — trop risqué sur des
     fichiers de données/état (ex. JSON sources de vérité).
4. Écrire `audit/<repo>/REPORT-<date>.md` (voir format ci-dessous) — **uniquement à ce
   stade, jamais sur interruption**.
5. Mettre à jour `STATE.md` : `statut = terminé`, ajouter une ligne dans la table de
   rotation (`dernier_audit_termine = date du jour` pour ce repo) et dans l'historique
   des cycles. Committer/pousser `claude-os`.
6. Poster le lien du rapport (et de la PR, mergée ou non) en commentaire signé sur la
   tâche Asana consignes.

### 6. Reboucler

S'il reste du budget après un plan terminé : reboucler en (2)/(3) sur le **prochain**
repo (rotation par staleness, sauf nouvelle consigne Asana entretemps) — façon `gauto`,
ne jamais s'arrêter spontanément après un seul plan.

### 7. Arrêt

Trois conditions seulement :
- (a) Extinction des crédits — rien de spécial à faire, le firing suivant échouera ou ne
  produira rien ; l'état déjà commité n'est jamais perdu.
- (b) Guillaume écrit `gstop`, ou désactive/supprime la Routine.
- (c) Bouton stop pressé.

Dans les cas (b)/(c) en cours d'exécution : dernier geste = `STATE.md` à jour (heartbeat
+ progression réelle) + commit/push, même si le plan n'est pas terminé. **Pas** de
`REPORT` dans ce cas (rapport = plan terminé uniquement, cf. décision Guillaume).

## Routine Claude Code Remote

Créée via `create_trigger`, cron horaire, `create_new_session_on_fire: true`, **désactivée
par défaut**. Prompt minimal et stable :

> Exécute un cycle `gaudit` (voir `claude-os/.claude/skills/gaudit/SKILL.md`) : lis
> `claude-os/audit/STATE.md`, décide s'il faut démarrer, reprendre ou t'arrêter
> immédiatement, agis en conséquence.

Activation/arrêt = décision de Guillaume (`fire_trigger` pour tester, `update_trigger
enabled:true` pour armer, `enabled:false` ou `delete_trigger` pour arrêter). Le cron
horaire + la garde anti-collision (§1) permettent de laisser tourner la routine sans
avoir à calculer une fenêtre précise avant le renouvellement hebdomadaire des crédits :
chaque réveil coûte quasi rien s'il n'y a rien à faire.

## Format du rapport standardisé — `audit/<repo>/REPORT-<date>.md`

```markdown
# Rapport gaudit — <repo> — <date>

## Période couverte
<date début du plan> → <date fin>

## Items traités
| Item | Diagnostic | Action | Résultat |
|---|---|---|---|
| ... | ... | ... | ... |

## Pull request
<lien PR> — <mergée automatiquement / en attente de validation manuelle (raison)>

## Items reportés au prochain cycle
- <item> — <pourquoi reporté>

## Risques / dette identifiés non traités
- <item> — <pourquoi pas traité ce cycle>

## Prochaine cible de rotation prévue
<repo suivant selon staleness, sauf nouvelle consigne Asana>
```

## Safety interdits

Rappelés dans `CLAUDE-DNA-CC-CORE.md` (garde-fous non déportables) — **tous s'appliquent
sans exception à `gaudit`**, à une seule exception documentée :

- Pas de force-push (jamais).
- Pas de `git branch -D` ni delete de branche remote.
- Pas de `--no-verify` ni skip de hooks.
- Pas de modif `.claude/settings.json` ni des hooks `.claude/hooks/`.
- **Merge de PR** : carve-out scopé à cette seule routine — merge automatique autorisé
  uniquement si CI verte + merge propre sans conflit (§5). Toute PR en conflit ou CI
  rouge reste en attente de validation humaine, sans exception, sans tentative de
  résolution automatique de conflit.

Toute violation de ce qui précède = arrêt immédiat du cycle + alerte Guillaume (commentaire
signé sur la tâche Asana consignes expliquant ce qui a été bloqué et pourquoi).
