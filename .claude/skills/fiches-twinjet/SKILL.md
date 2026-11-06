---
name: fiches-twinjet
description: >
  Fiches RH Twin Jet de Guillaume, remplies par script à partir du modèle déjà pré-rempli et signé
  (Dropbox) : « fiche de congé », « demande de congés », « pose de congés du … au … » (une ou
  plusieurs fiches d'un coup, PDF prêts à envoyer). Une seule commande, jamais de relecture des
  PDF. Fiche desiderata : pas encore (Guillaume doit déposer le modèle).
---

# fiches-twinjet — fiches RH Twin Jet par script

Décision de Guillaume, 2026-11-06 : aller vite, peu de tokens. Modèle suffisant : Haiku ou Sonnet.
Cette skill vit dans un repo **public** : aucun PDF, aucune signature, aucun identifiant ici.

## Fiche de congés

Le modèle est le PDF Dropbox déjà pré-rempli et signé (nom, case Twin Jet, signature). Le script
`remplir_conges.py` (dans ce dossier) y ajoute les dates du/au, la croix du type d'absence (congés
payés par défaut) et la date de la demande (aujourd'hui, heure de Paris). Positions figées dans le
script : **ne jamais lire ni analyser les PDF**.

1. **Dates** : une plage = `DEBUT..FIN` (`"30/12..03/01"`), un jour = `"21/12"`. Année absente =
   prochaine occurrence. Une dictée qui se répète ou se corrige (« au 3 décembre. Janvier ») :
   prendre l'interprétation la plus probable et l'annoncer. Un congé = une fiche.
2. **Modèle** : `ToolSearch` `select:mcp__Dropbox__download_link`, puis `download_link`
   (`expiration_in_sec` 900) sur
   `/pilote/selections compagnies/Twinjet/documents webcrm/Demande de congés ADM 100111V6CP (2).pdf`.
   Introuvable : `search` (`title_only`) « ADM 100111V6CP », puis demander lequel. Dropbox
   indisponible : demander à Guillaume de joindre le modèle et passer `--modele <fichier>`.
3. **Une commande** (dossier de sortie dans le scratchpad : sinon l'app ne peut pas ouvrir les PDF) :
   `python3 -I <dossier de cette skill>/remplir_conges.py --modele-url "<url>" --sortie "<scratchpad>/conges" "21/12" "30/12..03/01"`
   Options : `--type anticipation|sans-solde|familial` (défaut congés payés ; familial = justificatif
   à joindre), `--demande JJ/MM/AAAA` (défaut aujourd'hui), `--dry-run` (dates seules).
   Sortie : les dates lues, puis une ligne `OK <chemin>` par fiche (le script valide les dates
   avant de consommer le lien, vérifie le modèle, relit le texte de chaque fiche). `ECHEC` ou
   erreur : lire le message ; lien expiré ou déjà utilisé = nouveau `download_link`.
4. **Envoi** : `SendUserFile` des chemins `OK`. Réponse en 2-3 lignes : dates lues, type coché et date
   de demande (les deux hypothèses), ranger les PDF dans `demandes de congés/` (le connecteur
   Dropbox ne crée que du texte : pas d'écriture de PDF).

## Règles

- Le modèle est le fichier `… ADM 100111V6CP (2).pdf`, **pas** la fiche « été 2026 » (déjà datée :
  le script la refuse).
- Pas de rendu image ni de relecture du PDF produit : la ligne `OK` suffit. N'ouvrir un rendu que
  sur `ECHEC` ou si le formulaire a changé de révision.
- Jamais le modèle ni une fiche produite dans un repo (signature de Guillaume ; ce repo est public).
- Prérequis Python : `pypdf`, `reportlab` (présents dans l'image cloud ; sinon `pip install`).

## Maintenance

- Twin Jet change la révision du formulaire (réf. `ADM 100111V6/CP`) : re-mesurer les positions
  (méthode en tête du script).
- **Fiche desiderata** : à ajouter quand Guillaume dépose le modèle pré-rempli — même méthode
  (mesurer les champs une fois, `remplir_desiderata.py` à côté, mêmes appels). Suivi : `TODO.md`.
