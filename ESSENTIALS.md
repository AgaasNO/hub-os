# hub-os — the essentials

*One page. Most people need only this. [`FRAMEWORK.md`](FRAMEWORK.md) is the reference: look things up in it, don't read it cover to cover.*

## What a hub is

A Claude Code project that holds the full picture of one domain of work and keeps it straight across sessions. **Claude without a hub is a bot; Claude with a hub is a system.** A bot answers the current message. A hub knows what's live, remembers why decisions were made, enforces its own rules, and ends each session slightly more organised than it started.

## The 8 layers

Every hub has all eight from day one. Depth varies; none are optional.

| # | Layer | Lives in | Holds |
|---|---|---|---|
| 1 | Coordinator | `CLAUDE.md` | Archetype, mandate, routing table, never list |
| 2 | State | `OVERVIEW.md`, `kanban/` | What is true *now*. Overwritten, never appended |
| 3 | Auto-memory | `~/thehub/USER.md`, `memory/` | How *you* work, shared by every hub you build |
| 4 | Vault | `~/thehub/vault/wiki/` | What things *mean*: decisions with reasons, named lessons, people. One vault per user |
| 5 | Ops | `ops/{role}/` | Named specialists the coordinator routes work to |
| 6 | Safety | never list, hooks, split credentials | What the coordinator cannot do, enforced |
| 7 | Integration | "Tools available" in `CLAUDE.md` | External tools and their quirks |
| 8 | Cadence | rituals in `CLAUDE.md` + a session-start hook | When things happen |

**Where does something go?** Ask *"am I storing mechanics or meaning?"* Mechanics (state, rules, routing, schedules) go in layers 1–3 and 5–8. Meaning (why, what it's called, who someone is) goes in layer 4. Every fact has exactly one home.

## The rules that matter most

1. **The coordinator routes; it does not execute.** Specialist work goes to the specialist that carries the safety rules for it. (R-001)
2. **Never hand a subagent write credentials.** Reads load by default; writes need approval each session. (R-002, R-003)
3. **Critical rules are hooks, not sentences.** If breaking a rule would be an incident, a hook enforces it. When an instruction gets skipped, replace it with a mechanism; another instruction won't fix it. (R-004, R-009)
4. **State is overwrite-only.** History goes to `vault/wiki/log.md`, and resolved proposals leave the queue. (R-005)
5. **Measure the queue's shape, not its size.** Watch for a queue that feeds itself (open rows citing other rows) and for high-priority rows going stale. The skeleton's hook does both. (R-011)
6. **Instruments must not fail silently in the reassuring direction.** A check that can only be wrong toward "all clear" will never be corrected. (R-010)
7. **Every vault entry links every person and project it touches.** An unlinked note is invisible.
8. **Estimate agent cost, not human fatigue.** Tokens, tool calls, context, credentials. Agents don't get tired. (R-007)

Peers sit *beside* the coordinator rather than under it: audit, design, research, writing. They take direction from you, because a function that judges the coordinator's work can't be directed by it. See FRAMEWORK §4.5.

## Your first hub

1. Fill in `USER.md.template` → `~/thehub/USER.md`: at least *Identity*, *Working style*, *Scope note*.
2. **Do the interview before you touch any files.** Answer the 21 questions in FRAMEWORK §6.2 in a live conversation with Claude. Copying the skeleton without the interview gives you a hub that feels fine for a week and then falls apart.
3. `cp -r hub-os/skeleton ~/thehub/<your-hub>`. This includes `.claude/`, which holds the session-start hook. Fill in every `{slot}` in `CLAUDE.md`. For the **vault**: on your first hub, move the copied `vault/` to `~/thehub/vault/`; on later hubs, delete it. There is one vault per user.
4. Save the interview as `INSTANTIATION.md`, ending with a **Deviations** section: where you knowingly broke from the framework, and why.
5. Check: `python .claude/hooks/session-start.py` prints `{}` (needs `pip install pyyaml`). Then run the FRAMEWORK §6.4 checklist.
6. First session: one small piece of real work, one vault entry, reconcile `pending.yaml`, close.

Expect about an hour of reading (this page, then FRAMEWORK §1, §3 and §6.2), 1–2 hours for the interview, and 30 minutes to set up.

## When you go deeper

- A layer is starting to strain → FRAMEWORK §4.x for that layer, especially its *Anti-patterns*
- The vault feels like a filing cabinet → [`SEMANTIC-OPERATIONS.md`](SEMANTIC-OPERATIONS.md)
- You're running three or more hubs → FRAMEWORK §3.6
- Something broke and you wrote a rule for it → FRAMEWORK §8 (promotion)

## If something confuses you

Write down what you were trying to do and where you got stuck, and send it back. **Friction reports from people new to the framework are the most valuable input it can get.** So far every version has been checked only by its author's own hubs.
