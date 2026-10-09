---
name: gpilote
description: Chef d'orchestre des Routines de Guillaume (routine « Pilote quota », Sonnet). À chaque déclenchement, appelle gquota puis décide quelles tâches lancer, de la plus légère à la plus lourde, sans jamais les faire lui-même ; une seule tâche lourde par passage (tourniquet), une seule tâche du groupe candidaturePilote/claude-os à la fois. À invoquer par la routine « Pilote quota » ou quand Guillaume écrit `gpilote`.
effort: max
allowed-tools: Bash, mcp__claude-code-remote__list_events, mcp__claude-code-remote__get_trigger, mcp__claude-code-remote__fire_trigger, mcp__Asana__get_tasks
---

# gpilote — chef d'orchestre des routines

Le pilote **décide et lance**, il ne fait aucune tâche lui-même. Session courte : ne lis
aucun autre fichier que celui-ci et ceux qu'il cite, n'explore aucun repo.

## Tâches

Chaque tâche est une Routine sans horaire (déclenchée uniquement par le pilote) qui porte
son propre modèle et son prompt, et rappelle `gquota` avant chacune de ses étapes. « Sans
horaire » = `run_once_at` au 2099-12-31 : l'API ne sait pas retirer un cron, et un
`fire_trigger` manuel ne consomme pas ce lancement unique (vérifié le 2026-10-09).

| Clé | Routine (`trigger_id`) | Modèle | Classe | Règle d'éligibilité |
|---|---|---|---|---|
| `asana` | `trig_01GrfJRgJPURxDggBnaJK83M` | Sonnet 5.5 | légère | file Asana « pour claude » non vide |
| `offre` | `trig_01JUSVQ6CLSogoNBnqZpV3rB` | Sonnet 5.5 | groupe, moyenne | due si dernier lancement > 20 h |
| `veille` | `trig_01QUawXGgfoU7Ps5DPQJifGC` | Sonnet 5.5 | groupe, moyenne | due si dernier lancement > 6 j 12 h |
| `t7` | `trig_011FpKBMDrYoaUjFmxLaCs42` | Opus 5.5 (ultracode) | lourde | file Asana T7 non vide |
| `gaudit` | `trig_01TeYwhzzZtv2q7XqfyHJwQ3` | Sonnet 5.5 (ultracode) | groupe, lourde | tourniquet |
| `gauto` | `trig_01MJT4DgEnjHEb8JmHS1uQ1u` | Opus 4.8 | groupe, lourde | tourniquet |

« Groupe » = tâches qui écrivent dans candidaturePilote ou claude-os : **une seule à la fois**
(collisions sur `cibles-compagnies.json`, `TODO.md`, `REPRISE.md`, `audit/STATE.md`).
« Lourde » = **une seule par passage**, chacune son tour : c'est ce qui empêche une tâche de
manger tout le reliquat et de priver les autres.

## Procédure

1. **Garde-quota** : invoquer la skill `gquota` (si elle n'est pas chargée, appliquer à la
   main la procédure de `claude-os/.claude/skills/gquota/SKILL.md`). STOP → terminer en
   citant la ligne, rien d'autre. GO → garder la ligne pour l'étape 4 et calculer la
   **marge** = `seuil` − `hebdo` (fenêtre de fin de semaine, ligne avec `fin=` : marge illimitée).
2. **État** : `get_trigger` sur chacun des 6 `trigger_id` ; relever `last_run`
   (`fired_at`, `finished_at`, `status`).
   - **En cours** : `last_run` sans `finished_at` et `fired_at` de moins de 8 h (au-delà :
     session morte, la tâche redevient libre).
   - **Dernier lancement** = `last_run.fired_at`. Une tâche à cadence (`offre`, `veille`)
     dont le dernier lancement a échoué (`status` en échec) redevient due 24 h après.
3. **Choix**, dans cet ordre (une tâche en cours n'est jamais relancée) :
   1. **Légère** — `asana` : `mcp__Asana__get_tasks` (via ToolSearch) sur la section
      `1208173596025107` (« pour claude »), tâches incomplètes. Au moins une → retenue.
   2. **Moyenne** — si aucune tâche du groupe n'est en cours : parmi `offre` et `veille`
      dues, celle dont le retard rapporté à sa cadence est le plus grand → retenue.
   3. **Lourde** (une seule) — candidates : `t7` si sa file est non vide (même appel sur les
      sections `1219334593652347` « Claude — en cours » et `1219329114419835` « Demandes pour
      Claude ») ; `gaudit` et `gauto` seulement si aucune tâche du groupe n'est en cours ni
      retenue en 3.2. Retenir celle dont le dernier lancement est le plus ancien (jamais
      lancée = la plus ancienne ; égalité → `t7`, puis `gaudit`).
   4. **Marge < 5 points** : ne lancer que la première tâche retenue (ordre 3.1 → 3.3), pour
      que plusieurs sessions parallèles ne dépassent pas ensemble le seuil.
   - **Asana indisponible** dans la session : `asana` et `t7` restent candidates seulement si
     leur dernier lancement date de plus de 24 h (elles s'arrêtent seules si leur file est vide).
4. **Lancement** : `fire_trigger` sur chaque tâche retenue, dans l'ordre ci-dessus, avec
   `text` = « Lancée par le pilote le <date heure de Paris>. gquota : <ligne GO> ».
5. **Récap** : une ligne par tâche — lancée / file vide / en cours / pas son tour / pas due.

## Garde-fous

- Ne jamais modifier, activer, désactiver ou supprimer une Routine (`update_trigger`,
  `delete_trigger`) : seul Guillaume pilote les Routines.
- Ne jamais lancer deux fois la même tâche dans un passage.
- Ne faire aucune tâche soi-même, même courte.

## Routines « Pilote quota »

- `trig_01QZGCU8HUB1XWbMFc8STKkK` : `CRON_TZ=Europe/Paris 31 0,5,10,15,20 * * 0-5`
  (5 passages par jour, **sauf le samedi** : ce jour-là il n'y a aucun jour révolu, gquota
  répondrait STOP à chaque passage). Le passage de 20h31 le vendredi tombe dans la fenêtre de
  fin de semaine tant que le reset est à 21h00 heure de Paris.
- `trig_01KPhGAFkbV836y1kpZAkQfk` : `CRON_TZ=Europe/Paris 31 19 * * 5` (passage
  supplémentaire du vendredi, décision `hiverA` : couvre la fenêtre si le reset tombe à 20h00
  heure de Paris en hiver ; sinon passage ordinaire).
- Modèle Sonnet 5.5. Prompt : « Invoque la skill gpilote (ajoute et clone pignol-g/claude-os si
  absent ; si la skill n'est pas chargée, lis claude-os/.claude/skills/gpilote/SKILL.md et
  applique-la). »
- Connecteurs et dépôts se règlent depuis l'interface claude.ai (Routines) : l'API ne permet
  ni l'un ni l'autre. Une modification par l'interface impose un horaire : le retirer ensuite
  (`run_once_at` 2099) sur les Routines de tâches.

Les anciennes Routines (Gaudit, gaudit horaire, Utilisation crédit hebdo, analyse-offre
nocturne, audit-veille, Traitement auto asana, Passe Asana T7) restent désactivées, pour
archive (décision `anciennesA`, 2026-10-09).

## Limites connues

- **Connecteurs** : une Routine créée depuis une session (`create_trigger`) n'a aucun
  connecteur (paramètre refusé pour l'organisation) ; Asana a été ajouté depuis l'interface
  claude.ai le 2026-10-09 aux 7 premières Routines, pas encore à celle du vendredi. Sans lui :
  pré-check en repli 24 h, et `t7`/`asana` s'arrêtent en le signalant.
- **Effort** : non réglable par l'API sur une Routine ; `effort: max` ne s'applique que si
  la skill est chargée comme skill.
- **Détection « en cours »** fondée sur `last_run` : une tâche qui plante sans
  `finished_at` bloque sa place 8 h au maximum ; une tâche qui finit son tour en laissant
  une commande en arrière-plan paraît libre (les prompts l'interdisent).
- `asana` reste hors du groupe : elle peut committer `qa_log.json` / `INBOX-QUESTIONS.md`
  pendant qu'une tâche du groupe tourne (conflit rare, résolu par un merge au push suivant).
