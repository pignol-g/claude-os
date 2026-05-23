# REPRISE — claude-os

**Dernière session : 2026-05-23**

## État courant

DNA-CC **v2.1** : ajout du trigger `gauto` (mode autonome longue durée) + `gstop` (arrêt explicite) dans la section 1 du Core, entre `gpose` et `Méta-règles d'éducation`. PR #2 mergée sur `main`.

- [CLAUDE-DNA-CC-CORE.md](CLAUDE-DNA-CC-CORE.md) — v2.1, ~190 lignes, injecté par hook
- [CLAUDE-DNA-CC-REF.md](CLAUDE-DNA-CC-REF.md) — inchangé v2.0
- [CLAUDE-DNA-CHAT.md](CLAUDE-DNA-CHAT.md) — inchangé v1.8 (gauto/gstop = CC-only, pas d'équivalent Chat)
- [CLAUDE-DNA-CC.md](CLAUDE-DNA-CC.md) — redirect stub (compatA, à supprimer une fois tous les projets migrés)

## Actions Guillaume en attente

- `chatSyncDNAChatOk` — uploader `CLAUDE-DNA-CHAT.md` v1.8 dans Instructions globales claude.ai (hérité v1.8, pas créé cette session).
- **Mettre à jour `DNA_URL` dans chaque projet client** (hook `.claude/hooks/session-start.sh`) :
  - `https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC.md` → `…/CLAUDE-DNA-CC-CORE.md`
  - Et copier `CLAUDE-DNA-CC-CORE.md` localement si on veut le mode `local` (sinon `curl` fonctionne).
  - Projets connus à migrer : **ClaudeAchatMaison** (tracé en TODO M2 selon le brief Chat).

## Questions ouvertes pour prochaine session

- Tester `gauto` en vrai sur un projet (création RECAP-AUTO, boucle pilotée, rebase auto avant push).
- Quand supprimer `CLAUDE-DNA-CC.md` (redirect stub) ? → après migration de tous les hooks projets clients.
- Faut-il créer un `CLAUDE.md` projet pour `claude-os` lui-même (anomalie : actuellement absent à la racine) ?

## Options de reprise (prochaine session)

- `resA` — vérifier merge PR + lancer migration `ClaudeAchatMaison` (mise à jour `DNA_URL` + tests).
- `resB` — créer `CLAUDE.md` projet manquant pour claude-os.
- `resC` — réviser CLAUDE-DNA-CHAT.md pour ajuster les références "DNA-CC.md" → "DNA-CC-CORE/REF.md" dans le Core répliqué.
- `resD` — premier test de `gauto` sur un projet réel (vérifier la boucle complète + RECAP-AUTO).
