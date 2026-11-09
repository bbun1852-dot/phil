#!/usr/bin/env python3
import datetime as dt
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# 1. Merge funnel row
funnel_payload = {
    "mode": "paper",
    "screener": "unscreened fallback per CYCLE.md & Argon-Pro Protocol to preserve Gemini daily RPD budget; researched 6 candidate markets from active scan pool across CPI, commodities, metals, and tech product releases",
    "researched": [
        {
            "market_id": "6747249",
            "category": "commodities",
            "skip_reason": "market-agrees",
            "forecast_id": "29c7d7e644c2",
            "note": "WTI close > $85 on Nov 9: spot at $87.19-$89.85 with ~9h left, well above strike. P(Close>85)~0.85 vs book 0.823/0.841 mid 0.832. Market agrees."
        },
        {
            "market_id": "6902983",
            "category": "commodities",
            "skip_reason": "wide-spread-veto",
            "forecast_id": "935fdfa4cab2",
            "note": "WTI close > $87 on Nov 10: spot at $87.50, strike $87 ATM with 1d left. Own 0.50 vs mid 0.48. Book 0.44/0.52 spread 0.08 > max_spread 0.06 -> wide-spread-veto."
        },
        {
            "market_id": "6764511",
            "category": "commodities-touch",
            "skip_reason": "wide-spread-veto",
            "forecast_id": "4b7e648c352a",
            "note": "Henry Hub NG hit High $3.50 wk of Nov 9: spot around $2.80-$3.00, needs +20% spike in 4d. Base rate ~0.18. Book 0.18/0.29 spread 0.11 > max_spread 0.06 -> wide-spread-veto; stale last trade 0.85."
        },
        {
            "market_id": "6764491",
            "category": "commodities-touch",
            "skip_reason": "market-agrees",
            "forecast_id": "bbdf1e3f51c4",
            "note": "Silver XAGUSD hit Low $49 wk of Nov 9: spot at $52.50, $49 is -6.7% away with 5d left. Weekly sigma ~4.5% gives P(touch 49)~0.20 vs book 0.17/0.21 mid 0.19. Market agrees."
        },
        {
            "market_id": "6066698",
            "category": "product-release",
            "skip_reason": "market-agrees",
            "forecast_id": "1b5a756bb2bd",
            "note": "Anthropic IPO by Nov 20: S-1/A filed Nov 2, targeting week of Nov 16 before Thanksgiving. Tech market volatility creates slight timing risk. Own 0.53 vs book 0.52/0.53 mid 0.525. Market agrees."
        },
        {
            "market_id": "5699270",
            "category": "econ-cpi",
            "skip_reason": "wide-spread-veto",
            "forecast_id": "73656270e2f3",
            "note": "Oct Core CPI MoM 0.1%: consensus 0.20%, Cleveland Fed Nowcast 0.21%. 0.1% is -1 sigma tail P~0.10. Book 0.01/0.14 spread 0.13 > max_spread 0.06 -> wide-spread-veto."
        }
    ],
    "placed": 0,
    "settled": {"bets": 0, "forecasts": 0},
    "mech": "skipped (operator runner, no signer)",
    "headline_arena": []
}

tmp_file = ROOT / "strategy" / "tools" / "funnel_merge.json"
tmp_file.write_text(json.dumps(funnel_payload, indent=2))

res = subprocess.run(
    ["python3", "core/funnel.py", "merge", "--cycle", "2026-11-09T14:12:25Z", "--file", str(tmp_file)],
    capture_output=True, text=True, check=True
)
print("funnel merge:", res.stdout.strip())
tmp_file.unlink(missing_ok=True)

# 2. Update schedule.json
sched_path = ROOT / "strategy" / "schedule.json"
sched = json.loads(sched_path.read_text())
sched["next_full_cycle_after"] = "2026-11-09T20:00:00Z"
sched["reason"] = "FULL cycle completed (oracle-gemini, gemini-3.8-flash): settled 0, placed 0, recorded 6 forecasts, unscreened fallback under Argon-Pro Protocol. Next FULL after 20:00Z."
sched_path.write_text(json.dumps(sched, indent=2) + "\n")
print("schedule.json updated: next_full_cycle_after =", sched["next_full_cycle_after"])

# 3. Append to journal/cycles.log
now_iso = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log_line = (
    f"{now_iso} cycle done: settled 0, placed 0, cash $925.60 "
    f"(FULL, oracle-gemini, paper; CI status unknown; resolve 0 bets / 0 forecasts settled; "
    f"prepared 300 in 15 batches under reports/screener-work/20261109T141225Z, unscreened fallback under Argon-Pro Protocol to preserve Gemini daily RPD budget; "
    f"researched 6 candidates across CPI, commodities, metals, and tech product releases, recorded 6 forecasts: "
    f"WTI close >85 Nov 9 0.85 market-agrees, WTI close >87 Nov 10 0.50 wide-spread-veto spread 0.08, "
    f"Natural Gas High 3.50 wk Nov 9 0.18 wide-spread-veto spread 0.11, Silver Low 49 wk Nov 9 0.20 market-agrees, "
    f"Anthropic IPO Nov 20 0.53 market-agrees, Oct Core CPI MoM 0.1% 0.10 wide-spread-veto spread 0.13; "
    f"monitor: 3 open bets (Sweden PM No, NYC home value Jan27, UK Q3 GDP Nov13), no action; "
    f"next_full_cycle_after 2026-11-09T20:00:00Z; gemini-3.8-flash)\n"
)

log_path = ROOT / "journal" / "cycles.log"
with open(log_path, "a") as f:
    f.write(log_line)
print("journal/cycles.log appended:", log_line.strip())
