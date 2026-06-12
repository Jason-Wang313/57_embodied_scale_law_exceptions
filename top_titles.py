import csv
from pathlib import Path
root = Path(r'C:\Users\wangz\robotics_60_paper_batch\57_embodied_scale_law_exceptions')
with (root/'docs'/'related_work_matrix.csv').open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
for i,r in enumerate(rows[:40],1):
    print(i, r['year'], r['title'])
