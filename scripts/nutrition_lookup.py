#!/usr/bin/env python3
"""Lookup packaged foods in Open Food Facts or create a manual estimate stub.

This script uses only the Python standard library. It requires internet access for
Open Food Facts lookups. If lookup fails, it returns a manual-estimate template.
"""
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-fitness-coach/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def by_barcode(barcode: str) -> dict:
    url = f"https://world.openfoodfacts.org/api/v2/product/{urllib.parse.quote(barcode)}.json"
    data = fetch_json(url)
    if data.get("status") != 1:
        return manual_stub(barcode, "barcode_not_found")
    p = data.get("product", {})
    n = p.get("nutriments", {})
    return {
        "food": p.get("product_name") or barcode,
        "brand": p.get("brands"),
        "quantity": p.get("quantity"),
        "kcal_per_100g": n.get("energy-kcal_100g"),
        "protein_g_per_100g": n.get("proteins_100g"),
        "carbs_g_per_100g": n.get("carbohydrates_100g"),
        "fat_g_per_100g": n.get("fat_100g"),
        "fiber_g_per_100g": n.get("fiber_100g"),
        "source": "open_food_facts_barcode",
        "confidence": "high",
        "url": p.get("url"),
    }


def by_search(query: str) -> dict:
    params = urllib.parse.urlencode({"search_terms": query, "search_simple": 1, "action": "process", "json": 1, "page_size": 5})
    url = f"https://world.openfoodfacts.org/cgi/search.pl?{params}"
    data = fetch_json(url)
    products = data.get("products", [])
    if not products:
        return manual_stub(query, "search_not_found")
    out = []
    for p in products[:5]:
        n = p.get("nutriments", {})
        out.append({
            "food": p.get("product_name"),
            "brand": p.get("brands"),
            "quantity": p.get("quantity"),
            "kcal_per_100g": n.get("energy-kcal_100g"),
            "protein_g_per_100g": n.get("proteins_100g"),
            "source": "open_food_facts_search",
            "confidence": "medium",
            "url": p.get("url"),
        })
    return {"query": query, "matches": out, "source": "open_food_facts_search", "confidence": "medium"}


def manual_stub(food: str, reason: str) -> dict:
    return {
        "food": food,
        "source": "manual_estimate_required",
        "confidence": "low",
        "reason": reason,
        "required_inputs": ["portion size", "label if available", "cooking method", "sauce/oil details if restaurant meal"],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--barcode")
    g.add_argument("--query")
    args = p.parse_args()
    try:
        result = by_barcode(args.barcode) if args.barcode else by_search(args.query)
    except Exception as exc:
        result = manual_stub(args.barcode or args.query, f"lookup_error: {exc}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
