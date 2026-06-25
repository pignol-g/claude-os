---
name: asana-anti-interruption
description: >
  Protocole anti-interruption pour le travail Asana de Guillaume (projet « Claude »,
  routine asana-pass, sessions web autonomes gauto). Encode comment survivre à une
  EXTINCTION DE CRÉDITS / fin de session (plan Pro, quota hebdo serré) en cours de passe :
  le board Asana EST l'état durable, chaque tâche est une unité atomique « bouclée jusqu'au
  board », et une mort subite ne coûte au pire qu'une tâche en vol, reprise sans ambiguïté.
  À charger en complément de asana-pass dès qu'une passe traite plusieurs tâches, qu'une
  tâche est longue/multi-étapes, ou en exécution planifiée Claude web. Triggers : « anti
  interruption », « anti coupure », « survie session », « passe Asana sûre », ou quand
  l'extinction de crédits / la limite de session menace une passe en cours.
---

# asana-anti-interruption — survivre à l'extinction de crédits en cours de passe

Module opérationnel qui durcit `asana-pass` (et toute passe Asana en `gauto` / routine
web) contre la **condition d'arrêt (a) « Extinction crédits / session limit atteint »**
(`CLAUDE-DNA-CC-CORE.md` §gauto Arrêt). Sur le plan **Pro** (quota hebdo serré), une
session web peut mourir **à n'importe quel turn**. Ce protocole garantit qu'une mort
subite ne perd jamais de travail et n'exige **aucune mémoire de conversation** pour
reprendre.

> **Doctrine de référence** : `CLAUDE-DNA-ASANA.md` (système « nous 3 ») et `asana-pass`
> (la passe elle-même). En cas de divergence, **la doctrine prime**. Ce module n'ajoute
> pas d'étape métier — il fixe **l'ordre et le grain** de ce que `asana-pass` fait déjà.

## Principe fondateur — le board EST l'état durable

La loi anti-divergence (`CLAUDE-DNA-ASANA.md` §3) dit déjà : la donnée vit dans son
propriétaire unique, pas en mémoire de conversation. Conséquence directe ici :

> **L'état d'avancement d'une passe se lit entièrement sur Asana** : la **lane** d'une
> tâche dit à qui de jouer ; ses **commentaires `[Claude]`** disent ce qui est déjà fait.
> Aucun scratch local, aucune mémoire chat. Une session fraîche qui relance la passe
> repart exactement où la précédente est morte, **sans rien savoir d'elle**.

Tout le protocole découle de cette idée : rendre chaque tâche **bouclée-au-board** de
façon atomique et **idempotente**, pour qu'une reprise soit toujours « finir ou ne rien
faire », jamais « dupliquer ».

## Invariant 1 — une tâche bouclée-au-board, dans cet ordre

Traiter **une seule tâche à la fois**, jusqu'au bout, avant de toucher la suivante.
« Jusqu'au bout » = ces 4 sous-étapes **dans cet ordre précis** :

1. **Faire le travail** (répondre / agir, cf. asana-pass §4).
2. **Persister le livrable repo** s'il y en a un : écrire le markdown dans le bon repo,
   `commit` + `push`. (Réponse longue → fichier repo + lien, cf. asana-pass §4.)
3. **Poster le commentaire** signé `[Claude] ` (qui *référence le lien déjà poussé*).
4. **Déplacer la lane** vers « à lire / valider » — **en DERNIER**.

Le **déplacement de lane est le point de commit** de la tâche. Tant qu'il n'a pas eu
lieu, la tâche reste dans la file d'entrée et sera simplement **re-traitée** par la
prochaine session. L'ordre 2→3 garantit qu'un commentaire ne **link jamais un fichier
non poussé** ; l'ordre 3→4 garantit qu'une tâche n'arrive **jamais en « à lire /
valider » sans sa réponse**.

## Invariant 2 — chaque sous-étape idempotente (reprise = finir, pas dupliquer)

La mort peut frapper **entre** deux sous-étapes. Donc chaque sous-étape doit être **sûre
à refaire**. Avant d'agir sur une tâche de la file d'entrée, vérifier ce qui est déjà fait :

- **Commentaire déjà posté ?** Lire le fil : si le **dernier** commentaire `[Claude]`
  répond déjà à la consigne courante de Guillaume (cf. asana-pass : dernier commentaire
  non préfixé `[Claude]` = consigne), **ne pas re-répondre** → passer directement au
  déplacement de lane (sous-étape 4). La session précédente est morte entre 3 et 4.
- **Livrable déjà poussé ?** `git status` + chercher le fichier attendu avant de
  réécrire : le commit a peut-être déjà eu lieu. Ne pas créer de doublon de fichier.
- **Lane déjà déplacée ?** Une tâche en « à lire / valider » n'est plus dans la file
  d'entrée → asana-pass l'ignore déjà (balle côté Guillaume). Rien à faire.

Résultat : re-traiter une tâche « en vol » est toujours un **no-op-ou-finition**, jamais
un dédoublement de commentaire ou de fichier.

## Invariant 3 — tâche longue : breadcrumb « EN COURS » sur le board

Si **une seule** tâche demande un travail multi-étapes qu'un turn ne peut pas boucler
sûrement (long research, gros livrable), déposer un **fil d'Ariane sur le board** pour
qu'une session fraîche reprenne **au milieu** de la tâche :

- Poster un commentaire court `[Claude] EN COURS — <étape atteinte / prochaine étape>`,
  **mis à jour** au fil de l'eau (ou ré-posté), puis **remplacé par la réponse finale**
  quand la tâche est bouclée (sous-étape 3 ci-dessus).
- La tâche **reste dans la file d'entrée** pendant tout ce temps (lane = « pas fini »).
  Une reprise lit le breadcrumb et continue ; elle ne recommence pas de zéro.
- Préférer toujours **sous-découper** une tâche longue en livrables intermédiaires
  commités (asana-pass §4 + CORE Posture) : chaque commit poussé est du progrès qui
  survit, indépendamment d'Asana.

## Invariant 4 — ordre de passe : perte minimale d'abord (dimension crédit)

Le crédit peut s'éteindre à tout moment ; ordonner la passe pour qu'une coupure perde
le **moins** possible :

- **Tâches atomiques / rapides d'abord** : chacune est bouclée-au-board vite, donc
  définitivement acquise tôt. Plus on avance, plus le board reflète de tâches finies.
- **Tâches lourdes (1 grosse) en dernier** : on ne risque le travail coûteux qu'une fois
  le maximum de tâches déjà sécurisées sur le board.
- **Annoncer le budget** avant une grosse passe (CORE §Économie tokens) : nombre de
  tâches, estimation, recommandation de modèle. Si la passe est large, la faire **par
  vagues** — chaque vague laisse des tâches **entièrement** bouclées, jamais N tâches à
  moitié faites.

## Invariant 5 — dernier turn propre (miroir CORE §gauto Arrêt)

Les 3 conditions d'arrêt (extinction crédits / `gstop` / bouton stop) imposent toutes un
**dernier turn propre**. Traduction pour une passe Asana :

- Si une tâche est **en vol** : la **boucler au board** si possible (commentaire + lane),
  sinon la **laisser intacte dans la file d'entrée** (jamais à moitié déplacée) avec son
  breadcrumb `EN COURS`. **Ne jamais** laisser une tâche en « à lire / valider » sans sa
  réponse.
- **Commit + push** de tout livrable repo en cours (rien en mémoire seule).
- **Récap chat** final (asana-pass §8) : tâches bouclées, tâche éventuellement en vol +
  son breadcrumb, où une reprise repartira.

## Garde-fous

- **Rien d'externe à cheval sur une coupure possible** : ne jamais *commencer* un envoi
  mail / candidature près d'une limite de crédit — ces gestes sont de toute façon la main
  de Guillaume (doctrine §1) et n'ont pas de point de commit idempotent.
- **Jamais `completed`** (asana-pass) : la validation reste la main de Guillaume. Le
  point de commit d'une tâche côté Claude, c'est le **déplacement de lane**, pas la
  complétion.
- **Toujours signer `[Claude] `** : sans la signature, l'idempotence de l'invariant 2
  casse (impossible de distinguer ma réponse déjà postée d'une consigne de Guillaume).
- **Reprise = relancer asana-pass**, simplement. Aucune commande spéciale : la passe
  re-sélectionne « tout sauf à lire / valider » et les invariants 1–2 font le reste.
