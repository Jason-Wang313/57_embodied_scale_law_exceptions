import csv, re
from pathlib import Path
root = Path(r'C:\Users\wangz\robotics_60_paper_batch\57_embodied_scale_law_exceptions')
docs = root / 'docs'
rows = []
with (docs / 'crossref_seed.csv').open(encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        rows.append(r)
keep_terms = re.compile(r'(robot|robotic|embod|manipulation|grasp|locomotion|control|policy|action|tactile|sim-to-real|world model|foundation model|vision-language|vision language|multimodal|embodied intelligence|physical ai|humanoid|drone|aerial|navigation|planning|imitation learning|reinforcement learning|learning from demonstration)', re.I)
score_terms = {
    'scaling': re.compile(r'(scal|power law|data scaling|model scaling|size scaling)', re.I),
    'foundation': re.compile(r'(foundation model|generalist|vla|robot foundation)', re.I),
    'contact': re.compile(r'(contact|force|tactile|dexter|friction)', re.I),
    'world': re.compile(r'(world model|latent dynamics|dynamics model|predictive model)', re.I),
    'embodied': re.compile(r'(embod|physical ai|embodied intelligence)', re.I),
    'transfer': re.compile(r'(sim-to-real|transfer|generalization|zero-shot|out-of-distribution)', re.I),
}
filtered = []
for r in rows:
    text = f"{r['title']} {r['abstract']} {r['venue']}"
    if not keep_terms.search(text):
        continue
    score = 0
    for k,p in score_terms.items():
        if p.search(text):
            score += 2
    if re.search(r'robot|robotic|embod|manipulation|control|policy|action', text, re.I):
        score += 2
    if re.search(r'2025|2026', r['year'] or ''):
        score += 1
    year = int(r['year']) if r['year'] and str(r['year']).isdigit() else 0
    filtered.append({**r, 'score': str(score), 'tags': ''})
filtered.sort(key=lambda x: (-int(x['score']), -(int(x['year']) if x['year'] and str(x['year']).isdigit() else 0), x['title'].lower()))
fields = ['rank','score','year','tags','query','title','venue','doi','url','type','abstract']
out = docs / 'related_work_matrix.csv'
with out.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for i, r in enumerate(filtered[:1500], 1):
        w.writerow({'rank': i, **{k: r.get(k,'') for k in fields if k!='rank'}})
print('filtered rows', len(filtered))
for name, n in [('serious_skim.csv',300), ('deep_read.csv',240), ('hostile_prior.csv',100)]:
    with (docs / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(filtered[:n], 1):
            w.writerow({'rank': i, **{k: r.get(k,'') for k in fields if k!='rank'}})
print('done')
