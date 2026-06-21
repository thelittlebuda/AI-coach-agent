---
name: tracker-integration
description: Defines how Hermes should exchange plans, workout logs, PRs, and weekly volume data with a fitness tracker UI or Canvas app.
version: 1.0.0
author: Álvaro / ChatGPT
license: MIT
metadata:
  hermes:
    tags: [fitness, tracker, csv, integration, app]
    related_skills: [training-planner, progress-reviewer, data-quality-guard]
---

# Tracker Integration

## When to use
Use when exporting plans to a tracker, importing completed workouts, syncing PRs, generating dashboards, or mapping Hermes decisions to app state.

## Architectural rule
Hermes is the coach and decision layer. The tracker is the input/output surface. Do not let the UI become the source of coaching logic.

## Export responsibilities
Export from Hermes/local data to tracker:
- Active weekly plan.
- Exercise list.
- Sets, reps, RPE/RIR, rest.
- Warm-ups and cooldowns.
- Optional 4th day.
- Low-energy variants.
- Target calories/protein.

## Import responsibilities
Import from tracker to local data:
- Completed sessions.
- Set-level loads and reps.
- Duration.
- PR flags.
- Exercise notes.
- Pain notes.
- Body metrics if captured.

## Data mapping
Workout screen fields should map to `training_log.jsonl`:
- workout date -> `date`
- planned session id -> `planned_session_id`
- exercise name -> `exercises[].name`
- set number -> `exercises[].sets[]`
- weight -> `kg`
- reps -> `reps`
- RPE -> `rpe`
- completed checkmark -> `completed_sets`
- pain note -> `pain`

Progress screen fields:
- weekly volume by muscle group -> derived from completed sets and exercise metadata.
- PRs -> computed from historical set data.
- adherence -> completed sessions / planned sessions.

## Sync rules
- Never overwrite raw logs without backup.
- If tracker data and Hermes data conflict, preserve both and flag conflict.
- PRs should be derived, not manually trusted unless user confirms.
- Imported data must pass data-quality checks before driving adjustments.

## Output format
For any integration task, provide:
- Source data file.
- Destination format.
- Mapping table.
- Conflict handling.
- Validation steps.
