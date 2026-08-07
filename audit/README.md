# `audit/` — état et livrables de la routine `gaudit`

Ce dossier est le cœur de persistance de la skill `gaudit` (`.claude/skills/gaudit/SKILL.md`)
— audit de projet autonome, résilient à l'interruption, pensé pour tourner comme Routine
Claude Code Remote (session neuve à chaque déclenchement, sans mémoire de conversation).

- **`STATE.md`** — point d'entrée unique, lu en premier à chaque cycle. Dit quel repo est
  en cours, à quel stade, et sert de garde anti-collision entre firings qui se chevauchent.
- **`<repo>/`** — un dossier par repo cible (`claude-os`, `general`, `candidaturePilote`,
  `ClaudeAchatMaison`) :
  - `PLAN-AAAA-MM-JJ.md` — plan détaillé du cycle en cours ou du dernier cycle (diagnostic,
    items priorisés Tier 1/2/3, cases faites/à faire).
  - `REPORT-AAAA-MM-JJ.md` — rapport standardisé, généré **uniquement** en fin de cycle
    **terminé** (jamais sur interruption).

**Convention** : ces fichiers vivent dans `claude-os` (le repo DNA), pas dans le repo
audité lui-même — c'est le point de centralisation qui permet à une session totalement
neuve de savoir, sans ambiguïté, où reprendre (cf. `STATE.md`).
