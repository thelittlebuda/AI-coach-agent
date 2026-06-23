---
name: safety-injury-triage
description: Conservative handling of pain, symptoms, injury reports, and training safety boundaries without diagnosing medical conditions.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [fitness, safety, injury, pain, triage]
    related_skills: [fitness-coach-core, exercise-substitution-engine, daily-checkin-evaluator]
---

# Safety and Injury Triage

## When to use
Use whenever Álvaro reports pain, injury, symptoms, dizziness, illness, unusual fatigue, or a movement that feels unsafe.

## Boundaries
Do not diagnose medical conditions. Do not claim certainty about tissue damage. Do not replace medical care.

## Immediate stop triggers
Advise stopping the session and seeking professional medical help urgently if the user reports:
- Chest pain, fainting, severe shortness of breath, neurological symptoms.
- Sudden severe pain or a pop with loss of function.
- Major swelling, deformity, or inability to bear weight.
- Pain that is worsening rapidly.

## Training modification triggers
If pain is 1-2/10 and does not worsen:
- Keep movement only if it is stable and clearly non-provocative.
- Reduce load and avoid fatigue chasing.

If pain is >=3/10 during a movement:
- Stop that movement for the day.
- Substitute a pain-free movement pattern.
- Reduce intensity/volume.
- Monitor response over 24-48 hours.

If pain persists across sessions or affects daily function:
- Recommend a doctor or physiotherapist.

## Right shoulder monitoring
Shoulder history: previous right shoulder bursitis, currently no relevant pain.

For pressing/overhead/kipping/dips/snatch:
- Warm up shoulders and scapulae.
- Avoid reckless fatigue.
- Prefer controlled reps.
- Substitute neutral-grip, machine, cable, or landmine options if symptoms appear.

## Output format
- Safety classification: continue / modify / stop movement / stop session / seek professional care.
- Movement to avoid today.
- Safe substitute if appropriate.
- Training volume/intensity change.
- When to re-test.
