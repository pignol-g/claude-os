# CLAUDE-DNA-CC — Redirect stub (v2.0)

**Version : v2.0-redirect — 2026-05-19**

<!-- Ce fichier est conservé en backward compat (compatA) pour les hooks projet qui pointent encore vers CLAUDE-DNA-CC.md. -->
<!-- Le DNA-CC a été splité en deux fichiers depuis v2.0 (2026-05-19) — voir ci-dessous. -->
<!-- Version : 2026-05-19 v2.0-redirect -->

---

## DNA-CC splité en CORE + REF depuis v2.0

Ce fichier monolithique n'est plus le master. Le DNA-CC vit désormais en deux fichiers complémentaires :

| Fichier | Rôle | Quand le charger |
|---|---|---|
| [`CLAUDE-DNA-CC-CORE.md`](CLAUDE-DNA-CC-CORE.md) | Règles actives (~150 lignes) — Posture, Q/R, gpose, économie tokens, comportements CC, sommaire des procédures rares | **À chaque session** (injecté par le hook SessionStart) |
| [`CLAUDE-DNA-CC-REF.md`](CLAUDE-DNA-CC-REF.md) | Procédures rares (~450 lignes) — archi CC↔Chat, templates, bootstrap, migration, historique | **À la demande** quand un trigger du sommaire CORE est rencontré (curl raw GitHub) |

### Si tu lis ce fichier en contexte CC

Tu es probablement chargé par un hook projet legacy (DNA v1.x) dont le `DNA_URL` pointe encore vers `CLAUDE-DNA-CC.md`. Pour que la session soit complète :

```bash
curl -s https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-CORE.md
```

Et signaler à Guillaume que le hook projet doit être mis à jour (cf. section [#migrate-projet](CLAUDE-DNA-CC-REF.md#migrate-projet) du REF).

### Raw URLs

- CORE : `https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-CORE.md`
- REF : `https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-CC-REF.md`

### Quand supprimer ce fichier

Une fois tous les projets clients migrés vers `DNA_URL=…CORE.md` (cf. checklist dans le projet master claude-os). À ce moment : `git rm CLAUDE-DNA-CC.md` et bump DNA v2.1.
