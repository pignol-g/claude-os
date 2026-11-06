#!/usr/bin/env python3
"""Remplit la fiche « Demande de congés / absence » Twin Jet (réf. ADM 100111V6/CP).

On part du modèle déjà pré-rempli et signé par Guillaume (nom, prénom, case Twin Jet, signature)
et on y ajoute, aux positions mesurées une fois pour toutes :
  - le premier et le dernier jour pris (Arial 11 pt, format JJ/MM/AA) ;
  - la croix sur le type d'absence (« Congés payés » par défaut) ;
  - la date de présentation de la demande (aujourd'hui, heure de Paris, sauf --demande).
Le reste (intérim, responsable, personnel navigant) reste vide, comme sur la fiche « été 2026 ».

Une fiche PDF par congé demandé. Le script vérifie le modèle, écrit les fiches, relit leur texte
(auto-contrôle sans rendu d'image) et affiche une ligne par fiche. Aucun PDF n'est lu à la main.

Usage :
  python3 -I remplir_conges.py --modele-url URL --sortie DOSSIER [--type cp] [--demande JJ/MM/AAAA] CONGE...
  python3 -I remplir_conges.py --modele FICHIER.pdf --sortie DOSSIER CONGE...
  CONGE = JJ/MM[/AA|/AAAA] (un jour)  ou  DEBUT..FIN  ou  « DEBUT au FIN »  (AAAA-MM-JJ accepté).
  Année absente : première date à partir d'aujourd'hui (la fin : à partir du début). Ex. :
  "21/12"  "30/12..03/01"  (nous sommes en nov. 2026 : 21/12/2026, puis 30/12/2026 au 03/01/2027).
  --dry-run : affiche seulement l'interprétation des dates (sans télécharger ni écrire).

Les dates sont validées AVANT le téléchargement : le lien Dropbox est à usage unique.

Origine des positions (si le gabarit change de révision, les re-mesurer) : fiche « Demande de congés
été 2026 » de Guillaume, remplie avec Adobe Fill & Sign (un formulaire imbriqué par champ, Arial 11 pt).
Lecture : pypdf (matrice de chaque formulaire = coin du champ) et pdfplumber (glyphes des cases).
Coordonnées en points PDF, origine en bas à gauche, A4 = 595 x 842.
"""
import argparse
import functools
import io
import os
import re
import sys
from collections import Counter

sys.dont_write_bytecode = True  # pas de __pycache__ dans le dépôt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I ne le fait pas
from outils import aujourd_hui, jm, lire_date, lire_plage, modele_local  # noqa: E402

try:
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
except ImportError as e:
    sys.exit(f"Module Python manquant : {e.name}. Installer : pip install pypdf reportlab")

# --- Géométrie du formulaire -----------------------------------------------------------------
POLICE_TTF = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # largeurs d'Arial
TAILLE = 11
POS_DU = (200.946, 610.351)        # ligne de base du texte « du (premier jour pris) »
POS_AU = (422.184, 610.351)        # « au (dernier jour pris) »
POS_DEMANDE = (155.128, 429.696)   # « Demande présentée le » (une chaîne alignée sur les pointillés)
CROIX_ORIGINE = (59.5639 + 1.5055, 557.926 + 1.5055)  # coin de la croix « Congés payés »
CROIX_COTE = 12.044
CROIX_EPAISSEUR = 1.505
PAS_CASES = 17.28                  # écart vertical entre les 4 cases « Type d'absence »
TYPES = {  # clé : (rang de la case, libellé, suffixe du nom de fichier)
    "cp": (0, "Congés payés", ""),
    "anticipation": (1, "Congés par anticipation", " anticipation"),
    "sans-solde": (2, "Congés sans solde", " sans solde"),
    "familial": (3, "Congés pour évènement familiaux (justificatif à joindre)", " évènement familial"),
}


def libelle(d1, d2):
    if d1 == d2:
        return f"{jm(d1)} {d1.year}"
    if d1.year != d2.year:
        return f"{jm(d1)} {d1.year} au {jm(d2)} {d2.year}"
    if d1.month != d2.month:
        return f"{jm(d1)} au {jm(d2)} {d2.year}"
    return f"{d1.day} au {jm(d2)} {d2.year}"


# --- Modèle ----------------------------------------------------------------------------------
def a_une_image(objet, vus=None):
    """Vrai si la page contient une image (la signature), formulaires imbriqués compris."""
    vus = set() if vus is None else vus
    res = objet.get("/Resources")
    xo = res.get_object().get("/XObject") if res is not None else None
    if xo is None:
        return False
    for ref in xo.get_object().values():
        o = ref.get_object()
        if id(o) in vus:
            continue
        vus.add(id(o))
        if o.get("/Subtype") == "/Image" or (o.get("/Subtype") == "/Form" and a_une_image(o, vus)):
            return True
    return False


def verifier_modele(chemin):
    lecteur = PdfReader(chemin)
    if len(lecteur.pages) != 1:
        sys.exit(f"Modèle refusé : {len(lecteur.pages)} pages (1 attendue).")
    page = lecteur.pages[0]
    texte = re.sub(r"\s+", " ", page.extract_text() or "")
    if "DEMANDE DE CONGES" not in texte or "PIGNOLET" not in texte:
        sys.exit("Modèle refusé : ce n'est pas la « Demande de congés / absence » pré-remplie (nom absent).")
    if re.search(r"\b\d{2}/\d{2}/\d{2,4}\b", texte):
        sys.exit("Modèle refusé : il contient déjà des dates (ce doit être le modèle SANS dates, "
                 "pas une fiche déjà remplie comme « été 2026 »).")
    if not a_une_image(page):
        print("ATTENTION : aucune signature (image) détectée dans le modèle — modèle non signé ?")


# --- Écriture --------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def police():
    if os.path.exists(POLICE_TTF):
        pdfmetrics.registerFont(TTFont("LiberationSans", POLICE_TTF))
        return "LiberationSans"
    return "Helvetica"  # mêmes largeurs que l'Arial du formulaire


def calque(du, au, demande, rang_case):
    """Page A4 transparente ne contenant que les ajouts."""
    jj, mm, aaaa = demande.split("/")
    tampon = io.BytesIO()
    c = canvas.Canvas(tampon, pagesize=(595, 842), initialFontName=police(), initialFontSize=TAILLE)
    c.setFillColorRGB(0, 0, 0)
    c.setFont(police(), TAILLE)
    c.drawString(*POS_DU, du)
    c.drawString(*POS_AU, au)
    c.drawString(*POS_DEMANDE, f"{jj}     {mm}   {aaaa}")  # même espacement que la fiche « été 2026 »
    x, y = CROIX_ORIGINE
    y -= PAS_CASES * rang_case
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(CROIX_EPAISSEUR)
    c.setLineCap(1)  # extrémités arrondies, comme la croix Twin Jet du modèle
    c.line(x, y, x + CROIX_COTE, y + CROIX_COTE)
    c.line(x + CROIX_COTE, y, x, y + CROIX_COTE)
    c.showPage()
    c.save()
    tampon.seek(0)
    return PdfReader(tampon).pages[0]


def ecrire(modele, sortie, du, au, demande, rang_case):
    ecrivain = PdfWriter(clone_from=PdfReader(modele))
    ecrivain.pages[0].merge_page(calque(du, au, demande, rang_case))
    with open(sortie, "wb") as f:
        ecrivain.write(f)


def controler(sortie, du, au, demande):
    """Relit le texte de la fiche écrite ; renvoie la liste des anomalies (vide = OK)."""
    lecteur = PdfReader(sortie)
    anomalies = []
    if len(lecteur.pages) != 1:
        anomalies.append(f"{len(lecteur.pages)} pages au lieu de 1")
    texte = re.sub(r"\s+", " ", lecteur.pages[0].extract_text() or "")
    for valeur, besoin in Counter([du, au]).items():
        if texte.count(valeur) < besoin:
            anomalies.append(f"date {valeur} introuvable dans la fiche")
    jj, mm, aaaa = demande.split("/")
    if not re.search(rf"\b{jj} {mm} {aaaa}\b", texte):
        anomalies.append(f"date de demande {demande} introuvable")
    if "PIGNOLET" not in texte:
        anomalies.append("nom absent")
    return anomalies


# --- Programme -------------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="Remplit les fiches de congés Twin Jet.")
    source = p.add_mutually_exclusive_group()
    source.add_argument("--modele-url", help="lien temporaire Dropbox (download_link), à usage unique")
    source.add_argument("--modele", help="modèle PDF déjà téléchargé")
    p.add_argument("--sortie", help="dossier d'écriture des PDF (dans le scratchpad pour pouvoir les envoyer)")
    p.add_argument("--type", choices=list(TYPES), default="cp", help="type d'absence coché (défaut : cp)")
    p.add_argument("--demande", help="date de présentation JJ/MM/AAAA (défaut : aujourd'hui, Paris)")
    p.add_argument("--dry-run", action="store_true", help="n'affiche que l'interprétation des dates")
    p.add_argument("conges", nargs="+", metavar="CONGE")
    a = p.parse_args()

    aujourd = aujourd_hui()
    try:
        demande = lire_date(a.demande, aujourd).strftime("%d/%m/%Y") if a.demande else aujourd.strftime("%d/%m/%Y")
        plages = [lire_plage(s, aujourd) for s in a.conges]
    except ValueError as e:
        sys.exit(f"Erreur : {e}")
    rang, nom_type, suffixe = TYPES[a.type]

    for d1, d2 in plages:
        jours = (d2 - d1).days + 1
        alerte = "  <- ATTENTION : plage très longue, dates à revérifier" if jours > 45 else ""
        print(f"  {libelle(d1, d2)} -> du {d1:%d/%m/%y} au {d2:%d/%m/%y} ({jours} j){alerte}")
    print(f"  type : {nom_type} | demande présentée le {demande}")
    if a.dry_run:
        return
    if not a.sortie or not (a.modele or a.modele_url):
        sys.exit("Erreur : --sortie et (--modele-url ou --modele) sont requis hors --dry-run.")

    os.makedirs(a.sortie, exist_ok=True)
    echecs = 0
    with modele_local(a.modele, a.modele_url) as modele:
        verifier_modele(modele)
        for d1, d2 in plages:
            du, au = d1.strftime("%d/%m/%y"), d2.strftime("%d/%m/%y")
            sortie = os.path.abspath(os.path.join(a.sortie, f"Demande de congés{suffixe} {libelle(d1, d2)}.pdf"))
            ecrire(modele, sortie, du, au, demande, rang)
            anomalies = controler(sortie, du, au, demande)
            if anomalies:
                echecs += 1
                print(f"ECHEC  {sortie} : " + " ; ".join(anomalies))
            else:
                print(f"OK  {sortie}")
    if a.type == "familial":
        print("Rappel : congé pour évènement familial = justificatif à joindre à la fiche.")
    sys.exit(1 if echecs else 0)


main()
