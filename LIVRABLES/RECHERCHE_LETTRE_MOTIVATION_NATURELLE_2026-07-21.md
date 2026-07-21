# Recherche — Meilleure méthode pour une lettre de motivation naturelle avec Claude

**Date** : 2026-07-21 (mis à jour même jour après retour de Guillaume) · **Méthode** : grech
(recherche approfondie multi-agents)
**Agents** : 4 (Sonnet) · **Sources cumulées** : ~211 (56 + 38 + 53 + 62 + 2, avec recoupements)
**Fichiers internes croisés** : `CLAUDE-DNA-CC-CORE.md` (§ Rédiger à la voix de Guillaume),
`profil-redactionnel-guillaume.md`, `.claude/skills/asana-pass/SKILL.md`

> ⚠️ **Voir l'Addendum en fin de document** : Guillaume a confirmé avoir déjà testé un vrai
> profil rédactionnel (dans `candidaturePilote`, avec **Opus 4.8**, pas Sonnet) sans succès, et
> que le feature "Styles" de claude.ai recommandé ci-dessous a été retiré (migration vers
> "Skills"). Ça déplace le diagnostic vers l'hypothèse "outil" (§TL;DR point 1) plutôt que
> "donnée de style manquante" (§TL;DR point 2, à lire avec cette réserve).

---

## TL;DR

- **Le suspect n°1 n'est ni le modèle ni ChatGPT vs Claude : c'est l'outil.** Le system prompt
  public de Claude Code impose la concision ("fewer than 4 lines", "minimize output tokens",
  "avoid preamble") — un outil conçu pour du terminal/code, pas pour de la prose. Ça suffit à
  expliquer le ton sec/synthétique observé, indépendamment de la qualité de Claude lui-même.
  **Confirmé par Guillaume** : même avec un vrai profil de voix chargé et Opus 4.8 (le modèle le
  plus capable), le résultat reste artificiel dans Claude Code — l'outil semble bien être le
  facteur dominant, pas la donnée de style ni le modèle.
- ~~Trouvaille interne~~ **Nuancé après retour de Guillaume** : le fichier censé injecter TA vraie
  voix avant toute rédaction (`profil-redactionnel-guillaume.md`, imposé par ton propre CLAUDE.md)
  est un stub vide côté `claude-os`, mais un vrai profil existait et a été **utilisé** côté
  `candidaturePilote` — et ça n'a pas suffi. Voir Addendum pour le diagnostic révisé.
- **La pollution de contexte est un facteur réel et documenté** (pas une hypothèse) : Anthropic a
  elle-même publié un post-mortem où une seule ligne de contrainte système a mesurablement
  dégradé la qualité, et a coupé 80% du system prompt de Claude Code pour les modèles Fable 5
  pour cette raison.
- **Aucune donnée n'établit un modèle Claude "plus naturel"** qu'un autre pour ce type de tâche —
  Fable n'est PAS un modèle créatif malgré son nom (positionné code/agentique long-horizon par
  Anthropic). Le vrai levier disponible : le feature produit **"Styles → Add a Writing Example"**
  de claude.ai, quasi inconnue, qui fait exactement ce que le fichier profil aurait dû faire.

---

## La question et la prémisse

Question posée : *quel modèle Claude et quelle méthode donnent la lettre de motivation la plus
naturelle, et pourquoi ChatGPT (réputé moins naturel) fait mieux en pratique ?*

**Prémisse corrigée** : la comparaison Claude vs ChatGPT est probablement la mauvaise question.
La variable qui explique l'écart observé est plus vraisemblablement *Claude Code (outil CLI
terse) + profil de voix jamais rempli*, pas *Claude (le modèle) vs ChatGPT (le modèle)*. Les
comparatifs qui existent sur le naturel Claude/ChatGPT (peu fiables, contenu marketing) penchent
même plutôt en faveur de Claude sur l'écriture longue.

---

## Tableau des scénarios

| Scénario | Statut | Motif |
|---|---|---|
| Un modèle Claude (Opus/Sonnet/Fable/Haiku) est objectivement plus "naturel" pour ce cas d'usage | ❌ FERMÉE | Aucune model card ni benchmark Anthropic ne compare la naturalité rédactionnelle par modèle. Fable n'est pas positionné créatif. |
| Fable est le bon choix pour de la rédaction créative | ❌ FERMÉE | Positionnement officiel Anthropic : code/migrations volumineuses, sessions agentiques longues — pas de mention "voix"/"prose" dans les sources primaires. |
| ChatGPT est objectivement meilleur que Claude pour un texte naturel | ❌ FERMÉE (pas confirmée) | Aucune étude sérieuse ; les comparatifs marketing existants penchent plutôt pour Claude en écriture longue. |
| Le system prompt de Claude Code (terseness) dégrade la prose | ✅ OUVERTE — probable | Documenté noir sur blanc dans le system prompt public de l'outil ("fewer than 4 lines", "minimize output tokens"). |
| Le CLAUDE.md volumineux de Guillaume dilue les consignes de style | ✅ OUVERTE — plausible et documenté en général | "Context rot"/"lost in the middle" confirmés académiquement + post-mortem Anthropic avril 2026 ; pas de test A/B publié sur CE cas précis. |
| Le fichier de profil rédactionnel jamais rempli explique une bonne part du problème | ✅ OUVERTE — quasi certaine | Fait vérifié dans le dossier : stub vide, jamais migré depuis `candidaturePilote`, alors que le CORE l'impose "AVANT toute rédaction". |
| Réglable via la température/top_p dans Claude Code ou claude.ai | ❌ FERMÉE | Aucun réglage d'échantillonnage exposé sur ces deux canaux (API seulement). |
| Le feature "Styles" de claude.ai peut remplacer le profil manquant | ✅ OUVERTE — solution directe disponible | Fonctionnalité produit officielle, "Add a Writing Example" = few-shot calibré sur ta propre écriture. |

---

## Sections thématiques

### 1. Modèles Claude — naturalité rédactionnelle
Aucune source primaire Anthropic ne classe Opus/Sonnet/Fable/Haiku sur la naturalité créative.
Signal indirect communautaire : un flux "analyse avec Opus, rédaction avec Sonnet" est cité comme
"sweet spot" pour les lettres de motivation (source secondaire, non officielle). Fable 5 est
documenté officiellement comme modèle pour code/agentique long-horizon, PAS créatif — les
affirmations contraires viennent uniquement de blogs SEO tiers. Ni Claude Code ni claude.ai
n'exposent de réglage de température. Anthropic documente "AI slop" uniquement pour le design
frontend, aucune section équivalente officielle pour la prose.

### 2. Pollution de contexte (CLAUDE.md / system prompt)
Facteur réel et documenté, pas une hypothèse en l'air : concepts académiques convergents
("instruction dilution", "lost in the middle", "context rot"), et un cas concret publié par
Anthropic elle-même (post-mortem 16-23 avril 2026) où l'ajout d'une seule ligne de contrainte
système a dégradé la qualité de 3% de façon non anticipée en tests internes. Anthropic a depuis
coupé 80% du system prompt de Claude Code pour les modèles Fable 5, expliquant que trop de
contraintes "brident" plutôt qu'elles ne guident. Doctrine officielle : garder CLAUDE.md concis,
construit itérativement, plutôt qu'exhaustif. Pas de test A/B publié spécifiquement sur "rédaction
avec/sans CLAUDE.md volumineux", mais l'extrapolation est cohérente et vient d'Anthropic elle-même.

### 3. Claude vs ChatGPT/Gemini
Aucun benchmark indépendant sérieux. Les seules comparaisons disponibles sont du contenu
marketing d'outils de candidature concurrents, non répliqué — et elles penchent majoritairement
pour Claude, pas ChatGPT, contredisant la prémisse de départ. **Explication technique la plus
solide trouvée** : le system prompt public de Claude Code impose explicitement la terseness
("answer concisely with fewer than 4 lines", "avoid unnecessary preamble/postamble", "minimize
output tokens") — un biais d'outil (CLI conçu pour du code), pas de modèle. Distinction de
registre documentée : Claude est crédité en "long-form prose, nuanced tone" ; ChatGPT en
"short-form copy, structured business writing" — or une lettre de motivation est justement un
format court et structuré, terrain plus favorable à ChatGPT selon cette grille. Différence
d'alignement documentée : Anthropic (Constitutional AI/RLAIF, plus de nuance/hedging) vs OpenAI
(RLHF classique, plus tranché) — explique un style différent, pas une hiérarchie de qualité.

### 4. Techniques anti-"IA slop"
Technique la mieux documentée, convergente entre sources officielles Anthropic et guides
communautaires : **few-shot avec ses propres écrits + dialogue itératif court** (brouillon →
resserrement → passage voix), plutôt qu'un prompt unique exhaustif. Anthropic recommande des
instructions positives ("écris en prose fluide") plutôt que négatives ("n'utilise pas de
markdown"). Listes de clichés à bannir existent et sont utiles en complément mais insuffisantes
seules (FR : "crucial", "fort de mon expérience", "il est important de noter" ; EN : "delve",
"leverage", "pivotal", "in today's fast-paced world"). Signal recruteur documenté : homogénéité de
longueur de phrase (15-22 mots) = signal IA détecté ; casser volontairement ce rythme aide.
Claude.ai propose officiellement "Styles → Add a Writing Example" pour ce calibrage — exactement
la fonction que le fichier profil interne de Guillaume aurait dû remplir.

---

## Coûts / recours

Aucun coût financier — uniquement du temps de configuration (une fois) :
- Créer un Style claude.ai avec exemples perso : ~10 min, gratuit (inclus Pro).
- Rapatrier le vrai profil rédactionnel depuis `candidaturePilote` : quelques minutes de copier-coller.
- Modèle recommandé par défaut : **Sonnet** (rapide, cité comme "sweet spot" pour ce cas d'usage,
  économe en quota Pro). Opus en option pour une lettre à fort enjeu si Guillaume veut comparer.
  **Fable à éviter pour cet usage** (mauvais outil, conçu pour du code/agentique).

---

## Actions concrètes

1. **Immédiat** — Utiliser le prompt-type ci-dessous **dans claude.ai chat**, pas Claude Code,
   pour la prochaine lettre.
2. **Cette semaine** — Créer un Style claude.ai "Voix Guillaume" (Settings → Styles → Add a
   Writing Example) avec 2-3 textes que Guillaume a réellement écrits (mails, anciennes LM
   dont il est content). Réutilisable pour toutes les rédactions futures, pas que les LM.
3. **Dès que possible** — Rapatrier le vrai contenu de
   `candidaturePilote/livrables/lettres/_templates/profil-redactionnel-guillaume.md` dans le
   stub vide `claude-os/profil-redactionnel-guillaume.md`. Nécessite d'ajouter le repo
   `candidaturePilote` à une session Claude Code si Guillaume veut que ce soit fait pour lui —
   sinon copier-coller manuel.
4. **Si Claude Code reste nécessaire** (accès aux données de candidature) — ajouter une
   instruction explicite anti-terseness au prompt à chaque fois ("ceci est de la rédaction, pas
   du code — ignore les règles de concision par défaut, écris en prose complète"), ou lancer la
   rédaction finale dans un projet sans CLAUDE.md chargé.

### Prompt-type prêt à copier-coller (claude.ai chat, modèle Sonnet)

```
Tu es un rédacteur qui m'aide à écrire une lettre de motivation à MA voix, pas la tienne.

CONTEXTE : [poste visé, entreprise, 3-4 points clés de mon parcours pertinents pour ce poste]

MA VOIX — voici 2-3 exemples de texte que j'ai écrit moi-même, pour que tu calibres ton style
sur le mien et pas un style générique :
<example>
[coller un mail ou une lettre déjà écrite par moi]
</example>
<example>
[coller un deuxième exemple]
</example>

CONSIGNES DE STYLE (ce que je veux, pas ce que je ne veux pas) :
- Phrases de longueur variée (8 à 30 mots), jamais toutes identiques.
- Un détail concret et vérifiable par paragraphe (chiffre, fait, projet réel) plutôt qu'une
  affirmation générale.
- Ton direct, pas d'emphase artificielle, pas de superlatifs.
- Prose fluide en paragraphes, pas de liste à puces.
- Interdits explicites : "fort de mon expérience", "je suis convaincu que", "n'hésitez pas à me
  contacter", "passionné par", "opportunité unique", "crucial", "il est important de noter".

MÉTHODE : écris un premier brouillon complet. Je te dirai ensuite quoi resserrer — ne vise pas
la perfection au premier jet.
```

---

## Annexe — sources consultées

## Addendum — précisions de Guillaume après lecture (2026-07-21, validé avec corrections)

**Précisions reçues :**
1. Un profil rédactionnel avait déjà été **utilisé** (pas juste écrit) dans le projet
   `candidaturePilote` — **sans succès**. Le stub vide de `claude-os` n'était donc pas la seule
   cause : un vrai profil a existé et a échoué à produire un résultat naturel.
2. Modèle réellement utilisé : **Opus 4.8** dans Claude Code (pas Sonnet).
3. Tentative de créer un "Style" claude.ai comme recommandé → **fonctionnalité indisponible**,
   redirige maintenant vers "Skills".

**Diagnostic révisé** : le fait qu'un vrai profil de voix ait été chargé avec Opus 4.8 (le modèle
le plus capable, pas un modèle économique) dans Claude Code et ait quand même produit un texte
artificiel **renforce fortement l'hypothèse "outil"** (§3 ci-dessous : system prompt de Claude
Code optimisé pour la concision/le code) au détriment de l'hypothèse "donnée de style manquante".
Le profil existait ; il a été dilué ou écrasé par le comportement par défaut de l'outil CLI, pas
par une lacune de contenu.

**Styles → Skills, vérifié (recherche fraîche, 2026-07-21)** : Anthropic retire progressivement
le feature "Styles" de claude.ai au profit de "Skills" (migration en cours depuis juin 2026 —
[ai-toolbox.co](https://www.ai-toolbox.co/claude-management-and-productivity/how-to-set-up-claude-custom-instructions-2026),
[howtogeek.com](https://www.howtogeek.com/claude-feature-solved-biggest-frustration-anthropic-killed-it/)).
Différence importante et documentée : les Styles s'appliquaient automatiquement à **chaque**
message d'une conversation ; les Skills sont invoquées **seulement quand Claude juge que c'est
nécessaire** — un utilisateur documente explicitement cette régression de fiabilité pour un usage
qui doit "toujours" s'appliquer. Méthode actuelle pour fabriquer un skill de voix (sources
convergentes : [aiblewmymind.substack.com](https://aiblewmymind.substack.com/p/claude-skills-ai-write-like-you),
[joelmoran.com](https://joelmoran.com/guides/claude-voice-skill/)) : coller 4-6 textes dont on est
content → demander à Claude d'en extraire un guide de voix structuré (vocabulaire, structure de
phrase, tics) → l'empaqueter en Skill (Customize → Skills → Create skill, upload zip). **Piège
documenté** : Claude tend à **exagérer** les patterns détectés (parenthèses occasionnelles →
systématiques) sauf si on donne des règles absolues ("jamais X") plutôt que molles ("évite si
possible X").

**Recommandation mise à jour :**
- Vu la fiabilité incertaine du déclenchement des Skills, ne pas compter dessus seules pour un
  besoin "toujours actif" — soit les référencer explicitement dans le prompt à chaque lettre,
  soit garder la méthode few-shot directe (coller le profil dans le prompt), plus robuste.
- Séparer "recherche/données candidature" (peut rester en Claude Code) de "rédaction finale" (à
  faire en claude.ai chat, ou en demandant explicitement à Claude Code d'ignorer ses réflexes de
  concision pour cette tâche précise — ex. "ceci est de la prose, pas du code, ignore les règles
  de brièveté par défaut").
- Reconstruire le profil de voix selon la méthode "4-6 échantillons + règles absolues anti-tics",
  pas un profil générique de ton — le profil précédent (`candidaturePilote`) a peut-être échoué
  faute de ces règles absolues.
- **Question ouverte** : pourquoi le profil déjà utilisé dans `candidaturePilote` n'a pas suffi ?
  Sans voir son contenu réel, impossible à diagnostiquer précisément (mauvais format ? pas assez
  concret ? pas de règles absolues ? jamais vraiment chargé dans le contexte au moment de la
  rédaction ?).

---

## Addendum 2 — le vrai diagnostic était déjà dans `candidaturePilote` (2026-07-21, après inspection)

Guillaume a autorisé l'ajout du repo `candidaturePilote` à la session. Inspection de
`livrables/lettres/_templates/profil-redactionnel-guillaume.md` (le vrai fichier, pas le stub
claude-os) et de `.claude/skills/voix-guillaume/` + `.claude/skills/lm-francaise/`.

**Ce fichier n'est pas un stub — c'est un profil très riche** : corpus de 5 vraies LM 2024
(Oyonnair, Alpine, Twin Jet, Air France, HOP!), banque d'expressions verbatim FR+EN, structure
type, tics identifiés (ex. "la sécurité toujours citée en dernier"), garde-fous anti-invention de
faits. Deux skills Claude Code existent déjà pour l'appliquer. Et surtout : **le journal §11 du
profil documente qu'un ancien problème identique a déjà été diagnostiqué et résolu, le
2026-06-27** — avant que Guillaume ne relance la question aujourd'hui.

**Ce que dit le journal (verbatim, 2026-06-27) :**
> « Leçon de méthode (session chat) : **les règles abstraites font régresser la voix vers le
> corporate-ampoulé** (Erreur n°1 du CR). La rédaction doit partir du **corpus en contexte**
> (imiter une vraie lettre), pas des règles ; les interdits ne valent que littéraux et courts, en
> checklist de relecture. »
>
> « Modèle : la rédaction se fait de préférence sur **Sonnet** (**Opus sur-analyse et régresse**).
> Déléguer la rédaction à un sous-agent Sonnet. Skill de génération de LM à créer (prochaine
> étape) pour figer ce flux et ne plus dériver. »

Autrement dit : **une session précédente a testé exactement le scénario que la recherche
d'aujourd'hui devait élucider, et a trouvé que (1) donner une liste de règles de style abstraites
(comme le §8 "À FAIRE / À ÉVITER" du même profil) fait empirer le naturel, pas l'inverse, et que
(2) Opus sur-analyse et produit un résultat plus artificiel que Sonnet sur cette tâche
précise.** Preuve que la méthode corpus-first + Sonnet fonctionne : la lettre
`livrables/lettres/candidatures/buzz-737-v1.md` (générée le 2026-06-27 avec cette méthode) est
au ton naturel, très proche du corpus réel — seul le paragraphe "fit compagnie" y est signalé
incomplet (un problème de données, pas de voix).

**Pourquoi ça a quand même échoué pour Guillaume avec Opus 4.8 :**
1. **Le point (2) — Sonnet plutôt qu'Opus — n'a jamais été codifié dans les skills.** Ni
   `voix-guillaume/SKILL.md` ni `lm-francaise/SKILL.md` ne mentionnent le choix du modèle ou la
   délégation à un sous-agent Sonnet, alors que le journal le préconisait explicitement et
   annonçait la création d'un skill pour "figer ce flux". La leçon a été apprise mais jamais
   appliquée dans la procédure — rien n'empêche de rédiger directement avec Opus en agent
   principal, ce qui reproduit le mode d'échec déjà identifié.
2. **Risque de contournement du bon fichier** : la règle globale `CLAUDE-DNA-CC-CORE.md` §"Rédiger
   à la voix de Guillaume" pointe vers `claude-os/profil-redactionnel-guillaume.md` (le stub
   vide) comme "source de vérité unique". Si une lettre est demandée hors du contexte du projet
   `candidaturePilote` (ou si les skills locales ne se déclenchent pas), Claude Code peut retomber
   sur cette règle globale et charger le stub vide plutôt que le vrai profil du projet — plus
   fiable de rester dans candidaturePilote et d'invoquer explicitement `lm-francaise`.
3. **`REMONTEES-OS.md` (candidaturePilote) confirme le trou** : l'item **R-002** ("promouvoir le
   profil en artefact global") est toujours en `⏳ À remonter` depuis le 2026-06-13, jamais
   tranché ni migré — cohérent avec le stub vide trouvé côté claude-os.

**Diagnostic final (celui qui prime sur tout ce qui précède dans ce rapport)** : ce n'est ni la
pollution de contexte générique, ni un déficit de données de style, ni Claude vs ChatGPT — c'est
**une leçon déjà apprise (corpus-first + Sonnet, pas Opus) qui n'a jamais été gravée dans la
procédure** (les skills), et **un risque de repli sur le mauvais fichier** (stub global vide) si
la session ne reste pas dans le bon repo/skill.

**Actions concrètes révisées :**
1. Ajouter au `SKILL.md` de `lm-francaise` (et `voix-guillaume`) une ligne explicite : "Modèle :
   Sonnet par défaut pour la rédaction — ne pas laisser Opus rédiger directement (sur-analyse et
   régresse vers un ton corporate, cf. journal profil §11 2026-06-27). Déléguer à un sous-agent
   Sonnet si la session tourne sur Opus."
2. Trancher R-002 une bonne fois : soit vraiment migrer/globaliser le profil (et le CORE pointe
   correctement), soit assumer que ce profil reste scopé à `candidaturePilote` et corriger le CORE
   pour ne pas laisser une session hors-projet retomber sur un stub vide silencieusement.
3. Toujours rédiger une LM **en restant dans le repo `candidaturePilote`**, en invoquant
   explicitement le skill `lm-francaise` (ne pas rédiger en freestyle dans une session Opus
   générique).
4. Le prompt-type et le conseil "Styles claude.ai" des addenda précédents restent valables comme
   **filet de sécurité** si Guillaume rédige hors Claude Code, mais la vraie solution pour les LM
   pilote est déjà construite dans `candidaturePilote` — il manque juste (1) et (2) ci-dessus.

---

### Agent 1 — Modèles Claude (naturalité rédactionnelle) — 56 sources
https://www.anthropic.com/claude/fable [citée] · https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5 [citée] · https://claude.com/resources/tutorials/choosing-the-right-claude-model [citée] · https://platform.claude.com/docs/en/api/messages [citée] · https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices [citée] · https://willfrancis.com/how-to-stop-claude-writing-like-an-ai/ [citée] · https://github.com/anthropics/claude-code/issues/6096 [citée] · https://github.com/deepseek-ai/awesome-deepseek-integration/issues/531 [citée] · https://reapply.app/blog/claude-vs-chatgpt-cover-letters [citée] · https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf [citée] · https://aiforanything.io/blog/claude-model-selection-guide-haiku-sonnet-opus-2026 [citée] · https://www.buildmvpfast.com/articles/best-llms-2026-guide/creative-writing-ai [citée] · https://www.chatprd.ai/how-i-ai/claude-fable-5-review [citée] · https://yellow.com/news/sol-fable-5-creative-writing-test [citée] · https://opentools.ai/news/anthropics-claude-ai-gets-a-writing-style-makeover-customize-away [citée] · https://claude.com/blog/styles [consultée-404] · https://www.tomsguide.com/ai/claude-lets-you-personalize-your-ai-writing-heres-how [consultée] · https://knightli.com/en/2026/05/08/anthropic-claude-model-lineup/ [consultée] · https://www.usecarly.com/blog/claude-models-explained/ [consultée] · https://www.remoteopenclaw.com/blog/best-claude-models-2026 [consultée] · https://www.secondtalent.com/resources/every-claude-ai-model-explained-compared/ [consultée] · https://www.sitepoint.com/claude-model-selection-framework/ [consultée] · https://tygartmedia.com/claude-models-comparison/ [consultée] · https://github.com/danny-avila/LibreChat/discussions/3376 [consultée] · https://github.com/danny-avila/LibreChat/issues/3374 [consultée] · https://claudhq.com/claude-temperature-settings-guide/ [consultée] · https://clskillshub.com/blog/claude-temperature-settings-guide [consultée] · https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-request-response.html [consultée] · https://github.com/ccbogel/QualCoder/issues/1125 [consultée] · https://platform.claude.com/docs/en/claude_api_primer [consultée] · https://tokenmix.ai/blog/claude-temperature-control-2026 [consultée] · https://likeone.ai/blog/claude-temperature-settings-guide/ [consultée] · https://tomarcher.io/posts/temperature-top-p-creativity-knobs/ [consultée] · https://models.dev/models/anthropic/claude-fable-5/ [consultée] · https://findskill.ai/blog/how-to-prompt-claude-fable-5/ [consultée] · https://www.threads.com/@vavozamarketing/post/DZYAbmomEI7/ [consultée] · https://sidsaladi.substack.com/p/ai-cover-letter-writer-101-a-claude [consultée] · https://charliehills.substack.com/p/ai-slop [consultée] · https://www.ignorance.ai/p/the-field-guide-to-ai-slop [consultée] · https://medium.com/@porter.nicholas/anthropic-skills-marketplace-the-anti-ai-slop-ui-design-skill-a572d0cfef4f [consultée] · https://note.com/humble_bobcat51/n/n185741f3337f [consultée] · https://stackedo.com/ai-writing-cliches-to-avoid/ [consultée] · https://1up.ai/blog/ai-slop-guidelines [consultée] · https://neuraplus-ai.github.io/blog/how-to-use-anthropic-claude-for-blogging.html [consultée] · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents [consultée] · https://levelupwithai.substack.com/p/i-trained-claude-code-how-to-write [consultée] · https://www.notebookcheck.net/Anthropic-allows-Claude-AI-users-to-customize-writing-styles.924555.0.html [consultée] · https://www.aibase.com/news/13500 [consultée] · https://medium.com/ai-disruption/the-rise-of-personalized-ai-77cbcfac1d53 [consultée] · https://www.newsbytesapp.com/news/science/anthropic-unveils-custom-writing-styles-for-ai-assistant-claude/story [consultée] · https://dataconomy.com/2024/11/27/claude-ai-can-now-mirror-your-writing-style-perfectly/ [consultée] · https://www.maginative.com/article/anthropic-introduces-custom-writing-styles-for-claude-ai/ [consultée] · https://alitu.com/creator/content-creation/ai-writing-claude-styles/ [consultée] · https://gcmori.medium.com/inside-claudes-new-writing-engine-fca527e9e288 [consultée] · https://dev.to/dr_hernani_costa/claude-ai-models-2025-opus-vs-sonnet-vs-haiku-guide-24mn [consultée] · https://aigoestocollege.substack.com/p/claude-35-sonnet-is-really-good [consultée] · https://thezvi.substack.com/p/claude-4-you-the-quest-for-mundane-utility [consultée]

### Agent 2 — Pollution de contexte — 38 sources
https://github.com/Piebald-AI/claude-code-system-prompts [citée] · https://www.claudecodecamp.com/p/inside-claude-code-s-system-prompt [consultée] · https://code.claude.com/docs/en/overview [consultée] · https://platform.claude.com/docs/en/release-notes/system-prompts [consultée] · https://claude.com/blog/using-claude-md-files [citée] · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents [citée] · https://surendranb.com/articles/system-prompts-vs-user-prompts/ [consultée] · https://www.prompthub.us/blog/the-difference-between-system-messages-and-user-messages-in-prompt-engineering [consultée] · https://arxiv.org/abs/2404.13208 [citée] · https://openai.com/index/instruction-hierarchy-challenge/ [consultée] · https://cdn.openai.com/pdf/14e541fa-7e48-4d79-9cbf-61c3cde3e263/ih-challenge-paper.pdf [consultée] · https://model-spec.openai.com/2025-09-12.html [consultée] · https://medium.com/@kittikawin_ball/lost-in-the-middle-why-your-ai-forgets-everything-you-told-it-8eaabe8c6f6b [citée] · https://qubittool.com/blog/long-context-lost-in-the-middle [citée] · https://dev.to/letanure/claude-code-part-10-common-issues-and-quick-fixes-186g [consultée] · https://raythanni.substack.com/p/claude-code-memory-files-global-vs [consultée] · https://willfrancis.com/how-to-stop-claude-writing-like-an-ai/ [consultée] · https://www.the-ai-corner.com/p/ai-content-creation-claude-chatgpt-guide [consultée] · https://adamholter.substack.com/p/context-pollution [citée] · https://www.unite.ai/why-large-language-models-skip-instructions-and-how-to-address-the-issue/ [citée] · https://arxiv.org/abs/2605.01771 [citée] · https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html [citée] · https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices [citée] · https://github.com/anthropics/claude-code/issues/45704 [consultée] · https://www.anthropic.com/engineering/april-23-postmortem [citée] · https://www.infoq.com/news/2026/05/anthropic-claude-code-postmortem/ [citée] · https://www.makeuseof.com/anthropic-made-claude-worse-month-how-got-caught/ [consultée] · https://the-decoder.com/anthropic-says-it-cut-80-percent-of-claude-codes-system-prompt-because-fable-5-models-want-a-smaller-system-prompt/ [citée] · https://www.claudeainews.com/news/anthropic-cuts-claude-code-system-prompt-80-percent [citée] · https://forum.gnoppix.org/t/anthropic-says-it-cut-80-percent-of-claude-codes-system-prompt-because-fable-5-models-want-a-smaller-system-prompt/6671 [consultée] · https://news.hada.io/topic?id=28077 [consultée] · https://www.mindstudio.ai/blog/how-to-prompt-claude-fable-5-six-rules-anthropic [consultée] · https://www.emergentmind.com/topics/context-degradation-in-large-language-models [citée] · https://brimlabs.ai/blog/llm-personas-how-system-prompts-influence-style-tone-and-intent/ [citée] · https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e [consultée] · https://jamout.ai/blog/how-to-set-up-custom-instructions-in-claude-the-right-way-7-tips-that-make-your-ai-actually-sound-like-you-not-a-robot [citée] · https://clubjam.substack.com/p/how-to-set-up-custom-instructions [citée] · https://arxiv.org/html/2604.09443v2 [consultée] · https://arxiv.org/html/2606.07808v1 [consultée] · https://arxiv.org/pdf/2603.13351 [consultée]

### Agent 3 — Claude vs ChatGPT/Gemini — 53 sources
https://aitextdetector.ai/chatgpt-vs-claude-vs-gemini-detection/ [citée] · https://gptzero.me/ [consultée] · https://sapling.ai/ai-content-detector [consultée] · https://www.grammarly.com/ai-detector [consultée] · https://decopy.ai/ai-detector/ [consultée] · https://quillbot.com/ai-content-detector [consultée] · https://notegpt.io/ai-detector [consultée] · https://humanizerai.com/ai-detector [consultée] · https://dechecker.ai/ [consultée] · https://texttohuman.com/ai-detector [consultée] · https://reapply.app/blog/claude-vs-chatgpt-cover-letters [citée] · https://3box.ai/blog/claude-ai-cover-letters-vs-chatgpt [citée] · https://www.digitbin.com/chatgpt-vs-claude-writing/ [consultée] · https://www.mindstudio.ai/blog/chatgpt-vs-claude-2026-comparison [citée] · https://www.solutionhow.com/en-us/technology/claude-ai-vs-chatgpt-for-content-writing/ [consultée] · https://sageastraorion.medium.com/claude-vs-gemini-vs-chatgpt-for-writing-whats-actually-different-in-2026-611aad709c60 [consultée] · https://www.concretecms.com/about/blog/ai/chatgpt-vs-claude [consultée] · https://vife.ai/blog/claude-ai-vs-chatgpt-guide-writers-developers [consultée] · https://www.eyesift.com/blog/claude-vs-chatgpt-for-writing/ [consultée] · https://www.prompthq.run/learn/claude-vs-chatgpt-for-writing [citée] · https://www.tomsguide.com/ai/claude-4-sonnet-vs-chatgpt-4-5-for-creative-writing-one-blew-me-away [citée] · https://phrasly.ai/blog/is-gptzero-accurate-in-ai-detection-what-you-need-to-know/ [consultée] · https://fast.io/resources/gptzero-ai-detector-review-2026/ [consultée] · https://walterwrites.ai/gptzero-review/ [consultée] · https://gptzero.me/news/gpt5/ [consultée] · https://undetectable.ai/blog/gptzero-accuracy-rate/ [citée] · https://arxiv.org/pdf/2307.04251 [consultée] · https://arxiv.org/pdf/2606.04906 [citée] · https://arxiv.org/pdf/2606.21844 [consultée] · https://coverlettercopilot.ai/blog/are-ai-cover-letters-detectable-by-recruiters [citée] · https://coverlettercopilot.ai/blog/recruiters-human-vs-ai-cover-letters [consultée] · https://turboresume.ai/en/blog/cover-letter-guide-2026/ [consultée] · https://topresume.com/career-advice/ai-in-hiring-survey [citée] · https://aiapply.co/blog/can-employers-tell-if-you-use-ai-for-a-cover-letter [consultée] · https://www.liftmycv.com/blog/using-ai-for-cover-letter/ [consultée] · https://www.uschamber.com/co/run/human-resources/hiring-ai-job-applications [consultée] · https://hub.paper-checker.com/blog/ai-detection-job-applications-recruiters/ [consultée] · https://huntr.co/blog/chatgpt-vs-claude-vs-gemini-best-resume [citée] · https://www.reztune.com/blog/ai-solutions-compared/ [consultée] · https://3box.ai/blog/chatgpt-vs-claude-vs-gemini-resume-2026 [consultée] · https://skillupgradehub.com/chatgpt-vs-claude-vs-gemini-resume-2026/ [consultée] · https://tailorforge.com/blog/ai-resume-tools-compared [consultée] · https://www.resumewriting.net/ai-resume-rewriting-chatgpt-claude-gemini/ [consultée] · https://www.resumebuilder.com/82-of-hiring-managers-unable-to-identify-cover-letters-written-by-chatgpt/ [citée] · https://www.prweb.com/releases/resumebuilder-com-survey-finds-46-percent-of-job-seekers-use-chatgpt-to-write-their-resumes-and-or-cover-letters-849205898.html [consultée] · https://www.lesswrong.com/posts/ezfHZtu85yXi2d9Qa/constitutional-ai-vs-rlhf-vs-deliberative-alignment [citée] · https://www.datacamp.com/blog/anthropic-vs-openai [citée] · https://learn-prompting.fr/en/blog/rlhf-constitutional-ai-guide [consultée] · https://tdwi.org/blogs/ai-101/2026/05/constitutional-ai.aspx [consultée] · https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Anthropic/Claude%20Code/Prompt.txt [citée] · https://tactiq.io/learn/claude-system-prompt [consultée] · https://www.prompthub.us/blog/an-analysis-of-the-claude-4-system-prompt [consultée] · https://techcrunch.com/2024/08/26/anthropic-publishes-the-system-prompt-that-makes-claude-tick [consultée] · https://andrewpwheeler.com/2026/03/20/using-claude-code-to-help-me-write/ [citée] · https://hyperdev.matsuoka.com/p/why-i-switched-to-claude-code-for [consultée] · https://docs.bswen.com/blog/2026-02-23-claude-creative-writing-pros-cons/ [consultée]

### Agent 4 — Techniques anti-"IA slop" — 62 sources
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices [citée] · https://www.ignorance.ai/p/the-field-guide-to-ai-slop [citée] · https://github.com/hardikpandya/stop-slop [citée] · https://cbriansmith.substack.com/p/leash-the-robot-and-keep-your-emails [citée] · https://ruben.substack.com/p/delve [citée] · https://www.oneusefulthing.org/p/working-with-ai-two-paths-to-prompting [citée] · https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features [citée] · https://dubasque.org/les-mots-qui-trahissent-lintelligence-artificielle-ia-generative-plaidoyer-pour-une-vigilance-lexicale/ [citée] · https://rewordify.pro/blog/humaniser-lettre-de-motivation [citée] · https://scale.jobs/blog/write-cover-letter-using-ai-without-sounding-like-bot [citée] · https://www.forbes.com/sites/gracefoster/2025/10/31/using-ai-to-write-a-cover-letter-make-sure-it-sounds-like-you/ [consultée-403] · https://linkedin.com/posts/emollick_linkedin-should-let-us-all-mute-the-following-activity [citée] · https://arxiv.org/html/2509.14543v1 [citée] · https://yes-we-prompt.fr/megaprompts-ia/lettre-motivation-chatgpt/ [consultée] · https://vocacia.com/fr/blog/chatgpt-lettre-de-motivation/ [citée] · https://www.letudiant.fr/jobsstages/lettres-de-motivation_1/comment-faire-un-prompt-pour-ecrire-une-lettre-de-motivation-avec-lia.html [consultée] · https://www.onlinecv.fr/lettre-de-motivation-avec-chatgpt-ia/ [consultée] · https://intelligence-artificielle.com/prompt-lettre-motivation/ [consultée] · https://trajectio.fr/chat-gpt-lettre-motivation [consultée] · https://www.lebigdata.fr/prompt-chatgpt-lettre-de-motivation [consultée] · https://powermycv.fr/chatgpt-ia-lettre-de-motivation/ [consultée] · https://medium.com/@jobari/how-to-use-chatgpt-to-write-a-cover-letter-that-does-not-sound-like-ai-b618cc4e33f1 [citée] · https://jobwizard.ai/blog/how-to-make-a-cover-letter-not-sound-like-ai [consultée] · https://applybolt.io/blog/ai-cover-letter-generator-guide [consultée] · https://www.liftmycv.com/blog/humanizeai-cover-letter/ [consultée] · https://seekario.ai/bpost/how-to-use-ai-to-write-a-cover-letter-without-sounding-generic [consultée] · https://www.extern.com/post/chatgpt-cover-letter [citée] · https://resumegenius.com/blog/cover-letter-help/chatgpt-cover-letter [citée] · https://www.atsresumeai.com/blog/chatgpt-cover-letter [consultée] · https://findskill.ai/blog/chatgpt-cover-letter-one-prompt/ [consultée] · https://www.jobscan.co/blog/use-chatgpt-to-generate-a-cover-letter/ [citée] · https://walterwrites.ai/most-common-chatgpt-words-to-avoid/ [citée] · https://yoursaislopboresme.com/ai-cliche-phrases [citée] · https://yoursaislopboresme.com/chatgpt-overused-words [consultée] · https://hastewire.com/blog/avoid-overused-chatgpt-phrases-make-ai-writing-human [consultée] · https://alstonantony.com/chatgpt-overused/ [consultée] · https://medium.com/practice-in-public/7-common-chatgpt-phrases-and-why-you-must-avoid-them-5420e60cda9d [consultée] · https://plusai.com/blog/the-most-overused-chatgpt-words/ [citée] · https://medium.com/learning-data/words-and-phrases-that-make-it-obvious-you-used-chatgpt-2ba374033ac6 [consultée] · https://gadlet.com/posts/negative-prompting/ [citée] · https://empromptu.ai/blog/prompting-techniques-exhaust-categories-positive-wording [citée] · https://www.linkedin.com/pulse/llm-negative-prompts-avoid-unintended-consequences-chris-clark-fdvwe [consultée] · https://www.walturn.com/insights/mastering-prompt-engineering-for-claude [consultée] · https://blog.logrocket.com/stop-one-shot-prompt-claude-better/ [consultée] · https://www.mindstudio.ai/blog/iterative-refinement-loop-claude-design-multimodal [consultée] · https://www.aiapps.com/blog/ghostwriting-secret-make-claude-sound-like-human/ [citée] · https://artificialcorner.com/p/voice [citée] · https://medium.com/@A.Rehman_GhostWriter/the-claude-prompt-i-use-to-make-every-blog-post-sound-human-859f413065dd [consultée] · https://aiblewmymind.substack.com/p/claude-skills-ai-write-like-you [citée] · https://www.mediabistro.com/be-inspired/productivity/ai-prompting-writers/ [consultée] · https://clskillshub.com/blog/ghost-claude-prompt [consultée] · https://ranthebuilder.cloud/blog/how-i-use-claude-cowork-to-write-with-ai-in-my-voice/ [consultée] · https://www.donbarger.com/p/give-claude-your-voice-the-three [citée] · https://www.tomsguide.com/ai/claude-lets-you-personalize-your-ai-writing-heres-how [citée] · https://www.croma.com/unboxed/claude-ai-can-now-adapt-to-your-unique-writing-style [citée] · https://www.guideflow.com/tutorial/how-to-create-a-custom-style-in-claudeai [consultée] · https://www.ai-toolbox.co/claude-management-and-productivity/how-to-set-up-claude-custom-instructions-2026 [consultée] · https://runtheprompts.com/resources/claude-info/claude-custom-writing-style-tool/ [consultée] · https://blog.jmatthews.uk/developing-a-writing-style-with-claude [consultée] · https://lucijatomsic.substack.com/p/how-to-train-claude-to-write-like [consultée] · https://godofprompt.ai/blog/train-claude-to-understand-writing-style/ [consultée] · https://www.mywritingtwin.com/blog/how-to-make-claude-sound-like-you [consultée] · https://learnprompting.org/docs/reliability/calibration [consultée] · https://latitude-blog.ghost.io/blog/how-examples-improve-llm-style-consistency/ [citée] · https://www.prompthub.us/blog/the-few-shot-prompting-guide [citée] · https://pub.towardsai.net/how-to-make-llms-write-stylishly-6691be12b970 [consultée] · https://github.com/anthropics/claude-cookbooks [consultée] · https://claude.com/blog/best-practices-for-prompt-engineering [consultée]
