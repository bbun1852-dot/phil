#!/usr/bin/env python3
import pathlib, sys, json
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "core"))
import pmapi

for mid in sys.argv[1:]:
    m = pmapi.gamma_market(mid)
    tokens = pmapi.market_tokens(m)
    print(f"Market {mid}: question: {m.get('question')}")
    print(f"outcomes: {m.get('outcomes')}")
    print(f"tokens: {tokens}")
    for outcome, tid in (tokens or {}).items():
        q = pmapi.book_quote(tid)
        bid, ask = q["bid"], q["ask"]
        price, source = pmapi.displayed_price(tid, bid, ask) if (bid or ask) else (None, None)
        print(f"  outcome: {outcome} -> tid: {tid[:16]}... bid: {bid}, ask: {ask}, price: {price} ({source})")
