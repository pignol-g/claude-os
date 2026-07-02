# R&D — Résilience des sessions Claude Code : interruption, reprise, anti-perte

> **Statut : R&D (analyse + scénarios + tests proposés).** La skill générique
> viendra **après** validation de cette analyse (cf. §7 plan par phases).
> **Origine** : PR #13 / tâche Asana « Veille ». Demande de Guillaume : une skill
> **générique claude-os** qui répond à l'interruption & reprise entre sessions
> (surtout **extinction de crédit**), sans perte de travail.
> **Contrainte dure non négociable : surcoût token ~nul.**

---

## 1. Ce qui existe DÉJÀ (ne pas réinventer)

L'inventaire des repos montre qu'une grande partie de la fondation est posée :

- **`REPRISE.md`** (par projet) : snapshot d'état de session, commit-gated, mis à
  jour à chaque clôture / cycle. Reprise = lire l'entrée du haut → « PROCHAINE ACTION ».
- **`RECAP-AUTO/NUIT-YYYY-MM-DD.md`** : récap des sessions longues/autonomes,
  lisible au réveil en 2 min.
- **Mode `gauto`** (DNA-CORE) : boucle autonome qui **commit/push à chaque étape**,
  met à jour REPRISE par cycle, et prévoit un **arrêt gracieux** sur extinction de
  crédit (dernier tour : MAJ REPRISE + RECAP + push).
- **Hooks** : `session-start.sh` (`git pull --rebase` au démarrage),
  `session-end.sh` (**auto-commit WIP best-effort** si la session se ferme sans
  `/close`), `close-session.sh` (commit + rebase + push avec retries).
- **Discipline atomique** : « 1 étape = 1 commit + push, jamais d'état à moitié
  fait non commité ».
- **Proposition `.reprise/<slug>.md`** (v0, cette PR) : plan coché + pointeur étape.

**Conclusion** : le socle « plan = historique de commits, mémoire = fichiers,
reprise = relire où on en était » existe. Ce qui manque = (a) **généraliser** en
une skill claude-os unique, (b) couvrir les **angles morts** révélés ci-dessous
(crédit, subagents, oubli), (c) **valider empiriquement** par des tests.

---

## 2. Que se passe-t-il VRAIMENT ? (réponses factuelles à tes questions)

Recherche sur la doc officielle Claude Code. Réponses honnêtes, y compris les
incertitudes.

### 2.1 « Plus de crédit en plein milieu — est-ce possible ? Que se passe-t-il ? »

**Oui, c'est possible** (limite de session, limite hebdomadaire, ou crédits
prépayés épuisés). Deux régimes très différents :

- **Erreur transitoire** (429 rate-limit, 529 surcharge) → Claude Code **réessaie
  automatiquement** (~10 tentatives, backoff exponentiel). **Récupérable seul**,
  rien à faire.
- **Quota dur** (session/semaine atteinte, crédit épuisé) → la session **se bloque
  net**. Le modèle **n'apprend l'erreur qu'au rejet de la requête suivante** : il
  ne peut **pas** réagir, committer, ni écrire un checkpoint avant de s'arrêter.

➡️ **Ta perception est exacte : « tu t'arrêtes net » — et je n'en ai PAS
conscience à l'avance.** Je ne vois pas la limite arriver.

### 2.2 « Moi, si je reviens sur la session ? Reprendre exactement où ça s'est arrêté ? »

- **La conversation est persistée** (web/app/`--resume`) → tu peux rouvrir la
  session et le fil est là.
- **Mais l'arbre de travail non commité dans le conteneur cloud est éphémère** :
  - si tu reviens **vite** (conteneur encore vif) → WIP intact, on reprend ;
  - si tu reviens **tard** (conteneur **récupéré**) → **seul le commité+pushé
    survit**. Le timeout exact de récupération n'est **pas documenté** (incertitude).
- **Donc** : « reprendre exactement où ça s'est arrêté » = garanti pour la
  *conversation*, **pas** pour le *travail non commité*. D'où le commit fréquent.

### 2.3 « Et si je ne reviens pas (oubli), et que je vis dans Asana ? »

C'est le scénario le plus exigeant. Les filets « de dernière minute » sont **non
fiables** ici :

> ⚠️ **Insight central de cette R&D** : les hooks `SessionEnd`/`Stop` et tout
> « commit du dernier souffle » **ne se déclenchent PAS quand la session est
> bloquée par un quota dur** (la session est gelée, plus rien ne tourne). On ne
> peut donc **pas** compter sur une sauvegarde au moment de la mort.

➡️ **Corollaire de design** : l'état doit être **déjà commité AVANT l'arrêt**
(checkpoint en avance de phase), jamais « sauvé à la fin ». Et pour survivre à
l'oubli, **l'état doit aussi vivre hors de la session** : dans le **git** (REPRISE
+ commits) **et** dans **Asana** (la tâche porte un pointeur vers l'état).

### 2.4 Subagents en vol

- Les subagents **partagent le même budget** d'usage que la session principale.
- Si le crédit s'épuise pendant qu'ils tournent, ils sont **vraisemblablement
  tués** et **leurs résultats non écrits sont perdus** (comportement non
  explicitement documenté — incertitude).
- Un subagent **n'a pas de moyen fiable de committer en parallèle** sur la même
  branche (conflits). → cf. §5 le bon pattern.

---

## 3. Scénarios (les tiens + tests à mener)

| # | Déclencheur | Ce qui survit | Ce qui se perd | Parade |
|---|---|---|---|---|
| S1 | Crédit épuisé, **retour rapide** (conteneur vif) | conversation + WIP | rien | reprendre via la conversation |
| S2 | Crédit épuisé, **retour tardif** (conteneur récupéré) | commité+pushé seulement | WIP non commité | **checkpoint par étape** (commit avant l'arrêt) |
| S3 | Crédit épuisé **pendant subagents** | ce que l'orchestrateur a déjà persisté | résultats subagents non écrits | orchestrateur **persiste/commit dès chaque retour** ; ou worktrees |
| S4 | **Oubli total**, suivi via Asana | git (REPRISE + commits) + Asana | rien si l'état est dans Asana | tâche Asana = **pointeur d'état** (lien REPRISE/PR + étape courante) |
| S5 | Rate-limit **transitoire** | tout | rien | retry auto, ne rien faire |

**Tests empiriques proposés (phase 2, session dédiée)** — car plusieurs
comportements sont non documentés :

1. **Interruption réelle** : appuyer Stop à mi-tâche, rouvrir la session →
   qu'est-ce que la session reprise voit réellement (WIP ? plan ?).
2. **Déclenchement hooks** : le hook `SessionEnd` tourne-t-il sur **Stop** ? Et
   sur **blocage quota** (attendu : non) ? Confirmer empiriquement.
3. **Surcoût token** : mesurer le coût réel d'un cycle checkpoint (écriture `.md`
   + commit) vs le gain à la reprise (ne pas recharger l'historique).
4. **Subagents** : tuer une session pendant un fan-out, vérifier ce qui a été
   persisté selon le pattern « commit à chaque retour ».

---

## 4. Comparaison des approches (mode R&D)

| Approche | Survit crédit ? | Survit perte conteneur ? | Survit oubli ? | Coût token | Verdict |
|---|---|---|---|---|---|
| **A. Commit-as-checkpoint granulaire** (étapes atomiques, commit+coche) | ✅ | ✅ | ✅ (via git) | ~0 (git hors LLM) | **socle** |
| B. Resume natif (`--continue`/`--resume`, conversation) | ⚠️ partiel | ❌ | ❌ | 0 | confort retour rapide |
| C. Hooks (SessionStart restore / SessionEnd save) | ❌ (bloqué = pas de run) | ✅ si déclenché | ⚠️ | ~0 | **filet**, pas socle |
| D. Asana = registre d'état macro | ✅ | ✅ | ✅ | faible | **complément anti-oubli** |
| E. Workflow tool (resume par journal/cache) | intra-session | ❌ frontière session | ❌ | variable | gros fan-out intra-session |

**Recommandation** : **socle = A**, car c'est la **seule** approche qui survit à
*tout* (crédit + conteneur + oubli) **sans dépendre d'un dernier souffle**.
Complétée par : **C** (hooks, filet), **D** (Asana, anti-oubli macro), **E** pour
les gros fan-out, **B** pour le confort de retour rapide.

---

## 5. Design proposé de la skill générique (claude-os)

**Nom proposé** : skill `reprise` (ou `checkpoint`), **globale claude-os** (dispo
dans les 3 projets, cloud + local).

1. **Déclenchement** : tâche longue (> N étapes) ou explicite ; **auto-détection**
   au démarrage d'un `.reprise/*.md` avec `statut: en_cours`.
2. **Fichier d'état** : `.reprise/<slug>.md` **commité** —
   frontmatter (`statut`, dates) + bloc **« Contexte de reprise »** (court, suffit
   à repartir à froid) + **« PROCHAINE ACTION → étape N »** + **plan coché**.
   → distinct de `REPRISE.md` (qui reste le **snapshot de session** ; `.reprise/`
   est le **suivi fin d'exécution** d'un chantier).
3. **Discipline** : **1 étape = 1 commit** (message normalisé
   `checkpoint(<tache>): <étape> [n/N]`), étapes **idempotentes** (« le livrable
   existe déjà ? → skip »).
4. **Subagents** (le point que tu soulevais) : la voie robuste **n'est pas** de
   faire committer N subagents en parallèle (conflits de branche). Deux patterns :
   - **Orchestrateur-persiste** (défaut) : chaque subagent **renvoie son résultat
     structuré tôt** ; l'orchestrateur **commit dès réception** → on ne perd au
     pire qu'un subagent en vol.
   - **Worktree par subagent** (`isolation: worktree`) si les subagents doivent
     vraiment écrire en parallèle sans se marcher dessus.
5. **Lien Asana** : la tâche Asana porte un **pointeur d'état** (lien REPRISE/PR +
   étape courante) → reprise possible **même sans rouvrir la session** (scénario S4).
6. **Reprise** : lire `.reprise/`, prendre la **première case non cochée**,
   vérifier l'idempotence, continuer. Aucun besoin de l'historique de conversation.
7. **Intégration filets existants** : `session-start.sh` signale les `.reprise`
   `en_cours` ; `session-end.sh` (auto-WIP) reste le filet pour les arrêts **non**
   liés au quota.

---

## 6. Économie de token (la contrainte dure)

- Le **checkpointing coûte ~0 token en propre** : git s'exécute **hors LLM**.
- Le seul coût LLM = (a) écrire/mettre à jour un `.md` **squelettique** (quelques
  lignes), (b) relire à la reprise le bloc « Contexte de reprise » (**200-500
  tokens** par design).
- **Net token-POSITIF** : reprendre via un fichier court **évite de recharger un
  long historique de conversation** — c'est l'inverse d'un surcoût.
- **Garde-fous anti-surcoût** : ne **pas** checkpointer des micro-étapes triviales
  (1 checkpoint = 1 vraie unité de travail) ; garder le `.md` squelettique (pas de
  re-résumé verbeux) ; pas de commit pour une ligne.

---

## 7. Plan R&D par phases

- **Phase 1 (cette PR)** : cette analyse + décisions à trancher (§8). *← ici.*
- **Phase 2 (session dédiée)** : **tests empiriques** (§3) — lever les incertitudes
  (timeout conteneur, hooks sous quota, surcoût mesuré).
- **Phase 3** : **build** de la skill générique claude-os + intégration hooks +
  convention Asana.
- **Phase 4** : **rollout** dans les 3 projets + capitalisation dans DNA-CORE.

---

## 8. Décisions à trancher (Guillaume)

1. **Valides-tu le socle A** (commit-as-checkpoint) + compléments C/D, plutôt qu'un
   pari sur les hooks de dernière minute (qui ne survivent pas au blocage quota) ?
2. **Emplacement de l'état** : `.reprise/<slug>.md` pour l'exécution fine **et**
   `REPRISE.md` pour le snapshot de session (recommandé) — ou tout dans REPRISE.md ?
3. **Pattern subagents** : « orchestrateur-commit-à-chaque-retour » par défaut,
   worktrees seulement si écriture parallèle réelle — OK ?
4. **Veux-tu la phase 2 (tests empiriques) avant le build**, ou on construit
   directement la skill sur cette analyse ?

---

## 9. Incertitudes assumées (à confirmer en phase 2)

- Timeout exact de récupération du conteneur cloud : **non documenté**.
- Déclenchement des hooks `SessionEnd`/`Stop` **sous blocage quota** : attendu
  **non**, à confirmer.
- Sort précis des subagents en vol à l'extinction de crédit : **non documenté**.
