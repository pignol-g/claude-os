/**
 * Prépa vol Twinjet — SANDBOX avec colonnes d'override — VARIANTE AUTONOME
 * ========================================================================
 * Même effet que sandbox-override.gs, mais exécutable SANS le menu
 * Extensions du Sheet (indisponible sur mobile / Chrome Android).
 *
 * Utilisation :
 *   1. Ouvrir https://script.google.com → « Nouveau projet ».
 *   2. Coller ce fichier à la place du contenu par défaut, enregistrer (💾).
 *   3. Dans la barre du haut, sélectionner la fonction `creerSandbox`
 *      puis appuyer sur « Exécuter » (▶). Autoriser le script à la
 *      première exécution (c'est ton propre script).
 *   4. Ouvrir le Sheet : l'onglet « prepa SANDBOX » est prêt.
 *
 * Ré-exécuter `creerSandbox` supprime et recrée le sandbox depuis `prepa`.
 * `replierTout` / `deplierTout` se lancent de la même façon (sélecteur de
 * fonction + Exécuter). L'onglet de prod `prepa` n'est JAMAIS modifié.
 */

// ----------------------------- Configuration -----------------------------

var SPREADSHEET_ID = '1SJ3Lh8e7zmp8Ij0idzvYaSRnkeQWkXz77mz2ArU0TOE'; // « Prépa vol twinjet »
var SOURCE_SHEET = 'prepa';          // onglet de production (jamais modifié)
var SANDBOX_SHEET = 'prepa SANDBOX'; // onglet créé/recréé par le script
var N_VOLS = 6;                      // nombre de colonnes vol (B..G dans l'onglet prepa)
var OVERRIDE_COLOR = '#fce5cd';      // orange clair
var OVERRIDE_WIDTH = 70;             // largeur des colonnes override (pixels)
var SHEET_VOLS = 'données vols';     // table de référence par numéro de vol
var SHEET_AVIONS = 'avions';         // table DOW/DOI par immatriculation

// Lignes de `prepa` (libellé colonne A, insensible à la casse) → colonne de `données vols`
var MAP_DONNEES_VOLS = {
  'horaire dep': 2,
  'horraire arr': 3,
  'horaire arr': 3,
  'trip fuel': 4,
  'alternate': 5,
  'alternate fuel': 5,
  'taxi': 6,
  'taxi fuel': 6,
  'cdb fuel': 7,
  'niveau de vol': 10,
  'callsign': 11,
  'mea': 12,
  'altitude depart': 13,
  'altitude terrain depart': 13,
  'altitude terr arr': 14,
  'altitude terrain arrivée': 14,
  'asd': 15,
  'aarg': 16
};

// --------------------------- Action principale ---------------------------

function creerSandbox() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);

  var source = ss.getSheetByName(SOURCE_SHEET);
  if (!source) {
    throw new Error('Onglet « ' + SOURCE_SHEET + ' » introuvable.');
  }

  var existant = ss.getSheetByName(SANDBOX_SHEET);
  if (existant) {
    Logger.log('Onglet « %s » existant supprimé, recréation depuis « %s ».', SANDBOX_SHEET, SOURCE_SHEET);
    ss.deleteSheet(existant);
  }

  var sh = source.copyTo(ss).setName(SANDBOX_SHEET);
  try {
    ss.setActiveSheet(sh);
    ss.moveActiveSheet(source.getIndex() + 1);
  } catch (e) {
    // positionnement de l'onglet purement cosmétique : sans gravité
  }
  sh.setTabColor('#ff6d01');

  transformerEnSandbox(sh);
  Logger.log('Onglet « %s » prêt. Saisie manuelle = colonnes oranges.', SANDBOX_SHEET);
}

function transformerEnSandbox(sh) {
  var lastRow = sh.getLastRow();

  // Libellés de la colonne A (avant toute insertion : les numéros de ligne ne bougent pas)
  var labels = sh.getRange(1, 1, lastRow, 1).getValues().map(function (r) {
    return String(r[0]).trim().toLowerCase();
  });
  var rowNumeroVol = labels.indexOf('numero vol') + 1; // première occurrence
  var rowAvion = labels.indexOf('avion') + 1;
  var rowCrew = labels.indexOf('crew') + 1;

  // 1) Insertion des colonnes override, de droite à gauche.
  //    Vols en B..G (colonnes 2..N_VOLS+1) → après insertion : vol k en 2k, override en 2k+1.
  for (var k = N_VOLS; k >= 1; k--) {
    sh.insertColumnAfter(1 + k);
  }

  // 2) Transformation colonne par colonne.
  for (var v = 1; v <= N_VOLS; v++) {
    var colVol = 2 * v;
    var colOv = colVol + 1;

    var rgVol = sh.getRange(1, colVol, lastRow, 1);
    var formules = rgVol.getFormulasR1C1();
    var valeurs = rgVol.getValues();
    var formats = rgVol.getNumberFormats();

    var newFormules = [];
    var ovValeurs = [];

    for (var i = 0; i < lastRow; i++) {
      var label = labels[i];
      var f = formules[i][0];
      var val = valeurs[i][0];
      var base;

      if (f) {
        // Formule existante : conservée comme valeur auto
        base = f.replace(/^=/, '');
      } else if (label === 'dow' && rowAvion && rowCrew) {
        base = formuleDowDoi(rowAvion, rowCrew, true);
      } else if (label === 'doi' && rowAvion && rowCrew) {
        base = formuleDowDoi(rowAvion, rowCrew, false);
      } else if (MAP_DONNEES_VOLS[label] && rowNumeroVol) {
        base = formuleDonneesVols(rowNumeroVol, MAP_DONNEES_VOLS[label]);
      } else {
        base = '""';
      }

      // Valeur saisie à la main → déplacée dans la colonne override
      ovValeurs.push([(!f && val !== '' && val !== null) ? val : '']);
      newFormules.push(['=IF(RC[1]<>"",RC[1],' + base + ')']);
    }

    var rgOv = sh.getRange(1, colOv, lastRow, 1);
    rgOv.setValues(ovValeurs);
    rgOv.setNumberFormats(formats);          // mêmes formats (heures, nombres…) que la colonne vol
    rgOv.setBackground(OVERRIDE_COLOR);
    rgVol.setFormulasR1C1(newFormules);

    sh.setColumnWidth(colOv, OVERRIDE_WIDTH);

    // 3) Groupe escamotable individuel sur la colonne override, replié par défaut
    sh.getRange(1, colOv, 1, 1).shiftColumnGroupDepth(1);
    try {
      sh.getColumnGroup(colOv, 1).collapse();
    } catch (e) {
      // groupe déjà replié ou non localisable : sans gravité
    }
  }
}

// ------------------------- Formules automatiques --------------------------

// Recherche dans `données vols` par numéro de vol (clé lue dans la colonne du vol courant)
function formuleDonneesVols(rowNumeroVol, idx) {
  return 'VLOOKUP(R' + rowNumeroVol + 'C[0],\'' + SHEET_VOLS + '\'!C1:C16,' + idx + ',FALSE)';
}

// DOW/DOI depuis `avions` : colonne selon crew (2/0 → DOW col2 / DOI col3 ; 2/1 → DOW col4 / DOI col5)
function formuleDowDoi(rowAvion, rowCrew, isDow) {
  var cle = 'R' + rowAvion + 'C[0]';
  var plage = '\'' + SHEET_AVIONS + '\'!C1:C5';
  var col21 = isDow ? 4 : 5;
  var col20 = isDow ? 2 : 3;
  return 'IF(R' + rowCrew + 'C[0]="2/1",' +
    'VLOOKUP(' + cle + ',' + plage + ',' + col21 + ',FALSE),' +
    'VLOOKUP(' + cle + ',' + plage + ',' + col20 + ',FALSE))';
}

// --------------------------- Replier / déplier ----------------------------

function replierTout() {
  basculerGroupes(true);
}

function deplierTout() {
  basculerGroupes(false);
}

function basculerGroupes(replier) {
  var sh = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SANDBOX_SHEET);
  if (!sh) {
    throw new Error('Onglet « ' + SANDBOX_SHEET + ' » introuvable. Exécuter creerSandbox d\'abord.');
  }
  for (var v = 1; v <= N_VOLS; v++) {
    try {
      var g = sh.getColumnGroup(2 * v + 1, 1);
      if (replier) g.collapse(); else g.expand();
    } catch (e) {
      // pas de groupe sur cette colonne : on continue
    }
  }
}
