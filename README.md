# claude-os

Repo « DNA » de Guillaume Pignolet : la doctrine versionnée qui définit comment Claude doit se
comporter avec lui, sur toutes les surfaces (Claude Code local et cloud, Claude Chat/claude.ai,
Asana). Ce n'est **pas** du code applicatif — c'est de la configuration-as-doctrine, pointée
(jamais copiée) par les autres repos projet de Guillaume.

- **`CLAUDE-DNA-CC-CORE.md`** — règles actives, injectées à chaque session Claude Code.
- **`CLAUDE-DNA-CC-REF.md`** — procédures rares, chargées à la demande.
- **`CLAUDE-DNA-CHAT.md`** — variante autonome pour claude.ai.
- **`CLAUDE-DNA-ASANA.md`** — workflow Guillaume + Claude + Asana.
- **`.claude/skills/`** — skills implémentant les triggers `g*` du DNA (`gauto`, `gaudit`,
  `gpose`, `gprompt`, `grech`, `gtri`, `asana-pass`).

Détails complets : [`CLAUDE.md`](CLAUDE.md).
