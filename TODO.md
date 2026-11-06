# TODO — claude-os

## 🔴 Prioritaire

## ⏳ À faire / en cours

- [ ] Skill `gdoc` v0.2 : l'arriéré par passes de 20–25 fichiers (Guillaume copie d'abord le dossier Dropbox dans la boîte Drive) ; mise à jour de la skill avec les coûts réels de chaque passe — la passe test de 20 fichiers a été appliquée le 2026-11-06 (2026-11-06)
- [ ] DNA privé et canal Chat ↔ Code : étude dans `general/perso/securite/` (privé), en attente du choix de Guillaume (`dnaPrive`, `canal`) ; ensuite, session dédiée « refonte de `claude-os` » (2026-11-06)

## ⏸️ Plus tard / idées

- [ ] `gdoc` différé (décision `docPorteeA`) : texte intégral à la demande, Actions Asana pour les échéances repérées, passage en Routine avec `gquota`, indexation du coffre existant (session locale à part), arriéré du dossier Dropbox à copier dans le Drive par Guillaume (2026-11-06)
- [ ] Purge de l'historique des repos privés (décision `secuHistorique` B) : plan dans `general/perso/securite/`, en attente de l'accord de Guillaume (`purge`) ; ne rien supprimer ni réécrire avant (2026-11-06)
- [ ] Purger toutes les PR ouvertes en attente, tous repos sauf `T7` — grand ménage voulu par Guillaume « plus tard, pas tout de suite » ; état au 2026-10-20 : `ClaudeAchatMaison` 11 ouvertes dont 2 brouillons (#46, #47), `general` 6 (#11, #12, #15 à #18), `claude-os` 0, `candidaturePilote` 18 dont 13 brouillons (#29 à #305 ; une revue de 42 PR y avait déjà été faite en juillet, #133). Méthode à proposer avant d'agir : merger ce qui est propre, résoudre les conflits seul, clore l'obsolète, n'avertir que sur arbitrage de fond (2026-10-20) @github
- [ ] Skill `asana-revue` v0.2 — modes quotidien court (≈ 5 min) puis hebdomadaire (lundi), après 3 revues manuelles ; mesurer la durée d'une revue avec cache (cible 15-25 min) ; passage en Routine = décision de Guillaume, avec garde-quota `gquota` (2026-10-28)
- [ ] Ménage de l'inbox Asana (~200 tâches non triées) — à proposer à part, hors revue (2026-10-28)

## ✅ Fait (archive courte — élaguer régulièrement)

- [x] Skill `asana-revue` v0.1 (trigger `grevue`, CORE v3.9, ASANA v1.2) : revue en delta de toutes les tâches Asana hors `T7`, planning à deux voies, état et carnet de préférences dans `general/perso/revue-asana/` — décision `skillRevueA` (2026-10-28)
- [x] Merge de PR automatique, tous repos sauf `T7` — règle `mergeAuto` (CORE v3.7), persistée dans le `CLAUDE.md` de chaque projet (2026-10-20)
