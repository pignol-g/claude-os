---
name: grech
description: >
  Recherche approfondie multi-agents de Guillaume : reproduit au maximum la fonctionnalité
  « recherche avancée » de Claude chat, dans Claude Code. À invoquer quand Guillaume tape
  /grech, écrit « grech » n'importe où dans un message, ou demande « recherche poussée »,
  « recherche approfondie », « lance une deep research ». Processus : décomposer la question
  en angles indépendants → 1 subagent Sonnet par angle en parallèle (autant que nécessaire,
  pas de limite à 4) → chaque agent source CHAQUE affirmation et rend la liste complète des
  URLs consultées (cible cumulée : >100 sources) → croiser avec l'état interne du dossier
  (JSON pivots, fichiers projet) → rapport consolidé : TL;DR, scénarios ouverts/fermés,
  coûts chiffrés, recommandation, annexe de sources. Livrable persisté + commité.
---

# grech — recherche approfondie multi-agents

Reproduire dans Claude Code la « recherche avancée » de Claude chat : large fan-out de
subagents, sourçage systématique, rapport détaillé. Modèle éprouvé le 05/07/2026 sur la
question « étalement QT BE1900D » (4 agents, ~125 sources, verdict inattendu trouvé en
croisant web + dossier interne) : `impots2025/LIVRABLES/RECHERCHE_ETALEMENT_QT_2026-07-05.md`.

> **Posture (DNA)** : vérifier l'état réel du dossier AVANT de chercher dehors — la réponse
> est parfois déjà dans les fichiers internes, et la prémisse de la question peut être fausse.
> Économie de tokens : Opus orchestre et parle à Guillaume, **Sonnet exécute les recherches**
> (Haiku possible pour du factuel pur : barèmes, URLs, définitions).

## Étape 0 — Cadrage (Opus, avant tout lancement)

1. **Reformuler la question** en une phrase, avec la prémisse implicite de Guillaume.
2. **Lire l'état interne** : JSON pivots, notes de session, décisions déjà prises sur le
   sujet. Si la question a déjà été tranchée, le dire — et chercher ce qui a changé depuis.
3. **Découper en angles indépendants** (= futurs agents). Grille de départ, à adapter :
   - **Sources officielles / primaires** (textes, doctrine, documentation de référence)
   - **Jurisprudence / précédents / historique**
   - **Retours d'expérience** (forums spécialisés, communautés, témoignages)
   - **Pratique et coûts** (à qui demander, procédures, tarifs, délais)
   - Angles supplémentaires si le sujet l'exige : comparaison internationale, données
     chiffrées/statistiques, acteurs du marché, risques/contre-arguments…
4. **Autant d'agents que d'angles utiles** — pas de plafond à 4. Deux règles seulement :
   chaque agent doit avoir un angle **réellement distinct** (sinon fusionner), et au-delà de
   ~6-8 agents, vérifier que le quota du plan tient (annoncer l'estimation à Guillaume si la
   session est interactive ; en autonome, rester ≤ 6 sauf enjeu fort).

## Étape 1 — Lancement des agents (parallèle, en un seul bloc)

Chaque prompt d'agent contient obligatoirement :

1. **Le rôle** (« Tu es un agent de recherche [angle] ») et l'outil (WebSearch + WebFetch,
   ou MCP Gmail/Drive/GitHub selon la cible).
2. **Le CONTEXTE complet** : qui est Guillaume, les faits chiffrés, ce qui est déjà acquis
   (« DÉJÀ CAPTÉ — NE PAS REDOCUMENTER » pour éviter les doublons).
3. **Les questions numérotées** (3-6 max par agent, précises, fermées quand possible).
4. **Le plancher de sources** : « minimum 20-25 sources consultées », en privilégiant les
   sources primaires de l'angle (officiel → BOFiP/Légifrance ; communautaire → forums…).
5. **Le FORMAT DE RÉPONSE imposé** :
   - réponse par point, **chaque affirmation sourcée** (URL + référence précise) ;
   - plafond de mots (700-800) pour forcer la densité ;
   - section finale « LISTE COMPLÈTE DES SOURCES CONSULTÉES » — toutes les URLs, une par
     ligne, marquées **[citée]** ou **[consultée]** (c'est ce qui permet le total >100) ;
   - un **verdict** en une phrase (clair/flou, favorable/défavorable, trouvé/vierge).
6. **Modèle** : `sonnet` (défaut). Lancer tous les Agent() dans le même bloc, en arrière-plan.

## Étape 2 — Croisement (Opus, au fil des retours)

- À chaque retour d'agent : signaler à Guillaume en 2-4 phrases **ce qui est load-bearing**
  (pas un résumé exhaustif), surtout les surprises et les contradictions.
- **Confronter systématiquement les trouvailles à l'état interne du dossier** — c'est là
  que naissent les vrais verdicts (ex. QT : le web disait « déficit reportable », le dossier
  montrait qu'il était déjà appliqué → question sans objet).
- Deux agents qui se contredisent = point à trancher explicitement dans le rapport (vérifier
  soi-même la source primaire si nécessaire, ex. numéro de jurisprudence).

## Étape 3 — Rapport consolidé (livrable)

Fichier Markdown daté dans le dossier livrables du projet concerné
(ex. `LIVRABLES/RECHERCHE_<SUJET>_<AAAA-MM-JJ>.md`). Structure :

1. **En-tête méthodo** : date, nb d'agents, nb de sources, fichiers internes croisés.
2. **TL;DR** : 2-4 puces, verdict d'abord.
3. **La question et la prémisse** — corrigée si elle est fausse.
4. **Tableau des scénarios** : chaque option ✅ OUVERTE / ❌ FERMÉE, avec le motif sourcé.
   Fermer explicitement les scénarios impossibles est aussi important que documenter les
   scénarios ouverts.
5. **Sections thématiques** (une par angle d'agent, condensées).
6. **Coûts / recours chiffrés** si pertinent (tableau : option, coût, délai, valeur, verdict).
7. **Actions concrètes** avec échéances.
8. **Annexe sources** : listes complètes par agent, [citée]/[consultée].

## Étape 4 — Persistance (non négociable)

- **Rapport** commité dans le repo projet.
- **Conclusions** reportées dans les fichiers d'état du projet (JSON pivot, ETAT_SESSION,
  mémoire…) : une recherche non persistée sera repayée à la prochaine session.
- Envoyer le fichier à Guillaume (SendUserFile) + message final : verdict d'abord, détail
  ensuite. Push fin de session.

## Anti-patterns

- ❌ Lancer les agents sans avoir lu l'état interne (risque : re-répondre à une question
  déjà tranchée, ou rater le fait qui inverse le verdict).
- ❌ Agents aux angles qui se recouvrent (tokens brûlés pour des doublons).
- ❌ Affirmation sans URL dans le rapport final.
- ❌ Résumer chaque agent exhaustivement à Guillaume au fil de l'eau — ne remonter que ce
  qui change la réponse.
- ❌ Oublier l'annexe de sources ou la persistance JSON.
