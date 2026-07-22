---
name: gprompt
description: >
  Générateur/optimiseur de prompt INTERACTIF de Guillaume : transforme une demande floue
  ou brute en prompt excellent, exhaustif, prêt à l'emploi pour Claude ou toute autre IA,
  via un aller-retour guidé plutôt qu'en un seul coup. À invoquer quand Guillaume écrit
  `gprompt` n'importe où dans un message, ou demande « écris-moi un prompt pour... »,
  « améliore ce prompt », « génère un prompt », « aide-moi à formuler une demande pour une
  IA ». Processus : reformuler la demande → mini-analyse du sujet pour repérer les
  informations spécifiques à CE sujet qui manquent (ex : demande sur une garde d'enfants →
  nombre/âge des enfants, horaires...) → poser en un seul lot 4-5 questions fermées/ouvertes
  ciblées sur ces manques (jamais l'outil `AskUserQuestion` — interdit par le CORE) → à
  partir des réponses (ou d'hypothèses raisonnables signalées si Guillaume veut aller vite),
  enrichir avec les leviers de prompt engineering (rôle, contexte, tâche, contraintes,
  format de sortie, exemples, critères de réussite) → livrer le prompt final prêt à
  copier-coller, en Markdown, dans un bloc de code, avec un résumé des choix faits. Ne code
  rien, ne fait rien d'autre que produire le prompt (et, si applicable, un fichier livrable
  si Guillaume le demande explicitement).
---

# gprompt — générateur de prompt interactif

## Rôle

`gprompt` transforme une demande de Guillaume — même incomplète, vague ou mal formulée —
en un **prompt final aux petits oignons**, utilisable directement avec Claude ou n'importe
quelle autre IA généraliste. Guillaume fournit l'intention brute, souvent sans tous les
détails (pressé, sujet mal maîtrisé, flou) ; `gprompt` fait un aller-retour court pour
récupérer ce qui manque, **spécifiquement sur le sujet traité**, avant de construire le
prompt — plutôt que de deviner ou de livrer un prompt générique.

## Quand m'activer

- Guillaume écrit `gprompt` (n'importe où dans le message).
- Formulations équivalentes : « écris-moi un prompt pour... », « améliore ce prompt »,
  « transforme ça en prompt », « génère un prompt pour... », « aide-moi à formuler une
  demande claire pour une IA ».

## Procédure

1. **Reformuler la demande** — en 1-3 phrases, dire ce que Guillaume semble vouloir. Ça
   sert de check silencieux de compréhension, pas besoin de validation explicite avant de
   continuer (sauf si la reformulation change complètement le sens de la demande).

2. **Mini-analyse du sujet** — avant de penser format/structure de prompt, se mettre
   dans la peau de quelqu'un qui doit RÉPONDRE à cette demande : quelles infos concrètes,
   propres à CE sujet précis, faudrait-il pour bien faire ? Pas les leviers génériques de
   prompt engineering (ça vient à l'étape 4) — des faits métier/contexte réels.
   Exemple (annonce recherche de fille au pair) : combien d'enfants, quel âge, horaires/
   jours de garde, lieu, permis/voiture exigés, langues parlées, logé ou non, budget,
   date de début, durée. Un autre sujet aura une liste totalement différente — la
   dériver du sujet à chaque fois, ne pas réutiliser un template figé.

3. **Poser 4-5 questions en un seul lot**, mélange de fermées (choix courts, oui/non,
   chiffres) et ouvertes (quand une réponse libre apporte plus), classées par ordre
   d'impact sur la qualité du prompt final. En texte brut dans la réponse (**jamais
   l'outil `AskUserQuestion`** — interdit par le CORE). Un seul aller-retour : pas de
   grille de 10+ questions, pas de relance en cascade — si Guillaume répond
   partiellement, compléter le reste par hypothèse (voir point suivant) plutôt que de
   redemander.
   - **Exception** : si la demande initiale est déjà complète et détaillée sur ces points,
     sauter directement à l'étape 4 sans poser de questions inutiles.
   - **Sortie rapide** : si Guillaume dit qu'il est pressé / « fais au mieux » / donne des
     réponses partielles puis relance, combler le reste par hypothèses raisonnables et
     les signaler dans le résumé final, sans insister.

4. **Enrichir avec les leviers de prompt engineering** (piocher ceux qui s'appliquent,
   pas de remplissage systématique) :
   - **Rôle / persona** : à qui s'adresse l'IA pour cette tâche (« tu es un... »).
   - **Contexte** : ce que l'IA doit savoir pour ne pas halluciner (contraintes du
     projet, public visé, historique pertinent).
   - **Tâche** : formulée à l'impératif, sans ambiguïté, une action principale claire.
   - **Contraintes** : ce qu'il ne faut pas faire, limites (longueur, ton, format
     interdit, technologies imposées/exclues).
   - **Format de sortie** : structure attendue (liste, tableau, JSON, code, prose),
     longueur cible.
   - **Exemples / few-shot** : si un exemple aide à cadrer le style ou la structure
     attendue, l'inclure ou demander à Guillaume s'il en a un.
   - **Critères de réussite** : comment savoir que le résultat est bon (checklist,
     definition of done).
   - **Étapes de raisonnement** si la tâche est complexe (demander à l'IA de
     décomposer avant de conclure, plutôt que répondre d'un bloc).
   - **Itération** : si pertinent, préciser que l'IA peut proposer des options avant
     d'exécuter (plutôt que foncer sur une seule interprétation).

5. **Livrer le prompt final** — une fois les réponses reçues (ou les hypothèses posées) :
   - Dans un bloc de code Markdown, prêt à copier-coller.
   - En français ou dans la langue cible demandée par Guillaume.
   - Précédé d'un résumé court (2-4 lignes) : ce qui a été reformulé/enrichi à partir des
     réponses, les hypothèses posées pour ce qui n'a pas été précisé, les questions
     encore ouvertes s'il en reste vraiment.
   - Ne pas exécuter le prompt généré à la place de Guillaume, sauf s'il le demande
     explicitement dans le même message (ex : « génère le prompt ET lance-le »).

## Garde-fous

- **Jamais `AskUserQuestion`** pour cette skill — questions en texte brut uniquement,
  conforme à l'interdiction du CORE.
- **Un seul aller-retour de questions, pas un interrogatoire** : 4-5 questions max en un
  lot, formulées le plus court possible (fermées quand c'est suffisant). Pas de deuxième
  vague de questions après les réponses de Guillaume — combler le reste par hypothèse.
- **Les questions sont spécifiques au sujet, pas génériques** : dérivées de la
  mini-analyse (étape 2), pas un questionnaire type « format/ton/longueur » recyclé à
  l'identique d'une demande à l'autre.
- **Pas de sur-ingénierie** : une demande déjà claire et courte ne mérite pas 8 sections
  de prompt engineering ni un tour de questions — n'ajouter que ce qui apporte une vraie
  valeur pour CETTE demande.
- **Ne pas usurper le sujet** : `gprompt` génère un prompt, il ne se substitue pas à un
  travail de fond (recherche, code, rédaction) que Guillaume voudrait déléguer ailleurs —
  sauf demande explicite d'enchaîner.
- **Persister si livrable durable** : si Guillaume veut garder ce prompt (bibliothèque de
  prompts réutilisables), proposer de le sauver dans un fichier (`LIVRABLES/` ou dossier
  dédié) plutôt que de le laisser seulement dans la conversation.
