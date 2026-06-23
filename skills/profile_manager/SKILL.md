---
name: profile-manager
description: Maintains Álvaro's stable fitness profile, distinguishes durable profile changes from noisy daily logs, and updates profile data safely.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [fitness, profile, memory, onboarding, data-governance]
    related_skills: [fitness-coach-core, data-quality-guard]
---

# Profile Manager

## When to use
Use this skill when the user reports a stable change to body metrics, goals, injuries, equipment, schedule, food restrictions, preferences, or tracking ability.

Do not use this skill for ordinary daily logs. Daily logs belong in `data/*.jsonl` or CSV files.

## Stable profile fields
Store or update durable facts such as:
- Current bodyweight baseline after a meaningful change.
- Waist baseline after a new measurement cycle starts.
- Training availability.
- Equipment access.
- Medical restrictions stated by a doctor/physio.
- Persistent pain or resolved pain status.
- Dietary restrictions, allergies, or new excluded foods.
- Long-term schedule constraints.
- Preference changes that affect adherence.

## Non-profile data
Do not write these into profile or memory:
- Single-day bodyweight.
- One-off bad workout.
- One restaurant meal.
- One high-alcohol weekend.
- Temporary travel unless it affects multiple weeks.
- Short-term soreness.

## Update protocol
Before changing profile data:
1. Identify the field being changed.
2. Identify whether the update is durable or temporary.
3. Compare it with existing profile data if available.
4. If contradictory, ask one focused clarification or mark the entry as uncertain.
5. Write or propose a structured profile update.

## Output format
When updating profile, return:

```json
{
  "profile_update": {
    "field": "training_availability.days_per_week",
    "old_value": "3-4",
    "new_value": "4",
    "effective_date": "YYYY-MM-DD",
    "durability": "stable|temporary|unknown",
    "reason": "User reported a schedule change.",
    "confidence": "high|medium|low"
  }
}
```

## Rules
- Prefer local `data/profile.yaml` as source of truth for the fitness project.
- Use Hermes memory only for compact durable facts that should carry across conversations.
- Do not overwrite the profile silently.
- Do not treat user-reported body-fat percentage as precise.
