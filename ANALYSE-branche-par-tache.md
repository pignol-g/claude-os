# Analyse — « une branche Git par tâche Asana » comme système anti-interruption

> Réponse à la tâche Asana 135 (« Skill découpage anti interruption crédit »),
> commentaire Guillaume du 2026-06-26. Question posée : est-ce le bon système de
> travail, ou existe-t-il un process plus fluide et fiable ?

## Verdict court

**Oui, c'est le bon principe — et il ne part pas de zéro : la doctrine
anti-interruption existe DÉJÀ dans `CLAUDE-DNA-CC-CORE.md`** (mode autonome §boucle
pilotée). Ce que tu décris ajoute la pièce qui manque vraiment : **l'isolation par
tâche + le lien explicite Asana ↔ branche.** À adopter, avec 5 renforcements pour le
rendre *fiable* (pas seulement *possible*).

## Ce qui existe déjà (ne pas réinventer)

Le DNA-CC encode aujourd'hui, pour le mode autonome :

- `REPRISE.md` = snapshot « état ultra-récupérable comme si la session pouvait finir
  imprévu », mis à jour **à chaque cycle**.
- `RECAP-AUTO-YYYY-MM-DD.md` = journal de cycles.
- **1 commit + push par étape significative** (pas de batch tardif), `fetch + rebase`
  avant push.
- Condition d'arrêt explicitement prévue : **« (a) extinction crédits / session limit
  atteint »** → dernier turn obligatoire = MAJ REPRISE + commit/push.

Autrement dit, **la mémoire persistante est déjà là** (fichier d'état + commits
fréquents). Ce qui manque dans ce dispositif, et que ta proposition apporte :

1. **L'isolation** : aujourd'hui tout vit sur une branche de session ; rien ne sépare
   deux tâches menées en parallèle ou reprises à des moments différents.
2. **Le lien Asana ↔ branche** : aucun pointeur ne dit « cette tâche = cette branche ».

Ta proposition comble exactement ces deux trous. D'où : **convergence, pas
remplacement.**

## Forces de ta proposition

- La branche survit à l'éphémère (cloud = seul le poussé survit) → robuste aux limites
  de contexte / changements de session.
- Outillage standard (git), rien à inventer.
- S'aligne sur la convention de branches de session déjà en place
  (`claude/<nom>-<suffixe>`).
- Règle 4 (petite Q/R = pas de branche) = bon filtre anti-surcharge.

## Risques / angles morts (et comment les fermer)

1. **Un historique de commits n'est pas une bonne mémoire de reprise.** Relire des
   diffs pour « retrouver où on en était » est lent et fragile. → Réutiliser le format
   qui existe : **un fichier d'état par branche** (`WIP-<tache>.md`, calqué sur
   RECAP-AUTO/REPRISE) avec *Objectif / Plan / Fait / Prochaine étape / lien Asana*,
   commité à chaque arrêt. La reprise lit CE fichier, pas le diff.

2. **Multi-repo.** Une tâche peut toucher `candidaturePilote` ET `claude-os` ; une
   branche ne traverse pas les repos. → Noter dans Asana le(s) repo(s) concerné(s),
   **une branche par repo** sous le même nom logique.

3. **Prolifération + règle DNA « pas de delete branch ».** Beaucoup de tâches → beaucoup
   de branches, jamais supprimées. → Cycle de vie clair adossé à Asana : tâche validée
   par Guillaume → **merge de la PR** (clôture la branche sans la supprimer, conforme au
   DNA). Une branche « vivante » = une tâche en cours.

4. **Lien à double sens.** Tu prévois le nom de branche dans Asana ✓. Manque le retour :
   mettre **l'URL de la tâche Asana dans `WIP-<tache>.md`** → depuis la branche on
   retrouve la tâche.

5. **Visibilité mobile.** Un historique git ne se lit pas au téléphone — or c'est ton
   cas d'usage central. → **La PR draft (déjà imposée par le harness) EST la surface
   mémoire mobile** : sa description = plan vivant + checklist, lisible et éditable
   depuis GitHub/Gmail mobile. Mieux qu'un fichier pour le coup d'œil rapide.

## Système cible recommandé (synthèse)

- **1 tâche Asana de DÉV = 1 branche + 1 PR draft.** Nom de branche **et** lien PR
  écrits dans la description Asana dès la création.
- **Dans la branche : `WIP-<tache>.md`** = Objectif / Plan / Fait / Prochaine étape /
  lien Asana. Commit + push **à chaque arrêt** (déjà la règle « 1 étape = 1 commit »).
- **Reprise** : `fetch` la branche → lire `WIP-<tache>.md` (+ description de la PR) →
  continuer. Pas de relecture de diff.
- **Petite Q/R** : pas de branche (ta règle 4).
- **Clôture** : Guillaume valide la tâche Asana → merge de la PR (pas de suppression de
  branche, conforme DNA).

## Lien avec le « découpage anti-interruption / crédit »

Le cœur anti-interruption n'est pas la branche, c'est la **granularité** : **1 passe =
1 commit poussé.** Si une interruption (limite crédit, fin de session) tombe, on perd au
pire la passe en cours, jamais le travail déjà poussé. C'est exactement le même principe
que tu décline aux tâches 168 (routine crédit) et 173 (avance autonome) : la branche est
le *contenant*, le découpage en passes commitées est le *mécanisme*.

## À trancher (balle chez Guillaume)

1. Je formalise ça en **patch du DNA-CC CORE** (convention officielle « branche + PR +
   WIP par tâche dev ») ?
2. J'adapte la **skill `asana-pass`** pour qu'à la prise d'une tâche de dév elle
   crée/relie automatiquement branche + PR draft et inscrive le nom de branche dans la
   description Asana ?

Sur ton GO, je porte (1) + (2) ; cette analyse devient alors la base du patch.
