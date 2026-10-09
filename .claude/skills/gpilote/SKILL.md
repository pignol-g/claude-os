---
name: gpilote
description: Chef d'orchestre des Routines de Guillaume (routine « Pilote quota », Sonnet). À chaque déclenchement, appelle gquota puis décide quelles tâches lancer, de la plus légère à la plus lourde, sans jamais les faire lui-même ; tourniquet entre les tâches lourdes, une seule tâche du groupe candidaturePilote/claude-os à la fois. À invoquer par la routine « Pilote quota » ou quand Guillaume écrit `gpilote`.
effort: max
allowed-tools: Bash, mcp__claude-code-remote__list_events, mcp__claude-code-remote__get_trigger, mcp__claude-code-remote__fire_trigger
---

# gpilote — chef d'orchestre des routines

Le pilote **décide et lance**, il ne fait aucune tâche lui-même. Session courte : ne lis
aucun autre fichier que celui-ci et ceux qu'il cite, n'explore aucun repo.

## Tâches

Chaque tâche est une Routine sans horaire (déclenchée uniquement par le pilote) qui porte
son propre modèle et son prompt, et rappelle `gquota` avant chacune de ses étapes.

| Clé | Routine (`trigger_id`) | Modèle | Classe | Règle d'éligibilité |
|---|---|---|---|---|
| `t7` | `trig_011FpKBMDrYoaUjFmxLaCs42` | Opus 5.5 (ultracode) | prioritaire | file Asana T7 non vide |
| `asana` | `trig_01GrfJRgJPURxDggBnaJK83M` | Sonnet 5.5 | prioritaire | file Asana « pour claude » non vide |
| `offre` | `trig_01JUSVQ6CLSogoNBnqZpV3rB` | Sonnet 5.5 | groupe, moyenne | dernier lancement > 20 h |
| `veille` | `trig_01QUawXGgfoU7Ps5DPQJifGC` | Sonnet 5.5 | groupe, moyenne | dernier lancement > 6 j 12 h |
| `gaudit` | `trig_01TeYwhzzZtv2q7XqfyHJwQ3` | Sonnet 5.5 (ultracode) | groupe, lourde | tourniquet |
| `gauto` | `trig_01MJT4DgEnjHEb8JmHS1uQ1u` | Opus 4.8 | groupe, lourde | tourniquet |

« Groupe » = tâches qui écrivent dans candidaturePilote ou claude-os : **une seule à la fois**
(collisions sur `cibles-compagnies.json`, `TODO.md`, `REPRISE.md`, `audit/STATE.md`).

## Procédure

1. **Garde-quota** : invoquer la skill `gquota` (si elle n'est pas chargée, appliquer à la
   main la procédure de `claude-os/.claude/skills/gquota/SKILL.md`). STOP → terminer en
   citant la ligne, rien d'autre. GO → garder la ligne pour l'étape 4.
2. **État** : `get_trigger` sur chacun des 6 `trigger_id`. Pour chaque tâche, relever
   `last_run.fired_at`. Une tâche est **en cours** si `last_run` existe sans `finished_at`
   et que `fired_at` a moins de 8 h (au-delà : session morte, la tâche redevient libre).
3. **Choix**, dans cet ordre (une tâche en cours n'est jamais relancée) :
   1. `t7` : `mcp__Asana__get_tasks` (via ToolSearch) sur les sections `1219334593652347`
      (« Claude — en cours ») et `1219329114419835` (« Demandes pour Claude »), tâches
      incomplètes seulement. Au moins une → retenue.
   2. `asana` : même appel sur la section `1208173596025107` (« pour claude »). Au moins
      une → retenue.
   3. Groupe : si une tâche du groupe est en cours → aucune. Sinon la première éligible :
      `offre`, puis `veille`, puis la lourde (`gaudit` ou `gauto`) dont le dernier
      lancement est le plus ancien (jamais lancée = la plus ancienne ; égalité → `gaudit`).
   - **Asana indisponible** dans la session : `t7` et `asana` sont retenues seulement si
     leur dernier lancement date de plus de 24 h (elles s'arrêtent seules si leur file est
     vide).
4. **Lancement** : `fire_trigger` sur chaque tâche retenue, dans l'ordre ci-dessus, avec
   `text` = « Lancée par le pilote le <date heure de Paris>. gquota : <ligne GO> ».
5. **Récap** : une ligne par tâche — lancée / file vide / en cours / pas son tour / pas due.

## Garde-fous

- Ne jamais modifier, activer, désactiver ou supprimer une Routine (`update_trigger`,
  `delete_trigger`) : seul Guillaume pilote les Routines.
- Ne jamais lancer deux fois la même tâche dans un déclenchement.
- Ne faire aucune tâche soi-même, même courte.

## Routine « Pilote quota »

`trig_01QZGCU8HUB1XWbMFc8STKkK`, créée sans horaire tant que Guillaume ne l'a pas armée. À l'armement :
`cron_expression = CRON_TZ=Europe/Paris 31 0,5,10,15,20 * * *` (5 passages par jour ; celui
de 20h31 tombe, le vendredi, dans la fenêtre de fin de semaine de `gquota`). Modèle Sonnet 5.5.
Prompt : « Invoque la skill gpilote (ajoute et clone pignol-g/claude-os si absent ; si la skill
n'est pas chargée, lis claude-os/.claude/skills/gpilote/SKILL.md et applique-la). »

Les anciennes Routines (Gaudit, gaudit horaire, Utilisation crédit hebdo, analyse-offre
nocturne, audit-veille, Traitement auto asana, Passe Asana T7) restent désactivées, pour
archive (décision `anciennesA`, 2026-10-09).

## Limites connues

- Les Routines créées depuis une session ne peuvent pas porter de connecteur (paramètre
  refusé pour l'organisation). Si Asana manque dans les sessions des tâches `t7` et `asana`,
  l'ajouter à ces Routines depuis l'interface claude.ai (Routines).
- L'effort d'une Routine n'est pas réglable par l'API : `effort: max` ne s'applique que si
  la skill est chargée comme skill.
- Détection « en cours » fondée sur `last_run` : une tâche qui plante sans `finished_at`
  bloque sa place 8 h au maximum.
