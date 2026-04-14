---
type: index
title: "Vault Index"
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
tags: [meta, index]
---

# Vault Index

*Catalog of everything in this vault. Maintained as the vault grows. Read this when `hot.md` isn't enough but you don't yet know which specific page to drill into.*

## Decisions

*Every non-trivial call with its rationale and context. The WHY layer.*

_(empty on day one; populates as decisions are made and filed under `decisions/`)_

## Lessons

*Named reusable patterns extracted from experience. Each lesson has: what-it-is, when-safe, when-unsafe, how-to-apply.*

_(empty on day one; populates as patterns emerge and deserve a name)_

## People

*Domain actors — counterparties, collaborators, suppliers. Per-hub people live here. People who recur across all the user's hubs live in `~/thehub/USER.md` People section, not here.*

_(empty on day one; populates as domain actors enter the hub's world)_

## Projects

*Initiatives, ventures, ongoing work streams within this hub. Each has its own page with current state, history, and wikilinks to affected people and decisions.*

_(empty on day one; populates as initiatives cross from "task" to "project")_

## {counterparty_folder — clients / customers / collaborators / subjects}

*Agent-oriented briefs for each counterparty. Strategy, constraints, standing rules, cross-agent notes.*

_(empty on day one; populates when the domain has counterparties. Rename the folder per domain if needed — see FRAMEWORK.md Section 4.4 slots.)_

## Timeline archives

*Archived history from overflowing briefs. Created when a counterparty brief's Cross-Agent Notes section exceeds ~10 entries.*

_(empty on day one; populates via timeline rotation in session-end ritual)_

## How to add an entry

New file in the appropriate subfolder. Required frontmatter: `type`, `status`, `date`. Every non-trivial entry must wikilink to the people and projects it affects — without links the graph stays flat and the vault loses most of its value (FRAMEWORK.md Section 4.4, non-negotiable rule).
