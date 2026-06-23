---
name: meal-logging-estimator
description: Estimates calories and protein for supermarket, restaurant, homemade, and barcode-based meals with source and confidence tagging.
version: 1.0.0
author: thelittlebuda
license: 
metadata:
  hermes:
    tags: [nutrition, logging, OpenFoodFacts, BLS, USDA, Germany]
    related_skills: [nutrition-planner, data-quality-guard]
---

# Meal Logging Estimator

## When to use
Use this skill when Álvaro logs food, asks for meal calories/macros, provides a barcode, describes a restaurant meal, or wants a German supermarket product estimated.

## Source hierarchy
Use the most specific data available:
1. User-entered nutrition label or barcode scan.
2. Open Food Facts for packaged EU/German foods.
3. German BLS database for generic foods and dishes if available locally.
4. USDA FoodData Central as fallback for generic foods.
5. Manual estimate for restaurant or unknown mixed meals.

## Required confidence labels
Every estimate must include source and confidence.

Confidence rules:
- high: exact label, barcode match, or verified product entry with serving size.
- medium: generic database match or close product match.
- low: restaurant meal, homemade dish without weights, rough portion estimate.

## Portion logic
If portion is unclear:
- Use a realistic default serving.
- State the assumed portion.
- Ask for one clarifying detail only if it materially changes the estimate.

## Restaurant and mixed meals
Return a range when uncertainty is high.

Example:
```json
{
  "food": "restaurant schnitzel with fries",
  "assumed_portion": "1 plate",
  "kcal_range": [850, 1250],
  "protein_g_range": [35, 55],
  "source": "manual_estimate",
  "confidence": "low",
  "notes": "Main uncertainty: oil, breading, fries portion, sauce."
}
```

## Logging output
If creating a log entry, use:
```json
{
  "date": "YYYY-MM-DD",
  "meal_name": "dinner",
  "items": [
    {
      "food": "Magerquark",
      "quantity": "500 g",
      "kcal": 335,
      "protein_g": 60,
      "carbs_g": 20,
      "fat_g": 1,
      "source": "label_or_database",
      "confidence": "high"
    }
  ],
  "total_kcal": 335,
  "total_protein_g": 60,
  "confidence": "high"
}
```

## Rules
- Do not overstate accuracy.
- Do not let perfect data block useful tracking.
- Prefer consistency of estimation method over false precision.
- If the user is under target protein, suggest a simple protein anchor instead of a full meal redesign.
