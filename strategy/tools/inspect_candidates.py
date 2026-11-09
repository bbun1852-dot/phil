import json, sys, glob

work_dir = sys.argv[1] if len(sys.argv) > 1 else "reports/screener-work/20261109T031156Z"
start_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 5
end_idx = int(sys.argv[3]) if len(sys.argv) > 3 else 15

for b in sorted(glob.glob(f"{work_dir}/batch-*.json"))[start_idx:end_idx]:
    with open(b) as f:
        data = json.load(f)
    print(f"=== {b} ===")
    for m in data['markets']:
        m_id = m.get('id') or m.get('market_id') or m.get('id_')
        mid = data.get('mids', {}).get(m_id, {})
        print(f"ID: {m_id} | Title: {m.get('question')} | Out: {m.get('outcomes')} | End: {m.get('endDate')} | Mid: {mid}")
