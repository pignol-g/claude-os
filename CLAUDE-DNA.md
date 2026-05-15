# CLAUDE-DNA — Convention Claude de Guillaume Pignolet

<!-- MASTER FILE — Source de vérité unique pour tous les projets Claude de Guillaume -->
<!-- Version : 2026-05-15 v1.3 -->
<!-- GitHub canonique : github.com/pignol-g/claude-os — branche main (public) -->
<!-- Raw URL sync : https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA.md -->
<!-- Drive (chemin Mac réel) : /Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA.md -->
<!-- Note : claude-os est un repo git dans Drive — Drive sync = master local, GitHub = master cloud -->
<!--
  Ce fichier est l'ADN de la convention Claude de Guillaume.
  Il est agnostique à tout domaine et à tout projet.
  Toute instance Claude (CC ou Chat) qui le lit sait :
    — comment se comporter avec Guillaume
    — comment l'architecture CC↔Chat est câblée
    — comment initialiser ou synchroniser un projet
    — quoi injecter à chaque niveau (CC global, CLAUDE.md projet, Chat Memory, Project Knowledge)
-->

---

## 1. Convention Guillaume

### Posture Guide
Toujours proposer 2–3 options avec impact + coût avant d'exécuter. Attendre validation explicite de Guillaume sauf s'il dit "vas-y" ou équivalent. Ne jamais implémenter sans accord sur la direction.

### Convention Q/R codes
Proposer systématiquement les choix sous forme de codes copier-collables `<thème><lettre>` (ex : `resA`, `offB`, `visC`). Guillaume répond en un mot. Toujours lister les options avant de demander le code.

### Économie tokens (plan Pro)
Annoncer plan + estimation coût avant toute tâche lourde. Lectures volumineuses (PDF, image, XLSX, fichiers > 300 lignes) → subagent Sonnet/Haiku ciblé, jamais lecture directe en Opus. Sous-agents pour tâches parallèles indépendantes.

### Persistance disciplinée
Toute décision structurante → fichier dans le repo, pas en mémoire de conversation. La mémoire de conversation est volatile. Le repo GitHub est la vérité. Ce qui n'est pas commité n'existe pas.

### Commits fréquents
Push GitHub en fin de session = filet de sécurité. Messages de commit explicites. Référencer le lien de session Claude Code dans chaque commit body. Ne jamais finir une session sans avoir pushé.

### Ton et format
Réponses courtes et directes. Markdown github-flavored. Pas d'emojis sauf demande explicite. Pas de commentaires de code sauf si le WHY est non-obvieux. Pas de docstrings multiligne.

---

## 2. Architecture CC↔Chat — 3 couches

### Contexte du problème

| Instance | Persistance | Force | Limite |
|---|---|---|---|
| CC cloud (web) | VM éphémère — `~/.claude/` perdu à chaque session | Actions, fichiers, git | Redémarre à zéro hors repo |
| CC Mac local | `~/.claude/` persiste | Actions + contexte global | Lié à un device |
| Chat (claude.ai) | Memory + Project Knowledge | Réflexion, stratégie, mobile | Ne persiste pas dans les fichiers |

**Seul le repo GitHub survit partout et toujours.** Tout le reste est éphémère.

**Rythme typique Guillaume** : CC le matin pour actions → Chat en déplacement pour réflexion → CC le soir pour persistance.

---

### Couche 1 — Préférences globales dans le repo

**Principe** : les conventions Guillaume (ce fichier, CLAUDE-DNA.md) vivent dans le repo. CC cloud les charge automatiquement car le repo est cloné à chaque session.

**CC Mac local** : `~/.claude/CLAUDE.md` contient une seule instruction : "lire CLAUDE-DNA.md en premier" (chemin Drive). Voir section 4.1.

**CC cloud** : lit la copie de `CLAUDE-DNA.md` commitée à la racine du repo projet. Voir section 5.3 pour la synchronisation.

---

### Couche 2 — CC → Chat : Project Knowledge par projet

**Principe** : 1 fichier unique `knowledge/CONNAISSANCE-PROJET.md` par projet — exhaustif, structuré, uploadé dans la Project Knowledge du projet claude.ai correspondant. Zéro friction : 1 delete + 1 upload à chaque mise à jour.

**CC le maintient** via Edit diff-only (cheap). CC annonce dans la conversation quelles sections ont changé.

**Contenu type** : rôle Chat pour ce projet, périmètre, méthode complète, principes consolidés, index des items actifs, item actif exhaustif, état courant session, questions ouvertes.

**Quand mettre à jour** :
- Nouvel apprentissage ou principe → section méthode
- Paramètres projet changent → section périmètre
- Nouvel item actif ou avancement → section item actif + index
- Décisions / état session → section état courant

**CC dit à Guillaume quand uploader** : chaque fois que CONNAISSANCE-PROJET.md change, CC termine le commit avec "⚠ Action : uploader `knowledge/CONNAISSANCE-PROJET.md` dans Project Knowledge claude.ai (projet [nom])."

**Workflow upload Guillaume** : claude.ai → projet → Project Knowledge → supprimer l'ancienne version → uploader la nouvelle → 30 secondes.

---

### Couche 3 — Chat → CC : export de session

**Dossier** : `from-chat/` dans chaque repo projet.

**Chat génère** automatiquement un export structuré en fin de session dès que des infos nouvelles ont été transmises, des décisions prises, ou des analyses faites.

**Format export** (Chat doit générer exactement ceci) :

```markdown
# Session Chat — YYYY-MM-DD

## Infos nouvelles transmises par Guillaume
<!-- Ce que Guillaume a dit que CC ne sait pas encore -->

## Décisions prises
<!-- Choix actés pendant la session -->

## Analyses et conclusions
<!-- Raisonnements utiles à capitaliser -->

## Fichiers à créer ou modifier dans CC
<!-- Instructions explicites pour CC : quel fichier, quel contenu -->

## Questions ouvertes à traiter en CC
<!-- Points non résolus à reprendre -->
```

**Guillaume dépose** le fichier `.md` dans `from-chat/YYYY-MM-DD-session.md` du repo projet (via Drive sync ou éditeur).

**CC au démarrage** : si des fichiers existent dans `from-chat/` → les lire et intégrer avant toute action métier → supprimer après intégration confirmée.

---

## 3. Comportements attendus par instance

### Claude Code — tout projet

**Au démarrage de chaque session :**
1. Lire `CLAUDE-DNA.md` (depuis Drive si Mac local, depuis repo si CC cloud)
2. Lire `CLAUDE.md` du projet
3. Vérifier `from-chat/` : si des fichiers existent → les intégrer en priorité absolue → supprimer
4. Lire `REPRISE.md` du projet
5. Proposer les options de reprise codées (`resA`, `resB`...)

**Pendant la session :**
- Posture Guide : proposer avant d'exécuter
- Q/R codes systématiques
- Persistance disciplinée : toute décision → fichier commité
- Signaler proactivement si CONNAISSANCE-PROJET.md doit être uploadé

**En fin de session (Guillaume dit "stop", "fin", "je m'arrête") :**
1. Mettre à jour `REPRISE.md` (état actuel, questions ouvertes, options de reprise)
2. Mettre à jour `knowledge/CONNAISSANCE-PROJET.md` si état projet a changé
3. Commiter tous les changements + pusher
4. Lister les actions manuelles pour Guillaume :
   - Si CONNAISSANCE-PROJET.md a changé → "⚠ Uploader dans Project Knowledge claude.ai"
   - Si CLAUDE-DNA.md a changé → "⚠ Propager DNA (voir section 5.2)"

**Vérification fraîcheur DNA :**
Lire la ligne `<!-- Version : ... -->` de `CLAUDE-DNA.md` local. Si la date est > 30 jours, signaler : "DNA local daté du [date]. Veux-tu synchroniser depuis le master ? → dis 'sync DNA'."

---

### Claude Chat — tout projet

**Au démarrage de chaque session :**
1. Lire la Project Knowledge du projet (CONNAISSANCE-PROJET.md injecté automatiquement)
2. Annoncer en 1 phrase l'état courant : "[projet] — [item actif] — [statut]"
3. Si Project Knowledge inaccessible : le dire explicitement. Ne jamais improviser le contexte.
4. Appliquer immédiatement les conventions : Q/R codes, posture, raisonnement dans le cadre du projet

**Pendant la session :**
- Rester dans le rôle défini par CONNAISSANCE-PROJET.md
- Ne pas modifier de fichiers (c'est le rôle de CC)
- Signaler si une info nouvelle mérite d'être persistée : "Note pour l'export : [info]"

**En fin de session :**
Générer automatiquement l'export structuré (format section 2 couche 3) dès qu'une information utile a été échangée.
Rappeler : "Dépose ce fichier dans `from-chat/YYYY-MM-DD-session.md` du repo projet."

---

## 4. Texte exact à injecter par niveau

### 4.1 ~/.claude/CLAUDE.md — CC global Mac

```markdown
# ~/.claude/CLAUDE.md — CC Global Guillaume

Avant toute action, lire le fichier DNA global :
/Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA.md

Ce fichier contient toutes les conventions globales, l'architecture CC↔Chat,
et les comportements attendus pour tous les projets.
```

### 4.2 Template CLAUDE.md — racine de chaque projet

```markdown
# CLAUDE.md — [Nom du projet]

<!-- DNA : lire CLAUDE-DNA.md à la racine de ce repo avant ce fichier -->
<!-- Conventions globales (posture, Q/R, couches CC↔Chat) : voir CLAUDE-DNA.md -->

## Rôle
[Définir le rôle spécifique au domaine du projet]

## Périmètre et contraintes
[Règles métier, limites, paramètres fixes du projet]

## Méthode par tâche
[Référence à SKILL.md ou équivalent si applicable]

## Architecture repo
[Arborescence du projet avec description de chaque fichier clé]

## Comportements automatiques spécifiques
[Triggers et actions propres au domaine :
 - Si [signal X] → faire [action Y]
 - Si "reprise" → lire REPRISE.md + proposer options]

## Mémoire de session
[REPRISE.md tient l'état courant. Mettre à jour en fin de session.]
```

### 4.3 Chat Memory globale — texte à coller dans claude.ai → Paramètres → Mémoire

```
Je suis Guillaume Pignolet. Voici ma convention Claude.

POSTURE : propose 2-3 options codées (resA, resB...) avant d'agir. Attends ma validation.
CODES Q/R : toujours des codes copier-collables <thème><lettre>. Je réponds en un mot.
TOKENS : annonce le plan avant tâche lourde. Délègue les lectures lourdes.

ARCHITECTURE CC↔Chat :
- CC persiste dans le repo GitHub. Chat réfléchit. La vérité est dans le repo.
- En fin de session Chat : génère automatiquement un export structuré (infos nouvelles /
  décisions / analyses / fichiers à créer / questions ouvertes). Je le dépose dans from-chat/.
- Tu ne modifies pas de fichiers. CC s'en charge.

DÉBUT DE SESSION : lis la Project Knowledge du projet, annonce l'état en 1 phrase.
FIN DE SESSION : génère l'export Chat→CC automatiquement si infos utiles échangées.

DNA COMPLET : github.com/pignol-g/claude-os (public) — raw : https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA.md
Drive local : Drive/Claude/claude-os/CLAUDE-DNA.md
Je peux te le fournir en session (ou tu peux le fetcher via l'URL raw si web access activé).
```

### 4.4 Template knowledge/CONNAISSANCE-PROJET.md

Voir `templates/CONNAISSANCE-PROJET-template.md` dans le repo `pignol-g/claude-os`.

Structure minimale :
1. Rôle et comportements de l'assistant Chat pour ce projet
2. Périmètre et règles immuables
3. Méthode (synthèse des étapes clés)
4. Principes consolidés (apprentissages accumulés)
5. Index des items évalués/traités
6. Item actif détaillé (données complètes)
7. État courant — session en cours

---

## 5. Workflow de propagation — Option A (copie dans chaque repo)

### 5.1 Où vit le master

| Emplacement | Rôle | Mis à jour par |
|---|---|---|
| `github.com/pignol-g/claude-os` (public) | Master canonique + source sync CC cloud | CC (session claude-os) |
| `/Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA.md` | Master local Mac — même fichier, Drive sync git | Automatique via Drive sync + git push |
| `CLAUDE-DNA.md` à la racine de chaque repo projet | Copie projet | CC via commande "sync DNA" |

**Relation Drive ↔ GitHub** : claude-os est un repo git **dans Drive**. Drive sync gère la copie locale. `git push` depuis claude-os sur Mac met à jour GitHub. Les deux sont en sync automatiquement.

### 5.2 Modifier le DNA (processus complet)

CC fait tout ce qui est automatisable. Guillaume fait uniquement les actions signalées.

**Étapes CC (automatiques) :**
1. Ouvrir session CC dans repo `pignol-g/claude-os`
2. Éditer `CLAUDE-DNA.md` (incrémenter Version + date dans l'en-tête)
3. Commiter + pusher dans claude-os → Drive sync met à jour le fichier local automatiquement
4. Générer le texte mis à jour pour Chat Memory (section 4.3)
6. Lister les repos projets à synchroniser

**Actions Guillaume (manuelles) :**
- Coller le nouveau texte 4.3 dans claude.ai → Paramètres → Mémoire (si Chat Memory a changé)
- Dans chaque session projet CC concernée : dire "sync DNA"

### 5.3 Synchroniser une copie projet (Guillaume dit "sync DNA")

**Règle critique : la source de sync est TOUJOURS claude-os. Jamais depuis un autre projet.**
claude-os est public → curl sans auth fonctionne depuis CC cloud et CC Mac.

CC exécute automatiquement l'une des deux méthodes :

**Méthode 1 — curl depuis GitHub (CC cloud ou Mac, marche partout) :**
```bash
curl -s https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA.md > CLAUDE-DNA.md
git add CLAUDE-DNA.md
git commit -m "sync: update CLAUDE-DNA from canonical (claude-os)"
git push
```

**Méthode 2 — copie depuis Drive (Mac local uniquement, si hors ligne) :**
```bash
cp "/Users/pignolet/Library/CloudStorage/GoogleDrive-guillaume.pignolet25@gmail.com/Mon Drive/Claude/claude-os/CLAUDE-DNA.md" ./CLAUDE-DNA.md
git add CLAUDE-DNA.md
git commit -m "sync: update CLAUDE-DNA from Drive (claude-os)"
git push
```

**⚠ Ne jamais curl depuis `ClaudeAchatMaison` ou un autre repo projet** — ce sont des copies, pas le master. Même si un projet contient une version plus récente (ex : session de travail), elle doit d'abord être pushée dans claude-os avant d'être propagée ailleurs.

### 5.4 Bootstrap d'un nouveau projet (checklist complète)

**CC fait automatiquement :**
- [ ] Créer repo GitHub + cloner
- [ ] `curl` CLAUDE-DNA.md depuis claude-os (ou copie Drive)
- [ ] Créer `CLAUDE.md` depuis template 4.2 (adapter rôle + périmètre)
- [ ] Créer `from-chat/README.md` (template standard couche 3)
- [ ] Créer `REPRISE.md` initial (état vierge + options de reprise vides)
- [ ] Créer `knowledge/CONNAISSANCE-PROJET.md` depuis template 4.4
- [ ] Créer la structure de dossiers du projet
- [ ] Premier commit + push

**Guillaume fait (CC lui dit quand et quoi) :**
- [ ] Créer le projet dans claude.ai (si pas existant)
- [ ] Uploader `knowledge/CONNAISSANCE-PROJET.md` dans Project Knowledge du projet claude.ai
- [ ] Vérifier que Chat Memory globale (4.3) est à jour dans claude.ai → Paramètres → Mémoire

### 5.5 Vérification fraîcheur DNA au démarrage CC

CC lit la ligne `<!-- Version : YYYY-MM-DD vN -->` dans `CLAUDE-DNA.md` du projet.
Si la date est ancienne de plus de 30 jours :
> "CLAUDE-DNA.md local daté du [date]. Le master a peut-être évolué. Dis 'sync DNA' pour mettre à jour depuis claude-os, ou 'ignore DNA' pour continuer sans sync."

---

## 6. Arborescence standard d'un projet Claude

```
CLAUDE-DNA.md              ← copie du master (sync depuis pignol-g/claude-os)
CLAUDE.md                  ← instructions projet (référence CLAUDE-DNA.md)
REPRISE.md                 ← état session courante (mis à jour chaque fin de session)
knowledge/
  CONNAISSANCE-PROJET.md  ← fichier unique Project Knowledge Chat (remplacé à chaque update)
from-chat/
  README.md                ← format export Chat→CC
  [fichiers session]/      ← déposés par Guillaume, traités par CC au démarrage
[dossiers domaine]/        ← structure propre au projet
```

---

## 7. Pourquoi cette architecture — décisions actées

### Pourquoi les préférences vivent dans le repo et pas dans ~/.claude/
`~/.claude/` n'existe pas en CC cloud (VM éphémère). Seul le repo GitHub survit. Les préférences dans le repo = disponibles partout, toujours.

### Pourquoi Project Knowledge plutôt que connecteur Drive MCP
Le MCP Drive oblige Chat à appeler un outil pour lire chaque fichier (comportement aléatoire, coût ×N). La Project Knowledge injecte le fichier dans le contexte natif, déterministe, coût fixe payé une fois.

### Pourquoi 1 fichier CONNAISSANCE-PROJET.md et pas plusieurs
La Project Knowledge de claude.ai active le RAG automatiquement à partir d'environ 15 fichiers. Avec RAG, Claude ne "voit" pas tout — il cherche les chunks. Rester sous ce seuil = contexte complet injecté = comportement déterministe. 1 fichier remplacé = toujours la vérité courante, zéro ambiguïté.

### Pourquoi Chat ne persiste pas dans les fichiers
1. **Coût** : écriture via MCP Drive = lire + régénérer + réécrire = 3 opérations lourdes, 30–50 % d'une session.
2. **Fiabilité** : Chat peut décider de ne pas exécuter les instructions MCP selon le contexte. CC a des outils natifs déterministes (Edit = diff-only, cheap, fiable).

### Pourquoi Option A (copies) plutôt que submodule git
Les submodules git en CC cloud ne sont pas garantis (clone --recurse-submodules dépend de la config). Les copies + sync sont plus robustes et plus simples à déboguer. La commande "sync DNA" couvre le besoin de mise à jour.

### Pourquoi la Chat Memory globale est du texte court et non un fichier
claude.ai ne supporte pas l'upload de fichiers au niveau utilisateur global — uniquement du texte dans la mémoire. Les fichiers s'uploadent uniquement par projet dans Project Knowledge. Le texte court en Memory = behaviors universels. Le fichier en Project Knowledge = contexte projet complet.

---

## Historique des versions

| Version | Date | Changements |
|---|---|---|
| v1 | 2026-05-15 | Création initiale — extrait et généralisé depuis CLAUDE.md ClaudeAchatMaison |
| v1.1 | 2026-05-15 | Chemins Drive Mac réels intégrés. Décision actée : claude-os public. Chat Memory raccourcie (path court). |
| v1.2 | 2026-05-15 | claude-os confirmé repo git dans Drive. Chemins corrigés (claude-os/CLAUDE-DNA.md). Raw URL GitHub ajoutée. Section 5.1 clarifiée (Drive sync automatique via git). Chat Memory : URL raw pour fetch manuel. |
| v1.3 | 2026-05-15 | Copie racine Drive/Claude/CLAUDE-DNA.md supprimée (redondante). Règle sync 5.3 clarifiée : source = claude-os uniquement, jamais depuis un projet. Avertissement curl repo privé documenté. |
