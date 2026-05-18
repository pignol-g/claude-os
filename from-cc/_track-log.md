# Track log — versions des fichiers from-cc/ (projet claude-os)

<!-- Historique chronologique des bumps de version. CC ajoute une ligne à chaque bump. -->

| Date | Fichier | Version | Raison du bump | Statut upload |
|---|---|---|---|---|
| 2026-05-17 | CLAUDE-DNA-CHAT.md | v1.5 | Split initial du DNA v1.4 en CC + CHAT. Première version Chat autonome. | uploaded 2026-05-17 |
| 2026-05-17 | CLAUDE-DNA-CC.md | v1.6 | DNA pointé, jamais copié (sec 6.2, 7, 8 réécrites). Core inchangé, donc DNA-CHAT reste v1.5 (pas de re-upload Chat). | n/a (CC-only, lu via pointeur) |
| 2026-05-17 | CLAUDE-DNA-CC.md + CLAUDE-DNA-CHAT.md | v1.7 | Trigger `gpose` ajouté au Core (combo réflexion). Section 9 "Migration projet legacy" ajoutée côté CC. "sync DNA" verbalement déprécié. Core touché → DNA-CHAT à re-uploader. | DNA-CHAT uploaded 2026-05-17 |
| 2026-05-17 | CLAUDE-DNA-CC.md + CLAUDE-DNA-CHAT.md + _TEMPLATE-knowledge.md | v1.8 | Réalignement convention : 1 fichier knowledge unique par défaut (`knowledge-projet-vX.Y.md`), < 15 max si multiples (seuil RAG claude.ai). Corrige dérive v1.5. | DNA-CHAT pending upload |
| 2026-05-18 | CLAUDE-DNA-CC.md + .claude/settings.json + .claude/hooks/session-start.sh | v1.9 | Hook SessionStart projet (commité) remplace hook global Mac. Injecte DNA-CC dans contexte CC au démarrage, marche cloud + local. Hook global supprimé (`~/.claude/settings.json` + `~/.claude/hooks/`). | n/a (CC-only) |
