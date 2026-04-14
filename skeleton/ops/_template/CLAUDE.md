# {Role Name} — {role_verb}

*Per-role operating spec for the `{role_slug}` specialist. Copy this template to `ops/{role-name}/CLAUDE.md` and fill every `{slot}` placeholder when adding a new role.*

*A specialist is a **mini-coordinator for a narrower domain**. Its job is to execute domain-specific work that the top-level coordinator refuses to do directly. It inherits identity and working style from the top-level `CLAUDE.md` and `~/thehub/USER.md` — does not duplicate them. Only what's narrow and specific to this role lives here.*

*Naming rule: roles are named after the **verb of their work**, not the tool they use. "Store Manager" not "Shopify Agent." "Translation Agent" not "Lokalise Integration." Tools change; verbs don't. See FRAMEWORK.md Section 4.5.*

---

## Mandate

*1–2 sentences: what this role does, and — just as important — what it doesn't do.*

{Replace with real mandate.}

---

## Tools

*Which external tools this role uses. Reference Layer 7 contracts in the top-level `CLAUDE.md` "Tools available" section. If a tool has quirks specific to how this role uses it, document here. Otherwise point at the canonical contract.*

- {tool — purpose for this role; cross-ref to Layer 7 contract if one exists}

---

## Credentialed surfaces

*What this role can mutate, and how credentials are structured. Read-default, write-approved per R-003.*

*If this role has no mutation capability, delete this section.*

*If this role has mutation capability:*

- **Read credentials:** load path, auto-loaded on session start. Cheap and safe.
- **Write credentials:** load path, explicitly loaded **only on user approval in the current session**. Never auto-loaded.
- **Write operations this role performs:** {list the kinds of mutations this role is allowed to do}
- **Approval gate:** {how the coordinator/user confirms write capability is appropriate for the specific mutation}

---

## Per-role never list

*Hard lines this specialist refuses to cross. Inherits the top-level never list from the hub's CLAUDE.md by default. Entries here are role-specific additions, not repetitions of the universal reflexes.*

- {populate as role-specific incidents surface — each entry references the incident that produced it}

---

## Context files

- **`CONTEXT.md`** — living context the top-level coordinator updates with cross-role signals. Populated when the coordinator dispatches this role and has signals worth passing down. Per R-006, ops context flows both directions — the coordinator reads from it *and* writes to it.
- **`decisions.md`** *(optional, create only when this role makes recurring decisions worth tracking per-role)* — per-role decision log.

---

## How this role is invoked

*How the top-level coordinator dispatches to this role. Typically via the routing table in the hub's top-level `CLAUDE.md`.*

- The coordinator's routing table must have an entry pointing at this directory. If it doesn't, this role is orphaned (FRAMEWORK.md Section 4.5 anti-pattern) and either (a) the routing table needs updating, or (b) this role should be deleted.
- The coordinator **never** dispatches this role with mutation credentials as prompt arguments (R-002). If this role needs write access, either the coordinator performs the mutation itself under this role's direction, or this role runs as a subprocess with its own credential environment.
