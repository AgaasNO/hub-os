# hub-os — Framework for Cognitive-Operational Hubs

*Version 0.2.4 — snapshot extracted from chiefofstaff hub 2026-04-13, reviewed and patched 2026-04-14*

---

## Table of Contents

1. Preamble
2. Core Concepts
3. Architecture
   - 3.1 The 8 layers
   - 3.2 The canonicality decision table
   - 3.3 Visual
   - 3.4 Minimum vs. expansion
   - 3.5 Growth triggers
4. Layer Reference
   - 4.1 Coordinator
   - 4.2 State
   - 4.3 Auto-memory
   - 4.4 Metacognition (Vault)
   - 4.5 Ops (Delegation)
   - 4.6 Safety (Enforcement)
   - 4.7 Integration
   - 4.8 Cadence (Rituals)
5. The User-Scoped Layer — `USER.md`
6. Instantiation Playbook
7. The Reflex Card
8. Promotion Rules
9. Canonicality Rules *(see Section 3.2)*
10. Anti-patterns *(see per-layer sections in Section 4)*
11. Evolution Log

---

## 1. Preamble

### The core analogy

A hub is an organism, not an assembly.

Nobody understands the economy. Not because supply chains or monetary policy or labor markets are individually incomprehensible — each part can be studied in isolation by someone smart enough. The economy is incomprehensible because it is *living*: its behavior emerges from how the parts interact, and emergence is too much for one head. You can understand every organ in isolation and still not be able to predict the organism, because the organism isn't the sum of its organs — it's the *pattern of their interaction*.

A sufficiently ambitious domain of operational work behaves the same way. Any one client can be held in your head. Any one venture, any one project. But the moment you're running six of each across four ventures with shifting priorities, compounding decisions, and threads that cross-reference, the system outgrows any single head. What's missing isn't intelligence — it's a place for the whole thing to live. A hub is that place.

hub-os is a skeleton for building these organisms.

### What hub-os is

hub-os defines **8 layers** (you can think of them as *organs*) that every hub exercises, a **minimum implementation** for each layer, and a set of **interaction rules** that govern how layers exchange information. None of the layers are optional — they are faculties every hub has, at some depth. A day-one hub exercises them at minimum depth. A mature hub exercises them at substantive depth. Both are legitimate hubs; neither is missing an organ.

The distilled content of hub-os is the structure of `chiefofstaff`, stripped of its ecommerce specifics. What remains is universal: the layers, the slots inside them, the rules for filling the slots, the rituals that keep the layers coherent over time, and the reflexes accumulated from real incidents other hubs have already survived.

The core premise is simple: **Claude without a hub is a bot. Claude with a hub is a system.** A bot answers the current message. A hub holds the world, remembers why decisions were made, enforces its own reflexes, and gets smarter per session rather than resetting. The gap is not a prompt — it's a layered structure. hub-os is that structure, written down.

### What hub-os is not

- **Not a generator.** There is no command that says "make me thehub for webdesign" and produces a working hub. The domain interview — *what archetype fits? what roles exist? what credentialed surfaces need safety?* — happens in a live session. hub-os provides the skeleton; it does not replace the thinking.
- **Not a replacement for Claude Code.** It sits on top as a pattern. Every file is plain markdown or YAML; no new runtime, no magic.
- **Not complete.** This is a snapshot of what `chiefofstaff` had learned by 2026-04-13. Reflexes that prove universal get promoted in; patterns that fail get removed. Section 11 tracks changes.
- **Not opinionated about the domain.** hub-os is opinionated about *structure* — how information flows, where rationales live, how delegation works, how safety gets enforced — and agnostic about *content*. It works for ecommerce consulting, web design, research, writing, bookkeeping, or anything else where one operator needs to hold a big picture.

### Who it's for

- **Primary:** a single operator running multiple complex domains who wants Claude to hold the full picture across all of them, without re-teaching the working style every time a new hub is built.
- **Secondary:** someone willing to pay the upfront cost of codifying their working style once (`USER.md`) in exchange for every future hub inheriting it automatically.
- **Less suitable:** single-use bots, one-shot task runners, teams with multiple primary users (hub-os assumes one), or ephemeral projects where accumulation is waste.

### The insight driving the user/hub split

Every hub-os user will eventually build more than one hub. Without a framework, hub #2 starts from zero — no working style, no feedback history, no accumulated design preferences, none of the hard-won rules about how to push back. The second hub ends up being the first hub again, minus the scar tissue.

hub-os fixes this by drawing a hard line between **what belongs to the hub** and **what belongs to the user across all their hubs**. The user-scoped layer (`USER.md` + auto-memory) is inherited by every new hub automatically. The hub-scoped layers are built fresh per domain. The operator pays the teaching cost once and every future hub starts smart.

### A note on `USER.md` location

`USER.md` is provisionally located at `~/thehub/USER.md`, sibling to every hub directory. This location is flagged for reflection before first instantiation. Three angles to think through:

- **thehub namespace vs. user namespace.** `~/thehub/` is the umbrella directory for current work. If a hub ever gets built outside that umbrella, a `USER.md` trapped under `~/thehub/` doesn't serve it. Alternatives: `~/.claude/USER.md` (alongside auto-memory) or `~/USER.md` (pure user scope).
- **Single file vs split.** One `USER.md` or a `user/` directory with section-per-file? Single file is simpler until it grows past ~2000 words; split is cleaner after.
- **Relationship to Claude Code auto-memory.** Claude Code's existing `~/.claude/projects/{project-path}/memory/` is per-project-path. `USER.md` is the layer that escapes this per-project trap. Whether `USER.md` lives *next to* auto-memory or *above* it is an unresolved convention question.

Recommendation for the first real instantiation: start with `~/thehub/USER.md`. The cost of relocating later is a one-line change per hub.

---

## 2. Core Concepts

These are the terms the rest of the document assumes. Read this section before any other.

### Hub

A Claude Code project directory that holds the full operational picture of one domain of work. Every hub exercises all 8 layers at some depth. A hub is not just a folder with a CLAUDE.md — it is a *layered organism* where each layer carries a specific kind of information and a clear rule about what goes where.

### Coordinator

The top-level agent in a hub. Holds the big picture, makes decisions, delegates specialist work, and is **forbidden from doing specialist work directly**. The coordinator's job is coordination — the moment it starts executing, it loses the altitude it needs to see the whole board.

Every coordinator has:

- An **archetype** — a named historical or fictional figure whose reflexes fit the domain's failure modes
- A **mandate** — what the coordinator is responsible for and what it refuses to do
- A **routing table** — explicit task → specialist mapping (can start empty)
- A **never list** — hard lines the coordinator refuses to cross (starts seeded from the reflex card)
- A **working style section** — imported from `USER.md`

The coordinator's personality is load-bearing, not decoration. Wrong archetype = wrong reflexes at every decision point = hub feels permanently off.

### Layer (organ)

A faculty every hub exercises, implemented as a set of files with a common purpose. There are 8 layers total. No layer is optional — but each has a defined **minimum implementation** and an **expansion path**. Some minimums are substantive (Layer 1 coordinator, Layer 2 state). Some are near-empty stubs (Layer 5 ops with no roles yet, Layer 7 integration with no tools yet).

Layers are *orthogonal* — no layer can be implemented inside another. If two layers start overlapping, one of them is wrong. Section 3.2's canonicality rules keep them separated.

### Slot

A placeholder inside a layer that gets filled per-hub or per-domain. `{archetype}`, `{mandate}`, `{ops_roster}`, `{never_list}`, `{credentialed_surfaces}` — these are all slots. A framework is a collection of slots plus rules for filling them. hub-os is exactly that.

### Scope

Every piece of information in a hub has a scope: either **hub-scoped** (lives in one hub) or **user-scoped** (shared across every hub the same user owns). Scope determines file location. Getting scope wrong is the main reason hub #2 ends up being hub #1 minus the wisdom. Rule of thumb: *"Will this still be true in a hub I build three years from now for a totally different domain?"* If yes, user-scoped.

### Promotion

The upward flow of learnings. Two paths:

- **Hub → framework.** When a reflex that started in one hub proves universal, it gets promoted into this framework doc (Layer 6 never-list seeds, Section 7 reflex card).
- **Hub → USER.md.** When a working-style lesson from one hub applies to every hub the same user will ever build, it gets promoted into `USER.md`.

Promotion is the mechanism that keeps the framework living. Without it, the framework freezes and real wisdom stays trapped in individual hubs.

### Reflex

A rule that exists because something broke. Every reflex has: incident, rule, why, date. Reflexes are the scar tissue that makes a hub robust. Section 7 is the reflex card — scar tissue available to every new hub so day-one hubs don't have to re-earn every lesson.

### Canonicality

The rule that every piece of information has exactly **one authoritative location**. No piece is stored in two layers. If a decision is in the vault, it is not also in OVERVIEW.md. If a rule is in CLAUDE.md, it is not also duplicated in the reflex card.

Canonicality is what keeps the layer graph honest. Without it, information duplicates, duplicates drift, and the hub starts lying to itself. Section 3.2 is the canonicality decision table.

---

## 3. Architecture

### 3.1 The 8 layers

Every hub exercises 8 layers. They are not modules you add or skip — they are faculties every hub has, implemented at some depth.

| # | Layer | Scope | One-line purpose |
|---|---|---|---|
| 1 | **Coordinator** | hub | The thinking layer — archetype, mandate, routing, never list |
| 2 | **State** | hub | What is currently true — OVERVIEW.md, kanban |
| 3 | **Auto-memory** | user | Cross-session preferences and user profile — USER.md, memory/ |
| 4 | **Metacognition (vault)** | hub | Why decisions were made, what was learned — vault/wiki/ |
| 5 | **Ops (delegation)** | hub | Named specialists and the routing that enforces them — ops/ |
| 6 | **Safety (enforcement)** | hub | Hard rules the coordinator can't violate — never list, hooks, cred split |
| 7 | **Integration** | hub | External tools and their contracts — MCP, APIs, per-tool notes |
| 8 | **Cadence (rituals)** | hub | Session rituals and scheduled rhythms — start/end routine, cron |

### 3.2 The canonicality decision table

Canonicality is the rule that governs how layers stay separate. It is load-bearing enough to live in the architecture section, not the back of the book. Before writing anything into a hub, ask: *which layer owns this kind of information?*

| Information type | Lives in (canonical) | Never lives in |
|---|---|---|
| What is currently true, live work | Layer 2 (OVERVIEW.md, kanban/) | Layer 4 (vault), duplicated in Layer 1 CLAUDE.md |
| Why a decision was made | Layer 4 (`vault/wiki/decisions/`) | Layer 2 state, inline in CLAUDE.md |
| A reusable pattern with a name | Layer 4 (`vault/wiki/lessons/`) | CLAUDE.md, reflex card |
| An actor in the domain (person, project, client) | Layer 4 (`vault/wiki/people/`, `projects/`, `clients/`) | Layer 2 state |
| A hard rule the coordinator must follow | Layer 1 declaration (never list) + Layer 6 enforcement (hook/architecture) | Layer 4 vault |
| A cross-session user preference | Layer 3 (`USER.md` or `memory/`) | Layer 1 CLAUDE.md inlined |
| Per-role execution rules | Layer 5 (`ops/{role}/CLAUDE.md`) | Layer 1 top-level CLAUDE.md |
| Tool contracts and quirks | Layer 7 ("Tools available" in CLAUDE.md or dedicated integration notes) | Inline where the tool is used |
| Session rituals and scheduled rhythms | Layer 8 (declared in Layer 1 CLAUDE.md rituals section) | Layer 3 memory/ |
| An incident that produced a rule | Section 7 reflex card + Layer 4 vault decision | Duplicated in Layer 1 |
| Recent context cache (what just happened) | Layer 4 (`vault/wiki/hot.md`) | Layer 2 state |

The rule of thumb when unsure: **"Would I need this to DO something?"** → a fact layer (2, 5, 6, 7). **"Would I need this to UNDERSTAND something I'm about to decide?"** → Layer 4 (vault). **"Is this about me, not about the hub?"** → Layer 3 (auto-memory).

### 3.3 Visual

```
                    ┌──────────────────────────────┐
                    │      USER.md (user-scoped)   │
                    │  imported by every hub CLAUDE.md
                    └───────────────┬──────────────┘
                                    │
        ╔═══════════════════════════▼════════════════════════════╗
        ║              Layer 1: Coordinator                       ║
        ║   CLAUDE.md — archetype, mandate, routing, never list   ║
        ╚═══════╤═════════╤═════════╤══════════╤════════╤════════╝
                │         │         │          │        │
                ▼         ▼         ▼          ▼        ▼
           ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ ┌────────┐
           │   L2   │ │   L3   │ │   L4   │ │  L5   │ │   L6   │
           │ State  │ │ Memory │ │ Vault  │ │  Ops  │ │ Safety │
           └────────┘ └────────┘ └────────┘ └───────┘ └────────┘
                │                    │         │        │
                └────────┬───────────┴─────────┴────────┘
                         ▼
                   ┌─────────────┐  ┌─────────────┐
                   │     L7      │  │     L8      │
                   │ Integration │  │   Cadence   │
                   └─────────────┘  └─────────────┘

       All 8 layers are present in every hub. Depth varies.
```

### 3.4 Minimum vs. expansion

Every layer has a **minimum implementation** — what must exist on day one — and an **expansion path** — what grows as the hub matures under pressure.

| Layer | Day-one minimum | Grows toward |
|---|---|---|
| 1 Coordinator | Archetype, mandate, working-style import, never list (seeded from reflex card), empty routing table, status pointer | Rich archetype (own file), full routing table, domain map, tool catalog |
| 2 State | OVERVIEW.md with 4 canonical sections, empty `kanban/proposals/pending.yaml` | Briefs, reports, per-project state, domain-extended schemas |
| 3 Auto-memory | `USER.md` reference, `memory/MEMORY.md` index skeleton | Populated feedback, user-profile files, project memories, reference pointers |
| 4 Vault | `vault/wiki/hot.md`, `index.md`, `log.md`, empty subfolders | Populated decisions, lessons, people, projects, client briefs, timeline archives |
| 5 Ops | `ops/` folder containing `_template/CLAUDE.md`, empty routing table in Layer 1 | Populated roles with per-role CLAUDE.md, context files, cross-role signals |
| 6 Safety | Never list (non-empty, seeded from reflex card), credential separation pattern declared | Hooks, dedicated safety configs, credential split in practice |
| 7 Integration | "Tools available" section (may be empty) | Per-tool contracts, MCP wiring, endpoint quirks, documentation pointers |
| 8 Cadence | Session start/end ritual documented | Scheduled automation, daily/weekly/monthly reviews, reconciliation loops, cron |

Some minimums are substantive (Layers 1, 2, 6, 8). Some are near-empty stubs (Layer 5 with no roles, Layer 7 with no tools, Layer 4 with a skeleton). **All 8 are present on day one.** The hub grows inside its layers, not by adding new layers.

### 3.5 Growth triggers

Expansion happens under pressure, not on schedule. These are the signals that a specific layer wants to grow beyond its current depth. None are commands — they're invitations.

| Layer | When it's ready to grow |
|---|---|
| 1 Coordinator | CLAUDE.md feels thin; archetype section wants more space; never list grows past 3–4 entries |
| 2 State | Proposals start needing more than a YAML row; scheduled work starts producing outputs |
| 3 Auto-memory | Feedback and preferences start accumulating; user notices they've taught the same thing twice |
| 4 Vault | A decision's rationale matters but has nowhere to live; a pattern emerges that deserves a name |
| 5 Ops | The coordinator is doing specialist work it shouldn't; the CLAUDE.md grows domain-specific execution rules |
| 6 Safety | A new mutation-capable tool enters; an incident happens; the never list grows from inherited reflexes |
| 7 Integration | A new external tool gets used regularly; tool quirks worth documenting accumulate |
| 8 Cadence | Informal rituals emerge and want to be codified; scheduled automation becomes useful |

When a trigger fires, grow that layer. When it doesn't, leave it at its current depth. A hub that tries to grow every layer at once collapses under the bureaucracy.

---

## 4. Layer Reference

Each layer section follows the same sub-structure: **Purpose / Files / Slots / Minimum / Expansion / Example from chiefofstaff / Anti-patterns**. Read sections for layers you're implementing; skim the rest.

---

### 4.1 Coordinator *[hub-scoped]*

#### Purpose

The coordinator holds the big picture and makes decisions. It delegates specialist work and refuses to execute it directly. Its job is to keep the altitude the hub needs to see the whole board.

If the coordinator starts executing, it loses altitude. Altitude is the thing specialists cannot provide for themselves — they are each inside their own domain. Only the coordinator sees across. Protect that by keeping execution out.

The coordinator is the hub's thinking layer: state is what's true, vault is why, ops is who does it, coordinator is *what to do next* — the decision layer on top of all the others.

#### Files

- **`CLAUDE.md`** at hub root. The coordinator's complete operating spec. Required sections in order:
  - **Identity** — archetype, character, how it applies to this hub
  - **Working style** — imported from `USER.md`, or inlined if `USER.md` doesn't exist yet
  - **Session rituals** — session start + session end routines declared inline (see Section 4.8 for canonical content). Placed high so the coordinator reads it before any domain content; rituals are foundational and need to be in the first screenful.
  - **Mandate** — 1–3 sentences on what the coordinator is responsible for
  - **Domain map** — what work this hub coordinates
  - **Routing table** — task → specialist mapping (can be empty)
  - **Never list** — hard lines the coordinator refuses to cross (seeded from Section 7 reflex card)
  - **Current status** — pointer to `OVERVIEW.md`, not duplicated
  - **Tools available** — per-tool contracts or pointer to Layer 7

- **`ARCHETYPE.md`** *(appears during expansion)*. If the archetype section in CLAUDE.md grows past ~500 words, split to its own file.

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{archetype}` | A named real or fictional figure whose reflexes fit the domain | Charlie Munger |
| `{mandate}` | 1–3 sentence statement of coordinator's job | "Hold the full picture of everything Gabriel is building so he doesn't have to hold it all in his head" |
| `{domain}` | What kind of work the hub coordinates | E-commerce consulting + ventures |
| `{primary_user}` | Who the coordinator reports to | Gabriel (one user, one hub) |
| `{routing_table}` | Task → specialist mapping | 6 roles in `../ops/` |
| `{never_list}` | Hard lines coordinator refuses | "No direct Shopify writes. No subagent credential passing." |

#### Archetype selection — the hard slot

This is the slot that most affects hub quality. A wrong archetype produces wrong reflexes at every decision point and the hub feels permanently off. Rules:

1. **Pick a real, named figure.** Historical, cultural, fictional — but concrete. "A senior engineer" doesn't have reflexes. Munger does. Rams does. Feynman does. Jane Jacobs does. Vignelli does. Carse does. Specificity is the whole point.

2. **Pick for reflexes, not aesthetics.** What does the domain punish? What does it reward? The archetype's native reflexes should match. Ecommerce consulting punishes impulse and rewards patience — Munger's reflexes are exactly patience and skepticism. Design punishes decoration and rewards restraint — Rams's reflex is "less, but better." Don't pick an archetype because you admire them; pick one whose instincts cover the domain's failure modes.

3. **Pick someone with character contrast to the user — someone the user respects but would disagree with sometimes.** The archetype is a counterweight, not a mirror. A high-drive user with a high-drive archetype amplifies impulse and the hub becomes noise. A high-drive user with a patient archetype introduces friction in exactly the right place. A yes-man archetype is useless; the archetype has to be credible enough for its pushback to land and distinct enough for the pushback to be real. Use the user profile (`USER.md`) to find contrast points.

4. **Write the fit.** 1–2 paragraphs in CLAUDE.md explaining *why this archetype for this domain*. Future Claude sessions need to know, and future promotion checks need something to compare against.

#### Minimum (day one)

```
CLAUDE.md
├── Identity (archetype + 1 paragraph fit)
├── Working style (import from USER.md)
├── Session rituals (start + end, per Section 4.8)
├── Mandate (1-3 sentences)
├── Domain map (bulleted)
├── Routing table (empty table with column headers)
├── Never list (seeded from reflex card — minimum 2-3 entries)
├── Current status → pointer to OVERVIEW.md
└── Tools available → empty or minimal
```

Notice that **the never list is non-empty on day one**. It is seeded from Section 7 (reflex card). A new hub inherits at least the incidents other hubs have already survived, so day-one Layer 6 is non-trivial.

#### Expansion

- **Populate the routing table** when specialists get added (Layer 5 grows)
- **Extend the never list** when incidents happen or new mutation-capable tools enter
- **Split ARCHETYPE.md** when the archetype section crosses ~500 words
- **Enrich the domain map** as the hub coordinates more work

#### Example (chiefofstaff)

- **Archetype:** Charlie Munger — patient, multidisciplinary, blunt, allergic to foolishness. Fit: the domain punishes impulse and rewards patient capital allocation. Gabriel is high-drive low-orderliness; Munger's patience is the counterweight.
- **Mandate:** one sentence. Holds the full picture so Gabriel doesn't have to.
- **Routing table:** 6 ops roles with task → role mapping, each row including what the coordinator must never do directly.
- **Never list:** no direct Shopify writes, no subagent credential passing, no bypass of named roles. All three seeded from the 2026-03-27 incident.

#### Anti-patterns

- **Coordinator as executor.** The coordinator starts doing specialist work. Recognize when CLAUDE.md grows long execution rules or session logs show domain-API calls instead of delegations. Fix: promote execution to a specialist, strip it from the coordinator.
- **Generic archetype.** "A thoughtful advisor." "A senior engineer." These produce generic reflexes, which are no reflexes at all. Fix: pick a real named figure with documented character.
- **Aesthetic archetype.** Picked because the user likes the person, not because reflexes fit. Fix: pick for reflex fit; verify by asking *what does this domain punish, and does the archetype flinch from it?*
- **Mirror archetype.** Agrees with the user on everything. Useless. Fix: pick contrast, especially on user weaknesses.
- **Empty never list.** The never list exists as a section but is empty because no incident has happened yet. This is how incidents happen. Fix: seed from the reflex card on day one.
- **Mandate creep.** The mandate grows over time and starts including every new thing. Fix: mandate changes go through deliberate revision, not drift.
- **State duplication.** "Current status" section in CLAUDE.md gets copied from OVERVIEW.md instead of pointing. Fix: pointer only, never a copy.

---

### 4.2 State *[hub-scoped]*

#### Purpose

State is **what is currently true**. It is the operational snapshot of the hub's live work — active priorities, blocked items, decisions waiting, open proposals, things at risk of being forgotten. Where the coordinator looks to remember what's on its plate.

Sharp distinction from Layer 4 (vault): **state = what is true now; vault = why it's true, or what we learned from it.** A decision rationale belongs in vault. The fact that the decision is active and waiting for action belongs in state. Mixing the two is the fastest way to rot the hub. Section 3.2's canonicality table governs this.

**State is overwrite-only.** History does not live here. If history matters, it belongs in Layer 4.

#### Files

- **`OVERVIEW.md`** at hub root. A single living document, completely overwritten as things change. Required sections:
  - **Active priorities** — what's being worked on right now, ranked
  - **Blocked / waiting on** — items held up on something external
  - **Decisions needed** — explicit decisions the user owes
  - **Things that might be falling through the cracks** — items the coordinator suspects are at risk

- **`kanban/`** directory — structured work queue. Canonical subfolders:
  - **`kanban/proposals/pending.yaml`** — open proposals awaiting decision. Minimum schema: `id`, `title`, `status`, `created_date`, `resolved_date?`, `resolved_note?`, domain extensions per hub.
  - **`kanban/briefs/`** *(appears during expansion)* — per-item context files when a proposal needs more than a YAML row
  - **`kanban/reports/`** *(appears during expansion)* — outputs from scheduled runs (once Layer 8 automation activates)

Other subfolders can be added per hub (drafts, campaigns, research threads), but the framework defines only these as canonical starters.

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{state_topology}` | What unit the kanban tracks | Proposals + briefs + reports |
| `{proposal_schema_extensions}` | Per-hub fields beyond the minimum | `client`, `venture`, `value_nok` |
| `{overview_sections}` | Optional rename of the four canonical sections | Active / Blocked / Decisions / Cracks |

#### Minimum (day one)

```
OVERVIEW.md                 # four canonical sections, may be near-empty
kanban/
└── proposals/
    └── pending.yaml        # empty array with schema reference comment
```

That's the whole minimum. Briefs and reports appear later when expansion triggers fire.

#### Expansion

- **Add `briefs/`** when a proposal grows past what fits in a YAML row
- **Add `reports/`** when Layer 8 cadence grows scheduled runs that produce outputs
- **Add custom subfolders** when the domain has a natural unit that isn't a proposal (drafts in a writing hub, campaigns in an ads hub, research threads in a research hub)
- **Extend the proposal schema** with domain-specific fields when triage needs them. Resist over-fielding.

#### Example (chiefofstaff)

- **`OVERVIEW.md`** is overwritten every session where real work happened. All four canonical sections in use.
- **`kanban/proposals/pending.yaml`** — open proposals reconciled at session end (the rule is non-negotiable in CLAUDE.md).
- **`kanban/briefs/`** — weekly briefs from scheduled cadence.
- **`kanban/reports/`** — daily health checks and failure logs from Layer 8 automation.

#### Anti-patterns

- **State drift.** `OVERVIEW.md` stops getting updated and goes stale. Coordinator operates from memory instead of file. Fix: the session-end reconciliation ritual (Layer 8) must overwrite `OVERVIEW.md` every session; the coordinator's CLAUDE.md should name it as non-negotiable.
- **History leaks into state.** Old resolved proposals pile up in `pending.yaml`. Fix: periodic deletion or archive-to-vault. Resolved items leave state.
- **State in vault.** User files current status notes in the vault because it felt reflective. Next session's coordinator reads `OVERVIEW.md` and misses half the actual state. Fix: see Section 3.2 — state goes in Layer 2, only *why* goes in Layer 4.
- **Kanban sprawl.** Every subproject grows its own folder with its own schema. Unnavigable. Fix: one canonical schema per hub, resist per-project forking, use briefs instead.
- **OVERVIEW.md as changelog.** User adds dates and diffs inline. Fix: state is overwrite-only; changelog is `vault/wiki/log.md`.
- **Duplication with CLAUDE.md.** Current status copied into CLAUDE.md instead of pointed at. Drifts instantly. Fix: pointer only.

---

### 4.3 Auto-memory *[user-scoped]*

#### Purpose

Auto-memory is where the **user** lives across all their hubs. It carries working style, decision lens, feedback history, user profile, and any rule the user has taught the system that applies *regardless of which hub it's working in*. It is the only user-scoped layer in hub-os, and it's what makes hub #2 start smart instead of naive.

Sharp distinctions:
- **Auto-memory vs Vault (Layer 4):** auto-memory is about *the user*; vault is about *the hub's domain*. If the insight would still be valid in a completely different hub, it's Layer 3. If removing the hub would make the insight meaningless, it's Layer 4.
- **Auto-memory vs Coordinator (Layer 1):** CLAUDE.md is per-hub operating spec; auto-memory is cross-hub user wisdom. Layer 1 imports from Layer 3 by reference.

Without auto-memory done right, every new hub you build starts as a naive bot on day one and has to be re-taught what you already taught the last one.

#### Files

Two sub-locations with different lifecycles:

- **`USER.md`** at the user-namespace root (provisional location: `~/thehub/USER.md`; see Section 1 preamble for the pending reflection). Human-curated durable profile. Rarely edited, never auto-written by Claude. Contains identity-stable content: how the user thinks, their profile markers, their collaboration preferences, their decision lens.

- **`memory/`** at `~/.claude/projects/{hub-path}/memory/` — Claude Code's native auto-memory, auto-created per hub, **not inside the hub directory itself**. Per-hub staging ground that Claude writes to as it learns. Contains fresh feedback, recent project-specific patterns, reference pointers — all awaiting promotion. The path uses a mangled version of the hub's absolute path as its folder name (e.g. `C--Users-Gabri-thehub-chiefofstaff`), which is how Claude Code identifies which hub a memory belongs to.

The two locations have different roles:

| | `USER.md` | `memory/` |
|---|---|---|
| Scope | User (cross-hub) | Staging ground (starts per-hub) |
| Writer | Human + Claude via promotion | Claude auto-writes during sessions |
| Lifecycle | Stable anchor; rarely changes | Accumulates then gets promoted |
| Role | Day-one inheritance for every hub | Fresh observation buffer |

Every hub's Layer 1 CLAUDE.md imports `USER.md` by reference. Day-one hubs inherit the stable wisdom. Per-hub observations accumulate fresh in each hub's `memory/` and get promoted up into `USER.md` when they prove cross-hub.

**`memory/` is a staging area, not a final destination.** Its contents flow outward to other layers via promotion (see Section 8):
- Cross-hub user preferences → promoted up to `USER.md`
- Hub-specific domain knowledge → promoted down/across to Layer 4 vault
- Ephemeral session state → deleted

This staging-area framing is critical. Without it, `memory/` becomes an unstructured dumping ground that mixes user-scoped and hub-scoped content, which violates canonicality and poisons hub #2's inheritance.

#### Slots

| Slot | What fills it | Example |
|---|---|---|
| `{user_profile}` | Who the user is operationally | "ENK consultant, 3w4, ADHD, low orderliness (6), high drive (19)" |
| `{working_style}` | How the user wants to be collaborated with | "Direct, no hedging; systems thinking; pushback expected and wanted" |
| `{decision_lens}` | Framework for weighing tradeoffs | "Boring Empire: does it compound? does it build reusable infra?" |
| `{recurring_people}` | Humans who show up across the user's life regardless of project | Family, long-term partners |
| `{cross-hub_preferences}` | Rules that apply in every hub | Don't perform caution; no emojis; design preferences |

#### Minimum (day one)

```
USER.md
├── Identity (1-3 paragraphs)
├── Working style (bulleted rules)
├── Decision lens (optional, may be empty)
├── People (optional, may be empty)
├── Cross-hub preferences (optional, may be empty)
└── Scope note

memory/
├── MEMORY.md   # index with section headers, no populated entries
└── (empty, Claude will populate as it learns)
```

`USER.md` needs at minimum the Identity and Working style sections populated, plus the scope note. The rest can accumulate. `memory/` starts with just the index skeleton.

#### Expansion

- **Promote proven preferences** from `memory/` up into `USER.md` when patterns emerge (Section 8)
- **Grow `memory/`** per-hub as feedback and domain-specific observations accumulate
- **Split `USER.md`** into multiple files if it crosses ~2000 words (one per canonical section)
- **Add domain-specific sections to `USER.md`** only if they're cross-hub (e.g., "Investment lens" applies to every hub that touches money)

#### Example (chiefofstaff → Gabriel's `USER.md`)

See Section 5.6 for a fully worked example of a populated `USER.md`.

#### Anti-patterns

- **USER.md bloat.** Hub-specific project memories get stuffed into `USER.md` because they felt important. Now `USER.md` is a single-hub journal instead of a user anchor. Fix: project memories go in Layer 4 vault.
- **Auto-memory as permanent storage.** `memory/` grows without promotion, becomes an unstructured soup of user-scoped and hub-scoped content mixed together. Fix: `memory/` is a staging area; promotion rules (Section 8) move entries out to their canonical home.
- **Teaching the same thing twice.** User re-teaches a preference in hub #2 that was already learned in hub #1 because it was left in hub #1's `memory/` instead of promoted to `USER.md`. Fix: promote proven preferences immediately.
- **Hub-specific rules in USER.md.** A rule like "don't mutate Shopify directly" ends up in `USER.md`. But a webdesign hub doesn't have Shopify. Fix: Layer 1 never list for hub-specific rules; `USER.md` only for cross-hub ones. The general principle ("never pass mutation credentials to subagents") goes in `USER.md`; the specific application ("no direct Shopify writes") goes in the hub's never list.
- **Split auto-memory.** Same rule written in both `USER.md` and `memory/`. Drifts. Fix: one canonical location.
- **USER.md written by Claude.** `USER.md` is human-curated. Claude proposes promotions but the user approves them. Fix: `memory/` is where Claude writes freely; `USER.md` changes go through explicit promotion.

---

### 4.4 Metacognition (Vault) *[hub-scoped]*

#### Purpose

The vault is where the hub **remembers why**. Not what is happening now, but what was decided, why, what was learned from it, and how everything connects. The graph of rationales, lessons, people, projects, and timeline that makes the hub able to *reflect on its own work* rather than just execute it.

The vault is what makes a hub **wise** as opposed to merely **functional**. A hub without a vault can execute but cannot explain. A hub with a vault can trace any decision back to its reasoning and any pattern back to its origin incident.

Sharp distinctions (see Section 3.2 canonicality table):
- **Vault vs State (Layer 2):** state is what's true now; vault is why it's true and what we learned. A pricing decision's *status* goes in state; its *rationale* goes in vault.
- **Vault vs Auto-memory (Layer 3):** vault is about *this hub's domain*; auto-memory is about *the user across hubs*. General design preferences go in `USER.md`; the specific decision "we picked palette X for project Y because of Z" goes in that hub's vault.
- **Vault vs Coordinator (Layer 1):** CLAUDE.md is the operating spec (how the coordinator behaves); vault is the history and rationale (what the coordinator has decided and learned).

#### Files

`vault/wiki/` with canonical subfolders (modeled on the chiefofstaff vault scaffolded 2026-04-11):

- **`hot.md`** — recent context cache, ~500 words, **complete overwrite each session-end**. What the coordinator reads first at session start to get caught up without loading the full index.
- **`index.md`** — catalog of everything in the vault. Maintained as the vault grows. Coordinator reads this when `hot.md` isn't enough.
- **`log.md`** — **append-only** session log. Newest entries at top, never edit past entries. Diachronic record of what happened across sessions.
- **`decisions/`** — per-decision markdown files. Each contains: title, date, context, options considered, choice, rationale, wikilinks to affected people/projects.
- **`lessons/`** — per-lesson markdown files. Each contains: name, what-it-is, when-safe, when-unsafe, how-to-apply. Named patterns extracted from experience.
- **`people/`** — per-person markdown files. Domain actors: clients, collaborators, counterparties, suppliers. (Contrast with Layer 3 `USER.md` People section, which lists people who recur *across all* the user's hubs.)
- **`projects/`** — per-project markdown files. Initiatives, ventures, ongoing work streams within this hub.
- **`clients/`** *(appears when the domain has clients)* — per-client agent-oriented briefs with strategy, constraints, standing rules, cross-agent notes.
- **`timeline/`** *(appears when briefs overflow)* — archived history. "Client Name — YEAR.md" files preserved verbatim, newest at top.

#### The wikilink graph — the vault's whole value

The vault's value is not the individual notes. It is the **graph they form when cross-referenced.** A decision written as a bare note is half a decision. The same decision written with links to `[[Person]]`, `[[Project]]`, `[[Lesson]]` becomes queryable from any of those nodes. A month later, when the coordinator is reading a person's page, the decision surfaces automatically because it was linked.

**Rule: every decision and lesson must wikilink every affected person and project.** Without links the graph stays flat and the vault loses most of its value. This is the single non-negotiable vault rule.

Corollary: **no orphans.** A note that nothing links to and that links to nothing is effectively invisible. At session end, check for orphans; either link them in or delete them.

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{domain_actors}` | People types that matter in the domain | Clients, suppliers, partners, family |
| `{project_types}` | What counts as a "project" in this domain | Ventures, campaigns, research threads |
| `{lesson_naming}` | How lessons are titled | "Boring Empire philosophy," "Turn-boundary hot-patch" |
| `{counterparty_folder}` | What the domain calls its clients | `clients/`, `customers/`, `collaborators/`, `subjects/` (research) |

#### Minimum (day one)

```
vault/wiki/
├── hot.md           # 1-line seed or empty
├── index.md         # skeleton with section headers, no entries
├── log.md           # empty, ready for first append
├── decisions/       # empty folder
├── lessons/         # empty folder
├── people/          # empty folder
├── projects/        # empty folder
└── clients/         # empty folder (or renamed per domain)
```

A day-one vault is just the skeleton. No decisions yet, no lessons yet. The coordinator starts filing the first entries the moment real work happens.

#### Expansion

- **Populate `decisions/`** after the first non-trivial decision
- **Populate `lessons/`** when a reusable pattern emerges and deserves a name
- **Populate `people/`** when a new domain actor enters the hub's world
- **Populate `projects/`** when an initiative crosses from "task" to "project"
- **Add `clients/`** (or its domain-specific rename) when the domain has counterparties
- **Add `timeline/`** when a client brief's cross-agent notes section overflows (~10 entries)
- **Add domain-specific subfolders** — `experiments/` for a research hub, `drafts/` for a writing hub, `campaigns/` for a marketing hub

#### Rituals (owned by Layer 8)

Vault reads and writes happen on a schedule owned by Layer 8 (Cadence). The specific ritual steps — what gets read on session start, what gets written on session end, timeline rotation, cross-agent notes promotion — are canonically declared in Section 4.8. This subsection exists only to note that the vault *participates* in rituals; the rituals themselves live in Layer 8. Duplicating them here would be an R-008 violation.

#### Obsidian syntax convention

The vault is designed around Obsidian Flavored Markdown conventions because they make the wikilink graph queryable without custom tooling. Files in `vault/wiki/` use:

- Wikilinks as `[[Note Name]]` (filenames unique, no paths)
- Embeds as `![[file]]`
- Properties as YAML frontmatter
- Callouts as `> [!type] Title`
- Tags as `#tag`

Not mandatory for hub-os to work, but strongly recommended — it lets the user open the vault in Obsidian for visual graph traversal, and it keeps the syntax consistent across every hub.

#### Example (chiefofstaff)

- **`hot.md`** — maintained every session with recent decisions, active threads, agent signals
- **`decisions/`** — every non-trivial decision as its own file with wikilinks to affected people/projects
- **`lessons/`** — "Boring Empire philosophy," "Turn-boundary hot-patch capability," "Human-frame cost estimation bias"
- **`people/`** — Alex, Robin, Sam, Casey, Devon, Quinn, Morgan, River, and others as they arrive
- **`projects/`** — Omarsson Consulting, AGAAS, Black Rabbit, STRATAVON, each active venture
- **`clients/`** — agent-oriented briefs for each paying client with strategy, constraints, cross-agent notes
- **`timeline/`** — "Hackit — 2026.md" type archives when briefs overflow

#### Anti-patterns

- **State in vault.** User files current status notes here because it felt reflective. Next session's coordinator reads OVERVIEW.md and misses half the state. Fix: state in Layer 2, vault for *why* only.
- **Vault as scratch pad.** Dumping session notes with no wikilinks. Graph stays flat. Fix: every entry links affected people/projects. No links = no entry.
- **Orphan pages.** A note exists but nothing links to it, and it links to nothing. Effectively invisible. Fix: session-end ritual checks for orphans; link them in or delete.
- **hot.md accumulating history.** User adds to `hot.md` instead of overwriting. It grows to 3000 words and stops being a hot cache. Fix: `hot.md` is overwrite-only, ~500 words, history goes in `log.md`.
- **Vault without rituals.** The vault exists but nothing is written to it because there's no enforced session-end trigger. Fix: Layer 8 session-end must name vault writes as non-negotiable when real work happened.
- **Everything is a decision.** User files every minor choice as a decision file. Decisions folder becomes noise. Fix: decisions are non-trivial; small choices don't need vault entries.
- **Lesson with no name.** User files patterns without distinctive names. They can't be referenced elsewhere. Fix: every lesson gets a memorable name so it can appear in cross-references.
- **Duplicate with auto-memory.** A hub-specific project note gets filed in both `vault/wiki/projects/` and `memory/MEMORY.md`. Fix: hub-scoped = vault; user-scoped = auto-memory. Section 3.2's canonicality table governs.
- **Duplicate with CLAUDE.md.** Coordinator's CLAUDE.md starts quoting vault content inline. Drifts. Fix: CLAUDE.md can reference vault pages by name but never duplicates their content.

---

### 4.5 Ops (Delegation) *[hub-scoped]*

#### Purpose

Ops is where **specialist work lives**. A coordinator that tries to do everything directly loses altitude; a coordinator that delegates keeps altitude while specialists keep domain depth. Layer 5 is the folder where specialists live and the routing that maps work to them.

A specialist is a **mini-coordinator for a narrower domain**. It has its own CLAUDE.md (its own archetype if warranted, its own mandate, its own rules, its own safety boundaries), its own context files, and its own credentials if it needs mutation capability. The top-level coordinator delegates to specialists via the routing table in Layer 1.

The core invariant: **the coordinator routes, the specialists execute.** A specialist doing specialist work is healthy. A coordinator doing specialist work is a Layer 5 failure.

Sharp distinctions:
- **Ops vs Coordinator (Layer 1):** Layer 1 is the thinking layer that *decides what should happen*; Layer 5 is the execution layer that *does the thing*. The routing table in Layer 1 is the bridge.
- **Ops vs Safety (Layer 6):** Layer 5 is the *structure* that makes delegation possible; Layer 6 is what *prevents the structure from being bypassed*. Without Layer 6, a coordinator under time pressure will shortcut past a specialist, and that shortcut is how incidents happen.

#### Files

- **`ops/`** directory at hub root
- **`ops/_template/CLAUDE.md`** — template for new roles. Exists from day one even when no roles are populated, so adding the first role is a copy-and-fill operation.
- **`ops/{role}/CLAUDE.md`** — per-role operating spec. Same structure as Layer 1 CLAUDE.md but narrower: role's archetype (if distinct), mandate, tools, per-role never list, credentialed surfaces.
- **`ops/{role}/CONTEXT.md`** *(appears when cross-role signals matter)* — living context the coordinator updates with signals from one role that another needs
- **`ops/{role}/decisions.md`** *(appears when a role makes recurring decisions)* — per-role decision log
- **Routing table** lives in Layer 1's CLAUDE.md, mapping task → role, referencing `../ops/{role}/` directories. The routing table is *shared between Layer 1 and Layer 5*; it's declared in Layer 1 but describes the Layer 5 roster.

#### The role-naming rule

Roles are named after the **verb of their work**, not the tool they use. "Store Manager" not "Shopify Agent." "Translation Agent" not "Lokalise Integration." "SEO Agent" not "Ahrefs Operator."

Tools change; verbs don't. A role named after a verb survives tool swaps. A role named after a tool becomes noise the moment you change tools — and worse, its CLAUDE.md starts to read like a tool manual instead of a domain operating spec.

The verb-naming test: **"If we replaced every tool this role uses with a different tool tomorrow, would the role's name still make sense?"** If yes, the name is right. If no, rename.

#### The coordinator delegation rule

The coordinator **does not pass mutation credentials to dispatched subagents.** If a specialist needs write access, one of:

1. **The coordinator performs the mutation itself after user approval.** Credentials stay loaded in *its own* context; the coordinator can do this directly under the specialist's direction, or after a subagent has done the read-phase research and analysis.
2. **The specialist runs as a subprocess with its own credential environment.** Credentials are loaded via the subprocess's own env vars, not passed down the prompt chain.

Subagents spun up by the coordinator **never** receive write tokens as dispatch arguments. This is the 2026-03-27 reflex (R-002), hard-wired into every hub-os hub.

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{role_roster}` | Named specialists in this hub | Store Manager, SEO, Ads, Translation, Image, Accounting |
| `{role_naming}` | Verb-based naming convention | "Store Manager" (manages stores), "SEO Agent" (optimizes discovery) |
| `{credentialed_roles}` | Roles that need mutation capability | Store Manager, Ads, Translation, Accounting |
| `{shared_context_files}` | Common per-role context | `CONTEXT.md`, `decisions.md` |

#### Minimum (day one)

```
ops/
└── _template/
    └── CLAUDE.md       # role template with required sections

# Layer 1 CLAUDE.md routing table:
| Task | Role | Directory |
|------|------|-----------|
| (empty — populated as roles are added)
```

Day-one Layer 5 is an empty `ops/` folder with one template file. The routing table in Layer 1 exists as a table with column headers and no rows. This is legitimate — a hub with one kind of work and one actor doesn't need populated specialists yet. The **structure is present waiting to be filled**; what's minimal is the population, not the layer.

#### Expansion

- **Add a role** when the coordinator finds itself doing recurring specialist work that would benefit from its own mini-coordinator, its own archetype, or its own safety boundaries
- **Populate the routing table** every time a role is added — never leave a role in `ops/` unreferenced from the routing table
- **Add `CONTEXT.md`** to a role when cross-role signals start mattering
- **Add `decisions.md`** when a role makes recurring decisions worth tracking per-role

**Rule of thumb: don't create roles preemptively.** A hub with zero populated roles is healthy. Creating an empty role folder "just in case" is worse than no role because it creates a delegation path with no substance behind it.

#### Example (chiefofstaff)

Six roles in `ops/`, each verb-named: **Store Manager** (manages Shopify stores), **SEO Agent** (optimizes discovery), **Translation Agent** (manages locales), **Ads Agent** (runs Meta campaigns), **Image Agent** (produces visuals), **Accounting Agent** (manages invoicing and MVA). Each has its own CLAUDE.md with domain-specific rules, credentials, and safety boundaries. Munger (Layer 1) never touches Shopify or Meta directly; every mutation flows through the relevant ops role after approval.

The 2026-03-27 incident happened specifically because a coordinator session bypassed this layer and spun up ad-hoc subagents with raw credentials. The routing table and the never list were added the next day.

#### Anti-patterns

- **Tool-named roles.** "Shopify Agent" instead of "Store Manager." Fix: name after the verb, not the tool.
- **Coordinator executing specialist work.** Layer 1 CLAUDE.md grows long sections of domain-specific execution rules, or session logs show the coordinator calling tools instead of routing. Fix: promote execution to a specialist, strip it from Layer 1.
- **Pre-populated empty roles.** Creating 10 role folders on day one "just in case." Fix: add roles under pressure, not preemptively.
- **Credentials passed to subagents.** Coordinator dispatches a subagent with write tokens in the prompt. Fix: credentials stay in the coordinator's context; specialists run as subprocesses or the coordinator performs the mutation.
- **Role with no CLAUDE.md.** A folder exists in `ops/` but has no operating spec. Fix: every role has a CLAUDE.md, even if minimal.
- **Role CLAUDE.md duplicates top-level.** A role's spec repeats identity/working-style content that belongs in Layer 1 or `USER.md`. Fix: role spec inherits by reference and stays narrow and specific.
- **Silent bypass.** Coordinator decides "I'll just do this specialist task directly because it's quick." This is how incidents happen. Fix: routing table entries are non-negotiable; if a task is in the table, the coordinator routes it, period.
- **Orphan role.** A role folder exists but nothing in the routing table points to it. Dead code. Fix: every role is either in the routing table or deleted.

---

### 4.6 Safety (Enforcement) *[hub-scoped]*

#### Purpose

Safety is where the hub enforces **hard lines that instructions alone cannot hold**.

Layer 1's never list is *written down*; Layer 6 is what makes it *enforceable*. The difference matters: a never list without enforcement is a note on the fridge. A never list with hooks behind it is a physical barrier. Instructions work 95% of the time. Hooks work 100% of the time. Anything whose violation would constitute an incident must be enforced by a hook, not just written in a CLAUDE.md section.

Every hub needs Layer 6 from day one, even tiny read-only ones — the minimum is the never list seeded from the reflex card. Hubs that can mutate live state need more: credential separation, hooks, subagent isolation, CRITICAL-rule enforcement.

Sharp distinctions:
- **Safety vs Coordinator (Layer 1):** Layer 1 *declares* the rules (the never list is a Layer 1 section); Layer 6 *guarantees* them (hooks, credential architecture, subagent isolation). The declaration and the enforcement are split across layers on purpose — the declaration is readable by humans and Claude, the enforcement is mechanical.
- **Safety vs Ops (Layer 5):** Layer 5 is the *structure* that makes delegation possible. Layer 6 is what *prevents delegation from being bypassed*. Without Layer 6, a coordinator under time pressure will shortcut past Layer 5.

#### The hooks-over-instructions principle

The single most important Layer 6 principle is: **rules that matter cannot rely solely on instructions.**

A CRITICAL rule written in CLAUDE.md without a backing hook is a wish. Claude follows instructions most of the time, but "most of the time" is exactly wrong for rules whose violation constitutes an incident. If a rule is important enough to be CRITICAL, it is important enough to be enforced mechanically.

The test: **"If this rule is violated, is it an incident?"** If yes → hook. If no → CLAUDE.md is enough.

(This is R-004 in Section 7, the meta-reflex that governs how other reflexes should be enforced.)

#### Files

- **Never list** — lives in Layer 1 CLAUDE.md (declaration), backed by Layer 6 enforcement. The split is deliberate.
- **`.claude/settings.json`** — Claude Code's built-in hook configuration. Every hook-capable hub uses this.
- **`hooks/`** directory *(appears during expansion)* — shell scripts or supplementary hook configs when more than one or two hooks exist and they need version control separate from `.claude/settings.json`
- **Credential layout** — convention for separating read-only and write credentials. Universal pattern, domain-specific implementation.
- **Reflex card reference** — Section 7 of this document; every hub's never list seeds from it on day one.

#### The credential separation pattern

Any mutation-capable integration has a **read-default, write-approved** split:

- Read credentials load automatically on session start; reading is cheap and safe
- Write credentials never auto-load; they require explicit user approval in the current session before being read into context
- Write credentials live in a separate file the coordinator's auto-loading does not touch
- The split is enforced by the credential-loading code, not by discipline

In chiefofstaff this is:
- `ops/sites/{store}/read-credentials.env` — auto-loaded
- `ops/sites/{store}/write-credentials.env` — explicitly loaded only on approval
- `load_store(slug)` = read-only by default
- `load_store(slug, write=True)` = loads write credentials, requires explicit session approval

The *pattern* (read-default, write-approved) is universal. The *implementation* (which files, which functions) is domain-specific. A webdesign hub with a Figma integration would have `figma-read.env` vs `figma-write.env` with the same pattern.

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{credentialed_surfaces}` | Things the hub can mutate | Shopify stores, Meta ad accounts, Notion databases |
| `{read_vs_write_layout}` | How credentials are split on disk | `read-credentials.env` vs `write-credentials.env` per store |
| `{enforceable_never_list}` | Rules important enough to warrant hooks | No direct Shopify writes; no subagent credential passing |
| `{hook_triggers}` | What events hooks fire on | Tool use, file write, subagent dispatch, credential load |

#### Minimum (day one)

```
Layer 1 CLAUDE.md:
└── Never list (seeded from reflex card, minimum 2-3 entries)
    └── Every entry either:
        - Is enforced by a hook (for CRITICAL rules)
        - Or is explicitly noted as "discipline-only" (for preferences)

.claude/settings.json:
└── Minimal hook config (may be empty if no hooks yet)

Credential separation pattern:
└── Declared in CLAUDE.md even if no credentials exist yet
    └── "Mutation credentials, when they exist, follow read-default-write-approved"

hooks/:
└── Empty or absent (appears during expansion)
```

Day-one Layer 6 is: a non-empty never list (seeded from Section 7), a declaration of the credential separation pattern even without credentials yet, and whatever minimal hook config Claude Code ships with. **The never list is the non-negotiable minimum** — every hub, even read-only reflection hubs, has one.

#### Expansion

- **Add the first hook** the first time an incident almost happens or actually happens that instruction-level rules didn't prevent. Every hook has an incident of origin.
- **Implement credential separation** the first time a mutation-capable tool is added to the hub
- **Extend the never list** whenever a new incident surfaces; after extending, check whether the new rule is universal and promote it to the reflex card (Section 7)
- **Split out `hooks/`** as its own directory when there are more than one or two hooks and they need version control
- **Add enforcement for routing** when a coordinator has been caught bypassing a specialist role

#### Example (chiefofstaff)

- **Never list:** no direct Shopify writes, no subagent credential passing, no bypass of named ops roles. All three seeded from the 2026-03-27 incident.
- **Credential separation:** implemented 2026-04-01. Read and write credentials live in separate env files. Auto-loading touches only read. Write requires `load_store(write=True)` with session approval.
- **Hooks:** Claude Code hooks configured in `.claude/settings.json` for sensitive tool use.
- **Subagent rule:** coordinator never dispatches a subagent with write tokens in its prompt. Enforced by convention plus the credential separation (write tokens are not in the coordinator's auto-loaded context, so there's nothing to pass).

On 2026-03-27 a Munger session bypassed the ops routing, spun up ad-hoc subagents with raw Shopify credentials, and published 12 unauthorized blog articles to a live client store. Layer 6 as it exists in chiefofstaff today is the direct product of that incident.

#### Anti-patterns

- **Rules without enforcement.** A CRITICAL rule lives in CLAUDE.md with no hook backing it. Works until it doesn't. Fix: every CRITICAL rule has a hook. The test is "would violation be an incident?"
- **Empty never list.** Layer 6 section is blank because "no incidents yet." This is how you get your first incident. Fix: seed from the reflex card (Section 7) on day one.
- **Unified credentials.** Read and write share one env file that auto-loads with write capability every session. One misstep is an incident. Fix: split read-default, write-approved.
- **Subagent credential passing.** Coordinator dispatches a subagent with write tokens in the prompt. The 2026-03-27 incident in one sentence. Fix: credentials never leave the coordinator's context as prompt arguments.
- **Performative never list.** Rules are worded as suggestions. "Try to avoid direct writes." Fix: hard language. "Coordinator does not mutate store data directly. Period."
- **Hooks that can be disabled casually.** `--no-verify` culture where hooks are bypassed on a whim. Fix: hooks that matter cannot be skipped; if a hook fails, investigate and fix the root cause rather than bypassing.
- **Safety treated as optional.** User declines to populate the never list because "this is a simple hub." Fix: Layer 6 is present from day one; the reflex card provides universal seeds.
- **Documentation-only enforcement.** "We have a rule against X" — and the rule is in a markdown file nobody reads at the moment of temptation. Fix: put the rule where it can't be ignored, which is a hook that fires on the offending action.
- **Split declaration and enforcement drift.** Layer 1 never list says one thing, Layer 6 hook enforces something slightly different. Fix: hooks reference the declared rules by name; when you change one you change both together.

---

### 4.7 Integration *[hub-scoped]*

#### Purpose

Integration is where **external tools meet the hub**. MCP servers, APIs, CLIs, SDKs, file-system conventions, anything Claude reaches outside its own context to interact with. Layer 7 is the layer that documents *what tools exist, how to use them, and what their quirks are*.

The core value of Layer 7 is **accumulated tool wisdom**. First time you use an API, you discover its quirks the hard way. Second time, you discover them again unless you wrote them down. Layer 7 is where you write them down so the third, fourth, and fiftieth time are frictionless. Without it, every new session re-learns the same gotchas and wastes the same tokens.

Sharp distinctions:
- **Integration vs Safety (Layer 6):** Layer 7 documents *how* tools are used; Layer 6 enforces *rules about what tools can be used for*. The Shopify API quirks go in Layer 7; the rule "don't mutate Shopify without approval" goes in Layer 6.
- **Integration vs Ops (Layer 5):** Layer 5 defines specialists who *use* tools; Layer 7 defines the tools themselves. The Store Manager (Layer 5) uses the Shopify API (Layer 7). The Shopify contract doesn't belong in Store Manager's CLAUDE.md — it belongs in Layer 7 so every role that uses Shopify can reference the same canonical contract.

#### Files

- **Layer 1 CLAUDE.md has a "Tools available" section** — the index. Short references, one line per tool, not full contracts.
- **`integrations/`** directory *(appears during expansion)* — per-tool markdown files with full contracts when "Tools available" crosses ~10 lines or any single tool needs more than ~3 lines of documentation.
- **`integrations/{tool}.md`** — per-tool contract: purpose, auth pointer, docs pointer, known quirks, examples, failure modes, rate limits, first-call rules.
- **`.claude/mcp.json`** (or framework equivalent) — MCP server configuration, the native Claude Code file for MCP integrations.
- **Environment variable conventions** — declared either in CLAUDE.md or per-tool, with credential layout cross-referencing Layer 6.

#### What belongs in a tool contract

A Layer 7 tool contract is not a tutorial. Official vendor docs are better at tutorials and they stay fresher. A tool contract documents only the things vendor docs don't:

- **Hub-specific conventions** — how *this* hub uses the tool, what env vars, what helper functions exist
- **Non-obvious parameter quirks** — "use `keywords` param, not `terms`"
- **Known failure modes** — how it fails and how to recognize the failure
- **First-call rules** — "always call `doc` first for any new Ahrefs endpoint"
- **Rate-limit surprises** — the ones you only learn by hitting them
- **Pointer to canonical docs** — vendor URL or Context7 library ID

Everything else defers to vendor docs via pointer. If a future session needs the full API reference, it fetches from the vendor or Context7; Layer 7 only carries the accumulated hub-specific wisdom.

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{tool_roster}` | MCP servers, APIs, CLIs the hub uses | Ahrefs MCP, Shopify Admin API, Meta Marketing API, Notion, Tripletex |
| `{tool_contracts}` | Per-tool quirks worth documenting | Ahrefs `keywords-explorer-matching-terms` param quirk |
| `{auth_setup}` | How each tool authenticates | API keys, OAuth, session tokens (layout in Layer 6) |
| `{first_call_rules}` | Gotchas to prevent before first use | "Call `doc` first for any new Ahrefs endpoint" |
| `{canonical_docs_pointers}` | Where to fetch latest docs | Context7 library IDs, vendor URLs |

#### Minimum (day one)

```
Layer 1 CLAUDE.md:
└── Tools Available section (may list what Claude Code ships with, or be near-empty)

.claude/mcp.json (or equivalent):
└── Whatever MCP servers the hub needs, possibly empty
```

Day-one Layer 7 is the "Tools Available" section in CLAUDE.md. It may be near-empty. The *slot* exists from day one so tool contracts have a home the moment the first tool is added.

#### Expansion

- **Add a tool contract** the first time a tool has a non-obvious quirk worth documenting. The first instance of the quirk *is* the trigger.
- **Split to `integrations/`** when "Tools available" crosses ~10 lines or any single tool needs more than ~3 lines
- **Add environment variable documentation** when credentials are involved (coordinating with Layer 6's credential pattern)
- **Add canonical-docs pointers** when tool docs are external and change frequently
- **Add first-call rules** when misuse is likely or expensive

#### Example (chiefofstaff)

- **Ahrefs MCP** — with the specific `keywords-explorer-matching-terms` param note (`keywords` not `terms`) and the "always call `doc` first for any new endpoint" first-call rule.
- **Shopify Admin API** — accessed via `load_store()` with the read/write split; contract cross-references Layer 6's credential pattern.
- **Meta Marketing API** — integrated for Hackit ad management.
- **Notion API/MCP** — command center, task databases.
- **Tripletex API** — invoicing, with webhooks/checksum and fields-param optimization notes.

Most of chiefofstaff's tool contracts are currently one-line references in CLAUDE.md's "Tools Available" section. None have been split to `integrations/` yet. That's appropriate for the current tool surface — the expansion trigger hasn't fired.

#### Anti-patterns

- **Tool wisdom scattered across roles.** Shopify quirks duplicated in Store Manager's CLAUDE.md and Ads Agent's CLAUDE.md, slightly different in each. Drifts. Fix: one canonical home in Layer 7; roles reference by pointer.
- **No first-call rule.** User learns tool quirks the hard way repeatedly across sessions. Fix: document the quirk the first time it bites.
- **Hardcoded endpoints in prose.** CLAUDE.md contains URLs and endpoint paths inline. These rot when the vendor changes API versions. Fix: reference canonical docs via Context7 or vendor URLs; fetch latest when needed.
- **Tool contract as tutorial.** "How to use the API" rewritten from scratch when official docs exist. Fix: point to official docs, document only the hub-specific quirks.
- **Credential info mixed into tool contract.** Authentication secrets or credential layouts documented inside Layer 7 files. Fix: credential layout is Layer 6; tool contract is Layer 7; they cross-reference, they don't merge.
- **Over-eager MCP installation.** User adds every MCP server they can find "just in case." Context bloat. Fix: add tools when triggered by real need.
- **Missing failure mode notes.** Tool fails in a specific way and the failure mode isn't documented. Fix: every known failure mode gets a line in the contract.
- **Contract without an owner.** A tool's contract exists but no Layer 5 role actually uses it, or the tool is used but no contract exists. Fix: every tool in the contract list is used; every tool used is in the list.

---

### 4.8 Cadence (Rituals) *[hub-scoped]*

#### Purpose

Cadence is where the hub's **rhythms** live. Session rituals, scheduled automation, reconciliation loops, daily/weekly/monthly reviews — anything that happens on a *timing*, whether that timing is "every session" or "every Monday" or "after the first Saturday of the month."

**A hub without explicit cadence is a filing cabinet. A hub with cadence is a system.** The difference: filing cabinets accumulate; systems process. State drifts without session-end reconciliation. Vaults rot without session-end writes. Auto-memory leaks without promotion cycles. Layer 8 is what keeps the other seven layers alive over time.

This is why the minimum non-trivial cadence is required day-one for every hub. Without session rituals, the whole layered structure decays within a week. With them, each session leaves the hub slightly more organized than it started.

Sharp distinctions:
- **Cadence vs Coordinator (Layer 1):** Layer 1 is the spec for *what the coordinator does*; Layer 8 is the spec for *when it does each thing*. "Read OVERVIEW.md on session start" is a cadence rule; "read OVERVIEW.md" without the timing qualifier is homeless.
- **Cadence vs Auto-memory (Layer 3):** cadence sometimes gets put in auto-memory because both are "cross-session," but they're different. Auto-memory is *user preferences that persist across sessions*; cadence is *hub operations that happen on a schedule*. The session-start routine is cadence, not memory.

#### The minimum non-trivial cadence

Every hub has, at minimum, two rituals:

1. **Session start.** Coordinator reads state (OVERVIEW.md, `kanban/proposals/pending.yaml`) and, if Layer 4 is populated, `vault/wiki/hot.md`. Checks in with the user on what's changed since last session.

2. **Session end (when real work was done).** Coordinator reconciles work against open proposals, overwrites OVERVIEW.md, marks resolved proposals. If Layer 4 is populated: updates `hot.md`, files new decisions/lessons as needed, appends to `log.md`. Runs promotion checks (Section 8).

These two are declared in Layer 1 CLAUDE.md at day one. Without them, state and memory go stale within a week.

#### Files

- **Layer 1 CLAUDE.md has a "Rituals" or "Session routine" section** — declares the rituals inline so the coordinator reads them at every session start. This is the declaration half of cadence and is required day one.
- **`cadence/`** directory *(appears during expansion)* — for scheduled automation scripts, cron configs, and rhythm documentation that outgrows CLAUDE.md
- **`cadence/session-start.md`** and **`cadence/session-end.md`** *(during expansion)* — canonical forms when rituals grow past what fits inline in CLAUDE.md
- **Scheduled task configs** — cron, Windows Task Scheduler, GitHub Actions, launchd, whatever the host OS provides
- **`kanban/reports/`** *(lives in Layer 2, but populated by Layer 8)* — canonical destination for scheduled-run outputs

#### Slots

| Slot | What fills it | Example (chiefofstaff) |
|---|---|---|
| `{session_start_steps}` | What the coordinator reads at every session start | OVERVIEW → vault hot.md → check in |
| `{session_end_steps}` | What the coordinator writes at session end | Reconcile pending.yaml → overwrite OVERVIEW → update hot.md → append log.md |
| `{scheduled_tasks}` | Recurring automation beyond sessions | Daily health checks, weekly briefs, calendar sync, ad monitoring |
| `{reconciliation_loops}` | Recurring checks that close open items | pending.yaml reconciliation, cross-agent signal review, timeline rotation |
| `{promotion_triggers}` | When to check for promotion | At session end if patterns emerged |

#### Minimum (day one)

```
Layer 1 CLAUDE.md:
└── Session rituals section
    ├── Session start:
    │   1. Read OVERVIEW.md
    │   2. Read kanban/proposals/pending.yaml
    │   3. (If vault populated) Read vault/wiki/hot.md
    │   4. Check in with user
    └── Session end (when real work was done):
        1. Reconcile kanban/proposals/pending.yaml
        2. Overwrite OVERVIEW.md with current state
        3. (If vault populated) Update hot.md, append log.md, file decisions/lessons
        4. Run promotion checks

cadence/:  # appears during expansion, absent on day one
```

Day-one Layer 8 is a pair of short bulleted lists in CLAUDE.md. No scripts, no cron, no directory. The two rituals are *declared*, which is enough to make the coordinator perform them every session.

#### Expansion

- **Add scheduled automation** when recurring tasks emerge and deserve to run on a clock. Every scheduled task has a *reason it exists* — not "weekly reviews sound responsible."
- **Split rituals to `cadence/`** when session-start or session-end procedures grow past ~5 steps each
- **Activate `kanban/reports/`** in Layer 2 when scheduled runs start producing outputs
- **Add reconciliation loops** for domain-specific recurring checks
- **Add explicit promotion cycles** in session-end when the framework is living (cf. Section 8)
- **Add timeline rotation** when archival overflow is likely

#### Example (chiefofstaff)

- **Session start:** read OVERVIEW.md, read `~/Thehub/vault/wiki/hot.md`, check in with Gabriel on what's changed, offer COO check-in if ops agents have been used since last session
- **Session end:** reconcile `kanban/proposals/pending.yaml`, overwrite OVERVIEW.md, update vault `hot.md`, append to `log.md`, file decisions/lessons if any, review cross-agent notes in touched client briefs, promote important signals to `hot.md`'s agent signals section, timeline rotation if any brief overflows
- **Scheduled automation (built 2026-03-14):** daily store health checks, proposal resurfacing, calendar sync, ad monitoring, weekly briefs. Runs on Windows Task Scheduler. Outputs land in `kanban/reports/`.
- **Reconciliation loop:** `pending.yaml` reconciliation named as non-negotiable in CLAUDE.md.

#### Anti-patterns

- **Implicit cadence.** Rituals exist in the user's head but aren't declared in CLAUDE.md. Coordinator doesn't know when to do what. Fix: declare rituals explicitly in Layer 1 so they're read every session.
- **Cadence in auto-memory.** User puts session rituals in `memory/MEMORY.md` because "it's cross-session." Canonicality violation. Fix: rituals are Layer 8 and declared in Layer 1 CLAUDE.md under a rituals section.
- **Drift between declared and actual.** CLAUDE.md says "reconcile pending.yaml at session end" but coordinator skips it. Fix: rule is non-negotiable or isn't a rule; if skipping happens, add hook enforcement via Layer 6 or remove the declaration.
- **Scheduled automation with no output home.** Cron runs produce files but there's no canonical `kanban/reports/` destination, so outputs scatter. Fix: Layer 8 automation writes to Layer 2's `kanban/reports/` by convention.
- **Over-scheduled.** User adds daily/weekly/monthly reviews that nobody reads. Bureaucracy. Fix: every scheduled task exists because a real need produced it.
- **Session-end skipped.** Real work is done but session-end reconciliation is skipped because "I'll get it next time." State drifts, vault rots. Fix: this is exactly the kind of rule Layer 6 should enforce via hook.
- **Rituals as prose essay.** Session-start routine is described as flowing narrative. Unreadable under time pressure. Fix: bulleted, numbered, actionable steps.
- **Rituals too long.** Session-start routine grows to 20 steps and the coordinator quietly skips half. Fix: short enough to always be performed, or split into sub-routines that run conditionally.

---

## 5. The User-Scoped Layer — `USER.md`

### 5.1 Purpose

`USER.md` is the **single anchor of user-scoped wisdom** that every hub inherits. It's the reason hub #2 starts smart instead of naive. Without it, every new hub has to re-learn the user's working style, decision lens, cross-hub preferences, and recurring people — and the user has to pay the teaching cost over and over again.

`USER.md` is the reference implementation of Layer 3's user-scoped half. The user writes it once, maintains it rarely, and every future hub's Layer 1 CLAUDE.md imports it automatically.

One-sentence version: **If you removed the current hub tomorrow and built a new one for a completely different domain, `USER.md` would still be true. Everything else in the hub would not.**

### 5.2 Location

Provisional location: `~/thehub/USER.md`, sibling to every hub directory. This is flagged for reflection — see Section 1 preamble for the three open angles (thehub namespace vs user namespace; single file vs split; relationship to Claude Code auto-memory).

### 5.3 Canonical sections

`USER.md` has six canonical sections. Every hub expects to find them in this order:

```
USER.md
├── 1. Identity
├── 2. Working style
├── 3. Decision lens
├── 4. People
├── 5. Cross-hub preferences
└── 6. Scope note
```

#### 1. Identity

Who the user is *operationally*. Role, background, capacity, constraints, relevant personality markers. This is the section that tells Claude how to frame advice — a senior engineer gets a different explanation than a student learning to code.

Good identity sections include:
- Professional role and domain
- Relevant personality traits (Enneagram, Big Five, MBTI — whichever the user finds useful)
- Cognitive patterns that affect collaboration
- Operational constraints (time, attention, energy)
- What the user is optimizing for at a life level

Bad identity sections: generic résumé content, aspirational self-descriptions, lists of tools the user knows.

#### 2. Working style

How the user wants to be collaborated with. This is the section that controls how Claude talks, pushes back, and paces responses. It's the single highest-impact section for daily experience.

Good working style sections include:
- Directness preference (hedging vs. blunt)
- Detail preference (concise vs. expansive)
- Pushback tolerance (yes-man vs. devil's advocate)
- When to extract-before-solution vs. jump to answers
- How to handle ambiguous requests
- What the user doesn't want Claude to do

#### 3. Decision lens

How the user weighs tradeoffs. This is the section that shapes *recommendations* across every hub. A framework-agnostic rubric the user applies when deciding what's worth doing.

Good decision lens sections include:
- Named decision philosophies the user has committed to
- Filters the user applies
- Explicit anti-patterns the user has learned to avoid
- The user's time horizon and risk posture

This section is the closest thing the user has to a *written philosophy of their own work*. Most people don't have this written down anywhere. Forcing it into `USER.md` is one of the highest-leverage moves in the entire framework.

#### 4. People

Humans who recur **across** the user's hubs, not within a single one. Family, long-term business partners, regular collaborators, key advisors. Per-hub people (a specific client, a specific counterparty in one domain) belong in that hub's `vault/wiki/people/`, not here.

The test: *"Will this person still matter in a hub I build three years from now for a different domain?"* If yes, `USER.md`. If no, hub-specific vault.

#### 5. Cross-hub preferences

Rules that apply in every hub the user will ever build. Not domain-specific, not client-specific. The universal slice of the user's preferences.

Examples of what belongs here:
- Design preferences
- Communication preferences
- Meta-rules the user has taught Claude through feedback
- Cross-tool conventions the user always uses

Examples of what does *not* belong here:
- Hub-specific rules (e.g., "don't mutate Shopify without approval" — lives in the relevant hub's never list)
- Domain-specific practices (e.g., "always pull GSC alongside Ahrefs" — lives in the SEO ops role's CLAUDE.md)

#### 6. Scope note

A short closing section that tells future Claude sessions *what this file is not for*. Critical because without it, `USER.md` bloats — every piece of reflection starts to look like it belongs here, and suddenly the file is 10,000 words of mixed hub-scoped and user-scoped content.

A good scope note names the canonical alternatives and ends with the default test: *"Would this still be true in a completely different hub?"*

### 5.4 Import pattern

Every hub's Layer 1 CLAUDE.md imports `USER.md` by **reference**, not by copying.

```markdown
## Working style

See `~/thehub/USER.md` for full user profile, working style, decision lens, and cross-hub preferences.

Key reminders in this hub's context:
- [1-3 lines of hub-specific reinforcement, if needed]
```

This does two things:
1. **Prevents drift.** There is one canonical copy. Updates to `USER.md` propagate to every hub on the next session start.
2. **Keeps each hub's CLAUDE.md short.** Layer 1 doesn't need to repeat identity/working-style content; it just points.

### 5.5 What goes in vs. what doesn't

| Belongs in `USER.md` | Belongs elsewhere |
|---|---|
| How the user thinks | Hub-specific current status (→ OVERVIEW.md) |
| How the user wants to collaborate | Per-client briefs (→ hub `vault/wiki/clients/`) |
| Decision lens the user applies everywhere | Hub-specific decisions (→ hub `vault/wiki/decisions/`) |
| People who recur across every hub | People specific to one hub's domain (→ hub `vault/wiki/people/`) |
| Cross-hub preferences ("no emojis") | Hub-specific rules ("no Shopify writes") → hub never list |
| Cross-tool conventions | Tool-specific quirks → hub Layer 7 contracts |
| Named lessons the user has accepted as universal | Hub-specific lessons (→ hub `vault/wiki/lessons/`) |

The core test, repeated: **"Will this still be true in a totally different hub I build three years from now?"** If yes, `USER.md`. If not, hub-specific.

### 5.6 Worked example

Below is a fleshed-out example showing what a real, populated `USER.md` looks like. Specific to one user; any user's version would be equally specific to them.

```markdown
# USER.md

Canonical user profile shared by every hub I build. Imported by each hub's Layer 1
CLAUDE.md by reference, not by copy.

---

## 1. Identity

I'm Gabriel, an independent operator based in Bergen, Norway. I build and run things —
ecommerce ventures, consulting work, software, design. My default mode is systems
thinking: I see problems as interactions, not isolated parts, and I tend to build
infrastructure I can reuse across work rather than one-off solutions.

**Operational style:** ENK (single-person company) by legal structure, solo operator by
choice, but I collaborate deeply with a small number of people.

**Personality markers that matter for collaboration:**
- Enneagram 3w4 — "The Professional." Core drive: build things that work AND that are
  authentically mine. Under stress I equate productivity with self-worth and launch new
  things because starting feels like progress.
- Big Five highlights:
  - Neuroticism: 48 (low) with Immoderation 13 (high) — calm under pressure, but impulse
    control is my weak spot
  - Extraversion: 99 with Gregariousness 11 — energized by people, deeply assertive, but
    I want depth not crowds
  - Openness: 88 with Intellect 20, Liberalism 11 — love ideas intensely, respect proven
    structures
  - Agreeableness: 90 with Altruism 18 — high trust, over-gives to people I care about
  - Conscientiousness: ~95 with Achievement-Striving 20, Self-Discipline 18, but
    **Orderliness 6** — I push relentlessly but cannot maintain tidy systems. This is
    why Claude exists in my workflow.
- ENTJ — commander type. Strategy and delegation natural; impatient with inefficiency.

**Patterns to watch for:**
1. Starting new things as a substitute for finishing current things
2. Doing free work for people I care about when overextended
3. Information scattered everywhere because I can't maintain organizational systems
4. Mistaking motion for traction

---

## 2. Working style

- **Be direct.** No hedging, no corporate speak. If I'm wrong, say so. If a priority is
  misaligned, push back. I hired you to think, not to agree.
- **Extract before solving.** When I dump a wall of context at you, your first job is to
  extract what actually matters and reflect it back before jumping to solutions.
- **Meet me in systems.** Don't give me isolated advice — show me how things connect.
- **Let me talk through things.** I sometimes need to talk through something before I
  know what I'm actually asking. Make space for that, then help me land on the real
  question.
- **Be the counterweight.** When I'm spinning up something new while existing things are
  unfinished, say so directly.
- **Don't perform caution.** Pick the right answer and defend it. Stop recommending the
  lighter option, suggesting session close, or hedging as "your call."
- **No human-frame cost bias.** Don't project human fatigue onto agent work. Name which
  agent-scale cost drives any "defer/lighter" recommendation.
- **Short responses default.** Terse is better than complete.

---

## 3. Decision lens

**Boring Empire philosophy.** No dramatic single bets. Build scalable, systematic,
repeatable infrastructure. Compound small advantages. This came from a past failure
(dropshipping → wholesale commitment → tax debt → wind down). Lesson: no hero bets.

**Investment lens.** Peter Lynch concentrated approach — invest in what I understand.
I think about "wisdom layer" companies — businesses where deep institutional knowledge
is the moat.

**When weighing tradeoffs, apply these filters:**
1. Does this compound, or is it a one-off?
2. Does this build infrastructure I can reuse?
3. Am I the bottleneck? If so, how do we unblock?
4. What's the cost of *not* deciding right now?

**Anti-patterns I've learned to watch for:**
- Premature abstraction — three similar lines is better than a wrong framework
- Starting new things as a form of progress theater
- Over-giving time to friends/family at the expense of paying work
- Confusing activity with traction

---

## 4. People

People who recur across every hub I build, regardless of domain:

- **Alex** — my father. Enterprise systems architect. Highly capable but I struggle to
  delegate to him effectively.
- **Robin** — long-term business partner. Co-founder of multiple ventures. Capable
  salesperson.
- **Sam** — business partner. Co-founder. The vision guy; sees the big picture.
- **Quinn** — girlfriend.

(Per-domain people live in each hub's `vault/wiki/people/`, not here.)

---

## 5. Cross-hub preferences

- **Credential safety:** never pass write credentials to dispatched subagents. Mutation
  tokens stay in the coordinator's context and require session-level approval.
- **Hooks over instructions:** CRITICAL rules need hook enforcement, not just CLAUDE.md
  prose.
- **Design preferences:** no AI clutter (eyebrow text, trust badges, heavy borders, emoji
  lists, "revolutionary" copy). Iterate via hotter/colder.
- **Pricing research rule:** never anchor to one data point. Separate math from strategy.
  Cross-reference parallel research.
- **Bidirectional ops updates:** when using ops agents, push status DOWN to their context
  files, don't just read from them.
- **No emoji in files unless explicitly requested.**
- **Obsidian flavored markdown** in any vault-adjacent content.
- **Decision records with wikilinks** — every non-trivial decision links affected people
  and projects.

---

## 6. Scope note

This file is user-scoped. Things it is **not** for:

- **Current operational state** → hub's `OVERVIEW.md` (Layer 2)
- **Hub-specific decisions and rationales** → hub's `vault/wiki/decisions/` (Layer 4)
- **Per-client context** → hub's `vault/wiki/clients/` (Layer 4)
- **Per-project context** → hub's `vault/wiki/projects/` (Layer 4)
- **Hub-specific rules** → hub's Layer 1 never list
- **Hub-specific tool contracts** → hub's Layer 7 integration notes
- **Session rituals** → hub's Layer 1 CLAUDE.md rituals section (Layer 8)
- **Cross-session agent behavior context** → Claude auto-memory per-hub

**Default test:** *"Would this still be true in a completely different hub I build three
years from now?"* If yes, it belongs here. If no, it goes in the hub.
```

### 5.7 Maintenance

- **Human-curated.** `USER.md` is written and edited by the user, not auto-written by Claude. Claude *proposes* promotions (see Section 8); the user *approves* them.
- **Rarely edited.** If `USER.md` is changing weekly, something is wrong — probably hub-specific content is sneaking in. Monthly edits are healthy; daily edits are a smell.
- **Session-end promotion check.** Layer 8's session-end ritual includes "check whether any feedback memories from this session are universal enough to promote to `USER.md`" — but the check only *proposes*, never auto-writes.
- **Split when it grows.** When `USER.md` crosses ~2000 words, split into section files: `USER/identity.md`, `USER/working-style.md`, etc.

### 5.8 Anti-patterns

- **Bloat.** Hub-specific content sneaks in because it felt important. Fix: scope note + "would this be true in a different hub?" test.
- **Auto-written by Claude.** Claude writes to `USER.md` directly during a session. Drifts, duplicates, loses the human-curated discipline. Fix: Claude proposes, user approves.
- **Split too early.** User splits `USER.md` into five files on day one. Fragmented, hard to maintain. Fix: single file until it crosses ~2000 words.
- **Canonicality violation with auto-memory.** Same rule written in both `USER.md` and `memory/MEMORY.md`. Drifts. Fix: `memory/` is staging; `USER.md` is the canonical home for promoted rules.
- **No scope note.** `USER.md` grows indefinitely because there's no reminder of what it's *not* for. Fix: section 6 is non-optional; write it day one.
- **Working-style section too short.** "Be direct" and nothing else. Produces generic collaboration. Fix: populate with the feedback you've actually given Claude over time.
- **Identity section as résumé.** "I know TypeScript and Python." Useless for collaboration. Fix: identity is *how you think and operate*, not *what skills you have*.

---

## 6. Instantiation Playbook

This section is the **step-by-step guide for turning hub-os from a skeleton into a live hub**. It assumes you have already built at least one hub (or are working from a reference hub like chiefofstaff) and understand the eight layers in principle. If not, read Sections 3 and 4 first.

### 6.1 The golden rule of instantiation

**Do the interview before you touch any files.** The failure mode hub-os is most vulnerable to is *cargo culting* — copying the chiefofstaff directory, renaming Munger to some other name, deleting the parts that look unfamiliar, and shipping. Cargo-culted hubs feel functional for a week and then collapse because the slots were filled without the reasoning that justifies the fillings.

The interview is a conversation between the user and Claude that answers a specific set of questions *before* any file gets written. If you skip it, you will build the wrong hub. If you do it properly, the file operations that follow are mechanical.

### 6.2 The pre-instantiation interview

These are the questions the interview must answer. Don't start file operations until all of them have real answers — not placeholders.

#### Domain questions

1. **What domain does this hub coordinate?** One sentence. If the answer needs more than one sentence, the domain is too broad — split it.
2. **What does this domain punish?** What kinds of decisions go wrong? What failure modes recur? This is the single most important input to archetype selection.
3. **What does this domain reward?** What patterns compound? What reflexes pay off over time?
4. **Is this hub the user's *only* hub, or one of several?** If one of several, a `USER.md` already exists to inherit from. If it's the first, `USER.md` needs to be built as part of this instantiation.

#### Archetype questions

5. **Given the punishments and rewards, what archetype's native reflexes match?** Pick a real named figure (Section 4.1 rules). Write 1–2 paragraphs on *why this archetype for this domain*.
6. **Does this archetype contrast with the user's weaknesses, or amplify them?** If amplify, pick a different one.
7. **Does the user respect this archetype enough for its pushback to land, but disagree with it sometimes?** If always agreement, pick a different one.

#### Structure questions

8. **What is the mandate?** 1–3 sentences. The coordinator's job in plain language.
9. **Who is the primary user?** Just confirm — should be the same user `USER.md` describes.
10. **What domains of work does the hub coordinate?** The domain map. Bulleted.
11. **Do any specialist roles need to exist from day one?** Often the answer is *no*. If yes, name them with verb-based names (not tool-based) and answer questions 12–14 for each.
12. **For each day-one role: what does it do, what tools does it use, and does it have mutation capability?**
13. **What credentialed surfaces exist?** Anything the hub can mutate — APIs, databases, external services, file systems with write access.
14. **Which of those surfaces auto-load on session start, and which require explicit approval?** Answer should always be: read auto-loads, write requires approval.

#### Cadence questions

15. **What session-start ritual makes sense?** Minimum: read OVERVIEW + pending.yaml. Add hot.md if Layer 4 is populated.
16. **What session-end ritual makes sense?** Minimum: reconcile pending.yaml + overwrite OVERVIEW. Add vault writes, promotion checks, and reconciliation loops as needed.
17. **Are there any scheduled tasks that should exist from day one?** Usually no. If yes, name them and their cadences.

#### Integration questions

18. **What external tools does the hub need?** MCP servers, APIs, CLIs.
19. **For each: what's the minimum contract?** At least: purpose, auth pointer, docs pointer.

#### Reflex questions

20. **Which reflexes from the reflex card (Section 7) apply to this hub?** Usually most of them — they're universal by design.
21. **Are there any known failure modes specific to this domain that aren't in the reflex card?** Write them down now. They become this hub's own seed entries in Layer 6.

When every question has a real answer, the interview is done. Save the answers somewhere — you'll reference them during file operations.

### 6.3 File operations (in order)

Now that the interview is done, the file operations are mechanical. Do them in this order.

#### Step 1 — Create the hub directory

Sibling to other hubs. Name the directory after the domain, not the archetype (chiefofstaff, not munger).

#### Step 2 — Ensure `USER.md` exists

If this is not the user's first hub, `USER.md` already exists. Verify the path is right and you can import it. If this *is* the first hub:

1. Draft `USER.md` using the Section 5.3 canonical six-section structure.
2. Fill in real content for at least Identity, Working style, and the Scope note.
3. Decision lens, People, and Cross-hub preferences can start partial and grow.
4. Save to the chosen location (default: `~/thehub/USER.md`).

#### Step 3 — Create Layer 1 (`CLAUDE.md`)

Copy the hub-os CLAUDE.md template into the new hub directory. Fill the slots from the interview answers:

- Identity (archetype + 1–2 paragraph fit from Q5–7)
- Working style (reference to `USER.md`)
- Mandate (from Q8)
- Domain map (from Q10)
- Routing table (from Q11; empty table with headers if no day-one roles)
- Never list (seeded from reflex card + any domain-specific additions from Q21)
- Current status (pointer to `OVERVIEW.md`)
- Tools available (from Q18–19)
- Rituals section (from Q15–16)

#### Step 4 — Create Layer 2 (state)

```
OVERVIEW.md                        # four canonical sections, mostly empty
kanban/
└── proposals/
    └── pending.yaml               # empty array
```

#### Step 5 — Verify Layer 3 is wired up

Layer 3 is the only user-scoped required layer and its two sub-locations have different lifecycles:

- **`USER.md`** — verify it's in place at its chosen location (`~/thehub/USER.md` by default) and that Layer 1 CLAUDE.md imports it by reference. This is the day-one work.
- **`memory/`** — Claude Code's auto-memory lives at `~/.claude/projects/{hub-path}/memory/`, *not* inside the hub directory. Claude Code creates this directory automatically on first session. No day-one scaffolding required; it populates itself as sessions accumulate. If this is the user's first hub ever, Claude Code may need one session to create the initial `MEMORY.md` index — that happens naturally, not as part of instantiation.

#### Step 6 — Create Layer 4 (vault)

```
vault/wiki/
├── hot.md                         # 1-line seed, ~50 words
├── index.md                       # section headers, no entries yet
├── log.md                         # empty, ready for first append
├── decisions/
├── lessons/
├── people/
├── projects/
└── clients/                       # rename per domain if needed
```

#### Step 7 — Create Layer 5 skeleton

```
ops/
└── _template/
    └── CLAUDE.md                  # role template
```

If the interview named day-one roles, create each one with its own CLAUDE.md and CONTEXT.md. Update the routing table in Layer 1 CLAUDE.md to point at them.

#### Step 8 — Declare Layer 6 patterns

Layer 6 doesn't usually get its own files on day one. Instead:

1. Never list in Layer 1 CLAUDE.md is non-empty (seeded in Step 3)
2. Credential separation pattern is **declared** in CLAUDE.md, even if no credentials exist yet
3. If credentialed surfaces already exist (Q13–14), set up the actual read/write credential split

#### Step 9 — Declare Layer 7 tools

"Tools available" section in Layer 1 CLAUDE.md populated from Q18–19. One line per tool, with a pointer to canonical docs.

#### Step 10 — Declare Layer 8 rituals

"Rituals" or "Session routine" section in Layer 1 CLAUDE.md populated from Q15–16.

#### Step 11 — (Optional) Create `reflexes.md` for tracked inheritance

If you want to make reflex inheritance visible, create `hub/reflexes.md` listing which reflex IDs from Section 7 are active in this hub.

### 6.4 Day-one verification

Before running the first real session, verify the hub is structurally sound:

- [ ] `CLAUDE.md` exists at the hub root with all required sections
- [ ] `CLAUDE.md` references `USER.md` by import path, not by copy
- [ ] `USER.md` exists at its expected location and is readable
- [ ] `OVERVIEW.md` exists with the four canonical sections
- [ ] `kanban/proposals/pending.yaml` exists (even if empty)
- [ ] `vault/wiki/` exists with all canonical subfolders and `hot.md`, `index.md`, `log.md`
- [ ] `ops/_template/CLAUDE.md` exists
- [ ] Never list in `CLAUDE.md` is non-empty (has at least the inherited reflexes)
- [ ] Tools available section declared
- [ ] Rituals section declared with session start and session end
- [ ] If credentialed surfaces exist: read and write credentials are in separate files
- [ ] No top-level `memory/MEMORY.md` contains hub-scoped or ritual content (canonicality check)

### 6.5 First session

1. Read `CLAUDE.md`, which imports `USER.md`
2. Execute the session-start ritual from Layer 8
3. Notice that everything is mostly empty — this is expected on day one
4. Check in with the user to confirm the archetype feels right, the mandate makes sense, and the interview answers match reality

If any interview answer turned out to be wrong, fix it **now** — day one is the cheapest time to revise.

Then do one small piece of real work in the hub. File the first vault entry. Reconcile pending.yaml. Overwrite `OVERVIEW.md`. Update `hot.md`. Append to `log.md`. Close the session.

### 6.6 Common instantiation mistakes

- **Skipping the interview.** Produces a hub that feels almost right and silently fails.
- **Wrong archetype because it sounded cool.** Apply the punishment/reward test and the contrast test.
- **Over-populated ops on day one.** Start with zero populated roles.
- **Copying `USER.md` contents into `CLAUDE.md`.** Breaks inheritance.
- **Empty never list** because "no incidents yet." Seed from the reflex card.
- **Skipping credential declaration** because "no credentials yet." Declare the pattern as policy.
- **Putting session rituals in memory** instead of CLAUDE.md. Canonicality violation.
- **Starting the first session without reading `CLAUDE.md` yourself.**

---

## 7. The Reflex Card

### 7.1 Purpose

The reflex card is **inherited scar tissue**. Every rule in it exists because something broke somewhere — in `chiefofstaff`, in another hub-os hub, or in a pre-framework project — and the rule was added to prevent the same break from happening again. Rather than making every new hub earn its own scars from scratch, the reflex card lets new hubs inherit the rules and skip the incidents.

A day-one hub with zero reflexes is naive: it has a never list section but nothing in it, and the first time a mutation-capable tool gets added, the coordinator has no standing instructions against misusing it. A day-one hub seeded from the reflex card starts with a non-empty never list, declared safety patterns, and awareness of the failure modes that have already bitten other hubs.

The reflex card is therefore **load-bearing for day-one Layer 6.**

### 7.2 Schema

Each reflex entry has the following fields:

- **id** — `R-XXX`, sequential
- **incident** — One-sentence description of what broke
- **rule** — The rule that was added in response (hard language, imperative)
- **why** — The causal link — why this rule prevents this kind of incident
- **layer** — Which hub-os layer the rule affects
- **date** — When the reflex entered the card (YYYY-MM-DD)
- **source_hub** — Which hub surfaced it
- **enforcement** — `discipline-only` | `hook` | `architecture`

Reflex entries are rendered as markdown tables in Section 7.4 for readability.

**Enforcement values:**
- **discipline-only** — the rule is prose in CLAUDE.md; depends on Claude following instructions
- **hook** — the rule is enforced by a Claude Code hook that fires mechanically
- **architecture** — the rule is enforced by the file/credential layout

Architecture enforcement is strongest; hook is second; discipline-only is weakest. Every reflex should aim for the strongest enforcement its nature allows.

### 7.3 How new hubs use the reflex card

Day-one instantiation flow:

1. **Read the reflex card** (this section).
2. **Filter for universal reflexes** — any entry that isn't domain-specific. Most are.
3. **Seed Layer 1 never list** with the rules from those reflexes. Each never-list entry references its reflex ID.
4. **Seed Layer 6 enforcement patterns** — credential separation, subagent rules, hook principles.
5. **Optionally seed a `hub/reflexes.md` file** listing which reflex IDs are active in this hub.

A day-one hub should have **all eight reflexes active** by default — they are universal by design. R-001 through R-004 are the **safety-critical core** (incident-preventing rules about delegation, credentials, and enforcement); R-005 through R-008 are equally universal but address **operational hygiene** (state discipline, bidirectional ops flow, cost framing, canonicality). The only reason to drop a reflex during instantiation is if the domain genuinely doesn't exercise it — e.g., a read-only research hub has no mutation-capable surfaces and R-003 is a no-op until one appears. When in doubt, keep all eight.

### 7.4 The reflex card (v0.2)

**R-001 — Coordinator routes, coordinator does not execute**

| Field | Value |
|---|---|
| incident | 2026-03-27: A top-level Munger session in `chiefofstaff` bypassed the ops routing layer, spun up ad-hoc subagents with raw Shopify credentials, and published 12 unauthorized blog articles to a live client store. The named ops roles (SEO, Translation, Store Manager) were never consulted. |
| rule | The coordinator delegates specialist work to named ops roles and does not execute specialist work directly. If a task has a specialist in the routing table, the coordinator routes to that specialist — the coordinator never shortcuts around it. |
| why | Specialists carry domain-specific safety rules in their own CLAUDE.md files. When the coordinator bypasses them, those rules never get enforced. The coordinator has altitude; specialists have depth. Losing depth under time pressure is how incidents happen. |
| layer | 1 (declared in never list) + 5 (enforced via routing table) |
| date | 2026-03-27 |
| source_hub | chiefofstaff |
| enforcement | discipline-only (can be upgraded to hook) |

**R-002 — No subagent credential passing**

| Field | Value |
|---|---|
| incident | Same session as R-001: ad-hoc subagents were dispatched with raw Shopify access tokens in their prompts, giving them write capability outside the coordinator's oversight. |
| rule | The coordinator never dispatches a subagent with mutation credentials as prompt arguments. If a subagent needs write access, either the coordinator performs the mutation itself under the subagent's direction, or the subagent runs as a subprocess with its own credential environment. |
| why | Credentials passed down the prompt chain lose the approval surface. The coordinator can't enforce "ask the user before writing" on a subagent that already has the token. Keeping credentials in the coordinator's own context forces every mutation through the approval gate. |
| layer | 5 (ops delegation rule) + 6 (credential architecture) |
| date | 2026-03-27 |
| source_hub | chiefofstaff |
| enforcement | architecture |

**R-003 — Read-default, write-approved credential separation**

| Field | Value |
|---|---|
| incident | 2026-04-01 response to R-001 and R-002: unified credential files meant that every session had latent write capability, and a single mistake could activate it. |
| rule | Any mutation-capable integration separates read and write credentials into different files. Read credentials auto-load on session start. Write credentials never auto-load — they require explicit session approval before being read into context. |
| why | The window for mistakes is the window in which write capability is live. Minimize that window by making write capability opt-in per session, not on by default. A session that never calls the write-enabling function cannot write to the surface, period. |
| layer | 6 (safety architecture) |
| date | 2026-04-01 |
| source_hub | chiefofstaff |
| enforcement | architecture |

**R-004 — Hooks over instructions for CRITICAL rules**

| Field | Value |
|---|---|
| incident | Several chiefofstaff feedback cycles where CRITICAL/NEVER rules declared in CLAUDE.md were followed *most* of the time but violated under pressure. The violations produced real incidents. |
| rule | If a rule's violation would constitute an incident, the rule must be enforced by a mechanical hook (Claude Code hook or architecture), not by CLAUDE.md prose alone. Instructions are for preferences; hooks are for CRITICAL rules. |
| why | Claude follows instructions most of the time, but "most of the time" is exactly wrong for rules whose violation is an incident. The test: *"if this rule is violated, is it an incident?"* → if yes, hook; if no, CLAUDE.md is enough. |
| layer | 6 (enforcement principle, meta-reflex) |
| date | 2026-04 |
| source_hub | chiefofstaff |
| enforcement | meta-reflex |

**R-005 — State must be overwrite-only; history goes to vault**

| Field | Value |
|---|---|
| incident | Multiple chiefofstaff sessions where `OVERVIEW.md` accumulated stale entries or `pending.yaml` filled with resolved proposals left as open. Coordinator started operating from memory instead of the file because the file had become unreadable. Stale proposals describing finished work eroded trust in the entire state layer. |
| rule | Layer 2 (state) is overwrite-only. `OVERVIEW.md` is completely rewritten every session where work happened. Resolved proposals are marked `resolved` with a note and then deleted or archived to vault within one cycle. History lives in `vault/wiki/log.md`, not in state. |
| why | State is *what is true now*. The moment state includes things that are no longer true, the coordinator can't trust state at all, and the whole hub loses its ground. Overwrite discipline is what keeps state usable as a reference. |
| layer | 2 (state) + 8 (cadence ritual) |
| date | 2026-04 |
| source_hub | chiefofstaff |
| enforcement | discipline-only |

**R-006 — Bidirectional ops updates**

| Field | Value |
|---|---|
| incident | Chiefofstaff sessions where the coordinator read from ops agent context files but never wrote back. Over time, ops agents' own context files drifted out of sync with what the coordinator knew, and downstream sessions invoking those ops agents operated on stale context. |
| rule | When the coordinator uses an ops role, it must push any new relevant signals back *down* into that role's `CONTEXT.md` — not just read from the role's files. Ops context flows both directions. |
| why | Ops roles are mini-coordinators. Their CONTEXT.md is *their* state layer. If the top-level coordinator never updates it, the ops role's state rots the same way a neglected `OVERVIEW.md` rots. Bidirectional flow is how the whole structure stays coherent. |
| layer | 5 (ops) + 8 (cadence, session-end ritual) |
| date | 2026-04 |
| source_hub | chiefofstaff |
| enforcement | discipline-only |

**R-007 — Reason about agent-scale costs, not human-scale costs**

| Field | Value |
|---|---|
| incident | Chiefofstaff sessions where the coordinator recommended "let's defer this" or "do the lighter version" based on projected human fatigue — except the work would be performed by agents, not by the human. The recommendations were systematically biased toward smaller scope because the coordinator was modeling human effort. |
| rule | When estimating the cost of a piece of work, reason about agent-scale costs explicitly — tokens consumed, tool calls required, context window pressure, session continuity, credential surface — rather than projecting human fatigue. If a defer/lighter recommendation is being made, name which of the four agent-scale costs drives it. |
| why | Agents don't get tired; the economics of "defer for later" are different when the executor is an agent. Recommendations that silently assume human constraints misallocate work and confuse the user about what's actually expensive. |
| layer | 1 (coordinator reasoning) |
| date | 2026-04 |
| source_hub | chiefofstaff |
| enforcement | discipline-only |

**R-008 — Canonicality: every piece of information has exactly one home**

| Field | Value |
|---|---|
| incident | Chiefofstaff's `memory/MEMORY.md` accumulated a mix of user-scoped (working style, preferences) and hub-scoped (project status, current clients) content. The same information started appearing in two layers and drifted out of sync. Trust in both layers degraded. |
| rule | Every piece of information has exactly one canonical location. No piece is stored in two layers. When it looks like a piece could belong in two layers, apply the Section 3.2 canonicality decision table and pick one. |
| why | Duplication is how frameworks rot. When the same fact appears in two places, the two places drift, the user stops knowing which is authoritative, and eventually both are ignored. Single-source discipline is what keeps the layer graph honest. |
| layer | All (cross-cutting meta-rule) |
| date | 2026-04-13 (surfaced during hub-os extraction) |
| source_hub | chiefofstaff |
| enforcement | discipline-only (reinforced by Section 3.2) |

### 7.5 Maintenance

- **New reflexes are added when incidents happen.** A real incident + a rule that would have prevented it = a new reflex card entry. No speculative reflexes.
- **Universality check before adding.** Before a hub-specific reflex gets promoted into this card, it must pass the *"would this rule matter in a totally different hub?"* test. Hub-specific reflexes stay in the hub's own never list.
- **Enforcement upgrades over time.** A discipline-only reflex that keeps getting violated gets upgraded — first to a hook, then to architecture enforcement if possible.
- **Deprecation.** If a reflex turns out to be wrong, it gets marked deprecated rather than deleted, with a note on what replaced it. The deprecation record preserves the learning.
- **Version the card.** The reflex card has a version number (currently v0.2). Each version change is logged in Section 11.

---

## 8. Promotion Rules

### 8.1 Purpose

Promotion is the mechanism that keeps hub-os **living** rather than frozen. Without it, lessons learned in one hub stay trapped there, the framework never improves, and `USER.md` never accumulates the wisdom that would make hub #3 start smarter than hub #2.

Promotion is the upward flow from specific to general. A lesson learned in one session becomes a rule in one hub, becomes a cross-hub preference in `USER.md`, becomes (if universal enough) a reflex in the framework doc. Each step up raises the bar and widens the blast radius.

### 8.2 The three promotion paths

#### Path A — Staging (`memory/`) → `USER.md`

**What flows:** user-scoped preferences that have proven stable
**Scope:** one user, across every hub they build
**Authority:** Claude proposes, user approves
**Trigger:** session-end check + periodic review

#### Path B — Staging (`memory/`) → Hub vault (Layer 4)

**What flows:** hub-scoped domain knowledge that Claude accumulated but that belongs as a decision, lesson, or project note
**Scope:** one hub
**Authority:** Claude can write directly (Layer 4 is designed to accumulate)
**Trigger:** session-end when real work produced a vault-worthy entry

#### Path C — Hub reflex → Framework (this document)

**What flows:** reflexes that started as hub-specific rules but prove universal across domains
**Scope:** every hub-os instance, current and future
**Authority:** requires explicit user decision — highest bar
**Trigger:** pattern recognition when a new reflex is added to a hub, or when the same reflex surfaces in a second hub

The three paths have different blast radii. Path B affects one hub's future. Path A affects one user's every hub. Path C affects every user's every hub. **The bar scales with the blast radius.**

### 8.3 Triggers — when to check for promotion

| Trigger | What to check | Who decides |
|---|---|---|
| **Every session end (when real work was done)** | Did anything this session belong in the vault (Path B)? | Claude can file directly |
| **Every session end** | Did the user teach Claude something this session that might apply cross-hub (Path A)? | Claude proposes; user approves |
| **Monthly review** (or when building a new hub) | Is there anything in `memory/` that has been stable long enough to promote to `USER.md`? | Claude proposes; user approves |
| **When a new reflex is added to a hub's never list** | Is this reflex universal enough to promote to the framework (Path C)? | User decides explicitly |
| **When instantiating a new hub** | Does anything in the current hub's never list or vault lessons belong in the framework or `USER.md`? | User decides explicitly |

### 8.4 Bars and tests

#### Path A bar: the cross-hub test

**"Would this preference still matter in a completely different hub I build three years from now for a different domain?"**

- Yes → promote to `USER.md` cross-hub preferences section
- No → it stays hub-scoped
- Mixed → usually stays hub-scoped; promote only if you can state a *universal* version of the rule

#### Path B bar: the vault entry test

**"Is this a decision with a rationale, a named pattern, a domain actor, a project, or cross-cutting reflection?"**

- Yes → Claude can file directly in the appropriate vault subfolder
- No → don't file; it's either operational state (Layer 2) or ephemeral

Path B has the lowest bar because the vault is designed to accumulate.

#### Path C bar: the universality test

**"Would this reflex matter in a hub for web design? For research? For writing? For bookkeeping? In a hub for a totally different user?"**

- Yes to most → candidate for framework promotion
- Yes to some → candidate for `USER.md` (Path A), not framework
- Only this domain → stays hub-scoped

**Additional Path C test — the source diversity check:** if a reflex has only been surfaced by one hub, be suspicious. Wait until it shows up in a second hub (or until the user explicitly states it's general) before promoting.

### 8.5 The session-end promotion check

What the coordinator does at session end when real work happened:

1. **Path B check.** Scan the session's work for vault-worthy entries — decisions made, lessons named, new people/projects mentioned. File them directly in the appropriate vault subfolder with wikilinks.
2. **Path A proposal.** Scan for anything the user taught Claude this session that smells cross-hub. If found, *propose* to the user: *"Based on [feedback X], I'd propose adding this to your `USER.md` cross-hub preferences: [exact wording]. Approve, revise, or reject?"* Do not auto-write.
3. **Path C surfacing.** If a new reflex was added to the hub's never list this session, ask: *"This new reflex is domain-specific as written. Is there a universal version of it that should go in the hub-os reflex card?"* Defer to user judgment.

### 8.6 What *not* to promote

- **Anything still unstable.** If a rule has only been taught once, wait.
- **Ephemera.** "I was frustrated this session" is a mood, not a cross-hub preference.
- **Domain knowledge as preferences.** "In ecommerce, MVA deadlines matter" is domain knowledge, not a user preference.
- **Hub-specific tools as universal tools.** "Use Ahrefs for keyword research" is domain-specific.
- **Reflexes without incidents.** "We should have a rule against X" spoken speculatively is not a reflex.
- **Anything the user hasn't explicitly approved (Path A and C).**

### 8.7 Demotion and retraction

- **Demotion path:** framework → hub-scoped (the reflex turns out to be domain-specific after all)
- **Retraction path:** `USER.md` → removed (the preference turns out to be wrong or was taught under stress)
- **Reflex card deprecation:** entries get marked `deprecated` with a replacement pointer; they are not deleted

Retractions and deprecations are logged in Section 11 the same way promotions are.

### 8.8 Anti-patterns

- **Silent auto-promotion to `USER.md`.** Claude writes to `USER.md` without user approval. Fix: Claude proposes, user approves.
- **Never promoting.** User avoids promotion because "it's not quite ready." Fix: monthly review trigger.
- **Promoting without recording origin.** Rule appears with no incident trail. Fix: every framework reflex has an incident, date, and source hub.
- **Promoting hub-specific rules as universal.** "Never mutate Shopify without approval" gets promoted to the framework. But the framework doesn't know about Shopify. Fix: the *general* version is what's universal; the specific application stays in the hub.
- **Using promotion as praise.** Promoting something because it feels like a compliment rather than because it's universal. Fix: apply the universality test with actual rigor.
- **Mixing staging and canonical.** Leaving promoted content in `memory/` after it's been added to `USER.md`. Canonicality violation. Fix: after promotion, clean up the staging area.

---

## 9. Canonicality Rules

*See Section 3.2 for the canonicality decision table. Canonicality is foundational enough that it lives in the architecture section, not as a back-of-book reference.*

---

## 10. Anti-patterns

*Anti-patterns are distributed across the per-layer sections in Section 4. See the "Anti-patterns" subsection inside each layer (4.1–4.8), plus `USER.md` anti-patterns in Section 5.8, instantiation mistakes in Section 6.6, and promotion anti-patterns in Section 8.8.*

---

## 11. Evolution Log

Append-only changelog for the framework itself. Newest entries at top. Never edit past entries.

Every change gets one entry: a date, a version number, and a short note. Changes include: new reflexes promoted to Section 7, reflexes deprecated, layer definitions revised, new sections added, sections merged or split, structural rewrites, location conventions changing (e.g., if `USER.md` moves from `~/thehub/` to `~/.claude/`).

---

### 2026-04-14 — v0.2.4 (skeleton walk + vault rehaul parked)

First end-to-end walk of `skeleton/` against the framework spec. Four fixes applied. One architectural question surfaced that is too large for this pass and has been parked for a dedicated future session.

**Skeleton fixes applied:**

1. **`skeleton/memory/MEMORY.md` moved out of the skeleton.** The v0.2.2 fix to Section 4.3 clarified that Claude Code auto-memory lives at `~/.claude/projects/{hub-path}/memory/`, not inside the hub directory itself. But `skeleton/memory/MEMORY.md` still existed — meaning a fresh `cp -r skeleton/ ~/thehub/newhub/` would create `~/thehub/newhub/memory/MEMORY.md` at the wrong physical location, contradicting the framework. The file's content (a template showing what a populated MEMORY.md index should look like) is valuable enough to preserve, so it was relocated to `hub-os/MEMORY.md.reference` with a reference-mode header explicitly telling readers not to copy it. README.md updated to reflect the new file.

2. **CLAUDE.md section order in Section 4.1 updated to match skeleton + chiefofstaff reality.** The framework prescribed `Identity → Working style → Mandate → Domain map → Routing table → Never list → Current status → Tools available → Session rituals` (session rituals at position 9, the bottom). The skeleton CLAUDE.md and chiefofstaff's real CLAUDE.md both place session rituals at position 3 (right after working style). The skeleton-and-real order is better: session rituals are foundational and need to be in the first screenful of the file, not buried at the bottom where they'll be skipped on quick reads. Updated Section 4.1 Files list and Minimum code block to put Session rituals at position 3 and added a one-line justification for the placement in the Files list.

3. **README.md version label updated** from v0.2.1 to v0.2.4.

4. **README.md "Source" paragraph rewritten.** The prior version said *"the first application of the framework back to chiefofstaff (2026-04-14) surfaced an R-008 violation inside the framework doc itself — see v0.2.1 in the evolution log for that story."* Same narrator-voice tone as the v0.2.1 "Proof of the living loop" bullet we rewrote in v0.2.3. Replaced with a factual one-line pointer to Section 11 for change history. Going-forward rule from v0.2.3 holds: facts stay, evaluation goes.

**Parked for a dedicated session — vault scope + Layer 4 conceptual framing:**

The skeleton walk surfaced an architectural contradiction: Section 3.1's scope table labels Layer 4 (vault) as `hub`-scoped, but the skeleton CLAUDE.md uses absolute `~/thehub/vault/` paths and describes the vault as *"shared across all this user's hubs."* Chiefofstaff's actual vault also lives at `~/Thehub/vault/`, not inside the chiefofstaff hub directory. The framework's stated scope and the reference implementation's real scope disagree.

In-session discussion with the user produced a deeper framing than the scope question itself. The user's intuition: **the vault is semantic memory; everything outside the vault is procedural/structural memory.** When you query `Black Rabbit Games` from the procedural layers (`OVERVIEW.md`, `CLAUDE.md`, `ops/`, `kanban/`), you get routing rules, state snapshots, and task mechanics — *how things hang together*. When you query it from the vault, you get concepts, manifesto, philosophy, the people in its orbit, the decisions that shaped it — *what the thing means*. These are two genuinely different kinds of recall, mapping onto the classical cognitive-science distinction between procedural memory (know-how) and semantic memory (know-what).

Under that framing, the scope question becomes downstream. Semantic memory about "Black Rabbit as an idea" is inherently user-scoped — the concept doesn't care which hub you're working in — so a shared `~/thehub/vault/` is the natural home and hub-scoped per-hub vaults fragment the graph and lose most of the value. But this is a Section 4.4 rewrite, not a drive-by fix: Layer 4 probably wants to be renamed (current: "Metacognition (Vault)"; candidate: "Semantic Memory" or "Knowledge Substrate"), Section 3.1's scope table needs updating, Section 4.4's retrieval test needs to be rewritten in terms of mechanics-vs-meaning, and the whole "what goes where" boundary between vault and outside-vault layers deserves to be re-derived from the procedural/semantic distinction rather than from the WHY/WHAT distinction currently in use.

Parked as a **planned v0.3.0 revision** with a dedicated session. See the corresponding note in the vault's `hot.md` Active Threads and the concept page `vault/wiki/lessons/Vault is semantic memory.md` filed in parallel with this entry.

---

### 2026-04-14 — v0.2.3 (judgment-call cleanup from second review pass)

Applied the four judgment-call findings that v0.2.2 deferred. Each is recorded here with the reasoning so the user can challenge any of them on a later pass.

1. **Section 7.2 reflex schema reformatted** — was a YAML block, but Section 7.4 renders entries as markdown tables, so the schema format didn't match the actual format of the thing it was describing. Rewrote 7.2 as a field list (not a YAML block, not a table) and added a closing note that the fields are rendered as markdown tables in 7.4. *Why this shape rather than converting 7.4 to YAML:* markdown tables are strictly more readable for humans reading the doc top-to-bottom, and nothing is parsing this file as structured data. The schema is descriptive, not executable. Decoupling the field definition from the rendering format keeps the schema abstract — a future change to how entries render in 7.4 doesn't require editing 7.2.

2. **Section 4.5 coordinator-delegation options collapsed from 3 to 2.** Options 1 ("coordinator performs the mutation under the specialist's direction") and 3 ("work is broken into read phase via subagent + write phase by coordinator") both placed the mutation on the coordinator post-approval — they were the same pattern with or without a read-phase subagent in front of it. Folded them into a single option 1 that names both variants. Option 2 (specialist runs as subprocess with its own credential environment) was left intact because it is the genuinely distinct alternative — it's the only path where mutation credentials actually exist outside the coordinator's context. *Why this matters:* three apparently-distinct options that are really two-plus-one is confusing when the reader is trying to implement the rule. Two genuinely distinct patterns are clearer than three overlapping ones.

3. **Section 4.1 archetype-selection rules 3 and 4 folded into one.** Rule 3 ("character contrast") and rule 4 ("respects but would disagree with") were the same idea approached from two angles — contrast necessarily implies occasional disagreement, and disagreement without contrast is just noise. Merged into a single rule that names both the contrast principle and the respect/disagreement test together. Renumbered rule 5 ("Write the fit") to rule 4. The archetype selection list now has 4 rules instead of 5. *Why collapse rather than keep both:* rule lists where two adjacent items cover the same ground make readers wonder what the distinction is, which wastes attention. A single rule that names both faces of the same principle is more load-bearing than two rules that feel almost-but-not-quite redundant.

4. **Section 11 v0.2.1 "Proof of the living loop" bullet rewritten in dry factual voice.** Was written in narrator voice — "confirms the loop closes," "three iterations of the same principle in 24 hours," "not aspirational anymore" — which broke the evolution-log tone the rest of the doc maintains (and that the v0.2.2 entry explicitly established). Replaced with a factual statement of what was found and what was done ("Section 4.4 was duplicating Section 4.8's session-end ritual content — an R-008 canonicality violation in the framework doc itself. Replaced with a pointer to Section 4.8."). *Why rewrite rather than delete:* the fact itself is worth preserving — the framework doc violated its own rule, it got caught, it got fixed. Deleting the bullet would erase a real event. Rewriting it lets the fact stay while removing the editorializing. *Judgment call explicitly not made:* I did not rewrite any other bullets in the v0.2.1 entry, even though some have mild narrator voice. The rule going forward is: facts stay, evaluation goes. Past entries are only edited when they have obvious tone violations; new entries are written in the dry voice from the start.

---

### 2026-04-14 — v0.2.2 (second review pass — residual fixes)

A second end-to-end read of the framework found four residual issues the v0.2.1 pass had missed:

1. **Section 4.3 still carried the wrong description of where `memory/` lives.** The v0.2.1 pass fixed Section 6.3 Step 5 (the instantiation how-to) but left Section 4.3 (the layer definition) saying `memory/` is "inside each hub directory" with a parenthetical self-contradicting that claim. Rewrote 4.3 to state the correct path (`~/.claude/projects/{hub-path}/memory/`) and to name the mangled-path-as-folder-name convention Claude Code uses to identify hubs. The fix-the-symptom-miss-the-cause pattern here is itself an R-008 lesson: a bad mental model duplicated across two sections only got fixed in one.
2. **Section 4.1 required-sections list was missing Session Rituals.** Section 4.8 explicitly requires a Session Rituals section in Layer 1 CLAUDE.md day-one, and Section 6.3 Step 10 confirms it, but Section 4.1 itself listed only 8 sections. Added Session Rituals as the 9th required section in both the Files sub-list and the Minimum code block, with a pointer to Section 4.8.
3. **Section 3.2 canonicality table row 5 used an ambiguous "or".** The row read `Layer 1 (never list) or Layer 6 (hook)` as if they were alternatives, contradicting Section 4.6's explicit statement that the declaration-and-enforcement split is deliberate. Rewrote to `Layer 1 declaration (never list) + Layer 6 enforcement (hook/architecture)`.
4. **Footer version label was stale.** Said `v0.2` while the header said `v0.2.1`. Updated footer to `v0.2.2` to match this entry's header.

Four additional findings from the same review pass are **deferred** pending user judgment — they involve restructuring content the user wrote and should not be auto-patched:
- Section 7.2 reflex schema declares YAML but Section 7.4 uses markdown tables (format inconsistency, not a correctness bug)
- Section 4.5 coordinator-delegation options 1 and 3 overlap (both place the mutation on the coordinator post-approval; could collapse to two options)
- Section 4.1 archetype-selection rules 3 and 4 both describe contrast/disagreement from slightly different angles (could fold into one rule)
- Section 11 v0.2.1 entry's "Proof of the living loop" bullet is written in narrator voice rather than the dry factual tone of the rest of the evolution log

---

### 2026-04-14 — v0.2.1 (review pass + first source-hub application)

- **Review pass** — read FRAMEWORK.md end-to-end and applied seven fixes:
  1. Section 4.3 grammar: "is a naive bot on day one, has to be re-taught" → "starts as a naive bot on day one and has to be re-taught".
  2. Section 3.3 visual diagram: L7/L8 box widths were mismatched (`Integration` 13 chars, `Cadence` 12 chars). Both widened to 15 chars so the boxes align.
  3. Section 4.4 "Rituals (owned by Layer 8)" was a **live R-008 violation** — it contained the session-end numbered ritual steps that are canonically declared in Section 4.8. Replaced the duplicate with a pointer, explicitly citing R-008. The framework doc now complies with its own canonicality rule.
  4. Section 6.3 Step 5 conflated Claude Code's auto-memory (`~/.claude/projects/{hub-path}/memory/`) with a fictitious in-hub `memory/` directory. Rewrote the step to explain that Layer 3 has two sub-locations with different lifecycles and that `memory/` is auto-created by Claude Code, not instantiation-time work.
  5. Section 3.4 Layer 5 row: "`ops/` folder with `_template/CLAUDE.md` reference" → "`ops/` folder containing `_template/CLAUDE.md`".
  6. Section 7.3 "minimum R-001 through R-004" was misleading — all eight reflexes are universal and day-one. Replaced with a safety-critical-core vs. operational-hygiene framing that tells instantiators to keep all eight unless the domain explicitly doesn't exercise one.
  7. Section 7.4 R-008 layer field: "All (meta-rule, governs the framework itself)" → "All (cross-cutting meta-rule)" for consistency with other entries' format.
- **First real application of the framework back to its source hub** (`chiefofstaff`). Two canonicality violations fixed: (1) session rituals duplicated across `CLAUDE.md` and `memory/MEMORY.md` → consolidated into a new `## Session Rituals` section in `CLAUDE.md` as the canonical home. (2) State-scoped "Open Questions" items living in `memory/MEMORY.md` with decaying countdowns → migrated to `OVERVIEW.md` per R-005. Full decision record at `~/thehub/vault/wiki/decisions/Memory canonicality fixes applied from hub-os framework.md`. Phase 2 of the source-hub cleanup (16 hub-scoped project entries still in `memory/MEMORY.md`) and Phase 3 (creating `USER.md` for real) are deferred.
- **Self-application of R-008.** Section 4.4 was duplicating Section 4.8's session-end ritual content — an R-008 canonicality violation in the framework doc itself. Replaced with a pointer to Section 4.8. Same rule surfaced during the v0.2 extraction; this pass applied it to the doc that defines it.
- **Skeleton scaffolded.** After the patch pass, the `hub-os/skeleton/` directory was created with all 13 canonical subdirectories and 16 template files populated from the framework spec: `README.md` (quick-start guide), `USER.md.template` (user-scoped anchor template with 6 canonical sections), `skeleton/CLAUDE.md` (Layer 1 coordinator template with all required sections, all 8 reflex-card entries pre-seeded in the never list), `skeleton/OVERVIEW.md` (4 canonical state sections), `skeleton/kanban/proposals/pending.yaml` (schema-documented empty array), `skeleton/vault/wiki/{hot,index,log}.md` (frontmatter-seeded stubs), 5 `.gitkeep` marker files in the empty vault subfolders (each documenting what belongs in its directory), `skeleton/ops/_template/CLAUDE.md` (per-role template), and `skeleton/memory/MEMORY.md` (Layer 3 staging-ground template with the canonicality rules and what-doesn't-belong-here section baked in). First external instantiation can now proceed by copying `skeleton/` to a new hub directory and filling slots from the interview.

---

### 2026-04-13 — v0.2 (initial snapshot)

- **Extracted from `chiefofstaff` hub.** First formal externalization of the hub pattern that had evolved inside chiefofstaff since 2026-03 and earlier.
- **8 layers defined** with "all layers always present, minimum vs. expansion" framing (replaced an earlier "3 required + 5 optional" draft that proved dishonest during the extraction — see notes below).
- **Canonicality rules folded into Section 3.2** rather than living in a back-of-book Section 9. The reference placeholder in Section 9 points forward.
- **Anti-patterns distributed** across per-layer sections rather than collected in Section 10. The reference placeholder in Section 10 points forward.
- **Reflex card seeded with 8 entries** (R-001 through R-008), all surfaced from `chiefofstaff` incidents:
  - R-001 through R-003 from the 2026-03-27 credential-bypass incident
  - R-004 as the meta-reflex governing enforcement discipline
  - R-005 and R-006 from operational drift observations
  - R-007 from the human-frame cost estimation feedback
  - R-008 surfaced *during* the extraction itself (the `chiefofstaff` `memory/MEMORY.md` was mixing user-scoped and hub-scoped content, and the canonicality rule needed to be explicit)
- **`USER.md` specification drafted in Section 5** with six canonical sections, a worked example for Gabriel's profile, and the provisional location `~/thehub/USER.md` (flagged for reflection).
- **Instantiation playbook drafted in Section 6** with 21 interview questions + 11 file-operation steps + day-one verification checklist.
- **Three-path promotion model drafted in Section 8** (memory → USER.md, memory → vault, hub → framework) with bar-scales-with-blast-radius principle.
- **Notes on the extraction itself:**
  - The "3 required + 5 optional" framing was explicitly dropped in favor of "8 always-present layers, each with minimum + expansion." The old framing was trying to honor Gall's Law but conflated "whether a layer exists" with "how developed it is." The organism metaphor (every hub has all the organs; some are rudimentary) is more accurate.
  - The never list moved from "appears when Layer 6 activates" to "required day-one, seeded from reflex card." Layer 6 is no longer optional at its minimum.
  - The reflex card upgraded from "reference material" to "load-bearing source of day-one Layer 6 content." Without it, new hubs start with empty never lists.
  - The `USER.md` / hub-scoped split is identified as the single biggest leverage point in the framework — the reason hub #2 can start smart.

---

*End of FRAMEWORK.md v0.2.4*
