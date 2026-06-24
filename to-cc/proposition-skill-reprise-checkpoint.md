# Proposition — skill `reprise-checkpoint` (parade anti-interruption token)

> Statut : **proposition de technique** (à valider par Guillaume avant build).
> Origine : tâche Asana « Veille candidature » (projet Claude). Objectif demandé :
> en cas d'interruption (token, coupure, fin de session), **reprendre la tâche
> longue exactement là où elle s'est arrêtée**, via une **skill** réutilisable
> dans tous les repos (claude-os, candidaturePilote, ClaudeAchatMaison).

## 1. Principe (ce qu'on avait déjà fait, formalisé en skill)

La technique éprouvée = **plan très détaillé → suivi du plan → reprise après la
dernière étape cochée**. On la rend systématique et portable :

1. **Découper** la tâche longue en **étapes atomiques** — chacune assez petite
   pour tenir dans un budget token confortable ET committable seule
   (ex. veille : *1 fiche compagnie = 1 étape*).
2. **Écrire le plan** dans un fichier de suivi versionné, avec une case à cocher
   par étape + un pointeur « PROCHAINE ACTION ».
3. **Checkpoint après chaque étape** : cocher la case **et faire un commit git**.
   → l'historique git devient le journal réel ; le `.md` est l'index lisible.
4. **Reprise à froid** : à l'invocation, la skill lit le fichier, trouve la
   **première case non cochée** et repart de là — sans avoir besoin du contexte
   de la session précédente.

## 2. Format du fichier de suivi

Emplacement proposé : `.reprise/<slug-tache>.md` à la racine du repo concerné
(un dossier dédié, git-trackable, qui ne pollue pas l'arbo métier).

```markdown
---
tache: veille-fiches-compagnies
statut: en_cours        # en_cours | termine
cree: 2026-06-24
maj: 2026-06-24
---

## Contexte de reprise (à lire en premier, suffit à repartir à froid)
- But : monter les fiches compagnies manquantes via skill `recherche-compagnie`.
- Source de vérité : data/cibles-compagnies.json (candidaturePilote).
- Sortie : veille/rapports-compagnies/<slug>.md (+ MAJ _synthese-comparative.md).

## PROCHAINE ACTION → étape 4 (Transavia)

## Plan
- [x] 1. Ajouter au registre : One Air, TUI fly, Neos
- [x] 2. Fiche Swiftair (prio 1)
- [x] 3. Fiche ASL Airlines France (prio 1)
- [ ] 4. Fiche Transavia (prio 1)
- [ ] 5. Fiche easyJet (prio 1)
- [ ] 6. Fiche West Atlantic (prio 1)
- [ ] 7. Fiche Oyonnair (prio 1)
- [ ] 8. … prio 2/3
```

## 3. Règles qui rendent la reprise fiable

- **Atomicité** : une étape = une unité de travail + un commit. Jamais d'état
  « à moitié fait » non committé.
- **Idempotence** : relancer une étape déjà faite doit être sans danger
  (vérifier « le fichier existe-t-il déjà ? » avant d'écrire).
- **Le contexte vit dans le fichier**, pas dans la mémoire de session : le bloc
  « Contexte de reprise » doit suffire à repartir sans relire tout l'historique.
- **Commit = checkpoint** : message normalisé, ex.
  `checkpoint(veille): fiche Swiftair [3/8]`.
- **Fin** : quand toutes les cases sont cochées → `statut: termine`, puis on peut
  archiver/supprimer le fichier `.reprise/`.

## 4. Déclenchement de la skill

- **Auto** : au démarrage, si un `.reprise/*.md` avec `statut: en_cours` existe →
  la skill le signale et propose de reprendre.
- **Manuel** : `/reprise-checkpoint` (lister les chantiers en cours) ou
  `/reprise-checkpoint <slug>` (reprendre un chantier précis).

## 5. Note — parallèle avec l'outil natif

Claude Code dispose d'un mécanisme de **resume de workflow** (re-exécution qui
rejoue les étapes déjà faites depuis un cache). Cette skill en est la version
**chat/CC, manuelle et git-native** : pas de moteur, juste une discipline
plan + checkpoint + commit, lisible par un humain et portable entre repos.

## 6. Reste à trancher (Guillaume)

1. Emplacement : `.reprise/` à la racine **ou** réutiliser `REPRISE.md` existant
   (risque : `REPRISE.md` est déjà l'état de session, on mélangerait deux usages).
2. Granularité veille : **1 fiche / étape** (recommandé) ou lots de 2-3 ?
3. Skill **claude-os globale** (tous repos) — confirmé, c'est ta demande.
