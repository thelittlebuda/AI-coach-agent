---
name: decision-auditor
description: Ensures every material fitness adjustment is traceable, reversible, and supported by sufficient evidence.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [fitness, decision-log, traceability, audit]
    related_skills: [fitness-coach-core, progress-reviewer, daily-checkin-evaluator]
---

# Decision Auditor

## When to use
Use whenever the coach changes calories, protein targets, steps, training volume, exercise selection, conditioning, deload status, phase, or weekly structure.

## Purpose
Prevent silent drift. Every material change should be traceable to data and reversible if it does not work.

## Material changes
Decision logging is required for:
- Calorie target changes.
- Protein target changes.
- Step target changes.
- Training split changes.
- Main lift progression changes outside normal planned progression.
- Deloads.
- Exercise substitutions due to pain.
- Phase transitions.
- External event replans.

Decision logging is optional for:
- Normal planned load progression.
- Minor same-session exercise swaps due to equipment if stimulus is equivalent.
- Formatting or communication changes.

## Decision quality checklist
Before finalizing a change, verify:
- What data triggered the change?
- Is the data sufficient?
- Is the change proportional?
- What is the expected effect?
- When will it be reviewed?
- What would make the change wrong?

## Output schema
```json
{
  "date": "YYYY-MM-DD",
  "decision_type": "calorie_adjustment|training_adjustment|exercise_substitution|deload|phase_transition|external_event_replan|tracking_change",
  "input_summary": "Concise evidence summary.",
  "change": "Exact change.",
  "reason": "Why this change is appropriate.",
  "confidence": "high|medium|low",
  "next_review_date": "YYYY-MM-DD",
  "rollback_condition": "Condition that would reverse or modify this decision."
}
```

## Rules
- If confidence is low, prefer monitoring or a smaller change.
- If data quality is low, ask for the missing key metric or delay high-impact adjustment.
- Do not use decision logs as a place for long reasoning. Keep entries compact.
