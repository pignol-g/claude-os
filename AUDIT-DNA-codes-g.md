# Audit DNA — codes `gpose` / `gauto` / `gstop` (« je ne les trouve pas »)

> Tâches Asana : « Auditer DNA » (1208173596025197), « Skill gauto » (1208173596025171),
> « Skill gpose » (1208173596025170). Audit réalisé 2026-06-27.

## 1. Constat : les codes existent, mais sont mal découvrables

Contrairement à l'impression « introuvables dans la tâche mère du DNA », **les trois codes
sont bel et bien définis** :

| Code | Où il est défini | Version | Portée |
|---|---|---|---|
| `gpose` | `CLAUDE-DNA-CC-CORE.md` §« Combo réflexion » + `CLAUDE-DNA-CHAT.md` §« Combo réflexion » + `CLAUDE-DNA-CC-REF.md` (migration projet) | v1.7 | **Cross-plateforme** (CC + Chat) |
| `gauto` | `CLAUDE-DNA-CC-CORE.md` §« Combo autonome » | v2.1 | **CC uniquement** |
| `gstop` | `CLAUDE-DNA-CC-CORE.md` §« Combo autonome » (arrêt de `gauto`) | v2.1 | **CC uniquement** |

Donc le problème n'est pas l'absence de définition — c'est **un défaut de découvrabilité**.

## 2. Les 4 failles réelles

1. **Aucun index/registre des codes.** Les triggers vivent *en prose*, noyés au milieu du
   CORE (`gpose` §Combo réflexion, `gauto`/`gstop` §Combo autonome, `q:` §Inbox). Il n'existe
   nulle part une **table récapitulative « code → effet »** à scanner d'un coup d'œil. Un
   lecteur (humain ou Claude) qui cherche « gauto » par survol peut le rater.

2. **`gauto`/`gstop` sont CC-only.** Ils n'ont **aucun équivalent dans `CLAUDE-DNA-CHAT.md`**
   (cf. REPRISE.md : « gauto/gstop = CC-only, pas d'équivalent Chat »). En session Chat, ces
   codes sont donc **littéralement invisibles** → c'est « le problème pour le chat » pressenti
   par Guillaume.

3. **Dépendance au hook cloud.** En CC cloud, `~/.claude/` n'existe pas : le CORE est chargé
   par `curl` raw GitHub via `.claude/hooks/session-start.sh`. Si le hook échoue ou si le CORE
   n'est pas **entièrement** ingéré, les sections de fin (dont `gauto`) passent à la trappe.
   Un code « connu » devient alors « introuvable » selon l'aléa de chargement.

4. **Triggers ≠ skills.** Un trigger en prose n'est ni invocable explicitement (`/gauto`) ni
   planifiable (routine). Il dépend de la lecture intégrale du CORE à chaque session. Le
   transformer en **skill** le rend nommable, testable, versionné et appelable par une routine.

## 3. Recommandations (→ alimente les tâches skill)

- **R1 — Registre de codes dans le CORE.** Ajouter en tête du CORE une table unique
  `code | déclencheur | effet | portée (CC/Chat) | skill associée`. Source de vérité unique,
  fin des « je ne trouve pas ».
- **R2 — Skillifier les codes** (tâches dédiées) : `gauto` (mode autonome), `gpose` (combo
  réflexion). La skill **référence** la section DNA, ne la duplique pas (principe « pointé,
  jamais copié »). Cf. ébauches `.claude/skills/gauto/SKILL.md`.
- **R3 — Parité Chat.** Pour chaque code qu'on veut utilisable en Chat, soit porter une
  définition dans `CLAUDE-DNA-CHAT.md`, soit acter explicitement « CC-only » **dans le
  registre R1** (pour que l'absence soit un choix lisible, pas un trou).
- **R4 — Mécanisme de migration vers le Chat** (demande explicite de Guillaume) : à chaque
  skill créée, produire un **fichier de migration** `to-chat/MIGRATION-<skill>.md` contenant
  le prompt prêt-à-coller dans une session Chat (instructions + knowledge). Le répertoire
  `to-chat/` + `to-chat/_track-log.md` existent déjà → étendre ce flux. Guillaume colle, le
  Chat s'auto-configure. Action humaine minimale.
- **R5 — Garde-fou hook.** Au démarrage, après chargement du CORE, vérifier la présence d'un
  marqueur de fin de fichier (sentinelle) ; si absent → signaler « CORE partiellement chargé »
  au lieu de continuer en silence.

## 4. Réponse directe à Guillaume

> « Pourquoi tu ne trouves pas gauto/gpose/gstop dans le DNA ? »

Parce qu'ils y sont **mais sans index**, que **gauto/gstop sont CC-only** (donc absents en
Chat), et que le **chargement cloud par hook** peut tronquer le CORE. Les trois corrigés par :
un registre de codes (R1), la skillification (R2), la parité Chat actée (R3) et un fichier de
migration Chat par skill (R4).
