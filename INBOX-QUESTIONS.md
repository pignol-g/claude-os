# INBOX QUESTIONS — Global (claude-os)

> Questions différées hors-projet (méta CC, DNA, claude-os, perso non rattaché).
> Mécanisme : `CLAUDE-DNA-CC-CORE.md` §"Inbox questions différées — trigger `q:`".
> Pour questions liées à un projet spécifique → inbox de ce projet (`<projet>/INBOX-QUESTIONS.md`).

## ⏳ En attente

### 2026-07-21 — Pourquoi le profil rédactionnel déjà testé (candidaturePilote) a échoué ?
- **Constat mis à jour** (retour de Guillaume après lecture du rapport grech) : contrairement à
  l'hypothèse initiale, un vrai profil rédactionnel avait déjà été **utilisé** dans
  `candidaturePilote` (Opus 4.8, Claude Code) — sans succès. Le stub vide de `claude-os`
  n'explique donc pas tout ; l'hypothèse dominante devient le system prompt de Claude Code
  (terseness par design) qui dilue/écrase même un vrai profil chargé.
- **Décision à prendre** : Guillaume ajoute le repo `candidaturePilote` à une session pour que
  Claude inspecte le contenu réel du profil utilisé et diagnostique précisément pourquoi ça n'a
  pas suffi (format, absence de règles absolues anti-tics, jamais vraiment chargé au bon moment,
  etc.) ? Ou il diagnostique lui-même avec la grille fournie dans l'addendum du rapport ?
- Voir `LIVRABLES/RECHERCHE_LETTRE_MOTIVATION_NATURELLE_2026-07-21.md` (section Addendum).

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
- **Recommandation initiale** : rédiger dans claude.ai chat (pas Claude Code) avec le feature
  "Styles → Add a Writing Example" ou un few-shot avec ses propres textes ; modèle Sonnet par
  défaut ; prompt-type fourni dans le rapport.
- **Corrigé le même jour** (retour Guillaume) : le feature "Styles" est retiré de claude.ai
  (migration vers "Skills", confirmée par recherche complémentaire — moins fiable car invoquée
  seulement quand Claude juge nécessaire, pas à chaque message). Un vrai profil avait déjà été
  testé sans succès avec Opus 4.8 dans Claude Code, ce qui renforce l'hypothèse "outil" plutôt
  que "donnée manquante". Voir Addendum du rapport pour la méthode de fabrication d'un skill de
  voix (4-6 échantillons + règles absolues anti-tics) et la recommandation mise à jour.
- **Mise en œuvre** : voir `LIVRABLES/RECHERCHE_LETTRE_MOTIVATION_NATURELLE_2026-07-21.md`
  (4 agents, ~211 sources, avec addendum).

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
