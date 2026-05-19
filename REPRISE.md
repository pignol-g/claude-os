# REPRISE — claude-os

**Dernière session : 2026-05-19**

## État courant

DNA-CC v2.0 splité en CORE + REF (hot/cold split + lazy fetch via sommaire). Branche `feat/dna-v2-split-core-ref` poussée + PR ouverte.

- [CLAUDE-DNA-CC-CORE.md](CLAUDE-DNA-CC-CORE.md) — ~150 lignes, injecté par hook
- [CLAUDE-DNA-CC-REF.md](CLAUDE-DNA-CC-REF.md) — ~450 lignes, curl à la demande
- [CLAUDE-DNA-CC.md](CLAUDE-DNA-CC.md) — redirect stub (compatA, à supprimer une fois tous les projets migrés)
- [.claude/hooks/session-start.sh](.claude/hooks/session-start.sh) — `DNA_URL` pointe vers CORE
- `CLAUDE-DNA-CHAT.md` — inchangé v1.8 (splitChatB : pas de hook claude.ai → pas de gain)

## Actions Guillaume en attente

- `chatSyncDNAChatOk` — uploader `CLAUDE-DNA-CHAT.md` v1.8 dans Instructions globales claude.ai (hérité v1.8, pas créé cette session).
- **Mettre à jour `DNA_URL` dans chaque projet client** (hook `.claude/hooks/session-start.sh`) :
  - `https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC.md` → `…/CLAUDE-DNA-CC-CORE.md`
  - Et copier `CLAUDE-DNA-CC-CORE.md` localement si on veut le mode `local` (sinon `curl` fonctionne).
  - Projets connus à migrer : **ClaudeAchatMaison** (tracé en TODO M2 selon le brief Chat).

## Questions ouvertes pour prochaine session

- Quand supprimer `CLAUDE-DNA-CC.md` (redirect stub) ? → après migration de tous les hooks projets clients.
- Faut-il créer un `CLAUDE.md` projet pour `claude-os` lui-même (anomalie : actuellement absent à la racine) ?

## Options de reprise (prochaine session)

- `resA` — vérifier merge PR + lancer migration `ClaudeAchatMaison` (mise à jour `DNA_URL` + tests).
- `resB` — créer `CLAUDE.md` projet manquant pour claude-os.
- `resC` — réviser CLAUDE-DNA-CHAT.md pour ajuster les références "DNA-CC.md" → "DNA-CC-CORE/REF.md" dans le Core répliqué.
