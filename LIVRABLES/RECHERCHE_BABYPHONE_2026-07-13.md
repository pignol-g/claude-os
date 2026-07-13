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
2. **Le momcozy BM03 est le meilleur alignement à TES critères** : sans-WiFi pur (FHSS, aucune exposition internet), détection mouvement **ET** bruit, enregistrement clips sur SD **avec relecture locale sur l'écran parent**, et **la liaison la plus fiable** des retours consultés (aucun décrochage) — ce qui répond directement à ton problème GHB. **MAIS** (correction post-livraison) son prix réel est **145–220 € (svt 199,99 €), hors budget ≤100 €** — pas ~90 € comme indiqué initialement. Le **BOIFUN B0H1BXMHTH en mode strictement local** (~152 €) est un candidat équivalent qui **neutralise la faille Meari** (faille côté cloud) et ajoute le 24/7.
3. **Le score pondéré brut favorise le mainstream FR** (Babymoov ~95, Philips Avent/Babysense ~66, HelloBaby ~60) parce que les comparatifs FR sont quasi tous des blogs affiliés qui poussent ces marques — **le score n'est PAS la recommandation** ; il est corrigé par tes critères éliminatoires/prioritaires.
4. **Le budget ≤100 € est le vrai couperet** (vérifié A4 sur manuels) : quasiment tous les modèles ≤100 € **échouent sur la détection mouvement** (HelloBaby HB32/HB6550, Philips DECT, Babysense, Babymoov Simply/Yoo Go+) ou sur l'enregistrement (HelloBaby HB65 sans SD). **Seul le VTech VM924 (~65–70 €)** coche sans-WiFi + mouvement + son sous 100 € (réserve : relecture SD possiblement via app). Les mieux-disants (momcozy BM03, BOIFUN-local) sont à ~150–200 €.
5. **Qualité des sources faible** : aucun média national FR (Le Parisien, BFMTV…) ni test institutionnel récent ; seules Which? (UK), BabyGearLab et Fathercraft (US) ont une vraie méthodo terrain, mais hors marché FR et sans modèle sans-WiFi pur en tête.

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
| **momcozy BM03** | B0GHPKZHK9 | **145–220 € (svt 199,99 €)** | **Oui (FHSS pur)** | n-a (pas de wifi) | Clips 1 min/mvt, SD 32 Go incl., **relecture écran parent** | **Oui+Oui** | n-a (aucun cloud) | **Bonne** (3 étages, 0 décrochage) | **>100** | 4 | **47** | **✅ PASS élim. / hors budget** |
| Babymoov Yoo Moov | A014417 | ~110-120 € | Oui (radio privé) | n-a | Non documenté | Bruit oui / **Mvt incertain** (sources marketing, pas manuel — A4) | n-a | Moyenne-bonne | **>100** | 7 | **95** | ⚠️ mvt à confirmer + hors budget |
| Babymoov Simply Care / Yoo Go+ | — | 30-90 € | Oui (radio) | n-a | Non | **Mvt ABSENT** (VOX seul, A4) | n-a | Moyenne | ≤100 | (incl.) | — | ❌ FAIL (pas de mouvement) |
| Philips Avent DECT (SCD833/843/845) | — | 90-160 € | Oui (DECT) | n-a | Live, pas de SD | Bruit oui / **Mvt ABSENT** (confirmé manuel A4) | n-a | Bonne | mixte | 11 | **66** | ❌ FAIL (pas de mouvement) |
| Philips Avent Connected (SCD881…) | — | >150 € | **Non (WiFi)** | Non | App/cloud | Oui | non documenté | — | >100 | — | — | ❌ FAIL (wifi only) |
| Babysense V43 / MaxView | — | 120-230 € | Oui (radio) | n-a | Selon modèle | **Mvt ABSENT côté caméra** (A4 : détection = capteur respiration séparé Babysense 7) / bruit oui | n-a | Bonne | >100 | 6 | **66** | ❌ FAIL (pas de mouvement + >100 €) |
| HelloBaby HB65 | — | ~64 € | Oui (radio) | n-a | **Aucun (pas de slot SD)** | **Oui+Oui** (mvt confirmé A4) | n-a | Moyenne | ≤100 | 10 | **60** | ❌ FAIL (pas d'enregistrement local) |
| HelloBaby HB32 / HB6550 | — | 54-90 € | Oui (radio) | n-a | Non | Bruit oui / **Mvt absent (A4)** | n-a | Moyenne | ≤100 | (incl.) | — | ❌ FAIL (pas de mouvement) |
| **VTech VM924** | — | **~65–70 €** | **Oui (No WiFi)** | n-a | Clips SD **mais relecture via app MyVTech** (à vérifier) | **Oui+Oui** (mvt réglable sur écran, confirmé A4) | n-a | Bonne (DECT) | **≤100** | 7 | **47** | **✅ PASS élim.** (seul ≤100 €) |
| VTech DM1211 (audio) / VM901 (wifi) | — | 40-90 € | DM1211 oui / VM901 non | n-a | — | DM1211 pas de caméra / VM901 hybride | — | Bonne | ≤100 | (incl.) | — | ❌ FAIL (pas caméra / wifi) |
| Motorola (PIP1500/VM855/AM21) | — | 70-120 € | Oui (radio) selon modèle | n-a | Live | à confirmer | Hubble : **pas de 2FA** si wifi | Moyenne | mixte | 6 | ~40 | ⚠️ à confirmer |
| **BOIFUN** | B0H1BXMHTH | **~152 €** | Hybride — **écran dédié utilisable en mode local sans WiFi** (confirmé fiche Amazon.fr) | Oui | 2K, SD, relecture écran | Oui+Oui | AES-128 ; 5 CVE Meari/CloudEdge **mais côté cloud/P2P uniquement** → neutralisées si tenu 100% hors ligne | Moyenne (décrochages nocturnes signalés) | **>100** | 4 | **51** | ⚠️ **PASS élim. si strictement local** (cf. note sécu) — hors budget |
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

> ⚠️ **Correction post-livraison (prix + sécurité)** — voir la note dédiée en fin de section. Le momcozy BM03 est en réalité à **145–220 €** (et non ~90 €), donc **hors budget ≤100 €** ; et le BOIFUN en **mode strictement local** neutralise la faille Meari (faille côté cloud/P2P). Le classement ci-dessous intègre ces deux corrections.

### 🥇 1. momcozy BM03 (B0GHPKZHK9) — le meilleur alignement critères (mais >100 €)
- **Éliminatoires : PASS net** — sans-WiFi pur (FHSS), détection mouvement **et** bruit.
- **Priorités cochées** : aucune exposition internet (0 cloud, 0 app → **immunisé par conception** au risque Meari) ; enregistrement **local clips SD + relecture directe sur l'écran parent** ; **liaison la plus fiable** des retours (0 décrochage, 3 étages) — réponse directe au problème GHB.
- **Réserve** : **prix 145–220 € → hors budget** ; clips 1 min sur événement (pas de 24/7). À confirmer SAV : 100 % sans WiFi/app + relecture SD sur écran.

### 🥈 2. BOIFUN B0H1BXMHTH — en mode STRICTEMENT local (l'option 24/7)
- **Éliminatoires : PASS** en mode local — écran dédié fonctionnant **sans WiFi** (confirmé fiche Amazon.fr « WiFi or Local Mode »), détection **mouvement + cri**, enregistrement SD **24/7** relu à l'écran (avantage sur les clips du momcozy).
- **Sécurité** : la faille Meari est **côté cloud/P2P** → **neutralisée tant que l'appareil n'est JAMAIS appairé à l'app/WiFi**. Sûr **par discipline** (vs momcozy sûr par conception).
- **Réserve** : ~152 € (**hors budget**) ; **décrochages nocturnes signalés** dans les avis (à surveiller vu ton historique GHB) ; un seul appairage app l'enregistre sur le cloud vulnérable.

### 🥉 3. VTech VM924 (~65–70 €) — le SEUL ≤100 € qui passe les éliminatoires
- **PASS éliminatoires confirmé (A4, manuel)** : sans-WiFi (« No WiFi » explicite), **détection mouvement réglable directement sur l'écran parent** (MENU → Motion Detection → sensibilité), détection son.
- **Le seul modèle ≤100 € du corpus** dont la détection mouvement est prouvée par le manuel (tous les autres sous-100 € échouent : voir ci-dessous).
- **Réserve à lever au SAV** : la **relecture des clips SD** semble passer par l'app MyVTech Baby (le *live*, lui, reste 100 % écran sans WiFi) → si tu veux la relecture SD sur écran sans app, à vérifier avant achat.

**Pourquoi pas les autres ≤100 € (vérifié A4)** : HelloBaby HB65 (~64 €) = mouvement+son OK **mais aucun slot SD** ; HelloBaby HB32/HB6550 = **pas de mouvement** ; Philips Avent DECT = **pas de mouvement** (manuel) ; Babysense V43/MaxView = **pas de mouvement** caméra (la détection Babysense = capteur respiration séparé) ; Babymoov Yoo Moov = mouvement incertain + ~110 € ; Motorola PIP1500 No-WiFi = mouvement non confirmé (présent seulement sur la version Connect/WiFi).

**💰 Meilleur rapport qualité-prix ≤100 €** : **VTech VM924** (~65–70 €) — seul à cocher sans-WiFi + mouvement + son sous 100 €. Compromis : relecture SD possiblement via app (live OK sans app).

**⬆️ Si tu montes le budget (sans-WiFi maintenu)** : **momcozy BM03** (~150–200 €, sûr par conception, relecture SD sur écran sans app, liaison la plus fiable) ou **BOIFUN B0H1BXMHTH en mode strictement local** (~152 €, 24/7 SD, sûr si tenu hors ligne). Babysense MaxView (~229 €) écarté (pas de mouvement). À éviter : Nanit/Owlet/Cubo (WiFi-only → FAIL).

---

## Note — la faille Meari/CloudEdge et l'usage strictement local (correction)

**Ce qu'est la faille** : BOIFUN, ieGeek et Arenti reposent sur la plateforme cloud+app+P2P de l'OEM chinois **Meari** (marque grand public **CloudEdge**), partagée par 300+ marques. 5 CVE (CVE-2026-33356→62, mai 2026) : **clés cryptographiques P2P/DES/HMAC codées en dur et identiques sur tout le parc** (extraire la clé d'un appareil ouvre l'accès aux autres) ; **images d'alerte stockées en clair, sans auth, sur serveur Alibaba OSS (Chine)** ; ~1,1 M d'appareils joignables depuis internet.

**Point décisif** : c'est une faille du **canal internet/cloud/app**, PAS de la liaison radio locale. Un hybride utilisé **strictement sans WiFi** (jamais appairé à l'app, jamais connecté au cloud) **ne présente pas cette surface d'attaque** : rien n'est uploadé sur l'OSS, l'appareil ne rejoint pas le réseau P2P, il n'est pas joignable depuis internet. Le « FAIL sécurité » absolu initial valait pour l'usage **par défaut (connecté)**, pas pour un usage 100 % local.

**Ce qui départage momcozy et BOIFUN-local** :
- **momcozy = sûr par conception** : aucune capacité cloud/app (pur radio) → ne *peut pas* être mal connecté, surface cloud = zéro.
- **BOIFUN-local = sûr par discipline** : sûr tant qu'il reste hors ligne ; **un seul appairage app l'enregistre sur le cloud vulnérable**. Impossible de patcher hors ligne (mais inutile hors ligne).
- **Risque résiduel commun** : proximité radio (quelqu'un à portée), identique à tout babyphone radio, momcozy compris.
- **Fiabilité (séparé de la sécu)** : avis plus propres côté momcozy ; décrochages nocturnes signalés sur certains BOIFUN.

---

# D. Points d'incertitude à lever + questions SAV

| # | Incertitude | Impact | Action |
|---|---|---|---|
| 1 ✅ RÉSOLU | Détection mouvement par modèle (A4 relancé) | — | Vérifié sur manuels : seul **VTech VM924** passe sous 100 € ; HelloBaby/Philips DECT/Babysense/Babymoov échouent (voir §C) |
| 2 | **VTech VM924** : la **relecture des clips SD** se fait-elle sur l'écran parent, ou seulement via l'app MyVTech Baby ? | Détermine si le 🥉 ≤100 € coche aussi la relecture locale | SAV VTech : *« Sur le VM924, peut-on relire les clips enregistrés sur la carte microSD directement sur l'écran parent, sans l'application ? »* |
| 3 | **BOIFUN B0H1BXMHTH** : le « mode local » désactive-t-il **totalement** le WiFi/cloud (jamais d'upload OSS) ? La liaison locale est-elle FHSS radio ou point d'accès WiFi ? | Confirme la sécurité de l'usage 100 % local | SAV BOIFUN : *« En mode local, la caméra fonctionne-t-elle sans aucune connexion internet ni compte cloud ? La liaison caméra↔écran est-elle radio directe ? »* |
| 4 | momcozy BM03 : relecture SD sur écran **confirmée** (A4) ; reste le prix 145-220 € **hors budget** | Arbitrage budget | Décider : monter à ~150-200 € pour le mieux-disant, ou rester ≤100 € avec le VM924 |
| 5 | **CVE Meari/CloudEdge** : firmware ≥3.0.0 correctif déployé ? (pertinent seulement si tu comptes utiliser le WiFi) | Réhabiliterait l'usage connecté des hybrides | SAV BOIFUN/ieGeek/Arenti : *« Vos caméras 2026 embarquent-elles le firmware ≥3.0.0 corrigeant les vulnérabilités Meari (CVE-2026-33356 à 33362) ? »* |
| 6 | Clip-sur-événement (momcozy, VM924) vs 24/7 (BOIFUN local) | Arbitrage confort | Le 24/7 justifie-t-il de gérer la discipline « jamais de WiFi » du BOIFUN ? |

---

## Annexe — Sources par agent

**A1 (presse parentalité) — citées** : futura-sciences (×2), bebecool.fr, meilleurs.fr, avis-parents.com, nidenfant.fr, consobaby.com, laitfraisemag.fr, la-maison-intelligente.fr, babideal.fr, bebezecolo.fr, consomaman.fr. *Constat : angle presse pure quasi vide sur 24 mois (MagicMaman/Parents.fr/Doctissimo infetchables/non indexés).*

**A2 (médias tech/tests indé) — citées** : which.co.uk, babygearlab.com, fathercraft.com, thebump.com, selectos.eu, bedbedtime.com, passionteletravail.fr, nidenfant.fr, avis-parents.com, electroguide.com, futura-sciences.com, digitec.ch. *Hors fenêtre : test.de (2022), quechoisir (2018).*

**A3 (guides/agrégateurs) — citées** : new-baby.fr, bedbedtime.com, avis-parents (×2), babideal.fr (×2), electroguide.com, bebecool.fr, ecomparatif.fr, babyphone-sans-onde.fr, mon-centre-interphonie.com, la-maison-intelligente.fr, consomaman.fr, futura-sciences.com, fathercraft.com. *Bloqués : Forbes, chambredenfant, bebe9, babylist (limite outil).*

**A5 (sécurité/fiabilité) — citées clés** : github.com/xn0tsa/nobody-puts-baby-in-a-corner, smarthomeperfected.com/cloudedge-hack, blog.rankiteo.com (CVE Meari), arenti.com/pages/privacy, apis-us-west.arenti.net/…/Privacy.html, motherandbaby.com/…/momcozy-bm03, momcozy.com/…/baby-monitor-range, fcc.report/FCC-ID/2af2rhb30rx, todaysparent.com/vtech-dm221, walmart reviews (BOIFUN/VTech), mominformed.com (Motorola/Hubble). *Interrompu par quota avant Amazon ASIN directs + Philips WiFi + Reddit HelloBaby/Babysense.*

**A4 (fiches techniques) — relancé le 13/07 (GO `a4A`), abouti — citées** : amazon.fr/…/B0GHPKZHK9, idealo.fr (prix BM03), documents.philips.com (manuel SCD843, confirme absence mouvement), babysensemonitors.com (confirme mouvement = capteur respiration séparé), consobaby.com (Babymoov Yoo Moov), manualslib/manualzz (HelloBaby HB32/HB65), vtp-media.com (manuel VM924), camelcamelcamel (prix VM924), motorolanursery.com. *Verrouille la détection mouvement par modèle : seul VTech VM924 passe ≤100 €.*

---

*Rapport produit par la skill `grech` (PR #24, non mergée — chargée depuis la branche pour cette passe). Persistance : commit sur `claude/init-session-xebv38`.*
