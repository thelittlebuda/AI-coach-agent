# Hermes Fitness Coach Skills and Scripts

This package contains a Hermes-native fitness coach skeleton based on Build Plan v3.

It separates:
- Skills: procedural instructions for Hermes.
- Scripts: deterministic data handling, exports, validation, and prompt generation.
- Data files: local state and logs.
- Schemas: contracts for validation and future integrations.

## Recommended install layout

Copy each skill directory into your active Hermes profile skill directory, or point Hermes to this external skill directory if your setup supports external skill paths.

Typical local project layout:

```text
fitness-coach/
  .hermes.md
  data/
  schemas/
  skills/
  scripts/
```

Hermes skills are instructions and should not be used as mutable daily logs. Training, nutrition, body metrics, external events, and decisions should be written into `data/` files.

## First run

```bash
python scripts/bootstrap_project.py --root .
python scripts/validate_logs.py --root .
python scripts/summarize_week.py --root . --days 14 --format markdown
```

## Useful script-only cron examples

```bash
python scripts/check_missing_logs.py --root . --check bodyweight --after 10:00
python scripts/check_missing_logs.py --root . --check training --after 22:00
```

## Useful Hermes one-shot examples

```bash
python scripts/generate_today_workout_prompt.py --root . | hermes -z
python scripts/generate_weekly_review_prompt.py --root . | hermes -z
```

## Generated skills

- fitness-coach-core
- profile-manager
- training-planner
- exercise-substitution-engine
- nutrition-planner
- meal-logging-estimator
- daily-checkin-evaluator
- progress-reviewer
- external-event-handler
- data-quality-guard
- automation-gateway-operator
- tracker-integration
- decision-auditor
- safety-injury-triage

## Generated scripts

- bootstrap_project.py
- validate_logs.py
- summarize_week.py
- log_body_metric.py
- log_training_session.py
- log_nutrition_day.py
- log_decision.py
- nutrition_lookup.py
- generate_today_workout_prompt.py
- generate_weekly_review_prompt.py
- export_tracker_csv.py
- check_missing_logs.py
- compute_prs.py
- plan_to_markdown.py
- backup_data.py
