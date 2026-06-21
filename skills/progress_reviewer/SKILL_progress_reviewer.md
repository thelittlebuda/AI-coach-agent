---
name: progress-reviewer
description: Runs weekly and 4-week reviews using bodyweight averages, waist, training, nutrition, steps, recovery, and adherence to adjust targets.
version: 1.0.0
author: Álvaro / ChatGPT
license: MIT
metadata:
  hermes:
    tags: [fitness, progress-review, analytics, calorie-adjustment, weekly-review]
    related_skills: [fitness-coach-core, nutrition-planner, training-planner, decision-auditor]
---

# Progress Reviewer

## When to use
Use this skill for weekly reviews, monthly reviews, 4-week mesocycle reviews, phase decisions, calorie adjustments, and progress diagnosis.

## Weekly review inputs
Required if available:
- Body metrics for the last 14 days.
- 7-day average bodyweight this week and prior week.
- Waist at navel.
- Training sessions planned vs completed.
- Key lift performance.
- Calories average.
- Protein average.
- Steps average.
- Hunger, sleep, fatigue.
- Alcohol intake.
- External events.

## Core analysis rules
- Bodyweight alone is not enough; compare weight, waist, performance, and adherence.
- If adherence is low, fix adherence before changing targets.
- If waist decreases but scale weight is stable and performance improves, continue.
- If scale weight drops fast but performance/recovery worsens, reduce deficit or conditioning.
- If no trend change for 14 days with good adherence, change calories or steps.

## Adjustment thresholds
- Good adherence: >=80% target compliance.
- Low adherence: <70% target compliance.
- Slow loss: <0.2% bodyweight/week for 14 days with waist unchanged.
- Target loss: 0.4-0.7% bodyweight/week.
- Fast loss: >1.0% bodyweight/week, especially with hunger/recovery/performance issues.

## Decisions
Available decisions:
- Maintain targets.
- Reduce calories by 150-200 kcal/day.
- Increase calories by 100-200 kcal/day.
- Add 1,000 steps/day average.
- Reduce conditioning.
- Reduce training volume or deload.
- Simplify nutrition adherence.
- Add a daily protein anchor.
- Start a maintenance/diet-break week if recovery/adherence requires it.

## Output format
Return:
- Diagnosis.
- Evidence used.
- Keep/change decision.
- Exact targets for next week.
- Training modifications if any.
- Nutrition modifications if any.
- Risks to monitor.
- Decision log entry.

## Avoid
- Do not call a plateau from less than 14 days of data.
- Do not punish a single social/alcohol day with aggressive restriction.
- Do not increase training volume while recovery and adherence are poor.
- Do not treat body-fat estimate as a precise weekly signal.
