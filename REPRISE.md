# REPRISE — claude-os

**Dernière session : 2026-08-07** (cycle `gaudit`, premier passage réel)

## État courant

DNA-CC **v3.3** (bump ce cycle), DNA-Chat **v2.2** (bump ce cycle, aligné). Depuis la dernière
mise à jour de ce fichier (2026-05-23, v2.1), le repo a beaucoup avancé sans que `REPRISE.md`
soit tenu à jour — c'était en soi un des constats de ce cycle (cf. `audit/claude-os/PLAN-2026-08-07.md`
T1.3). Points marquants accumulés depuis :

- **`gtri`** — skill de triage claude-os → `general` (5 tests de décision, Q/R obligatoire). Premier
  passage exécuté 2026-07-21 : lettre de motivation, profil rédactionnel et recherche
  ChatGPT-vs-Claude transférés vers `general`, référencés depuis ici par pointeur raw URL.
- **`gprompt`** — skill générateur/optimiseur de prompt interactif. Ajoutée mi-2026 mais son
  trigger était resté absent du CORE et du DNA-Chat jusqu'à ce cycle `gaudit` (corrigé, cf. T1.1/T1.2).
- **`CLAUDE-DNA-ASANA.md`** — module autonome dédié à l'organisation Asana « nous 3 », référencé
  depuis le CORE §6.
- **Convention Q/R** — option `(recommandé)` obligatoire par bloc + code `reco` pour valider
  d'un coup toutes les recommandations d'un tour (CORE/CHAT v3.2/v2.1, 2026-07-22).
- **`gaudit`** — nouvelle skill d'audit de projet autonome et résilient (`.claude/skills/gaudit/`
  + `audit/STATE.md`), pensée pour tourner comme Routine Claude Code Remote. Landée via PR #33
  (mergée 2026-08-07). Carve-out documenté dans le CORE : merge auto de PR autorisé pour cette
  seule routine si CI verte + merge propre. **Ce cycle est son premier passage réel** — voir
  `audit/claude-os/PLAN-2026-08-07.md` et `audit/claude-os/REPORT-2026-08-07.md` une fois le
  plan bouclé.
- **`CLAUDE.md` racine** — créé (résolvait l'anomalie notée dans la session 2026-05-23 : absence
  de `CLAUDE.md` projet pour claude-os lui-même).

## Fichiers DNA — état des lieux

- [CLAUDE-DNA-CC-CORE.md](CLAUDE-DNA-CC-CORE.md) — v3.3, injecté par hook à chaque session CC.
- [CLAUDE-DNA-CC-REF.md](CLAUDE-DNA-CC-REF.md) — v2.1 (2026-06-13), procédures cold, curl à la demande.
- [CLAUDE-DNA-CHAT.md](CLAUDE-DNA-CHAT.md) — v2.2, à coller dans Instructions globales claude.ai.
- [CLAUDE-DNA-CC.md](CLAUDE-DNA-CC.md) / [CLAUDE-DNA.md](CLAUDE-DNA.md) — stubs de redirection
  legacy. Condition de retrait (tous les hooks projet connus migrés vers `DNA_URL=…CORE.md`)
  vérifiée remplie ce cycle (candidaturePilote + ClaudeAchatMaison) — voir décision T2.3 du plan
  d'audit pour le statut exact au moment de la lecture de ce fichier.

## Actions Guillaume en attente

- `chatSyncDNAChatOk` — uploader `CLAUDE-DNA-CHAT.md` v2.2 dans Instructions globales claude.ai
  (dernier upload connu antérieur au bump de ce cycle — le trigger `gprompt` manquait côté Chat).

## Questions ouvertes pour prochaine session

- `INBOX-QUESTIONS.md` a un item en attente depuis 2026-07-21 (correctifs `candidaturePilote`
  Sonnet-vs-Opus + migration profil rédactionnel) — décision Guillaume requise.
- Repo `candidaturePilote` : hook `session-start.sh` encore en v2.0 (pas de git pull auto au
  démarrage) — signalé au rapport `gaudit` de ce cycle, à corriger lors du prochain cycle
  `gaudit` ciblant ce repo (ou avant, si Guillaume préfère).
- Première Routine `gaudit` créée puis désactivée (`trig_01Y6mLjE6VSXYg8WtmdPA9aB`) faute de
  pouvoir attacher les connecteurs via l'API `create_trigger` — à réactiver après un
  `fire_trigger` de validation ou recréation depuis l'UI Routines de claude.ai.

## Options de reprise (prochaine session)

- `resA` — relire le rapport du cycle `gaudit` claude-os (`audit/claude-os/REPORT-2026-08-07.md`)
  et décider d'activer la Routine `gaudit` pour de bon.
- `resB` — trancher l'item `INBOX-QUESTIONS.md` du 2026-07-21 (candidaturePilote).
- `resC` — lancer un cycle `gaudit` manuel sur `candidaturePilote` (hook v2.0 à mettre à jour +
  autres pistes d'amélioration à diagnostiquer).
