# Research Method Cards

Use these cards as practical design moves. They are not paper summaries. Each card maps a research direction to an analog Advent crime-game artifact.

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
