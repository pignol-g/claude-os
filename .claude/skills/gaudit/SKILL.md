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
Si `claude-os` n'est pas dans le scope de la session (firing de Routine dans un
environnement qui ne l'a pas), l'ajouter d'abord via `add_repo` — idem pour le repo
cible dès qu'il est connu (étape 3).

### 1. Garde anti-collision

Si `statut = in_progress` **et** `dernier_heartbeat` a moins de ~4h30 : un autre cycle
est probablement encore en cours (session précédente pas encore terminée, ou firing qui
se chevauche). **S'arrêter immédiatement**, ne rien lire/écrire d'autre. Coût quasi nul —
c'est précisément ce qui rend un cron horaire sûr sans avoir besoin de connaître le quota
de crédits restant.

Sinon (statut `idle`/`terminé`, ou `in_progress` mais heartbeat ancien = cycle abandonné) :
continuer.

### 2. Lire la tâche Asana consignes

> **Dégradation gracieuse** : si les outils `mcp__Asana__*` ne sont pas chargeables dans
> cette session (Routine firée sans connecteur Asana attaché — cas connu, voir §Routine),
> **ne pas bloquer le cycle**. Sauter cette étape, le noter dans `STATE.md`
> (`consignes_asana: indisponible ce cycle`), et passer directement à la rotation par
> staleness (étape 3). Le cycle reste utile même sans lire les consignes amont.

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

  Si le repo cible est **`claude-os`**, lancer `bash scripts/verify-dna-consistency.sh`
  en tout début de diagnostic — automatise plusieurs checks de cohérence interne
  (versions CORE/REF/CHAT, bookkeeping `to-chat/`, liens cassés, skills non référencées)
  qu'un cycle refaisait manuellement à chaque passage et qui ont laissé passer 4 cycles
  de suite un vrai décalage (cf. §Historique du script et `audit/claude-os/REPORT-
  2026-08-14-2.md`). Un check qui échoue = candidat Tier 1 direct ; ça libère le temps de
  diagnostic pour la vraie réflexion R&D plutôt que pour re-dériver ces vérifications à
  la main.

  > ⚠️ **La R&D est une étape distincte du bug-hunting, pas un sous-produit.** Constat
  > (2026-08-14) : passé le premier cycle, les diagnostics ont convergé vers "aucun item
  > Tier 1/2/3" cycle après cycle sur les repos stables (claude-os, general) — parce que
  > le diagnostic restait *shaped* comme une chasse au bug (cohérence, liens cassés,
  > versions) qui, sur un repo sain, ne trouve structurellement rien. Chercher des bugs
  > et générer des idées R&D sont deux gestes mentaux différents ; le second ne se
  > produit pas par accident pendant le premier. **Avant de conclure "rien à Tier 2/3",
  > consacrer un temps dédié à se poser explicitement, à partir de l'objectif du projet
  > tel que décrit dans son `CLAUDE.md`** (pas un audit générique) : « qu'est-ce qui,
  > ajouté ou changé, ferait mieux réussir ce que ce projet essaie d'accomplir ? » —
  > au moins 2-3 pistes concrètes à évaluer, même si elles sont ensuite reportées en
  > Tier 3 faute d'être exécutables en autonome. Un plan qui conclut "aucun item Tier
  > 2/3" doit le justifier par cette réflexion explicitement menée (et tracée dans le
  > plan), jamais par défaut faute d'avoir cherché. Si le repo cible a une skill dédiée
  > à l'amélioration de son domaine (ex. `audit-veille` pour `candidaturePilote`), s'en
  > inspirer pour la forme sans se substituer à elle.
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
5bis. **Vérifier que le push a réellement atteint `origin`** avant de passer à l'étape 6 —
   ex. `git fetch origin <branche-défaut-claude-os>` puis comparer le SHA du commit qui
   vient d'être poussé à `origin/<branche>` (ou tout mécanisme équivalent). **Ne jamais
   sauter cette vérification** : un `git push` peut échouer silencieusement (réseau,
   session interrompue juste après) sans que les étapes suivantes (merge PR côté GitHub,
   commentaire Asana) s'en aperçoivent puisqu'elles passent par un chemin d'écriture
   indépendant (appels MCP). C'est précisément ce qui s'est produit le 2026-08-09 :
   `STATE.md` est resté 3 jours sur un pointeur obsolète alors que les PR cibles
   (candidaturePilote #166, ClaudeAchatMaison #37) étaient déjà mergées et les
   commentaires Asana de clôture déjà postés — cf. `audit/STATE.md` §Historique
   2026-08-10 pour le détail complet et `audit/candidaturePilote/REPORT-2026-08-09.md` +
   `audit/ClaudeAchatMaison/REPORT-2026-08-09.md` pour la reconstruction qui en a résulté.
   Si le push n'a pas abouti : retenter (mêmes règles que pour tout push git), et ne
   poster le commentaire Asana qu'une fois la vérification passée.
6. Poster le lien du rapport (et de la PR, mergée ou non) en commentaire signé sur la
   tâche Asana consignes. **Jamais avant l'étape 5bis** : le commentaire Asana ne doit
   jamais pouvoir donner l'impression qu'un cycle est clos si la persistance disque
   côté `claude-os` n'a pas réellement abouti côté remote.

### 6. Reboucler

S'il reste du budget après un plan terminé : reboucler en (2)/(3) sur le **prochain**
repo (rotation par staleness, sauf nouvelle consigne Asana entretemps) — façon `gauto`,
ne jamais s'arrêter spontanément après un seul plan.

> ⚠️ **Un tour de rotation complet (les 4 repos ont `dernier_audit_termine` = aujourd'hui)
> n'est PAS une condition d'arrêt.** C'est une illusion de point de contrôle naturel —
> constaté à plusieurs reprises (08-10, 08-13, deux fois le 08-14) : une session fraîche,
> sans mémoire du raisonnement des cycles précédents, referme la boucle après un tour
> complet en écrivant une phrase du type « fin du tour, je m'arrête ici pour cette
> série », alors qu'aucune des 3 conditions du §7 n'est remplie. **Un tour complet =
> repartir immédiatement sur un nouveau tour (repo le plus ancien de la table, donc en
> général le premier repris), sans pause ni narration de clôture.** N'écrire "je
> m'arrête" (ou toute formulation équivalente : "fin de série", "je termine là") **que**
> si l'une des 3 conditions du §7 est explicitement remplie — jamais par déduction du
> nombre de tours bouclés.

### 7. Arrêt

Trois conditions **seulement** — un tour de rotation complet n'en fait **pas** partie
(cf. avertissement §6) :
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

**Limite constatée à la création (2026-08-07), levée depuis** : `create_trigger` avait refusé
le paramètre `connectors` (« not available for this organization »), et la Routine prévenait
que les sessions déclenchées tourneraient sans outils `mcp__<serveur>__*` (d'où la
dégradation gracieuse §2, conservée par prudence). **Constat en conditions réelles depuis** :
sur les firings du 2026-08-09 et du 2026-08-10, `mcp__Asana__*` **et** `mcp__github__*` se sont
révélés disponibles dans la session déclenchée (chargés via `ToolSearch`, avec un court délai
de connexion au tout début de session plutôt qu'une indisponibilité totale) — les deux cycles
ont créé/mergé des PR cible et posté leurs commentaires Asana de clôture sans recourir à la
dégradation gracieuse §2. Le volet PR/merge (§5) fonctionne donc bien en mode Routine, sans
réserve. Le trigger `trig_01Y6mLjE6VSXYg8WtmdPA9aB` a été créé puis désactivé immédiatement à
la création par prudence ; l'obstacle technique qui justifiait cette prudence est levé, mais sa
réactivation reste, comme toute activation/désactivation de la Routine, une décision de
Guillaume (cf. paragraphe ci-dessus) — non déclenchée automatiquement par `gaudit` lui-même.

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
