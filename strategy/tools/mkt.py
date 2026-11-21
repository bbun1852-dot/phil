#!/usr/bin/env python3
"""Market id -> live book per outcome, in one call (read-only lookup).

Usage: python3 strategy/tools/mkt.py [--desc] <market_id> [<market_id> ...]

Why (cycle 2026-11-21 04:1xZ): quote.py takes token ids, but the screener
rows and siblings.py give gamma market ids, and the session sandbox blocks
ad-hoc curl/python one-liners. This bridges the two through core/pmapi.py's
read helpers. It prints, per market: question, version, negRisk, endDate,
createdAt (touch ladders: a strike counts only after creation, playbook
2026-11-13), and per outcome bid/ask/spread/top-ask size and the displayed
price score.py grades against. Moves no probability.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from core import pmapi  # noqa: E402


def main(argv):
    desc = "--desc" in argv
    ids = [a for a in argv if not a.startswith("--")]
    for mid in ids:
        try:
            m = pmapi.gamma_market(mid)
        except Exception as e:  # network or 404
            print(json.dumps({"market_id": mid, "error": str(e)[:200]}))
            continue
        row = {"market_id": mid, "question": m.get("question"),
               "version": m.get("version"), "negRisk": m.get("negRisk"),
               "end": m.get("endDate"), "created": m.get("createdAt"),
               "closed": m.get("closed"), "liq": m.get("liquidityNum"),
               "outcomes": {}}
        toks = pmapi.market_tokens(m) or {}
        for name, tid in toks.items():
            try:
                q = pmapi.book_quote(tid)
                shown, src = pmapi.displayed_price(tid, q["bid"], q["ask"])
                top = q["asks"][0][1] if q["asks"] else None
                row["outcomes"][name] = {
                    "bid": q["bid"], "ask": q["ask"],
                    "spread": round(q["ask"] - q["bid"], 4) if q["bid"] is not None and q["ask"] is not None else None,
                    "topask_sh": top, "shown": shown, "shown_src": src}
            except Exception as e:
                row["outcomes"][name] = {"error": str(e)[:120]}
        if desc:
            row["description"] = (m.get("description") or "")[:2000]
        print(json.dumps(row))


if __name__ == "__main__":
    main(sys.argv[1:])
