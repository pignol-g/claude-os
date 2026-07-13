# RECHERCHE APPROFONDIE — Babyphone caméra, comparatif pondéré

**Date : 2026-07-13** · Méthode : skill `grech` (multi-agents) · 5 agents Sonnet lancés en parallèle (4 aboutis, 1 tué par quota web).

## En-tête méthodo

| Élément | Valeur |
|---|---|
| Agents de recherche | 5 (A1 presse parentalité, A2 médias tech, A3 guides d'achat, A4 fiches techniques, A5 sécurité/fiabilité) |
| Agents aboutis | 4 — **A4 (fiches techniques) tué par limite de session web** (reset ~15h00 UTC) |
| Comparatifs ≤24 mois exploitables | ~28 (avec classement de plusieurs modèles) |
| Sources web consultées (cumulées) | >130 URLs (listées en annexe par agent) |
| État interne croisé | Étude préalable de Guillaume (GHB, momcozy BM03, BOIFUN ×2, ieGeek, Arenti AInanny) |
| Limite assumée | La détection **mouvement** par modèle mainstream n'a pu être confirmée pièce à pièce (A4 interrompu) → champs marqués « à confirmer » |

---

## TL;DR (verdict d'abord)

1. **Ta shortlist hybride (BOIFUN, ieGeek, Arenti) est disqualifiée sur la sécurité** : les trois reposent sur la plateforme **Meari/CloudEdge**, frappée en mai 2026 par 5 CVE (clés crypto codées en dur identiques sur tout le parc, images en clair sur serveur Chine, ~1,1 M d'appareils exposés). À écarter tant qu'un firmware ≥3.0.0 corrigé n'est pas confirmé.
2. **Le momcozy BM03 est le meilleur alignement à TES critères** : sans-WiFi pur (FHSS, aucune exposition internet), détection mouvement **ET** bruit, enregistrement clips sur SD **avec relecture locale sur l'écran parent**, ≤100 €, et **la liaison la plus fiable** des retours consultés (aucun décrochage) — ce qui répond directement à ton problème GHB. **Mais** il est sous-couvert par les comparatifs → score brut modeste (~47/100), d'où l'écart score↔reco détaillé plus bas.
3. **Le score pondéré brut favorise le mainstream FR** (Babymoov ~95, Philips Avent/Babysense ~66, HelloBaby ~60) parce que les comparatifs FR sont quasi tous des blogs affiliés qui poussent ces marques — **le score n'est PAS la recommandation** ; il est corrigé par tes critères éliminatoires/prioritaires.
4. **Qualité des sources faible** : aucun média national FR (Le Parisien, BFMTV…) ni test institutionnel récent ; seules Which? (UK), BabyGearLab et Fathercraft (US) ont une vraie méthodo terrain, mais hors marché FR et sans modèle sans-WiFi pur en tête.

---

## La question et sa prémisse

**Question** : quel babyphone caméra remplace au mieux le GHB (B0FYMQRC4K) radio 2,4 GHz qui décroche, pour un profil « sans-WiFi obligatoire (mobilité) + détection mouvement&bruit + priorité radio/vie privée + enregistrement local + ≤100 € » ?

**Prémisse validée** : tu as maintenant du WiFi dans la chambre, mais le **sans-WiFi reste éliminatoire** (usage nomade vacances/amis). Correction utile issue de la recherche : ton hésitation entre les 3 hybrides (BOIFUN/ieGeek/Arenti) est **tranchée par la sécurité** avant même le confort — donnée que ton étude initiale n'avait pas.

---

# A. Tableau des sites + coefficient de fiabilité C_site

Notes /5 sur 6 critères (Fraîcheur / Méthodo test réel / Indépendance / Autorité-trafic / Nb modèles comparés / Transparence). C_site = moyenne arrondie à 0,5.

| Site | URL | Date | Frch | Méth | Indp | Aut | NbM | Trsp | **C_site** | Justification courte |
|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| Which? (UK) | which.co.uk/reviews/baby-monitors | 2025-2026 | 5 | 5 | 5 | 5 | 5 | 4 | **5,0** | 36 testés, banc consumériste ; classement chiffré payant → exclu du scoring |
| BabyGearLab (US) | babygearlab.com/…/best-baby-monitor | 2026-03 | 5 | 5 | 5 | 4,5 | 5 | 5 | **5,0** | Labo indépendant, 106+ testés, achats propres |
| Fathercraft (US) | fathercraft.com/baby-monitor-reviews | 2026-06 | 5 | 5 | 4,5 | 3 | 4 | 5 | **4,5** | Mesure EMF pro, test portée réel ; petit site |
| The Bump (US) | thebump.com/a/best-baby-monitors | 2025-07 | 4,5 | 4 | 3,5 | 4,5 | 3,5 | 4 | **4,0** | Test multi-familles + sondage 300 parents |
| ConsoBaby (FR) | consobaby.com/…/meilleurs-babyphones | 2025-03 | 4 | 2,5 | 3,5 | 4 | 4 | 3 | **3,5** | Plus grosse base d'avis parents FR ; pas un test |
| Digitec (CH) | digitec.ch/…/toplist/babyphone | dynamique | 4 | 2,5 | 3,5 | 4,5 | 4,5 | 2,5 | **3,5** | Gros retailer, classement ventes/avis |
| Selectos (FR) | selectos.eu/meilleurs-babyphones | 2025-09 | 4,5 | 3,5 | 2,5 | 3,5 | 4,5 | 3,5 | **3,5** | 15 modèles, portée mesurée ; affilié |
| Avis-Parents (FR) | avis-parents.com/…/meilleur-babyphone | 2026-06 | 5 | 3 | 2,5 | 3 | 3 | 4 | **3,5** | Honnête sur les limites (portée /3-4) ; affilié |
| Avis-Parents caméra | avis-parents.com/…/meilleur-babyphone-camera | 2026-07 | 5 | 3 | 2,5 | 3 | 2,5 | 4 | **3,5** | Idem, focalisé caméra |
| Babideal (FR) | babideal.fr/guide-achat/meilleur-babyphone | 2025-03 | 4 | 3,5 | 2,5 | 3 | 4 | 4 | **3,5** | Auteur identifié, « comment nous testons » ; biais Babymoov |
| Futura-Sc. vidéo | futura-sciences.com/…/babyphone-video | 2025-09 | 4,5 | 2,5 | 2,5 | 4,5 | 3 | 3,5 | **3,5** | Grosse marque, exécution faible (3 modèles) |
| Futura-Sc. général | futura-sciences.com/…/babyphone-comparatif | 2025-09 | 4,5 | 2,5 | 2,5 | 4,5 | 3 | 3,5 | **3,5** | Idem |
| BebeCool vidéo | bebecool.fr/meilleur-babyphone-video | 2026-05 | 4,5 | 2 | 2,5 | 2,5 | 4,5 | 2,5 | **3,0** | Liste large à jour, zéro preuve de test |
| BebeCool général | bebecool.fr/meilleur-babyphone-comparatif | 2026-05 | 4,5 | 2 | 2,5 | 2,5 | 4,5 | 2,5 | **3,0** | Idem |
| Nid'Enfant (FR) | nidenfant.fr/…/meilleur-babyphone | 2025-08 | 4,5 | 3 | 2,5 | 2,5 | 2 | 3,5 | **3,0** | Revendique protocole, échantillon 3 modèles |
| new-baby (FR) | new-baby.fr/meilleur-babyphone-et-camera-2025 | 2025-08 | 4,5 | 2 | 2 | 2 | 4 | 2,5 | **3,0** | Sélection commerciale, peu de preuve |
| La Maison Intell. | la-maison-intelligente.fr/…/top-5 | 2026-04 | 5 | 2,5 | 3,5 | 2 | 3 | 3 | **3,0** | Pas d'affiliation détectée ; crédibilité non établie |
| LaitFraiseMag (FR) | laitfraisemag.fr/meilleur-babyphone | 2024-10 | 3,5 | 2 | 2,5 | 3 | 4,5 | 2,5 | **3,0** | MAJ en limite de fenêtre |
| BebeZecolo (FR) | bebezecolo.fr/comparatif-…-babyphones | 2026 (est.) | 4,5 | 2 | 2 | 2 | 5 | 2 | **3,0** | Notes /20 non justifiées |
| Electroguide (FR) | electroguide.com/top-7-meilleurs-babyphones | 2026 | 4 | 2 | 2,5 | 3 | 3,5 | 2,5 | **3,0** | Méthodo vague, pas de prix |
| bedbedtime (FR) | bedbedtime.com/meilleurs-babyphones-video | 2026-05 | 5 | 3 | 2,5 | 2 | 3,5 | 3 | **3,0** | Protocole affiché le plus crédible des petits FR |
| ConsoMaman (FR) | consomaman.fr/…-sans-wifi-2025-2026 | 2025 (est.) | 4 | 2 | 2 | 2 | 3 | 2,5 | **2,5** | Angle sans-WiFi aligné, zéro preuve terrain |
| Meilleurs.fr | meilleurs.fr/babyphone | 2026-07 | 5 | 1,5 | 1,5 | 2,5 | 5 | 1,5 | **2,5** | Profil ferme d'affiliation programmatique |
| PassionTélétravail | passionteletravail.fr/meilleurs-babyphones-video | 2025-11 | 4 | 1,5 | 2 | 2 | 3,5 | 2,5 | **2,5** | Hors-sujet historique, méthodo faible |
| Babideal longue portée | babideal.fr/…/babyphone-longue-portee | 2025-03 | 4 | 2 | 2 | 3 | 2,5 | 3 | **2,5** | 3/4 modèles Babymoov (biais mono-marque) |
| ecomparatif (FR) | ecomparatif.fr/…-longue-portee | 2024/25 | 3 | 1,5 | 2 | 2 | 3 | 1,5 | **2,0** | Aucune justification du classement |
| babyphone-sans-onde | babyphone-sans-onde.fr/babyphone-longue-portee | 2026 | 3,5 | 1,5 | 1,5 | 2 | 2,5 | 2 | **2,0** | Curation affiliée |
| mon-centre-interphonie | mon-centre-interphonie.com/meilleur-babyphone | 2026 | 3,5 | 1 | 1,5 | 1,5 | 5 | 1,5 | **2,0** | Volume élevé, rigueur nulle |

**Hors fenêtre (signalés, non comptés)** : Stiftung Warentest test.de (2022-09, 46 modèles, méthodo solide), UFC-Que Choisir (2018), Digitec testreport (2021). **Bloqués** : Forbes (403), TechRadar, Clubic (vide). **Constat** : aucun média tech généraliste FR (Les Numériques, 01net, Frandroid, Numerama) n'a de comparatif babyphone dédié récent.

---

# B. Tableau maison — tous les modèles

Score = `[Σ(C_site·s)/Σ(C_site)] × min(1 ; nb_comparatifs/5) × 100`, avec `s = (N−p+1)/N`. Éliminatoires : **sans-WiFi possible** + **détection mouvement ET bruit**.

| Modèle | ASIN | Prix | Radio sans-WiFi | WiFi désactiv. | Enregistrement | Mvt+Bruit | Chiffrement (hybride) | Portée/fiabilité | Budget | Nb comp. | **Score/100** | **PASS/FAIL** |
|---|---|---|:--:|:--:|---|:--:|---|---|:--:|:--:|:--:|:--:|
| **momcozy BM03** | B0GHPKZHK9 | ~90 € | **Oui (FHSS pur)** | n-a (pas de wifi) | Clips 1 min/mvt, SD 32 Go incl., **relecture écran parent** | **Oui+Oui** | n-a (aucun cloud) | **Bonne** (3 étages, 0 décrochage) | ≤100 | 4 | **47** | **✅ PASS** |
| Babymoov Yoo Moov / Simply Care | — | 60-120 € | Oui (radio DECT) | n-a | Live, pas de SD (selon modèle) | Bruit oui / **Mvt à confirmer** | n-a | Moyenne-bonne | mixte | 7 | **95** | ⚠️ PASS si mvt confirmé |
| Philips Avent (DECT SCD833/843/923) | — | 90-160 € | Oui (DECT) | n-a | Live, pas de SD | Bruit oui / **Mvt à confirmer** (souvent absent) | n-a | Bonne | mixte | 11 | **66** | ⚠️ à confirmer |
| Philips Avent Connected (SCD881…) | — | >150 € | **Non (WiFi)** | Non | App/cloud | Oui | non documenté | — | >100 | — | — | ❌ FAIL (wifi only) |
| Babysense Max View / V-series | — | 120-230 € | Oui (radio) | n-a | Selon modèle | **Oui+Oui** (V-series) | n-a | Bonne | >100 (Max View) | 6 | **66** | ✅ PASS (souvent >100 €) |
| HelloBaby (HB32/HB65/HB6550) | — | 33-76 € | Oui (radio) | n-a | Selon modèle (SD sur HB6550) | Bruit oui / **Mvt selon modèle** | n-a | Moyenne | ≤100 | 10 | **60** | ⚠️ à confirmer par modèle |
| VTech (DM1211/VM924/VM901) | — | 60-123 € | Oui (DECT) | n-a | Live | Bruit oui / **Mvt souvent absent** | n-a | Bonne (DECT) | ≤100 | 7 | **47** | ⚠️ probable FAIL mvt |
| Motorola (PIP1500/VM855/AM21) | — | 70-120 € | Oui (radio) selon modèle | n-a | Live | à confirmer | Hubble : **pas de 2FA** si wifi | Moyenne | mixte | 6 | ~40 | ⚠️ à confirmer |
| **BOIFUN** | B0H1BXMHTH | ~76 € | Hybride (mode local) | Oui (annoncé) | 2K, SD | Oui+Oui | **AES-128 mais 5 CVE Meari/CloudEdge** (clés en dur, OSS Chine) | Moyenne-mauvaise (décrochages) | ≤100 | 4 | **51** | ❌ FAIL sécurité |
| **BOIFUN 24/7** | B0DT3ZJ7FH | ~85 € | Hybride | Oui | **24/7 SD** (manuel) | Oui+Oui | idem CVE Meari | Moyenne | ≤100 | (incl. ci-dessus) | — | ❌ FAIL sécurité |
| **ieGeek** | B0BY2HBWWL | ~80 € | Hybride | non documenté | 2K, SD 128 Go cam + 32 Go écran + cloud | Oui+Oui | **CVE Meari** + instabilité >10 m reconnue | Moyenne | ≤100 | 2 | ~25 | ❌ FAIL sécurité |
| **Arenti AInanny 2K** | B0CF4KBJ1C | ~90 € | Hybride (dépend wifi) | Non (monitoring = internet requis) | 24/7 SD | Oui+Oui | AES-128 + 3 serveurs AWS **mais cité dans CVE Meari** | Moyenne (décrochage cam↔écran) | ≤100 | 3 | **33** | ❌ FAIL sécurité + liaison |
| GHB (actuel) | B0FYMQRC4K | ~60 € | Oui (radio) | n-a | Live | Bruit oui / mvt ? | n-a | **Moyenne (décroche)** | ≤100 | 3 | ~30 | ⚠️ le modèle à remplacer |

*Modèles mainstream traités au niveau marque/famille faute de A4 (grain ASIN non atteint). « à confirmer » = quota web épuisé avant vérification de la détection mouvement par référence exacte.*

---

## Détail du calcul — Top 5 par score brut

Formule : `Score = [Σ(C·s)/Σ(C)] × coverage × 100`, `coverage = min(1 ; nb_comparatifs/5)`.

**1. Babymoov ≈ 95/100** — apparaît #1 dans quasi tous les comparatifs FR affiliés.
Σ(C·s)=21,0 ; Σ(C)=22,0 → 0,955 ; coverage=min(1;7/5)=1,0 → **95,5**.

**2. Philips Avent ≈ 66/100**
Σ(C·s)=21,57 ; Σ(C)=32,5 → 0,664 ; coverage=1,0 → **66,4**.

**3. Babysense ≈ 66/100**
Σ(C·s)=13,60 ; Σ(C)=20,5 → 0,663 ; coverage=1,0 → **66,3**.

**4. HelloBaby ≈ 60/100**
Σ(C·s)=20,76 ; Σ(C)=34,5 → 0,602 ; coverage=1,0 → **60,2**.

**5. BOIFUN ≈ 51/100** (mais FAIL sécurité)
Σ(C·s)=7,63 ; Σ(C)=12,0 → 0,635 ; coverage=min(1;4/5)=0,8 → **50,8**.

**Hors top-5, illustrant l'écart score↔critères :**
- **momcozy BM03 ≈ 47/100** : Σ(C·s)=6,78 ; Σ(C)=11,5 → 0,589 ; coverage=0,8 → **47,1**. Pénalisé par la sous-couverture (vu dans 4 comparatifs) alors qu'il coche TOUS tes critères.
- VTech ≈ 47 ; Arenti ≈ 33 (FAIL) ; ieGeek ≈ 25 (FAIL).

> **Lecture** : le score brut mesure « à quel point les comparatifs FR aiment un modèle », pas « à quel point il te convient ». Babymoov domine parce que les blogs affiliés le classent #1, pas parce qu'il est le mieux adapté au sans-WiFi + mouvement + local. La reco ci-dessous corrige cela.

---

# C. Top 3 recommandations (au regard de TES critères)

### 🥇 1. momcozy BM03 (B0GHPKZHK9) — le meilleur alignement
- **Éliminatoires : PASS net** — sans-WiFi pur (FHSS), détection mouvement **et** bruit.
- **Priorités cochées** : aucune exposition internet (0 cloud, 0 app → immunisé au risque Meari qui coule les hybrides) ; enregistrement **local clips SD + relecture directe sur l'écran parent** (le mode que tu valorises) ; **liaison la plus fiable** des retours (0 décrochage, 3 étages) — réponse directe à ton problème GHB ; ≤100 €.
- **Réserve** : score brut modeste (sous-couvert par les comparatifs) ; clips 1 min sur mouvement (pas de 24/7). À confirmer au SAV : 100 % sans WiFi/app + relecture SD sur écran.

### 🥈 2. Babysense (V-series / Max View) — le sans-WiFi « premium fiable »
- **PASS** sur les éliminatoires (radio + mouvement + bruit sur les V-series), bien classé par la source la plus sérieuse du corpus (**#1 The Bump**, C=4,0) et par bedbedtime/ConsoMaman.
- **Réserve** : le Max View dépasse 100 € (~229 €) ; vérifier le modèle précis ≤100 € (ex. V43) et la présence mouvement + SD.

### 🥉 3. Babymoov Yoo Moov (ou HelloBaby à mouvement confirmé) — le mainstream sûr
- **Radio sans-WiFi**, n°1 des comparatifs FR, SAV/distribution FR solides, ≤100 € (Yoo Moov / HelloBaby HB65 ~64 €).
- **Réserve bloquante** : la **détection mouvement** n'est pas garantie sur ces gammes (souvent VOX/bruit seul) → **à confirmer avant achat** (c'est le trou laissé par l'agent A4).

**💰 Meilleur rapport qualité-prix ≤100 €** : **momcozy BM03 (~90 €)** — il fait tout ce dont tu as besoin sans cloud ni abonnement. Alternative moins chère si tu tolères une relecture plus limitée : HelloBaby HB65 (~64 €), sous réserve mouvement confirmé.

**⬆️ Si tu montes le budget (en gardant le sans-WiFi obligatoire)** : **Babysense Max View** (~229 €, sans-WiFi, #1 The Bump, grand écran, mouvement+bruit). À éviter malgré leur budget : Nanit/Owlet/Cubo (WiFi-only → FAIL éliminatoire) et tout hybride Meari tant que non patché.

---

# D. Points d'incertitude à lever + questions SAV

| # | Incertitude | Impact | Action |
|---|---|---|---|
| 1 | **Détection mouvement** non confirmée par modèle mainstream (Babymoov Yoo Moov, HelloBaby HB65, VTech) — agent A4 tué par quota | Peut faire basculer #3 en FAIL | **Relancer A4 après 15h00 UTC** (fiches fabricant/manuels) OU question SAV |
| 2 | momcozy BM03 : réellement **100 % sans WiFi ni app** ? Relecture des clips SD **sur l'écran parent** ? | Confirme le 🥇 | SAV momcozy : *« Le BM03 fonctionne-t-il entièrement sans WiFi ni application ? Peut-on relire les clips de la carte SD directement sur l'écran parent ? »* |
| 3 | **CVE Meari/CloudEdge** : firmware ≥3.0.0 correctif déployé sur BOIFUN/ieGeek/Arenti ? | Réhabiliterait éventuellement les hybrides | SAV BOIFUN/ieGeek/Arenti : *« Vos caméras 2026 embarquent-elles le firmware ≥3.0.0 corrigeant les vulnérabilités Meari (CVE-2026-33356 à 33362) ? »* |
| 4 | Babysense : modèle précis **≤100 € avec mouvement + sans-WiFi + SD** (V43 ?) | Précise le 🥈 | Fiche V43 / SAV Babysense |
| 5 | Clip-sur-événement (momcozy) vs 24/7 (BOIFUN B0DT3ZJ7FH, Arenti) | Arbitrage confort | Décider : le 24/7 justifie-t-il le risque hybride ? (à ce jour non, cf. sécurité) |

---

## Annexe — Sources par agent

**A1 (presse parentalité) — citées** : futura-sciences (×2), bebecool.fr, meilleurs.fr, avis-parents.com, nidenfant.fr, consobaby.com, laitfraisemag.fr, la-maison-intelligente.fr, babideal.fr, bebezecolo.fr, consomaman.fr. *Constat : angle presse pure quasi vide sur 24 mois (MagicMaman/Parents.fr/Doctissimo infetchables/non indexés).*

**A2 (médias tech/tests indé) — citées** : which.co.uk, babygearlab.com, fathercraft.com, thebump.com, selectos.eu, bedbedtime.com, passionteletravail.fr, nidenfant.fr, avis-parents.com, electroguide.com, futura-sciences.com, digitec.ch. *Hors fenêtre : test.de (2022), quechoisir (2018).*

**A3 (guides/agrégateurs) — citées** : new-baby.fr, bedbedtime.com, avis-parents (×2), babideal.fr (×2), electroguide.com, bebecool.fr, ecomparatif.fr, babyphone-sans-onde.fr, mon-centre-interphonie.com, la-maison-intelligente.fr, consomaman.fr, futura-sciences.com, fathercraft.com. *Bloqués : Forbes, chambredenfant, bebe9, babylist (limite outil).*

**A5 (sécurité/fiabilité) — citées clés** : github.com/xn0tsa/nobody-puts-baby-in-a-corner, smarthomeperfected.com/cloudedge-hack, blog.rankiteo.com (CVE Meari), arenti.com/pages/privacy, apis-us-west.arenti.net/…/Privacy.html, motherandbaby.com/…/momcozy-bm03, momcozy.com/…/baby-monitor-range, fcc.report/FCC-ID/2af2rhb30rx, todaysparent.com/vtech-dm221, walmart reviews (BOIFUN/VTech), mominformed.com (Motorola/Hubble). *Interrompu par quota avant Amazon ASIN directs + Philips WiFi + Reddit HelloBaby/Babysense.*

**A4 (fiches techniques) — ÉCHEC** : tué par limite de session (« resets 3pm UTC ») avant d'établir la grille ASIN. À relancer.

---

*Rapport produit par la skill `grech` (PR #24, non mergée — chargée depuis la branche pour cette passe). Persistance : commit sur `claude/init-session-xebv38`.*
