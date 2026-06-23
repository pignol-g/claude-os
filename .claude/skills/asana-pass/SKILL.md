---
name: asana-pass
description: >
  Passe de traitement automatique des tâches Asana du projet « Claude » de Guillaume
  (workspace PERSO). À invoquer quand Guillaume tape /asana-pass ou écrit « passe Asana »,
  « traite les tâches Asana », « fais une passe sur le projet Claude », ou en exécution
  planifiée (routine Claude web). Pour chaque tâche : répond aux questions en commentaire,
  réalise les actions faisables seul (RSS/URL, recherche, rédaction, analyse) et met la
  sortie en commentaire, puis range la tâche traitée dans la section « à lire / valider ».
  Ne complète jamais une tâche à la place de Guillaume.
---

# asana-pass — traitement automatique des tâches Asana (projet « Claude »)

Objectif : Guillaume dépose ses questions et tâches dans le projet Asana « Claude »
(souvent sans contexte, sans réso). Cette skill fait une **passe** : elle répond, agit
quand c'est possible, met la sortie **en commentaire à côté de la question** (rien ne se
perd), et **range** la tâche dans une section que Guillaume relit ensuite.

> **Posture (DNA)** : vérifier l'état réel avant d'agir (lire chaque tâche + ses
> commentaires, ne pas supposer). Sous-découper. Être frugal en commentaires. Ne jamais
> deviner quand il manque de la matière — demander précisément. Rien de destructif.

## Contexte fixe (workspace PERSO)

- **Projet « Claude »** : GID `1208173596025068`
- **Section « à lire / valider »** : GID `1208173596025094`
- Langue : **français**, style direct et concis de Guillaume.

> Si un GID ne répond plus (projet/section renommé ou recréé), le re-résoudre :
> `search_objects` (project) pour le projet, `get_project include_sections=true` pour
> retrouver la section « à lire / valider » (la créer à la main est impossible via l'API ;
> demander à Guillaume de la créer si elle a disparu).

## Quand m'activer

- `/asana-pass`, « passe Asana », « traite les tâches Asana », « passe sur le projet Claude »
- Exécution planifiée d'une routine Claude web

## Outils à charger (ToolSearch)

`mcp__Asana__get_tasks`, `get_task`, `add_comment`, `update_tasks`, `get_project`,
`search_objects`. Selon les actions : `WebFetch` (flux RSS / URL), `WebSearch`.

## Procédure

1. **Lister** les tâches incomplètes du projet `1208173596025068`
   (`get_tasks`, `opt_fields: name,completed,notes,assignee.name,memberships.section.name`).
2. **Filtrer** : ignorer les tâches déjà dans la section « à lire / valider »
   (`1208173596025094`), **sauf** si Guillaume y a ajouté un nouveau commentaire/contenu
   depuis le dernier passage (à traiter alors comme une relance).
3. Pour chaque tâche restante, la **lire en entier** (`get_task`, commentaires inclus) et
   la classer :
   - **(a) Question** (factuelle, méthode, conseil) → répondre **complètement** en
     commentaire.
   - **(b) Action réalisable seul** (résumer un flux RSS / une URL, rechercher, rédiger,
     analyser un fichier du repo) → **faire l'action**, puis poster le résultat en
     commentaire.
   - **(c) Besoin de matière / ambigu / hors périmètre** (pointe vers une session externe,
     fichier manquant, périmètre flou) → poster un commentaire **court** disant
     précisément ce qu'il faut de Guillaume, ou poser la question. **Ne pas deviner.**
4. **Routage** selon le sujet :
   - Immo (DVF, négo, vices, commune en zone) → logique repo `ClaudeAchatMaison`
     (skill `audit-immo-fr`).
   - Candidature pilote (offres, LM, CV, relance) → repo `candidaturePilote` ; si
     rédaction au nom de Guillaume, charger `profil-redactionnel-guillaume.md` +
     `structure-lm-pilote.md`. **Ne pas croiser AF/HOP** avec ce projet plan B.
   - Méta CC / DNA / claude-os → `INBOX-QUESTIONS.md` global.
5. **Commentaires** : `add_comment` en `html_text` (listes `<ul>/<li>`, `<strong>`,
   `<em>`). **Un seul commentaire de synthèse par tâche**, pas de bavardage.
6. **Ranger** : toute tâche ayant reçu un commentaire utile (cas a, b, ou c) est déplacée
   dans la section « à lire / valider » via
   `update_tasks add_projects:[{project_id:1208173596025068, section_id:1208173596025094}]`.
7. **Récap chat** final : tâches traitées + nature (réponse / action / besoin de matière),
   tâches laissées intactes et pourquoi, questions en attente de décision de Guillaume.

## Garde-fous

- **Ne jamais** marquer une tâche `completed` — c'est Guillaume qui valide après lecture.
- **Ne jamais** supprimer une tâche, ni envoyer quoi que ce soit en externe (mail,
  candidature) sans accord explicite.
- **Contrainte LYS** (base Lyon Saint-Exupéry) = forte sur les candidatures pilote :
  signaler tout conflit base / relocation avant de recommander un envoi.
- En cas de doute sur l'interprétation d'une tâche → commentaire question, pas d'action
  irréversible.
