---
name: research-backed-story-planner
description: Use when applying story-generation research from Awesome-Story-Generation to practical crime-game writing, especially suspense planning, hierarchical outlining, multi-agent critique, plot-hole detection, world-state tracking, relationship graphs, interactive-fiction state, pacing, and story evaluation.
---

# Research-Backed Story Planner

Use this skill to translate research patterns into practical design moves. Do not summarize papers for their own sake. Always connect the method to a concrete Advent crime-game artifact.

## Method Selection

Pick the smallest useful method:

- Suspense and reveal planning: use iterative planning and uncertainty control.
- Pacing: use hierarchical outline levels and even daily information load.
- Consistency: track time-aware world-state facts and contradiction intervals.
- Detective relationships: separate public relationships from secret relationships.
- Interactive play: model player-facing actions as preconditions and effects.
- Critique: run focused critic passes for logic, pacing, fairness, and prose.
- Evaluation: judge coherence, character development, interestingness, and solvability separately.

## Default Output Pattern

When asked to help design, return:

1. Chosen method cards
2. Why each method fits this case
3. Artifact to create or update
4. Concrete prompts or tables to use
5. Failure mode the method prevents

## Research Guardrails

- Treat LLM output as draft material, never as proof of solvability.
- For long-form consistency, maintain explicit state rather than relying on memory.
- For detective fiction, relationship graphs must include secret and viewpoint-specific relationships.
- For analog play, every generated clue must become a physical or textual artifact.
- For Advent pacing, optimize the daily discovery rhythm before polishing prose.

## References

- `../../references/source-index.md`
- `../../references/research-method-cards.md`
