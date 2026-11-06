#!/usr/bin/env python3
"""Remplit la « Demande de desiderata » Twin Jet (DOC 001 / INS ADM 01, Rev. 4 oct.25).

On part de la fiche déjà pré-remplie et signée par Guillaume (nom, prénom, escale, signature en
annotation). C'est un PDF à champs : le script ne remplace que la date de la demande, « du »,
« au », « soit » (nombre de jours) et le motif ; la section « Responsable » reste vide. Le
résultat reste modifiable. Aucun PDF n'est lu à la main : le script vérifie le modèle, écrit les
fiches, relit les champs et affiche une ligne par fiche.

Règles (formulaire et note de service CST033 du 24/10/2024) :
  - jours de week-end uniquement (samedi, dimanche) : sinon erreur, sauf --forcer ;
  - demande au plus tard le 05 du mois pour le mois suivant : sinon avertissement (non bloquant) ;
  - envoi par mail au RDOS avec copie à la gestion, ou par courrier (adresses : note CST033, dossier
    Dropbox « documents webcrm » ; pas d'adresse ici, ce dépôt est public).

Usage :
  python3 -I remplir_desiderata.py --modele-url URL --sortie DOSSIER [--motif TEXTE] [--demande JJ/MM/AAAA] [--forcer] WEEKEND...
  python3 -I remplir_desiderata.py --modele FICHIER.pdf --sortie DOSSIER WEEKEND...
  WEEKEND = we:JJ/MM          le week-end (samedi + dimanche) qui contient cette date
          | JJ/MM[/AA|/AAAA]  un seul jour
          | DEBUT..FIN        une plage (AAAA-MM-JJ accepté)
  Année absente : première date à partir d'aujourd'hui. Une fiche par WEEKEND.
  --dry-run : affiche seulement l'interprétation des dates (sans télécharger ni écrire).

Les dates sont validées AVANT le téléchargement : le lien Dropbox est à usage unique.

Champs du modèle (relevés une fois ; si la révision change, re-lister avec pypdf `get_fields()`) :
  Texte1 nom, Texte2 prénom, Texte3 escale (pré-remplis) ; Texte4 date de la demande, Texte5 du,
  Texte6 au, Texte7 soit, Texte8 motif ; Texte9 signature (texte, vide : la signature est une
  annotation Ink) ; Texte10 OUI, Texte11 NON, Texte12 motif, Texte13 signature du responsable.
"""
import argparse
import datetime
import os
import re
import sys

sys.dont_write_bytecode = True  # pas de __pycache__ dans le dépôt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I ne le fait pas
from outils import JOURS, aujourd_hui, jm, lire_date, lire_plage, modele_local  # noqa: E402

try:
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfbase.pdfmetrics import stringWidth
except ImportError as e:
    sys.exit(f"Module Python manquant : {e.name}. Installer : pip install pypdf reportlab")

CHAMPS = {"demande": "Texte4", "du": "Texte5", "au": "Texte6", "soit": "Texte7", "motif": "Texte8"}
FIXES = ("Texte1", "Texte2", "Texte3")                                # nom, prénom, escale
RESPONSABLE = ("Texte9", "Texte10", "Texte11", "Texte12", "Texte13")  # à laisser vides
MOTIF_DEFAUT = "week-end famille"  # valeur de la fiche d'exemple
REVISION = "Rev. 4 oct.25"
LARGEUR_MOTIF = 405                # points : case de 409 pt moins les marges, Helvetica 12


def lire_weekend(spec, ref):
    m = re.fullmatch(r"(?i)we\s*:\s*(.+)", spec.strip())
    if not m:
        return lire_plage(spec, ref)
    d = lire_date(m[1], ref)
    if d.weekday() == 5:
        return d, d + datetime.timedelta(days=1)
    if d.weekday() == 6:
        return d - datetime.timedelta(days=1), d
    raise ValueError(f"{spec!r} : {JOURS[d.weekday()]} {d:%d/%m/%y} n'est pas un jour de week-end")


def echeance(du):
    """Au plus tard le 05 du mois précédent le mois du premier jour demandé (note CST033)."""
    annee, mois = (du.year - 1, 12) if du.month == 1 else (du.year, du.month - 1)
    return datetime.date(annee, mois, 5)


def libelle(d1, d2):
    if d1 == d2:
        return f"{jm(d1)} {d1.year}"
    sep = "et" if (d2 - d1).days == 1 else "au"
    if d1.year != d2.year:
        return f"{jm(d1)} {d1.year} {sep} {jm(d2)} {d2.year}"
    if d1.month != d2.month:
        return f"{jm(d1)} {sep} {jm(d2)} {d2.year}"
    return f"{d1.day} {sep} {jm(d2)} {d2.year}"


def a_une_signature(lecteur):
    annots = lecteur.pages[0].get("/Annots")
    return annots is not None and any(a.get_object().get("/Subtype") == "/Ink" for a in annots.get_object())


def verifier_modele(chemin):
    lecteur = PdfReader(chemin)
    if len(lecteur.pages) != 1:
        sys.exit(f"Modèle refusé : {len(lecteur.pages)} pages (1 attendue).")
    champs = lecteur.get_fields() or {}
    manquants = [f"Texte{i}" for i in range(1, 14) if f"Texte{i}" not in champs]
    texte = re.sub(r"\s+", " ", lecteur.pages[0].extract_text() or "")
    if manquants or "DEMANDE DE DESIDERATA" not in texte:
        sys.exit("Modèle refusé : ce n'est pas la « Demande de desiderata » attendue (champs Texte1 à Texte13 "
                 "introuvables) ; la révision du formulaire a peut-être changé.")
    if not all(champs[n].get("/V") for n in FIXES):
        sys.exit("Modèle refusé : nom, prénom ou escale vides (le modèle doit être pré-rempli).")
    if any(champs[n].get("/V") for n in RESPONSABLE):
        sys.exit("Modèle refusé : la section « Responsable » est déjà remplie.")
    if REVISION not in texte:
        print(f"ATTENTION : révision du formulaire différente de « {REVISION} » : vérifier le rendu.")
    if not a_une_signature(lecteur):
        print("ATTENTION : aucune signature (annotation Ink) détectée dans le modèle — modèle non signé ?")


def ecrire(modele, sortie, valeurs):
    ecrivain = PdfWriter(clone_from=PdfReader(modele))
    ecrivain.update_page_form_field_values(ecrivain.pages[0], valeurs, auto_regenerate=False)
    with open(sortie, "wb") as f:
        ecrivain.write(f)


def controler(sortie, valeurs):
    """Relit les champs de la fiche écrite ; renvoie la liste des anomalies (vide = OK)."""
    lecteur = PdfReader(sortie)
    champs = lecteur.get_fields() or {}
    anomalies = []
    if len(lecteur.pages) != 1:
        anomalies.append(f"{len(lecteur.pages)} pages au lieu de 1")
    for nom, attendu in valeurs.items():
        lu = champs.get(nom, {}).get("/V")
        if lu != attendu:
            anomalies.append(f"{nom} = {lu!r} au lieu de {attendu!r}")
    if not all(champs.get(n, {}).get("/V") for n in FIXES):
        anomalies.append("nom, prénom ou escale vides")
    if not a_une_signature(lecteur):
        anomalies.append("signature absente")
    return anomalies


def main():
    p = argparse.ArgumentParser(description="Remplit les demandes de desiderata Twin Jet.")
    source = p.add_mutually_exclusive_group()
    source.add_argument("--modele-url", help="lien temporaire Dropbox (download_link), à usage unique")
    source.add_argument("--modele", help="modèle PDF déjà téléchargé")
    p.add_argument("--sortie", help="dossier d'écriture des PDF (dans le scratchpad pour pouvoir les envoyer)")
    p.add_argument("--motif", help=f"motif (défaut : « {MOTIF_DEFAUT} », celui de la fiche d'exemple)")
    p.add_argument("--demande", help="date de la demande JJ/MM/AAAA (défaut : aujourd'hui, Paris)")
    p.add_argument("--forcer", action="store_true", help="autorise des jours de semaine (hors règle du formulaire)")
    p.add_argument("--dry-run", action="store_true", help="n'affiche que l'interprétation des dates")
    p.add_argument("weekends", nargs="+", metavar="WEEKEND")
    a = p.parse_args()

    aujourd = aujourd_hui()
    try:
        demande = lire_date(a.demande, aujourd) if a.demande else aujourd
        plages = [lire_weekend(s, aujourd) for s in a.weekends]
    except ValueError as e:
        sys.exit(f"Erreur : {e}")
    motif = (a.motif if a.motif is not None else MOTIF_DEFAUT).strip()

    erreurs = []
    if not motif:
        erreurs.append("motif vide")
    for d1, d2 in plages:
        n = (d2 - d1).days + 1
        print(f"  {JOURS[d1.weekday()]} {d1:%d/%m/%y} -> {JOURS[d2.weekday()]} {d2:%d/%m/%y} ({n} j)")
        semaine = [d for d in (d1 + datetime.timedelta(days=i) for i in range(n)) if d.weekday() < 5]
        if semaine and not a.forcer:
            erreurs.append(f"{d1:%d/%m/%y}..{d2:%d/%m/%y} contient {', '.join(f'{JOURS[d.weekday()]} {d:%d/%m}' for d in semaine)} : "
                           "desiderata = samedi et dimanche uniquement (--forcer pour passer outre)")
        elif semaine:
            print("  ATTENTION : jours de semaine inclus (--forcer)")
        if d1 < demande:
            erreurs.append(f"{d1:%d/%m/%y} est antérieur à la date de la demande ({demande:%d/%m/%Y})")
        limite = echeance(d1)
        if demande > limite:
            print(f"  ATTENTION : échéance du {limite:%d/%m/%Y} dépassée (note CST033)")
    defaut = " (défaut : motif de la fiche d'exemple)" if a.motif is None else ""
    print(f"  motif : « {motif} »{defaut} | demande du {demande:%d/%m/%Y}")
    if stringWidth(motif, "Helvetica", 12) > LARGEUR_MOTIF:
        print("  ATTENTION : motif trop long pour la case, il sera coupé : le raccourcir")
    if erreurs:
        sys.exit("\n".join(f"Erreur : {e}" for e in erreurs))
    if a.dry_run:
        return
    if not a.sortie or not (a.modele or a.modele_url):
        sys.exit("Erreur : --sortie et (--modele-url ou --modele) sont requis hors --dry-run.")

    os.makedirs(a.sortie, exist_ok=True)
    echecs = 0
    with modele_local(a.modele, a.modele_url) as modele:
        verifier_modele(modele)
        for d1, d2 in plages:
            valeurs = {CHAMPS["demande"]: demande.strftime("%d/%m/%y"), CHAMPS["du"]: d1.strftime("%d/%m/%y"),
                       CHAMPS["au"]: d2.strftime("%d/%m/%y"), CHAMPS["soit"]: str((d2 - d1).days + 1),
                       CHAMPS["motif"]: motif}
            sortie = os.path.abspath(os.path.join(a.sortie, f"Demande de desiderata {libelle(d1, d2)}.pdf"))
            ecrire(modele, sortie, valeurs)
            anomalies = controler(sortie, valeurs)
            if anomalies:
                echecs += 1
                print(f"ECHEC  {sortie} : " + " ; ".join(anomalies))
            else:
                print(f"OK  {sortie}")
    sys.exit(1 if echecs else 0)


main()
