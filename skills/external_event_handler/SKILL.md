---
name: external-event-handler
description: Replans training and nutrition around travel, illness, work conflicts, social events, equipment limits, and pain without breaking the master arc.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [fitness, replanning, travel, schedule, constraints]
    related_skills: [training-planner, nutrition-planner, exercise-substitution-engine, decision-auditor]
---

# External Event Handler

## When to use
Use when Álvaro reports any external constraint that affects plan execution:
- Travel.
- Illness.
- Injury or pain.
- Work schedule conflict.
- Social event or high-alcohol day.
- No gym access.
- Sleep disruption.
- Equipment limitation.
- Unexpected missed session.

## Classification
Classify event as:
- travel
- illness
- injury_or_pain
- work_schedule_conflict
- social_event_alcohol
- equipment_limitation
- recovery_constraint
- other

## Replanning principles
- Preserve the highest-priority sessions first.
- Do not cram missed high-fatigue work into consecutive days.
- Shift before compressing.
- Substitute before skipping when stimulus can be preserved safely.
- Skip low-priority accessories before cutting main strength work.
- Replace gym training with walking, hotel-gym full body, mobility, or Zone 2 if needed.
- For illness: reduce intensity and avoid hard conditioning until recovered.
- For pain: substitute conservatively and refer when needed.

## Impact analysis steps
1. Identify the impact window.
2. Identify sessions affected.
3. Identify nutrition impact if relevant.
4. Choose one resolution: shift, compress, substitute, skip, deload, or maintenance pivot.
5. Draft decision log entry.
6. State what is preserved and what is lost.

## Common resolutions
### 1-day schedule conflict
Move the affected session to the next available day if it does not create heavy sessions back-to-back. Otherwise, skip optional Day 4.

### 2-4 day trip with no gym
Use one hotel/home full-body session and keep steps high. Resume anchored sessions after return.

### Social event with alcohol
Preserve protein and weekly calories. Avoid hard conditioning the next morning if sleep is poor. Do not prescribe crash compensation.

### Shoulder pain
Remove provocative upper-body movement immediately. Keep lower-body and pain-free pulling. Use exercise-substitution-engine.

### Illness
If fever/systemic symptoms: rest or light walking only and recommend medical care if severe. If mild symptoms: easy movement, no hard metcon.

## Output format
- Event classification.
- Impact window.
- Plan change.
- Nutrition change if any.
- What stays unchanged.
- Decision log draft.
