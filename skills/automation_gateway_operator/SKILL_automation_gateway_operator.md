---
name: automation-gateway-operator
description: Operates Hermes cron and messaging gateway routines for the fitness coach, including morning workouts, evening check-ins, weekly reviews, and no-agent reminders.
version: 1.0.0
author: Álvaro / ChatGPT
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, gateway, discord, telegram, automation]
    related_skills: [fitness-coach-core, data-quality-guard, progress-reviewer]
---

# Automation Gateway Operator

## When to use
Use when creating, reviewing, or modifying Hermes gateway and cron routines for the fitness coach.

## Operating model
Use two automation classes:

1. LLM-driven jobs for reasoning-heavy tasks:
- Morning workout delivery.
- Evening check-in prompts.
- Weekly review.
- Monthly progress review.

2. No-agent/script-only jobs for deterministic checks:
- Missing weigh-in reminder.
- Missing training log reminder.
- Data file validation.
- Backup/export notification.

## Security rules
Before gateway exposure:
- Confirm Discord/Telegram bot token is not in the repo.
- Restrict allowed users or use DM pairing.
- Do not enable public channel access until identity and authorization are verified.
- Prefer channel mentions unless a private fitness channel is intentionally configured as mention-free.
- Use command approvals for destructive or shell-access operations.
- Avoid giving broad terminal access to an agent reachable by unauthorized users.

## Cron prompt rules
Cron jobs run in fresh sessions. Prompts must be self-contained.

Every fitness cron prompt should include:
- Project root path.
- Relevant data files.
- The task.
- Expected output format.
- Whether to deliver or stay silent.

## Recommended jobs
### Morning workout
Schedule: 07:00 on training weekdays or daily if plan-aware.
Task: send today's workout or rest-day action from active plan.

### Evening check-in
Schedule: 20:00 daily.
Task: ask for workout completion, top sets, pain, energy, steps, calories, protein, hunger, and sleep.

### Weekly review
Schedule: Sunday evening or Monday morning.
Task: run weekly review from local data and propose next-week adjustments.

### Missing log watchdog
No-agent script-only job.
Task: if today's bodyweight or check-in is missing after a threshold time, send a concise reminder; otherwise print nothing.

## Output format for setup
Return shell commands and safety notes. Use placeholders only for secrets.
Do not print real tokens.
