---
name: sandbox-calendar-builder
description: Use when turning a crime case into an analog Advent calendar with 24 sandbox envelopes, coordinates, map and directory mechanics, newspapers, time budgets, daily pacing, hint ladders, physical props, and production manifests.
---

# Sandbox Calendar Builder

Use this skill when the case needs to become playable physical material. Default to the decentralized sandbox model: one start envelope, then coordinate or institution envelopes opened by following leads through a map, address book, newspaper, or prop.

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

## Envelope Rules

- Every critical envelope must be reachable from at least one earlier clue.
- A red herring may cost time, but it must give a fair exit sign.
- No envelope should reveal the final culprit without requiring synthesis.
- Keep daily play to roughly 10 to 20 minutes unless the user asks otherwise.
- If an envelope contains a puzzle gate, include the fallback hint ladder immediately.

## Required Outputs

For a full build, return:

- envelope manifest
- directory entries
- newspaper release schedule
- clue dependency map
- time-budget rules
- physical production checklist
- spoiler-safe hint structure

## References

- `../../assets/templates/envelope-manifest.example.json`
- `../../assets/templates/clue-ledger.template.md`
- `../../assets/templates/playtest-report.template.md`
