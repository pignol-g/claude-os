# CLAUDE-DNA-CC-REF — Procédures rares (cold)

**Version : v2.1 — 2026-06-13** (renommage dossiers échange `to-<destination>/` + flux `to-os/`)

<!-- Procédures cold : lues à la demande quand un trigger du sommaire CORE est rencontré. -->
<!-- Version : 2026-05-19 v2.0 -->
<!-- GitHub : github.com/pignol-g/claude-os — branche main (public) -->
<!-- Raw URL : https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-REF.md -->
<!-- Référencé depuis : CLAUDE-DNA-CC-CORE.md (sommaire en section 5) -->

Table des matières (ancres) :
- [archi-cc-chat](#archi-cc-chat)
- [comportements-cc-details](#comportements-cc-details)
- [templates](#templates)
- [dna-pointe](#dna-pointe)
- [bootstrap](#bootstrap)
- [arborescence](#arborescence)
- [migrate-projet](#migrate-projet)
- [historique](#historique)

---

<a id="archi-cc-chat"></a>
## Architecture CC↔Chat (vue CC)

### Contexte
| Instance | Persistance | Force | Limite |
|---|---|---|---|
| CC cloud | VM éphémère — `~/.claude/` perdu à chaque session | Actions, fichiers, git | Redémarre à zéro hors repo |
| CC Mac local | `~/.claude/` persiste | Actions + contexte global | Lié à un device |
| Chat (claude.ai) | Memory + Project Knowledge | Réflexion, stratégie, mobile | Ne persiste pas dans les fichiers |

**Seul le repo GitHub survit partout.** Tout le reste est éphémère.

### Convention de nommage des dossiers d'échange : `to-<destination>/`

Les dossiers d'échange sont nommés **par destinataire**, pas par émetteur. Principe : une
boîte d'envoi est **absolue** (« destiné à X ») et lisible identiquement depuis n'importe
quel conteneur — quand Guillaume arrive quelque part, une seule question : *« qu'y a-t-il
dans `to-<ici>` à faire rentrer ? »*. (Renommage 2026-06-13 ; ex-noms `from-cc/` /
`from-chat/` par émetteur, ambigus selon le conteneur.)

| Dossier | Ex-nom | Produit par | Destination (consommateur) | Cycle de vie |
|---|---|---|---|---|
| `to-chat/` | `from-cc/` | CC | Chat (upload manuel Guillaume) | **persistant + versionné** |
| `to-cc/` | `from-chat/` | Chat (collé par Guillaume) | CC (lu au démarrage) | **éphémère** (supprimé après intégration) |
| `to-os/` | *(nouveau)* | CC/Guillaume dans un projet client | repo `claude-os` (l'OS / le DNA) | **éphémère** (supprimé après remontée) |

### Flux CC → Chat (CC produit, Guillaume uploade dans claude.ai)

Dossier `to-chat/` à la racine de chaque projet contient les artefacts à uploader sur claude.ai :
- `instructions-vX.Y.md` → **Instructions du projet** claude.ai (un seul fichier)
- `knowledge-projet-vX.Y.md` → **Project Knowledge** claude.ai (**1 fichier unique par défaut**)
- En-tête obligatoire : `<!-- Version : YYYY-MM-DD vX.Y -->` + ligne visible `**Version : vX.Y — YYYY-MM-DD**`
- Nommage : version uniquement dans le nom de fichier (pas de date)

**Règle du fichier unique knowledge** : par défaut, un seul fichier `knowledge-projet-vX.Y.md` contient tout le contexte projet. Plusieurs fichiers `knowledge-<sujet>-vX.Y.md` ne sont autorisés que **si vraiment nécessaire** (volume ingérable, sujets très distincts) et **toujours strictement < 15 fichiers au total** dans Project Knowledge. Pourquoi : claude.ai active le RAG au-delà d'environ 15 fichiers → contexte cherché par chunks, non-déterministe. Rester en injection complète = comportement fiable.

**Tracking** :
- `to-chat/_upload-status.json` : état machine-lisible (current_version vs uploaded_version par fichier, `pending: true/false`).
- `to-chat/_TODO.md` : miroir humain pour Guillaume.
- `to-chat/_track-log.md` : historique versions + raison du bump.

**Workflow CC** :
1. CC détecte qu'un changement projet impacte le contexte Chat.
2. CC crée nouveau fichier `to-chat/<type>-vX.(Y+1).md` (ancien conservé).
3. CC update `_upload-status.json` (`pending: true`, increment version).
4. CC update `_track-log.md` (date, version, raison, statut).
5. CC affiche en fin de session : "⚠ Action Guillaume : coller `to-chat/<fichier>` dans claude.ai. Dis `chatSync<nom>Ok` quand fait."
6. En début de session suivante : si `pending: true`, CC relance (1 ligne max).
7. Quand Guillaume dit `chatSync<nom>Ok` → CC update `uploaded_version` et `pending: false`.

### Flux Chat → CC

Dossier `to-cc/` à la racine de chaque projet. Chat dépose un export structuré que CC lit au démarrage.

**Format export Chat** :
```markdown
# Session Chat — YYYY-MM-DD
## Infos nouvelles transmises
## Décisions prises
## Analyses et conclusions
## Fichiers à créer ou modifier dans CC
## Questions ouvertes à traiter en CC
```

**CC au démarrage** : si fichiers dans `to-cc/` → les intégrer en priorité absolue → supprimer après intégration confirmée.

### Flux projet → OS (remontée DNA)

Dossier `to-os/` à la racine d'un projet **client** (jamais dans claude-os lui-même). Y déposer
ce qui doit remonter dans le repo `claude-os` : conventions généralisables, règles candidates
au CORE, corrections du DNA repérées en projet.

- **Produit par** : CC (ou Guillaume) dans le projet client, quand un pattern mérite d'être promu.
- **Ingestion (osIngestA — manuelle)** : Guillaume copie le fichier du `to-os/` du projet vers
  une session `claude-os`, qui l'intègre au DNA (CORE/REF/CHAT selon le cas) puis **supprime**
  le fichier source. Symétrique de l'upload Chat manuel — pas de lecture cross-repo automatique.
- **Cycle de vie** : éphémère. Une fois remonté et acté dans le DNA, supprimer.

---

<a id="comportements-cc-details"></a>
## Comportements CC — détails

(La séquence condensée est dans CORE §4. Cette section donne les cas limites.)

- **`to-cc/` vide** : ne rien dire, passer à l'étape suivante.
- **`to-cc/` contient `.DS_Store` ou README** : les ignorer, ne traiter que les `.md` hors README.
- **`to-chat/_upload-status.json` absent** : signaler une seule fois à Guillaume + proposer création depuis template.
- **Dossiers legacy `from-cc/`/`from-chat/` présents** : projet non migré → signaler une fois + proposer `migrate-projet` ([#migrate-projet](#migrate-projet)). Pendant la transition, les traiter comme leurs équivalents `to-chat/`/`to-cc/`.
- **`REPRISE.md` absent** : proposer création + reprise sur état courant du repo (`git status`, derniers commits).
- **DNA > 30 jours** : signaler en début de session, **ne pas bloquer**. "sync DNA" = en réalité une migration (cf. [#migrate-projet](#migrate-projet)).
- **Hook session-start.sh** : si DNA-CC introuvable (local absent + curl échoué), le hook affiche un warning et la session démarre sans DNA injecté — comportement non-déterministe à signaler à Guillaume.

---

<a id="templates"></a>
## Templates par niveau

### `~/.claude/CLAUDE.md` — CC global Mac

```markdown
# ~/.claude/CLAUDE.md — CC Global Guillaume

Avant toute action, lire le fichier DNA-CC-CORE global :
/Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA-CC-CORE.md

Si une procédure rare est nécessaire (bootstrap, migration, archi détaillée…), curl :
https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-REF.md
```

### Template `CLAUDE.md` projet

Chaque projet a un `CLAUDE.md` à sa racine. **Pas de copie de DNA dans le projet** — pointeur global (Mac local) ou curl raw GitHub (CC cloud).

```markdown
# CLAUDE.md — [Nom du projet]

## DNA Claude Code (source de vérité globale)

Avant toute action, charger les conventions Claude de Guillaume :

- **CC Mac local** : déjà chargé via `~/.claude/CLAUDE.md` qui pointe vers Drive.
- **CC cloud** : `~/.claude/` n'existe pas. Le hook `.claude/hooks/session-start.sh` charge le CORE automatiquement. En fallback manuel :
  ```bash
  curl -s https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-CORE.md
  ```

## Rôle, périmètre, méthode (spécifique projet)
[...]
```

### Hook SessionStart projet (v2.0)

Chaque projet contient `.claude/settings.json` + `.claude/hooks/session-start.sh` commités. Le hook :

1. **Charge `CLAUDE-DNA-CC-CORE.md`** dans le contexte CC (stdout injecté en SessionStart) — local si présent, sinon curl raw GitHub. Garantit que les règles actives sont lues **partout, même en CC cloud**.
2. **Vérifie `to-chat/_upload-status.json`** : signale les uploads Chat pending.
3. **Termine par une ligne marqueur** : `✓ DNA-CC-CORE chargé (source, version). REF accessible via sommaire. [pending ou aucun]`.

Référence d'implémentation : `claude-os/.claude/hooks/session-start.sh` (à copier dans chaque projet au bootstrap).

**Pourquoi pas un hook global `~/.claude/settings.json` ?** `~/.claude/` n'existe pas en CC cloud (VM éphémère). Le hook projet est commité dans le repo → cloné par cloud → exécuté.

---

<a id="dna-pointe"></a>
## DNA pointé, jamais copié (v1.6+)

**Principe** : le DNA-CC vit en un seul exemplaire dans `claude-os` (master). Les projets ne le copient **jamais**. Ils le lisent via pointeur (Mac local) ou curl raw GitHub (cloud). Garantie : tout projet voit toujours la dernière version, sans "sync DNA" manuel.

Depuis v2.0, le DNA est **splité** en deux fichiers complémentaires :
- `CLAUDE-DNA-CC-CORE.md` — règles actives, ~150 lignes, injecté à chaque session par le hook.
- `CLAUDE-DNA-CC-REF.md` (ce fichier) — procédures rares, ~450 lignes, curl à la demande.

### Où vit le master
| Emplacement | Rôle |
|---|---|
| `github.com/pignol-g/claude-os` (public, raw URL) | Master canonique, source curl pour CC cloud |
| Drive local `claude-os/CLAUDE-DNA-CC-CORE.md` + `CLAUDE-DNA-CC-REF.md` | Master local Mac (même fichiers, Drive sync via git) |

**Relation Drive ↔ GitHub** : claude-os est un repo git dans Drive. `git push` met à jour GitHub. Drive sync gère le local.

### Mécanisme de lecture par session CC

| Contexte | Comment le DNA-CC est chargé |
|---|---|
| **CC Mac local** | Hook projet `.claude/hooks/session-start.sh` lit CORE local (si présent) ou curl. `~/.claude/CLAUDE.md` peut aussi pointer vers le Drive. |
| **CC cloud** | Pas de `~/.claude/`. Hook projet (commité dans le repo) lit CORE via curl raw GitHub au démarrage. REF curlé à la demande. |

### Modifier le DNA
1. Session CC dans `pignol-g/claude-os`.
2. Éditer `CLAUDE-DNA-CC-CORE.md` et/ou `CLAUDE-DNA-CC-REF.md` (incrémenter Version + date dans l'en-tête **et** la ligne visible `**Version : ...**`).
3. Si Core touché → répliquer dans `CLAUDE-DNA-CHAT.md` (sections marquées `[CORE]`).
4. Commiter + pusher claude-os.
5. Si DNA-CHAT (ou Core) touché → bumper `to-chat/_upload-status.json` du projet claude-os pour signaler upload pending dans Instructions globales claude.ai.

**Aucune action requise dans les projets clients** : ils liront automatiquement la nouvelle version à leur prochaine session.

### "sync DNA" — déprécié (depuis v1.7)

**Le mot "sync DNA" est obsolète.** Il signifiait "copier DNA dans ce projet" — ce qu'on ne fait plus. Si Guillaume dit "sync DNA", interpréter comme un appel à `migrate-projet` (cf. [#migrate-projet](#migrate-projet)) et **demander confirmation avant de lancer une migration lourde**.

Ne **jamais** recopier silencieusement le DNA dans un projet.

### Backward compat v1.x (depuis v2.0)

`CLAUDE-DNA-CC.md` à la racine du master existe encore comme **fichier redirect** ("ce DNA est splité, voir CORE et REF"). Les hooks projet anciens (DNA_URL pointant vers `CLAUDE-DNA-CC.md`) continuent de fonctionner pendant la migration progressive : ils chargent un fichier court qui réoriente CC vers CORE+REF. À retirer une fois tous les projets clients passés à `DNA_URL=…CORE.md`.

---

<a id="bootstrap"></a>
## Bootstrap nouveau projet

**CC automatiquement** :
- [ ] Créer repo + cloner
- [ ] Créer `CLAUDE.md` depuis template ([#templates](#templates)) avec bloc fallback curl pointant vers CORE
- [ ] Créer `to-cc/README.md`
- [ ] Créer `REPRISE.md` initial
- [ ] Créer `to-chat/` (instructions + knowledge + status + TODO + track-log depuis templates claude-os)
- [ ] Créer `to-os/` (avec `README.md`) — boîte de remontée vers claude-os
- [ ] Créer `.claude/settings.json` + `.claude/hooks/session-start.sh` (copie depuis `claude-os/.claude/`) → hook SessionStart projet
- [ ] **Ne pas créer** de `CLAUDE-DNA-CC*.md` à la racine
- [ ] Premier commit + push

**Guillaume** (CC lui dit) :
- [ ] Créer projet claude.ai
- [ ] Coller `to-chat/instructions-vX.Y.md` dans Instructions du projet
- [ ] Uploader `to-chat/knowledge-projet-vX.Y.md` (fichier unique) dans Project Knowledge
- [ ] Vérifier que `CLAUDE-DNA-CHAT.md` à jour dans Instructions globales claude.ai

---

<a id="arborescence"></a>
## Arborescence standard d'un projet Claude

```
CLAUDE.md                  ← instructions projet (pointe vers DNA-CC-CORE, contient fallback curl cloud)
REPRISE.md                 ← état session courante
.claude/                   ← config CC projet (commitée)
  settings.json                  (déclare le hook SessionStart)
  hooks/session-start.sh         (charge DNA-CC-CORE + check to-chat, marche cloud + local)
to-chat/                   ← artefacts CC → Chat (à uploader sur claude.ai)
  instructions-vX.Y.md           (1 fichier — Instructions du projet)
  knowledge-projet-vX.Y.md       (1 fichier unique par défaut — Project Knowledge)
  _upload-status.json
  _TODO.md
  _track-log.md
to-cc/                     ← exports Chat → CC (déposés par Guillaume)
  README.md
to-os/                     ← remontées projet → claude-os (déposées par CC/Guillaume, copiées à la main vers l'OS)
  README.md
[dossiers domaine]/
```

---

<a id="migrate-projet"></a>
## Migration projet legacy (v≤1.4 / v1.5-1.9 → v2.0, + renommage dossiers v2.5)

Quand CC ouvre un projet créé sous DNA ≤ v2.4 et que Guillaume veut le mettre à jour (mot-clé `migrate-projet`, ou "sync DNA" qui est l'ancien terme), suivre cette procédure. **Toujours `gpose` d'abord** : reformuler le plan, chiffrer le coût, demander confirmation avant d'exécuter.

### Diagnostic
| Présent dans le projet | Signification | Action de migration |
|---|---|---|
| `CLAUDE-DNA.md` (legacy v≤1.4 monolithique) à la racine | Copie obsolète du DNA monolithique | Supprimer. DNA-CC lu via pointeur global / curl. |
| `CLAUDE-DNA-CC.md` à la racine (v1.5-1.9) | Copie période transitoire | Supprimer. Pointeur suffit. |
| `knowledge/CONNAISSANCE-PROJET.md` (legacy monolithique) | Ancien Project Knowledge unique | À découper en `to-chat/knowledge-<sujet>-vX.Y.md` OU garder en l'état et renommer en `to-chat/knowledge-projet-v1.0.md` (migration minimale). Décision à prendre avec Guillaume. |
| `from-cc/` et/ou `from-chat/` à la racine (v≤2.4) | Nommage par émetteur, pré-v2.5 | `git mv from-cc to-chat` + `git mv from-chat to-cc` (historique préservé). Créer `to-os/README.md`. Mettre à jour le hook (voir ligne suivante). |
| Hook `session-start.sh` référençant `from-cc`/`from-chat` | Hook pré-v2.5 | Remplacer par la version claude-os (check `to-chat/_upload-status.json`). |
| Pas de `to-chat/` (ni `from-cc/`) | Structure d'échange manquante | Créer depuis templates `claude-os/to-chat/_TEMPLATE-*.md` + `to-cc/README.md` + `to-os/README.md`. |
| `CLAUDE.md` sans bloc fallback curl | Ne fonctionnera pas en CC cloud | Ajouter le bloc (cf. [#templates](#templates)). |
| Hook projet absent ou pointant vers ancien `CLAUDE-DNA-CC.md` | Setup v1.9 ou plus ancien | Copier `.claude/settings.json` + `.claude/hooks/session-start.sh` depuis claude-os ; mettre à jour `DNA_URL` vers CORE. |

### Procédure recommandée
1. **gpose** : reformuler ce qui sera fait, lister fichiers touchés, estimer le temps.
2. **Proposer** 3 niveaux :
   - `migA` minimal — suppression copies DNA legacy + update CLAUDE.md.
   - `migB` complet — `migA` + découpe knowledge en sujets + init `from-cc/` + hook projet v2.0.
   - `migC` aucune migration pour l'instant.
3. **Attendre choix**.
4. **Exécuter** dans cet ordre : (a) update `CLAUDE.md` avec bloc fallback CORE, (b) supprimer copies DNA legacy, (c) renommer dossiers d'échange (`git mv from-cc to-chat`, `git mv from-chat to-cc`) ou les créer depuis templates si absents, (d) créer `to-os/README.md`, (e) migrer knowledge legacy selon choix, (f) initialiser/migrer `_upload-status.json` / `_TODO.md` / `_track-log.md` dans `to-chat/`, (g) installer `.claude/hooks/session-start.sh` à jour (DNA_URL → CORE, check `to-chat/`), (h) commit "migrate: project to DNA v2.5 (dossiers to-*)", (i) lister les uploads pending pour Guillaume.

**Renommage seul (projet déjà en v2.0+)** : si le seul écart est `from-cc`/`from-chat`, faire uniquement (c) + (d) + (g) + commit `migrate: dossiers to-* (v2.5)`.

**Règle d'or** : pas de migration lourde silencieuse. Si CC voit du legacy, il `gpose` et demande.

---

<a id="historique"></a>
## Historique

| Version | Date | Changements |
|---|---|---|
| v2.1 (REF) / v2.5 (CORE) | 2026-06-13 | **Renommage des dossiers d'échange par destinataire** : `from-cc/`→`to-chat/`, `from-chat/`→`to-cc/` (via `git mv`, historique préservé). Nouveau `to-os/` (remontées projet → claude-os, ingestion manuelle osIngestA). Driver : `to-<destination>/` est absolu et lisible depuis n'importe quel conteneur (« qu'y a-t-il dans `to-<ici>` à faire rentrer ? »), vs `from-*` ambigu selon le conteneur. `migrate-projet` étendu pour migrer les projets clients (détection `from-*` + hook legacy). Transition : CORE/REF nomment les deux le temps de la bascule. |
| v2.0 | 2026-05-19 | **Split DNA-CC en CORE + REF** (hot/cold split). `CLAUDE-DNA-CC-CORE.md` (~150 lignes, règles actives, injecté à chaque session par le hook) + `CLAUDE-DNA-CC-REF.md` (ce fichier, ~450 lignes, procédures rares curlées à la demande via sommaire CORE §5). Driver : coût d'injection répétée par le hook v1.9 (~12k tokens/session). Pattern : hot/cold + index lazy-fetch via ancres `#archi-cc-chat`, `#templates`, `#dna-pointe`, `#bootstrap`, `#arborescence`, `#migrate-projet`, `#historique`. `CLAUDE-DNA-CC.md` legacy conservé comme redirect stub (compatA — migration progressive des hooks projet). `CLAUDE-DNA-CHAT.md` reste monolithique (splitChatB — pas de hook côté claude.ai, pas de gain tokens). |
| v1.9 | 2026-05-18 | Hook SessionStart **projet** (commité dans `.claude/`) remplace le hook global Mac. Charge DNA-CC en contexte CC (stdout injecté) + check from-cc + marqueur final. Marche en CC cloud (le hook global ne marchait pas car `~/.claude/` éphémère en cloud). |
| v1.8 | 2026-05-17 | Correction convention `from-cc/knowledge-*` : **1 fichier unique `knowledge-projet-vX.Y.md` par défaut**, multiples autorisés seulement si nécessaire et toujours < 15 (seuil RAG claude.ai). Réalignement avec la règle historique v1.4. |
| v1.7 | 2026-05-17 | Trigger `gpose` (Core, cross-platform CC/Chat/cloud) — invocation du combo réflexion (reformule + explique + propose + questionne). Section "Migration projet legacy" avec procédure explicite (diagnostic + migA/migB/migC). "sync DNA" verbalement déprécié → `migrate-projet`. |
| v1.6 | 2026-05-17 | DNA pointé, jamais copié. Suppression des copies `CLAUDE-DNA-CC.md` dans les projets. CC Mac local : pointeur `~/.claude/CLAUDE.md` → Drive. CC cloud : bloc fallback curl raw GitHub dans `CLAUDE.md` projet. "sync DNA" déprécié. Garantie : tout projet voit toujours la dernière version sans intervention. |
| v1.5 | 2026-05-17 | Split du DNA v1.4 en CLAUDE-DNA-CC.md + CLAUDE-DNA-CHAT.md. Introduction du dossier `from-cc/` (instructions/knowledge versionnés à uploader sur claude.ai, status tracking, TODO miroir, track-log). Hook SessionStart global pour relance uploads pending. |
| ≤ v1.4 | 2026-05-15 | Voir historique dans CLAUDE-DNA.md legacy. |
