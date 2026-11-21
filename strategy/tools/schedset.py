#!/usr/bin/env python3
"""Set the pacing pointer in strategy/schedule.json (one-line reason).

Usage: python3 strategy/tools/schedset.py --next 2026-11-21T12:05:00Z \
           --reason "Set by 10:13Z FULL Nov21 (operator): ..."

Why (2026-11-21 10:1xZ FULL): the `reason` field had grown to ~40KB of
chained PREVIOUS history, against the DEEP-2026-09-15 one-line rule, and
every tick reads it. Cycle logs said "scripted JSON rewrite was not
permitted this session" (ad-hoc python -c is blocked; Edit cannot match a
40KB line). This tool REPLACES the reason; history lives in git
(`git log -p strategy/schedule.json`). Other keys are left untouched.
"""
import argparse
import json
import os
import re
import sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schedule.json")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--next", required=True, help="ISO UTC, e.g. 2026-11-21T12:05:00Z")
    ap.add_argument("--reason", required=True)
    a = ap.parse_args(argv)
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", a.next):
        sys.exit("--next must look like 2026-11-21T12:05:00Z")
    if len(a.reason) > 1200:
        sys.exit("--reason over 1200 chars: keep it to one line; history is in git")
    with open(PATH) as f:
        d = json.load(f)
    old = len(json.dumps(d.get("reason", "")))
    d["next_full_cycle_after"] = a.next
    d["reason"] = a.reason
    with open(PATH, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    print(json.dumps({"next_full_cycle_after": a.next, "reason_chars_before": old,
                      "reason_chars_after": len(a.reason)}))


if __name__ == "__main__":
    main(sys.argv[1:])
