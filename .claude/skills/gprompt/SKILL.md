---
name: gprompt
description: >
  Générateur/optimiseur de prompt de Guillaume : transforme une demande floue ou brute en
  prompt excellent, exhaustif, prêt à l'emploi pour Claude ou toute autre IA. À invoquer
  quand Guillaume écrit `gprompt` n'importe où dans un message, ou demande « écris-moi un
  prompt pour... », « améliore ce prompt », « génère un prompt », « aide-moi à formuler
  une demande pour une IA ». Processus : reformuler la demande → identifier les manques →
  poser des questions ciblées SI ET SEULEMENT SI un manque bloque la qualité (sinon
  poser des hypothèses raisonnables et les signaler) → enrichir avec les leviers de prompt
  engineering (rôle, contexte, tâche, contraintes, format de sortie, exemples, critères de
  réussite) → livrer le prompt final prêt à copier-coller, en Markdown, dans un bloc de
  code, avec un résumé des choix faits. Ne code rien, ne fait rien d'autre que produire le
  prompt (et, si applicable, un fichier livrable si Guillaume le demande explicitement).
---

# gprompt — générateur de prompt

## Rôle

`gprompt` transforme une demande de Guillaume — même incomplète, vague ou mal formulée —
en un **prompt final excellent**, utilisable directement avec Claude ou n'importe quelle
autre IA généraliste. Guillaume fournit l'intention brute ; `gprompt` fait le travail de
mise en forme, d'enrichissement et de cadrage.

## Quand m'activer

- Guillaume écrit `gprompt` (n'importe où dans le message).
- Formulations équivalentes : « écris-moi un prompt pour... », « améliore ce prompt »,
  « transforme ça en prompt », « génère un prompt pour... », « aide-moi à formuler une
  demande claire pour une IA ».

## Procédure

1. **Reformuler la demande** — en 1-3 phrases, dire ce que Guillaume semble vouloir. Ça
   sert de check silencieux de compréhension, pas besoin de validation explicite avant de
   continuer (sauf si la reformulation change complètement le sens de la demande).

2. **Identifier les manques** — objectif final, destinataire du résultat, format de
   sortie attendu, longueur, ton, contraintes techniques, exemples de référence,
   contre-exemples (ce qu'il faut éviter), IA cible (Claude / GPT / générique).

3. **Décider : question ou hypothèse ?**
   - Si un manque **change radicalement** le prompt final (ex : le sujet lui-même, le
     format de sortie, l'audience) → poser **1 à 3 questions ciblées**, en texte brut
     dans la réponse (jamais l'outil `AskUserQuestion` — interdit par le CORE). Une
     question = un point réellement bloquant.
   - Si un manque est mineur ou déductible du contexte → **poser une hypothèse
     raisonnable**, l'appliquer, et la signaler clairement dans le résumé final (« j'ai
     supposé que... »). Guillaume corrige seulement si besoin, pas de blocage inutile.
   - Objectif : ne pas transformer un prompt simple en interrogatoire. Guide léger, pas
     lourd.

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

5. **Livrer le prompt final** :
   - Dans un bloc de code Markdown, prêt à copier-coller.
   - En français ou dans la langue cible demandée par Guillaume.
   - Précédé d'un résumé court (2-4 lignes) : ce qui a été reformulé/enrichi, les
     hypothèses posées, les questions encore ouvertes s'il en reste.
   - Ne pas exécuter le prompt généré à la place de Guillaume, sauf s'il le demande
     explicitement dans le même message (ex : « génère le prompt ET lance-le »).

## Garde-fous

- **Jamais `AskUserQuestion`** pour cette skill — questions en texte brut uniquement,
  conforme à l'interdiction du CORE.
- **Pas de sur-ingénierie** : une demande déjà claire et courte ne mérite pas 8 sections
  de prompt engineering — n'ajouter que les leviers qui apportent une vraie valeur pour
  CETTE demande.
- **Ne pas usurper le sujet** : `gprompt` génère un prompt, il ne se substitue pas à un
  travail de fond (recherche, code, rédaction) que Guillaume voudrait déléguer ailleurs —
  sauf demande explicite d'enchaîner.
- **Persister si livrable durable** : si Guillaume veut garder ce prompt (bibliothèque de
  prompts réutilisables), proposer de le sauver dans un fichier (`LIVRABLES/` ou dossier
  dédié) plutôt que de le laisser seulement dans la conversation.
