---
name: fiches-twinjet
description: >
  Fiches RH Twin Jet de Guillaume, remplies par script à partir du modèle déjà pré-rempli et signé
  (Dropbox) : « fiche de congé », « demande de congés », « pose de congés du … au … », et « demande
  de desiderata », « désidératas », « je veux le week-end du … » (une ou plusieurs fiches d'un
  coup, PDF prêts à envoyer). Une seule commande, jamais de relecture des PDF.
---

# fiches-twinjet — fiches RH Twin Jet par script

Décisions de Guillaume, 2026-11-06 : aller vite, peu de tokens. Modèle suffisant : Haiku ou Sonnet.
Cette skill vit dans un repo **public** : aucun PDF, aucune signature, aucune adresse mail ici.

## Principe (3-4 appels)

Chaque fiche part d'un modèle Dropbox déjà pré-rempli et signé ; un script y met les dates (et le
reste), vérifie son résultat et affiche une ligne `OK <chemin>` par fiche. **Ne jamais lire ni
analyser les PDF.** Un congé ou un week-end = une fiche.

1. **Demande** : en tirer les arguments du script (plus bas). Une dictée qui se répète ou se
   corrige (« au 3 décembre. Janvier ») : prendre l'interprétation la plus probable et l'annoncer.
2. **Modèle** : `ToolSearch` `select:mcp__Dropbox__download_link`, puis `download_link`
   (`expiration_in_sec` 900) sur le chemin du modèle. Introuvable : `search` (`title_only`) sur son
   nom, puis demander lequel. Dropbox indisponible : demander à Guillaume de joindre le modèle et
   passer `--modele <fichier>`.
3. **Une commande Bash** :
   `python3 -I <dossier de cette skill>/<script> --modele-url "<url>" --sortie "<scratchpad>/fiches" <arguments>`
   Sortie dans le scratchpad, sinon l'app ne peut pas ouvrir les PDF. Le script valide les dates
   **avant** de consommer le lien (usage unique), vérifie le modèle, relit sa fiche. `--dry-run` =
   dates seules. `ECHEC` ou erreur : lire le message ; lien expiré ou déjà utilisé = nouveau
   `download_link`.
4. **Envoi** : `SendUserFile` des chemins `OK`, puis 2-3 lignes : dates lues, hypothèses (voir
   chaque fiche), PDF à ranger dans le Dropbox (le connecteur ne crée que du texte : pas
   d'écriture de PDF).

## Congés — `remplir_conges.py`

- Modèle : `/pilote/selections compagnies/Twinjet/documents webcrm/Demande de congés ADM 100111V6CP (2).pdf`
  (pas la fiche « été 2026 », déjà datée : le script la refuse). À ranger dans `demandes de congés/`.
- Arguments : un jour `"21/12"`, une plage `"30/12..03/01"` (année absente = prochaine occurrence).
  `--type anticipation|sans-solde|familial` (défaut congés payés ; familial = justificatif à
  joindre), `--demande JJ/MM/AAAA` (défaut aujourd'hui, Paris).
- Le script met : du/au, croix du type, date de la demande. Hypothèses à annoncer : type coché,
  date de la demande.

## Desiderata — `remplir_desiderata.py`

- Modèle : `/pilote/selections compagnies/Twinjet/documents webcrm/demande de désidératas/Formulaire Demande de desiderata.pdf`
  (exemple pré-rempli et signé ; PDF à champs : date de la demande, du, au, soit, motif sont
  remplacés, la section « Responsable » reste vide). À ranger dans `demande de désidératas/`.
- Arguments : `"we:06/06"` = le week-end (samedi + dimanche) qui contient cette date ; un jour
  `"16/01"` ; une plage `"23/01..24/01"`. `--motif "…"` (défaut « week-end famille », celui de
  l'exemple : à annoncer), `--demande JJ/MM/AAAA`, `--forcer` (jours de semaine).
- Règles (formulaire + note de service CST033, dans `documents webcrm/`) : samedi et dimanche
  uniquement (le script refuse le reste) ; demande au plus tard le 05 du mois pour le mois suivant
  (le script avertit sans bloquer : le redire à Guillaume) ; envoi par mail au RDOS avec copie à la
  gestion (adresses dans la note), ou par courrier.
- Pas de brouillon Gmail avec le PDF en pièce jointe : il passerait en base64 par le modèle
  (des centaines de milliers de tokens). Un brouillon sans pièce jointe reste possible.

## Règles

- Pas de rendu image ni de relecture du PDF produit : la ligne `OK` suffit. N'ouvrir un rendu que
  sur `ECHEC` ou si le formulaire a changé de révision (le script le signale).
- Jamais un modèle ni une fiche produite dans un repo (signature de Guillaume ; ce repo est
  public). Pas d'adresse mail de collègue ici non plus.
- Prérequis Python : `pypdf`, `reportlab` (présents dans l'image cloud ; sinon `pip install`).

## Maintenance

- Twin Jet change la révision d'un formulaire (congés : réf. `ADM 100111V6/CP` ; desiderata :
  `Rev. 4 oct.25`) : congés = re-mesurer les positions (méthode en tête du script) ; desiderata =
  re-lister les champs (`get_fields()`), adapter `CHAMPS`.
- Autre formulaire du dossier `documents webcrm/` (note de frais PNT…) : même méthode, un script
  `remplir_<nom>.py` à côté (briques communes : `outils.py`), une section ici.
