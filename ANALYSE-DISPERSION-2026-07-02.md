# Analyse dispersion + réorganisation Asana — 2026-07-02 (passe gauto)

> Demande Guillaume : « Analyse ma façon de me disperser et réorganise si besoin les tâches dans Claude. »
> Périmètre observé : projet Asana **« Claude »** (64 tâches, 50 ouvertes) + les 22 PR ouvertes des repos.

## 1. Ce que je vois — la dispersion en 3 motifs

### Motif A — « Démarrer beaucoup, clôturer peu » (le plus coûteux)
**22 PR ouvertes, dont ~20 dormantes.** Chaque passe (asana-pass, nocturne) ouvre une branche + une PR draft… qui n'est jamais mergée ni fermée. Résultat : les PR **vieillissent et entrent en conflit entre elles** (plusieurs éditent `cibles-compagnies.json`, `sources.yaml`, le CORE). Le travail est bon ; c'est la **sortie** qui manque. → cf `TRIAGE-PR-2026-07-02.md`.

### Motif B — « L'outil mange l'objectif » (méta vs métier)
Sur les 8 PR claude-os ouvertes, **8/8 sont du méta-outillage** : gauto, gpose, audit-DNA, anti-interruption, routine-credit, découpage crédit, R&D résilience, persistance… Beaucoup se recouvrent (3 PR différentes tournent autour de « survivre à l'extinction crédit »). Pendant ce temps, l'objectif réel — **postuler** — avance peu : le CV maître n'est toujours pas calé/validé (bloque le 1er vrai dossier), et aucune LM n'est partie récemment.
> Ce n'est pas un reproche : construire l'atelier est utile. Mais l'atelier ne doit pas devenir le projet. **Règle proposée : max 2 chantiers méta “actifs” à la fois.**

### Motif C — « Tout dans le même seau, trié jamais »
Le projet « Claude » est ton **inbox de délégation** (tâche *amorce question* : tu y déposes des questions à traiter async — c'est un bon réflexe). Mais **rien ne distingue** :
- les **questions déléguées** (Rapport coût maison, Babea lait, Clé démembrement, Vivinter…),
- le **méta-outillage** (skills, DNA, routines),
- les **actions pilote** (candidatures, veille, alertes).

Tout cohabite dans `a travailler Guillaume` / `à lire / valider`, qui deviennent des fourre-tout. Deux exemples concrets :
- Les **16 tâches « Alerte mail — <compagnie> »** (déjà répondues, avec URL vérifiée) traînent en top-level dans « Section sans nom » : ce sont des **sous-résultats** de la tâche #131 « Activer les alertes mail par compagnie », pas des tâches à part.
- La section **« à lire / valider »** mélange du **vraiment traité** (à archiver) et des **méta-tâches encore ouvertes** (Skill gauto/gpose/deep-search, Auditer DNA…) qui ne sont que des stubs pointant une PR.

## 2. Réorganisation proposée du projet « Claude » (prête à appliquer)

Redéfinir les sections par **type de travail** (au lieu des libellés actuels ambigus) :

| Section cible | Contenu | Vient de |
|---|---|---|
| 📥 **Entrée — à traiter** | Questions/tâches déléguées non commencées | `pour claude` + délégations éparses |
| 🔧 **Méta — outillage Claude** | Skills, DNA, routines, hooks | méta-tâches de `à lire/valider` + `a travailler` |
| ✈️ **Pilote — actions** | Candidatures, veille, alertes (ou → projet **Pilote**) | tâches pilote de `a travailler` |
| 👀 **À relire / valider (Claude a fini)** | Uniquement le **réellement traité** | purge de `à lire/valider` |
| 📦 **Archive** | Terminé + lu | tâches complétées |

**Actions de rangement recommandées** (je ne les exécute pas seul — tu clôtures/déplaces en masse) :
1. **Convertir en sous-tâches de #131** les 16 « Alerte mail — <compagnie> » (ou les archiver : elles sont répondues).
2. **Fermer** les stubs méta dont la PR est tranchée : *Skill gauto* (#171) et *Skill gpose* (#170) → PR #20 **mergée** ✅ (voir mes commentaires). *Auditer DNA* / *Skill pass-asana* → répondu par PR #14/#18.
3. **Regrouper** sous UNE tâche parente « Résilience / crédit » les doublons : #135 (découpage), #168 (routine-credit), + R&D #13. Aujourd'hui = 3 fils pour un seul sujet.
4. **Router hors « Claude »** si tu préfères des projets dédiés : *Rapport coût maison* → **maison Meximieux** / achatmaison ; *Vivinter* → **Vie/Santé** ; *Clé démembrement* → **Finance** ; *Babea lait / barrière Charlie* → **Bébé** ; *Décompte Rhône express* → **Quotidien**. (Si « Claude » est ton inbox de délégation volontaire, garde-les — mais alors sépare-les dans 📥 Entrée.)
5. **Nettoyer les projets vides doublons** : `TOEIC`, `FCL055`, `Ryanair`, `Anglais` (0 tâche) recoupent des sections du projet Pilote.

## 3. La seule règle qui casse les 3 motifs

> **Cadence de sortie.** Toute PR / tâche déléguée se **merge ou se ferme sous 72 h**. Une passe autonome ne s'autorise une **nouvelle** branche que si elle a d'abord **fait avancer vers la fermeture** une branche existante. Et : **une seule PR ouverte par fichier chaud** (CORE, `cibles-compagnies.json`, `sources.yaml`).

C'est la contre-mesure directe des motifs A (clôturer) et B (plafond méta), et ça garde l'inbox (motif C) vivable parce qu'elle se vide.

---
*Passe gauto autonome — 2026-07-02. Détails PR : `TRIAGE-PR-2026-07-02.md`.*
