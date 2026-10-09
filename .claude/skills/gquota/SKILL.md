---
name: gquota
description: Garde-quota des Routines Claude Code Remote de Guillaume. Répond GO ou STOP selon la fenêtre 5 h et le quota hebdo, pour que la routine ne consomme que le reliquat des jours déjà écoulés de la semaine (reset vendredi 21h Paris) et s'arrête avant le reset. À invoquer au début d'une routine qui l'intègre, puis avant chaque nouvelle étape, ou quand Guillaume écrit `gquota`. Tourne en fork Haiku ; tout le calcul est fait par un script, le modèle ne fait que lire 3 valeurs.
model: haiku
context: fork
background: false
allowed-tools: Bash, mcp__claude-code-remote__list_events
---

# gquota — garde-quota des routines

Tu exécutes une procédure mécanique. Ne raisonne pas sur le quota, ne recalcule rien : le
script décide. Ta réponse finale = **la ligne renvoyée par le script, telle quelle**.

## Procédure

1. Lancer `bash ${CLAUDE_SKILL_DIR}/quota-gate.sh sid`.
   Si la ligne commence par `STOP`, la renvoyer telle quelle et s'arrêter.
2. Appeler `mcp__claude-code-remote__list_events` avec `session_id` = la valeur obtenue,
   `kinds: ["rate_limit_event"]`, `limit: 100`.
   Si `data` est vide et `has_more` vaut true : rappeler avec `before_id` = `first_id`
   (3 pages au maximum).
3. Prendre le **dernier** élément de `data` (le plus récent). Sous
   `rate_limit_event.internal_anthropic_catchall.rate_limit_info.unifiedWindows`, relever :
   `five_hour.utilization`, `seven_day.utilization`, `seven_day.resetsAt`.
   Valeur introuvable (ou `data` toujours vide) → la remplacer par `x`.
4. Lancer `bash ${CLAUDE_SKILL_DIR}/quota-gate.sh check <five_hour.utilization> <seven_day.utilization> <seven_day.resetsAt>`
   (valeurs recopiées telles quelles, ex. `check 0.07 0.31 1792177200`).
5. Répondre uniquement par la ligne `GO …` ou `STOP …` du script.

## Intégration dans une routine

Bloc à coller dans le prompt de la routine (la routine doit tourner avec claude-os dans ses sources) :

```
Garde-quota : invoque la skill gquota au démarrage, puis avant chaque nouvelle étape.
- Réponse commençant par GO → continuer.
- Réponse commençant par STOP, ou pas de réponse exploitable → persister l'état si la routine
  le prévoit (ex. STATE.md + commit/push), puis terminer immédiatement en citant la ligne STOP.
- GO avec fin=HH:MM (fenêtre de fin de semaine) → ne lancer aucune étape qui ne finira pas avant HH:MM.
```

## Règles appliquées par le script

Décisions Guillaume du 2026-10-09 : `sess5hA`, `fenBurnA`, `recheckA`, `tauxB`, `quotaKOA`,
plus « garde économe » → fork Haiku + calcul en script.

- La semaine va du reset hebdo Anthropic (lu dans `seven_day.resetsAt`, vendredi 21h Paris) au suivant.
- **Jours révolus** = nombre de passages à 21h (heure de Paris) depuis le début de semaine.
  Pas de prorata : mercredi 05h ou 19h = 4 jours ; mercredi 21h = 5.
- **Seuil** = jours révolus × 100/7 − 10 %. GO seulement si l'hebdo est strictement sous le seuil.
- STOP si la fenêtre 5 h dépasse 80 %, ou si l'hebdo dépasse 80 %.
- **Fenêtre de fin de semaine** (vendredi 20h30-20h59) : seuil et plafond 80 % ignorés pour
  consommer le reliquat, fenêtre 5 h toujours vérifiée. **STOP dur à 20h59.**
- Donnée absente, illisible ou périmée → STOP.

| Période (heure de Paris) | Jours révolus | GO si hebdo < |
|---|---|---|
| ven 21h → sam 20h59 | 0 | jamais |
| sam 21h → dim 20h59 | 1 | 4,3 % |
| dim 21h → lun 20h59 | 2 | 18,6 % |
| lun 21h → mar 20h59 | 3 | 32,9 % |
| mar 21h → mer 20h59 | 4 | 47,1 % |
| mer 21h → jeu 20h59 | 5 | 61,4 % |
| jeu 21h → ven 20h29 | 6 | 75,7 % |
| ven 20h30 → 20h58 | fenêtre de fin de semaine | toujours (si 5 h ≤ 80 %) |
| ven 20h59 → 21h | coupure | jamais |

## Limites connues

- **CC cloud uniquement** : la source est l'événement `rate_limit_event` de la session. En
  local, `sid` répond STOP (pas de source fiable).
- Le chemin `internal_anthropic_catchall` est un champ interne, il peut changer sans préavis :
  dans ce cas le script répond STOP, jamais GO.
- La vérification se fait entre deux étapes : une étape déjà lancée n'est pas interrompue.
  Découper les routines en étapes courtes près des seuils.
- Tester le script sans session : `QG_NOW=<epoch> bash quota-gate.sh check 0.10 0.45 <resetsAt>`.
