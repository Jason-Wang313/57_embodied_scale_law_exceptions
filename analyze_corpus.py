import csv, re, json
from collections import Counter, defaultdict
from pathlib import Path
root = Path(r'C:\Users\wangz\robotics_60_paper_batch\57_embodied_scale_law_exceptions')
docs = root / 'docs'
rows=[]
with (docs/'related_work_matrix.csv').open(encoding='utf-8', newline='') as f:
    rows=list(csv.DictReader(f))
cat_patterns={
 'scale_positive': re.compile(r'(scal|power law|generalization|zero-shot|more data|more embodiments|more compute)', re.I),
 'contact_rich': re.compile(r'(contact|tactile|force|grasp|dexter|friction)', re.I),
 'safety': re.compile(r'(safe|safety|risk|constraint|robust)', re.I),
 'morphology': re.compile(r'(embodiment|morpholog|locomotion|humanoid|quadruped|hexapod)', re.I),
 'world_model': re.compile(r'(world model|dynamics|predictive|latent)', re.I),
}
counts=Counter(); overlap=defaultdict(int)
for r in rows:
    text=f"{r['title']} {r['abstract']}"
    hits=[k for k,p in cat_patterns.items() if p.search(text)]
    for h in hits: counts[h]+=1
    for h in hits:
        for h2 in hits:
            if h<=h2: overlap[(h,h2)]+=1
summary={
 'total_rows': len(rows),
 'counts': counts,
 'top_titles': [r['title'] for r in rows[:25]],
 'top_years': Counter(r['year'] for r in rows[:200]),
}
(docs/'corpus_analysis.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2)[:2000])
