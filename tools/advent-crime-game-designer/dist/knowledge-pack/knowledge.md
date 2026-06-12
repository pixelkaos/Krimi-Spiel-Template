# Advent Crime Game Designer Knowledge Pack

This document consolidates the portable knowledge from the Codex plugin.

## Source Index

- `README.md` (readme, sha256 `c7fc1fc45b4a420941809778343a911420484816c1b4c2242f0286c8825804e0`)
- `skills/crime-case-architect/SKILL.md` (skill, sha256 `9386b04735bdff88f0f8b5b635b5279c0ae4722962b2d45d189705619b1cedd2`)
- `skills/deduction-consistency-auditor/SKILL.md` (skill, sha256 `3b4f047578b1189f32c1a74df10a8e93bcdb8b82c125237b4af7c725189c5467`)
- `skills/research-backed-story-planner/SKILL.md` (skill, sha256 `cbfe8220ae45f2f64c8b88140e0338862dc92ed1f218c66bdb442fec8e5d28c9`)
- `skills/sandbox-calendar-builder/SKILL.md` (skill, sha256 `88bce188ec34aefcf9cad420db6b6aae833f9e94c76cd154709fdb267a18db3c`)
- `references/advent-crime-design-guide.md` (reference, sha256 `3f1904bfc5fc3492bd41ba18d1ff40555ad4e88c2be19d82e9182040261efd12`)
- `references/research-method-cards.md` (reference, sha256 `855932cc8c44c5c6b55c119626e716ae2e0eaacf44613c52ab43c31cd9042224`)
- `references/source-index.md` (reference, sha256 `322753e60d4b5d43dc9533361b03a79fcd47a412c88def862cce52f2e9499d79`)
- `assets/templates/case-bible.template.md` (template, sha256 `54cd567699354f7282236a2671a3c9d7b3552a10e21992a7debba41e3888e09b`)
- `assets/templates/clue-ledger.template.md` (template, sha256 `3bf46f16b24c1afc4a276fc7eb2de2752cc213d99ce2af9862ffc97a7cf7e0f9`)
- `assets/templates/moca-matrix.template.md` (template, sha256 `0f4e54df45c077a8f0e08ac4aa2cd39a4af837797aafbae6a122426541247081`)
- `assets/templates/playtest-report.template.md` (template, sha256 `2a8ac32268deac508751d6f78f44f4f8f5cabf19958baafb2d484f7cf1fddd63`)
- `assets/templates/envelope-manifest.example.json` (template, sha256 `1de028079da37f2d95586580b81a3b069bc49943bbaaeb5f00a88b9fbd61c973`)
- `assets/templates/timeline.example.json` (template, sha256 `043905820e2d09064bb890ece6aa5f03a2f1e6e52dd2fc1436ab6327ff78946a`)
- `assets/templates/truth-map.example.json` (template, sha256 `7097d8c3ba628d9893ec047d86bc4b4ceed32fc8a50119b02998663af11b75a3`)

## Chunks

### Advent Crime Game Designer

Source: `README.md` | Kind: `readme` | Tags: md, readme

# Advent Crime Game Designer

Local Codex plugin for building an analog crime and deduction game in Advent calendar form.

The plugin is German-facing and optimized for a Sherlock-Holmes-Consulting-Detective-style sandbox calendar: coordinate envelopes, a map, an address book, staged newspapers, daily time budgets, clue networks, red herrings, and a final exclusive solution.

### Included Skills

Source: `README.md` | Kind: `readme` | Tags: md, readme

## Included Skills

- `crime-case-architect` - reverse-plot the case, suspects, MOCA matrix, crime timeline, alibis, and reveal logic.
- `research-backed-story-planner` - apply selected LLM-era story-generation research to practical crime-game planning.
- `sandbox-calendar-builder` - package the case into 24 coordinate envelopes, directory entries, newspapers, hints, and production lists.
- `deduction-consistency-auditor` - audit clues, truth maps, timelines, red herrings, liar mechanics, and playtest readiness.

### Included Scripts

Source: `README.md` | Kind: `readme` | Tags: md, readme

## Included Scripts

All scripts use only the Python standard library.

```bash
python3 scripts/validate_truth_map.py assets/templates/truth-map.example.json
python3 scripts/validate_timeline.py assets/templates/timeline.example.json
python3 scripts/validate_envelope_manifest.py assets/templates/envelope-manifest.example.json
```

Portable knowledge-pack export and local Qdrant indexing:

```bash
python3 scripts/export_knowledge_pack.py
python3 scripts/embed_knowledge_pack.py --dry-run
python3 scripts/embed_knowledge_pack.py
python3 scripts/query_knowledge_pack.py "Wie verteile ich Hinweise auf 24 Umschlaege?"
```

Defaults:

- Qdrant: `http://localhost:6333`
- Ollama: `http://localhost:11434`
- Embedding model: `qwen3-embedding:latest`
- Collection: `advent_crime_game_designer__qwen3_embedding`

The Qdrant script creates only the dedicated collection above unless `--collection` is passed. It refuses to reuse a populated unmanaged collection and only deletes/recreates a collection when `--recreate` is explicitly passed.

If Qdrant reports that a collection is missing but collection creation fails with `File exists`, the local Qdrant storage has an orphaned directory. Repair or restart/recreate the Qdrant container before rerunning the embedding script; the plugin will not delete unknown Qdrant storage directories automatically.

Generated portable artifacts are written to `dist/knowledge-pack/`:

- `instructions.md` - provider-neutral behavior instructions.
- `knowledge.md` - consolidated upload/paste knowledge.
- `chunks.jsonl` - RAG-ready chunks with stable IDs and source metadata.
- `manifest.json` - source hashes, chunk count, and embedding metadata.
- `llms.txt` - discovery index for LLM tooling.
- `qdrant-index.json` - local Qdrant index metadata after embedding.

### Primary Sources

Source: `README.md` | Kind: `readme` | Tags: md, readme

## Primary Sources

- Upstream research map: <https://github.com/yingpengma/Awesome-Story-Generation>
- Game outline source: `/Users/pixelkaos/Documents/Anleitungen/Adventskalender/Adventskalender-Raetselspiel-Entwicklung.md`

The plugin keeps a curated research playbook rather than copying full papers or datasets.

### SKILL.md

Source: `skills/crime-case-architect/SKILL.md` | Kind: `skill` | Tags: crime-case-architect, md, skill

---
name: crime-case-architect
description: Use when designing or revising the core analog crime case for an Advent calendar deduction game, including closed-circle suspects, MOCA matrices, true crime timeline, investigation timeline, alibis, motives, secrets, clue routes, and final exclusive solution logic.
---

### Crime Case Architect

Source: `skills/crime-case-architect/SKILL.md` | Kind: `skill` | Tags: crime-case-architect, md, skill

# Crime Case Architect

Use this skill to build the case before writing envelope text. Work in German unless the user asks otherwise. Prefer a closed-circle mystery with 3 to 8 suspects, a fixed objective truth, and a final solution that is not merely plausible but uniquely forced by evidence.

### Workflow

Source: `skills/crime-case-architect/SKILL.md` | Kind: `skill` | Tags: crime-case-architect, md, skill

## Workflow

1. State the target format in one sentence: sandbox calendar, chronological calendar, or hybrid. Default to sandbox calendar.
2. Define the final truth first: victim, culprit, method, motive, opportunity, cover story, and decisive contradiction.
3. Build the closed circle:
   - suspects
   - victim connections
   - locations
   - access rules
   - social secrets
4. Create a MOCA table for every suspect:
   - Motiv
   - Gelegenheit
   - Beziehung
   - Alibi
5. Split the case into two timelines:
   - objective crime timeline
   - player-facing investigation timeline
6. Add red herrings only after the main solution is stable. Each red herring needs a fair exit clue.
7. Write the deduction spine as "evidence therefore exclusion" steps, not as author intuition.

### Required Outputs

Source: `skills/crime-case-architect/SKILL.md` | Kind: `skill` | Tags: crime-case-architect, md, skill

## Required Outputs

For a new case, return:

- One-paragraph premise
- Cast list with roles and secrets
- MOCA matrix
- objective crime timeline
- investigation timeline
- core clue chain
- red herring list
- final answer sheet draft
- open design risks

For a revision, return:

- what changed
- which contradiction or weakness it fixes
- remaining missing clues
- next artifact to produce

### Quality Bar

Source: `skills/crime-case-architect/SKILL.md` | Kind: `skill` | Tags: crime-case-architect, md, skill

## Quality Bar

- No unknown culprit appearing late.
- No clue whose force depends on a hidden author assumption.
- No alibi contradiction unless time, distance, access, or witness reliability makes the contradiction concrete.
- Every emotional or literary beat must still carry a mechanical purpose.
- Keep optional subplots separable from the mandatory solution path.

### References

Source: `skills/crime-case-architect/SKILL.md` | Kind: `skill` | Tags: crime-case-architect, md, skill

## References

- `../../references/advent-crime-design-guide.md`
- `../../references/research-method-cards.md`
- `../../assets/templates/case-bible.template.md`
- `../../assets/templates/moca-matrix.template.md`
- `../../assets/templates/timeline.example.json`

### SKILL.md

Source: `skills/deduction-consistency-auditor/SKILL.md` | Kind: `skill` | Tags: deduction-consistency-auditor, md, skill

---
name: deduction-consistency-auditor
description: Use when reviewing an analog crime or Advent calendar deduction design for logical uniqueness, clue coverage, timeline contradictions, truth-map solvability, red herring fairness, liar mechanics, playtest readiness, and physical envelope reachability.
---

### Deduction Consistency Auditor

Source: `skills/deduction-consistency-auditor/SKILL.md` | Kind: `skill` | Tags: deduction-consistency-auditor, md, skill

# Deduction Consistency Auditor

Use this skill as a review pass. Be direct and evidence-based. Findings should identify the exact artifact, the broken inference, and the smallest fix.

### Audit Passes

Source: `skills/deduction-consistency-auditor/SKILL.md` | Kind: `skill` | Tags: deduction-consistency-auditor, md, skill

## Audit Passes

1. Exclusive plausibility:
   - Is the intended solution the only contradiction-free answer?
   - Which suspects remain plausible after all evidence?
2. Truth-map coverage:
   - Are all required pairings either stated or inferable?
   - Does each missing truth-map cell have enough exclusion clues?
3. Timeline:
   - Can any person be in two places at once?
   - Do travel, opening hours, witness times, and prop access align?
4. Clue dependency:
   - Is every critical clue reachable?
   - Is any clue required before it can be discovered?
5. Red herrings:
   - Does each false trail teach or reveal something?
   - Does each false trail have a fair exit?
6. Liar mechanic:
   - Are truth-tellers visibly reliable?
   - Is every lie anchored to a contradiction the player can detect?
7. Advent packaging:
   - Are day budgets coherent?
   - Are sealed items safe from accidental early information leaks?

### Output Format

Source: `skills/deduction-consistency-auditor/SKILL.md` | Kind: `skill` | Tags: deduction-consistency-auditor, md, skill

## Output Format

Return:

- Findings, ordered by severity
- Evidence or artifact reference
- Why it breaks fairness or logic
- Minimal repair
- Validation to rerun

If there are no findings, say that clearly and list residual playtest risk.

### Script Support

Source: `skills/deduction-consistency-auditor/SKILL.md` | Kind: `skill` | Tags: deduction-consistency-auditor, md, skill

## Script Support

Use these local scripts when the user provides compatible JSON:

```bash
python3 scripts/validate_truth_map.py <truth-map.json>
python3 scripts/validate_timeline.py <timeline.json>
python3 scripts/validate_envelope_manifest.py <envelopes.json>
```

### References

Source: `skills/deduction-consistency-auditor/SKILL.md` | Kind: `skill` | Tags: deduction-consistency-auditor, md, skill

## References

- `../../assets/templates/truth-map.example.json`
- `../../assets/templates/timeline.example.json`
- `../../assets/templates/envelope-manifest.example.json`

### SKILL.md

Source: `skills/research-backed-story-planner/SKILL.md` | Kind: `skill` | Tags: md, research-backed-story-planner, skill

---
name: research-backed-story-planner
description: Use when applying story-generation research from Awesome-Story-Generation to practical crime-game writing, especially suspense planning, hierarchical outlining, multi-agent critique, plot-hole detection, world-state tracking, relationship graphs, interactive-fiction state, pacing, and story evaluation.
---

### Research-Backed Story Planner

Source: `skills/research-backed-story-planner/SKILL.md` | Kind: `skill` | Tags: md, research-backed-story-planner, skill

# Research-Backed Story Planner

Use this skill to translate research patterns into practical design moves. Do not summarize papers for their own sake. Always connect the method to a concrete Advent crime-game artifact.

### Method Selection

Source: `skills/research-backed-story-planner/SKILL.md` | Kind: `skill` | Tags: md, research-backed-story-planner, skill

## Method Selection

Pick the smallest useful method:

- Suspense and reveal planning: use iterative planning and uncertainty control.
- Pacing: use hierarchical outline levels and even daily information load.
- Consistency: track time-aware world-state facts and contradiction intervals.
- Detective relationships: separate public relationships from secret relationships.
- Interactive play: model player-facing actions as preconditions and effects.
- Critique: run focused critic passes for logic, pacing, fairness, and prose.
- Evaluation: judge coherence, character development, interestingness, and solvability separately.

### Default Output Pattern

Source: `skills/research-backed-story-planner/SKILL.md` | Kind: `skill` | Tags: md, research-backed-story-planner, skill

## Default Output Pattern

When asked to help design, return:

1. Chosen method cards
2. Why each method fits this case
3. Artifact to create or update
4. Concrete prompts or tables to use
5. Failure mode the method prevents

### Research Guardrails

Source: `skills/research-backed-story-planner/SKILL.md` | Kind: `skill` | Tags: md, research-backed-story-planner, skill

## Research Guardrails

- Treat LLM output as draft material, never as proof of solvability.
- For long-form consistency, maintain explicit state rather than relying on memory.
- For detective fiction, relationship graphs must include secret and viewpoint-specific relationships.
- For analog play, every generated clue must become a physical or textual artifact.
- For Advent pacing, optimize the daily discovery rhythm before polishing prose.

### References

Source: `skills/research-backed-story-planner/SKILL.md` | Kind: `skill` | Tags: md, research-backed-story-planner, skill

## References

- `../../references/source-index.md`
- `../../references/research-method-cards.md`

### SKILL.md

Source: `skills/sandbox-calendar-builder/SKILL.md` | Kind: `skill` | Tags: md, sandbox-calendar-builder, skill

---
name: sandbox-calendar-builder
description: Use when turning a crime case into an analog Advent calendar with 24 sandbox envelopes, coordinates, map and directory mechanics, newspapers, time budgets, daily pacing, hint ladders, physical props, and production manifests.
---

### Sandbox Calendar Builder

Source: `skills/sandbox-calendar-builder/SKILL.md` | Kind: `skill` | Tags: md, sandbox-calendar-builder, skill

# Sandbox Calendar Builder

Use this skill when the case needs to become playable physical material. Default to the decentralized sandbox model: one start envelope, then coordinate or institution envelopes opened by following leads through a map, address book, newspaper, or prop.

### Build Order

Source: `skills/sandbox-calendar-builder/SKILL.md` | Kind: `skill` | Tags: md, sandbox-calendar-builder, skill

## Build Order

1. Start packet:
   - rule sheet
   - map
   - address book
   - first newspaper
   - case briefing
   - note sheet
2. Envelope manifest:
   - 24 envelope IDs
   - label or coordinate
   - unlock day
   - time cost
   - contents
   - clue IDs
   - leads unlocked
3. Pacing layer:
   - daily investigation hours
   - time-cost symbols
   - newspaper release days
   - bottleneck or milestone checks
4. Physical evidence:
   - letters
   - photos
   - receipts
   - newspaper clippings
   - map overlays
   - logic-grid slips
5. Hint system:
   - three spoiler-light hints per puzzle
   - final confirmation sheet

### Envelope Rules

Source: `skills/sandbox-calendar-builder/SKILL.md` | Kind: `skill` | Tags: md, sandbox-calendar-builder, skill

## Envelope Rules

- Every critical envelope must be reachable from at least one earlier clue.
- A red herring may cost time, but it must give a fair exit sign.
- No envelope should reveal the final culprit without requiring synthesis.
- Keep daily play to roughly 10 to 20 minutes unless the user asks otherwise.
- If an envelope contains a puzzle gate, include the fallback hint ladder immediately.

### Required Outputs

Source: `skills/sandbox-calendar-builder/SKILL.md` | Kind: `skill` | Tags: md, sandbox-calendar-builder, skill

## Required Outputs

For a full build, return:

- envelope manifest
- directory entries
- newspaper release schedule
- clue dependency map
- time-budget rules
- physical production checklist
- spoiler-safe hint structure

### References

Source: `skills/sandbox-calendar-builder/SKILL.md` | Kind: `skill` | Tags: md, sandbox-calendar-builder, skill

## References

- `../../assets/templates/envelope-manifest.example.json`
- `../../assets/templates/clue-ledger.template.md`
- `../../assets/templates/playtest-report.template.md`

### Advent Crime Design Guide

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

# Advent Crime Design Guide

This guide distills the attached rough draft into reusable plugin rules.

### Core Format

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Core Format

Default model:

- analog crime and deduction game
- Advent calendar pacing
- 24 envelopes or daily units
- SHCD-style open investigation
- no dice, randomizers, or hidden game master
- map, address book, newspapers, clue notes, and physical evidence

### Design Principles

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Design Principles

- Build the objective crime first, then the investigation path.
- Use a closed circle of suspects.
- The intended solution must be uniquely forced by evidence.
- Separate real truth from claims, lies, mistakes, and red herrings.
- Let players choose investigation order inside controlled pacing gates.
- Use physical materials as logic tools, not just decoration.

### Case Architecture

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Case Architecture

Every case needs:

- victim
- culprit
- method
- motive
- opportunity
- decisive contradiction
- closed-circle suspect list
- map constraints
- address book lookup terms
- timeline of the crime
- timeline of clue revelation

### MOCA Matrix

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## MOCA Matrix

For each suspect, maintain:

- Motiv: why they might do it
- Gelegenheit: whether they physically could do it
- Beziehung: public and secret links to victim and other suspects
- Alibi: claim, support, contradiction, and final status

### Truth Map

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Truth Map

Use mutually exclusive categories only when they are truly exclusive:

- one person at one location at one time
- one unique owner per marked object
- one envelope containing a specific artifact

Avoid forcing non-exclusive realities into a logic grid:

- motives
- emotional states
- social grudges
- vague access

### Sandbox Calendar Rules

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Sandbox Calendar Rules

For the decentralized sandbox model:

- the start packet opens on day 1
- envelopes are labeled by coordinates, institutions, or lead names
- players find envelope IDs through the directory, map, newspaper, and props
- daily time budget limits investigation pace
- newspaper releases add global leads on selected days
- critical clues must remain reachable

### Red Herrings

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Red Herrings

A red herring is allowed only if it:

- has a plausible entry clue
- reveals character, theme, or world information
- has a fair exit clue
- does not consume the only route to a critical clue

### Liar Mechanic

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Liar Mechanic

If using "the culprit lies, innocents tell the truth":

- signal reliable witness statements clearly
- make contradictions textual or physical, not tonal
- ensure two contradictory claims narrow the suspect set
- never require players to identify a lie from authorial vibes alone

### Playtesting

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Playtesting

Run three passes:

- Solution-path cut: remove active deception and test whether the core case is easy.
- Truth-map scrambling: rebuild the solution using only player-facing clues.
- Volunteer playtest: measure time, comprehension, frustration, and clue reachability.

### Expansion Points

Source: `references/advent-crime-design-guide.md` | Kind: `reference` | Tags: advent, crime, design, guide, md, reference

## Expansion Points

Future plugin versions can add:

- chronological 24-day mode
- 12-day mode
- printable prop templates
- newspaper generator
- stronger graph-based reachability checks
- richer visual production guidance

### Research Method Cards

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

# Research Method Cards

Use these cards as practical design moves. They are not paper summaries. Each card maps a research direction to an analog Advent crime-game artifact.

### Relationship Graphs for Detective Narratives

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Relationship Graphs for Detective Narratives

Source: Large Language Models Fall Short: Understanding Complex Relationships in Detective Narratives.

Design move:

- Track public relationships separately from secret relationships.
- Track viewpoint: who knows, suspects, hides, misreads, or lies about each relationship.
- Use at least one relationship contradiction as a deductive engine.

Artifact:

- relationship matrix
- suspect dossier
- clue map

Failure prevented:

- flat suspect lists where every motive feels interchangeable.

### Time-Aware World State Tracking

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Time-Aware World State Tracking

Source: FACTTRACK and DOME.

Design move:

- Store facts with validity intervals.
- Let facts become false later only through explicit events.
- Check all alibis against overlapping time intervals and locations.

Artifact:

- objective timeline JSON
- witness statement table
- alibi grid

Failure prevented:

- accidental contradictions created by long-form writing.

### Suspense Planning

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Suspense Planning

Source: Creating Suspenseful Stories.

Design move:

- Plan uncertainty deliberately: what the player knows, what they suspect, what they cannot yet know.
- Avoid revealing decisive facts before the player has competing hypotheses.
- Give each day either a new question, a partial answer, or a contradiction.

Artifact:

- reveal ladder
- daily pacing table
- clue dependency map

Failure prevented:

- clue dumps that solve the case too early or daily entries that feel inert.

### Pacing by Outline Granularity

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Pacing by Outline Granularity

Source: Improving Pacing in Long-Form Story Planning and WritingPath.

Design move:

- Keep daily entries at comparable information density.
- Expand vague outline nodes only when the player needs scene texture.
- Do not over-write low-importance branches.

Artifact:

- 24-envelope manifest
- scene expansion checklist

Failure prevented:

- one day overloaded with six key clues while several days add only atmosphere.

### Plot-Hole and Coherence Pass

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Plot-Hole and Coherence Pass

Source: Finding Flawed Fictions, SCORE, MLD-EA.

Design move:

- Run a separate contradiction pass after prose exists.
- Ask whether each claimed fact conflicts with state, motive, timeline, emotion, or action.
- Treat plot-hole detection as QA, not creativity.

Artifact:

- audit report
- fix list
- playtest readiness checklist

Failure prevented:

- beautiful text that breaks the logical case.

### Interactive Fiction State and Actions

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Interactive Fiction State and Actions

Source: STORY2GAME.

Design move:

- Convert investigation choices into action preconditions and effects.
- A lead has a precondition: the player must know a name, place, object, symbol, or newspaper item.
- Opening an envelope has effects: new clue, new lead, new contradiction, or red herring exit.

Artifact:

- envelope manifest
- directory table
- lead graph

Failure prevented:

- envelopes that can be opened but do not change the state of the investigation.

### Authorial Intent vs Emergent Play

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Authorial Intent vs Emergent Play

Source: StoryVerse and interactive drama research.

Design move:

- Define abstract acts for the case: discovery, expansion, false synthesis, contradiction, narrowing, accusation.
- Let player order vary inside each act, but protect the macro progression with newspapers and unlock days.

Artifact:

- act map
- newspaper release schedule
- bottleneck rules

Failure prevented:

- sandbox freedom that destroys the dramatic arc.

### Collective Critique

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Collective Critique

Source: Agents' Room and Collective Critics.

Design move:

- Review the same draft through separate critic roles:
  - logic critic
  - pacing critic
  - fair-play critic
  - physical-production critic
  - prose critic
- Do not let a prose fix change clue semantics without rerunning logic checks.

Artifact:

- revision checklist
- review notes

Failure prevented:

- improving one dimension while silently breaking another.

### Symbolic Constraints for Variation

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Symbolic Constraints for Variation

Source: Guiding and Diversifying LLM-Based Story Generation via Answer Set Programming.

Design move:

- Express hard constraints before brainstorming variants.
- Example: exactly one culprit, every suspect has motive, culprit has unique opportunity, no critical clue appears only in an optional locked branch.

Artifact:

- hard-constraint list
- truth-map JSON

Failure prevented:

- appealing alternative plots that violate fair deduction.

### Story Evaluation Criteria

Source: `references/research-method-cards.md` | Kind: `reference` | Tags: cards, md, method, reference, research

## Story Evaluation Criteria

Source: What Makes a Good Story and How Can We Measure It?

Design move:

- Score story quality separately from game solvability.
- Evaluate coherence, character development, interestingness, suspense, fair-play logic, and physical usability.

Artifact:

- playtest report
- post-test triage

Failure prevented:

- declaring a case "good" because the fiction is engaging while the puzzle is underdetermined.

### Source Index

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

# Source Index

This plugin uses the upstream repository as a curated research map:

- Awesome-Story-Generation: https://github.com/yingpengma/Awesome-Story-Generation
- README snapshot checked during plugin creation: `main` branch, `README.md`
- Citation metadata snapshot checked during plugin creation: `main` branch, `citations.json`

The chosen plugin mode is a curated playbook, not a full bibliography mirror. Use the upstream README for the full maintained list.

### High-Fit Research Links

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

## High-Fit Research Links

### Detective and Relationship Reasoning

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

### Detective and Relationship Reasoning

- Large Language Models Fall Short: Understanding Complex Relationships in Detective Narratives - https://arxiv.org/abs/2402.11051
- Are NLP Models Good at Tracing Thoughts: An Overview of Narrative Understanding - https://arxiv.org/abs/2310.18783
- BookWorm: A Dataset for Character Description and Analysis - https://arxiv.org/abs/2410.10372

### Planning, Suspense, and Pacing

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

### Planning, Suspense, and Pacing

- Creating Suspenseful Stories: Iterative Planning with Large Language Models - https://arxiv.org/abs/2402.17119
- Improving Pacing in Long-Form Story Planning - https://arxiv.org/abs/2311.04459
- Generating Long-form Story Using Dynamic Hierarchical Outlining with Memory-Enhancement - https://arxiv.org/abs/2412.13575
- Navigating the Path of Writing: Outline-guided Text Generation with Large Language Models - https://arxiv.org/abs/2404.13919
- Learning to Reason for Long-Form Story Generation - https://arxiv.org/abs/2503.22828

### Consistency and Plot-Hole Detection

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

### Consistency and Plot-Hole Detection

- FACTTRACK: Time-Aware World State Tracking in Story Outlines - https://arxiv.org/abs/2407.16347
- Finding Flawed Fictions: Evaluating Complex Reasoning in Language Models via Plot Hole Detection - https://arxiv.org/abs/2504.11900
- SCORE: Story Coherence and Retrieval Enhancement for AI Narratives - https://arxiv.org/abs/2503.23512
- MLD-EA: Check and Complete Narrative Coherence by Introducing Emotions and Actions - https://arxiv.org/abs/2412.02897

### Interactive and Game-Oriented Story Design

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

### Interactive and Game-Oriented Story Design

- STORY2GAME: Generating (Almost) Everything in an Interactive Fiction Game - https://arxiv.org/abs/2505.03547
- StoryVerse: Towards Co-authoring Dynamic Plot with LLM-based Character Simulation via Narrative Planning - https://arxiv.org/abs/2405.13042
- Towards Enhanced Immersion and Agency for LLM-based Interactive Drama - https://arxiv.org/abs/2502.17878
- NarrativeGenie: Generating Narrative Beats and Dynamic Storytelling with Large Language Models - https://ojs.aaai.org/index.php/AIIDE/article/view/31868

### Multi-Agent Critique and Collaboration

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

### Multi-Agent Critique and Collaboration

- Agents' Room: Narrative Generation through Multi-step Collaboration - https://arxiv.org/abs/2410.02603
- Collective Critics for Creative Story Generation - https://arxiv.org/abs/2410.02428
- IBSEN: Director-Actor Agent Collaboration for Controllable and Interactive Drama Script Generation - https://arxiv.org/abs/2407.01093
- HoLLMwood: Unleashing the Creativity of Large Language Models in Screenwriting via Role Playing - https://arxiv.org/abs/2406.11683

### Control, Diversity, and Evaluation

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

### Control, Diversity, and Evaluation

- Guiding and Diversifying LLM-Based Story Generation via Answer Set Programming - https://arxiv.org/abs/2406.00554
- What Makes a Good Story and How Can We Measure It? A Comprehensive Survey of Story Evaluation - https://arxiv.org/abs/2408.14622
- A Confederacy of Models: a Comprehensive Evaluation of LLMs on Creative Writing - https://arxiv.org/abs/2310.08433
- TIGERScore: Towards Building Explainable Metric for All Text Generation Tasks - https://arxiv.org/abs/2310.00752
- BooookScore: A systematic exploration of book-length summarization in the era of LLMs - https://arxiv.org/abs/2310.00785

### Upstream Categories to Recheck

Source: `references/source-index.md` | Kind: `reference` | Tags: index, md, reference, source

## Upstream Categories to Recheck

Before a major plugin expansion, re-open the upstream README and scan:

- Overview
- Plan And Write
- Multi Agent
- Multimodality
- Better Storytelling
- More Controllable
- More Personalized
- Evaluation
- Dataset
- Public Resources

### Case Bible Template

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

# Case Bible Template

### Premise

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Premise

- Working title:
- Setting:
- Calendar model: sandbox / chronological / hybrid
- Target players:
- Daily play time:
- Tone:

### Final Truth

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Final Truth

- Victim:
- Culprit:
- Method:
- Motive:
- Opportunity:
- Cover story:
- Decisive contradiction:
- Final proof:

### Closed Circle

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Closed Circle

| Suspect | Public role | Secret | Victim link | First lead | Final status |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Crime Timeline

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Crime Timeline

| Time | Objective event | Actors | Location | Evidence left | Who knows |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Investigation Timeline

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Investigation Timeline

| Release point | Player-facing artifact | New fact | New lead | Risk |
| --- | --- | --- | --- | --- |
| Day 1 start |  |  |  |  |

### Clue Spine

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Clue Spine

| Step | Clue | Inference | Excludes | Remaining suspects |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |

### Red Herrings

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Red Herrings

| Trail | Entry clue | Why plausible | Exit clue | What it still teaches |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Final Answer Sheet

Source: `assets/templates/case-bible.template.md` | Kind: `template` | Tags: bible, case, md, template

## Final Answer Sheet

- Who did it?
- How?
- Why?
- What was staged?
- Which clues prove it?
- Which red herrings are false and why?

### Clue Ledger Template

Source: `assets/templates/clue-ledger.template.md` | Kind: `template` | Tags: clue, ledger, md, template

# Clue Ledger Template

| Clue ID | Player-facing text | Source envelope | Fact type | Supports | Excludes | Leads to | Critical |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C001 |  |  | positive / negative / contradiction / texture |  |  |  | yes / no |

### Fact Types

Source: `assets/templates/clue-ledger.template.md` | Kind: `template` | Tags: clue, ledger, md, template

## Fact Types

- positive: confirms a pairing or event
- negative: excludes a pairing or event
- contradiction: conflicts with another claim
- texture: atmosphere or characterization, not required for solution

### Checks

Source: `assets/templates/clue-ledger.template.md` | Kind: `template` | Tags: clue, ledger, md, template

## Checks

- Every critical clue appears in at least one envelope.
- Every final accusation point has at least one clue.
- Every red herring has an exit clue.

### MOCA Matrix Template

Source: `assets/templates/moca-matrix.template.md` | Kind: `template` | Tags: matrix, md, moca, template

# MOCA Matrix Template

| Suspect | Motiv | Gelegenheit | Beziehung | Alibi | Contradiction | Final status |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

### Notes

Source: `assets/templates/moca-matrix.template.md` | Kind: `template` | Tags: matrix, md, moca, template

## Notes

- Motiv should be emotionally and socially plausible.
- Gelegenheit must be testable by time, access, distance, or witness evidence.
- Beziehung should separate public relationship from secret relationship.
- Alibi must include who states it, who supports it, who contradicts it, and when.

### Playtest Report Template

Source: `assets/templates/playtest-report.template.md` | Kind: `template` | Tags: md, playtest, report, template

# Playtest Report Template

### Session

Source: `assets/templates/playtest-report.template.md` | Kind: `template` | Tags: md, playtest, report, template

## Session

- Date:
- Test type: solution-path cut / truth-map scrambling / volunteer playtest
- Players:
- Duration:
- Version tested:

### Observations

Source: `assets/templates/playtest-report.template.md` | Kind: `template` | Tags: md, playtest, report, template

## Observations

| Moment | What players did | Expected behavior | Issue | Severity |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Deduction Results

Source: `assets/templates/playtest-report.template.md` | Kind: `template` | Tags: md, playtest, report, template

## Deduction Results

- Correct culprit?
- Correct method?
- Correct motive?
- Correct red herring exits?
- Unsupported assumptions made:

### Pacing

Source: `assets/templates/playtest-report.template.md` | Kind: `template` | Tags: md, playtest, report, template

## Pacing

- Average daily time:
- Longest day:
- Shortest day:
- Frustration points:

### Fixes

Source: `assets/templates/playtest-report.template.md` | Kind: `template` | Tags: md, playtest, report, template

## Fixes

| Priority | Fix | Artifact | Validation |
| --- | --- | --- | --- |
|  |  |  |  |

### envelope-manifest.example.json

Source: `assets/templates/envelope-manifest.example.json` | Kind: `template` | Tags: envelope, example, json, manifest, template

{
  "daily_time_budget": 3,
  "final_envelope": "solution",
  "critical_clues": ["C001", "C004"],
  "envelopes": [
    {
      "id": "start",
      "label": "Start packet",
      "unlock_day": 1,
      "time_cost": 0,
      "entry_point": true,
      "clues": ["C001"],
      "leads_to": ["12-nw", "library"],
      "critical": true
    },
    {
      "id": "12-nw",
      "label": "12 NW",
      "unlock_day": 1,
      "time_cost": 1,
      "entry_point": false,
      "clues": ["C002"],
      "leads_to": ["31-ec"],
      "critical": false
    },
    {
      "id": "library",
      "label": "Library",
      "unlock_day": 1,
      "time_cost": 1,
      "entry_point": false,
      "clues": ["C004"],
      "leads_to": ["solution"],
      "critical": true
    },
    {
      "id": "31-ec",
      "label": "31 EC",
      "unlock_day": 2,
      "time_cost": 1,
      "entry_point": false,
      "clues": ["C003"],
      "leads_to": [],
      "critical": false
    },
    {
      "id": "solution",
      "label": "Final accusation",
      "unlock_day": 24,
      "time_cost": 0,
      "entry_point": false,
      "clues": [],
      "leads_to": [],
      "critical": true
    }
  ]
}

### timeline.example.json

Source: `assets/templates/timeline.example.json` | Kind: `template` | Tags: example, json, template, timeline

{
  "events": [
    {
      "id": "E001",
      "time": "1888-11-22T08:00",
      "end_time": "1888-11-22T08:20",
      "actors": ["Ada"],
      "location": "Library",
      "truth_status": "objective",
      "revealed_in": ["Start"]
    },
    {
      "id": "E002",
      "time": "1888-11-22T08:30",
      "end_time": "1888-11-22T08:45",
      "actors": ["Bruno"],
      "location": "Kitchen",
      "truth_status": "claim",
      "revealed_in": ["12 NW"]
    },
    {
      "id": "E003",
      "time": "1888-11-22T09:00",
      "end_time": "1888-11-22T09:15",
      "actors": ["Ada", "Clara"],
      "location": "Garden",
      "truth_status": "witnessed",
      "revealed_in": ["31 EC"]
    }
  ]
}

### truth-map.example.json

Source: `assets/templates/truth-map.example.json` | Kind: `template` | Tags: example, json, map, template, truth

{
  "primary_category": "suspect",
  "categories": {
    "suspect": ["Ada", "Bruno", "Clara"],
    "location": ["Library", "Kitchen", "Garden"],
    "object": ["Silver Key", "Blue Glass", "Red Thread"]
  },
  "solutions": {
    "Ada": {
      "location": "Library",
      "object": "Silver Key"
    },
    "Bruno": {
      "location": "Kitchen",
      "object": "Blue Glass"
    },
    "Clara": {
      "location": "Garden",
      "object": "Red Thread"
    }
  },
  "clues": [
    {
      "id": "C001",
      "type": "positive",
      "subject_category": "suspect",
      "subject": "Ada",
      "target_category": "location",
      "target": "Library",
      "envelope": "Start"
    },
    {
      "id": "C002",
      "type": "negative",
      "subject_category": "suspect",
      "subject": "Bruno",
      "target_category": "object",
      "target": "Silver Key",
      "envelope": "12 NW"
    },
    {
      "id": "C003",
      "type": "negative",
      "subject_category": "suspect",
      "subject": "Clara",
      "target_category": "object",
      "target": "Blue Glass",
      "envelope": "31 EC"
    },
    {
      "id": "C004",
      "type": "negative",
      "subject_category": "suspect",
      "subject": "Ada",
      "target_category": "object",
      "target": "Blue Glass",
      "envelope": "Library"
    },
    {
      "id": "C005",
      "type": "negative",
      "subject_category": "suspect",
      "subject": "Bruno",
      "target_category": "location",
      "target": "Garden",
      "envelope": "Kitchen"
    },
    {
      "id": "C006",
      "type": "negative",
      "subject_category": "suspect",
      "subject": "Clara",
      "target_category": "location",
      "target": "Kitchen",
      "envelope": "Garden"
    },
    {
      "id": "C007",
      "type": "positive",
      "subject_category": "suspect",
      "subject": "Clara",
      "target_category": "object",
      "target": "Red Thread",
      "envelope": "31 EC"
    }
  ],
  "critical_solution": {
    "culprit": "Ada",
    "method": "staged accident",
    "decisive_clues": ["C001", "C004", "C007"]
  }
}
