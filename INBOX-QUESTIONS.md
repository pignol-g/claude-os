# INBOX QUESTIONS — Global (claude-os)

> Questions différées hors-projet (méta CC, DNA, claude-os, perso non rattaché).
> Mécanisme : `CLAUDE-DNA-CC-CORE.md` §"Inbox questions différées — trigger `q:`".
> Pour questions liées à un projet spécifique → inbox de ce projet (`<projet>/INBOX-QUESTIONS.md`).

## ⏳ En attente

_(vide)_

---

## ✅ Traitées (archive)

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
