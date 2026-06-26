---
name: asana-pass
description: >
  Passe de traitement collaboratif des tâches Asana du projet « Claude » de Guillaume
  (workspace PERSO), application opérationnelle de la doctrine CLAUDE-DNA-ASANA.md
  (système « nous 3 »). À invoquer quand Guillaume tape /asana-pass ou écrit « passe Asana »,
  « traite les tâches Asana », « fais une passe sur le projet Claude », ou en exécution
  planifiée (routine Claude web). Modèle « collaborateur » en ping-pong : Guillaume dépose
  ou renvoie une tâche dans la file d'entrée ; Claude répond / agit en commentaire signé
  « [Claude] », puis renvoie la tâche dans « à lire / valider ». Claude ne complète jamais
  une tâche — c'est Guillaume qui valide (ou relance).
---

# asana-pass — collaboration sur les tâches Asana (projet « Claude »)

Application concrète, sur le **projet « Claude »** (l'atelier des livrables, cf.
`CLAUDE-DNA-ASANA.md` §6), de la doctrine « nous 3 » (Guillaume = décideur, Claude =
moteur, Asana = couche opérationnelle). Claude est traité comme un **collaborateur** :
le travail se fait en **ping-pong** sur deux voies, et la conversation vit dans les
**commentaires**, à côté de la tâche.

> **Doctrine de référence** : `CLAUDE-DNA-ASANA.md` (raw GitHub claude-os). En cas de
> divergence, **la doctrine prime** sur cette skill.

> **Posture (DNA)** : vérifier l'état réel avant d'agir (lire chaque tâche + TOUS ses
> commentaires, ne pas supposer). Sous-découper. Être frugal. Ne jamais deviner quand il
> manque de la matière — demander précisément. Rien de destructif.

## Modèle collaboratif (les voies)

| Section | GID | Sens |
|---|---|---|
| « pour claude » | `1208173596025107` | **Balle côté Claude** — ma file d'entrée, à traiter |
| « a travailler Guillaume » | `1208173596025108` | **Balle côté Guillaume** — SA file à lui, NE PAS traiter |
| « à lire / valider » | `1208173596025094` | **Balle côté Guillaume** — il lit / décide / relance ce que j'ai traité |

> Note : « Section sans nom » (`1208173596025069`) est l'ancienne section par défaut (legacy),
> et le projet porte aussi un pipeline candidatures (« à postuler », « postulé »…). Ma file de
> travail est **uniquement « pour claude »**.

### Cycle de vie d'une tâche
1. **Guillaume** crée une tâche (ou la renvoie) dans la **file d'entrée**.
2. **Claude** la traite → commentaire **signé** → la déplace dans **« à lire / valider »**.
3. **Guillaume** lit. Puis :
   - **satisfait** → il **complète** la tâche (= clôture de l'Action, geste humain) ;
   - **veut une suite** → il **ajoute un commentaire** (sa relance) et **la renvoie dans la
     file d'entrée** → retour à l'étape 2, Claude traite la NOUVELLE consigne.

> C'est la boucle d'un collaborateur humain : on se répond dans les commentaires, et la
> position de la tâche (quelle lane) dit à qui de jouer.

## Règle de signature (CRITIQUE)

L'intégration Asana s'authentifie avec le compte de Guillaume : **mes commentaires sont
attribués à « Guillaume »**. Pour que la boucle fonctionne, je dois pouvoir distinguer nos
voix :

- **Tout commentaire que je poste commence par `[Claude] `** (signature **textuelle** —
  pas d'emoji, cf. doctrine §7).
- Donc, en lisant une tâche : **un commentaire NON préfixé `[Claude]` = une consigne de
  Guillaume** (nouvelle question ou relance) à traiter.

## Quand m'activer

- `/asana-pass`, « passe Asana », « traite les tâches Asana », « passe sur le projet Claude »
- Exécution planifiée d'une routine Claude web

## Outils à charger (ToolSearch)

`mcp__Asana__get_tasks`, `get_task`, `add_comment`, `update_tasks`, `get_project`,
`search_objects`. Selon les actions : `WebFetch` (flux RSS / URL), `WebSearch`.

## Procédure

1. **Lister** les tâches incomplètes du projet `1208173596025068`
   (`get_tasks`, `opt_fields: name,completed,notes,assignee.name,memberships.section.name`).
2. **Sélectionner ma file d'entrée** : les tâches **incomplètes** de la section
   **« pour claude »** (`1208173596025107`). C'est là que Guillaume dépose les nouvelles
   tâches ET renvoie les relances.
   → NE PAS traiter : « a travailler Guillaume » (`1208173596025108`, sa file à lui),
   « à lire / valider » (`1208173596025094`, balle déjà chez lui), le pipeline candidatures
   (« à postuler » / « postulé »), et toute tâche complétée.
3. Pour chaque tâche de la file, la **lire en entier** (`get_task`, commentaires inclus) :
   - Repérer le **dernier commentaire non préfixé `[Claude]`** = la consigne courante de
     Guillaume. **Agir sur CETTE consigne**, pas re-répondre à ce qui est déjà traité plus
     haut dans le fil.
   - S'il n'y a aucun commentaire (tâche neuve), partir de la description (`notes`).
4. **Classer & agir** :
   - **(a) Question** (factuelle, méthode, conseil) → répondre **complètement** en
     commentaire signé.
   - **(b) Action réalisable seul** (résumer un flux RSS / une URL, rechercher, rédiger,
     analyser un fichier du repo) → **faire l'action**, puis poster le résultat en
     commentaire signé.
   - **(c) Besoin de matière / ambigu / hors périmètre** → commentaire **court** signé
     disant précisément ce qu'il faut de Guillaume, ou poser la question. **Ne pas deviner.**

   **Format selon la longueur de la réponse** (économie de tokens + lisibilité) :
   - Réponse **courte / factuelle** → directement en commentaire signé (la réponse vit à
     côté de la question, rien ne se perd).
   - Réponse **longue ou structurée** (analyse, doc, protocole, comparatif) → écrire un
     **markdown dans le repo concerné** (immo → `ClaudeAchatMaison`, pilote →
     `candidaturePilote`, méta → `claude-os`) et **coller le lien** dans un commentaire
     signé court. Guillaume le lit quand il veut. Éviter de noyer le fil Asana sous un pavé.
   - **Pourquoi ça reste économe** : chaque tâche est traitée **isolément**, sans recharger
     l'historique d'une longue conversation chat → souvent moins cher qu'en chat. C'est
     justement l'intérêt du dépôt de questions ici (capture asynchrone, sans contexte, sans
     perdre les réponses). Si une tâche demande malgré tout un gros contexte, le signaler.
5. **Routage** selon le sujet :
   - Immo (DVF, négo, vices, commune en zone) → logique repo `ClaudeAchatMaison`
     (skill `audit-immo-fr`).
   - Candidature pilote (offres, LM, CV, relance) → repo `candidaturePilote` ; si
     rédaction au nom de Guillaume, charger `profil-redactionnel-guillaume.md` +
     `structure-lm-pilote.md`. **Ne pas croiser AF/HOP** avec ce projet plan B.
   - Méta CC / DNA / claude-os → `INBOX-QUESTIONS.md` global.
6. **Commentaires** : `add_comment` en **`text` (texte brut)**, PAS `html_text` — le client
   Asana de Guillaume affiche le HTML en BRUT (balises visibles). Structurer en texte simple
   (sauts de ligne, tirets « - » pour les listes). **Toujours préfixés `[Claude] `**.
   **Un seul commentaire de synthèse par passage**, pas de bavardage.
7. **Renvoyer la balle** : toute tâche traitée est déplacée dans « à lire / valider » via
   `update_tasks add_projects:[{project_id:1208173596025068, section_id:1208173596025094}]`.
   Exception : si la tâche attend une **action de moi** (pas une décision de Guillaume), la
   laisser dans « pour claude » jusqu'à ce que ce soit fait.
8. **Persister ce qui fait avancer le projet** (décision Guillaume, 2026-06-24) : pour toute
   tâche où une **décision est prise** ou une **orientation validée** (même brève), consigner
   dans le fichier de connaissance du repo concerné, puis **commit** :
   - candidature pilote → `candidaturePilote/data/qa_log.json`
   - immo → `ClaudeAchatMaison/INBOX-QUESTIONS.md`
   - méta CC / DNA / claude-os → `claude-os/INBOX-QUESTIONS.md`
   Format minimal : **Question / Décision / Pourquoi / Date / lien tâche Asana**. Synthétiser
   si l'échange est long (pas besoin du verbatim). Le **trivial** (aucune décision) reste en
   commentaire Asana seul — pas de commit pour une ligne. Pousser (cloud = seul le poussé survit).
9. **Récap chat** final : tâches traitées + nature (réponse / action / besoin de matière /
   relance), tâches laissées intactes (balle côté Guillaume) et pourquoi, questions en
   attente de décision de Guillaume.

## Garde-fous

- **Ne jamais** marquer une tâche `completed` — c'est Guillaume qui valide (ou relance).
  Cohérent doctrine §7 : on ne ferme que des Actions, et c'est sa main.
- **Ne jamais** supprimer une tâche, ni envoyer quoi que ce soit en externe (mail,
  candidature) sans accord explicite.
- **Toujours signer** mes commentaires `[Claude] ` (sans ça, la boucle de relance casse).
  Signature **textuelle**, pas d'emoji décoratif (doctrine §7).
- **Contrainte LYS** (base Lyon Saint-Exupéry) = forte sur les candidatures pilote :
  signaler tout conflit base / relocation avant de recommander un envoi.
- En cas de doute sur l'interprétation d'une tâche → commentaire question signé, pas
  d'action irréversible.

## Maintenance des GID

Si un GID ne répond plus (projet/section renommé ou recréé), le re-résoudre :
`search_objects` (project) pour le projet, `get_project include_sections=true` pour
retrouver les sections « pour claude », « a travailler Guillaume » et « à lire / valider »
par leur nom. **Créer une section dans un projet existant est impossible via le MCP**
(doctrine §4) ; demander à Guillaume de la (re)créer si besoin.
