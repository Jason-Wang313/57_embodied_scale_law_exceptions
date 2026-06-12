import csv, re, math
from pathlib import Path
root = Path(r'C:\Users\wangz\robotics_60_paper_batch\57_embodied_scale_law_exceptions')
docs = root / 'docs'
rows = []
with (docs / 'crossref_seed.csv').open(encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        rows.append(r)
patterns = {
    'scaling': [r'\bscal', r'scaling law', r'scale law', r'power law', r'law of scaling'],
    'robot_foundation': [r'foundation model', r'generalist', r'robot policy', r'robotics'],
    'embodied': [r'embodied', r'embodiment', r'physical ai', r'physical intelligence'],
    'manipulation': [r'manipulation', r'grasp', r'contact', r'pick and place', r'dexter'],
    'world_model': [r'world model', r'latent dynamics', r'predictive model', r'model-based', r'dynamics model'],
    'policy_learning': [r'imitation', r'behavior cloning', r'policy', r'control', r'planning'],
    'multimodal': [r'vision-language', r'vlm', r'multimodal', r'tactile', r'3d', r'point cloud', r'sensor'],
}
for r in rows:
    text = f"{r['title']} {r['abstract']} {r['venue']}".lower()
    score = 0
    hits = []
    for cat, pats in patterns.items():
        c = sum(bool(re.search(p, text)) for p in pats)
        if c:
            hits.append(cat)
            score += c
    if re.search(r'scaling|scale', text): score += 2
    if re.search(r'robot|embod|manipulation|locomotion|control|policy|world model', text): score += 2
    if re.search(r'foundation|generalist|multimodal|tactile|contact|sim-to-real|transfer', text): score += 1
    year = int(r['year']) if r['year'] and str(r['year']).isdigit() else 0
    if year >= 2023: score += 1
    if year >= 2024: score += 1
    r['score'] = str(score)
    r['tags'] = '|'.join(sorted(set(hits)))
rows.sort(key=lambda x: (-int(x['score']), -(int(x['year']) if x['year'] and str(x['year']).isdigit() else 0), x['title'].lower()))
# write matrix with top 1500
out = docs / 'related_work_matrix.csv'
fields = ['rank','score','year','tags','query','title','venue','doi','url','type','abstract']
with out.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for i, r in enumerate(rows[:1500], 1):
        w.writerow({'rank': i, **{k: r.get(k,'') for k in fields if k!='rank'}})
print('wrote', out, 'rows', len(rows[:1500]))
# shortlist candidates
for name, n in [('serious_skim.csv',300), ('deep_read.csv',240), ('hostile_prior.csv',100)]:
    with (docs / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(rows[:n], 1):
            w.writerow({'rank': i, **{k: r.get(k,'') for k in fields if k!='rank'}})
    print(name, n)
