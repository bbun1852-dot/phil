import json

def check_funnel():
    print("--- Funnel rows in window (Nov 3 - Nov 6) ---")
    with open("strategy/funnel.jsonl") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            cycle = row.get("cycle", "")
            if cycle >= "2026-11-03":
                print(f"Cycle: {cycle} | Type: {row.get('tick_type')} | Settled: {row.get('settled')} | Placed: {row.get('placed')} | Runner: {row.get('runner')}")

if __name__ == "__main__":
    check_funnel()
