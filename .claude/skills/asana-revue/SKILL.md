---
name: asana-revue
description: >
  Revue de TOUTES les tâches Asana de Guillaume (workspace PERSO), hors projet « T7 — Prépa vol B1900D »
  qui a ses propres revues. À invoquer quand Guillaume écrit `grevue` n'importe où dans un message, ou dit
  (souvent en dictée vocale) « j'ai revu », « j'ai revu tâche Asana », « fais la revue de mes tâches »,
  « fais-moi un planning pour 1h30 ». Revue en delta depuis la précédente (ancre et carnet de préférences
  dans le repo `general`, dossier `perso/revue-asana/`), preuves à bas coût (commentaires `[Claude]`, Gmail,
  Drive, Agenda, PR mergées), tri en tâches à cocher / doutes de priorité / questions sans réponse, puis
  planning à DEUX voies chiffrées (ses mains, groupées par canal / mon travail autonome). Brouillons Gmail
  seulement ; je ne coche jamais une tâche ; le carnet de préférences s'enrichit à chaque revue.
---

# asana-revue — revue des tâches Asana et planning à deux voies

Application opérationnelle, sur toute la vie de Guillaume (sauf `T7`), de la doctrine
`CLAUDE-DNA-ASANA.md` (« nous 3 » : Guillaume décide, Claude est le moteur, Asana est la
couche opérationnelle). Version v0.1 (2026-10-28), mode **à la demande uniquement**.

> **Doctrine de référence** : `CLAUDE-DNA-ASANA.md`. En cas de divergence, **la doctrine prime**.
> **Posture (DNA)** : vérifier l'état réel avant d'agir, être frugal, rien de destructif.

## Quand m'activer

- `grevue` n'importe où ; dictée « j'ai revu » / « j'ai revu tâche Asana » (variantes vocales de `grevue`).
  « j'ai revu » sans contexte tâches/planning/Asana : le demander en une phrase, ne pas deviner.
- « fais la revue de mes tâches », « fais-moi un planning pour 1h30 », « que fais-je aujourd'hui ? ».
- PAS pour traiter une tâche en profondeur (`asana-pass` ou travail direct) ni pour `T7`.

## Périmètre et garde-fous (non négociables)

- **Périmètre** : toutes les tâches de « Mes tâches » sauf le projet `T7` (gid `1219338040117369`) :
  filtrer par `memberships.project.gid`, ne jamais lister, modifier ni planifier une tâche `T7`.
- **Gmail** : brouillons uniquement ; jamais d'envoi sans un « envoie » explicite dans le message en cours.
- **Asana** : commentaires en texte brut (`text`, pas `html_text`) préfixés `[Claude] ` ; replanifier
  une date est permis (je le dis) ; **je ne coche ni ne supprime jamais** (je propose, il valide) ;
  je ne renomme que pour refléter une décision validée ; créer une tâche = capture légère (CORE).
- **Secrets** : ne jamais recopier mot de passe, IBAN complet ni identifiant sensible ; si un document
  Drive en contient en clair, le signaler une fois et proposer un gestionnaire de mots de passe.
- **Questions** : texte brut (jamais `AskUserQuestion`), en **un seul lot**. Chaque question = énoncé
  complet en français + réponses proposées numérotées + ma recommandation. Un code court (`revXxx`) peut
  suivre pour la trace, jamais seul : Guillaume lit sans ses tâches sous les yeux, les codes ne lui disent rien.
- **Sans réponse** = ma recommandation s'applique, SAUF cocher / envoyer / supprimer / payer (ça attend).
  Ce qu'il a refusé reste refusé : le noter dans PREFERENCES, ne pas le re-proposer.
- **Durées** : les durées réelles du carnet priment sur mes estimations. **Budget net = temps annoncé −
  durée de la revue elle-même − 10 % de marge.** Si la revue seule dépasse la moitié du temps annoncé, le
  dire d'entrée et proposer : revue allégée (échéances ≤ 3 jours), revue complète sans planning, ou
  planning direct sur la liste du jour.

## Fichiers d'état — repo `general`, `perso/revue-asana/`

Écrits pour qu'une autre IA puisse reprendre (cf. `CLAUDE.md` de `general` : pas de dépendance à Claude Code).

| Fichier | Rôle | Nature |
|---|---|---|
| `INDEX.md` | Explique le dispositif à n'importe quelle IA ; journal des revues (date, durée réelle, tâches vues, coches proposées, enseignements) | durable |
| `PREFERENCES.md` | Carnet : formes d'échange, garde-fous, aime / n'aime pas, contraintes pratiques (erreurs de dictée), tableau des durées (estimation Claude / réel) | durable, grandit à chaque revue |
| `ETAT.md` | Cache dérivé : ancre (horodatage UTC de fin de la dernière revue), décisions fermes, questions en suspens (texte complet), replanifications, coches attendues | jetable : absent ⇒ revue complète |

Lecture : clone local `/home/user/general` s'il existe, sinon `mcp__github__get_file_contents` (`pignol-g/general`).
Écriture : commit + PR + merge automatique (règle `mergeAuto`) depuis la branche de la session.
**Cache volontairement minimal** : lister titres + échéances et filtrer par script est bon marché ; ce qui a coûté
≈ 231 k tokens à la première revue, c'est la lecture des notes. `ETAT.md` ne garde donc jamais une copie de la liste.

## Outils à charger (ToolSearch)

`select:mcp__Asana__get_tasks,mcp__Asana__get_task,mcp__Asana__get_task_stories,mcp__Asana__add_comment,mcp__Asana__update_tasks,mcp__Asana__create_tasks,mcp__Gmail__search_threads,mcp__Gmail__create_draft,mcp__Gmail__update_draft,mcp__Google_Drive__list_recent_files,mcp__Google_Drive__search_files,mcp__Google_Calendar__list_events,mcp__github__get_file_contents,mcp__github__create_pull_request,mcp__github__merge_pull_request,mcp__claude-code-remote__subscribe_pr_activity`
Après une reconnexion MCP, recharger les schémas avant de réutiliser un outil.

## Procédure

0. **Cadrage** (1 phrase) : heure `TZ=Europe/Paris date` et `date -u` (jamais l'heure supposée : la session peut
   dormir des heures), temps annoncé, budget net.
1. **Lire** `PREFERENCES.md` et `ETAT.md`. Absent ⇒ revue complète. Annoncer l'état en 1 phrase
   (« revue du … , ancre …, N décisions fermes, M questions en suspens »). Commencer par demander à
   Guillaume les durées réelles des tâches faites depuis la dernière revue.
2. **Instantané, titres seulement** (aucune note lue à ce stade) :
   - *Delta* : `get_tasks(assignee="me", modified_since=<ancre>, completed_since="2099-01-01T00:00:00Z",
     limit=100, opt_fields="name,due_on,modified_at,completed,assignee_section.name,memberships.project.gid,memberships.project.name")`
     = tâches ouvertes modifiées depuis l'ancre. Avec `completed_since=<ancre>` : aussi celles cochées
     depuis (ce qu'il a fait seul). Pagination `offset=<next_page.offset>`.
   - *Fenêtre d'échéances* : même appel sans `modified_since`, filtré par script (`python3 -I`) : retard,
     `due_on` ≤ aujourd'hui + 7 j, section « aujourd'hui » ; exclure `T7` par gid. 100 titres lus en ligne
     ≈ 12 k tokens : si l'outil renvoie un fichier, le traiter par script, ne pas le relire en entier.
3. **Preuves à bas coût**, avant toute lecture de note : commentaires `[Claude]` récents
   (`get_task_stories(task_ids ≤ 50, resource_subtype="comment_added", created_after=<ancre>, sort_ascending=false)`),
   Gmail envoyés/reçus depuis l'ancre (`search_threads`, requêtes ciblées par sujet de tâche), Drive récent,
   Agenda (7 j passés + 7 à venir), titres des PR mergées (`claude-os`, `general`, `ClaudeAchatMaison`).
   Chercher aussi hors Asana ce qu'il pourrait oublier (ex. mails d'un changement d'adresse).
4. **Tri en six cases**, une ligne par tâche : (a) **à cocher**, preuve citée, il valide ; (b) à faire
   aujourd'hui ; (c) doutes de priorité ; (d) questions restées sans réponse (reprendre l'énoncé complet de
   `ETAT.md`) ; (e) en attente d'un tiers : relance **datée** avec le motif (modèle Evotion : ni appel ni mail
   maintenant, petit mail à date fixe si rien) ; (f) plus tard : replanifier en disant ce qui change.
5. **Un lot de questions** (garde-fous). Attendre ; rien d'exécuté avant sa réponse hors lecture.
6. **Planning à deux voies**, durées de `PREFERENCES.md` :
   - *Voie Guillaume (ses mains)*, groupée par canal : appels (heures d'ouverture, jour limite), mails à relire
     ou envoyer, en ligne, à la maison, déplacements ; ordre = fenêtre d'ouverture puis priorité.
   - *Voie Claude (autonome)* : brouillons, fiches, recherches, MAJ de fichiers, commentaires ; tourne pendant
     qu'il fait la sienne.
   - Chiffrer : « total X min / budget net Y min », et ce qui saute si ça déborde.
7. **Exécuter ma voie** (garde-fous). Chaque commentaire Asana : `[Claude] ` + décision + source, texte brut.
8. **Clôture** : (i) delta de contrôle depuis le début de la revue : toute modification qui n'est pas dans ma
   liste d'écritures est un changement de Guillaume à intégrer ; (ii) mettre à jour `ETAT.md` (ancre = `date -u`
   pris **après** toutes les écritures Asana, décisions, questions en suspens, replanifications, coches attendues),
   `INDEX.md` (une ligne de journal avec la durée réelle de la revue), `PREFERENCES.md` (durées réelles, goûts,
   refus) ; (iii) commit + push + PR + `subscribe_pr_activity` + merge automatique.

## Format de sortie

Court, dense, tutoiement, sans emoji : (1) État en 3 lignes ; (2) à cocher, avec preuve ; (3) planning deux voies
(tableaux, durées, total / budget net) ; (4) questions pour toi, texte complet ; (5) ce que j'ai fait (gids
commentés, dates replanifiées, brouillons Gmail).

## Pièges connus

- `search_tasks` est réservé aux comptes premium (`payment_required`) : utiliser `get_tasks`, `get_my_tasks`, `search_objects`.
- `completed_since` exige un datetime ISO (« now » est rejeté) ; une date lointaine = tâches non terminées seulement.
- Commentaires et changements d'échéance font bouger `modified_at` : poser l'ancre **après** mes écritures,
  sinon le delta suivant me renvoie mes propres modifications. Une écriture faite **après** l'ancre est
  listée dans `ETAT.md` (§ « Écritures postérieures à l'ancre ») pour être ignorée au prochain delta.
- Cocher une tâche **récurrente** (`recurrence` non nul dans `get_task`) crée aussitôt l'occurrence suivante
  (cas « Badge garage », 2026-10-28) : lire `recurrence` avant de proposer une coche ; pour arrêter la série,
  supprimer la dernière occurrence avec l'accord de Guillaume, ne pas la recocher.
- Mes commentaires apparaissent sous le nom « Guillaume » : seul `[Claude] ` les distingue ; ils ne sont pas
  éditables, une erreur se corrige par un commentaire rectificatif (relire avant de poster).
- Gmail : résultats en ligne seulement, pièces jointes illisibles ; corriger un brouillon avec `update_draft`
  plutôt qu'en créer un second.
- GitHub : une PR mergée peut s'afficher `merged:false` dans les listes ; se fier à `merged_at`.
- Dictée vocale : « Zana » = Asana, orthographes d'adresse instables : confirmer noms propres et adresses
  avant de les écrire quelque part.
- Sessions longues : les workers redémarrent ; persister dans `ETAT.md` au fil de l'eau, pas seulement à la fin.

## Évolution (backlog)

- v0.2 : mode quotidien court (≈ 5 min : aujourd'hui, retards, coches probables), puis hebdomadaire
  (lundi, cf. `CLAUDE-DNA-ASANA.md` §5), après 3 revues manuelles. Passer en Routine = décision de Guillaume
  (garde-quota `gquota` alors).
- Mesurer la durée d'une revue avec cache (cible 15-25 min) et l'inscrire dans `PREFERENCES.md`.
- Ménage de l'inbox Asana (~200 tâches non triées) : à proposer à part, pas dans une revue.
- Règles de goût contradictoires : la plus récente prime, datée dans `PREFERENCES.md`.
