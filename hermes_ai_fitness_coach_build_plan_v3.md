# Hermes AI Fitness Coach — Build Plan v3

Updated: 2026-06-21  
Target user: Álvaro  
Primary objective: moderate fat loss while preserving or increasing strength and muscle.

---

## 1. Executive Decision

Build this as a Hermes-native personal fitness operating system, not as a generic chatbot prompt.

The original idea is directionally good: onboarding, phase selection, weekly plan generation, daily check-ins, adaptive adjustments, and external-event handling. The main correction is architectural: **do not use Hermes skills as the primary database for daily mutable logs**. Use skills for procedures, project context files for instructions, memory for compact durable facts, and a local structured store for training/nutrition/progress data.

For Álvaro, skip generic onboarding unless data is missing. Seed the system from the known profile and only ask for new information when it materially changes execution.

Core stack:

- Hermes TUI / CLI for manual operation.
- Hermes Gateway for Discord and/or Telegram delivery.
- Hermes cron/automation for morning workout prompts, evening check-ins, weekly reviews, and monthly progress reviews.
- Local structured data store: JSONL/SQLite/CSV initially; upgrade later if needed.
- Project context file: `.hermes.md` or `AGENTS.md` for project-specific rules.
- Global `SOUL.md` only for general agent identity and tone, not project-specific fitness logic.
- Optional MCP servers later for Google Calendar, health data, nutrition databases, or fitness tracker integration.

---

## 2. Current Hermes Reality Check

### Corrected installation and launch assumptions

Use the official installer instead of the old raw GitHub script path.

```bash
# Linux, macOS, WSL2, Termux
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc   # or ~/.zshrc

# Native Windows PowerShell, if needed
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then:

```bash
hermes setup --portal      # optional, one OAuth for model + tools through Nous Portal
hermes doctor              # diagnose environment/model/tool issues
hermes update              # keep Hermes current
hermes --tui               # launch TUI explicitly
hermes --tui -c            # resume latest TUI session
```

Optional persistent TUI default:

```yaml
# ~/.hermes/config.yaml
display:
  interface: tui
```

Then `hermes` or `hermes chat` can launch the TUI depending on configuration.

### Corrected platform assumptions

The old claim “Linux, macOS, or WSL2 only; no native Windows” is obsolete. Keep macOS/Linux as the recommended production host for this project, but do not design around “Windows unsupported.”

Messaging should be part of the base architecture, not a far-future delivery swap. Hermes supports gateway operation across chat platforms. For Álvaro, prioritize Discord if that is the main agent interface; keep Telegram as a fallback or mobile reminder channel.

```bash
hermes gateway setup
hermes gateway start
```

Security must be configured before exposing the gateway:

- Restrict allowed users or use DM pairing.
- Keep bot tokens out of repo.
- Use command approvals for destructive operations.
- Prefer a sandboxed terminal backend for gateway-exposed agents when the agent can run shell commands.
- Do not allow public group/channel access until identity and authorization are verified.

### Corrected skill/memory assumptions

Hermes skills are procedural memory. They are suitable for repeatable workflows like “generate a weekly training plan” or “evaluate a check-in.” They are not ideal as a high-frequency mutable database.

Use:

- **Memory** for small durable facts: user preferences, equipment, stable health constraints, communication style.
- **Skills** for procedures: planning rules, check-in scoring, external event handling, nutrition adjustment logic.
- **Project context files** for project-specific operating rules.
- **Structured local data** for logs, bodyweight, waist, sessions, calories, decisions, and progress history.

### Corrected nutrition data assumptions

Hermes’ optional fitness/nutrition skill can use wger and USDA FoodData Central, but this is not enough for a user living in Germany.

Use data hierarchy:

1. User-entered nutrition label or barcode scan where available.
2. Open Food Facts for packaged EU/German foods.
3. German BLS database for generic foods and dishes.
4. USDA FoodData Central as fallback when EU/German data is unavailable.
5. Manual macro entries for restaurant meals, with uncertainty flag.

Do not pretend restaurant meals or mixed dishes are precise. Store estimates with confidence level.

---

## 3. Álvaro Fitness Profile Seed

Use this as the initial profile. Do not ask onboarding questions that are already answered.

```yaml
user:
  name: Álvaro
  sex: male
  age: 32
  height_cm: 190
  current_weight_kg: 100
  recent_usual_weight_kg: 105
  estimated_body_fat_pct: 27
  waist_navel_cm: 102

primary_goal: reduce_body_fat_percentage
secondary_goals:
  - preserve_or_gain_muscle
  - improve_strength
  - improve_flexibility
  - improve_cardio
  - improve_adherence

preferred_fat_loss_style: moderate
training_availability:
  days_per_week: 3-4
  preferred_days: [Monday, Tuesday, Thursday, Friday, Saturday, Sunday]
  session_duration_total_min: 45-60
  usual_time: after_19_00
  location: fully_equipped_gym

training_background:
  crossfit_years: 4
  strength_hiit_years: 4
  recent_irregular_training_months: 6
  skill_level: intermediate_to_advanced

approx_lifts:
  squat_kg: 130
  deadlift_kg: 200
  bench_press_kg: 90
  strict_press_kg: 60
  weighted_pullup_extra_kg: 9

health:
  current_injuries: none
  monitoring_points:
    - right_shoulder_previous_bursitis
  shoulder_current_status: no_relevant_pain_in_major_pressing_or_crossfit_movements

activity_recovery:
  daily_steps: 5000-6000
  cardio: cycling_to_work_15_min_each_way_when_applicable
  work: sedentary
  sleep_hours: 5-8
  sleep_quality_0_10: 6.8
  stress_0_10: 5

nutrition:
  current_intake_kcal_estimate: 1400-2200_variable
  current_protein_g_estimate: 90
  meals_per_day: 2-3
  meals_out_per_week: 4
  alcohol: beer_1_to_2_days_per_week_1_to_3_liters
  restrictions: none
  willing_to_track_calories_and_protein_weeks: 2-4

tracking:
  has_scale: true
  weigh_in_frequency: daily_or_most_days
  waist_frequency: weekly
  progress_photos_frequency_weeks: 2-4
  track_loads_reps: true
  expected_adherence_0_10: 7
```

Initial targets for the first 2–4 week calibration block:

```yaml
nutrition_targets:
  calories_kcal_per_day: 2400-2600
  protein_g_per_day: 180-210
  fiber_g_per_day: 25-40
  rate_of_loss_target_pct_bodyweight_per_week: 0.4-0.7

movement_targets:
  steps_initial_target: 7000_per_day_average
  steps_progression: add_1000_per_day_average_after_2_weeks_if_adherence_good

training_structure:
  default_split: adaptive_3_to_4_day_strength_hypertrophy
  priority_order_when_only_3_sessions: [Day_1, Day_2, Day_3]
  optional_4th_day: shorter_conditioning_hypertrophy_or_weak_points
```

---

## 4. Revised Training Phase Logic

The old phase taxonomy is useful but too rigid. Use it as a decision layer, not as a hard product boundary.

### Supported phases

| Phase | Use case | Calorie state | Max recommended block |
|---|---|---:|---:|
| Aggressive mini cut | Short controlled push, high motivation, lower training priority | Large deficit | 3–6 weeks |
| Moderate cut | Sustainable fat loss with strength retention | Moderate deficit | 8–16 weeks |
| Recomposition | Slow fat loss / muscle gain when deficit adherence is uncertain | Maintenance to slight deficit | 8–16 weeks |
| Maintenance | Recovery, diet break, habit consolidation | Maintenance | 2–8 weeks |
| Lean bulk | Muscle gain with limited fat gain | Small surplus | 12–24 weeks |
| Long bulk | Maximum muscle gain, accepting fat gain | Moderate surplus | 12–24 weeks |

For Álvaro now: **moderate cut with strength-focused recomposition behavior**.

This means:

- Moderate calorie deficit.
- High protein.
- Strength progression remains the backbone.
- Hypertrophy volume sufficient to maintain/gain muscle.
- Conditioning is present but capped so it does not compromise recovery.
- Bodyweight trend and waist drive calorie changes.

### Split decision rules v3

Do not support only “exactly three splits.” Support templates but keep choices constrained.

```text
IF available_days <= 2:
  use Minimal Full Body + steps/cardio

IF available_days == 3:
  use Full Body A/B/C OR Strength Full Body + upper/lower bias

IF available_days == 4:
  use Upper/Lower or Strength-Hypertrophy 4-day split

IF available_days == 5:
  use Upper/Lower + optional conditioning/hypertrophy day only if recovery is good

IF available_days >= 6:
  only use PPL/Arnold-style high-frequency split for short muscle-gain phases with high recovery capacity
  do not use for Álvaro's current moderate cut
```

For Álvaro: use **3 anchored sessions + optional 4th session**. This prevents failed weeks from breaking the plan.

Priority model:

1. Day 1: Lower strength + upper pull + short conditioning.
2. Day 2: Upper strength + posterior chain accessory.
3. Day 3: Full body hypertrophy + weightlifting/metcon controlled dose.
4. Day 4 optional: Zone 2 / conditioning / arms-delts-core / mobility depending on fatigue.

---

## 5. Timeline Hierarchy v3

Use a 16-week body recomposition/fat-loss arc, with 4-week mesocycles and weekly execution.

```text
16-Week Master Arc
  ├── Weeks 1-4: Calibration + Base Strength
  ├── Weeks 5-8: Progressive Overload + Movement Increase
  ├── Weeks 9-12: Consolidation + Conditioning Capacity
  └── Weeks 13-16: Fat-Loss Continuation or Maintenance Pivot

Each 4-week mesocycle
  ├── Week 1: baseline/re-entry
  ├── Week 2: progress
  ├── Week 3: progress or overload
  └── Week 4: deload/volume reduction if triggered; otherwise controlled progression

Each week
  ├── plan
  ├── execute
  ├── log
  ├── review
  └── adjust
```

Do not reject timelines shorter than 21 days as a hard failure. Instead:

- If user asks for less than 21 days, classify it as a micro-block, not a full phase.
- Explain that meaningful body composition assessment requires at least 3–4 weeks.
- Still provide an executable short-term plan if requested.

---

## 6. Data Architecture

### Do not store high-frequency logs in skills

Store daily mutable data outside skills:

```text
fitness-coach/
  README.md
  .hermes.md                         # project rules for Hermes
  config/
    coach_config.yaml
    data_sources.yaml
  data/
    profile.yaml
    active_plan.json
    nutrition_targets.json
    training_log.jsonl
    nutrition_log.jsonl
    body_metrics.csv
    external_events.jsonl
    decision_log.jsonl
    weekly_reviews.jsonl
  schemas/
    fitness_profile.schema.json
    training_session.schema.json
    nutrition_day.schema.json
    body_metric.schema.json
    weekly_review.schema.json
    decision.schema.json
  skills/
    fitness_coach_core/SKILL.md
    training_planner/SKILL.md
    nutrition_planner/SKILL.md
    daily_checkin_evaluator/SKILL.md
    progress_reviewer/SKILL.md
    external_event_handler/SKILL.md
    data_quality_guard/SKILL.md
  scripts/
    validate_logs.py
    summarize_week.py
    export_tracker_csv.py
    nutrition_lookup.py
  tests/
    test_split_rules.py
    test_calorie_adjustments.py
    test_checkin_adjustments.py
    test_external_events.py
```

### Skill responsibilities

| Skill | Purpose | Mutable data allowed? |
|---|---|---:|
| `fitness_coach_core` | coaching rules, safety boundaries, user profile interpretation | no |
| `training_planner` | generate weekly training from current phase/profile/logs | no |
| `nutrition_planner` | set targets, meal rules, alcohol handling, restaurant heuristics | no |
| `daily_checkin_evaluator` | evaluate session and produce next-session adjustment | no |
| `progress_reviewer` | weekly/monthly trend analysis and calorie/training changes | no |
| `external_event_handler` | travel, illness, pain, schedule constraints | no |
| `data_quality_guard` | validate missing, contradictory, or low-confidence inputs | no |

### Stored data entities

`training_log.jsonl` per performed session:

```json
{
  "date": "2026-06-21",
  "planned_session_id": "W01D1",
  "completed": "partial",
  "duration_min": 52,
  "exercises": [
    {"name": "Back Squat", "sets": [{"kg": 100, "reps": 5, "rpe": 7.5}]}
  ],
  "conditioning": {"type": "bike", "duration_min": 8, "intensity": "hard"},
  "energy_1_5": 4,
  "difficulty": "right",
  "pain": {"present": false, "area": null, "severity_0_10": 0},
  "notes": ""
}
```

`body_metrics.csv`:

```csv
date,weight_kg,waist_navel_cm,sleep_hours,sleep_quality_0_10,steps,resting_hr,notes
2026-06-21,100.0,102,7,6.8,6000,,baseline
```

`decision_log.jsonl`:

```json
{
  "date": "2026-06-28",
  "decision_type": "calorie_adjustment",
  "input_summary": "7d average weight unchanged for 14 days; waist unchanged; adherence 85%",
  "change": "reduce target calories by 150 kcal/day",
  "reason": "fat-loss trend below target despite adequate adherence",
  "confidence": "medium"
}
```

---

## 7. Operating Loops

### Daily loop

Morning:

- Send today’s workout or rest-day action.
- Keep message short.
- Include only today’s relevant exercises, sets, reps, RPE/RIR, and time cap.

Evening:

- Ask for check-in.
- Collect completion, top sets, pain, energy, hunger, steps, and calories/protein if tracking.
- Store data.
- Adjust only if rules are triggered.

### Weekly loop

Every Sunday evening or Monday morning:

- Compare planned vs completed sessions.
- Review 7-day average bodyweight.
- Review waist if available.
- Review calories/protein adherence.
- Review training performance on key lifts.
- Decide: maintain, increase, decrease, deload, or modify exercise selection.
- Generate next week.

### Monthly / 4-week loop

- Compare start/end weight trend, waist, photos, performance, adherence.
- Decide whether to continue cut, take maintenance week, or adjust calories/cardio.
- Keep the master arc current.

---

## 8. Adjustment Rules

### Calorie adjustment

```text
IF adherence >= 80% for 14 days
AND 7-day average weight loss < 0.2%/week
AND waist not decreasing:
  reduce calories by 150-200 kcal/day OR increase steps by 1000/day

IF weight loss > 1.0%/week
AND hunger >= 7/10 OR performance drops OR sleep worsens:
  increase calories by 100-200 kcal/day OR reduce conditioning

IF adherence < 70%:
  do not change targets first
  simplify meals, reduce tracking friction, or adjust restaurant/alcohol strategy
```

### Protein adjustment

```text
IF protein average < 160 g/day for 7 days:
  prescribe one simple protein anchor per day
  options: whey shake, skyr/quark, lean meat/fish, eggs + egg whites, high-protein ready meal

IF protein target repeatedly fails due to meal pattern:
  distribute across 2-3 meals instead of adding more meals
```

### Training adjustment

```text
IF session difficulty = too_easy for 2 comparable sessions
AND performance stable
AND no shoulder/pain issue:
  increase load 2.5-5% on main lift OR add 1 set to accessory, not both

IF session difficulty = too_hard OR completion < 70%:
  reduce next comparable session by 1 working set per main pattern OR reduce load 5-10%

IF sleep < 6h for 2 consecutive nights OR fatigue >= 8/10:
  cap session at RPE 7 and remove high-intensity conditioning

IF right shoulder pain >= 3/10 during pressing/overhead/dips/kipping:
  stop provocative movement for that day
  substitute neutral-grip or machine pattern
  avoid high-fatigue overhead work
  recommend physio/doctor if pain persists, worsens, or affects daily function
```

### Deload triggers

Deload for 4–7 days if two or more occur:

- Main lift performance drops >5% for two sessions.
- Sleep average <6h for one week.
- Persistent joint pain >3/10.
- Resting fatigue high for 4+ days.
- Missed ≥50% of sessions for two weeks.

Deload prescription:

- Keep movement frequency.
- Reduce volume 30–50%.
- Keep loads around RPE 6–7.
- Remove hard metcons.

---

## 9. Communication Contracts

The coach should be direct and execution-focused.

Do:

- Give exact next action.
- Use numbers: calories, protein, sets, reps, RPE/RIR, rest times.
- Flag uncertainty explicitly.
- Distinguish “known from data” vs “estimate.”
- Make the smallest change that solves the problem.
- Prioritize adherence over theoretical optimality.

Do not:

- Over-motivate.
- Diagnose injuries.
- Change the whole plan after one bad day.
- Treat body-fat estimates as precise.
- Add random exercise variation unless there is a reason.
- Store noisy daily data in long-term memory.

---

## 10. Hermes Project Context File

Recommended file: `.hermes.md` in the project root.

```markdown
# Hermes Fitness Coach Project Context

You are operating as Álvaro's personal fitness coach system.

Default language: Spanish for conversation. English is acceptable for code, schemas, prompts, and technical artifacts.

Mission: help Álvaro reduce body fat percentage while preserving or gaining muscle and strength. Secondary goals: flexibility, cardio, health, adherence.

Known user profile:
- Male, 32, 190 cm, 100 kg, estimated BF around 27%, waist at navel 102 cm.
- Training background: ~4 years CrossFit, ~4 years strength/HIIT, recent 6 months irregular.
- Approx lifts: squat 130 kg, deadlift 200 kg, bench 90 kg, strict press 60 kg, weighted pull-up +9 kg.
- Availability: 3-4 gym sessions/week, 45-60 min including warm-up, shower, stretching, usually after 19:00.
- Gym: fully equipped.
- Shoulder: previous right shoulder bursitis, currently no relevant pain. Monitor pressing/overhead/kipping/dips/snatch volume.
- Nutrition: current protein likely low (~90 g/day), intake variable, willing to track calories/protein for 2-4 weeks, no restrictions.
- Priority when goals conflict: reduce body fat percentage, not aggressive performance maximization.

Coaching rules:
- Do not ask onboarding questions already answered here.
- Ask clarifying questions only when missing data materially changes the decision.
- Use moderate deficit, high protein, progressive strength training, controlled conditioning, and gradually increased daily movement.
- Prefer 3 anchored sessions + optional 4th session over fragile 4-day-only plans.
- Use 7-day average bodyweight, waist, performance, hunger, recovery, and adherence for adjustments.
- Make small controlled changes: calories +/-150-200 kcal, steps +1000/day, volume +/-1 set, load +/-2.5-10% depending on context.
- Do not diagnose pain or medical issues; refer to doctor/physio for significant, persistent, or worsening symptoms.
- Keep answers practical, direct, and specific.

Data rules:
- Skills store procedures, not logs.
- Store daily logs in data/*.jsonl or CSV.
- Every adjustment must write or propose a decision_log entry with input summary, change, reason, and confidence.
- Mark restaurant/alcohol estimates as low or medium confidence unless exact labels are provided.
```

---

## 11. Skill Templates

### `fitness_coach_core/SKILL.md`

```markdown
# Fitness Coach Core

## When to use
Use for any request about Álvaro's training, nutrition, body recomposition, adherence, progress review, fatigue, or fitness planning.

## Core objective
Primary: reduce body fat percentage moderately while preserving or gaining muscle and strength.

## Non-negotiables
- Use Álvaro's known profile when available.
- Do not create a full new plan unless asked or unless a scheduled weekly/monthly planning loop requires it.
- Do not change calories/training after one noisy data point.
- Use 7-day average weight and weekly waist as primary body-composition signals.
- Treat right shoulder as a monitoring point.
- Do not diagnose injuries.

## Execution style
Be direct, practical, and numeric. Avoid motivational fluff.

## Standard outputs
For plan changes, include:
1. What changes.
2. Why it changes.
3. What stays the same.
4. How to measure whether it worked.
```

### `daily_checkin_evaluator/SKILL.md`

```markdown
# Daily Check-in Evaluator

## Input required
- Planned session.
- Actual completion.
- Main lift top sets or completed sets.
- Difficulty: too_easy / right / too_hard.
- Energy 1-5.
- Pain: area, severity 0-10, movement trigger.
- Optional: steps, calories, protein, hunger, sleep.

## Evaluation
Score is not a moral score. It is an execution-readiness score.

Weights:
- Completion: 30%
- Performance vs expected: 25%
- Pain/safety: 20%
- Energy/recovery: 15%
- Nutrition/movement adherence if available: 10%

## Adjustment rules
- Too easy twice + no pain + good recovery: add load OR one accessory set, not both.
- Too hard or partial: reduce next comparable session volume or load.
- Pain >=3/10: replace provocative movement, keep non-provocative work.
- Poor sleep/fatigue: remove hard conditioning first.

## Output format
- Session assessment: 2-4 lines.
- Next-session change: exact sets/reps/load/RPE change.
- Decision log draft.
- One practical instruction for tomorrow.
```

### `progress_reviewer/SKILL.md`

```markdown
# Progress Reviewer

## Weekly review inputs
- 7-day average bodyweight this week vs prior week.
- Waist at navel.
- Planned vs completed workouts.
- Key lift performance.
- Calories/protein averages.
- Steps average.
- Hunger, sleep, fatigue.
- Alcohol intake.

## Decision rules
- If adherence is low, fix adherence before changing physiology targets.
- If adherence is good and trend is too slow, reduce calories 150-200 or increase steps.
- If trend is too fast and performance/recovery suffers, increase calories 100-200 or reduce conditioning.
- If waist decreases but weight is stable and performance improves, continue.

## Output
- Trend diagnosis.
- Keep/change decision.
- Next week targets.
- Risks to monitor.
- Decision log entry.
```

---

## 12. Prompt Templates

### Seed profile prompt

```text
Use the known profile below as the starting profile. Do not ask for missing information unless it materially changes today's decision.

Known profile: {profile_yaml}
Current active plan: {active_plan_json}
Recent logs: {recent_training_and_body_metrics}

Task: {user_request}

Respond in Spanish. Be direct, practical, numeric, and clear about uncertainty.
```

### Daily workout delivery prompt

```text
You are sending Álvaro today's workout.

Inputs:
- Active weekly plan: {weekly_plan}
- Today's date: {date}
- Recent fatigue/pain notes: {recent_checkins}
- Time cap: 45-60 min total including warm-up and cooldown

Output:
1. Today's goal.
2. Warm-up: 5-8 min.
3. Main work: exercises, sets, reps, RPE/RIR, rest.
4. Conditioning or cooldown.
5. Low-energy modification.

Keep it concise. Do not redesign the week.
```

### Daily check-in prompt

```text
Evaluate this check-in against the active plan.

Profile: {profile}
Planned session: {planned_session}
Actual check-in: {checkin}
Recent 7-day context: {recent_context}

Tasks:
1. Determine whether the session was completed, partial, or skipped.
2. Identify performance signal: up / stable / down / unknown.
3. Identify safety signal, especially right shoulder.
4. Decide next-session adjustment: maintain / increase / decrease / substitute / rest.
5. Draft a decision_log entry.

Rules:
- Do not overreact to one isolated bad day.
- Be specific: exact set/load/RPE/conditioning change.
- If pain is significant or persistent, advise doctor/physio.

Output in Spanish.
```

### Weekly review prompt

```text
Run Álvaro's weekly fitness review.

Inputs:
- Body metrics for last 14 days: {body_metrics}
- Training log for last 14 days: {training_log}
- Nutrition log for last 14 days: {nutrition_log}
- Active targets: {targets}
- External events: {events}

Tasks:
1. Compare 7-day average weight trend.
2. Compare waist trend.
3. Review adherence: training, protein, calories, steps.
4. Review performance and recovery.
5. Decide whether to keep or adjust calories, protein, steps, training volume, conditioning.
6. Generate next week's plan if needed.
7. Create a decision_log entry.

Output:
- Diagnosis.
- Changes for next week.
- Exact targets.
- What to monitor.
```

### External event prompt

```text
Álvaro reported an external constraint: {event_message}

Inputs:
- Current plan: {active_plan}
- Calendar/schedule if available: {calendar_context}
- Recent logs: {recent_logs}

Classify event:
- travel
- illness
- injury/pain
- work schedule conflict
- social event/alcohol
- equipment limitation
- other

Determine:
1. Impact window.
2. Sessions affected.
3. Best resolution: shift / compress / substitute / skip / deload.
4. Nutrition adjustment if relevant.
5. Decision log entry.

Rules:
- Preserve weekly priority sessions if possible.
- Do not cram missed high-fatigue work into consecutive days.
- For pain/injury: conservative substitution and referral if needed.
```

---

## 13. Automation Plan

Use two types of automation.

### LLM-driven cron jobs

Use for reasoning-heavy summaries or plan generation.

Examples:

```bash
hermes cron create "0 7 * * 1-5" \
  "Send Álvaro today's workout or rest-day action from the active fitness plan. Use the fitness coach project context and recent logs. Keep it concise." \
  --name "fitness-morning-workout" \
  --deliver discord

hermes cron create "0 20 * * *" \
  "Ask Álvaro for a fitness check-in: workout completion, top sets, pain, energy, steps, calories, protein, hunger, and sleep. Keep it short." \
  --name "fitness-evening-checkin" \
  --deliver discord

hermes cron create "0 19 * * 0" \
  "Run Álvaro's weekly fitness review using the local fitness-coach data files, then propose next-week adjustments." \
  --name "fitness-weekly-review" \
  --deliver discord
```

### No-agent/script-only jobs

Use when no reasoning is needed.

Examples:

- Check whether `body_metrics.csv` has a weigh-in today.
- Check whether `training_log.jsonl` has a completed session after a planned workout.
- Send a fixed reminder if no log exists by 22:00.

No-agent jobs reduce model cost and avoid unnecessary sessions.

---

## 14. Data Source Integration Plan

### Exercise database

Use wger as the first exercise database because it is open-source and has a REST API. Use it for exercise metadata, muscle groups, equipment tags, and substitutions. Do not let it override the coach's programming logic.

### Nutrition databases

Use the following source order:

```text
IF barcode or packaged German/EU food:
  query Open Food Facts
ELSE IF generic German food/dish:
  query BLS
ELSE IF not found:
  query USDA FoodData Central
ELSE:
  manual estimate and mark low confidence
```

Store nutrition estimates with:

```json
{
  "food": "restaurant schnitzel meal",
  "kcal": 950,
  "protein_g": 45,
  "source": "manual_estimate",
  "confidence": "low"
}
```

---

## 15. Revised Sprint Plan

### Sprint 0 — Repo cleanup and Hermes setup

Exit criteria:

- `.hermes.md` created.
- `README.md` explains the project.
- `data/`, `schemas/`, `skills/`, `scripts/`, `tests/` created.
- Hermes updated and verified with `hermes doctor`.
- Gateway security configured if using Discord/Telegram.

### Sprint 1 — Manual TUI core loop

Build:

- Seed profile.
- Active 4-week plan file.
- Manual daily check-in prompt.
- Daily evaluator skill.
- Decision log.

Exit criteria:

- Manual flow works: show workout → receive check-in → evaluate → write decision → adjust next comparable session.

### Sprint 2 — Data validation and weekly review

Build:

- JSON schemas.
- `validate_logs.py`.
- Weekly review skill.
- Calorie/step/training adjustment rules.

Exit criteria:

- Weekly review produces stable, explainable adjustments from data.
- Bad/missing data is flagged instead of silently trusted.

### Sprint 3 — Gateway + scheduled routines

Build:

- Discord or Telegram delivery.
- Morning workout automation.
- Evening check-in automation.
- Weekly review automation.
- Message debouncing if platform spam/double-texting becomes an issue.

Exit criteria:

- Coach works from mobile/chat without opening the TUI.
- Unauthorized users cannot interact with the bot.

### Sprint 4 — Nutrition data adapter

Build:

- Open Food Facts lookup.
- BLS lookup/download workflow.
- USDA fallback.
- Restaurant/manual estimate rules.

Exit criteria:

- User can log common German supermarket foods with reasonable accuracy.
- Every nutrition estimate has source and confidence.

### Sprint 5 — Fitness tracker integration

Build:

- Export current plan to tracker UI.
- Import completed session logs from tracker.
- Sync PRs and weekly volume.
- Keep Hermes as coach/decision layer, not necessarily the UI.

Exit criteria:

- Tracker becomes the data input/output surface; Hermes remains the adaptive planning layer.

---

## 16. Test Scenarios

### Check-in tests

1. Completed session, too easy, no pain → maintain unless repeated twice; then small progression.
2. Partial session, poor sleep → reduce next comparable session; remove hard conditioning.
3. Shoulder pain during overhead press → substitute and flag monitoring.
4. Missed workout due to work trip → shift priority sessions; do not cram.
5. Weight unchanged for 14 days with good adherence → calorie or step adjustment.
6. Weight stable but waist down and strength up → continue.
7. Low protein adherence → add protein anchor, not full diet redesign.
8. High alcohol weekend → account for calories/recovery; do not moralize.

### Acceptance criteria

- Every plan fits 45–60 min.
- Every strength session has sets, reps, RPE/RIR, rest times.
- Every adjustment has a reason.
- Every nutrition estimate has source/confidence.
- Every pain report is handled conservatively.
- System does not ask already-known onboarding questions.
- System does not store noisy logs in memory or skills.

---

## 17. Main Gaps Fixed From v2

| Gap in v2 | v3 fix |
|---|---|
| Treats skills as mutable app state | Uses skills for procedures and local data files for logs |
| Generic onboarding despite known user profile | Seeds Álvaro's profile and asks only material missing questions |
| Outdated install path and Windows assumption | Uses current installer and acknowledges native Windows support |
| Telegram treated as future-only | Makes gateway/chat delivery part of base architecture |
| No security model | Adds allowlist/DM pairing, bot-token hygiene, command approvals, sandbox recommendation |
| No data provenance | Adds source/confidence for nutrition and decision log for changes |
| Too rigid split logic | Uses adaptive 3+1 structure for Álvaro's real 3–4 day availability |
| No nutrition-data localization | Adds Open Food Facts + BLS + USDA fallback hierarchy |
| No testing strategy | Adds test scenarios and acceptance criteria |
| No adherence-first logic | Adjusts targets only after adherence quality is known |

---

## 18. Immediate Next Build Order

1. Create project folder and `.hermes.md`.
2. Add `data/profile.yaml` using the seed profile above.
3. Add `data/body_metrics.csv` with current baseline.
4. Add `data/active_plan.json` for first 4-week block.
5. Add the three core skills first:
   - `fitness_coach_core`
   - `daily_checkin_evaluator`
   - `progress_reviewer`
6. Test manually in TUI for one simulated week.
7. Only then add gateway/cron delivery.

Do not start with a complex multi-agent system. The first reliable product is a tight loop: plan → execute → log → review → adjust.
