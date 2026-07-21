# Prompt de recherche — ChatGPT vs Claude (édition juillet 2026)

<!-- Version : 2026-07-21 v1.0 -->
<!-- Généré par CC sur demande Guillaume (branche claude/chatgpt-claude-comparison-mnrdyr). -->
<!-- Usage : coller la section "PROMPT" ci-dessous dans Claude.ai (recherche avancée),
     ChatGPT (deep research), ou en entrée de la skill `grech` (voir "Version grech" en fin
     de fichier — angles déjà découpés, prêts à lancer en agents parallèles). -->
<!-- Pré-chargé avec 12 recherches web faites le 21/07/2026 pour ne pas repayer les bases —
     la vraie valeur d'une recherche plus poussée est dans les questions ouvertes (section B). -->

---

## 🎯 PROMPT (à copier à partir d'ici)

Tu es un analyste produits IA. Objectif : comparatif à jour au **21 juillet 2026** entre
**ChatGPT (OpenAI)** et **Claude (Anthropic)**, pour un développeur expérimenté, power-user,
actuellement en **Claude Pro (20$/mois)** avec un quota hebdomadaire serré, qui évalue si
changer de plan (Claude ou ChatGPT) serait rentable compte tenu des annonces récentes
(sortie de GPT-5.6, offres ChatGPT à bas prix, statut de Claude Fable 5).

### A. Déjà établi (21/07/2026, sourcé) — ne pas re-documenter, seulement signaler si contredit

**Modèles**
- **GPT-5.6** sorti le **9 juillet 2026** (preview limitée dès le 26 juin), après un délai lié
  à une revue gouvernementale. Famille à 3 variantes : **Luna, Terra, Sol** (Sol = flagship,
  raisonnement complexe / code / agentique).
- **Claude Fable 5** (+ **Mythos 5**) lancés le **9 juin 2026** (tâches longue durée). **Mis hors
  ligne du 12 au 30 juin 2026** suite à une directive export-control du gouvernement américain
  — **PAS une dépréciation** : redéploiement mondial confirmé depuis le **1er juillet 2026**.
  ⚠️ Contredit la prémisse « retrait de Fable 5 » — à ce jour Fable 5 est de nouveau disponible
  depuis 3 semaines. À vérifier : restrictions résiduelles par pays.

**Plans & tarifs (prix officiels annoncés, à reconfirmer — variable et volatile)**
- **ChatGPT** : Free (0$) · **Go (8$/mois, ~8€ TTC France, lancé 15/01/2026, ~98 pays, avec
  pub, pas de mémoire ni d'outils avancés)** · Plus (20$/mois, ~22-24€ TTC France) · depuis le
  09/04/2026 le palier Pro est scindé en **Pro Codex (100$, limites Codex élevées)** et
  **Pro Max (200$, quotas Deep Research + GPT-5 Pro les plus hauts)** · Business (20$/siège/an
  ou 25$/mois, min. 2 sièges) · Enterprise (sur devis).
  → **Hypothèse à vérifier en premier** : le prix « 10€ » évoqué correspond vraisemblablement
  à **ChatGPT Go (8€)**, pas à Plus (~20-24€). Aucune source ne confirme un Plus à 10€.
- **Claude** : Free (0$) · Pro (20$/mois) · **Max 5x (100$)** · **Max 20x (200$)** · Team
  (à partir de 20$/siège/mois annuel) · Enterprise (sur devis).

**Quotas connus (chiffres trouvés, fiabilité variable — voir annexe)**
- ChatGPT Plus : **160 messages / 3h** sur GPT-5.5/5.6 Instant, **3000 messages Thinking /
  semaine**, 80 uploads/3h ; fenêtre de contexte **32k (Instant) / 256k (Thinking, sélection
  manuelle)** côté app. Au-delà de 160/3h, bascule vers un modèle "mini".
- ChatGPT Pro : usage "illimité" en fair-use sur le mode standard, mais un plafond distinct
  **"~50 messages Pro-mode/semaine"** documenté en **mai 2026 — donc AVANT la sortie du 5.6**,
  à revérifier en priorité. Pro Codex (100$) vs Pro Max (200$) n'élèvent pas les mêmes limites.
  Signal récent (Bleeping Computer) : OpenAI aurait *temporairement* assoupli/retiré la
  restriction des 5h sur Plus/Pro/Business — statut à confirmer, changement très récent.
- API GPT-5.6 (Luna/Terra/Sol) : fenêtre de contexte **~1,05M tokens**, sortie max **128k
  tokens** (chiffre agrégé multi-sources, PAS vérifié sur une page officielle OpenAI — à
  confirmer en priorité).
- Claude Pro : **~45 messages / fenêtre glissante de 5h** + plafond hebdomadaire tous modèles
  confondus (réinitialisé à heure fixe par compte). Usage partagé entre l'app Claude et
  Claude Code (un usage intensif de Code mange le même quota que le chat).
  **Le 6 mai 2026**, Anthropic a **doublé de façon permanente** les limites 5h de Claude Code
  pour Pro/Max/Team/Enterprise à siège, et supprimé le throttling aux heures de pointe pour
  Pro/Max (le plafond hebdomadaire, lui, n'a pas changé).
- Claude Max 5x / 20x : littéralement 5× / 20× les limites du plan Pro (pas de chiffre absolu
  trouvé en messages/tokens — à préciser).

**Benchmarks / coût (Sol vs Sonnet 5 — comparaisons tierces, pas de suite officielle
tête-à-tête simultanée, à traiter comme indicatif)**
- Terminal-Bench 2.1 : Sonnet 5 **63,2 %** vs Sol **64,6 %** (quasi ex-æquo) ; **Sol Ultra
  91,9 %** dépasse tous les modèles Claude dont Opus 4.8 (78,9 %).
- Artificial Analysis Coding Agent Index : Sol **80** (meilleur score recensé) vs Claude
  Fable 5 **77,2**.
- Tarif API : Sol **5$/30$ par 1M tokens (in/out)** vs Sonnet 5 **2$/10$ par 1M** — Sol ~3×
  plus cher en sortie.

**Écosystème agentique**
- **Claude Cowork** : GA sur tous les plans payants depuis le **9 avril 2026** ; app desktop
  (macOS/Windows uniquement depuis mai 2026) ; point fort = fichiers locaux/dossiers.
- **ChatGPT Work** : lancé le **9 juillet 2026** (même jour que GPT-5.6), basé sur Codex,
  **1400+ connecteurs** cloud @-mentionnables ; point fort = SaaS cloud + rendu d'artefacts
  soigné.
- **ChatGPT Atlas** (navigateur) : sunset annoncé pour le **9 août 2026**, ~10 mois après son
  lancement.

### B. Questions ouvertes (priorité décroissante — c'est là que doit porter l'effort)

**B1 — PRIORITAIRE : quotas GPT-5.6 exacts par plan**
1. Sous **Plus (20$)**, combien de messages / tokens / heures d'usage réel de GPT-5.6 (Instant,
   Thinking, et Sol si accessible) — au-delà du discours marketing, croiser avec des retours
   d'utilisateurs si OpenAI reste vague dans sa doc officielle.
2. Sous **Pro Codex (100$)** et **Pro Max (200$)** : le plafond "~50 messages Pro-mode/semaine"
   (mai 2026) est-il toujours d'actualité après le lancement du 5.6 le 9 juillet ? Quel est le
   multiplicateur réel vs Plus ?
3. La suppression *temporaire* de la limite des 5h (Plus/Pro/Business) signalée par la presse
   est-elle toujours active au moment de la recherche ? Depuis quand, jusqu'à quand ?
4. Convertir ces plafonds en ordre de grandeur **tokens/mois comparable** à un plan Claude,
   pour permettre un calcul coût-par-token utile.

**B2 — Tarifs : lever le doute définitivement**
5. Confirmer sur les pages officielles (**openai.com/pricing**, **claude.com/pricing**) le prix
   TTC France exact, à la date de la recherche, de CHAQUE palier des deux côtés. Signaler toute
   offre promo/étudiante/régionale qui pourrait expliquer un Plus perçu à 10€.

**B3 — Claude : quotas chiffrés équivalents**
6. Chiffrer Pro (45 msgs/5h + cap hebdo) et Max 5x/20x en messages/tokens/heures de Claude Code
   directement comparables aux réponses de B1.

**B4 — Modèles : positionnement qualitatif complet**
7. Situer GPT-5.6 (Luna/Terra/Sol) face à la gamme Claude actuelle (Sonnet 5, Opus 4.8,
   Haiku 4.5, Fable 5/Mythos 5) par usage : code long-terme, agents, raisonnement, coût/token.
8. Restrictions résiduelles de Claude Fable 5 par pays après la levée de la suspension export.

**B5 — Écosystème agentique : lequel pour un dev solo**
9. Cowork vs ChatGPT Work pour un usage développeur solo (beaucoup de fichiers locaux +
   quelques SaaS) : lequel a l'avantage réel aujourd'hui, pas seulement sur le papier ?
10. Le sunset d'Atlas (9 août 2026) change-t-il une recommandation ChatGPT côté navigateur ?

### Exigences de sourçage et de format

- **Chaque chiffre sourcé** : URL + date de publication. Priorité aux pages officielles
  (openai.com/pricing, help.openai.com, claude.com/pricing, support.claude.com,
  anthropic.com/news) ; à défaut, croiser **au moins 2 sources indépendantes** et signaler
  toute divergence entre elles.
- Distinguer explicitement **officiel** vs **communautaire/estimé** (Reddit, forums, retours
  d'expérience) — les deux comptent mais ne jamais les confondre dans le rendu.
- Signaler comme **volatil** tout chiffre modifié il y a moins de 30 jours (le secteur bouge
  vite ; plusieurs faits ci-dessus datent de juillet 2026 et peuvent déjà avoir changé).
- Livrable : **(1)** TL;DR = verdict en 3-4 puces, **(2)** tableau plans/tarifs/quotas côte à
  côte (ChatGPT vs Claude), **(3)** tableau modèles/benchmarks/coût-token, **(4)** recommandation
  pour le profil utilisateur ci-dessus, **(5)** liste complète des URLs consultées.

---

## 🧩 Version `grech` (angles pré-découpés, prêts pour lancement multi-agents)

Si la suite se fait via la skill `grech` : 4 agents Sonnet en parallèle, chacun hérite du
bloc "Déjà établi" ci-dessus (`DÉJÀ CAPTÉ — NE PAS REDOCUMENTER`) + son angle :

1. **Agent "Tarifs & quotas officiels"** → questions B1 (1-4) + B2 (5). Sources : pages
   pricing/help officielles OpenAI et Anthropic. Plancher 20-25 sources.
2. **Agent "Claude — quotas & statut modèles"** → questions B3 (6) + B4-8. Sources : docs
   Anthropic, support.claude.com, anthropic.com/news.
3. **Agent "Benchmarks & coût/token"** → approfondir section benchmarks (comparateurs tiers,
   Artificial Analysis, DataCamp, edenai, etc.), vérifier si un comparatif officiel simultané
   est sorti entretemps.
4. **Agent "Écosystème agentique & retours terrain"** → questions B5 (9-10) + retours
   d'expérience réels sur les quotas (Reddit r/OpenAI, r/ClaudeAI, Hacker News) pour
   confronter le discours officiel à l'usage réel — angle le plus utile si les pages
   officielles restent vagues sur B1.

Format de réponse par agent : réponse par point sourcée, 700-800 mots max, section finale
« LISTE COMPLÈTE DES SOURCES CONSULTÉES » ([citée]/[consultée]), verdict en une phrase.

---

## 📎 Annexe — recherches déjà effectuées (21/07/2026, 12 requêtes WebSearch, session CC)

- [ChatGPT 5.6: Release Date, Models, Pricing & Access](https://coursiv.io/blog/chatgpt-5-6)
- [OpenAI Confirms GPT-5.6 Release Date After Government Review Delay](https://www.macobserver.com/news/openai-confirms-gpt-5-6-release-date-after-government-review-delay/)
- [GPT-5.6 - Wikipedia](https://en.wikipedia.org/wiki/GPT-5.6)
- [OpenAI to publicly release GPT-5.6 (CNBC, 08/07/2026)](https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html)
- [ChatGPT Plus Price in France (2026)](https://www.glbgpt.com/hub/chatgpt-plus-price-in-france-2026-cost-euro-pricing-features/)
- [ChatGPT Plus Price Comparison 2026: Global Pricing Guide](https://familypro.io/en/chatgpt-price-in-different-countries)
- [ChatGPT Plans: Free, Go, Plus, Pro, Business & Enterprise](https://www.gradually.ai/en/chatgpt-pricing/)
- [ChatGPT Pricing Guide: Free, Go, Plus, Pro (July 2026)](https://felloai.com/chatgpt-pricing-guide-free-go-plus-pro-alternatives-october-2025/)
- [ChatGPT Plans | OpenAI officiel](https://chatgpt.com/pricing/)
- [Claude Fable 5 Discontinued? What It Means (OutlierKit)](https://outlierkit.com/resources/claude-fable-5-discontinued/)
- [Introducing Claude Fable 5 and Claude Mythos 5 — Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)
- [Anthropic Releases and Temporarily Suspends Claude Fable 5 — InfoQ](https://www.infoq.com/news/2026/06/claude-5-release/)
- [Model deprecations — Anthropic docs](https://docs.anthropic.com/en/docs/about-claude/model-deprecations)
- [Claude Subscription Plans & Pricing 2026 — IntuitionLabs](https://intuitionlabs.ai/articles/claude-pricing-plans-api-costs)
- [Claude Max Plan: $100 vs $200 Pricing & Usage Limits — IntuitionLabs](https://intuitionlabs.ai/articles/claude-max-plan-pricing-usage-limits)
- [ChatGPT Plus Limits 2026: Every Cap — CustomGPT.ai](https://customgpt.ai/chatgpt-plus-limits-2026/)
- [ChatGPT Usage Limits in 2026 — tokenkarma](https://tokenkarma.app/chatgpt-usage-limit/)
- [Is ChatGPT Go Available in Europe? (2026 EU Status Update)](https://www.glbgpt.com/hub/is-chatgpt-go-available-in-europe/)
- [ChatGPT Go à 8 euros : que vaut l'abonnement avec pubs ?](https://www.studeria.fr/articles-de-blog/chatgpt-go-abonnement-ia-8-euros-publicites)
- [ChatGPT Go arrive en France — Usine Digitale](https://www.usine-digitale.fr/intelligence-artificielle/openai/chatgpt-go-arrive-en-france-les-details-de-la-formule-low-cost-dopenai-pour-attirer-les-utilisateurs.NTXPCD6DGVEJZDQZA4BGFSQNXQ.html)
- [Claude Code Rate Limits & Usage Quotas Explained (2026) — TrueFoundry](https://www.truefoundry.com/blog/claude-code-limits-explained)
- [What is the Pro plan? — Claude Help Center](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)
- [Claude Limits 2026: 5-Hour Sessions, Weekly Caps, API Rules — TokenMix](https://tokenmix.ai/blog/complete-claude-limits-guide-2026-tokens-uploads-5-hour)
- [Claude Sonnet 5 vs GPT-5.6 Sol vs Gemini 3.1 — edenai](https://www.edenai.co/post/claude-sonnet-5-vs-gpt-5-6-sol-vs-gemini-3-1-benchmarks-pricing-which-to-use)
- [GPT-5.6 Sol vs Claude Sonnet 5 — docsbot.ai](https://docsbot.ai/models/compare/gpt-5-6-sol/claude-sonnet-5)
- [Claude Sonnet 5 vs. GPT-5.6 — DataCamp](https://www.datacamp.com/blog/claude-sonnet-5-vs-gpt-5-6)
- [Claude Sonnet 5 vs GPT-5.6 Sol — BenchLM.ai](https://benchlm.ai/compare/claude-sonnet-5-vs-gpt-5-6-sol)
- [GPT-5.6 in ChatGPT — OpenAI Help Center](https://help.openai.com/articles/11909943)
- [About ChatGPT Pro tiers — OpenAI Help Center](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers)
- [OpenAI temporarily relaxes GPT-5.6 Sol usage limits — Bleeping Computer](https://www.bleepingcomputer.com/news/artificial-intelligence/openai-temporarily-relaxes-gpt-56-sol-usage-limits/)
- [Claude Changed: The July 2026 Way to Use it](https://emergingai.substack.com/p/claude-changed-the-july-2026-way)
- [OpenAI is folding Codex into the ChatGPT app — The New Stack](https://thenewstack.io/openai-codex-work-atlas/)
- [Claude Cowork vs ChatGPT Agents: 2026 Comparison — TECHSY](https://techsy.io/en/blog/claude-cowork-vs-chatgpt-agents)
- [Claude Features 2026 — Suprmind](https://suprmind.ai/hub/claude/features/)

*Ces recherches sont un premier passage (moteur de recherche + synthèse automatique), pas
une vérification page-par-page. La recherche plus poussée (section B) doit revérifier les
chiffres critiques directement sur les pages sources, surtout ceux marqués « à confirmer ».*
