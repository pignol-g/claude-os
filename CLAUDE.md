# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Ce que ce repo est

`claude-os` est le repo « DNA » de Guillaume Pignolet : la doctrine versionnée qui définit comment Claude doit se comporter avec lui, sur toutes les surfaces (Claude Code local et cloud, Claude Chat/claude.ai, Asana). Ce n'est **pas** du code applicatif — c'est de la configuration-as-doctrine, pointée (jamais copiée) par les autres repos projet de Guillaume (ex. `candidaturePilote`).

Il n'y a ni build, ni lint, ni tests, ni CI : ce repo ne contient que des fichiers Markdown de doctrine et deux scripts shell utilitaires.

## Architecture — fichiers DNA

Le cœur du repo est la famille `CLAUDE-DNA-*.md`, avec une séparation **hot/cold** pour économiser le contexte :

- **`CLAUDE-DNA-CC-CORE.md`** (~300 lignes) — chargé à **chaque session CC** via le hook `SessionStart`. Contient : profil utilisateur, Posture Guide, convention des codes Q/R pour proposer des options, règles d'économie de tokens (choix de modèle Opus/Sonnet/Haiku), définitions des triggers `gpose`/`gauto`/`grech`/`gtri`, **interdits de sécurité durs** (pas de force-push, pas de merge sans validation, pas de `--no-verify`, pas de modification des hooks/settings), convention d'inbox de questions différées (`q:`), convention `TODO.md`, règles d'écriture à la voix de Guillaume, checklist de comportement début/fin de session.
- **`CLAUDE-DNA-CC-REF.md`** (~450 lignes) — compagnon « froid », procédures rares (architecture CC↔Chat↔OS, templates, checklist de bootstrap pour un nouveau projet, migration legacy, historique de versions). Récupéré à la demande (curl) quand un trigger du CORE matche, via le sommaire §5 du CORE.
- **`CLAUDE-DNA-CHAT.md`** — variante autonome, à coller telle quelle dans les Instructions globales de claude.ai (pas de mécanisme de hook sur cette surface).
- **`CLAUDE-DNA-ASANA.md`** — module séparé régissant le workflow « Guillaume + Claude + Asana » (taxonomie Actions assignables/clôturables vs Folders vs Resources ; règle anti-divergence : un item de données a un seul propriétaire).

**Convention de diffusion** : le DNA est **pointé, jamais copié**. Les repos projet le récupèrent via leur propre hook `session-start.sh`, soit en local (si `claude-os` est cloné à côté), soit par `curl` sur `raw.githubusercontent.com/pignol-g/claude-os/main/...`.

## `.claude/`

- **`settings.json`** — enregistre un unique hook `SessionStart`.
- **`hooks/session-start.sh`** (v2.1) — à chaque démarrage de session : (1) `git pull --rebase --autostash origin main` (échec doux : si conflits/pas de réseau, log un warning et continue — le DNA doit charger même hors ligne) ; (2) charge `CLAUDE-DNA-CC-CORE.md` (local sinon curl) dans le contexte ; (3) signale les uploads `to-chat/` en attente (lit `to-chat/_upload-status.json`) ; (4) affiche une ligne marqueur de confirmation (version DNA + statut git).
- **`skills/`** — 7 skills implémentant les triggers `g*` du CORE : `gauto` (mode autonome longue durée), `gaudit` (audit de projet autonome et résilient, pensé pour tourner en Routine Claude Code Remote), `gpose` (pause-réflexion, propose des options chiffrées avant d'agir), `gprompt` (générateur/optimiseur de prompt), `grech` (recherche approfondie multi-agents), `gtri` (triage et transfert claude-os → `general`), `asana-pass` (traitement collaboratif des tâches Asana en ping-pong).

## Autres répertoires

- **`scripts/install-claude-config.sh`** — bootstrap le `.claude/` d'un nouveau projet (copie locale depuis un mirror Drive, ou fallback curl en environnement cloud/CC-web).
- **`to-cc/`** — inbox d'exports collés depuis Claude Chat vers Claude Code ; éphémère, lu au démarrage CC puis vidé.
- **`to-chat/`** — outbox d'artefacts à uploader vers le Project Knowledge de claude.ai (templates + `_TODO.md`, `_track-log.md`, `_upload-status.json` qui trace les uploads en attente).
- **`REPRISE.md`** / **`INBOX-QUESTIONS.md`** — état de reprise de session et inbox de questions différées ; artefacts opérationnels du workflow DNA, pas du code.
- **`audit/`** — état persistant de la skill `gaudit` (`STATE.md` = point d'entrée unique
  résumable multi-session, `<repo>/PLAN-*.md` + `<repo>/REPORT-*.md` par repo cible).

## Repo consommateur

Le repo `general` (connaissances/livrables multi-IA, hors outillage Claude Code) reçoit du contenu triagé par la skill `gtri`, référencé ici par pointeur raw-URL plutôt que dupliqué.
