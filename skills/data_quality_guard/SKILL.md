---
name: data-quality-guard
description: Validates fitness logs, identifies missing/contradictory/low-confidence data, and prevents bad data from driving bad plan changes.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [fitness, data-quality, validation, reliability]
    related_skills: [fitness-coach-core, profile-manager, meal-logging-estimator, progress-reviewer]
---

# Data Quality Guard

## When to use
Use before progress reviews, calorie adjustments, weekly plan changes, or any conclusion based on logs.

## Core rule
Do not silently trust incomplete or contradictory data. Mark uncertainty explicitly and avoid high-impact adjustments when confidence is low.

## Data quality dimensions
Evaluate:
- Completeness: are required fields present?
- Recency: is data current enough for the decision?
- Consistency: do fields contradict each other?
- Plausibility: are values within realistic ranges?
- Source quality: label/database/manual estimate?
- Confidence: high/medium/low.

## Plausibility checks
Flag but do not automatically reject:
- Weight change >2 kg in one day.
- Waist change >3 cm in one week.
- Calories <1,200 or >5,000 unless clearly explained.
- Protein >300 g/day.
- Steps >40,000/day.
- Training session duration >180 min.
- Pain severity outside 0-10.
- RPE outside 1-10.

## Missing data rules
- Missing one bodyweight day: acceptable.
- Fewer than 4 weigh-ins in 7 days: weak weight trend.
- No waist measurement for 2+ weeks: do not infer recomposition strongly.
- No nutrition logs: do not adjust calories based on presumed intake.
- No exercise load data: performance signal is unknown.

## Output format
Return:
```json
{
  "data_quality": "high|medium|low",
  "usable_for_decision": true,
  "issues": [
    {"field": "body_metrics.weight_kg", "issue": "Only 2 weigh-ins in 7 days", "severity": "medium"}
  ],
  "recommended_action": "Proceed with weekly review, but do not adjust calories unless trend persists."
}
```

## Rules
- Low-confidence restaurant estimates can be used for adherence patterns, not precise calorie math.
- Do not block all coaching because data is imperfect.
- Prefer robust decisions based on multiple signals.
