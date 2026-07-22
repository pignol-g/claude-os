# Recherche — ChatGPT vs Claude (rapport consolidé, 21 juillet 2026)

<!-- Version : 2026-07-21 v1.0 -->
<!-- Méthode grech : 4 agents Sonnet en parallèle, à partir de
     recherches/PROMPT-RECHERCHE_chatgpt-vs-claude_2026-07-21.md -->
<!-- Fichiers internes croisés : PROMPT-RECHERCHE_chatgpt-vs-claude_2026-07-21.md (recherche
     préliminaire, 12 requêtes) -->

## En-tête méthodo

- **4 agents Sonnet** en parallèle, ~254 tool-uses cumulés, ~2213s de durée max par agent :
  (1) tarifs/quotas officiels ChatGPT, (2) quotas & statut modèles Claude, (3) benchmarks &
  coût/token, (4) écosystème agentique & retours terrain.
- **≈300 sources consultées cumulées** (doublons inter-agents non dédupliqués), dont environ
  200 explicitement citées à l'appui d'une affirmation — largement au-dessus de la cible >100.
- **Limite rencontrée** : l'agent 1 (angle « sources officielles OpenAI ») n'a pas pu accéder
  directement à openai.com / chatgpt.com / help.openai.com — bloqués par la politique d'egress
  de l'organisation (confirmé même via miroir Wayback Machine ; community.openai.com et
  status.openai.com, eux, répondaient normalement). L'agent n'a pas tenté de contourner ce
  blocage. Les chiffres officiels ChatGPT ci-dessous sont donc **triangulés via 25+ sources
  techniques tierces concordantes**, pas vérifiés de première main. **Recommandation reprise
  du verdict de l'agent : rouvrir toi-même chatgpt.com/pricing et help.openai.com avant tout
  changement de plan pour confirmation directe.**

## TL;DR

- **Ta prémisse sur Fable 5 avait raison, mais pas pour la bonne raison.** Ce n'est pas la
  suspension export-control de juin (levée depuis le 1er juillet, non permanente). C'est un
  changement de facturation **du 20 juillet** (hier) : Fable 5 est sorti du forfait **Pro**
  (le tien) — accès désormais en crédits API payants ($10/$50 par MTok, crédit ponctuel de
  $100 jusqu'au 2 août). Il reste inclus en Max/Team/Entreprise Premium.
- **Le "Plus à 10€" est infirmé explicitement** : aucune offre officielle ne descend Plus
  sous ~23€ TTC en France/Belgique. C'est très probablement **ChatGPT Go (~8€)** que tu avais
  en tête — un palier en dessous, avec pub et sans mémoire/outils avancés.
- **Quotas GPT-5.6 sur Plus (20$)** : Sol 15-90 messages/5h, Terra 20-110/5h, Luna 50-280/5h
  (convergence 5+ sources, non vérifié en direct). Sur **Pro** ($100 ou $200 — pas de « Pro
  Codex »/« Pro Max » officiels, ce sont juste deux tiers "ChatGPT Pro" à 5x/20x Plus), les
  totaux ne sont pas publiés ; l'extrapolation communautaire donne ~75-450/5h (100$) ou
  ~300-1800/5h (200$). La limite des 5h est actuellement **levée temporairement** (12/07,
  Codex+Work seulement, pas le Chat général) — sans date de retour annoncée.
- **Aucun signal ne justifie un changement de plan sur la seule base des benchmarks** : Opus
  4.8 gagne sur le code réel (SWE-bench Pro, 69,2% vs 64,6% pour Sol) et coûte moins cher en
  usage mixte ; Sol/Sol Ultra gagne nettement sur l'agentique terminal et la latence. Les deux
  éditeurs sont en pleine « guerre des limites » instable (assouplissements temporaires des
  deux côtés) — tout chiffre de quota a une durée de vie courte en ce moment.

## La question et la prémisse

**Question initiale (reformulée)** : Guillaume, sur Claude Pro (20$/mois, quota serré),
demande un comparatif ChatGPT/Claude à jour suite à la sortie de GPT-5.6 et une rumeur de
retrait de Claude Fable 5, avec un focus sur les plans payants (notamment un ChatGPT Plus
perçu à 10€) et les quotas réels de GPT-5.6 en Plus/Pro.

**Prémisses corrigées** :
1. *« Retrait de Fable 5 »* — ✅ partiellement vraie, mais pas pour l'épisode qu'on pensait.
   La suspension export-control (12-30 juin) est résolue et non permanente. Le vrai
   changement, plus récent et plus pertinent pour Guillaume, est la sortie de Fable 5 du
   quota inclus du plan **Pro** depuis le 20 juillet 2026 (voir section Claude).
2. *« Plus à 10€ »* — ❌ infirmée. Confusion quasi certaine avec ChatGPT Go (~8€).

## Tableau des scénarios

| Scénario | Statut | Motif (sourcé) |
|---|---|---|
| Fable 5 définitivement retiré/déprécié | ❌ FERMÉ | Suspension export-control levée depuis le 01/07/2026, redéploiement mondial confirmé (anthropic.com/news, CNBC 30/06) |
| Fable 5 toujours inclus dans le forfait Pro | ❌ FERMÉ | Sorti du quota Pro depuis le 20/07/2026, accès en crédits API payants uniquement (support.claude.com/15424964, officiel) |
| Fable 5 inclus dans Max/Team/Entreprise Premium | ✅ OUVERT | Confirmé officiel, présenté comme permanent (même source) |
| ChatGPT Plus disponible à ~10€ en France/Belgique | ❌ FERMÉ | Aucune offre officielle trouvée ; seul palier proche est Go (~8€), palier inférieur avec pub (mac4ever.com, lerenardia.fr) |
| Promo étudiante ChatGPT Plus applicable en France | ❌ FERMÉ | Programme SheerID limité USA/Canada (clos), pilote invitation Australie/Colombie — pas France/Belgique (krater.ai) |
| GPT-5.6 = supériorité nette sur toute la gamme Claude | ❌ FERMÉ | Split net par tâche : Opus 4.8 devant sur code réel + coût mixte ; Sol devant sur agentique terminal + latence (SWE-bench Pro / Terminal-Bench 2.1, Artificial Analysis) |
| Limite des 5h ChatGPT définitivement supprimée | ❌ FERMÉ (pour l'instant) | "Temporaire" depuis le 12/07, Codex+Work seulement, aucune date de retour annoncée — statut volatil (bleepingcomputer.com) |
| Comparatif officiel simultané OpenAI/Anthropic existant | ❌ FERMÉ | Chaque éditeur cite des benchmarks tiers, jamais une suite conjointe (artificialanalysis.ai, blog Opus 4.8) |
| "Pro Codex" / "Pro Max" = noms officiels ChatGPT | ❌ FERMÉ | Les deux tiers s'appellent officiellement "ChatGPT Pro" ($100 et $200), distingués par multiplicateur seul (community.openai.com/1378752, 9to5mac) |

## Sections thématiques

### 1. Tarifs & quotas officiels ChatGPT (accès direct bloqué — triangulé via tiers)

Prix TTC France confirmés par recoupement : Free 0€ · Go ~8€ (lancé déc. 2025/janv. 2026,
avec pub) · Plus 20$ ≈ 23€ (22-24€ selon TVA ; 24,20€ Belgique à 21% TVA) · Pro 100$ ≈ 103€
(lancé 09/04/2026) · Pro 200$ ≈ 184-200€ · Business 20$/siège annuel ou 25$/mois (baissé de
25$/30$ le 02/04/2026) · Enterprise sur devis (estimation tierce non confirmée : 45-75$/siège,
~150 sièges minimum).

Correction terminologique importante : **"Pro Codex" et "Pro Max" ne sont pas des noms
officiels.** Les deux tiers Pro s'appellent tous deux "ChatGPT Pro" (100$/200$), distingués
par un multiplicateur d'usage (5x/20x Plus) annoncé le 09/04/2026.

Quotas GPT-5.6 sur Plus (convergence 5+ sources, non vérifié en direct) : Sol 15-90 msg/5h,
Terra 20-110/5h, Luna 50-280/5h. Sol n'est disponible qu'en Chat sur Plus (modes Medium/High) ;
Terra et Luna jamais en Chat standard, uniquement via Work/Codex/API ; le mode de raisonnement
maximal ("Sol Pro") exige le plan Pro, Business ou Enterprise depuis le 09/07 — l'ancien
plafond "~50 messages Pro-mode/semaine" (mai 2026) visait ce mode sur Plus et est obsolète
dans sa forme depuis. Les totaux Pro (5x/20x) ne sont pas publiés par OpenAI ; extrapolation
communautaire : ~75-450/5h (100$) ou ~300-1800/5h (200$). Fenêtres de contexte confirmées :
128K (Terra/Luna), 272K (Sol) côté app — à distinguer du contexte API (~1,05M tokens,
non revérifié ce passage).

Limite des 5h : levée temporairement depuis le 12/07/2026 (annonce Thomas "Tibo" Sottiaux,
OpenAI), mais **seulement pour Codex + ChatGPT Work**, pas la limite générale du Chat, sur
Plus/Business/Pro. Accompagnée d'une réduction temporaire de contexte (372k→272k, retour non
daté) et d'un gain d'efficacité Sol ~10%. Toujours active au 19-20/07, plafonds hebdomadaires
inchangés, aucune date de retour annoncée — statut explicitement temporaire.

### 2. Claude — quotas & statut des modèles

Anthropic ne publie aucun chiffre absolu pour Pro/Max — politique éditoriale assumée
(support.claude.com, plusieurs pages consultées). Structure confirmée : fenêtre glissante de
5h + plafond hebdomadaire séparé, partagés app Claude + Claude Code. Estimations communautaires
seules (non officielles) : ~45 messages/5h et ~40-80h Sonnet/semaine (Pro) ; ~140-280h Sonnet
+ 15-35h Opus/semaine (Max 5x) ; ~240-480h Sonnet + 24-40h Opus/semaine (Max 20x).

Chronologie des changements récents : 6 mai — doublement permanent des limites 5h Claude Code
(Pro/Max/Team/Entreprise à siège) + fin du throttling heures de pointe (Pro/Max). 13 mai —
+50% de limite hebdomadaire Claude Code, promo prolongée 4 fois : 13 juil. → 19 juil. →
**19 août 2026** (officiel, @ClaudeDevs + helpnetsecurity.com) — 4ᵉ report en 10 semaines,
statut volatil. 14 mai — projet de séparation de l'usage programmatique (Agent SDK, `claude -p`,
GitHub Actions) vers un pool de crédits séparé dès le 15 juin, **annulé avant application**.

**Fable 5/Mythos 5, chronologie complète** : lancés le 9 juin (long-horizon) → suspendus
mondialement le 12 juin 17h21 ET (directive export US, PAS une dépréciation) → contrôles levés
le 30 juin → redéploiement mondial le 1er juillet (nouveau classifieur bloquant >99% du
contournement signalé) → **période d'inclusion promotionnelle sur Pro/Max/Team expirée le 19
juillet 23:59:59 PT** → depuis le 20 juillet : Max/Team/Entreprise Premium gardent Fable 5
inclus (présenté comme permanent) ; **Pro et Team/Entreprise Standard perdent l'inclusion** —
accès en crédits API ($10/$50 par MTok) avec un crédit ponctuel de $100 (réclamable jusqu'au 2
août). Mythos 5 reste exclusivement Project Glasswing (sur invitation), jamais grand public.
Résidus : aucune restriction UE documentée ; Bedrock officiellement redéployé, Vertex/Foundry
sans date précise ; rumeur non vérifiée de contrôle chinois sortant côté Chine (2ᵉ main).

Positionnement : Sonnet 5 = cheval de travail courant, Opus 4.8 = défaut tâches difficiles,
Fable 5 = réservé aux tâches trop complexes/longues pour Opus 4.8 — pas un remplaçant du
quotidien.

### 3. Benchmarks & coût/token

**Correction au dossier initial** : les scores 63,2%/64,6% déjà cités comme "Terminal-Bench
2.1 quasi-égalité" sont en réalité ceux de **SWE-bench Pro**. Une fois démêlé :

- **SWE-bench Pro** (code réel, BenchLM maj 20/07) : Opus 4.8 69,2% (meilleur modèle actif) >
  Fable 5 80,0% signalé "suspendu" par ce site malgré le redéploiement — discordance à noter >
  Sol 64,6% > Terra 63,4% > Sonnet 5 63,2% > Luna 62,7%.
- **Terminal-Bench 2.1** (agentique terminal, forte divergence inter-harnais) : vals.ai donne
  Sol 85,8%, Fable 5 80,5%, Sonnet 5 74,5% ; Artificial Analysis donne Sol 88-89,5% ; OpenAI au
  lancement revendique Sol 88,8% (Sol Ultra 91,9%) ; BenchLM donne Sonnet 5 80,4%, Opus 4.8
  74,6% (ce dernier chiffre confirmé par le blog officiel Anthropic du lancement d'Opus 4.8).
  Sol devant de +10 à +17 points selon harnais/mode — traiter comme indicatif, aucune
  méthodologie commune.
- **AA Coding Agent Index** : Sol 80 (record) > Fable 5 77,2 > Terra 77 > Luna 75.
- **Aucun comparatif officiel simultané** : chaque éditeur cite des chiffres tiers (OpenAI cite
  Artificial Analysis pour Sol vs Fable 5 ; Anthropic ne compare que face à GPT-5.5/Gemini 3.1
  dans son dernier post officiel, pas de mise à jour face au 5.6).

**Tarification API officielle confirmée** : Claude — Haiku 4.5 $1/$5, Sonnet 5 $2/$10 (→ $3/$15
dès le 1er septembre 2026, hausse actée), Opus 4.8 $5/$25, Fable 5/Mythos 5 $10/$50 (par 1M
tokens in/out). GPT-5.6 — Sol $5/$30, Terra $2,50/$15, Luna $1/$6. Sol et Opus 4.8 partagent le
même prix d'entrée (5$) mais Sol coûte 20% de plus en sortie.

**Opus 4.8 vs Sol** (comparaison directe Artificial Analysis) : Intelligence Index à égalité
parfaite (56 chacun, chiffre volatil — une autre source tierce donne 58,9/55,7 à quelques
jours d'écart) ; prix mixte $4,35/1M (Sol) vs $3,85/1M (Opus 4.8, ~11% moins cher) ; Sol
nettement plus rapide au premier token (10,5s vs 27s), débit de sortie quasi identique.
Anthropic publie un exemple chiffré officiel : 1h de code avec Opus 4.8 (50k in/15k out) =
$0,705 sans cache, $0,525 avec cache — aucun équivalent officiel côté OpenAI trouvé. **Rappel
clé** : ces tarifs sont de l'API à l'usage, un modèle différent de l'abonnement forfaitaire
Pro à 20$/mois — la comparaison en dollars ne s'applique que si Guillaume bascule vers
l'API/Claude Code à l'usage.

### 4. Écosystème agentique & retours terrain

Retours réels sur les quotas GPT-5.6 : plaintes de quota épuisé "en quelques prompts" dès le
9/07, réponse OpenAI = levée temporaire du plafond 5h le 12/07 "après deux jours d'activité
intense" — le plafond hebdo, lui, n'a pas bougé, donc pas d'illimité réel. Anthropic a
réajusté ses propres limites 31 minutes après l'annonce OpenAI — lu par la communauté comme
réactif plutôt que stratégique.

Retours Claude Pro/Max : mitigés — doubler le plafond 5h ne change rien si le plafond hebdo
reste le mur réel ; précédent de méfiance (janvier 2026, mêmes plaintes après un bonus vacances
expiré, Anthropic avait nié toute coupe permanente). Un power-user rapporte être redescendu de
Max 20x à Max 5x après 6 semaines (n'utilisant que 30-50% du quota supérieur) et signale qu'à
**90% d'usage, Claude rétrograde silencieusement d'Opus vers Sonnet** — mécanisme peu
documenté officiellement, à vérifier si applicable en Pro.

Cowork vs ChatGPT Work : Cowork = desktop/filesystem-first, bonne réputation sur les refactors
multi-fichiers et la doc, mais UI jugée lente, coûts en tokens jugés excessifs ("12$ pour
corriger une coquille"), connecteurs Drive/Calendar peu fiables. **Alerte sécurité** :
rapport d'injection de prompt exfiltrant des identifiants via Cowork (promptarmor.com), plus
une plainte isolée de suppression de 11 Go de fichiers — signaux isolés mais à ne pas ignorer
si usage sur dossiers sensibles. ChatGPT Work (lancé 9/07) : retours encore trop frais pour un
verdict mûr, surtout de la confusion utilisateur vs Codex.

Sunset ChatGPT Atlas (9/08, confirmé officiellement) : lu par la communauté comme un pattern
"grandes annonces puis dépréciations discrètes" (comparé au sort de Sora) — signal de risque
produit côté OpenAI, pas un signal sur la qualité de GPT-5.6 en tant que tel.

Consensus dev (Reddit/HN, semaine du 9/07) : pas de vainqueur absolu. Sentiment pro-Sol
dominé par le prix ("$8,39 vs $21,63", "Terra à égalité avec Fable pour 1/4 du prix") ; sur
r/ClaudeCode, le commentaire le plus voté (478 upvotes) menace de migrer si Anthropic n'aligne
pas ses prix. Citation HN qui résume : *"GPT est le meilleur programmeur, Opus reste le
meilleur architecte système."*

## Coûts / plans — tableau comparatif

| Palier ChatGPT | Prix | Palier Claude | Prix |
|---|---|---|---|
| Free | 0€ | Free | 0$ |
| Go | ~8€/mois (avec pub, sans mémoire) | — | — |
| Plus | 20$ (~23€ TTC FR) | Pro | 20$ |
| ChatGPT Pro (100$, 5x Plus) | ~103€ | Max 5x | 100$ |
| ChatGPT Pro (200$, 20x Plus) | ~184-200€ | Max 20x | 200$ |
| Business | 20$/siège/an ou 25$/mois | Team | dès 20$/siège/an |
| Enterprise | sur devis | Enterprise | sur devis |

**Aucune offre à ~10€ n'existe des deux côtés** au niveau "Plus"/"Pro" — le point d'entrée
payant réel le plus proche est Go (~8€), avec des limitations fonctionnelles significatives
(pub, pas de mémoire, pas d'outils avancés).

## Recommandation pour Guillaume (Pro, dev, quota serré)

1. **Pas de cas clair pour basculer entièrement vers ChatGPT.** Sur le code réel, Opus 4.8
   gagne et coûte moins cher en usage mixte ; l'avantage de Sol est concentré sur
   l'agentique terminal et la vitesse — un profil différent d'un usage repo classique.
2. **Le vrai changement qui te concerne directement est la sortie de Fable 5 du quota Pro
   (hier).** Si l'accès à Fable 5 dans le forfait comptait pour toi, rester en Pro ne te le
   donne plus — seul Max (ou Team/Entreprise Premium) le garde inclus. À trancher : est-ce
   que Fable 5 spécifiquement t'apportait quelque chose que Sonnet 5/Opus 4.8 ne couvrent pas ?
3. **Si la frustration vient du quota serré plus que des capacités**, le levier le plus
   pertinent n'est pas de changer d'écosystème mais d'évaluer **Max 5x (100$)** — un
   power-user cité le juge suffisant sans besoin du 20x, mais c'est un saut de prix ×5 à
   mettre en face de ton usage réel.
4. **Les deux éditeurs sont en pleine instabilité de limites** (assouplissements temporaires
   récents des deux côtés, sans garantie de durée) — ne pas figer une décision de plan sur les
   chiffres de cette semaine précise ; revérifier avant d'agir.
5. **Si tu veux juste tester GPT-5.6** : Go (~8€) ou Plus (~23€) suffisent pour Sol en Chat,
   mais Terra/Luna ne sont accessibles que via Work/Codex/API — un vrai test de toute la
   famille demande plus qu'un abonnement Chat classique.

## Actions concrètes

| Action | Échéance |
|---|---|
| Revérifier chatgpt.com/pricing et help.openai.com en direct (accès agent bloqué ce passage) | Avant tout changement de plan |
| Décider si l'accès Fable 5 inclus justifie de rester/passer en Max | Avant le 2 août (fin du crédit $100 sur Pro) |
| Surveiller si la promo "+50% limite hebdo Claude Code" est prolongée au-delà du 19 août | 19 août 2026 |
| Vérifier si le downgrade silencieux Opus→Sonnet à 90% d'usage s'applique aussi en Pro | Pas d'échéance — à clarifier |
| Revérifier le statut de la levée temporaire du plafond 5h ChatGPT (Codex/Work) avant tout essai intensif | Avant un test GPT-5.6 |

## Annexe sources

Les 4 agents ont cumulé environ 300 sources consultées. Listes complètes conservées dans les
transcripts de session (non reproduites intégralement ici pour lisibilité) ; principales
sources **citées** à l'appui des affirmations ci-dessus :

**Agent 1 (tarifs ChatGPT)** : community.openai.com/t/1378752 · digitalapplied.com (usage
pools GPT-5.6) · bleepingcomputer.com (limites temporaires) · finance.biggo.com · mac4ever.com
· lerenardia.fr · glbgpt.com · iphonesoft.fr (Pro 103€, ×2 articles) · simplemetrics.xyz ·
winbuzzer.com · aitoolly.com · digg.com · krater.ai (promo étudiante) · familypro.io ·
gptprompts.ai · itdaily.com · 9to5mac.com (×2) · thenextweb.com · coworker.ai · inference.net ·
spendhound.com.

**Agent 2 (Claude/Fable5)** : anthropic.com/news/redeploying-fable-5 ·
support.claude.com/15424964 (Fable 5 hors Pro) · support.claude.com (11647753, 11145838,
11049741, 8325606, 12429409) · platform.claude.com (rate-limits, introducing-fable-5-mythos-5)
· helpnetsecurity.com · usecarly.com · truefoundry.com · verdent.ai · appwrite.io · morphllm.com
· x.com/ClaudeDevs · aboutamazon.com · cnbc.com · digitalapplied.com · appscale.blog ·
techtimes.com · xenospectrum.com · bleepingcomputer.com · pcworld.com (×2) · forbes.com (×2) ·
venturebeat.com · thehackernews.com · marktechpost.com.

**Agent 3 (benchmarks/coût)** : vals.ai · benchlm.ai (swePro, terminalBench2, ×4 comparatifs) ·
morphllm.com/swe-bench-pro · artificialanalysis.ai (×3) · platform.claude.com/pricing ·
x.com/OpenAI · x.com/ArtificialAnlys · eesel.ai (×3) · edenai.co (×2) · datacamp.com (×2) ·
layer3labs.io (×2) · officechai.com (×2) · llm-stats.com (×3) · swe-rebench.com ·
arxiv.org (2506.17208, 2603.23749) · the-decoder.com · openai.com/previewing-gpt-5-6-sol.

**Agent 4 (écosystème/terrain)** : five.reviews · explainx.ai · digitalapplied.com ·
paddo.dev · windowsforum.com · findskill.ai · 9to5google.com · verdent.ai · x.com/ClaudeDevs ·
helpnetsecurity.com · theregister.com · veracalloway.com (downgrade Opus→Sonnet) ·
jdhodges.com · eigent.ai · techsy.io · coworkhow.com · wonderingaboutai.substack.com ·
promptarmor.com · news.ycombinator.com (×2) · techcrunch.com · macrumors.com ·
business-standard.com · techbuzz.ai · piunikaweb.com · morphllm.com · botmonster.com.

*Rapport généré par méthode grech (4 agents Sonnet parallèles) à partir de
`recherches/PROMPT-RECHERCHE_chatgpt-vs-claude_2026-07-21.md`. Plusieurs chiffres marqués
volatils dans le corps du texte ci-dessus ont moins de 30 jours et peuvent avoir changé au
moment de la lecture.*
