import csv, json, os, re, sys, time
from pathlib import Path
from urllib.parse import quote
import requests

root = Path(r'C:\Users\wangz\robotics_60_paper_batch\57_embodied_scale_law_exceptions')
docs = root / 'docs'
docs.mkdir(exist_ok=True)
queries = [
    'robotics scaling law', 'robot foundation model', 'embodied intelligence scaling',
    'robot manipulation scaling', 'robot world model', 'imitation learning robotics',
    'robot locomotion scaling', 'sim-to-real robotics', 'contact-rich manipulation',
    'robot policy foundation model', 'embodiment generalization robotics',
    'vision language action robotics', 'multimodal robot learning', 'robot grasping learning',
    'robot planning learning', 'robot control learning', 'robot tactile perception',
    'robot 3D perception', 'robot reinforcement learning', 'robot self-supervised learning'
]
headers = {'User-Agent': 'codex-paper-batch/1.0 (mailto:example@example.com)'}
rows = []
seen = set()
for qi, q in enumerate(queries, 1):
    for off in range(0, 200, 100):
        url = f'https://api.crossref.org/works?query.title={quote(q)}&rows=100&offset={off}&select=DOI,title,author,issued,container-title,type,URL,abstract'
        try:
            r = requests.get(url, headers=headers, timeout=30)
            data = r.json()['message']['items']
        except Exception as e:
            print(f'query fail {q} off {off}: {e}')
            continue
        for item in data:
            title = ' '.join(item.get('title') or []).strip()
            doi = (item.get('DOI') or '').lower().strip()
            if not title:
                continue
            key = doi or title.lower()
            if key in seen:
                continue
            seen.add(key)
            year = None
            issued = item.get('issued', {}).get('date-parts', [[None]])[0][0]
            year = issued
            venue = ' '.join(item.get('container-title') or []).strip()
            rows.append({
                'query': q,
                'title': title,
                'year': year,
                'venue': venue,
                'doi': item.get('DOI',''),
                'url': item.get('URL',''),
                'type': item.get('type',''),
                'abstract': (item.get('abstract') or '')[:500],
            })
        time.sleep(0.2)
print('rows', len(rows))
out = docs / 'crossref_seed.csv'
with out.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['query','title','year','venue','doi','url','type','abstract'])
    w.writeheader(); w.writerows(rows)
print(out)
