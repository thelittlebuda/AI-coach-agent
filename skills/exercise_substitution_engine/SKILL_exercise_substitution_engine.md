---
name: exercise-substitution-engine
description: Provides safe, goal-preserving exercise substitutions based on equipment, fatigue, pain reports, movement pattern, and shoulder monitoring.
version: 1.0.0
author: Álvaro / ChatGPT
license: MIT
metadata:
  hermes:
    tags: [fitness, exercise-substitution, injury-monitoring, gym]
    related_skills: [training-planner, daily-checkin-evaluator, safety-injury-triage]
---

# Exercise Substitution Engine

## When to use
Use this skill when an exercise cannot be performed due to equipment availability, pain, fatigue, schedule limits, technique risk, or user preference.

## Substitution hierarchy
Preserve, in this order:
1. Safety.
2. Movement pattern.
3. Training stimulus.
4. Loadability/progression.
5. Time efficiency.
6. User preference.

## Movement pattern map
### Squat pattern
- Back squat -> front squat -> safety bar squat -> hack squat -> leg press -> goblet squat.
- If knee discomfort: reduce ROM temporarily only if pain-free, try leg press or box squat, avoid forcing depth.

### Hinge pattern
- Conventional deadlift -> trap bar deadlift -> Romanian deadlift -> rack pull -> hip thrust -> back extension.
- If low-back fatigue is high: use hip thrust, hamstring curl, or chest-supported back extension.

### Horizontal press
- Barbell bench -> dumbbell bench -> machine chest press -> push-up -> cable press.
- If shoulder symptoms: neutral-grip dumbbell press or machine press; reduce ROM if needed; avoid painful dips.

### Vertical press
- Strict press -> seated dumbbell press -> landmine press -> high-incline press -> machine shoulder press.
- If shoulder symptoms: landmine press or neutral-grip machine press; avoid high-fatigue overhead work.

### Vertical pull
- Weighted pull-up -> bodyweight pull-up -> assisted pull-up -> lat pulldown -> single-arm pulldown.

### Horizontal pull
- Barbell row -> chest-supported row -> cable row -> machine row -> one-arm dumbbell row.
- If low-back fatigue is high: prefer chest-supported or cable row.

### Weightlifting / CrossFit-style movements
- Power clean -> hang power clean -> clean pull -> kettlebell swing -> med-ball clean.
- Snatch -> hang power snatch -> high pull -> kettlebell snatch -> dumbbell snatch.
- Kipping pull-up -> strict pull-up -> assisted pull-up -> lat pulldown.
- Dips -> close-grip push-up -> machine press -> cable pressdown.

## Shoulder monitoring rules
If right shoulder pain is >=3/10 during pressing, dips, kipping, snatch, or overhead work:
- Stop the provocative movement for the day.
- Substitute a pain-free neutral-grip, machine, cable, or landmine pattern.
- Reduce load and fatigue exposure.
- Keep lower-body and non-provocative work if safe.
- Recommend doctor/physio if pain persists, worsens, or affects daily function.

## Output format
Return:
- Original exercise.
- Substitution.
- Reason.
- Preserved training stimulus.
- Exact prescription: sets, reps, RPE/RIR, rest.
- When to re-test the original exercise.
