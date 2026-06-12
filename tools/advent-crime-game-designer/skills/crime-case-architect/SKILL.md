---
name: crime-case-architect
description: Use when designing or revising the core analog crime case for an Advent calendar deduction game, including closed-circle suspects, MOCA matrices, true crime timeline, investigation timeline, alibis, motives, secrets, clue routes, and final exclusive solution logic.
---

# Crime Case Architect

Use this skill to build the case before writing envelope text. Work in German unless the user asks otherwise. Prefer a closed-circle mystery with 3 to 8 suspects, a fixed objective truth, and a final solution that is not merely plausible but uniquely forced by evidence.

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

## Quality Bar

- No unknown culprit appearing late.
- No clue whose force depends on a hidden author assumption.
- No alibi contradiction unless time, distance, access, or witness reliability makes the contradiction concrete.
- Every emotional or literary beat must still carry a mechanical purpose.
- Keep optional subplots separable from the mandatory solution path.

## References

- `../../references/advent-crime-design-guide.md`
- `../../references/research-method-cards.md`
- `../../assets/templates/case-bible.template.md`
- `../../assets/templates/moca-matrix.template.md`
- `../../assets/templates/timeline.example.json`
