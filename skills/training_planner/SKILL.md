---
name: training-planner
description: Generates strength-focused 3+1 weekly training plans for Álvaro, including exercises, sets, reps, RPE/RIR, rest, progression, and low-energy variants.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [fitness, training, strength, hypertrophy, programming]
    related_skills: [fitness-coach-core, exercise-substitution-engine, daily-checkin-evaluator, progress-reviewer]
---

# Training Planner

## When to use
Use this skill when generating or modifying a weekly training plan, a 4-week block, a single session, a deload week, or training substitutions that affect the plan structure.

## Current default structure for Álvaro
Use 3 anchored sessions + optional 4th session.

Priority order when only 3 sessions happen:
1. Day 1: Lower strength + upper pull + short conditioning.
2. Day 2: Upper strength + posterior-chain accessory.
3. Day 3: Full-body hypertrophy + controlled weightlifting/metcon dose.
4. Day 4 optional: Zone 2 / conditioning / arms-delts-core / mobility depending on fatigue.

This is preferred over a fragile fixed 4-day plan because Álvaro sometimes trains 3 days and sometimes 4 days.

## Session constraints
- Total time: 45-60 minutes including warm-up, shower, and stretching.
- Strength work first, conditioning second.
- Warm-up: 5-8 minutes plus movement-specific ramp-up sets.
- Main lift rest: 2-4 minutes.
- Accessory rest: 60-120 seconds.
- Conditioning: 6-12 minutes if high-intensity, or 20-35 minutes if Zone 2 and session allows.
- Avoid random exercise variety. Change exercises only for clear reasons.

## Intensity language
Use RPE/RIR primarily:
- Main strength work: usually RPE 7-8, occasionally 8.5.
- Accessories: usually 1-3 RIR.
- Low-energy days: cap main lifts at RPE 7 and remove hard conditioning.

Use percentages only when an estimated 1RM is reliable.

## Programming rules
For a moderate cut with strength-focused recomposition behavior:
- Preserve intensity on main lifts.
- Keep hypertrophy volume sufficient but recoverable.
- Cap high-intensity conditioning to avoid recovery debt.
- Do not stack heavy hinge, hard metcon, and poor sleep together.
- Right shoulder: use controlled pressing volume and sensible warm-ups.

## Default weekly template
Use this as a first-pass template if no active plan exists.

### Day 1 — Lower strength + pull
- Warm-up: 5 min bike/row + hips/ankles + squat ramp-up.
- Back squat: 4 x 4-6 @ RPE 7-8, rest 2-4 min.
- Romanian deadlift: 3 x 6-8 @ RPE 7, rest 2 min.
- Pull-up or lat pulldown: 4 x 6-10 @ 1-2 RIR, rest 90-120 s.
- Split squat or leg press: 2-3 x 8-12 @ 1-3 RIR.
- Conditioning: 6-8 min bike/row intervals, hard but not maximal.

### Day 2 — Upper strength + posterior chain
- Warm-up: 5 min easy cardio + shoulder/scapula prep + bench ramp-up.
- Bench press: 4 x 4-6 @ RPE 7-8, rest 2-4 min.
- Strict press or neutral-grip DB press: 3 x 5-8 @ RPE 7, rest 2 min.
- Barbell row or chest-supported row: 4 x 6-10 @ 1-2 RIR.
- Hip thrust or hamstring curl: 3 x 8-12.
- Lateral raise + face pull: 2-3 supersets x 12-20.

### Day 3 — Full body hypertrophy + controlled metcon
- Warm-up: 5 min + dynamic prep.
- Deadlift variation or front squat: 3 x 3-5 @ RPE 7-8.
- Incline DB press or machine press: 3 x 8-12 @ 1-3 RIR.
- Seated cable row: 3 x 8-12 @ 1-2 RIR.
- Leg curl or leg extension: 2-3 x 10-15.
- Core: 2-3 sets.
- Metcon: 8-10 min controlled, no technical failure.

### Day 4 optional — Recovery-biased capacity
Choose based on fatigue:
- Good recovery: Zone 2 bike/row 25-35 min + mobility.
- Medium recovery: arms/delts/core 30-40 min + easy cardio.
- Poor recovery: mobility + walk only.

## Progression rules
- If a main lift hits the top of the rep range across all sets at target RPE for two comparable sessions, add 2.5-5 kg next time.
- For upper-body lifts, prefer 2.5 kg jumps or rep progression.
- For accessories, add reps first; add load when the top of the range is reached with clean form.
- Do not add load and volume in the same movement pattern at the same time unless the prior week was clearly underdosed.

## Deload rules
Deload for 4-7 days if two or more triggers occur:
- Main lift performance drops >5% for two sessions.
- Sleep average <6h for one week.
- Persistent joint pain >3/10.
- Resting fatigue high for 4+ days.
- Missed >=50% of sessions for two weeks.

Deload prescription:
- Volume down 30-50%.
- Loads around RPE 6-7.
- Keep movement frequency.
- Remove hard metcons.

## Required output for a weekly plan
For every session include:
- Session goal.
- Warm-up.
- Exercises.
- Sets, reps, RPE/RIR, rest.
- Conditioning or cooldown.
- Low-energy modification.
- Progression rule for the next comparable session.
