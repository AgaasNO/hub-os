# hub-os

Framework for building **cognitive-operational hubs** — Claude Code projects that hold the full picture of a complex, multi-threaded domain of work and coordinate it without dropping context.

## What's in here

| Path | What it is |
|---|---|
| **`FRAMEWORK.md`** | The full specification. 8 layers, minimum implementations, reflex card, instantiation playbook, promotion rules. Start here if you want to understand *why*. |
| **`skeleton/`** | The copy-able directory structure for a new hub. Used during instantiation — see Section 6 of `FRAMEWORK.md`. |
| **`USER.md.template`** | Template for the user-scoped profile file. Copy to `~/thehub/USER.md` the first time you set up hub-os. See `FRAMEWORK.md` Section 5. |
| **`MEMORY.md.reference`** | Reference for what Claude Code's auto-memory index should contain. **Not** copied into your hub — Claude Code auto-creates `memory/MEMORY.md` at `~/.claude/projects/{hub-path}/` on first session. Read this only to understand what the file should look like. |
| **`README.md`** | This file — quick-start for using hub-os. |

## The golden rule of instantiation

**Do the interview before you touch files.** The failure mode hub-os is most vulnerable to is *cargo culting* — copying the skeleton, renaming the archetype, deleting the parts that look unfamiliar, and shipping. Cargo-culted hubs feel functional for a week and then collapse because the slots were filled without the reasoning that justifies the fillings.

Read `FRAMEWORK.md` Section 6.2 and answer the 21 interview questions in a live conversation with Claude *before* any file operation. The instantiation flow is mechanical after the interview; it is disastrous without it.

## Quick start — instantiating your first hub

1. **Read `FRAMEWORK.md` Section 1 (Preamble) and Section 3 (Architecture).** You need to understand the organism metaphor and the 8 layers before touching anything.
2. **Ensure `~/thehub/USER.md` exists.** If this is your first hub, copy `USER.md.template` to `~/thehub/USER.md` and populate at least sections 1 (Identity), 2 (Working style), and 6 (Scope note). The other three sections can start empty and grow under pressure (Section 5.3).
3. **Run the pre-instantiation interview** (`FRAMEWORK.md` Section 6.2) in a live Claude conversation. Answer all 21 questions. Save the answers.
4. **Copy the skeleton** to a new hub directory:
   ```bash
   cp -r hub-os/skeleton ~/thehub/{your-hub-name}
   ```
5. **Fill the slots** in the new hub's `CLAUDE.md` using your interview answers. Every `{slot_name}` placeholder gets replaced with real content.
6. **Run the day-one verification checklist** (`FRAMEWORK.md` Section 6.4). If any checkbox is no, fix it before the first session.
7. **Start your first session.** The coordinator reads `CLAUDE.md` (which imports `USER.md`) and runs the session-start ritual. Do one small piece of real work, file the first vault entry, reconcile `pending.yaml`, close the session.

## Instantiating hub #2 and beyond

The whole point of hub-os is that hubs after the first one start smart. The second hub inherits `USER.md` automatically — no re-teaching working style, decision lens, cross-hub preferences, or recurring people. Steps 2 and 3 above become much cheaper the second time around; the interview focuses on what's *different* about the new domain rather than re-establishing the user profile from scratch.

If you find yourself re-teaching Claude something that applied to the last hub, that's a signal the lesson should be promoted to `USER.md` (see `FRAMEWORK.md` Section 8 — promotion rules).

## Living framework

hub-os is a living document. Every time a real incident surfaces a rule that proves universal across domains, the rule gets promoted into `FRAMEWORK.md` Section 7 (reflex card). Every time a `USER.md` learning turns out to apply to every hub a user builds, it gets promoted into the user's anchor file. The framework compounds through use.

Current version: **v0.2.4** (2026-04-14). See `FRAMEWORK.md` Section 11 for the full evolution log.

## Source

hub-os was extracted 2026-04-13 from `chiefofstaff`, an e-commerce consulting hub that had evolved the pattern organically over weeks of real operational work. The framework is the pattern stripped of its ecommerce specifics. See `FRAMEWORK.md` Section 11 for the full change history.

The framework evolves as new hubs are built from it and new incidents produce new reflexes. Contributions flow one direction only: **up** (hub → `USER.md` → framework), per Section 8 promotion rules.
