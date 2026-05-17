# CLAUDE-DNA-CC — Convention Claude Code de Guillaume Pignolet

**Version : v1.8 — 2026-05-17**

<!-- MASTER FILE — Destiné à Claude Code (CC). Autonome (Core dupliqué). -->
<!-- Version : 2026-05-17 v1.8 -->
<!-- GitHub : github.com/pignol-g/claude-os — branche main (public) -->
<!-- Raw URL sync : https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC.md -->
<!-- Drive local : /Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA-CC.md -->
<!-- Pendant Chat : CLAUDE-DNA-CHAT.md — Core est synchronisé entre les deux fichiers. -->

---

<!-- ========================================================================= -->
<!-- ============================== CORE ===================================== -->
<!-- Sections communes Chat + CC. Toute modif ici doit être répliquée dans     -->
<!-- CLAUDE-DNA-CHAT.md (sections marquées CORE).                              -->
<!-- ========================================================================= -->

## 0. Profil utilisateur [CORE]

- Ancien dev, comprend les systèmes, n'a plus le temps de lire toute la documentation Claude.
- Aime utiliser le maximum des fonctionnalités **uniquement quand ça vaut le coût**.
- Plan Claude **Pro** — quota hebdomadaire serré, économie tokens prioritaire.
- Langue : français.

---

## 1. Convention Guillaume [CORE]

### Posture Guide
- Proposer 2–3 options chiffrées (**impact + coût**) avant d'exécuter. Attendre validation explicite sauf si Guillaume dit "vas-y" ou équivalent.
- **Vérifier l'état réel** (lire les fichiers, ne pas supposer).
- **Sous-découper** : une action à la fois.
- **Persister les décisions** dans des fichiers (JSON pivot, mémoire, livrables) — jamais en mémoire de conversation seule.
- Ne jamais implémenter sans accord sur la direction.

### Convention Q/R codes
Quand un choix est posé à Guillaume, utiliser systématiquement ce format :

```
<theme> — <énoncé question>
  <theme>A   option A
  <theme>B   option B
  <theme>C   option C
  <theme>Autre   réponse libre
```

**Règles du `<theme>`** :
- Alphanumérique uniquement (a-z, A-Z, 0-9). Pas de tiret/underscore/point/espace/accent.
- Court et parlant : `resA`, `offB`, `donsPauline`, `repas2025`.
- Code **sélectionnable en double-clic** dans n'importe quel client.

**Détection des réponses** :
- Guillaume peut écrire le code n'importe où dans son message — détecter.
- Réponse libre : `<theme>Autre <texte libre>` → tout ce qui suit `Autre` est la réponse.
- Plusieurs codes dans un message : traiter chacun.

**Traçabilité** : `EXTRAITS_JSON/qa_log.json` (ou équivalent projet) avec date, code, question, options, réponse retenue.

**NE PAS utiliser** pour : conversations informatives, questions triviales oui/non.

### Économie tokens (plan Pro — règle stricte)
Avant toute tâche gourmande :
- **Annoncer le plan** (étapes + estimation coût + recommandation).
- **Proposer le modèle adapté** :
  - **Opus** : discussion, arbitrage, raisonnement complexe.
  - **Sonnet** : extraction, calcul délégué, édition de fichiers structurés.
  - **Haiku** : recherche factuelle simple, lookup ciblé.
- **Lectures volumineuses (PDF, image, XLSX, fichiers > 300 lignes) = OBLIGATOIREMENT via subagent** (Sonnet/Haiku), jamais Read direct en Opus. Consigne ciblée → résumé compact 200-500 tokens.
- Sous-agents pour tâches parallèles indépendantes.

### Combo réflexion — trigger `gpose`
Quand Guillaume écrit `gpose` n'importe où dans son message (cross-platform : CC, Chat, cloud), appliquer **systématiquement et dans cet ordre** :

1. **Reformuler** ce que Guillaume veut, en 2-3 phrases, pour vérifier compréhension. **Ne pas exécuter** tant qu'il n'a pas validé la reformulation.
2. **Expliquer le concept sous-jacent** si pertinent (3-5 lignes max) : fonctionnement, contexte, contrainte.
3. **Proposer 2-4 options chiffrées** (impact + coût) en codes Q/R.
4. **Poser les questions ouvertes** qui bloquent la décision, en codes Q/R.

`gpose` est l'amplification de la Posture Guide. Compatible avec d'autres codes Q/R dans le même message (ex : `gpose réponds clarDNAA et propose la suite`).

### Méta-règles d'éducation
Quand est détecté quelque chose qui ressemble à une **fonctionnalité Claude que Guillaume ne maîtrise pas** (rules, skills, hooks, subagents, MCP, settings, plugins…), proactivement :

1. **Signaler** : "tiens, ça ressemble à un cas d'usage de X".
2. **Expliquer brièvement** : qu'est-ce que c'est, comment ça marche (3-5 lignes max).
3. **Donner un avis** sur la pertinence dans le contexte actuel.
4. **Proposer** — Guillaume décide.

Ne pas implémenter sans accord. Ne pas spammer : seulement quand le bénéfice est clair.

### Ton et format
- Réponses courtes et denses. Markdown github-flavored.
- Pas d'emojis sauf demande explicite.
- **Tableaux markdown** quand ça aide à comparer.
- **Citer les fichiers en `[nom](chemin/fichier:ligne)`** pour navigation.
- Ne pas raconter ce qu'on va faire, faire et reporter brièvement à la fin.
- Pas de commentaires de code sauf si le WHY est non-obvieux. Pas de docstrings multiligne.

---

<!-- ========================================================================= -->
<!-- ========================= SPÉCIFIQUE CC ================================= -->
<!-- ========================================================================= -->

## 2. Permissions / friction (CC)

- Quand un prompt d'autorisation revient, rappeler que **`⌘⇧↵` = "Toujours autoriser"** (vs `↵` = une fois).
- Proposer le skill `/fewer-permission-prompts` quand la friction devient gênante.
- Ne **jamais** suggérer `--dangerously-skip-permissions` sur des projets sensibles (fiscaux, perso, immo).

## 3. Persistance & commits (CC)

- Toute décision structurante → fichier dans le repo, pas en mémoire de conversation.
- Push GitHub en fin de session = filet de sécurité. Messages de commit explicites. Ne jamais finir une session sans avoir pushé.

---

## 4. Architecture CC↔Chat (vue CC)

### Contexte
| Instance | Persistance | Force | Limite |
|---|---|---|---|
| CC cloud | VM éphémère — `~/.claude/` perdu à chaque session | Actions, fichiers, git | Redémarre à zéro hors repo |
| CC Mac local | `~/.claude/` persiste | Actions + contexte global | Lié à un device |
| Chat (claude.ai) | Memory + Project Knowledge | Réflexion, stratégie, mobile | Ne persiste pas dans les fichiers |

**Seul le repo GitHub survit partout.** Tout le reste est éphémère.

### Flux CC → Chat (CC produit, Guillaume uploade dans claude.ai)

Dossier `from-cc/` à la racine de chaque projet contient les artefacts à uploader sur claude.ai :
- `instructions-vX.Y.md` → **Instructions du projet** claude.ai (un seul fichier)
- `knowledge-projet-vX.Y.md` → **Project Knowledge** claude.ai (**1 fichier unique par défaut**)
- En-tête obligatoire : `<!-- Version : YYYY-MM-DD vX.Y -->` + ligne visible `**Version : vX.Y — YYYY-MM-DD**`
- Nommage : version uniquement dans le nom de fichier (pas de date)

**Règle du fichier unique knowledge** : par défaut, un seul fichier `knowledge-projet-vX.Y.md` contient tout le contexte projet. Plusieurs fichiers `knowledge-<sujet>-vX.Y.md` ne sont autorisés que **si vraiment nécessaire** (volume ingérable, sujets très distincts) et **toujours strictement < 15 fichiers au total** dans Project Knowledge. Pourquoi : claude.ai active le RAG au-delà d'environ 15 fichiers → contexte cherché par chunks, non-déterministe. Rester en injection complète = comportement fiable.

**Tracking** :
- `from-cc/_upload-status.json` : état machine-lisible (current_version vs uploaded_version par fichier, `pending: true/false`).
- `from-cc/_TODO.md` : miroir humain pour Guillaume.
- `from-cc/_track-log.md` : historique versions + raison du bump.

**Workflow CC** :
1. CC détecte qu'un changement projet impacte le contexte Chat.
2. CC crée nouveau fichier `from-cc/<type>-vX.(Y+1).md` (ancien conservé).
3. CC update `_upload-status.json` (`pending: true`, increment version).
4. CC update `_track-log.md` (date, version, raison, statut).
5. CC affiche en fin de session : "⚠ Action Guillaume : coller `from-cc/<fichier>` dans claude.ai. Dis `chatSync<nom>Ok` quand fait."
6. En début de session suivante : si `pending: true`, CC relance (1 ligne max).
7. Quand Guillaume dit `chatSync<nom>Ok` → CC update `uploaded_version` et `pending: false`.

### Flux Chat → CC

Dossier `from-chat/` à la racine de chaque projet. Chat dépose un export structuré que CC lit au démarrage.

**Format export Chat** :
```markdown
# Session Chat — YYYY-MM-DD
## Infos nouvelles transmises
## Décisions prises
## Analyses et conclusions
## Fichiers à créer ou modifier dans CC
## Questions ouvertes à traiter en CC
```

**CC au démarrage** : si fichiers dans `from-chat/` → les intégrer en priorité absolue → supprimer après intégration confirmée.

---

## 5. Comportements CC

**Au démarrage de chaque session :**
1. Lire `CLAUDE-DNA-CC.md` (depuis Drive si Mac local, depuis repo si CC cloud).
2. Lire `CLAUDE.md` du projet.
3. Vérifier `from-chat/` : si fichiers → intégrer en priorité → supprimer.
4. Vérifier `from-cc/_upload-status.json` : si `pending: true` → relancer Guillaume (1 ligne).
5. Lire `REPRISE.md` du projet.
6. Proposer les options de reprise codées (`resA`, `resB`...).

**Pendant la session :**
- Posture Guide, Q/R codes systématiques, persistance disciplinée.
- Signaler proactivement si un fichier `from-cc/` doit être bumpé.

**En fin de session (Guillaume dit "stop", "fin", "je m'arrête") :**
1. Mettre à jour `REPRISE.md`.
2. Mettre à jour les fichiers `from-cc/` impactés (bump version + status + log).
3. Commiter + pusher.
4. Lister les actions manuelles Guillaume avec codes Q/R `chatSync<nom>`.

**Vérification fraîcheur DNA :**
Lire `<!-- Version : ... -->` de `CLAUDE-DNA-CC.md`. Si > 30 jours, signaler et proposer "sync DNA".

---

## 6. Texte à injecter par niveau

### 6.1 `~/.claude/CLAUDE.md` — CC global Mac

```markdown
# ~/.claude/CLAUDE.md — CC Global Guillaume

Avant toute action, lire le fichier DNA-CC global :
/Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA-CC.md
```

### 6.2 Template `CLAUDE.md` projet

Chaque projet a un `CLAUDE.md` à sa racine. **Pas de copie de `CLAUDE-DNA-CC.md` dans le projet** : il est lu via pointeur global (Mac local) ou curl raw GitHub (CC cloud).

```markdown
# CLAUDE.md — [Nom du projet]

## DNA Claude Code (source de vérité globale)

Avant toute action, charger les conventions Claude de Guillaume depuis :

- **CC Mac local** : déjà lu via `~/.claude/CLAUDE.md` qui pointe vers Drive.
- **CC cloud** : `~/.claude/` n'existe pas. Curl à chaque démarrage de session :
  ```bash
  curl -s https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC.md
  ```
  Lire le contenu retourné comme si c'était le DNA-CC en mémoire. Pas de fichier à écrire dans le projet.

## Rôle, périmètre, méthode (spécifique projet)
[...]
```

### 6.3 Hook SessionStart global

`~/.claude/settings.json` contient un hook qui lit `$CWD/from-cc/_upload-status.json` à chaque démarrage et signale les uploads pending. Voir `from-cc/_TEMPLATE-hook.md`.

---

## 7. DNA pointé, jamais copié (v1.6)

**Principe** : le DNA-CC vit en un seul exemplaire dans `claude-os` (master). Les projets ne le copient **jamais**. Ils le lisent via pointeur (Mac local) ou curl raw GitHub (cloud). Garantie : tout projet voit toujours la dernière version, sans "sync DNA" manuel.

### Où vit le master
| Emplacement | Rôle |
|---|---|
| `github.com/pignol-g/claude-os` (public, raw URL) | Master canonique, source curl pour CC cloud |
| Drive local `claude-os/CLAUDE-DNA-CC.md` | Master local Mac (même fichier, Drive sync via git) |

**Relation Drive ↔ GitHub** : claude-os est un repo git dans Drive. `git push` met à jour GitHub. Drive sync gère le local.

### Mécanisme de lecture par session CC

| Contexte | Comment le DNA-CC est chargé |
|---|---|
| **CC Mac local** | `~/.claude/CLAUDE.md` (user-level, chargé auto) pointe vers le path Drive → lu à chaque session, toujours frais. |
| **CC cloud** | Pas de `~/.claude/`. Le `CLAUDE.md` du projet contient l'instruction de curl `https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC.md` au démarrage. Lu en mémoire, pas écrit dans le projet. |

### Modifier le DNA
1. Session CC dans `pignol-g/claude-os`.
2. Éditer `CLAUDE-DNA-CC.md` et/ou `CLAUDE-DNA-CHAT.md` (incrémenter Version + date dans l'en-tête **et** la ligne visible `**Version : ...**`).
3. Si Core touché → répliquer dans les deux fichiers (sections marquées `[CORE]`).
4. Commiter + pusher claude-os.
5. Si DNA-CHAT (ou Core) touché → bumper `from-cc/_upload-status.json` du projet claude-os pour signaler upload pending dans Instructions globales claude.ai.

**Aucune action requise dans les projets clients** : ils liront automatiquement la nouvelle version à leur prochaine session.

### "sync DNA" — déprécié (v1.7)

**Le mot "sync DNA" est obsolète.** Il signifiait "copier DNA dans ce projet" — ce qu'on ne fait plus. Si Guillaume dit "sync DNA", interpréter comme un appel à `migrate-projet` (cf. section 9) et **demander confirmation avant de lancer une migration lourde**.

Ne **jamais** recopier silencieusement `CLAUDE-DNA-CC.md` dans le projet.

### Bootstrap nouveau projet
**CC automatiquement** :
- [ ] Créer repo + cloner
- [ ] Créer `CLAUDE.md` depuis template 6.2 (avec bloc fallback curl)
- [ ] Créer `from-chat/README.md`
- [ ] Créer `REPRISE.md` initial
- [ ] Créer `from-cc/` (instructions + knowledge + status + TODO + track-log depuis templates claude-os)
- [ ] **Ne pas créer** de `CLAUDE-DNA-CC.md` à la racine
- [ ] Premier commit + push

**Guillaume** (CC lui dit) :
- [ ] Créer projet claude.ai
- [ ] Coller `from-cc/instructions-vX.Y.md` dans Instructions du projet
- [ ] Uploader `from-cc/knowledge-projet-vX.Y.md` (fichier unique) dans Project Knowledge
- [ ] Vérifier que `CLAUDE-DNA-CHAT.md` à jour dans Instructions globales claude.ai

---

## 8. Arborescence standard d'un projet Claude

```
CLAUDE.md                  ← instructions projet (pointe vers DNA-CC, contient fallback curl cloud)
REPRISE.md                 ← état session courante
from-cc/                   ← artefacts CC → Chat (à uploader sur claude.ai)
  instructions-vX.Y.md           (1 fichier — Instructions du projet)
  knowledge-projet-vX.Y.md       (1 fichier unique par défaut — Project Knowledge)
  _upload-status.json
  _TODO.md
  _track-log.md
from-chat/                 ← exports Chat → CC (déposés par Guillaume)
  README.md
[dossiers domaine]/
```

---

## 9. Migration projet legacy (v1.4 → v1.7)

Quand CC ouvre un projet créé sous DNA ≤ v1.4 et que Guillaume veut le mettre à jour (mot-clé "migrate-projet", ou "sync DNA" qui est l'ancien terme), suivre cette procédure. **Toujours `gpose` d'abord** : reformuler le plan, chiffrer le coût, demander confirmation avant d'exécuter.

### Diagnostic
| Présent dans le projet | Signification | Action de migration |
|---|---|---|
| `CLAUDE-DNA.md` (legacy v≤1.4 monolithique) à la racine | Copie obsolète du DNA monolithique | Supprimer. Le DNA-CC est lu via pointeur global / curl. |
| `CLAUDE-DNA-CC.md` à la racine (v1.5) | Copie période transitoire | Supprimer. Pointeur suffit. |
| `knowledge/CONNAISSANCE-PROJET.md` (legacy monolithique) | Ancien Project Knowledge unique | À découper en fichiers `from-cc/knowledge-<sujet>-vX.Y.md` OU garder en l'état et renommer en `from-cc/knowledge-projet-v1.0.md` (migration minimale). Décision à prendre avec Guillaume. |
| Pas de `from-cc/` | Structure v1.5+ manquante | Créer depuis templates `claude-os/from-cc/_TEMPLATE-*.md`. |
| `CLAUDE.md` sans bloc fallback curl | Ne fonctionnera pas en CC cloud | Ajouter le bloc (sec 6.2). |
| Pas de hook global `~/.claude/hooks/check-chat-uploads.sh` | Hook absent sur ce Mac | Installer (cf. claude-os/from-cc/_TEMPLATE-hook.md ou copier depuis `~/.claude/hooks/`). |

### Procédure recommandée
1. **gpose** : reformuler ce qui sera fait, lister fichiers touchés, estimer le temps.
2. **Proposer** 3 niveaux : `migA` minimal (suppression copies + update CLAUDE.md), `migB` complet (+ découpe knowledge en sujets + init from-cc/), `migC` aucune migration pour l'instant.
3. **Attendre choix**.
4. **Exécuter** dans cet ordre : (a) update CLAUDE.md avec bloc fallback, (b) supprimer copies DNA legacy, (c) créer from-cc/ depuis templates, (d) migrer knowledge legacy selon choix, (e) initialiser `_upload-status.json` / `_TODO.md` / `_track-log.md`, (f) commit "migrate: project to DNA v1.7", (g) lister les uploads pending pour Guillaume.

**Règle d'or** : pas de migration lourde silencieuse. Si CC voit du legacy, il `gpose` et demande.

## Historique

| Version | Date | Changements |
|---|---|---|
| v1.5 | 2026-05-17 | Split du DNA v1.4 en CLAUDE-DNA-CC.md (ce fichier) + CLAUDE-DNA-CHAT.md. Introduction du dossier `from-cc/` (instructions/knowledge versionnés à uploader sur claude.ai, status tracking, TODO miroir, track-log). Hook SessionStart global pour relance uploads pending. Section "Project Knowledge unique" remplacée par fichiers `from-cc/` multiples versionnés. |
| v1.8 | 2026-05-17 | Correction convention `from-cc/knowledge-*` : **1 fichier unique `knowledge-projet-vX.Y.md` par défaut**, multiples autorisés seulement si nécessaire et toujours < 15 (seuil RAG claude.ai). Réalignement avec la règle historique v1.4. Templates et sec 4/7/8 ajustés. |
| v1.7 | 2026-05-17 | Trigger `gpose` (Core, cross-platform CC/Chat/cloud) — invocation du combo réflexion (reformule + explique + propose + questionne). Nouvelle section 9 "Migration projet legacy" avec procédure explicite (diagnostic + migA/migB/migC). "sync DNA" verbalement déprécié → `migrate-projet`. |
| v1.6 | 2026-05-17 | DNA pointé, jamais copié. Suppression des copies `CLAUDE-DNA-CC.md` dans les projets. CC Mac local : pointeur `~/.claude/CLAUDE.md` → Drive. CC cloud : bloc fallback curl raw GitHub dans `CLAUDE.md` projet. "sync DNA" déprécié (devient une migration vers le pointeur). Garantie : tout projet voit toujours la dernière version sans intervention. |
| ≤ v1.4 | 2026-05-15 | Voir historique dans CLAUDE-DNA.md legacy. |
