# {hub_name} — Auto-memory

*Layer 3 staging ground for this hub. Claude Code writes here automatically during sessions as it learns new preferences, corrections, and observations.*

*This file lives at `~/.claude/projects/{hub-path}/memory/MEMORY.md` — not inside the hub directory itself. The hub-os skeleton provides this template as a reference for what the file should look like when Claude Code first scaffolds it. You may not need to create this file manually; Claude Code often creates it on first session.*

---

## What belongs here

- **Fresh feedback** the user has given Claude this hub that hasn't been promoted yet
- **Hub-specific observations** pending migration to `~/thehub/vault/wiki/` (Layer 4) via Path B promotion
- **Cross-hub preferences** pending promotion to `~/thehub/USER.md` (Layer 3 user-scoped anchor) via Path A promotion
- **Short-term reference pointers** relevant to this hub

## What does NOT belong here (canonicality checks per R-008)

- **Session rituals** → hub's Layer 1 CLAUDE.md `Session Rituals` section (Layer 8 canonical home). Rituals do NOT belong in auto-memory.
- **Current operational state** → hub's `OVERVIEW.md` (Layer 2). State with countdowns or deadlines decays silently here.
- **Hub-scoped project details** → `~/thehub/vault/wiki/projects/` or `clients/` (Layer 4). A project state snapshot here becomes a historical artifact that reads as current.
- **Stable user-scoped preferences** → once a preference has proven cross-hub stable, promote to `~/thehub/USER.md` via Path A. Then remove from here.

## The staging-area principle

This file is a **staging ground**, not a final destination. Its contents flow outward via promotion (FRAMEWORK.md Section 8):

- Cross-hub user preferences → promoted up to `~/thehub/USER.md`
- Hub-scoped domain knowledge → promoted across to `~/thehub/vault/wiki/`
- Ephemeral session state → deleted

Without this discipline, `memory/` becomes an unstructured dumping ground that mixes scopes and poisons hub #2's inheritance. R-008 violation was how hub-os found its first bug in its own source material.

---

## User

- See `~/thehub/USER.md` for canonical user profile

## Feedback

*Claude populates here as the user teaches new preferences or corrects past behavior. Each entry is a short rule + a reason. Stable entries get promoted to `~/thehub/USER.md` cross-hub preferences section.*

_(empty on day one; populates as sessions accumulate)_

## Hub-specific observations

*Short-term observations about this specific hub pending promotion to `~/thehub/vault/wiki/`.*

_(empty on day one; populates as observations emerge)_

## Reference

*Pointers to external resources relevant to this hub.*

_(empty on day one; populates as tools and external systems are used)_
