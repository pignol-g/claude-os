---
name: routine-credit
description: >
  Routine de décision qui, en fonction du crédit hebdomadaire restant, décide s'il faut
  lancer une passe d'avance autonome (skill gauto) pour consommer utilement le surplus de
  quota plutôt que de le perdre. À utiliser en exécution planifiée (trigger quotidien) ou
  quand Guillaume écrit « routine crédit », « passe crédit », « check crédit ». N'a PAS
  d'accès programmatique au crédit (confirmé par la doc CC) : lit le dernier commentaire
  daté de la tâche Asana « Crédit hebdo » où Guillaume colle chaque jour son % d'usage +
  l'heure de reset, et applique une formule calendaire. Ne lance jamais rien sans matière
  fraîche.
---

# routine-credit — déclencheur d'avance autonome selon le crédit restant

> **Décision Guillaume (tâches Asana 168 + 171, GO 2026-07-01/02).** But : les ~20 % de
> quota quotidiens sont perdus s'ils ne sont pas consommés. Cette routine détecte le
> **surplus** (« on est en avance de consommation ») et lance une passe utile pour le brûler.
> Elle **décide** ; elle ne fait pas le travail elle-même — le travail, c'est `gauto`.

## Pourquoi une entrée manuelle (et pas une mesure auto)

Recherche doc faite (doc officielle CC + issue #44328) : **aucun accès programmatique fiable
au crédit hebdo**.

- `/usage` est **interactif**, calculé depuis l'**historique local de la machine**, et
  **n'inclut pas claude.ai ni les autres appareils**. Or la limite de Guillaume est partagée
  CC + claude.ai → ce chiffre serait faux pour ce besoin.
- Pas de commande `claude usage` ni d'endpoint exposant le % restant (feature request #44328).
- Hook `StopFailure` (matcher `rate_limit`) : **réactif** (limite déjà atteinte), pas le %
  restant.
- OpenTelemetry : compteurs de tokens, pas le % de limite hebdo.

**Conclusion, actée avec Guillaume : plan B calendaire.** Une tâche Asana dédiée où il colle
chaque jour un commentaire **daté** avec son % d'usage + l'heure de reset. La routine lit ce
commentaire et calcule.

## Entrée (source de vérité)

Tâche Asana **« Crédit hebdo — photo/% quotidien »** (projet Claude, lane « a travailler
Guillaume ») :
`https://app.asana.com/1/1201637952171333/project/1208173596025068/task/1216088523150608`

Guillaume y poste chaque jour un commentaire **daté** du type :

```
55% — reset vendredi 21h
```

(ou une photo de l'écran `/usage` accompagnée du % et de l'heure de reset).

La routine prend la **date du commentaire** comme « maintenant ». Elle lit **le dernier
commentaire daté** (ignorer les commentaires `[Claude]`).

## Logique de décision

1. Budget hebdo = **100 %** ; rythme quotidien attendu = **100 / 7 ≈ 14,3 %/jour**.
2. Déterminer le **jour courant** = date du commentaire ; et le **jour/heure de reset** (dans
   le texte du commentaire).
3. `jours_restants` = nombre de **jours entiers** avant le prochain reset.
4. `usage_attendu = 100 − (100 / 7) × jours_restants`.
   *(= là où l'usage « devrait » être si on consomme linéairement et qu'on veut finir la
   semaine à 100 %.)*
5. **SI `usage_actuel < usage_attendu`** → on est **en avance / il reste du surplus** →
   **LANCER** la skill `gauto` (avance autonome : dérouler un backlog utile — voir « Contenu »).
6. **SINON** → clôturer la routine, **ne rien faire** (pas de surplus à brûler).

### Exemple (validé par Guillaume)

Reset **vendredi 21h**. On est **mercredi 21h** = J-2 → `jours_restants = 2`.
`usage_attendu = 100 − (100/7) × 2 = 71 %`. `usage_actuel = 55 %`.
`55 < 71` → **surplus** → on lance `gauto`.

## Contenu de la passe lancée (ce que fait `gauto` ici)

`routine-credit` est le **déclencheur** ; `gauto` (skill mode autonome) est le **contenu**.
Quand elle déclenche, `gauto` reçoit la consigne « brûler du crédit **utilement**, tâche libre »
(décision Guillaume 2026-07-01, tâche 171) :

1. **Prendre l'état réel** via les canaux dispo : derniers travaux (GitHub PRs/commits récents,
   projet Asana « Claude » file « pour claude »), REPRISE.md des repos.
2. **Lister les travaux en cours**, les **prioriser** (valeur opérationnelle).
3. Dérouler en priorité, si rien de plus prioritaire :
   - le backlog veille `candidaturePilote/veille/AMELIORATION-backlog.md` ;
   - l'enrichissement de fiches compagnies / pré-montage de dossiers (`livrables/dossiers/`) ;
   - une passe `decouverte-sources` ou `audit-veille`.
4. **1 passe = 1 commit + push** (grain anti-interruption), PR draft par tâche.

> Sans instruction claire de projet, c'est **volontaire** : Guillaume veut « brûler du crédit
> mais de manière utile ; toute tâche sera bonne à prendre ». Choisir la plus utile trouvée.

## Garde-fous

- **Pas de commentaire daté du jour dans la tâche « Crédit hebdo »** → **ne rien lancer**
  (ne pas deviner l'usage) et le **signaler** (commentaire court, ou log de routine).
- **Commentaire ambigu** (pas de %, ou pas d'heure de reset lisible) → ne rien lancer, demander
  la donnée manquante.
- Respecter tous les **Safety interdits** de `gauto` (CORE) : pas de merge PR sans validation
  explicite Guillaume, pas de force-push, pas de delete branch, pas de `--no-verify`, pas de
  modif hooks/settings.
- **Jamais d'envoi externe** (mail, candidature) — la passe reste interne (repo + Asana).
- Idempotence : si une passe a déjà tourné pour la journée, ne pas la relancer (vérifier
  l'activité git/Asana du jour avant de déclencher).

## Invocation & planification

- **Manuelle** : `/routine-credit`, « routine crédit », « check crédit ».
- **Planifiée** : trigger quotidien (routine Claude web), idéalement en soirée après que
  Guillaume ait posté son % du jour.
- **Sortie** : soit « rien à faire (usage ≥ attendu, ou pas de matière) », soit délègue à
  `gauto` et rend le compte rendu de la passe.
