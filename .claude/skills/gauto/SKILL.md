---
name: gauto
description: >-
  ÉBAUCHE (à itérer avec Guillaume). Mode autonome longue durée — Claude pilote seul un
  projet jusqu'à arrêt explicite (gstop), bouton stop, ou extinction des crédits. À invoquer
  quand Guillaume écrit `gauto`, tape /gauto, ou via une routine planifiée (ex : routine-credit
  quand il reste du surplus hebdo). Encode la boucle pilotée + persistance + safety déjà
  spécifiées au DNA-CC-CORE §« Combo autonome ».
---

# gauto — mode autonome longue durée

> **Statut : ÉBAUCHE v0.1** — brouillon demandé par Guillaume (tâche Asana 1208173596025171)
> pour itérer ensemble. Ne pas considérer comme figé.
>
> **Source de vérité = DNA-CC-CORE §« Combo autonome — trigger `gauto` / arrêt `gstop` »**
> (v2.1). Cette skill **référence** cette section, ne la duplique pas. En cas de divergence,
> le CORE prime. La skill ajoute : invocabilité explicite (`/gauto`), planifiabilité (routine),
> et un point d'entrée nommé.

## Quand m'activer

- Guillaume écrit `gauto` n'importe où dans un message.
- Invocation explicite `/gauto` (ou via une routine planifiée, ex : `routine-credit`).
- Arrêt : `gstop`, bouton stop CC, ou extinction crédits / session limit.

## Boucle pilotée (ne JAMAIS s'arrêter spontanément)

1. **Analyse** de l'état projet — lire `REPRISE.md`, l'INDEX, le bien/dossier actif, les
   `TODO.md` ouverts, l'inbox `q:`.
2. **Plan d'action priorisé** — Tier 1 / 2 / 3 par valeur opérationnelle.
3. **Découpage** en étapes atomiques.
4. **Exécution étape par étape** — 1 commit + push par étape significative
   (granularité anti-interruption : une coupure ne coûte au pire que la passe en cours).
5. **MAJ `REPRISE.md`** à chaque cycle (état ultra-récupérable, comme si la session pouvait
   finir à l'imprévu) + alimenter `RECAP-AUTO-YYYY-MM-DD.md`.
6. **Reboucler en (1)** dès le plan épuisé — réanalyser, identifier les nouvelles priorités.
   En fin de plan principal, piocher dans `INBOX-QUESTIONS.md` `## ⏳ En attente`
   (priorité 🔴 puis FIFO).

## Persistance & git

- Commit/push après **chaque** étape (jamais de batch tardif).
- Avant chaque push : `git fetch origin && git rebase origin/main`.
- `RECAP-AUTO-YYYY-MM-DD.md` à la racine projet, lié dans `REPRISE.md`.
- Documenter chaque décision autonome significative (revue de Guillaume au réveil).

## Économie API (jamais crasher)

- Batchs séquentiels, pas de pic multimodal parallèle (max 5 Read images/message).
- Retry doux sur 529 (attente 30 s puis abandon propre du cycle courant).
- Modèles légers (Sonnet/Haiku) pour Read volumineux ou tâches structurées.

## Arrêt (3 conditions) — dernier turn obligatoire

(a) extinction crédits / session limit · (b) `gstop` · (c) bouton stop.
Dans tous les cas : **MAJ `REPRISE.md` + `RECAP-AUTO` finalisé + commit/push** avant de rendre la main.

## Safety interdits (violation = arrêt + alerte Guillaume)

- Pas de merge PR sans validation explicite de Guillaume.
- Pas de force-push (jamais). Pas de `git branch -D` ni delete de branche distante.
- Pas de `--no-verify` ni skip de hooks. Pas de modif `.claude/settings.json` ni `.claude/hooks/`.

## Points ouverts à trancher avec Guillaume (itération)

- **Portée par défaut** : `gauto` sans projet précisé → quel projet pilote-t-il ? (le repo
  courant ? un ordre de priorité claude-os > pilote > immo ?)
- **Lien routine-credit** : quand `routine-credit` déclenche `gauto`, sur quel backlog se
  rabat-on en priorité (veille / fiches compagnies / pré-montage dossiers) ?
- **Parité Chat** : `gauto` reste-t-il CC-only (acté au registre DNA) ou faut-il un fichier
  `to-chat/MIGRATION-gauto.md` ?
