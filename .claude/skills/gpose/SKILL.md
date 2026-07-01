---
name: gpose
description: >
  Combo réflexion « pose-toi » de Guillaume : amplification de la Posture Guide.
  À invoquer dès que Guillaume écrit `gpose` n'importe où dans un message (déclenchement
  inline, milieu de phrase compris), ou dit « pose-toi », « propose d'abord », « ne code
  pas encore, réfléchis ». Applique systématiquement, DANS CET ORDRE : reformuler la
  demande → expliquer le concept sous-jacent si utile → proposer 2-4 options chiffrées
  (impact + coût) en codes Q/R → poser les questions ouvertes qui bloquent la décision.
  Ne RIEN exécuter tant que Guillaume n'a pas validé. Compatible avec les autres codes Q/R.
---

# gpose — combo réflexion (« pose-toi avant d'agir »)

`gpose` est l'**amplification de la Posture Guide** : quand Guillaume l'écrit, il ne veut
pas une exécution, il veut que Claude **se pose, cadre et propose** avant tout code ou toute
action irréversible. Le mot-clé peut apparaître **n'importe où** dans le message (y compris
en milieu de phrase) — le simple fait qu'il soit présent déclenche cette skill.

> **Source de vérité** : cette skill EST le corps de la procédure. Le `CLAUDE-DNA-CC-CORE.md`
> ne garde qu'une ligne-trigger qui pointe ici (patron « CORE pointe, skill contient »,
> validé 2026-07-01, cf. PLAN-ARCHITECTURE-SKILLS.md chantier A).

## Quand m'activer

- Guillaume écrit `gpose` (n'importe où dans le message).
- Formulations équivalentes : « pose-toi », « propose d'abord / avant de coder »,
  « réfléchis, ne fais rien encore », « donne-moi des options ».

## Procédure — systématique et DANS CET ORDRE

1. **Reformuler** ce que Guillaume veut (2-3 phrases) → vérifier la compréhension.
   **Ne rien exécuter** tant qu'il n'a pas validé la reformulation.
2. **Expliquer le concept sous-jacent** si pertinent (3-5 lignes max) — le « pourquoi »
   technique ou méthodologique qui éclaire la décision. Sauter si évident.
3. **Proposer 2-4 options chiffrées** : pour chacune, **impact** (ce que ça change) et
   **coût** (effort / risque / réversibilité). Présenter en **codes Q/R**.
4. **Poser les questions ouvertes** qui bloquent la décision, en **codes Q/R**. Une question
   = un point réellement bloquant, pas du remplissage. Donner une **recommandation** par
   question quand j'en ai une (« reco : … »).

## Garde-fous

- **Zéro exécution avant GO.** `gpose` interdit d'enchaîner sur le code / la modif / l'action
  externe dans le même tour. Le livrable de ce tour = la reformulation + options + questions.
- **GO partiel accepté** : si Guillaume répond « lance l'option B » ou « fais A d'abord »,
  n'exécuter QUE ce qu'il a validé, pas l'ensemble.
- **Chiffrer honnêtement** : ne pas sous-estimer le coût ni survendre un impact. Signaler
  l'irréversible et les dépendances entre options.
- Compatible avec les autres **codes Q/R** de Guillaume (peut se combiner dans le même message).

## Rappel — Posture Guide (dont gpose est l'amplification)

La Posture Guide par défaut : proposer avant d'imposer, expliquer les arbitrages, laisser
Guillaume décider. `gpose` la pousse au maximum quand l'enjeu est structurant (architecture,
migration, choix engageant) ou quand Guillaume veut explicitement ralentir avant d'agir.
