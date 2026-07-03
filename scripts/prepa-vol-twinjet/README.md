# Prépa vol Twinjet — sandbox avec colonnes d'override

Script Apps Script pour le Google Sheet **« Prépa vol twinjet »** (Drive Guillaume).
Livré le 2026-07-03 (session CC cloud, demande gpose : O1 en repli de O4, Q1 B / Q2 A / Q3 A).

## Ce que fait le fichier « Prépa vol twinjet » (analyse)

Feuille de préparation de journée de vol : une colonne par vol, ~100 lignes mêlant
checklist mémo (notams, CTOT, catering…), saisie du jour (avion, pax, météo, block fuel)
et valeurs auto-calculées par recherches croisées sur `données vols` (par numéro de vol :
horaires, trip fuel, alternate, callsign, MEA, altitudes, ASD/AARG) et `avions` (DOW/DOI
par immat et crew). La feuille en déduit corrections, mini fuel, charge offerte, EZFW/ETOW
et altitudes antibruit. `MXP`/`BLQ`/`PUF` : suivis carburant par étape. `ameliorations` :
backlog perso — dont « auto **en gardant la possibilité de modifier** », généralisé ici
par le mécanisme d'override.

## Installation (2 minutes)

**Sur ordinateur (recommandé)** — `sandbox-override.gs` :

1. Ouvrir le Sheet « Prépa vol twinjet » → **Extensions ▸ Apps Script**.
2. Coller le contenu de `sandbox-override.gs` dans l'éditeur (remplacer le contenu par défaut), enregistrer.
3. Recharger le Sheet : un menu **« Prépa SANDBOX »** apparaît.
4. Menu ▸ **Créer / recréer l'onglet SANDBOX** (autoriser le script à la première exécution).

**Sur mobile (Android)** — `sandbox-override-standalone.gs` : le menu Extensions n'existe pas
dans Sheets mobile (ni en « version pour ordinateur » de Chrome Android). Variante autonome :

1. Ouvrir https://script.google.com → **Nouveau projet**.
2. Coller `sandbox-override-standalone.gs`, enregistrer.
3. Sélectionner la fonction **`creerSandbox`** dans la barre du haut → **Exécuter** (▶), autoriser.
4. Ouvrir le Sheet : l'onglet `prepa SANDBOX` est prêt. Ré-exécuter = recréer ;
   `replierTout` / `deplierTout` se lancent de la même façon.

## Ce que produit le script

- Onglet **`prepa SANDBOX`** (copie de `prepa` — **la prod n'est jamais touchée**), onglet coloré orange.
- Une **colonne override orange clair** à droite de chaque colonne vol, **repliable individuellement**
  (boutons −/+ au-dessus de la grille), repliée par défaut. Menu pour tout replier/déplier.
- Chaque cellule vol devient `=IF(override<>""; override; valeur_auto)` :
  - formule existante conservée comme valeur auto ;
  - **DOW/DOI auto** depuis `avions` (immat + crew 2/0 ou 2/1) ;
  - **trip fuel, alternate, taxi, cdb fuel, horaires, callsign, MEA, altitudes, ASD, AARG auto**
    depuis `données vols` (par numéro de vol) ;
  - lignes purement manuelles : la valeur effective vient de la cellule override.
- Les valeurs saisies à la main le jour de la copie sont **déplacées dans les colonnes override**
  (rien n'est perdu, tout reste affiché dans la colonne vol).

## Règles d'usage

- **Toute saisie manuelle se fait dans les colonnes oranges.** Taper directement dans une
  colonne vol écrase sa formule (récupérable en recréant le sandbox).
- Vider une cellule orange ⇒ retour à la valeur automatique.
- Les `#N/A` restent volontairement visibles (pas de masquage d'erreur sur une prépa de vol) :
  ils signalent un numéro de vol / une immat absents des tables de référence.

## Limites connues

- Les lignes `correction temp` / `correction qnh` ne sont **pas** branchées sur `données vols`
  (sémantique ambiguë entre coefficient par degré et correction par vol) : formules existantes
  conservées telles quelles, override disponible.
- Si un numéro de vol est saisi en texte alors que `données vols` le stocke en nombre,
  le VLOOKUP renverra `#N/A` (même comportement que les formules actuelles du fichier).
- `N_VOLS = 6` (colonnes B..G) : ajuster en tête de script si la feuille s'élargit.
