---
name: deduction-consistency-auditor
description: Use when reviewing an analog crime or Advent calendar deduction design for logical uniqueness, clue coverage, timeline contradictions, truth-map solvability, red herring fairness, liar mechanics, playtest readiness, and physical envelope reachability.
---

# Deduction Consistency Auditor

Use this skill as a review pass. Be direct and evidence-based. Findings should identify the exact artifact, the broken inference, and the smallest fix.

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

## Output Format

Return:

- Findings, ordered by severity
- Evidence or artifact reference
- Why it breaks fairness or logic
- Minimal repair
- Validation to rerun

If there are no findings, say that clearly and list residual playtest risk.

## Script Support

Use these local scripts when the user provides compatible JSON:

```bash
python3 scripts/validate_truth_map.py <truth-map.json>
python3 scripts/validate_timeline.py <timeline.json>
python3 scripts/validate_envelope_manifest.py <envelopes.json>
```

## References

- `../../assets/templates/truth-map.example.json`
- `../../assets/templates/timeline.example.json`
- `../../assets/templates/envelope-manifest.example.json`
