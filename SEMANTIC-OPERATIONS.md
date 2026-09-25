# The six semantic operations

*Companion to `FRAMEWORK.md` Section 4.4. The framework states the rule; this file is the full procedure. You don't need it on day one. Read it when the vault is big enough that a stale neighbourhood starts misleading decisions.*

*Wikilinks such as `[[The filing cabinet pattern]]` refer to lesson nodes in the source hub's vault. They're kept so the examples read naturally, but those nodes aren't part of this repo.*

## At a glance

Wikilinks give a vault a graph. They don't make it behave like memory. A vault where notes get written and occasionally opened is a **filing cabinet with cross-references**: it stores meaning but never retrieves it at the moment it would change a decision. What turns storage into memory is six named operations, each built only from primitives a coordinator already has (Read, Glob, Grep, frontmatter parsing, following wikilinks). No database, no embeddings, no extra tooling.

| # | Operation | Family | Trigger | What it does |
|---|---|---|---|---|
| 1 | **Primary consolidation** | write | session end, when a claim survived the session | Turns an episode into a node. Split the session into claims and apply the **observer-swap test** to each: strip the first-person perspective. If the meaning survives, it is procedural and belongs outside the vault; if it does not, it is semantic and belongs in it. Title gate: if you can't write a concrete one-line title, the insight isn't ready yet. |
| 2 | **Integration** | write | right after #1, in the same commit | Writes the *inbound* edges: every node the new one links to gets a back-reference. **Integration is what upgrades references to edges.** A link that resolves in only one direction is a reference, not an edge. Dead links are fixed on the spot: repoint or remove, never stub. |
| 3 | **Re-consolidation** | write | integration escalates; a drift report; a stale framing noticed mid-session | Updates an existing node whose neighbourhood has moved. **Re-consolidation is constitutional interpretation, not editing.** The original body is preserved; the update goes in as a dated callout at the top. Never run it for polish. At most one cascade per session. |
| 4 | **Priming** | read | session start, once | Loads the baseline frame: CLAUDE.md, auto-memory, `OVERVIEW.md`, `hot.md`. Then checks whether the user's opening message is a continuation or a pivot, and re-primes on a pivot. Priming's failure mode is not absence, it is **confirmation bias**: the loaded frame gets applied to a topic it doesn't fit. |
| 5 | **Pattern surfacing** | read | session end if budget remains (walk the clusters touched); on demand | Walks several nodes looking for what exists in the aggregate but has no node of its own. **Find the question the cluster answers, then check whether that question has a node.** Output is a report in `kanban/reports/`, never a vault node. |
| 6 | **Activation** | read | a `[[wikilink]]` or a named concept enters the conversation | Loads the comprehension frame around a concept: the node, its contrastive neighbours in full, its co-occurring neighbours in summary, two hops at most. Seed from the most specific node that covers the need, not the densest hub. It also watches for concepts the loaded frame can't reach. **Activation's value includes detecting absence of coverage, not just loading existing coverage.** |

**Adoption, honestly.** In the source hub, the writes (#1, #2) and priming (#4) run most sessions. Pattern surfacing and activation run far less often than designed, because nothing triggers them mechanically, which is the same gap `FRAMEWORK.md` Section 4.8 addresses for rituals. Start with #1, #2 and #4. Add the others when the vault is big enough to need them.

---

## The framework in one paragraph

Semantic operations split into two families: **reads** (the graph is the source — activation, priming, pattern surfacing) and **writes** (the graph is the destination — primary consolidation, integration, re-consolidation). Each family has three operations with distinct triggers, ritual steps, and failure modes. Reads consume what writes produce; writes carry the schema that reads later depend on. Running the six together produces a vault that behaves as semantic memory rather than as a filing cabinet with cross-references. Running any subset degrades the whole proportionally.

## Theoretical substrate

The ritual designs draw from five independent traditions, all of which converge on the same shape when applied to this problem:

- **Fillmore's frame semantics (1977–1982)** — a concept's "neighborhood" is the frame required to comprehend it in context, bounded semantically not topologically. Activation's comprehension-frame target comes from here. Fillmore's observation that "words specify a perspective from which the frame is viewed" independently derives the observer-swap test — same finding in a different tradition.
- **Collins & Loftus spreading activation (1975)** — activation decays with distance, divides at branch points, peripheral seeds beat hub seeds. The propagation mechanics for activation (one-hop strong, two-hop attenuated, three-hop noise) come from here. The counterintuitive insight — densely connected nodes are *bad* activation seeds because activation dilutes across too many paths — is this tradition's most actionable contribution.
- **Saussure's paradigmatic/syntagmatic distinction** — edges come in two types: co-occurrence (syntagmatic) and contrast-in-same-slot (paradigmatic). The schema's `relation` field and the weighted-frame loading in activation come from here.
- **Lakoff's conceptual metaphor** — abstract concepts are compiled residues of concrete experience. Informs the concept-node body shape that primary consolidation uses for nodes like `[[delegation]]`, `[[trust]]`, `[[compounding]]`, distinct from lesson or decision shapes.
- **Semantic satiation** — over-familiar priming content saturates over repeated reads. Justifies hot.md's delta-over-baseline curation.

The convergence across three traditions (cognitive science, linguistics, empirical psychology) is the strongest signal that the design is tracking something real rather than a local rationalization. Other hubs instantiating this framework should land on approximately the same shape.

---

## Operation 1: Primary consolidation (write)

**Framing.** Writing a new node FROM an episode. Output: a new semantic node with its initial edges and pass-1 metadata. Input: a session experience containing at least one claim that fails the observer-swap test.

**Trigger.**
- Primary: session end, when real work happened and produced a semantic claim.
- Secondary: mid-session when an insight crystallizes hard enough to risk loss if deferred.
- Explicit: "file this" from the user.

**Ritual steps.**
1. **Enumerate candidate claims** from the session. Think at the claim level, not the document level.
2. **Observer-swap each candidate.** Strip first-person perspective; if meaning survives → procedural (goes to OVERVIEW.md / kanban / hot.md); if meaning doesn't survive → semantic (candidate for vault).
3. **Cluster by coherence of framing, not by temporal co-occurrence.** Multiple semantic claims may belong in one node (coherent framing) or several (distinct concepts).
4. **One-line title gate.** If you can't write a concrete title in one line, the insight isn't crystallized — park in `log.md` and keep thinking. Vague titles produce thin nodes.
5. **Draft body using standard shape:** *What it is / Why it matters / When safe to apply / When unsafe / Origin / Related.* Concept nodes use a different shape per Lakoff: *Origin instances / Shared pattern / Predictions / Contrast*.
6. **Articulate every wikilink in prose.** No bare-link footnotes. The surrounding sentence must explain why the linked node is relevant here.
7. **Frontmatter with pass-1 `semantic_neighbors` from day one** (see Schema below). Non-negotiable. A node without `semantic_neighbors` is incomplete and must not be committed.
8. **File to the right sub-folder:** `decisions/`, `lessons/`, `people/`, `projects/`, `clients/`. Filename matches title; must be globally unique (Obsidian wikilink resolution is filename-based).
9. **Append to `log.md`** — newest at top, one line per new node with `[[wikilink]]`.

**Procedural primitives.** Read (confirm neighbors exist before linking), Write (file node), Edit (append log.md).

**Failure modes.**
1. Observer-swap skipped or applied at document level → mixed-content nodes. Prevention: step 2 non-skippable, applied per claim.
2. Bare wikilinks without articulation → edges without content, graph with no semantic weight. Prevention: step 6 as write-time gate.
3. Over-filing → thin nodes, filing cabinet on the filing process itself. Prevention: step 4's one-line title gate.
4. Missing pass-1 metadata → forces retroactive reconstruction later, degrades re-consolidation. Prevention: step 7 as hard contract.
5. Temporal clustering over semantic clustering → unfocused nodes forced together because they happened in the same session. Prevention: step 3's coherence test.

**Worked example.** The 2026-04-14 phase 3 session produced the original version of this spec plus a paradigmatic cluster of lessons earlier in the day (`[[Procedural and semantic — two axes]]`, `[[The filing cabinet pattern]]`, and a sibling lesson from the same session about mixed content types — parked tension, not included here). Audit scores (B+/C/F/D-) survived observer-swap → procedural → stayed in conversation. The content/operations split, the observer-swap test, the filing cabinet diagnosis, and the mixed-content-types tension all failed the swap → semantic → filed. Four semantic claims clustered by the coherence test (root theory + diagnosis + parked tension). Each filed node carries pass-1 `semantic_neighbors`. All wikilinks are articulated in body prose.

---

## Operation 2: Integration (write)

**Framing.** Integration is what upgrades references to edges. Primary consolidation writes the new node's outbound edges from the new node's perspective; integration writes the existing graph's inbound edges to the new node from the graph's perspective. Same write event, two halves. A wikilink that only resolves in one direction is a reference; an edge is bidirectional by construction. Integration is the ritual that upgrades references to edges.

**Trigger.**
- Primary: immediately after primary consolidation on a new node, within the same session, before commit. Never standalone.
- Secondary: when an existing node gets a substantive body edit (not a typo or metadata-only change).
- Not a trigger: stale-graph sweeps for missed back-references — that's pattern surfacing's job.

**Ritual steps.**
1. **Walk every wikilink in the new node.** For each `[[X]]`: does `X.md` exist? Glob `vault/**/*.md` to resolve. If no → dead link. Two options only: rewrite the reference to an existing node that covers the same concept, or remove the reference. **Stubs are forbidden.** "File for later" produces filing-cabinet thin nodes. If neither rewrite nor removal works, file the real node now.
2. **Bidirectionality check.** For each live target X: does X's body or `semantic_neighbors` reference the new node? If yes → skip. If no → the edge is currently unidirectional. Go to step 3.
3. **Classify the back-reference update: integration or escalation?**
   - **Integration (lightweight, usually syntagmatic)** — add the new node to X's `semantic_neighbors` as a pass-N entry with `type: integration`. Body unchanged. The edge is load-bearing for meaning but doesn't require X's prose to change.
   - **Escalation to re-consolidation (usually paradigmatic)** — if X's body needs updating because the new node changes how X reads, stop and escalate to operation #3. Don't rewrite X's body under the integration label.
   - **Decision rule:** can X be read front-to-back without the new node and still make sense? Integration. Does reading X without the new node now feel misleading? Re-consolidation.
4. **Spot cross-cluster bridges.** If the new node links to nodes in two previously disconnected clusters, record the bridge in the new node's `Related` section as one sentence. Bridges are rare and high-information.
5. **Dead-link sweep.** Grep the new node for `\[\[.*?\]\]` patterns in the final state, verify each resolves. Catches typos and case mismatches.
6. **Single commit.** Primary consolidation + integration ship as one atomic commit. Never split — committing a new node without its back-references leaves the graph inconsistent between sessions, and a read from that interval forms wrong assumptions.

**Procedural primitives.** Glob (`vault/**/*.md`), Read, Grep (`\[\[NewNodeName\]\]` to find organic back-references), Edit (update `semantic_neighbors` on existing nodes), frontmatter parse.

**Failure modes.**
1. Unidirectional edges → graph walks backward miss the new node entirely. Prevention: steps 2–3.
2. Silent dead links → discovered at audit instead of write time. Prevention: step 1 as write-time gate.
3. Over-integration → every link gets a back-reference entry, frontmatter noise weakens signal. Prevention: step 3's load-bearing test. If integration entries happen on every outbound link, the threshold is wrong.
4. Integration/re-consolidation confusion → ad-hoc body rewrites under the integration label bypass mutation-with-evidence. Prevention: step 3's decision rule; when in doubt, escalate.
5. Split commits → graph inconsistent in the interval between partial writes. Prevention: step 6 as hard rule.

**Worked example.** Filing `[[Procedural and semantic — two axes]]` (PSA) on 2026-04-14. Step 1: three wikilinks, all eventually resolvable in the same commit (the filing cabinet pattern node was filed immediately after PSA in the same session, closing the transient dead-link window before step 5). Step 2 on `[[Vault is semantic memory]]`: unidirectional. Step 3: VISM's body needs a callout because the two-axis framing now extends its content-layer thesis. Escalate to re-consolidation. Step 4: no cross-cluster bridge (all within the vault-metacognition cluster). Step 5–6: all three of the day's lessons shipped as one commit with their back-references.

---

## Operation 3: Re-consolidation (write)

**Framing.** Re-consolidation is constitutional interpretation, not editing. When an existing node's framing is stale relative to its current neighborhood, re-consolidation adds authoritative interpretation that coexists with the original text rather than replacing it. The cardinal rule is **mutation with evidence**: original content is preserved; updates are overlays. Think append-only memory, not mutable state.

**Trigger.**
- **Integration escalation** (hard, automatic) — operation #2's step 3 classifies a back-reference update as needing body changes.
- **Pattern-surfacing output** (periodic, deferred) — operation #5 flags drifted nodes for re-consolidation.
- **Reactive read** (opportunistic, soft) — mid-session notice that an old framing feels stale.
- Not a trigger: scheduled time-based re-reads. Re-consolidation is context-shift-driven, not time-driven.

**Ritual steps.**
1. **Identify candidate and trigger.** Log which trigger fired — it carries different prior evidence (integration-escalation has a specific new node driving it; pattern-surfacing has a drift report; reactive has only intuition).
2. **Read candidate fully + all passes + follow every wikilink in the body to read neighbors' current state.** Cannot re-consolidate without reading the current neighborhood — the whole point is the neighborhood has shifted.
3. **Diff framing: original thesis vs current understanding.** What holds, what's incomplete, what's misleading. Pure thinking step, no artifact — output is an internal diff surfaced to the user before any write.
4. **Classify update type:**
   - **Extension** — original thesis still holds; new context adds nuance. Most common.
   - **Refinement** — original slightly wrong, needs narrowing. Callout marks the narrowing.
   - **Supersession** — original wrong, replaced by a new node. Frontmatter `status: deprecated`, deprecation callout pointing at the replacement, body preserved as historical record.
   - **Polish** — minor wording improvements without semantic change. **Hard rule: re-consolidation does not run for polish.** Stop. Polish is deferred entirely or happens opportunistically during primary consolidation of an adjacent write.
5. **Write overlay — callout at top of body:**
   ```markdown
   > [!note] Refined YYYY-MM-DD
   > [One paragraph: what changed, why, which nodes drove the refinement. Wikilinks articulated in prose, same discipline as primary consolidation step 6.]
   ```
   The original body is preserved **unchanged** beneath the callout. Callout is the only content re-consolidation produces. A reader can scroll past the callout and read the original in its entirety.
6. **Append a new pass entry to `semantic_neighbors`.** Passes are append-only. Old passes never change. Entries usually carry `paradigmatic` relation (the new context typically changes contrast space — that's why re-consolidation fired rather than integration). The `note` field is **mandatory** for `type: re-consolidation`: a pass without a note is a pass without evidence.
7. **Re-run integration on the callout's wikilinks.** The callout introduces new wikilinks. Walk them, resolve, check bidirectionality, possibly escalate. Re-consolidation can recursively trigger more re-consolidation.
8. **Recursion bound: at most one cascade per session.** Further cascades are deferred to future sessions (logged as candidates, not processed). Preserves single-commit invariant and prevents runaway walks. One is the minimum bound that still preserves graph consistency with the immediately-adjacent node.
9. **Single commit.** Candidate + callout + pass entry + any cascaded re-consolidation + any integration updates ship as one atomic commit.

**Procedural primitives.** Read (candidate + full neighborhood), Glob, Grep (find related content for diff step), Edit (callout + pass entry), frontmatter parse. No Write — re-consolidation never creates new nodes. Supersession produces two operations: primary consolidation of the replacement + re-consolidation of the original to mark supersession.

**Failure modes.**
1. Silent rewrite of original content → lost history, future readers can't see original claim. Prevention: step 5's "callout is the only content" rule. Body text below the callout is frozen.
2. Polish masquerading as re-consolidation → budget spent on cosmetics, filing cabinet operating on the re-consolidation process itself. Prevention: step 4's polish rejection as hard gate.
3. Cascading re-consolidation walking the whole vault → session runs out before converging. Prevention: step 8's explicit recursion bound.
4. Premature triggering on still-unstable new context → stale callout that itself needs re-consolidation later. Prevention: re-consolidation runs late — either at session end or on integration escalation, never mid-session on speculative framings.
5. Overlay accumulation degrading readability → museum problem, the node becomes unreadable as callouts stack. Prevention: **supersession escape valve** — when overlays accumulate past roughly two passes without convergence, the next re-consolidation produces a new node that supersedes the old. Readability is the judgment test, not a mechanical threshold. The old stays as `status: deprecated` with full history visible; the new carries the current framing at pass 1.

**Worked example.** The 2026-04-14 VISM pass-2 is the reference instance. Trigger: integration escalation from PSA. Step 3 diff: original thesis ("vault is semantic memory") holds; what changed is that "procedural" was doing double duty and the content-layer framing needed a second axis. Step 4: extension (not refinement, not supersession, not polish). Step 5: callout `> [!note] Refined 2026-04-14 (later same day)` added at the top of VISM's body; original content preserved unchanged beneath. Step 6: pass-2 entry type `re-consolidation` with mandatory note present. Neighbors labeled — carry-over edges from pass 1 stayed `syntagmatic`, new edges (PSA, FCP) labeled `paradigmatic` because they genuinely change the contrast space VISM sits in. Note that pass-2 was originally written in cumulative form (including carry-over nodes); going forward passes encode delta only (just what's new or changed at that pass). The cumulative-form artifact is preserved as visible historical evidence of the schema's evolution — editing it would violate the append-only invariant. Step 7–8: no cascade. Step 9: single commit.

---

## Operation 4: Priming (read)

**Framing.** The baseline frame loaded ahead of any specific input. Determines which concepts feel relevant at turn 1, before any deliberate fetching. Priming's failure mode is not absence — it's bias toward confirming what's already loaded. The same mechanism that makes pattern recognition work also drives confirmation bias. The fix is not weaker priming; it's explicit pivot detection, external correction channels, and delta-over-baseline curation.

**Trigger.**
- Primary: session start, exactly once, before first substantive exchange.
- Secondary: mid-session re-priming when evidence falsifies a core assumption (rare, distinct from adding nuance — falsification, not refinement).
- Not a trigger: turn-by-turn reload. Priming is baseline, not continuous. Reloading priming every turn would destroy its function.

**Ritual steps.**
1. **Static priming load in parallel:** CLAUDE.md (Claude Code built-in), MEMORY.md (Claude Code auto-memory), OVERVIEW.md, `hot.md`. This is the baseline layer.
2. **Pivot detection on the opening input.** After the user's first substantive message, classify: continuation of hot.md's threads, pivot to a different topic, or genuinely ambiguous. Most openings are obviously one or the other; the failure is skipping the classification step, not the classification being hard.
3. **Dynamic re-prime on pivot.** If pivot: identify the cluster the opening is about, load its canonical entry points (client brief / project page / lesson root), read top 5–10 `log.md` entries for recent activity in the pivot cluster, explicitly reset the active framing.
4. **Bias-correction checkpoint (named but light).** Single question: *"Is there a frame I'm holding from priming that might not fit the current topic?"* Answer honestly, update or confirm. **The heavy lifting is not done by this step.** It's done by the external correction channels — the user in conversation, and gap detection running inside activation. Step 4 is a named moment where the frame is explicitly examined rather than implicitly assumed; it's a lower bar than "catch all bias" but a higher bar than "no examination at all."

**Hot.md curation discipline** (the write side of priming; the rules hot.md must follow at session-end write time):
- **~500 word budget.** Enforces selectivity. Not a summary; a priming layer.
- **At least 2–3 active threads**, not just the dominant one. Pivot safety — a single-thread hot.md leaves the next session brittle against pivots.
- **Hot.md reports, doesn't predict.** The NEXT SESSION PRIORITY pointer is explicitly *likely*, not guaranteed.
- **Lean on delta (what changed) over baseline (what's ongoing).** Stable content saturates over repeated reads per semantic satiation; delta content stays sharp.
- **Preserve paradigmatic relations more aggressively than syntagmatic during trim.** Syntagmatic co-occurrences saturate, paradigmatic contrasts don't — the differences between alternatives keep their edge.

**Procedural primitives.** Read (the four priming sources + pivot re-prime), Glob (cluster entry points), Grep (rare).

**Failure modes.**
1. Pivot blindness → opening topic misframed through hot.md's loaded cluster. Prevention: step 2 non-skippable.
2. Single-thread hot.md → no pivot safety. Prevention: curation rule 2.
3. Confirmation bias operating silently → notice only what confirms loaded frame. Prevention: step 4 + external correction (user + gap detection).
4. Stale hot.md → primes from days ago. Prevention: session-end discipline (primary consolidation step 9 equivalent).
5. Over-priming on procedural detail → biases toward procedural framing. Prevention: 500-word budget; ties go to semantic.

**Worked example.** The 2026-04-14 phase 3 session's opening. Read OVERVIEW.md + hot.md in parallel at turn 0. Hot.md primed for "phase 3 vault rewrite." User opening message ("hello there should be a handoff since i just cleared context") confirmed continuation — no pivot. No dynamic re-prime needed. Mid-session, the Obsidian frame was falsified (plugin turned out to be a Claude Code extension, not an Obsidian plugin). Secondary re-prime triggered at low cost because the falsification was sub-framework — one claim within the session, not topic replacement. The phase 3 framing stayed intact; only the "what caused phantom stubs" sub-frame got replaced.

---

## Operation 5: Pattern surfacing (read)

**Framing.** Walks across multiple nodes looking for things that exist in the aggregate but aren't named in any single node. Produces two output classes from the same walk: emergent structure (→ primary consolidation) and drift signals (→ re-consolidation). The only semantic-read operation that walks the graph cross-cluster under normal conditions. Re-consolidation's candidate-selection ceiling is set by pattern surfacing's quality.

**Trigger.**
- **Post-write session-end** (opportunistic, cluster-scoped) — after primary consolidation ships at session end, if session budget remains, walk the cluster(s) touched during the session. **This is the primary adoption path.** Ties discovery to the work that just happened, when evidence is warm.
- **On-demand** — user-initiated: "walk the [cluster] cluster and look for drift."
- **Scheduled full vault** — natural breakpoints only (framework revisions, major refactors), not calendar-driven. Monthly is aspirational; in practice these run when a session has dedicated budget.

**Three scope types:**
- **Cluster walk** (5–15 nodes) — typical post-write scan. 2–5 flags output.
- **Targeted walk** (variable) — on-demand, specific question. 1–10 flags.
- **Full vault walk** (50+ nodes) — rare. 10–50 flags. Dispatch parallel sub-walks via Agent subagents per sub-folder to avoid loading the entire vault into one context.

Below 5 nodes, emergent-pattern classification is skipped — patterns need ~5+ related nodes to be visible. Tiny walks still run the other discovery categories.

**Ritual steps.**
1. **Choose walk scope and type.** For post-write session-end: scope = cluster(s) containing nodes written or edited during the session.
2. **Load the scope.** Glob `vault/wiki/<sub>/**/*.md`, Read each node fully. **For cluster walks, seed from peripheral nodes (fewest outbound links in the cluster) and walk inward toward hubs.** Per Collins-Loftus, dense hubs are poor seeds — activation dilutes across too many paths. Pattern recognition is sharper from the periphery.
3. **Graph walk inside scope.** For each node: outbound wikilinks, union of all `semantic_neighbors` pass.nodes, bidirectional state of each outbound link, dead links.
4. **Cross-text scan with four targets:**
   - **Drift signal** — diff the body's current wikilinks against the union of pass.nodes across all passes. If more than ~30% of current body wikilinks are missing from pass history → re-consolidation candidate. Catches metadata lagging behind text.
   - **Gap detection (audit-time variant)** — Grep the whole vault for each node's title *without* wikilink brackets. Finds organic mentions that should be edges. **Same mechanism as activation's live-stream gap detection, different substrate (written text vs. live conversation).** Catches text lagging behind semantic reality. Output: each hit is a surprise signal — either missing edge (integration candidate) or missing concept (primary consolidation candidate if cluster-wide).
   - **Paradigmatic cluster detection** (Saussure-informed) — walk the scope for 3+ nodes occupying similar semantic slots but answering differently. **Mechanical criterion: find the question the cluster appears to be answering, then check if that question is itself named by a node in the cluster.** If not, the question is the candidate for a new concept or lesson node. This is the operational replacement for the vague "look for structure."
   - **Vocabulary shifts** — search for pairs of terms that name the same concept under old/new framings.
5. **Classify each discovery into one of six categories:**
   - **Emergent pattern (paradigmatic cluster)** — N nodes answer similar questions differently, contrast space unnamed. Consumer: primary consolidation.
   - **Re-consolidation candidate (drift)** — metadata lags behind text. Consumer: operation #3.
   - **Integration candidate (gap)** — text acknowledges an edge that doesn't formally exist. Consumer: operation #2 at next touch.
   - **Dead-link cleanup** — wikilink resolves to nothing. Consumer: operation #2 step 1.
   - **Duplication** — same entity at two paths. Usually parked for framework revision.
   - **Framing drift** — vocabulary mismatch with current cluster framing. Consumer: operation #3 as extension or refinement.

   Severity ordering: paradigmatic cluster + drift + duplication are high (structural). Gap + framing drift are medium (write-time fixable). Dead-link cleanup is low (cosmetic).
6. **Write the report to `kanban/reports/pattern-surface-<YYYY-MM-DD>-<scope>.md`.** The report is a **procedural artifact, not a vault node.** Observer-swap: the flags themselves survive first-person swap → procedural → outside vault. Filing reports as vault nodes would be the filing cabinet pattern operating on the discovery process itself. **Step 6 is not optional even when discoveries flow directly into step 7** — the report is the persistent record; the handoff is volatile consumption.
7. **Hand off to consumers.** The report is input to subsequent write operations, usually in a future session. Emergent pattern → primary consolidation. Drift candidate → re-consolidation. Gap → integration at next touch. Etc.
8. **Report decay.** Reports age out after consumers process them. Status: `open` → `in-progress` → `consumed` → `archived`. Kanban discipline, not vault discipline.

**Procedural primitives.** Glob, Read (heavy), Grep (heavy for cross-text scan), frontmatter parse, Agent dispatch for full vault walks.

**Failure modes.**
1. Never runs → the dominant failure. Prevention: post-write session-end trigger is the load-bearing adoption path. At 30–50% adoption it's still infinitely better than 0%.
2. Noise flood from wide walks → unacted reports. Prevention: step 5 severity ordering + step 7 explicit handoff.
3. Drift threshold too loose or tight → over-flagging or missed drift. Prevention: start at 30%, tune empirically from first 2–3 real walks.
4. Emergent-pattern filed without primary consolidation rigor. Prevention: step 5 produces *candidates*, filing happens under operation #1's discipline.
5. Reports filed as vault nodes → observer-swap failure on the output artifact. Prevention: step 6 hard rule.
6. Legacy nodes without `semantic_neighbors` can't be drift-detected mechanically → fallback to subjective signals. Bootstrap cost, not flaw. As legacy nodes get re-consolidated they acquire pass history.
7. **Step 6 skipped because discoveries flow directly into step 7** (observed retroactively in the 2026-04-14 audit — the session produced three lessons without writing a pattern-surface report). Prevention: discipline rule that step 6 is never optional.

**Worked example.** The 2026-04-14 vault audit was a full vault walk. Output: a paradigmatic cluster of emergent patterns filed as lessons (`[[Procedural and semantic — two axes]]`, `[[The filing cabinet pattern]]`, and a sibling lesson about mixed content types — parked tension, not included here), ~30 dead-link flags (mostly missing agent-as-character pages), 1 duplication flag (`projects/X` + `clients/X` for several entities) that the folder taxonomy was creating, multiple vocabulary drifts ("procedural" double-duty). Step 6 was skipped — discoveries flowed directly to filing — which is itself a ritual-design lesson: write the report even when the next action feels more productive than documentation.

---

## Operation 6: Activation (read)

**Framing.** Surfaces the comprehension frame of a concept when that concept becomes relevant mid-session. Reactive, not preloaded. Consumes what primary consolidation, integration, and re-consolidation produce. The most downstream operation — its quality is bounded by the rigor of every upstream operation. Activation is where the loop closes: where the vault's semantic content finally becomes semantic memory rather than semantic storage.

Fillmore defines the goal: neighborhoods are bounded by comprehension, not topology. Collins-Loftus defines propagation: one-hop strong, two-hop attenuated, three-hop noise; peripheral seeds beat hub seeds. Saussure defines edge weighting: paradigmatic neighbors load full, syntagmatic load summary.

**Trigger.**
- **Wikilink encounter** (hard, automatic) — every `[[X]]` in the main body text of current input fires activation on X unless X is already in the active frame. `Related` section wikilinks are indexes, not comprehension triggers — available for explicit manual activation but don't auto-fire.
- **Named concept** (soft, judgment-required) — when the stream mentions a concept by title without wikilink brackets, activation *may* fire if the concept is comprehension-relevant for the current reading.
- **Gap detection replacement** — mid-ritual restart on a new seed when gap detection produces a frame-mismatch signal.

**Ritual steps.**
1. **Identify activation seed.** The specific concept whose frame needs loading.
2. **Prefer peripheral seeds over hub seeds.** If the stream mentions a dense hub like `[[onboarding]]` but what's comprehension-relevant is a specific sub-concept (e.g., `[[onboarding checklist v2]]`), use the sub-concept as the seed. Ask: *"what's the most specific node that covers what I need to understand right now?"* The answer is the seed.
3. **Read seed node fully** — body + all passes of `semantic_neighbors`. This is the starting activation energy.
4. **Build one-hop frame with relation-weighted activation.** From seed's body wikilinks + `semantic_neighbors` union:
   - **Paradigmatic edges → full weight.** Contrastive alternatives that make the concept sharp.
   - **Syntagmatic edges → partial weight.** Co-occurrence history; often bears on origin, rarely on current comprehension.
5. **Load one-hop frame into working context:**
   - Seed: full-read (body + frontmatter)
   - Paradigmatic one-hop: full-read
   - Syntagmatic one-hop: summary only (title + first paragraph + *What it is* section)
6. **Load two-hop frame at attenuated weight — paradigmatic only.** For each one-hop paradigmatic neighbor, follow *its* paradigmatic edges at summary weight. Syntagmatic two-hop is noise at that distance. Weighting cascade: seed 1.0, paradigmatic one-hop ~0.8, syntagmatic one-hop ~0.3, paradigmatic two-hop ~0.2, everything else unloaded. Three hops and beyond never loaded by default.
7. **Mark frame as active in working session state.** Mental bookkeeping — Claude Code has no persistent frame state, so this is internal tracking across turns using the conversation history as the state record. Imperfect, accepted cost. Maximum two frames simultaneously (primary + secondary for legitimately cross-cluster sessions).
8. **Run gap detection (live-stream variant).** For every subsequent concept that enters the stream: is this concept reachable from the active frame within 2 hops at non-trivial weight?
   - **Reachable** → expected co-occurrence, no signal.
   - **Not reachable** → surprise signal. Classify:
     - **(a) Missing edge candidate** — concept is semantically related to the frame but the vault doesn't know it. Flag for integration/primary consolidation via `kanban/reports/`.
     - **(b) Frame mismatch** — concept is genuinely in a different frame. Active frame is wrong. Trigger step 9.
9. **Frame replacement on strong mismatch** (2+ surprises within a short turn window pointing to the same unrelated cluster, or 1 direct hit invalidating a core assumption). De-activate old frame, re-run steps 1–7 on new seed. **Activation's value includes detecting absence of coverage, not just loading existing coverage** — if the vault lacks a node for the new frame, the surprise signal itself is the useful output. Dead-frame cases file as `kanban/reports/` pointing at the absent concept; they're high-signal coverage-gap flags.
10. **Decay on topic shift, not turn count.** Active frames persist until explicit re-activation replaces them or a new high-signal trigger from outside the current frame fires. Two-frame maximum enforces displacement — the third activation displaces the older of the two.

**Procedural primitives.** Glob (resolve wikilinks), Read (heavy — seed + paradigmatic full-read, syntagmatic summary), Grep (gap-detection investigation on surprises), frontmatter parse. No Write to vault. Surprise signals write to `kanban/reports/`.

**Schema dependency.** Activation is the operation that finally *consumes* the Saussure `relation` labels in its implementation. Without labels, step 4's weighting degrades to flat edge weight and activation can't distinguish comprehension-essential edges from co-occurrence history. With labels, the distinction is mechanical. This is the deferred payoff for the schema change — activation is where relation labels pay out.

**Failure modes.**
1. Never fires → invisible cost, the missing frames are exactly what would have shown the missing context. Prevention: step 1 wikilink-encounter as automatic, non-skippable.
2. Fires too cheaply → background noise. Prevention: step 4 relation weighting + step 6 two-hop attenuation + re-fire suppression (concepts already in frame don't re-load).
3. Hub-seed activation → flat dilution across too many paths. Prevention: step 2 peripheral-seed preference as explicit rule.
4. Frame lock-in / confirmation bias → everything interpreted through wrong frame. Prevention: step 8 gap detection + step 9 replacement. **Mechanical replacement for priming's soft bias-correction.** The 2026-04-14 Obsidian-misdiagnosis case is the reference failure — had gap detection been running, the mention of "plugin from Github" would have fired a surprise signal because "plugin" wasn't reachable from the vault-metacognition frame.
5. Decay too fast / too slow. Prevention: topic-bounded decay (step 10) + two-frame max displacement.
6. Relation-label degradation on legacy nodes → flat weighting. Graceful fallback: treat unlabeled edges as syntagmatic (the unmarked default). Bootstrap cost, not flaw.
7. Gap detection surprise flood → every unreachable mention fires. Prevention: weight threshold — surprises are high-signal only when frame is strongly loaded AND surprise concept is directly referenced, not tangentially adjacent.
8. **Token cost of frame loading.** Real. Full-load paradigmatic + summary syntagmatic can consume 5–10 file reads per activation. Accepted — semantic memory costs tokens; the alternative ("read when asked") is the filing cabinet operating under a different name.
9. **Dead-frame case** — surprise fires but vault lacks a node for the replacement frame. The surprise itself is valuable output; file as `kanban/reports/` entry pointing at the absent concept. Activation detects coverage gaps even when it can't fill them.

**Worked example.** The 2026-04-14 session's Obsidian misdiagnosis is the reference failure trace. The user said "Obsidian auto-create." No vault node for Obsidian directly; closest match is `[[The filing cabinet pattern]]` via its Obsidian stub cleanup mention. Frame loaded: vault-metacognition cluster (FCP + paradigmatic neighbor PSA full-read + syntagmatic neighbors VISM, hub-os Layer 4 summary-read). The user then mentioned "plugin I installed from Github." Check: is "plugin" reachable from the active vault-metacognition frame within 2 hops? No — the frame contains vault phenomena, filing cabinet, content/operation split, and none of those reach "plugin" in the Claude Code environment sense. **Surprise signal fires.** Classify: frame mismatch (case 8b) — the stream has moved from "vault phenomena" to "Claude Code environment," not adding nuance to the current frame. Step 9 replacement attempt: find a vault node for the new frame. **Fails — the vault has no node covering Claude Code environment, plugins, or session infrastructure.** This is a dead-frame case: activation correctly identifies the frame mismatch but can't complete replacement because of a coverage gap. The surprise signal itself is the useful output — it would have blocked the "parallel cognition" misdiagnosis by flagging "stop interpreting this through the vault frame, the topic is different." Operational value: detection of the mismatch, not successful frame load.

---

## Schema specification

```yaml
semantic_neighbors:
  - pass: N                    # integer, append-only
    date: YYYY-MM-DD
    type: primary | integration | re-consolidation
    note: "one-line evidence"  # mandatory for re-consolidation, optional otherwise
    nodes:
      - node: "[[Target Node Name]]"
        relation: syntagmatic | paradigmatic
```

**Discipline rules:**
- **Passes are append-only.** Mutation with evidence. Old passes never change.
- **Passes encode delta, not cumulative state.** Each pass lists only what's new or changed at that pass. Current full neighborhood = union over all passes.
- **`relation` defaults to `syntagmatic`** when omitted. Paradigmatic is the marked case and must be explicitly labeled. Asymmetric safety: an under-labeled paradigmatic is still a valid syntagmatic; a falsely-labeled paradigmatic creates a false contrast, which is more corrosive.
- **`note` is mandatory for `type: re-consolidation`**, optional for `primary` and `integration`. Re-consolidation passes without notes lose the evidence that makes them useful to future readers.
- **Legacy nodes without `semantic_neighbors` are incomplete.** They acquire pass history when re-consolidation naturally touches them; not through a migration sweep.

## Cross-operation dependencies

```
PRIMARY CONSOLIDATION → produces nodes and pass-1 edges
    ↓
INTEGRATION → upgrades references to bidirectional edges
    ↓
RE-CONSOLIDATION → preserves history while extending framing
    ↓
PRIMING (baseline load) + PATTERN SURFACING (periodic walk) → consume what writes produce
    ↓
ACTIVATION → consumes all of the above to load comprehension frames on demand
```

Activation is the most downstream operation. Its ceiling is set by the rigor of every upstream operation. A vault with good primary consolidation but missing relation labels, no pass history, and no peripheral-seed discipline will still do activation, but the activation will be flat, noisy, and bias-prone. The six compose into a single cognitive loop where the write-side produces the semantic content and metadata and the read-side finally closes the loop by using the produced content as memory rather than as filed storage.


## When safe to apply

- When executing any session that touches the vault. Every session should run at least priming + activation on reads, and primary consolidation + integration on writes when real work happens.
- When designing a new operation type (e.g., "teaching from the vault," "exporting a cluster"). The content/operation split and the observer-swap test apply regardless of the specific operation.
- When auditing a vault's health. The six operations give you six axes to score against, and the filing cabinet pattern's four content properties give you four more.

## When unsafe to apply

- As a migration plan for legacy nodes. Retroactive application produces thrash and writes without occasion. Legacy nodes acquire pass history when re-consolidation naturally touches them, not through a migration sweep.
- As a reason to defer writing anything until the full discipline can be applied. The discipline grows into place through use; waiting for perfect conditions produces no writes at all.
- As justification for building runtime infrastructure (graph databases, embeddings pipelines, MCP servers). The whole design target is approximating semantic operations using procedural primitives that already exist. If a design path starts needing tooling, the ritual isn't the right answer.
