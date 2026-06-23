---
name: daily-checkin-evaluator
description: Evaluates daily training, nutrition, pain, energy, and recovery check-ins and produces controlled next-session adjustments.
version: 1.0.0
author: thelittlebuda
metadata:
  hermes:
    tags: [fitness, check-in, adjustment, autoregulation]
    related_skills: [fitness-coach-core, training-planner, exercise-substitution-engine, decision-auditor]
---

# Daily Check-in Evaluator

## When to use
Use after Álvaro reports a workout, missed workout, rest day, pain, energy, hunger, sleep, calories, protein, or steps.

## Required input
Minimum useful check-in:
- Planned session or planned rest day.
- Completed / partial / skipped.
- Main lifts or top sets if trained.
- Difficulty: too_easy / right / too_hard.
- Energy 1-5.
- Pain: area, severity 0-10, movement trigger.

Optional but useful:
- Steps.
- Calories.
- Protein.
- Hunger 1-10.
- Sleep hours and quality.
- Notes.

## Scoring model
The score is execution readiness, not a moral score.

Weights:
- Completion: 30%.
- Performance vs expected: 25%.
- Pain/safety: 20%.
- Energy/recovery: 15%.
- Nutrition/movement adherence if available: 10%.

Interpretation:
- 8-10: strong execution; continue or progress if repeated.
- 6-7: acceptable; usually maintain.
- 4-5: partial or recovery-constrained; reduce next comparable dose.
- 1-3: safety/recovery issue or missed session; simplify and protect priority work.

## Adjustment rules
- If too_easy for 2 comparable sessions, performance stable/up, and no pain: increase load 2.5-5% on main lift OR add one accessory set, not both.
- If too_hard or completion <70%: reduce next comparable session by one working set per main pattern OR reduce load 5-10%.
- If sleep <6h for 2 consecutive nights or fatigue >=8/10: cap next session at RPE 7 and remove high-intensity conditioning.
- If right shoulder pain >=3/10 during pressing/overhead/dips/kipping/snatch: stop provocative movement, substitute neutral-grip/machine/landmine option, avoid high-fatigue overhead work.
- If pain is significant, persistent, worsening, or affects daily function: recommend doctor/physio.
- Do not modify calories because of one day unless safety or extreme intake is relevant.

## Output format
Return:
1. Session assessment: 2-4 lines.
2. Classification: completed / partial / skipped.
3. Performance signal: up / stable / down / unknown.
4. Safety signal: clear / monitor / substitute / stop-and-refer.
5. Next-session adjustment with exact prescription.
6. Decision log draft.
7. One practical instruction for tomorrow.

## Decision log draft schema
```json
{
  "date": "YYYY-MM-DD",
  "decision_type": "training_adjustment",
  "input_summary": "Partial session; sleep 5.5h; shoulder pain 0/10; difficulty too_hard.",
  "change": "Reduce next squat accessory volume from 3 sets to 2 sets and remove hard conditioning.",
  "reason": "Completion and recovery were below target; protect strength work and adherence.",
  "confidence": "medium",
  "next_review_date": "YYYY-MM-DD"
}
```
