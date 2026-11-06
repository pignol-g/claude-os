"""Briques communes aux scripts de la skill fiches-twinjet : dates, téléchargement du modèle.

Importé par chemin explicite : `python3 -I` n'ajoute pas le dossier du script à sys.path.
"""
import contextlib
import datetime
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile

# pypdf déverse des pages d'avertissements sur les polices CFF des modèles (fontTools absent) :
# inutiles ici, et chaque ligne affichée coûte des tokens au modèle qui lit la sortie.
logging.getLogger("pypdf").setLevel(logging.CRITICAL)

MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre")
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")


def aujourd_hui():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Paris")).date()
    except Exception:  # base de fuseaux absente : date locale
        return datetime.date.today()


def lire_date(texte, plancher):
    """JJ/MM/AAAA, JJ/MM/AA, AAAA-MM-JJ ou JJ/MM (année absente : 1re occurrence >= plancher)."""
    t = texte.strip()
    try:
        m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
        if m:
            return datetime.date(int(m[1]), int(m[2]), int(m[3]))
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{4}|\d{2}))?", t)
        if not m:
            raise ValueError("format attendu JJ/MM, JJ/MM/AA, JJ/MM/AAAA ou AAAA-MM-JJ")
        jour, mois, an = int(m[1]), int(m[2]), m[3]
        if an is not None:
            return datetime.date(int(an) + (2000 if len(an) == 2 else 0), mois, jour)
        for annee in range(plancher.year, plancher.year + 8):
            try:
                d = datetime.date(annee, mois, jour)
            except ValueError:  # 29/02 hors année bissextile
                continue
            if d >= plancher:
                return d
        raise ValueError("date impossible")
    except ValueError as e:
        raise ValueError(f"date illisible {texte!r} : {e}") from None


def lire_plage(spec, ref):
    """Un jour (« 21/12 ») ou une plage (« 30/12..03/01 », « 30/12 au 03/01 ») -> (début, fin)."""
    morceaux = re.split(r"\s*(?:\.\.|→|\s+au\s+)\s*", spec.strip())
    if len(morceaux) > 2:
        raise ValueError(f"plage illisible {spec!r} : une seule plage « début..fin » attendue")
    debut = lire_date(morceaux[0], ref)
    fin = lire_date(morceaux[1], debut) if len(morceaux) == 2 else debut
    if fin < debut:
        raise ValueError(f"plage {spec!r} : le dernier jour précède le premier")
    return debut, fin


def jm(d):
    return f"{d.day} {MOIS[d.month - 1]}"


def telecharger(url, dossier):
    destination = os.path.join(dossier, "modele.pdf")
    r = subprocess.run(["curl", "-sS", "-f", "-L", "-o", destination, url], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("Téléchargement impossible (lien expiré ou déjà utilisé : redemander download_link) : "
                 + r.stderr.strip()[:200])
    return destination


@contextlib.contextmanager
def modele_local(chemin, url):
    """Chemin du modèle : le fichier fourni, sinon téléchargé dans un dossier neuf (hors dépôt),
    supprimé à la sortie pour ne pas laisser traîner le PDF signé."""
    if chemin:
        yield chemin
        return
    tmp = tempfile.mkdtemp(prefix="modele-twinjet-")
    try:
        yield telecharger(url, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
