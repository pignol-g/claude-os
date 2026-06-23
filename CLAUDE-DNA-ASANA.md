# CLAUDE-DNA-ASANA — Doctrine d'usage Asana de Guillaume (système « nous 3 »)

**Version : v1.0 — 2026-06-23**

<!-- Module autonome de la famille CLAUDE-DNA. Décrit comment Guillaume, Claude -->
<!-- et Asana travaillent ensemble sur l'ENSEMBLE des projets (pas que Pilote). -->
<!-- Raw : https://raw.githubusercontent.com/pignol-g/claude-os/main/CLAUDE-DNA-ASANA.md -->
<!-- À câbler dans CLAUDE-DNA-CC-CORE.md (sommaire procédures) + CLAUDE-DNA-CHAT.md (Référence). -->

> Cette doctrine ne réinvente rien : elle formalise le système que Guillaume avait
> déjà écrit dans ses projets Asana « Utilisation ASANA » et « Organisation »
> (compte rendu semaine 24), puis dilué sur ~29 projets. Le but est de le
> réappliquer et de brancher Claude dessus comme moteur.

---

## 1. Le système « nous 3 »

Trois acteurs, trois rôles non interchangeables.

| Acteur | Rôle | Fait | Ne fait pas |
|---|---|---|---|
| **Guillaume** | Décideur + main humaine | Tranche, valide/édite les brouillons, exécute les Actions assignées (postuler, envoyer, passer un entretien), archive les projets | Le travail de tenue/synchro de routine |
| **Claude** | Moteur | Tient les Dossiers/Ressources à source de vérité (ex. candidatures→JSON), génère les Actions datées, rédige les comptes-rendus, relie chaque session à ses tâches | Décider à la place de Guillaume ; rien de destructif sans accord |
| **Asana** | Couche opérationnelle | Porte les Actions du jour, les rappels mobile, le board d'avancement | Stocker l'historique/la donnée de référence (sauf Ressources) |

---

## 2. Les trois types d'objets (vocabulaire Guillaume)

| Objet | Définition | Assigné ? | Se ferme ? | Vit dans |
|---|---|---|---|---|
| **Action** | une chose concrète à faire | oui | oui | une section de board, datée |
| **Dossier** (« pro-tâche ») | un mini-projet ; ses sous-tâches listent/structurent | non | jamais | une section « Dossiers » |
| **Ressource** | donnée de référence (liste, lien, note) | non | jamais | une section « Ressources » |

Règle d'or de Guillaume : **on n'assigne que les Actions, jamais les Dossiers ni les Ressources.**

---

## 3. La loi fondatrice (anti-divergence)

> « Avoir des tâches qui s'ouvrent et se ferment, alors que la donnée reste
> accessible et vivante. » — Guillaume, compte rendu semaine 24.

Conséquence : **une donnée, un seul propriétaire.** On ne duplique jamais la même
information aux deux endroits (le piège Excel↔JSON du projet candidaturePilote).

| Nature de l'info | Propriétaire unique |
|---|---|
| Action à faire + échéance + rappel | **Asana** (Action) |
| État / historique d'un objet qui a une source de vérité git (candidatures) | **le JSON du repo** (ex. `candidaturePilote/data/candidatures.json`) → dashboard |
| Donnée de référence sans source git | **Asana** (Ressource) |

Pont : un objet suivi des deux côtés porte une référence croisée (l'Action cite
l'id JSON + le lien dashboard ; le JSON porte `asana_task_gid`).

---

## 4. Périmètre des outils (MCP Asana) — qui peut quoi

Le serveur MCP Asana exposé à Claude est **partiel**. À connaître pour répartir le travail.

| Capacité | Claude (MCP) | Guillaume (UI, 2 clics) |
|---|---|---|
| Créer un projet (avec sections) | oui | oui |
| Créer / déplacer / dater / assigner / clôturer une tâche | oui | oui |
| Déplacer une tâche entre projets / sections (si la section existe) | oui | oui |
| Poster un compte-rendu (status update) | oui | oui |
| Commenter, supprimer une tâche | oui | oui |
| **Créer une section dans un projet EXISTANT** | **non** | oui |
| **Archiver / supprimer un projet** | **non** | oui |

Donc : Claude prépare et migre ; **Guillaume crée les sections d'un projet existant
et archive les projets** (c'est aussi sain que ce soit sa main sur le destructif).

---

## 5. Le rythme hebdomadaire

| Moment | Acteur | Quoi |
|---|---|---|
| **Lundi — Planning** | Claude | Poste le plan de la semaine : Actions dues, livrables produits, décisions à prendre. Dans le projet « Organisation ». |
| **Quotidien** | Guillaume | Ouvre « Mes tâches » → les Actions du jour (rappels mobile). |
| **Vendredi/dimanche — Compte-rendu** | Claude | Récap hebdo par projet actif, en status update (« Aperçu »). |

Le rythme couvre **tous les projets vivants** (Bébé, Départ d'InAdvans, Vie/Santé,
Pilote…), pas seulement Pilote.

---

## 6. QG de la collaboration (rôles séparés)

| Projet | Rôle |
|---|---|
| **Organisation** | Planning du lundi + comptes-rendus transverses. Le « poste de pilotage ». |
| **Claude** | Atelier des livrables produits ensemble (candidatures, voix, scripts…), avec lien `claude.ai/code` par tâche. |

---

## 7. Conventions

- **Pas d'emoji décoratif** (règle DNA générale). Les préfixes de section sont textuels.
- **Lier les sessions** : toute tâche issue d'un travail Claude porte en notes le lien `claude.ai/code/session_…`.
- **Dédoublonnage** : une intention = une seule tâche. Avant de créer, vérifier l'existant.
- **Q/R codes** (cf. CORE) pour tout choix posé à Guillaume.
- **Ne jamais clôturer un Dossier ou une Ressource** ; on ne ferme que des Actions.

---

## 8. Cible de structure (refonte — état d'avancement)

Décidée le 2026-06-23. Avancement tenu à jour ici.

**Phase 1 — Dégonfler la galaxie pilote**
- Fusionner les doublons projet↔section : `Ryanair`, `Anglais`, `TOEIC`, `FCL055` → sections de `Pilote`.
- Archiver les projets terminés : `UPRT` (18/18), `Planification` (4/4).
- Créer dans `Pilote` la section pipeline candidatures plan B (board par statut : À postuler → Postulé → Relance → Entretien → Réponse → Clos).

**Phase 2 — Archiver le passé** : `New York`, `Écosse 2024`.

**Phase 3 — Requalifier les listes** : `Pauline`, `Ressources/Listes/Aides`, etc. → marquées « Ressource » (jamais d'Action assignée dessus).

**Phase 4 — Câbler le rythme** : §5 + §6 actifs.

> Rappel §4 : la création de sections dans `Pilote` et les archivages sont des
> actions UI de Guillaume ; Claude migre les tâches une fois les sections créées.

---

## Historique

| Version | Date | Changements |
|---|---|---|
| v1.0 | 2026-06-23 | Création. Formalise le système « nous 3 » (Guillaume/Claude/Asana), les 3 types d'objets, la loi anti-divergence, le périmètre MCP, le rythme hebdo, le QG, la cible de refonte. |
