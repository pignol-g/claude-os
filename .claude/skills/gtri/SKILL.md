---
name: gtri
description: >
  Tri et transfert claude-os → general de Guillaume : critères de classification pour
  distinguer l'outillage Claude Code (reste dans claude-os) de la connaissance/livrables
  produits avec l'aide d'une IA sur un sujet quelconque (part vers le repo `general`,
  multi-IA — Claude, ChatGPT, autre). À invoquer quand Guillaume écrit `gtri` n'importe
  où dans un message, ou demande « fais le tri », « qu'est-ce qui doit partir dans
  general », « transfère vers general », « range ça ». Processus : scanner les candidats
  → appliquer les 5 tests de décision → proposer chaque candidat en Q/R (jamais de
  transfert silencieux) → exécuter le transfert validé (fichier recréé dans
  `general/<catégorie>/` avec en-tête de provenance, source supprimée ou remplacée par
  pointeur raw URL si référencée ailleurs dans le DNA) → tracer dans
  `general/_TRANSFERTS-LOG.md` → commit + push des deux repos.
---

# gtri — tri et transfert claude-os → general

## Pourquoi cette skill existe

Deux repos, deux rôles distincts :

| Repo | Rôle | Géré par |
|---|---|---|
| `claude-os` | Outillage Claude Code de Guillaume : DNA, hooks, skills, scripts, conventions `to-chat/to-cc/to-os`. Parle de **comment Claude doit se comporter/être configuré**. | Claude Code exclusivement (mécaniques CC) |
| `general` | Tous les sujets généraux : recherches, livrables, notes, profils personnels. Parle d'**un sujet que Guillaume traite avec l'aide d'une IA**, peu importe laquelle. | N'importe quelle IA (Claude, ChatGPT, autre) |

En session normale, le travail se fait là où la session CC est ouverte — souvent
`claude-os` par habitude/proximité. Ça fait dériver dans `claude-os` du contenu qui n'a
rien à voir avec l'outillage Claude (une recherche carrière, un profil rédactionnel, une
lettre de motivation). `gtri` est la passe de rattrapage récurrente qui détecte cette
dérive et migre le contenu au bon endroit.

## La question qu'on tranche, pour chaque fichier candidat

> Est-ce que ce contenu décrit **comment Claude (Code ou Chat) doit se comporter ou être
> configuré pour Guillaume**, ou est-ce que c'est **une substance/un sujet** que Guillaume
> traite avec l'aide d'une IA (peu importe laquelle) ?

Premier cas → reste `claude-os`. Second cas → part vers `general`.

## Les 5 tests de décision (dans l'ordre, le premier qui tranche gagne)

1. **Dépendance à l'outil** — le fichier a-t-il pour SUJET des mécaniques Claude Code
   (hooks, skills, MCP, `settings.json`, triggers `gXXX`, dossiers `to-chat/to-cc/to-os`) —
   pas juste une mention en passant ? → OUI = **reste claude-os**.
   Exemples : `CLAUDE-DNA-CC-CORE.md`, `.claude/skills/*`, `scripts/install-claude-config.sh`.

2. **Portabilité inter-IA** — ouvert demain dans ChatGPT/Gemini, sans aucun contexte
   Claude Code, le fichier resterait-il utile TEL QUEL (à la reformulation de prompt
   près) ? → OUI = **candidat general**.
   Exemple : un profil rédactionnel, une recherche fiscale, une lettre de motivation.

3. **Sujet vs outil** — le fichier est-il un LIVRABLE (recherche, lettre, analyse,
   décision) où Claude n'a été qu'un OUTIL d'exécution, sur un sujet qui existerait sans
   Claude ? → OUI = **general**.
   Contre-exemple à ne pas transférer trop vite : une recherche comparant des IA entre
   elles peut avoir pour vrai sujet une décision d'architecture claude-os (quel modèle/outil
   utiliser pour quelle tâche CC) — dans ce cas précis, c'est le test 1 qui prime. Voir
   « Cas ambigus » plus bas, ne pas trancher seul.

4. **Utile sans Claude Code** — si Guillaume n'ouvrait plus jamais Claude Code (juste
   Claude Chat web ou ChatGPT), ce fichier resterait-il pertinent ? → OUI = **general**.
   (Test réservé aux livrables/connaissances ; ne s'applique pas aux mécaniques d'outil,
   hors-sujet dans ce cas de figure.)

5. **Profil/identité personnelle** — fichiers de profil personnel (voix rédactionnelle,
   préférences, bio) référencés PAR claude-os mais dont le CONTENU est intrinsèquement
   personnel et réutilisable par toute IA → **general**, avec un pointeur depuis
   claude-os (raw URL, pas de copie — même logique que « DNA pointé, jamais copié »,
   `CLAUDE-DNA-CC-REF.md#dna-pointe`).

## Ce qui reste TOUJOURS dans claude-os

`CLAUDE-DNA*.md` (tous), `.claude/` (hooks, skills, settings), `scripts/`, `to-chat/`,
`to-cc/`, `to-os/`, `README.md` du repo, `REPRISE.md`, `TODO.md`, `INBOX-QUESTIONS.md`
(le fichier-mécanisme lui-même — une entrée dont le SUJET est hors-Claude peut, elle,
être extraite vers `general/_INBOX/` avec référence croisée).

## Ce qui part TOUJOURS vers general

- `LIVRABLES/` — par nature un livrable est un résultat métier/personnel, jamais un
  réglage Claude (sauf s'il documente littéralement une décision DNA/skill).
- `recherches/` dont le sujet n'est pas claude-os/Claude Code lui-même (carrière,
  immobilier, santé, fiscal, vie perso...). Le dossier `recherches/` de claude-os ne
  devrait garder QUE des recherches dont le sujet est claude-os/l'architecture DNA.
- Profils personnels (test 5).

## Cas ambigus — toujours gpose, jamais trancher seul

- **Comparatifs d'outils IA** (Claude vs ChatGPT, choix de modèle...) : reste claude-os SI
  le but est d'éclairer une décision d'architecture claude-os/DNA ; part en general SI le
  but est une connaissance/veille générale sans lien avec une décision DNA en cours.
- **`INBOX-QUESTIONS.md`** : le fichier reste, une entrée isolée peut partir.
- Tout candidat qui hésite entre deux tests → proposer en Q/R plutôt que choisir seul.

## Protocole d'exécution

1. **Scanner** claude-os : racine + `LIVRABLES/` + `recherches/` + tout dossier hors
   `.claude/`, `to-chat/`, `to-cc/`, `to-os/`, `scripts/`, `CLAUDE-DNA*.md`, `README.md`,
   `REPRISE.md`, `TODO.md`. Lister les candidats avec le test qui a tranché pour chacun.
2. **Proposer en Q/R** — jamais d'exécution silencieuse :
   ```
   tri — <fichier> : test <n°> → <verdict proposé>
     triA   transférer vers general/<catégorie>/
     triB   garder dans claude-os
     triC   fusionner/résumer (si redondant avec un doc déjà présent dans general)
   ```
3. **Exécuter le transfert validé** :
   a. Créer le fichier dans `general/<catégorie>/<nom>.md` avec en-tête de provenance :
      `<!-- Transféré depuis claude-os le AAAA-MM-JJ (skill gtri) -->`.
   b. Classer selon `general/README.md` (choisir/créer le dossier catégorie).
   c. `git rm` le fichier source dans claude-os — sauf s'il est référencé ailleurs dans
      le DNA, auquel cas le remplacer par un pointeur raw URL vers `general` (jamais de
      doublon : une info, un seul propriétaire, cf. loi anti-divergence
      `CLAUDE-DNA-ASANA.md` §3).
   d. Si le fichier transféré était référencé dans `CLAUDE-DNA-CC-CORE.md` ou ailleurs,
      mettre à jour la référence vers le nouveau raw URL `general`.
   e. Commit + push **séparément** dans les deux repos (claude-os ET general — deux repos
      git distincts, deux commits).
4. **Tracer** : une ligne dans `general/_TRANSFERTS-LOG.md` (date, fichier, origine,
   test utilisé, décision Guillaume).

## Quand m'activer

- Guillaume écrit `gtri` n'importe où dans son message.
- Formulations équivalentes : « fais le tri », « qu'est-ce qui doit partir dans
  general », « transfère vers general », « range ça ».
- Facultatif, priorité basse, en fin de boucle `gauto` si le backlog principal est traité.

## Anti-patterns

- ❌ Transférer sans Q/R, même pour un cas qui semble évident.
- ❌ Dupliquer (garder une copie dans claude-os ET general) — un seul propriétaire.
- ❌ Confondre « parle de Claude » avec « est un mécanisme Claude Code » : un fichier qui
  mentionne Claude Chat en général (ex. `CLAUDE-DNA-CHAT.md`) mais qui EST un réglage DNA
  reste dans claude-os (test 1).
- ❌ Sur-découper la classification `general/` dès le premier passage — peu de catégories
  larges, affiner à l'usage.
