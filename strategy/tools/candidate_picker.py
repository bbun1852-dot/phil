#!/usr/bin/env python3
"""Inspect market details by market ID."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "core"))

import pmapi

def main():
    if len(sys.argv) < 2:
        print("Usage: candidate_picker.py <market_id> ...")
        return
    for mid in sys.argv[1:]:
        matches = pmapi.gamma_markets(id=mid)
        if not matches:
            print(f"Market {mid} not found")
            continue
        m = matches[0]
        token_ids = pmapi.token_ids(m)
        out = {
            "id": m.get("id"),
            "question": m.get("question"),
            "end_date": m.get("endDate"),
            "outcomes": m.get("outcomes"),
            "outcome_prices": m.get("outcomePrices"),
            "tokens": token_ids,
            "description": m.get("description"),
        }
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
