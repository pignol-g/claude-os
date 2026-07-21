# INBOX QUESTIONS — Global (claude-os)

> Questions différées hors-projet (méta CC, DNA, claude-os, perso non rattaché).
> Mécanisme : `CLAUDE-DNA-CC-CORE.md` §"Inbox questions différées — trigger `q:`".
> Pour questions liées à un projet spécifique → inbox de ce projet (`<projet>/INBOX-QUESTIONS.md`).

## ⏳ En attente

### 2026-07-21 — Profil rédactionnel toujours vide → migration bloquée
- **Constat** (issu de la recherche grech lettre de motivation) : `profil-redactionnel-guillaume.md`
  est un stub vide depuis le 13/06/2026, alors que le CORE impose de le charger avant toute
  rédaction en son nom. Contenu réel censé venir de
  `candidaturePilote/livrables/lettres/_templates/profil-redactionnel-guillaume.md`.
- **Décision à prendre** : Guillaume ajoute le repo `candidaturePilote` à une session pour que
  Claude fasse la migration, ou colle le contenu lui-même ? Sans ça, toute rédaction "à sa voix"
  reste générique par construction, quel que soit le modèle utilisé.
- Voir `LIVRABLES/RECHERCHE_LETTRE_MOTIVATION_NATURELLE_2026-07-21.md`.

---

## ✅ Traitées (archive)

### 2026-07-21 — Recherche : lettre de motivation naturelle avec Claude (skill grech)
- **Question** : quel modèle Claude et quelle méthode donnent la lettre de motivation la plus
  naturelle ? Pourquoi ChatGPT (réputé moins naturel) a donné de meilleurs résultats en pratique
  que Claude Code ?
- **Verdict** : pas un problème de modèle (aucune donnée ne classe Opus/Sonnet/Fable/Haiku sur la
  naturalité rédactionnelle ; Fable n'est pas un modèle créatif malgré son nom). Deux causes
  probables identifiées : (1) le system prompt de Claude Code impose la concision par design
  (outil CLI/code, pas rédaction) ; (2) le fichier `profil-redactionnel-guillaume.md` censé
  injecter sa vraie voix est un stub vide depuis le 13/06/2026 — jamais de style réel injecté,
  peu importe le modèle. La pollution de contexte par un CLAUDE.md volumineux est un facteur
  réel et documenté par Anthropic elle-même (post-mortem avril 2026, -80% du system prompt
  Claude Code pour Fable 5), même si pas prouvé spécifiquement sur ce cas.
- **Recommandation** : rédiger dans claude.ai chat (pas Claude Code) avec le feature "Styles →
  Add a Writing Example" ou un few-shot avec ses propres textes ; modèle Sonnet par défaut ;
  prompt-type fourni dans le rapport.
- **Mise en œuvre** : voir `LIVRABLES/RECHERCHE_LETTRE_MOTIVATION_NATURELLE_2026-07-21.md`
  (4 agents, ~209 sources).

### 2026-06-24 — Persistance des décisions (skill asana-pass)
- **Question** : quand je réponds dans Asana, faut-il aussi enregistrer dans le repo pour centraliser la base de connaissance ?
- **Décision** : oui, persister au MAXIMUM ce qui fait avancer le projet (question + décision + justification), par commits fréquents ; synthèse si l'échange est long ; le trivial reste en commentaire Asana seul.
- **Pourquoi** : les commentaires Asana sont persistants mais pas centralisés/réutilisables ; tracer décisions + raisons permet de reconstituer plus tard « on avait décidé X pour Y ».
- **Mise en œuvre** : nouvelle étape 8 de la skill `asana-pass` (routage qa_log.json / INBOX-QUESTIONS.md + format Question/Décision/Pourquoi/Date/lien).
- Tâche Asana : « amorce question » (gid 1208173596025086).

### 2026-06-24 — File d'entrée = section « pour claude »
- **Question** : comment la skill identifie-t-elle ce qu'elle doit traiter, maintenant que Guillaume a créé des sections dédiées ?
- **Décision** : la file de travail de Claude = uniquement la section **« pour claude »** ; « a travailler Guillaume » est la file de Guillaume (jamais traitée) ; « à lire / valider » = balle chez Guillaume.
- **Pourquoi** : l'ancienne règle « tout sauf à lire/valider » aurait à tort inclus la file de Guillaume et le pipeline candidatures.

### 2026-06-24 — Commentaires Asana en texte brut
- **Décision** : poster les commentaires via `text` (brut), pas `html_text`.
- **Pourquoi** : le client Asana de Guillaume affiche le HTML en brut (balises visibles), obligeant à reposter une version lisible.
