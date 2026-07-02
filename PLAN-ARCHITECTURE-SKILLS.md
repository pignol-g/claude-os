# Plan — architecture « skills & routines » (proposition)

> **Statut : PROPOSITION à valider.** Rédigé en réponse à la tâche Asana
> « Amélioration continue architecture claude » (projet Claude, section « pour claude »).
> Rien n'est implémenté : ce document reformule, propose des chantiers chiffrés et pose les
> questions qui bloquent la décision (posture `gpose`). Sur GO de Guillaume, chaque chantier
> devient une PR dédiée.

## 1. Reformulation de la demande

Guillaume veut faire **évoluer l'architecture Claude** de « gros DNA monolithique + quelques
skills » vers un modèle **davantage composé de skills et de routines**, avec en particulier :

1. **Convertir les triggers `gpose` et `gauto`/`gstop` en skills** (aujourd'hui ce sont des
   comportements écrits en dur dans `CLAUDE-DNA-CC-CORE.md`).
2. **Créer une skill de création de LM** (lettre de motivation).
3. **Composer des skills entre elles** — ex. une skill « création de dossier candidature »
   qui appelle la skill « création de LM » **et** une skill « mise à jour CV ».

## 2. État des lieux (ce qui existe déjà)

**Le DNA (instructions longues, chargées au démarrage)**
- `CLAUDE-DNA-CC-CORE.md` (~150 l, injecté à chaque session par le hook) — contient en dur :
  posture, choix de modèle, **`gpose`** (§combo réflexion), **`gauto`/`gstop`** (§combo autonome),
  inbox `q:`, TODO projet, voix de Guillaume…
- `CLAUDE-DNA-CC-REF.md` (~450 l, curlé à la demande) — procédures rares.
- `CLAUDE-DNA-CHAT.md`, `CLAUDE-DNA-ASANA.md`, `profil-redactionnel-guillaume.md`.

**Les skills existantes**
- `claude-os` : `asana-pass` (1 seule).
- `candidaturePilote` : `analyse-offre`, `audit-veille`, `recherche-compagnie`,
  **`lm-francaise`** (composer une LM FR à la voix de Guillaume, ancrée corpus 2024),
  **`voix-guillaume`** (rédiger à sa voix, charge le profil rédactionnel).
- `deep-research` existe déjà (harness/claude-os) — fan-out web + vérif adverse + rapport cité.

**Point important déjà en place** : la « création de LM » n'est **pas** un vide — `lm-francaise`
+ `voix-guillaume` couvrent déjà l'essentiel, mais **scopées au projet pilote**. Le CV a une
source structurée : `candidaturePilote/livrables/cv/cv-data-complete.md` (+ exports docx/pdf).

## 3. Principe directeur proposé

> **Le DNA garde les *règles de posture* toujours actives ; les *procédures* déménagent en
> skills. Une skill = 1 source de vérité, invocable, composable. Le DNA ne fait plus que
> *pointer* vers la skill (trigger fin), il ne recopie plus la procédure.**

Bénéfices : CORE plus léger (moins de tokens injectés à chaque session), procédures versionnées
et testables une par une, réutilisation entre projets, composition explicite.

**Tension à trancher (cf. Q1)** : `gpose`/`gauto` se déclenchent aujourd'hui par un **mot-clé
n'importe où dans un message** (« gpose » en milieu de phrase). Une skill s'invoque
explicitement (`/nom`) ou par matching de description. Pour ne pas perdre le déclenchement
inline, le patron recommandé est **hybride** : garder dans le CORE une ligne-trigger minimale
(« si `gpose` apparaît → invoquer la skill `gpose` ») et déplacer **tout le corps** de la
procédure dans la skill. Le CORE maigrit sans casser l'ergonomie.

## 4. Chantiers proposés

### Chantier A — `gpose` en skill
- Créer `claude-os/.claude/skills/gpose/SKILL.md` : reprend le corps actuel (reformuler →
  expliquer → proposer 2-4 options chiffrées → poser les questions Q/R).
- Dans `CORE`, remplacer le bloc §« Combo réflexion » par un trigger d'1-2 lignes pointant la skill.
- **Coût** : ~1 PR courte, faible risque. Réversible.

### Chantier B — `gauto`/`gstop` en skill (ou routine)
- Créer `claude-os/.claude/skills/gauto/SKILL.md` : boucle pilotée, persistance/git, économie API,
  conditions d'arrêt, **safety interdits** (pas de merge/force-push/delete-branch/--no-verify).
- Idem CORE : trigger minimal + pointeur.
- **Nuance** : `gauto` est une *boucle longue durée* → c'est plutôt une **routine** qu'une skill
  ponctuelle. À décider si on la modélise comme skill invocable ou comme routine planifiée
  (cf. Q2). Les **safety interdits restent dans le CORE** (garde-fous non déportables).
- **Coût** : ~1 PR moyenne, risque moyen (comportement autonome — bien tester la boucle).

### Chantier C — skill « création de LM » (globale)
- **Ne pas repartir de zéro** : `lm-francaise` + `voix-guillaume` existent déjà (pilote).
- Deux options (cf. Q3) : (C1) **promouvoir** une skill LM générique dans `claude-os` qui
  délègue à `voix-guillaume` pour la voix ; (C2) **garder** `lm-francaise` projet et n'exposer
  qu'un point d'entrée commun. Recommandation : **C2 d'abord** (moins de duplication), promotion
  globale seulement si un 2ᵉ projet a besoin de LM.
- **Coût** : faible si C2 (essentiellement du câblage + description).

### Chantier D — skill « mise à jour CV »
- **Nouveau** : pas de skill CV aujourd'hui. Source de vérité = `livrables/cv/cv-data-complete.md`.
- Skill = met à jour les heures de vol / qualifs, régénère les exports, journalise la version.
- **Pré-requis** : figer la **source de vérité CV** et le format d'export attendu (cf. Q4).
- **Coût** : moyen (dépend du niveau d'automatisation des exports docx/pdf).

### Chantier E — skill composite « dossier candidature »
- `dossier-candidature/SKILL.md` : orchestre le montage d'un dossier complet en **appelant**
  les skills C (LM) et D (CV), plus `recherche-compagnie` et le rapport commuting.
- La composition en Claude Code = la SKILL.md du composite **invoque** les sous-skills (référence,
  pas copie). S'aligne sur ce que fait déjà la routine `analyse-offre` (pré-montage `livrables/dossiers/`).
- **Coût** : à faire **en dernier** (dépend de C et D). Risque : bien définir le contrat d'entrée/sortie
  de chaque sous-skill pour que la composition soit fiable.

## 5. Séquencement recommandé

1. **A (`gpose`)** — le plus simple, valide le patron « CORE pointe, skill contient ».
2. **B (`gauto`)** — même patron, une fois A éprouvé.
3. **C + D** en parallèle (LM câblage + CV nouvelle).
4. **E (composite)** — quand C et D sont stables.

Chaque étape = 1 PR draft dédiée, branche par chantier, validation avant merge (jamais de
migration lourde silencieuse — cf. DNA-REF §migration).

## 6. Questions ouvertes (à trancher avant de coder)

- **Q1 — patron trigger** : on garde bien le modèle **hybride** (trigger inline minimal dans le
  CORE + corps en skill), pour ne pas perdre le déclenchement `gpose`/`gauto` en milieu de phrase ? (recommandé : oui)
- **Q2 — `gauto` : skill ou routine ?** Le modélise-t-on en **skill invocable** (comme `gpose`)
  ou en **routine planifiée** (boucle longue durée, cohérente avec les routines nocturnes existantes) ?
- **Q3 — skill LM** : **C1** (skill LM globale dans claude-os) ou **C2** (garder `lm-francaise`
  projet + point d'entrée commun) ? (recommandé : C2)
- **Q4 — CV** : confirme-t-on `cv-data-complete.md` comme **source de vérité** unique, et jusqu'où
  automatiser les exports (docx/pdf régénérés par script, ou édition manuelle laissée à Guillaume) ?
- **Q5 — périmètre du composite E** : le « dossier candidature » doit-il **créer aussi la tâche
  Asana « à postuler »** (comme la routine `analyse-offre` aujourd'hui), ou s'arrêter au dossier prêt ?

## 7. Ce que je ne fais pas sans GO

Aucune modification du CORE, aucun déplacement de `gpose`/`gauto`, aucune création de skill tant
que Guillaume n'a pas validé le principe (§3) et répondu aux questions (§6). Sur GO — même partiel,
p.ex. « lance A » — j'ouvre la PR du chantier concerné.
